"""
ALFRED — src/knowledge/knowledge_quality_gate.py
Knowledge Quality Gate — voir
docs/architecture/vision_knowledge_training_finetuning_alfred.md, P0
(document source, section 5).

Évalue une connaissance candidate (réponse obtenue via repli cloud, quand
Ollama local a échoué) avant qu'elle ne puisse un jour intégrer le
Knowledge Store ou un dataset d'entraînement. Ne classe jamais rien
VALIDATED ni training_eligible=True automatiquement — contraintes non
négociables #2 et #3 du document source : aucune sortie de LLM externe
n'est Ground Truth par défaut, aucune recherche externe n'entre
automatiquement dans le Training Dataset.

Réutilise src.security.safety_gate.assess_prompt_sensitivity() pour la
confidentialité plutôt que de réinventer une échelle à 5 niveaux
(PUBLIC/INTERNAL/PRIVATE/SENSITIVE/SECRET) que rien d'autre dans ce code
n'utilise encore — voir le document de vision pour la justification
complète de ce choix.
"""
from __future__ import annotations

from typing import Any

from src.security.safety_gate import assess_prompt_sensitivity


def evaluate_candidate(query: str, external_source: str) -> dict[str, Any]:
    """
    Évalue une connaissance candidate acquise via repli cloud.

    Args:
        query          : la question/texte à l'origine de l'acquisition.
        external_source: fournisseur ayant produit la réponse ("openai",
                         "anthropic"...).

    Returns:
        {"privacy_level": "LOCAL_ONLY" | "STANDARD",
         "source_type": str,
         "status": "TO_VERIFY",
         "training_eligible": False}
    """
    sensitivity = assess_prompt_sensitivity(query)

    return {
        "privacy_level": sensitivity["privacy_level"],
        "source_type": external_source or "unknown",
        # Jamais VALIDATED à l'acquisition — voir document source section 6
        # (ACTIVE, STALE, TO_VERIFY, CONFLICT, REJECTED, ARCHIVED) : une
        # validation humaine reste nécessaire avant qu'une connaissance
        # candidate entre réellement dans le Knowledge Store.
        "status": "TO_VERIFY",
        "training_eligible": False,
    }
