from __future__ import annotations

"""
PROJECT      : ALFRED
BLOCK        : B18
FUNCTION     : 18.09
FILE         : src/knowledge/knowledge_candidates.py
ROLE         : Stockage du contenu réel des connaissances candidates

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-08-21
UPDATED      : 2026-08-21
VERSION      : V1.0
STATUS       : TESTED

DESCRIPTION :
Voir docs/architecture/vision_knowledge_training_finetuning_alfred.md, P1.
"""

"""
ALFRED — knowledge_candidates.py
Distinct de gap_dataset.py (diagnostic pur : requête + métadonnées
d'échec/succès, toujours journalisé) : ce store ne conserve le CONTENU réel
que lorsque le Knowledge Quality Gate juge la requête d'origine non
sensible (privacy_level == "STANDARD"). Si LOCAL_ONLY, le contenu n'est
jamais persisté ici — cohérent avec la politique déjà en place
(safety_gate.py) qui a justement empêché la donnée sensible de partir vers
le cloud ; il serait incohérent de la stocker en clair après coup.

Format JSONL append-only, comme gap_dataset.py — une promotion
(gap_curation.promote_candidate_to_knowledge) n'édite jamais une ligne
existante, elle ajoute un marqueur de promotion séparé.
"""

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

_ROOT = Path(__file__).resolve().parents[2]
CANDIDATES_FILE = _ROOT / "data" / "knowledge" / "knowledge_candidates.jsonl"
CANDIDATES_FILE.parent.mkdir(parents=True, exist_ok=True)


def record_candidate(
    query: str,
    external_source: str,
    response_text: str,
    quality: dict[str, Any],
) -> str:
    """
    Enregistre le contenu d'une connaissance candidate si sa confidentialité
    le permet (quality["privacy_level"] == "STANDARD").

    Returns:
        Le candidate_id, utilisable ensuite par
        gap_curation.promote_candidate_to_knowledge().
    """
    candidate_id = f"cand_{uuid.uuid4().hex[:12]}"
    redacted = quality.get("privacy_level") != "STANDARD"

    event = {
        "candidate_id": candidate_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "query": query,
        "external_source": external_source,
        "response_text": None if redacted else response_text,
        "redacted": redacted,
        "quality": quality,
        "promotion_marker": False,
    }
    with CANDIDATES_FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")
    return candidate_id


def _iter_events():
    if not CANDIDATES_FILE.exists():
        return
    for line in CANDIDATES_FILE.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            yield json.loads(line)
        except json.JSONDecodeError:
            continue


def get_candidate(candidate_id: str) -> Optional[dict[str, Any]]:
    """Retourne l'enregistrement d'origine (pas un éventuel marqueur de
    promotion) pour candidate_id, ou None si introuvable."""
    match = None
    for event in _iter_events():
        if event.get("candidate_id") == candidate_id and not event.get("promotion_marker"):
            match = event
    return match


def read_pending_candidates(limit: int = 50) -> list[dict[str, Any]]:
    """Candidats au contenu disponible (non rédigés) et pas encore promus."""
    originals: dict[str, dict[str, Any]] = {}
    promoted_ids: set[str] = set()

    for event in _iter_events():
        cid = event.get("candidate_id")
        if not cid:
            continue
        if event.get("promotion_marker"):
            promoted_ids.add(cid)
        elif not event.get("redacted"):
            originals[cid] = event

    pending = [ev for cid, ev in originals.items() if cid not in promoted_ids]
    return pending[-limit:]


def mark_promoted(candidate_id: str, knowledge_id: str) -> None:
    """Append-only : ajoute un marqueur de promotion plutôt que d'éditer
    l'enregistrement d'origine."""
    event = {
        "candidate_id": candidate_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "promotion_marker": True,
        "knowledge_id": knowledge_id,
    }
    with CANDIDATES_FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")
