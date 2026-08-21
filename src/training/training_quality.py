from __future__ import annotations

"""
PROJECT      : ALFRED
BLOCK        : B18
FUNCTION     : 18.21
FILE         : src/training/training_quality.py
ROLE         : Contrôle qualité/confidentialité/duplication avant training_eligible

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-08-21
UPDATED      : 2026-08-21
VERSION      : V1.0
STATUS       : TESTED

DESCRIPTION :
Voir docs/architecture/vision_knowledge_training_finetuning_alfred.md, P1
(document source, section 16 — Data Quality for Training).
"""

"""
ALFRED — training_quality.py
Ne recalcule pas accuracy/completeness/consistency/relevance/
representativeness (ces dimensions demandent un jugement humain ou un
modèle d'évaluation que ce projet n'a pas encore) : quality_score reste un
paramètre fourni par la personne qui valide l'exemple, jamais une
heuristique inventée ici. Ce module ne calcule que ce qui est réellement
mesurable sans jugement subjectif : confidentialité (réutilise
safety_gate.py) et duplication (similarité de texte contre les entrées déjà
présentes dans la catégorie).
"""

from difflib import SequenceMatcher
from typing import Any, Optional

from src.security.safety_gate import assess_prompt_sensitivity
from src.training.dataset_store import read_current

DUPLICATE_THRESHOLD = 0.92


def _duplicate_score(text: str, category: str) -> float:
    """Similarité maximale (0-1) avec les entrées déjà présentes dans le
    fichier courant de la catégorie — pas de comparaison inter-catégories."""
    existing = read_current(category)
    if not existing or not text:
        return 0.0

    best = 0.0
    for entry in existing:
        candidate_text = entry.get("instruction") or entry.get("prompt") or ""
        if not candidate_text:
            continue
        ratio = SequenceMatcher(None, text, candidate_text).ratio()
        best = max(best, ratio)
    return round(best, 3)


def evaluate_training_entry(
    text_for_privacy: str,
    text_for_duplicate: str,
    category: str,
    quality_score: Optional[float] = None,
) -> dict[str, Any]:
    """
    Args:
        text_for_privacy   : texte à évaluer pour la confidentialité
                              (généralement l'instruction/prompt).
        text_for_duplicate : texte à comparer aux entrées déjà présentes.
        category            : catégorie dataset_store ("instructions",
                              "preferences"...).
        quality_score       : fourni par la personne qui valide l'exemple —
                              jamais recalculé automatiquement ici. Sans
                              valeur, training_eligible reste False.

    Returns:
        {"privacy_check": bool, "privacy_level": str,
         "duplicate_score": float, "quality_score": float | None,
         "training_eligible": bool}
    """
    sensitivity = assess_prompt_sensitivity(text_for_privacy)
    duplicate_score = _duplicate_score(text_for_duplicate, category)

    privacy_check = sensitivity["privacy_level"] == "STANDARD"
    is_duplicate = duplicate_score >= DUPLICATE_THRESHOLD

    training_eligible = bool(
        privacy_check
        and not is_duplicate
        and quality_score is not None
        and quality_score >= 0.7
    )

    return {
        "privacy_check": privacy_check,
        "privacy_level": sensitivity["privacy_level"],
        "duplicate_score": duplicate_score,
        "quality_score": quality_score,
        "training_eligible": training_eligible,
    }
