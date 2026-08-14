"""
════════════════════════════════════════════════════════════
PROJECT      : ALFRED
BLOCK        : B02
FUNCTION     : 02.01
FILE         : test_memory_engine_retention.py
ROLE         : Tests de la politique de rétention (MemoryEngine.retention_days)

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-08-14
UPDATED      : 2026-08-14
VERSION      : V1.0
STATUS       : ACTIVE

DESCRIPTION :
Point P3 du chantier "sobriété/indépendance LLM externe"
(docs/architecture/vision_architecture_cognitive_alfred.md). Avant ce
point, dialogue_history.json grandissait indéfiniment — aucune purge,
aucune politique. Vérifie que retention_days=None préserve le
comportement actuel (rien n'est jamais retiré), et que retention_days=N
retire bien les échanges plus anciens que N jours sans toucher aux
récents ni aux entrées sans timestamp exploitable.
════════════════════════════════════════════════════════════
"""

import json
from datetime import datetime, timedelta

from src.memory.memory_engine import MemoryEngine


def _write_history(path, entries):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(entries, f, ensure_ascii=False)


def test_default_retention_none_keeps_everything(tmp_path):
    history_path = tmp_path / "dialogue_history.json"
    old_entry = {
        "timestamp": (datetime.now() - timedelta(days=365)).isoformat(timespec="seconds"),
        "user": "vieux message", "alfred": "vieille réponse",
    }
    _write_history(history_path, [old_entry])

    engine = MemoryEngine(history_path=str(history_path))

    assert len(engine.history) == 1


def test_retention_days_prunes_old_entries_on_load(tmp_path):
    history_path = tmp_path / "dialogue_history.json"
    old_entry = {
        "timestamp": (datetime.now() - timedelta(days=120)).isoformat(timespec="seconds"),
        "user": "vieux message", "alfred": "vieille réponse",
    }
    recent_entry = {
        "timestamp": (datetime.now() - timedelta(days=1)).isoformat(timespec="seconds"),
        "user": "message récent", "alfred": "réponse récente",
    }
    _write_history(history_path, [old_entry, recent_entry])

    engine = MemoryEngine(history_path=str(history_path), retention_days=90)

    assert len(engine.history) == 1
    assert engine.history[0]["user"] == "message récent"


def test_retention_prunes_after_save_exchange(tmp_path):
    history_path = tmp_path / "dialogue_history.json"
    old_entry = {
        "timestamp": (datetime.now() - timedelta(days=120)).isoformat(timespec="seconds"),
        "user": "vieux message", "alfred": "vieille réponse",
    }
    _write_history(history_path, [old_entry])

    engine = MemoryEngine(history_path=str(history_path), retention_days=90)
    engine.save_exchange("nouveau message", "nouvelle réponse")

    assert len(engine.history) == 1
    assert engine.history[0]["user"] == "nouveau message"

    with open(history_path, "r", encoding="utf-8") as f:
        on_disk = json.load(f)
    assert len(on_disk) == 1


def test_entry_without_timestamp_is_kept_not_dropped(tmp_path):
    history_path = tmp_path / "dialogue_history.json"
    _write_history(history_path, [{"user": "sans date", "alfred": "réponse"}])

    engine = MemoryEngine(history_path=str(history_path), retention_days=30)

    assert len(engine.history) == 1


def test_stats_exposes_retention_days(tmp_path):
    history_path = tmp_path / "dialogue_history.json"
    engine = MemoryEngine(history_path=str(history_path), retention_days=45)

    assert engine.stats()["retention_days"] == 45
