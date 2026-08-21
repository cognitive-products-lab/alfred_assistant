from __future__ import annotations

"""
PROJECT      : ALFRED
BLOCK        : B18
FUNCTION     : 18.13
FILE         : src/knowledge/freshness_checker.py
ROLE         : Gestion de la fraîcheur des fiches knowledge

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-08-21
UPDATED      : 2026-08-21
VERSION      : V1.0
STATUS       : TESTED

DESCRIPTION :
Voir docs/architecture/vision_knowledge_training_finetuning_alfred.md, P0
(document source, section 8).
"""

"""
ALFRED — freshness_checker.py
Détermine VALID/STALE/REVALIDATION_REQUIRED à partir de
metadata["verified_at"] + metadata["freshness_policy"] (voir
knowledge_schema.py). Diagnostique uniquement — une information périmée
n'est jamais supprimée ni modifiée automatiquement (document source
section 8 : "elle peut être archivée et remplacée", jamais en un clic
automatique).
"""

from datetime import datetime, timezone
from typing import Any, Optional

# None = jamais périmé (STATIC). Les autres valeurs sont des seuils en
# jours — voir document source section 5 pour la liste des politiques.
FRESHNESS_POLICY_DAYS: dict[str, Optional[int]] = {
    "STATIC": None,
    "LONG_TERM": 365,
    "90_DAYS": 90,
    "30_DAYS": 30,
    "7_DAYS": 7,
    "24_HOURS": 1,
    "REAL_TIME": 0,
}

# Au-delà du seuil de la politique : STALE (encore utilisable, à
# surveiller). Au-delà de REVALIDATION_MULTIPLIER x ce seuil :
# REVALIDATION_REQUIRED (ne plus faire confiance sans revérifier).
REVALIDATION_MULTIPLIER = 2.0


def check_freshness(metadata: dict[str, Any], now: Optional[datetime] = None) -> str:
    """
    Args:
        metadata : le sous-objet "metadata" d'une entrée
                   KnowledgeLoader.knowledge_index (ou tout dict portant
                   "freshness_policy"/"verified_at").
        now       : horloge injectable pour les tests, sinon UTC actuel.

    Returns:
        "VALID" | "STALE" | "REVALIDATION_REQUIRED" | "UNKNOWN"

        "UNKNOWN" si freshness_policy n'est pas reconnue ou si verified_at
        est absent/invalide — volontairement distinct de "VALID" : une
        fiche sans date de vérification ne doit jamais être présumée
        fraîche par défaut.
    """
    now = now or datetime.now(timezone.utc)
    policy = metadata.get("freshness_policy")

    if policy not in FRESHNESS_POLICY_DAYS:
        return "UNKNOWN"

    max_days = FRESHNESS_POLICY_DAYS[policy]
    if max_days is None:
        return "VALID"

    verified_at = metadata.get("verified_at")
    if not verified_at:
        return "UNKNOWN"

    try:
        verified_dt = datetime.fromisoformat(verified_at)
    except (ValueError, TypeError):
        return "UNKNOWN"
    if verified_dt.tzinfo is None:
        verified_dt = verified_dt.replace(tzinfo=timezone.utc)

    age_days = (now - verified_dt).total_seconds() / 86400

    if age_days <= max_days:
        return "VALID"
    if age_days <= max_days * REVALIDATION_MULTIPLIER:
        return "STALE"
    return "REVALIDATION_REQUIRED"


def scan_knowledge_index(knowledge_index: dict[str, dict[str, Any]]) -> dict[str, list[str]]:
    """
    Balaie un KnowledgeLoader.knowledge_index et regroupe les knowledge_id
    par statut de fraîcheur — outil de maintenance (document source
    section 8), jamais d'action automatique sur le corpus.
    """
    grouped: dict[str, list[str]] = {
        "VALID": [], "STALE": [], "REVALIDATION_REQUIRED": [], "UNKNOWN": [],
    }
    for knowledge_id, item in knowledge_index.items():
        metadata = item.get("metadata", {}) or {}
        status = check_freshness(metadata)
        grouped[status].append(knowledge_id)
    return grouped
