"""
════════════════════════════════════════════════════════════
PROJECT      : ALFRED
BLOCK        : B01 V2
FUNCTION     : 01.V2.02
FILE         : src/v2/confidence/confidence_scorer.py
ROLE         : Score de confiance de réponse multi-sources V2

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-06-01
UPDATED      : 2026-06-03
VERSION      : V1.0
STATUS       : ACTIVE

DESCRIPTION :
Calcule un score de confiance (0–1) pour chaque réponse ALFRED
en combinant plusieurs signaux :
  - Qualité de la fusion (fusion_score)
  - Couverture mémoire (faits mémorisés vs question posée)
  - Pertinence knowledge (score du routeur)
  - Cohérence émotionnelle (mode actuel vs émotion détectée)
  - Longueur et structure de la réponse

Usage : brancher dans response_generator.py (V2).
La confidence est transmise dans le dict de réponse
pour adapter le ton (doute explicite si confidence < 0.4).
════════════════════════════════════════════════════════════
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


# ─── Types ────────────────────────────────────────────────────────────────────

@dataclass
class ConfidenceSignal:
    """Un signal contribuant au score de confiance."""
    name:    str
    value:   float        # 0–1
    weight:  float = 1.0
    details: dict = field(default_factory=dict)


@dataclass
class ConfidenceResult:
    """Résultat du scoring de confiance."""
    score:          float          # 0–1 score global
    level:          str            # "high" | "medium" | "low" | "uncertain"
    signals:        list[ConfidenceSignal]
    dominant:       str            # signal dominant
    should_hedge:   bool           # True si ALFRED doit exprimer un doute
    hedge_phrase:   str            # phrase de couverture suggérée
    metadata:       dict = field(default_factory=dict)

    @property
    def is_confident(self) -> bool:
        return self.score >= 0.6

    def to_dict(self) -> dict[str, Any]:
        return {
            "score": self.score,
            "level": self.level,
            "should_hedge": self.should_hedge,
            "dominant": self.dominant,
        }


# ─── Phrases de couverture par niveau ────────────────────────────────────────

_HEDGE_PHRASES = {
    "low":       "Je ne suis pas certain·e de cette réponse, mais voici ce que je sais : ",
    "uncertain": "Je manque d'informations précises sur ce sujet, mais je pense que ",
    "medium":    "",   # pas de hedge pour medium
    "high":      "",   # pas de hedge pour high
}


# ─── Moteur de scoring ────────────────────────────────────────────────────────

class ConfidenceScorer:
    """
    Calcule le score de confiance d'une réponse ALFRED.

    Signaux disponibles :
      fusion_quality     : score de fusion (depuis FusionResult.fusion_score)
      memory_coverage    : présence de faits mémorisés pertinents (0/1)
      knowledge_coverage : pertinence du knowledge récupéré (0–1)
      emotion_alignment  : cohérence mode/émotion (0–1)
      response_quality   : qualité structurelle de la réponse (0–1)
    """

    _SIGNAL_WEIGHTS = {
        "fusion_quality":     0.30,
        "memory_coverage":    0.25,
        "knowledge_coverage": 0.25,
        "emotion_alignment":  0.10,
        "response_quality":   0.10,
    }

    _THRESHOLDS = {"high": 0.70, "medium": 0.45, "low": 0.25}

    def score(
        self,
        fusion_score:        float = 0.0,
        memory_coverage:     float = 0.0,
        knowledge_coverage:  float = 0.0,
        emotion:             str   = "neutral",
        mode:                str   = "complicite",
        response_text:       str   = "",
    ) -> ConfidenceResult:
        """
        Calcule le score de confiance global.

        Args:
            fusion_score       : score de FusionEngine (0–1)
            memory_coverage    : 1.0 si mémoire pertinente, 0.0 sinon
            knowledge_coverage : pertinence knowledge (0–1)
            emotion            : émotion détectée dans le message
            mode               : mode ALFRED actif
            response_text      : texte de la réponse générée
        """
        signals = [
            ConfidenceSignal(
                name="fusion_quality",
                value=float(min(1.0, max(0.0, fusion_score))),
                weight=self._SIGNAL_WEIGHTS["fusion_quality"],
            ),
            ConfidenceSignal(
                name="memory_coverage",
                value=float(min(1.0, max(0.0, memory_coverage))),
                weight=self._SIGNAL_WEIGHTS["memory_coverage"],
            ),
            ConfidenceSignal(
                name="knowledge_coverage",
                value=float(min(1.0, max(0.0, knowledge_coverage))),
                weight=self._SIGNAL_WEIGHTS["knowledge_coverage"],
            ),
            ConfidenceSignal(
                name="emotion_alignment",
                value=self._emotion_alignment(emotion, mode),
                weight=self._SIGNAL_WEIGHTS["emotion_alignment"],
                details={"emotion": emotion, "mode": mode},
            ),
            ConfidenceSignal(
                name="response_quality",
                value=self._response_quality(response_text),
                weight=self._SIGNAL_WEIGHTS["response_quality"],
                details={"length": len(response_text)},
            ),
        ]

        total_weight = sum(s.weight for s in signals)
        weighted_sum = sum(s.value * s.weight for s in signals)
        score = round(weighted_sum / total_weight, 3) if total_weight > 0 else 0.0

        level = self._level(score)
        dominant = max(signals, key=lambda s: s.value * s.weight).name
        should_hedge = score < self._THRESHOLDS["medium"]
        hedge_phrase = _HEDGE_PHRASES.get(level, "") if should_hedge else ""

        return ConfidenceResult(
            score=score,
            level=level,
            signals=signals,
            dominant=dominant,
            should_hedge=should_hedge,
            hedge_phrase=hedge_phrase,
            metadata={
                "total_weight": total_weight,
                "emotion": emotion,
                "mode": mode,
            },
        )

    def _emotion_alignment(self, emotion: str, mode: str) -> float:
        """Cohérence entre émotion détectée et mode ALFRED."""
        alignment_map = {
            ("stressed", "support"):    1.0,
            ("sad",      "support"):    1.0,
            ("anxious",  "support"):    1.0,
            ("happy",    "complicite"): 1.0,
            ("excited",  "challenge"):  1.0,
            ("focused",  "focus"):      1.0,
            ("neutral",  "complicite"): 0.8,
            ("neutral",  "focus"):      0.8,
        }
        # Alignement parfait connu
        if (emotion, mode) in alignment_map:
            return alignment_map[(emotion, mode)]
        # Désalignement fort
        if emotion in ("stressed", "sad") and mode in ("challenge", "focus"):
            return 0.3
        return 0.6  # alignement neutre par défaut

    def _response_quality(self, text: str) -> float:
        """Qualité structurelle de la réponse (longueur, ponctuation)."""
        if not text:
            return 0.0
        length = len(text)
        if length < 20:
            return 0.2
        if length < 80:
            return 0.5
        if length > 2000:
            return 0.7   # très long = risque de divagation
        return 1.0

    def _level(self, score: float) -> str:
        if score >= self._THRESHOLDS["high"]:
            return "high"
        if score >= self._THRESHOLDS["medium"]:
            return "medium"
        if score >= self._THRESHOLDS["low"]:
            return "low"
        return "uncertain"

    def adjust_response(self, response_text: str, result: ConfidenceResult) -> str:
        """Préfixe la réponse avec la phrase de couverture si nécessaire."""
        if result.should_hedge and result.hedge_phrase:
            return result.hedge_phrase + response_text
        return response_text


# ─── Singleton ────────────────────────────────────────────────────────────────

_scorer: ConfidenceScorer | None = None


def get_confidence_scorer() -> ConfidenceScorer:
    global _scorer
    if _scorer is None:
        _scorer = ConfidenceScorer()
    return _scorer


def reset_confidence_scorer() -> None:
    global _scorer
    _scorer = None
