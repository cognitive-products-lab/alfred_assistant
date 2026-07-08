"""
════════════════════════════════════════════════════════════
PROJECT      : ALFRED
BLOCK        : B01 V2
FUNCTION     : 01.V2.03
FILE         : src/v2/decision/decision_engine.py
ROLE         : Moteur de décision contextuelle V2

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-06-01
UPDATED      : 2026-06-03
VERSION      : V1.0
STATUS       : VALIDATED

DESCRIPTION :
Sélectionne la stratégie de réponse optimale en combinant :
  - FusionResult  → qualité et sources du contexte
  - ConfidenceResult → niveau de confiance
  - Émotion détectée
  - Mode ALFRED actif
  - Historique récent (éviter la répétition)

Retourne un DecisionResult avec la stratégie choisie,
le paramétrage de la réponse (ton, longueur, hedge) et
les actions post-réponse recommandées.

Usage : brancher dans alfred_behavior_engine.py (V2),
appelé après FusionEngine et ConfidenceScorer.
════════════════════════════════════════════════════════════
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


# ─── Stratégies ───────────────────────────────────────────────────────────────

class ResponseStrategy(str, Enum):
    DIRECT       = "direct"        # réponse directe, confiance haute
    EMPATHETIC   = "empathetic"    # priorité à l'écoute émotionnelle
    EXPLORATORY  = "exploratory"   # question de clarification
    FALLBACK_LLM = "fallback_llm"  # déléguer au LLM sans contexte enrichi
    KNOWLEDGE    = "knowledge"     # réponse basée sur la base de connaissances
    MEMORY       = "memory"        # réponse depuis la mémoire personnelle
    HEDGED       = "hedged"        # réponse avec couverture explicite de doute
    PROACTIVE    = "proactive"     # suggestion proactive (non sollicitée)


# ─── Types ────────────────────────────────────────────────────────────────────

@dataclass
class DecisionResult:
    """Résultat de la décision contextuelle."""
    strategy:         ResponseStrategy
    tone:             str        # "warm" | "neutral" | "precise" | "playful"
    max_length:       int        # longueur cible réponse (caractères)
    should_hedge:     bool
    hedge_prefix:     str
    post_actions:     list[str]  # ex: ["save_to_memory", "trigger_proactive"]
    rationale:        str        # explication de la décision (debug)
    metadata:         dict = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "strategy": self.strategy.value,
            "tone": self.tone,
            "max_length": self.max_length,
            "should_hedge": self.should_hedge,
            "post_actions": self.post_actions,
        }


# ─── Règles de décision ───────────────────────────────────────────────────────

_TONE_BY_MODE = {
    "support":    "warm",
    "complicite": "playful",
    "focus":      "precise",
    "challenge":  "precise",
}

_LENGTH_BY_MODE = {
    "support":    600,
    "complicite": 400,
    "focus":      800,
    "challenge":  700,
}


class DecisionEngine:
    """
    Moteur de décision V2 — sélectionne la stratégie de réponse optimale.
    """

    def decide(
        self,
        confidence_score:   float = 0.5,
        confidence_level:   str   = "medium",
        fusion_score:       float = 0.5,
        primary_source:     str   = "llm",
        emotion:            str   = "neutral",
        mode:               str   = "complicite",
        user_message:       str   = "",
        has_memory:         bool  = False,
        has_knowledge:      bool  = False,
        is_question:        bool  = False,
        recent_strategies:  list[str] | None = None,
    ) -> DecisionResult:
        """
        Sélectionne la stratégie et les paramètres de réponse.

        Args:
            confidence_score  : score de confiance ConfidenceScorer (0–1)
            confidence_level  : "high" | "medium" | "low" | "uncertain"
            fusion_score      : score de fusion FusionEngine (0–1)
            primary_source    : source dominante ("memory" | "knowledge" | "llm")
            emotion           : émotion détectée
            mode              : mode ALFRED actif
            user_message      : texte du message utilisateur
            has_memory        : True si mémoire personnelle pertinente
            has_knowledge     : True si knowledge pertinent trouvé
            is_question       : True si le message est une question
            recent_strategies : stratégies utilisées récemment (éviter répétition)
        """
        recent = recent_strategies or []

        # ── Sélection stratégie ───────────────────────────────────────────────

        strategy, rationale = self._select_strategy(
            confidence_score, confidence_level, emotion, mode,
            has_memory, has_knowledge, is_question, primary_source, recent
        )

        # ── Paramètres ───────────────────────────────────────────────────────

        tone       = _TONE_BY_MODE.get(mode, "neutral")
        max_length = _LENGTH_BY_MODE.get(mode, 500)

        # Ajustements selon émotion
        if emotion in ("stressed", "sad", "anxious", "tired"):
            tone       = "warm"
            max_length = min(max_length, 400)   # réponses courtes en détresse

        should_hedge = confidence_level in ("low", "uncertain")
        hedge_prefix = (
            "Je manque d'informations précises, mais je pense que "
            if confidence_level == "uncertain"
            else "Je ne suis pas certain·e, mais "
            if confidence_level == "low"
            else ""
        )

        # ── Actions post-réponse ─────────────────────────────────────────────

        post_actions = self._post_actions(
            strategy, has_memory, has_knowledge, confidence_score, emotion
        )

        return DecisionResult(
            strategy=strategy,
            tone=tone,
            max_length=max_length,
            should_hedge=should_hedge,
            hedge_prefix=hedge_prefix,
            post_actions=post_actions,
            rationale=rationale,
            metadata={
                "confidence_score": confidence_score,
                "fusion_score": fusion_score,
                "emotion": emotion,
                "mode": mode,
            },
        )

    def _select_strategy(
        self,
        confidence: float,
        level: str,
        emotion: str,
        mode: str,
        has_memory: bool,
        has_knowledge: bool,
        is_question: bool,
        primary_source: str,
        recent: list[str],
    ) -> tuple[ResponseStrategy, str]:
        """Règles de sélection de stratégie (priorité décroissante)."""

        # Détresse émotionnelle → empathie avant tout
        if emotion in ("stressed", "sad", "anxious") and mode == "support":
            return ResponseStrategy.EMPATHETIC, "Détresse émotionnelle détectée en mode support"

        # Confiance très faible → question de clarification
        if level == "uncertain" and is_question and "exploratory" not in recent:
            return ResponseStrategy.EXPLORATORY, "Confiance très faible + question → clarification"

        # Confiance basse → réponse avec couverture
        if level in ("low", "uncertain"):
            return ResponseStrategy.HEDGED, f"Confiance {level} → hedge explicite"

        # Mémoire personnelle dominante
        if primary_source == "memory" and has_memory and confidence >= 0.6:
            return ResponseStrategy.MEMORY, "Source mémoire dominante, confiance suffisante"

        # Knowledge dominant + focus/challenge
        if has_knowledge and mode in ("focus", "challenge") and confidence >= 0.5:
            return ResponseStrategy.KNOWLEDGE, "Knowledge pertinent + mode expert"

        # Confiance haute → direct
        if confidence >= 0.7:
            return ResponseStrategy.DIRECT, "Confiance haute → réponse directe"

        # Fallback LLM
        return ResponseStrategy.FALLBACK_LLM, "Pas de source dominante → LLM direct"

    def _post_actions(
        self,
        strategy: ResponseStrategy,
        has_memory: bool,
        has_knowledge: bool,
        confidence: float,
        emotion: str,
    ) -> list[str]:
        """Actions recommandées après la réponse."""
        actions = []

        # Mémoriser si la réponse est de qualité
        if confidence >= 0.6:
            actions.append("save_to_memory")

        # Déclencher proactif après réponse directe de qualité
        if strategy == ResponseStrategy.DIRECT and confidence >= 0.7:
            actions.append("trigger_proactive")

        # Tracker l'émotion pour le wellbeing
        if emotion in ("stressed", "sad", "anxious", "tired"):
            actions.append("track_wellbeing")

        return actions


# ─── Singleton ────────────────────────────────────────────────────────────────

_engine: DecisionEngine | None = None


def get_decision_engine() -> DecisionEngine:
    global _engine
    if _engine is None:
        _engine = DecisionEngine()
    return _engine


def reset_decision_engine() -> None:
    global _engine
    _engine = None
