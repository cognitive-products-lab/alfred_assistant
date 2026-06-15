"""
PROJECT      : ALFRED
BLOCK        : B11 -- Intelligence Cognitive
FUNCTION     : 11.04.001 -> 11.04.006
FILE         : src/v3/proactive/proactive_engine.py
ROLE         : Moteur proactif -- declenchement suggestions sans sollicitation

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-05-14
UPDATED      : 2026-05-14
VERSION      : V1.0
STATUS       : VALIDATED

DESCRIPTION :
Moteur proactif ALFRED V3.
Analyse le contexte et l'etat utilisateur pour declencher des suggestions
pertinentes sans attendre que l'utilisateur demande explicitement.

Ethique : ALFRED ne relance jamais de maniere intrusive.
La proactivite est toujours optionnelle et silencieuse si non souhaitee.

Fonctions couvertes :
  11.04.001 Detection opportunite proactive          OK V1
  11.04.002 Generation suggestion contextuelle       OK V1
  11.04.003 Filtre anti-intrusion                    OK V1
  11.04.004 Historique suggestions emises            OK V1
  11.04.005 Cooldown entre suggestions               OK V1
  11.04.006 Statut moteur proactif                   OK V1
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any


# ============================================================
# Constantes
# ============================================================

DEFAULT_COOLDOWN_MINUTES = 15   # Delai minimum entre 2 suggestions
MAX_SUGGESTIONS_PER_SESSION = 10


# ============================================================
# Modele suggestion proactive
# ============================================================

@dataclass
class ProactiveSuggestion:
    """Une suggestion proactive generee par ALFRED."""
    trigger:     str   = ""          # Ce qui a declenche la suggestion
    content:     str   = ""          # Texte de la suggestion
    category:    str   = "general"   # wellbeing / task / memory / context
    priority:    int   = 1           # 1 (bas) -> 5 (urgent)
    can_dismiss: bool  = True        # L'utilisateur peut ignorer
    timestamp:   str   = field(default_factory=lambda: datetime.now().isoformat())


# ============================================================
# ProactiveEngine
# ============================================================

class ProactiveEngine:
    """
    Moteur proactif ALFRED V3.

    Genere des suggestions contextuelles au bon moment.
    Respecte le cooldown et la limite de suggestions par session.

    Usage :
        engine = ProactiveEngine()
        suggestion = engine.check_and_suggest(
            context_signal=context,
            emotion_signal=emotion,
            wellbeing_state=wellbeing,
        )
        if suggestion:
            display(suggestion.content)
    """

    def __init__(
        self,
        cooldown_minutes: int = DEFAULT_COOLDOWN_MINUTES,
        max_suggestions:  int = MAX_SUGGESTIONS_PER_SESSION,
        enabled:          bool = True,
    ):
        self.cooldown_minutes = cooldown_minutes
        self.max_suggestions  = max_suggestions
        self.enabled          = enabled

        self._history:    List[ProactiveSuggestion] = []
        self._last_sent:  Optional[datetime] = None

    # --------------------------------------------------------
    # Verification et suggestion
    # --------------------------------------------------------

    def check_and_suggest(
        self,
        context_signal:  Optional[Dict[str, Any]] = None,
        emotion_signal:  Optional[Dict[str, Any]] = None,
        wellbeing_state: Optional[Any] = None,
    ) -> Optional[ProactiveSuggestion]:
        """
        Verifie si une suggestion proactive est appropriee.

        Args:
            context_signal  : Contexte session (energy_level, period, etc.)
            emotion_signal  : Etat emotionnel detecte
            wellbeing_state : WellbeingState depuis wellbeing_tracker

        Returns:
            ProactiveSuggestion si une suggestion est pertinente, None sinon
        """
        if not self.enabled:
            return None

        if not self._can_suggest():
            return None

        # Evaluer par priorite : wellbeing > emotion > contexte
        suggestion = (
            self._check_wellbeing(wellbeing_state) or
            self._check_emotion(emotion_signal) or
            self._check_context(context_signal)
        )

        if suggestion:
            self._record(suggestion)

        return suggestion

    def _can_suggest(self) -> bool:
        """Verifie cooldown et limite session."""
        if len(self._history) >= self.max_suggestions:
            return False
        if self._last_sent is None:
            return True
        elapsed = datetime.now() - self._last_sent
        return elapsed >= timedelta(minutes=self.cooldown_minutes)

    # --------------------------------------------------------
    # Detecteurs specifiques
    # --------------------------------------------------------

    def _check_wellbeing(self, state) -> Optional[ProactiveSuggestion]:
        if state is None:
            return None
        fatigue = getattr(state, "fatigue_score", 0.0)
        flow    = getattr(state, "flow_detected", False)

        if fatigue >= 0.8:
            return ProactiveSuggestion(
                trigger  = "high_fatigue",
                content  = "Tu sembles tres fatiguee. Une pause de 10 minutes peut vraiment aider.",
                category = "wellbeing",
                priority = 4,
            )
        if flow:
            return ProactiveSuggestion(
                trigger  = "flow_state",
                content  = "Tu es dans le flow -- je reste discret pour ne pas te deranger.",
                category = "wellbeing",
                priority = 1,
            )
        return None

    def _check_emotion(self, emotion_signal: Optional[Dict]) -> Optional[ProactiveSuggestion]:
        if not emotion_signal:
            return None
        emotion   = emotion_signal.get("emotion", "neutral")
        intensity = float(emotion_signal.get("intensity", 0.0))

        if emotion in {"stressed", "sad"} and intensity >= 0.6:
            return ProactiveSuggestion(
                trigger  = f"emotion_{emotion}",
                content  = "Je sens que ce n'est pas facile en ce moment. Tu veux qu'on ralentisse ?",
                category = "wellbeing",
                priority = 3,
            )
        return None

    def _check_context(self, context_signal: Optional[Dict]) -> Optional[ProactiveSuggestion]:
        if not context_signal:
            return None
        period       = context_signal.get("period", "")
        energy_level = context_signal.get("energy_level", "medium")

        if period == "nuit" and energy_level == "low":
            return ProactiveSuggestion(
                trigger  = "late_night_low_energy",
                content  = "Il est tard et ton energie est basse. Un dernier point avant de terminer ?",
                category = "context",
                priority = 2,
            )
        return None

    # --------------------------------------------------------
    # Gestion suggestions forcees
    # --------------------------------------------------------

    def force_suggestion(self, content: str, category: str = "general") -> ProactiveSuggestion:
        """
        Force l'emission d'une suggestion (bypass cooldown).
        Utile pour les tests et les cas d'urgence.
        """
        suggestion = ProactiveSuggestion(
            trigger  = "forced",
            content  = content,
            category = category,
            priority = 5,
        )
        self._record(suggestion)
        return suggestion

    # --------------------------------------------------------
    # Utilitaires
    # --------------------------------------------------------

    def _record(self, suggestion: ProactiveSuggestion) -> None:
        self._history.append(suggestion)
        self._last_sent = datetime.now()

    def get_history(self, n: int = 10) -> List[ProactiveSuggestion]:
        return self._history[-n:]

    def clear_history(self) -> None:
        self._history = []
        self._last_sent = None

    def enable(self) -> None:
        self.enabled = True

    def disable(self) -> None:
        self.enabled = False

    def status(self) -> dict:
        return {
            "enabled":          self.enabled,
            "cooldown_minutes": self.cooldown_minutes,
            "max_suggestions":  self.max_suggestions,
            "suggestions_sent": len(self._history),
            "last_sent":        self._last_sent.isoformat() if self._last_sent else None,
            "version":          "proactive_v1",
        }
