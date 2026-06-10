"""
PROJECT      : ALFRED
BLOCK        : B11 -- Intelligence Cognitive
FUNCTION     : 11.01.001 -> 11.01.006
FILE         : src/v3/fusion/multi_signal_fusion_engine.py
ROLE         : Fusion multi-signaux -- agregation NLP + emotion + contexte + memoire

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-05-14
UPDATED      : 2026-05-14
VERSION      : V1.0
STATUS       : TESTED

DESCRIPTION :
Moteur de fusion multi-signaux ALFRED V3.
Combine les sorties des differents capteurs cognitifs en un signal unifie :
  - Signal NLP (intent, entities, language)
  - Signal emotionnel (emotion, intensity, valence)
  - Signal contextuel (heure, energie, conversation stage)
  - Signal memoire (recent exchanges, relevance)

Fonctions couvertes :
  11.01.001 Fusion signal NLP + emotion              OK V1
  11.01.002 Ponderation signaux selon confiance      OK V1
  11.01.003 Score coherence globale                  OK V1
  11.01.004 Signal fusionne -> decision mode          OK V1
  11.01.005 Historique signaux fusion                OK V1
  11.01.006 Export signal pour confidence_engine     OK V1
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional


# ============================================================
# Modele signal fusionne
# ============================================================

@dataclass
class FusedSignal:
    """Resultat de la fusion multi-signaux."""
    intent:          str   = "general"
    dominant_emotion: str  = "neutral"
    emotion_intensity: float = 0.0
    energy_level:    str   = "medium"
    confidence:      float = 0.0
    recommended_mode: str  = "focus"
    coherence_score: float = 1.0
    sources_used:    list  = field(default_factory=list)
    timestamp:       str   = field(default_factory=lambda: datetime.now().isoformat())
    method:          str   = "fusion_v1"


# ============================================================
# Poids de fusion par defaut
# ============================================================

_DEFAULT_WEIGHTS = {
    "nlp":      0.35,
    "emotion":  0.30,
    "context":  0.20,
    "memory":   0.15,
}

# Correspondance emotion -> mode
_EMOTION_TO_MODE = {
    "distress":  "support",
    "stressed":  "support",
    "sad":       "support",
    "tired":     "support",
    "confused":  "support",
    "motivated": "challenge",
    "happy":     "complicite",
    "focused":   "focus",
    "curious":   "complicite",
    "neutral":   "focus",
}

# Correspondance intent -> mode
_INTENT_TO_MODE = {
    "emotional_support": "support",
    "wellbeing":         "support",
    "greeting":          "complicite",
    "engineering":       "focus",
    "knowledge_request": "focus",
    "task":              "focus",
    "question":          "focus",
    "product_knowledge": "challenge",
}


# ============================================================
# MultiSignalFusionEngine
# ============================================================

class MultiSignalFusionEngine:
    """
    Moteur de fusion multi-signaux ALFRED V3.

    Fusionne les signaux NLP, emotionnels, contextuels et memoire
    pour produire un signal unifie avec recommandation de mode.

    Usage :
        engine = MultiSignalFusionEngine()
        signal = engine.fuse(nlp_signal, emotion_signal, context_signal)
        mode = signal.recommended_mode
    """

    def __init__(self, weights: Optional[Dict[str, float]] = None):
        """
        Args:
            weights : Poids de fusion {nlp, emotion, context, memory}.
                      Utilise les poids par defaut si None.
        """
        self.weights = weights or _DEFAULT_WEIGHTS.copy()
        self._history: List[FusedSignal] = []

    # --------------------------------------------------------
    # Fusion principale
    # --------------------------------------------------------

    def fuse(
        self,
        nlp_signal:     Optional[Dict[str, Any]] = None,
        emotion_signal: Optional[Dict[str, Any]] = None,
        context_signal: Optional[Dict[str, Any]] = None,
        memory_signal:  Optional[Dict[str, Any]] = None,
    ) -> FusedSignal:
        """
        Fusionne les signaux disponibles en un signal unifie.

        Args:
            nlp_signal     : Resultat de analyze_v2() -- intent, confidence, etc.
            emotion_signal : Resultat de detect_emotion() -- emotion, intensity, valence
            context_signal : Resultat de build_context() -- energy_level, period, etc.
            memory_signal  : Dict avec recent_context, relevance_score

        Returns:
            FusedSignal avec mode recommande et scores
        """
        sources_used = []
        confidence_sum = 0.0
        weight_sum = 0.0

        # -- Signal NLP --
        intent = "general"
        nlp_confidence = 0.0
        if nlp_signal:
            intent = nlp_signal.get("intent", "general")
            nlp_confidence = float(nlp_signal.get("confidence", 0.0))
            confidence_sum += nlp_confidence * self.weights.get("nlp", 0.35)
            weight_sum += self.weights.get("nlp", 0.35)
            sources_used.append("nlp")

        # -- Signal emotionnel --
        dominant_emotion = "neutral"
        emotion_intensity = 0.0
        if emotion_signal:
            dominant_emotion = emotion_signal.get("emotion", "neutral")
            emotion_intensity = float(emotion_signal.get("intensity", 0.0))
            emotion_confidence = min(1.0, emotion_intensity + 0.3)
            confidence_sum += emotion_confidence * self.weights.get("emotion", 0.30)
            weight_sum += self.weights.get("emotion", 0.30)
            sources_used.append("emotion")

        # -- Signal contextuel --
        energy_level = "medium"
        if context_signal:
            energy_level = context_signal.get("energy_level", "medium")
            ctx_confidence = {"high": 0.8, "medium": 0.5, "low": 0.3}.get(energy_level, 0.5)
            confidence_sum += ctx_confidence * self.weights.get("context", 0.20)
            weight_sum += self.weights.get("context", 0.20)
            sources_used.append("context")

        # -- Signal memoire --
        if memory_signal:
            mem_relevance = float(memory_signal.get("relevance_score", 0.0))
            confidence_sum += mem_relevance * self.weights.get("memory", 0.15)
            weight_sum += self.weights.get("memory", 0.15)
            sources_used.append("memory")

        # -- Confiance globale --
        global_confidence = round(confidence_sum / max(weight_sum, 0.001), 3)

        # -- Recommandation mode --
        recommended_mode = self._resolve_mode(dominant_emotion, intent, energy_level)

        # -- Coherence --
        coherence = self._compute_coherence(dominant_emotion, intent, energy_level)

        fused = FusedSignal(
            intent           = intent,
            dominant_emotion = dominant_emotion,
            emotion_intensity = emotion_intensity,
            energy_level     = energy_level,
            confidence       = global_confidence,
            recommended_mode = recommended_mode,
            coherence_score  = coherence,
            sources_used     = sources_used,
        )
        self._history.append(fused)
        return fused

    # --------------------------------------------------------
    # Resolution mode
    # --------------------------------------------------------

    def _resolve_mode(self, emotion: str, intent: str, energy_level: str) -> str:
        """
        Determine le mode ALFRED recommande.
        Priorite : energie basse > emotion negative > intent.
        """
        # Energie basse -> toujours support
        if energy_level == "low":
            return "support"

        # Emotion negative dominante -> support
        if emotion in {"distress", "stressed", "sad", "tired", "confused"}:
            return _EMOTION_TO_MODE.get(emotion, "support")

        # Emotion positive -> mode selon emotion
        if emotion in _EMOTION_TO_MODE:
            return _EMOTION_TO_MODE[emotion]

        # Fallback intent
        return _INTENT_TO_MODE.get(intent, "focus")

    # --------------------------------------------------------
    # Score coherence
    # --------------------------------------------------------

    def _compute_coherence(
        self, emotion: str, intent: str, energy_level: str
    ) -> float:
        """
        Calcule un score de coherence entre signaux (0.0 -> 1.0).
        Coherence elevee = signaux concordants.
        """
        score = 1.0

        # Incoherence : energie haute + emotion negative severe
        if energy_level == "high" and emotion in {"distress", "stressed"}:
            score -= 0.3

        # Incoherence : intent task + emotion distress
        if intent in {"task", "engineering"} and emotion == "distress":
            score -= 0.4

        return round(max(0.0, score), 2)

    # --------------------------------------------------------
    # Historique
    # --------------------------------------------------------

    def get_history(self, n: int = 10) -> List[FusedSignal]:
        """Retourne les N derniers signaux fusionnes."""
        return self._history[-n:]

    def clear_history(self) -> None:
        """Vide l'historique."""
        self._history = []

    def status(self) -> Dict[str, Any]:
        """Retourne l'etat du moteur."""
        return {
            "weights":        self.weights,
            "history_count":  len(self._history),
            "version":        "fusion_v1",
        }
