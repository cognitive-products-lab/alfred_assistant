from __future__ import annotations

"""
PROJECT      : ALFRED
BLOCK        : B18
FUNCTION     : 18.22
FILE         : src/training/instruction_dataset.py
ROLE         : Instruction Dataset — exemples instruction → bonne réponse pour SFT

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-08-21
UPDATED      : 2026-08-21
VERSION      : V1.0
STATUS       : TESTED

DESCRIPTION :
Voir docs/architecture/vision_knowledge_training_finetuning_alfred.md, P1
(document source, section 13).
"""

"""
ALFRED — instruction_dataset.py
Écriture volontairement manuelle : appeler record_instruction_candidate()
EST l'acte de validation humaine attendu par le document — jamais une
conversation copiée automatiquement (section 10 : "les conversations ne
doivent jamais être copiées automatiquement dans le dataset d'entraînement").
"""

from typing import Any, Optional

from src.training.dataset_store import append_entry
from src.training.training_quality import evaluate_training_entry

CATEGORY = "instructions"


def record_instruction_candidate(
    instruction: str,
    response: str,
    context: str = "",
    source: str = "manual",
    quality_score: Optional[float] = None,
) -> dict[str, Any]:
    """
    Args:
        instruction   : la question/instruction.
        response      : la bonne réponse associée.
        context       : contexte additionnel éventuel.
        source        : provenance ("manual", "gap_curation",
                        "user_correction"...).
        quality_score : évaluation humaine 0-1 — sans valeur,
                        training_eligible reste False (voir
                        training_quality.py).

    Returns:
        L'entrée écrite, avec son évaluation qualité/confidentialité/
        duplication.
    """
    quality = evaluate_training_entry(
        text_for_privacy=f"{instruction}\n{context}".strip(),
        text_for_duplicate=instruction,
        category=CATEGORY,
        quality_score=quality_score,
    )

    entry = {
        "instruction": instruction,
        "context": context,
        "response": response,
        "source": source,
        "quality_score": quality_score,
        "privacy_level": quality["privacy_level"],
        "duplicate_score": quality["duplicate_score"],
        "training_eligible": quality["training_eligible"],
        "validated": True,
    }
    append_entry(CATEGORY, entry)
    return entry
