from __future__ import annotations

"""
PROJECT      : ALFRED
BLOCK        : B18
FUNCTION     : 18.11
FILE         : src/knowledge/gap_curation.py
ROLE         : Outil de curation — promotion d'une connaissance candidate en fiche knowledge

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-08-21
UPDATED      : 2026-08-21
VERSION      : V1.0
STATUS       : TESTED

DESCRIPTION :
Voir docs/architecture/vision_knowledge_training_finetuning_alfred.md, P1.
"""

"""
ALFRED — gap_curation.py
Transforme une connaissance candidate validée (knowledge_candidates.py) en
vraie fiche du corpus Knowledge.

Action volontairement manuelle et explicite (jamais automatique) — cohérent
avec les contraintes non négociables du document source : une réponse LLM
externe n'est jamais Ground Truth par défaut, une validation humaine
(l'appel de cette fonction avec des champs éditoriaux choisis à la main —
titre, résumé, contenu structuré) est le seul chemin vers le corpus RAG.
"""

import json
import os
import re
import unicodedata
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

from src.knowledge.knowledge_candidates import get_candidate, mark_promoted

_ROOT = Path(__file__).resolve().parents[2]
_REGISTRY_PATH = _ROOT / "knowledges" / "knowledge_registry.json"


def _slugify(text: str) -> str:
    normalized = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    normalized = normalized.lower()
    normalized = re.sub(r"[^a-z0-9]+", "_", normalized).strip("_")
    return normalized or "fiche"


def promote_candidate_to_knowledge(
    candidate_id: str,
    domain: str,
    subdomain: str,
    title: str,
    summary: str,
    content: dict[str, Any],
    tags: Optional[list[str]] = None,
    purpose: str = "",
) -> str:
    """
    Matérialise une connaissance candidate validée en fiche knowledge réelle
    et l'enregistre dans knowledge_registry.json.

    Args:
        candidate_id : identifiant retourné par
                        knowledge_candidates.record_candidate().
        domain, subdomain : emplacement dans l'arborescence knowledges/.
        title, summary, content, tags, purpose : champs éditoriaux choisis
                        par la personne qui valide — jamais copiés
                        automatiquement depuis la réponse brute du LLM
                        externe, même si celle-ci peut inspirer le contenu.

    Returns:
        Le knowledge_id de la nouvelle fiche.

    Raises:
        ValueError si le candidat est introuvable, rédigé pour
        confidentialité, ou si une fiche existe déjà à cet emplacement.
    """
    candidate = get_candidate(candidate_id)
    if candidate is None:
        raise ValueError(f"Candidat introuvable : {candidate_id}")
    if candidate.get("redacted"):
        raise ValueError(
            f"Candidat {candidate_id} rédigé pour confidentialité (privacy_level "
            "non STANDARD à l'acquisition) — ne peut pas être promu automatiquement, "
            "reformule-le à la main si nécessaire."
        )

    slug = _slugify(title)
    knowledge_id = f"{domain}.{subdomain}.{slug}"
    relative_file = f"knowledges/{domain}/{subdomain}/{slug}.json"
    file_path = _ROOT / relative_file

    if file_path.exists():
        raise ValueError(f"Une fiche existe déjà à ce chemin : {relative_file}")

    now = datetime.now(timezone.utc).isoformat()
    quality = candidate.get("quality", {}) or {}

    fiche = {
        "schema_version": "1.2",
        "type": "knowledge_unit",
        "knowledge_id": knowledge_id,
        "title": title,
        "version": "1.0.0",
        "status": "active",
        "domain": domain,
        "subdomain": subdomain,
        "category": domain,
        "priority": "to_review",
        "safety_level": "normal",
        "summary": summary,
        "purpose": purpose,
        "tags": tags or [],
        "intents": [],
        "usage_context": [],
        "content": content,
        # Schéma additif — voir src/knowledge/knowledge_schema.py.
        "provenance": {
            "source_type": candidate.get("external_source", "unknown"),
            "acquired_at": candidate.get("timestamp"),
            "verified_at": now,
            "confidence": None,
            "freshness_policy": "STATIC",
            "privacy_level": quality.get("privacy_level", "STANDARD"),
            "training_eligible": False,
            # VALIDATED : un humain vient d'appeler cette fonction avec des
            # champs éditoriaux choisis à la main — c'est précisément l'acte
            # de validation attendu par le document source (section 6).
            "status": "VALIDATED",
        },
    }

    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(json.dumps(fiche, indent=2, ensure_ascii=False), encoding="utf-8")

    _register_in_registry(knowledge_id, relative_file, domain, subdomain, slug)
    mark_promoted(candidate_id, knowledge_id)

    return knowledge_id


def _register_in_registry(
    knowledge_id: str, relative_file: str, domain: str, subdomain: str, slug: str
) -> None:
    """Écriture atomique (fichier temporaire + remplacement) : ce registre
    porte 1190+ entrées et est relu à chaque démarrage d'ALFRED — une
    écriture interrompue en plein milieu ne doit jamais le laisser
    tronqué/invalide."""
    with _REGISTRY_PATH.open("r", encoding="utf-8-sig") as f:
        registry = json.load(f)

    registry.setdefault("knowledges", []).append({
        "id": knowledge_id,
        "file": relative_file,
        "domain": domain,
        "subdomain": subdomain,
        "filename": f"{slug}.json",
        "status": "active",
        "version": "1.0.0",
        "priority": "to_review",
        "source": "gap_curation",
    })
    registry.setdefault("stats", {})["total_json_files"] = len(registry["knowledges"])

    tmp_path = _REGISTRY_PATH.with_suffix(".json.tmp")
    with tmp_path.open("w", encoding="utf-8") as f:
        json.dump(registry, f, indent=2, ensure_ascii=False)
    os.replace(tmp_path, _REGISTRY_PATH)
