"""
════════════════════════════════════════════════════════════
PROJECT      : ALFRED
BLOCK        : B01 V2
FUNCTION     : 01.V2.01
FILE         : src/v2/fusion/fusion_engine.py
ROLE         : Moteur de fusion multi-sources V2 — mémoire + knowledge + LLM

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-06-01
UPDATED      : 2026-06-01
VERSION      : V1.0
STATUS       : ACTIVE

DESCRIPTION :
Fusionne les contributions de 3 sources pour construire le contexte
optimal d'une réponse ALFRED :
  1. Mémoire épisodique  — historique récent + faits mémorisés
  2. Knowledge retrieval — domaines pertinents au message
  3. LLM context        — contexte déjà construit dans le pipeline

Retourne un FusionResult avec context_blocks, weights, source_map.
Usage : brancher dans alfred_behavior_engine.py (V2).
════════════════════════════════════════════════════════════
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


# ─── Types ────────────────────────────────────────────────────────────────────

@dataclass
class SourceContribution:
    """Contribution d'une source au contexte fusionné."""
    source:     str            # "memory" | "knowledge" | "llm"
    content:    str            # texte injecté dans le contexte
    weight:     float = 1.0   # importance relative (0–1)
    metadata:   dict = field(default_factory=dict)


@dataclass
class FusionResult:
    """Résultat de la fusion multi-sources."""
    context_blocks: list[SourceContribution]
    merged_context: str          # contexte prêt à injecter dans le prompt
    primary_source: str          # source dominante
    weights:        dict[str, float]
    fusion_score:   float        # qualité estimée 0–1
    metadata:       dict = field(default_factory=dict)

    def to_context_string(self, max_chars: int = 2000) -> str:
        """Retourne le contexte fusionné tronqué pour le prompt."""
        return self.merged_context[:max_chars]


# ─── Moteur de fusion ─────────────────────────────────────────────────────────

class FusionEngine:
    """
    Moteur de fusion V2 — combine mémoire, knowledge et contexte LLM.

    Stratégies disponibles :
      "weighted"    : pondération par source (défaut)
      "priority"    : source prioritaire + compléments
      "round_robin" : alternance équilibrée
    """

    _DEFAULT_WEIGHTS = {
        "memory":    0.40,
        "knowledge": 0.35,
        "llm":       0.25,
    }

    def __init__(self, strategy: str = "weighted", weights: dict | None = None) -> None:
        self.strategy = strategy
        self.weights  = weights or self._DEFAULT_WEIGHTS.copy()

    def fuse(
        self,
        memory_context:    str = "",
        knowledge_context: str = "",
        llm_context:       str = "",
        user_message:      str = "",
        emotion:           str = "neutral",
        mode:              str = "complicite",
    ) -> FusionResult:
        """
        Fusionne les 3 sources et retourne un FusionResult.

        Args:
            memory_context    : historique/faits de la mémoire épisodique
            knowledge_context : blocs knowledge pertinents
            llm_context       : contexte déjà construit par le pipeline
            user_message      : message utilisateur (pour pondération adaptive)
            emotion           : émotion détectée (influe sur le poids mémoire)
            mode              : mode ALFRED (influe sur le poids knowledge)
        """
        weights = self._adapt_weights(user_message, emotion, mode)

        contributions: list[SourceContribution] = []

        if memory_context:
            contributions.append(SourceContribution(
                source="memory",
                content=memory_context,
                weight=weights["memory"],
                metadata={"emotion": emotion},
            ))

        if knowledge_context:
            contributions.append(SourceContribution(
                source="knowledge",
                content=knowledge_context,
                weight=weights["knowledge"],
                metadata={"mode": mode},
            ))

        if llm_context:
            contributions.append(SourceContribution(
                source="llm",
                content=llm_context,
                weight=weights["llm"],
            ))

        merged = self._merge(contributions)
        primary = max(weights, key=weights.get) if contributions else "llm"
        score   = self._score(contributions)

        return FusionResult(
            context_blocks=contributions,
            merged_context=merged,
            primary_source=primary,
            weights=weights,
            fusion_score=score,
            metadata={"strategy": self.strategy, "user_message_len": len(user_message)},
        )

    def _adapt_weights(self, user_message: str, emotion: str, mode: str) -> dict[str, float]:
        """Adapte les poids selon l'émotion et le mode."""
        w = self.weights.copy()

        # Émotion forte → boost mémoire (contexte personnel)
        if emotion in ("stressed", "sad", "anxious", "tired"):
            w["memory"]    = min(0.60, w["memory"] + 0.15)
            w["knowledge"] = max(0.15, w["knowledge"] - 0.10)

        # Mode focus/challenge → boost knowledge (contenu expert)
        elif mode in ("focus", "challenge"):
            w["knowledge"] = min(0.55, w["knowledge"] + 0.15)
            w["memory"]    = max(0.20, w["memory"] - 0.10)

        # Normaliser à somme = 1
        total = sum(w.values())
        if total > 0:
            w = {k: round(v / total, 3) for k, v in w.items()}

        return w

    def _merge(self, contributions: list[SourceContribution]) -> str:
        """Fusionne les contributions en un bloc de contexte unique."""
        if not contributions:
            return ""

        if self.strategy == "priority":
            # Source prioritaire d'abord, reste tronqué
            sorted_c = sorted(contributions, key=lambda c: c.weight, reverse=True)
            parts = [sorted_c[0].content]
            for c in sorted_c[1:]:
                parts.append(c.content[:200])
            return "\n\n".join(p for p in parts if p)

        # Stratégie weighted (défaut) : proportionnel aux poids
        parts = []
        for c in sorted(contributions, key=lambda x: x.weight, reverse=True):
            max_chars = max(100, int(1500 * c.weight))
            parts.append(c.content[:max_chars])

        return "\n\n".join(p for p in parts if p)

    def _score(self, contributions: list[SourceContribution]) -> float:
        """Score de qualité de la fusion (0–1)."""
        if not contributions:
            return 0.0
        n_sources = len(contributions)
        coverage  = n_sources / 3.0   # 3 sources max
        avg_weight = sum(c.weight for c in contributions) / max(1, n_sources)
        return round(min(1.0, coverage * 0.6 + avg_weight * 0.4), 3)

    def update_weights(self, **kwargs: float) -> None:
        """Met à jour les poids (memory/knowledge/llm)."""
        for k, v in kwargs.items():
            if k in self.weights:
                self.weights[k] = max(0.0, min(1.0, v))


# ─── Singleton ────────────────────────────────────────────────────────────────

_engine_instance: FusionEngine | None = None


def get_fusion_engine(strategy: str = "weighted") -> FusionEngine:
    """Retourne le singleton FusionEngine."""
    global _engine_instance
    if _engine_instance is None:
        _engine_instance = FusionEngine(strategy=strategy)
    return _engine_instance


def reset_fusion_engine() -> None:
    """Réinitialise le singleton (pour les tests)."""
    global _engine_instance
    _engine_instance = None
