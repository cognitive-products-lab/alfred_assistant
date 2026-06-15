"""
PROJECT      : ALFRED
BLOCK        : B11 -- Intelligence Cognitive
FUNCTION     : 11.03.001 -> 11.03.004
FILE         : src/v3/fusion/contradiction_detector.py
ROLE         : Detection contradictions entre signaux cognitifs

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-05-14
UPDATED      : 2026-05-14
VERSION      : V1.0
STATUS       : VALIDATED

DESCRIPTION :
Detecteur de contradictions entre les signaux entrants.
Identifie les incoherences signal/comportement qui reduisent la fiabilite.
Ex : utilisateur dit "ca va" mais emotion detectee = distress.

Fonctions couvertes :
  11.03.001 Detection contradiction texte/emotion    OK V1
  11.03.002 Detection contradiction energie/contenu  OK V1
  11.03.003 Score incoherence                        OK V1
  11.03.004 Rapport contradictions                   OK V1
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional


# ============================================================
# Modele contradiction
# ============================================================

@dataclass
class Contradiction:
    """Represent une contradiction detectee."""
    type:        str    = ""           # ex: "emotion_text_mismatch"
    severity:    str    = "low"        # low / medium / high
    description: str    = ""
    signal_a:    str    = ""           # Premier signal en conflit
    signal_b:    str    = ""           # Second signal en conflit
    timestamp:   str    = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class ContradictionReport:
    """Rapport complet des contradictions detectees."""
    contradictions:   List[Contradiction] = field(default_factory=list)
    incoherence_score: float = 0.0   # 0.0 = coherent, 1.0 = tres incoherent
    has_critical:     bool   = False
    timestamp:        str    = field(default_factory=lambda: datetime.now().isoformat())


# ============================================================
# ContradictionDetector
# ============================================================

class ContradictionDetector:
    """
    Detecteur de contradictions inter-signaux ALFRED V3.

    Compare les signaux NLP, emotionnels et contextuels
    pour identifier les incoherences significatives.

    Usage :
        detector = ContradictionDetector()
        report = detector.analyze(
            text="ca va tres bien",
            emotion_signal={"emotion": "distress", "intensity": 0.9},
        )
    """

    # Paires de contradiction connues : (texte_keyword, emotion_detectee)
    _TEXT_EMOTION_PAIRS = [
        (["ca va", "bien", "super", "top", "genial"], {"distress", "stressed", "sad"}),
        (["fatiguee", "epuisee", "crevee"],           {"happy", "motivated"}),
        (["motivee", "on y va", "super"],             {"distress", "sad"}),
    ]

    def analyze(
        self,
        text:           str = "",
        emotion_signal: Optional[Dict] = None,
        context_signal: Optional[Dict] = None,
    ) -> ContradictionReport:
        """
        Analyse les contradictions entre signaux.

        Args:
            text           : Texte brut de l'utilisateur
            emotion_signal : Dict emotion (emotion, intensity, valence)
            context_signal : Dict contexte (energy_level, period, etc.)

        Returns:
            ContradictionReport avec liste contradictions et score incoherence
        """
        contradictions: List[Contradiction] = []
        text_lower = text.lower()

        # -- Contradiction texte / emotion --
        if emotion_signal:
            emotion = emotion_signal.get("emotion", "neutral")
            intensity = float(emotion_signal.get("intensity", 0.0))

            for positive_kws, negative_emotions in self._TEXT_EMOTION_PAIRS:
                if any(kw in text_lower for kw in positive_kws):
                    if emotion in negative_emotions and intensity >= 0.5:
                        contradictions.append(Contradiction(
                            type="emotion_text_mismatch",
                            severity="medium" if intensity < 0.8 else "high",
                            description=(
                                f"Texte positif mais emotion detectee = {emotion} "
                                f"(intensite {intensity:.1f})"
                            ),
                            signal_a=f"text:{text[:40]}",
                            signal_b=f"emotion:{emotion}",
                        ))

        # -- Contradiction energie / contenu --
        if context_signal and emotion_signal:
            energy = context_signal.get("energy_level", "medium")
            emotion = emotion_signal.get("emotion", "neutral")
            if energy == "high" and emotion in {"distress", "sad"}:
                contradictions.append(Contradiction(
                    type="energy_emotion_mismatch",
                    severity="low",
                    description=(
                        f"Energie context = high mais emotion = {emotion}"
                    ),
                    signal_a=f"context:energy={energy}",
                    signal_b=f"emotion:{emotion}",
                ))

        # -- Score incoherence --
        severity_weights = {"low": 0.2, "medium": 0.5, "high": 1.0}
        incoherence_sum = sum(severity_weights.get(c.severity, 0.0) for c in contradictions)
        incoherence_score = round(min(1.0, incoherence_sum / max(1.0, len(contradictions) * 1.5)), 3)

        has_critical = any(c.severity == "high" for c in contradictions)

        return ContradictionReport(
            contradictions    = contradictions,
            incoherence_score = incoherence_score,
            has_critical      = has_critical,
        )

    def has_contradictions(self, report: ContradictionReport) -> bool:
        """True si le rapport contient au moins une contradiction."""
        return len(report.contradictions) > 0

    def get_severity_summary(self, report: ContradictionReport) -> Dict[str, int]:
        """Compte les contradictions par niveau de severite."""
        counts = {"low": 0, "medium": 0, "high": 0}
        for c in report.contradictions:
            counts[c.severity] = counts.get(c.severity, 0) + 1
        return counts
