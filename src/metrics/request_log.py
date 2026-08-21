from __future__ import annotations

"""
PROJECT      : ALFRED
BLOCK        : B18
FUNCTION     : 18.30
FILE         : src/metrics/request_log.py
ROLE         : Journal minimal de chaque requête — dénominateur des KPI de taux

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-08-21
UPDATED      : 2026-08-21
VERSION      : V1.0
STATUS       : TESTED

DESCRIPTION :
Voir docs/architecture/vision_knowledge_training_finetuning_alfred.md, P2
(document source, section 26 — KPI). Décision d'architecture posée
explicitement à Céline avant implémentation (21/08/2026) : journal dédié
retenu plutôt qu'un compteur agrégé sans historique ou une réutilisation de
dialogue_history.json (tours de conversation, pas requêtes pipeline —
compte des commandes hors-LLM, et purgé par retention_days).
"""

"""
ALFRED — request_log.py
Tourne sur 100% du trafic (pas seulement les échecs, à la différence de
src.knowledge.gap_dataset) — volontairement sans texte de requête : y
conserver chaque question poserait un problème de sobriété de données que
gap_dataset.py n'a pas (lui ne journalise que les échecs, un sous-ensemble
minoritaire du trafic).
"""

import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

_ROOT = Path(__file__).resolve().parents[2]
REQUEST_LOG_FILE = _ROOT / "data" / "metrics" / "request_log.jsonl"
ARCHIVE_DIR = _ROOT / "data" / "metrics" / "request_log_archives"
REQUEST_LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

MAX_LOG_LINES = 20_000
MAX_LOG_BYTES = 5 * 1024 * 1024  # 5 Mo


def _rotate_if_needed() -> None:
    if not REQUEST_LOG_FILE.exists():
        return
    size = REQUEST_LOG_FILE.stat().st_size
    lines = sum(1 for _ in REQUEST_LOG_FILE.open(encoding="utf-8"))
    if size < MAX_LOG_BYTES and lines < MAX_LOG_LINES:
        return
    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    dest = ARCHIVE_DIR / f"request_log_{ts}.jsonl"
    shutil.copy2(REQUEST_LOG_FILE, dest)
    REQUEST_LOG_FILE.write_text("", encoding="utf-8")


def record_request(
    local_success: bool,
    used_knowledge: bool,
    route: str = "",
    external_source: Optional[str] = None,
) -> dict[str, Any]:
    """
    Args:
        local_success    : True si Ollama local a répondu (voir
                            LLMRouter.last_provider == "ollama").
        used_knowledge    : True si le B18 Knowledge Retrieval Engine a
                            chargé au moins une fiche pour ce tour
                            (context["knowledge_ids"] non vide).
        route             : mode/route de ce tour (context["adaptation"]["mode"]).
        external_source   : "openai"/"anthropic" si le repli cloud a
                            répondu, None sinon.
    """
    event = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "local_success": local_success,
        "used_knowledge": used_knowledge,
        "route": route,
        "external_source": external_source,
    }
    _rotate_if_needed()
    with REQUEST_LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")
    return event


def read_requests(limit: Optional[int] = None) -> list[dict[str, Any]]:
    if not REQUEST_LOG_FILE.exists():
        return []
    lines = REQUEST_LOG_FILE.read_text(encoding="utf-8").splitlines()
    if limit is not None:
        lines = lines[-limit:]
    events: list[dict[str, Any]] = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        try:
            events.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return events


def count_requests() -> int:
    return len(read_requests())
