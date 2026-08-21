"""
ALFRED — src/knowledge/gap_dataset.py
Journal structuré des cas où ALFRED local échoue — voir
docs/architecture/vision_knowledge_training_finetuning_alfred.md, P0
(document source, section 9).

Alimenté depuis src/core/response_generator.py::generate_response(), le
seul point du pipeline qui connaît à la fois la requête posée et quel
fournisseur a finalement répondu (src.llm.llm_router.LLMRouter.last_provider).
Remplace le print() console qui existait jusqu'ici sur le chemin de repli
cloud (aucune persistance, aucune matière pour piloter la roadmap).

Format JSONL + rotation par taille, même pattern que
src/security/audit_trail.py — pas le même fichier : le schéma de
write_audit_event() est pensé pour une décision d'accès (ALLOW/DENY par
rôle+ressource), pas pour un échec/succès de recherche.
"""
from __future__ import annotations

import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

_ROOT = Path(__file__).resolve().parents[2]
GAP_FILE = _ROOT / "data" / "knowledge" / "gap_dataset.jsonl"
ARCHIVE_DIR = _ROOT / "data" / "knowledge" / "gap_dataset_archives"
GAP_FILE.parent.mkdir(parents=True, exist_ok=True)

MAX_GAP_LINES = 10_000
MAX_GAP_BYTES = 5 * 1024 * 1024  # 5 Mo

# Catégories suggérées par le document source (section 9) — indicatives,
# pas imposées : failure_reason reste une chaîne libre, la catégorie exacte
# dépend souvent d'une relecture humaine a posteriori.
FAILURE_REASONS = (
    "KNOWLEDGE_MISSING", "RETRIEVAL_FAILURE", "INTENT_FAILURE",
    "ROUTING_FAILURE", "MODEL_CAPABILITY", "TOOL_MISSING",
    "BAD_RESPONSE", "UNKNOWN",
)


def _rotate_if_needed() -> None:
    if not GAP_FILE.exists():
        return
    size = GAP_FILE.stat().st_size
    lines = sum(1 for _ in GAP_FILE.open(encoding="utf-8"))
    if size < MAX_GAP_BYTES and lines < MAX_GAP_LINES:
        return
    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    dest = ARCHIVE_DIR / f"gap_dataset_{ts}.jsonl"
    shutil.copy2(GAP_FILE, dest)
    GAP_FILE.write_text("", encoding="utf-8")


def record_gap_event(
    query: str,
    local_route: str = "",
    local_success: bool = False,
    failure_reason: Optional[str] = None,
    external_source: Optional[str] = None,
    external_success: Optional[bool] = None,
    resolved: Optional[bool] = None,
    candidate_quality: Optional[dict[str, Any]] = None,
) -> dict[str, Any]:
    """
    Enregistre un cas où le local a échoué (n'appeler que si
    local_success=False — un succès local n'est pas un gap, inutile de
    journaliser le cas courant).

    candidate_quality : verdict de
        src.knowledge.knowledge_quality_gate.evaluate_candidate() quand une
        connaissance candidate a été produite (external_success=True) —
        optionnel, None si aucun candidat (échec total local+cloud).
    """
    event = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "query": query,
        "local_route": local_route,
        "local_success": local_success,
        "failure_reason": failure_reason,
        "external_source": external_source,
        "external_success": external_success,
        "resolved": resolved,
        "candidate_quality": candidate_quality,
    }
    _rotate_if_needed()
    with GAP_FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")
    return event


def read_recent_gaps(limit: int = 50) -> list[dict[str, Any]]:
    """Retourne les derniers événements du Gap Dataset, plus récents en dernier."""
    if not GAP_FILE.exists():
        return []
    lines = GAP_FILE.read_text(encoding="utf-8").splitlines()
    events: list[dict[str, Any]] = []
    for line in lines[-limit:]:
        line = line.strip()
        if not line:
            continue
        try:
            events.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return events
