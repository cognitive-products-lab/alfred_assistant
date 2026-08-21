from __future__ import annotations

"""
PROJECT      : ALFRED
BLOCK        : B18
FUNCTION     : 18.23
FILE         : src/training/preference_dataset.py
ROLE         : Preference Dataset — paires chosen/rejected pour DPO

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-08-21
UPDATED      : 2026-08-21
VERSION      : V1.0
STATUS       : TESTED

DESCRIPTION :
Voir docs/architecture/vision_knowledge_training_finetuning_alfred.md, P1
(document source, section 14).
"""

"""
ALFRED — preference_dataset.py
Écriture volontairement manuelle, même principe que instruction_dataset.py.
"""

from typing import Any

from src.training.dataset_store import append_entry

CATEGORY = "preferences"


def record_preference(
    prompt: str,
    chosen: str,
    rejected: str,
    preference_source: str = "user",
    confidence: float = 1.0,
) -> dict[str, Any]:
    """
    Args:
        prompt            : la question/instruction commune aux deux réponses.
        chosen             : la réponse préférée.
        rejected           : la réponse écartée.
        preference_source : origine de la préférence ("user", "curator"...).
        confidence         : confiance dans cette préférence, 0-1.
    """
    entry = {
        "prompt": prompt,
        "chosen": chosen,
        "rejected": rejected,
        "preference_source": preference_source,
        "confidence": confidence,
    }
    append_entry(CATEGORY, entry)
    return entry
