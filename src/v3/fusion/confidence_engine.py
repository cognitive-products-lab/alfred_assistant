"""
PROJECT      : ALFRED
BLOCK        : B11 -- Intelligence Cognitive
FUNCTION     : 11.02.001 -> 11.02.005
FILE         : src/v3/fusion/confidence_engine.py
ROLE         : Moteur de confiance -- evaluation fiabilite signaux et decisions

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-05-14
UPDATED      : 2026-05-14
VERSION      : V1.0
STATUS       : TESTED

DESCRIPTION :
Moteur d'evaluation de confiance ALFRED V3.
Calcule la fiabilite d'une decision depuis les signaux disponibles.
Determine si ALFRED doit agir, attendre, ou demander clarification.

Fonctions couvertes :
  11.02.001 Score confiance global                  OK V1
  11.02.002 Seuils d'action (haut/moyen/bas)        OK V1
  11.02.003 Recommandation action selon confiance   OK V1
  11.02.004 Facteurs de confiance par source        OK V1
  11.02.005 Historique confiance session            OK V1
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional


# ============================================================
# Seuils de confiance
# ============================================================

CONFIDENCE_THRESHOLDS = {
    "high":   0.70,   # Action directe autorisee
    "medium": 0.40,   # Action avec prudence
    "low":    0.0,    # Clarification ou abstention
}


# ============================================================
# Modele decision confiance
# ============================================================

@dataclass
class ConfidenceDecision:
    """Decision basee sur l'evaluation de confiance."""
    score:       float  = 0.0
    level:       str    = "low"        # high / medium / low
    action:      str    = "clarify"    # act / proceed_cautiously / clarify / abstain
    explanation: str    = ""
    factors:     dict   = field(default_factory=dict)
    timestamp:   str    = field(default_factory=lambda: datetime.now().isoformat())


# ============================================================
# ConfidenceEngine
# ============================================================

class ConfidenceEngine:
    """
    Moteur d'evaluation de confiance ALFRED V3.

    Evalue la fiabilite des signaux entrants et determine
    le niveau d'action approprie (agir / proceder avec prudence / clarifier).

    Usage :
        engine = ConfidenceEngine()
        decision = engine.evaluate(fused_signal)
        if decision.action == "act":
            # Executer avec confiance
    """

    def __init__(self, thresholds: Optional[Dict[str, float]] = None):
        self.thresholds = thresholds or CONFIDENCE_THRESHOLDS.copy()
        self._history: List[ConfidenceDecision] = []

    # --------------------------------------------------------
    # Evaluation principale
    # --------------------------------------------------------

    def evaluate(self, fused_signal) -> ConfidenceDecision:
        """
        Evalue la confiance depuis un FusedSignal.

        Args:
            fused_signal : Instance de FusedSignal depuis MultiSignalFusionEngine

        Returns:
            ConfidenceDecision avec score, niveau et action recommandee
        """
        score = getattr(fused_signal, "confidence", 0.0)
        coherence = getattr(fused_signal, "coherence_score", 1.0)
        sources = getattr(fused_signal, "sources_used", [])

        # Penalite si peu de sources
        source_factor = min(1.0, len(sources) / 3.0)

        # Score ajuste
        adjusted_score = round(score * 0.6 + coherence * 0.3 + source_factor * 0.1, 3)

        level, action = self._resolve_action(adjusted_score)

        factors = {
            "raw_confidence":  score,
            "coherence":       coherence,
            "sources_count":   len(sources),
            "source_factor":   round(source_factor, 3),
            "adjusted_score":  adjusted_score,
        }

        explanation = self._build_explanation(level, action, factors)

        decision = ConfidenceDecision(
            score       = adjusted_score,
            level       = level,
            action      = action,
            explanation = explanation,
            factors     = factors,
        )
        self._history.append(decision)
        return decision

    def evaluate_from_score(self, score: float, coherence: float = 1.0) -> ConfidenceDecision:
        """
        Evalue directement depuis un score numerique.

        Args:
            score     : Score de confiance brut (0.0 -> 1.0)
            coherence : Score de coherence des signaux

        Returns:
            ConfidenceDecision
        """
        adjusted = round(score * 0.7 + coherence * 0.3, 3)
        level, action = self._resolve_action(adjusted)
        decision = ConfidenceDecision(
            score       = adjusted,
            level       = level,
            action      = action,
            explanation = self._build_explanation(level, action, {}),
        )
        self._history.append(decision)
        return decision

    # --------------------------------------------------------
    # Resolution action
    # --------------------------------------------------------

    def _resolve_action(self, score: float) -> tuple[str, str]:
        """Determine le niveau et l'action depuis le score."""
        if score >= self.thresholds["high"]:
            return "high", "act"
        elif score >= self.thresholds["medium"]:
            return "medium", "proceed_cautiously"
        else:
            return "low", "clarify"

    def _build_explanation(self, level: str, action: str, factors: dict) -> str:
        explanations = {
            "act":                 "Confiance elevee -- action directe recommandee.",
            "proceed_cautiously":  "Confiance moderee -- proceder avec prudence.",
            "clarify":             "Confiance insuffisante -- demander clarification.",
            "abstain":             "Confiance trop faible -- abstention recommandee.",
        }
        return explanations.get(action, "Evaluation en cours.")

    # --------------------------------------------------------
    # Utilitaires
    # --------------------------------------------------------

    def is_high_confidence(self, score: float) -> bool:
        return score >= self.thresholds["high"]

    def is_low_confidence(self, score: float) -> bool:
        return score < self.thresholds["medium"]

    def get_history(self, n: int = 10) -> List[ConfidenceDecision]:
        return self._history[-n:]

    def clear_history(self) -> None:
        self._history = []

    def status(self) -> dict:
        return {
            "thresholds":    self.thresholds,
            "history_count": len(self._history),
            "version":       "confidence_v1",
        }
