"""
════════════════════════════════════════════════════════════
PROJECT      : ALFRED
BLOCK        : B20
FUNCTION     : 20.13
FILE         : tests/security_tests/test_policy_decision_point_history.py
ROLE         : Tests de la journalisation des décisions Zero Trust (point C4-C)

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-07-13
VERSION      : V1.0
STATUS       : ACTIVE

DESCRIPTION :
Vérifie que decide_access() journalise bien chaque décision dans
data/security/access_decisions_history.json (self-initialisant, append-only,
plafonné à _MAX_HISTORY_ENTRIES).
════════════════════════════════════════════════════════════
"""

import json

import pytest

from src.security import policy_decision_point as pdp


@pytest.fixture
def isolated_history(tmp_path, monkeypatch):
    history_file = tmp_path / "access_decisions_history.json"
    monkeypatch.setattr(pdp, "_HISTORY_FILE", history_file)
    return history_file


def test_decide_access_creates_history_file(isolated_history):
    assert not isolated_history.exists()
    pdp.decide_access("OWNER", "LOW", "READ_MEMORY")
    assert isolated_history.exists()


def test_decide_access_appends_expected_fields(isolated_history):
    pdp.decide_access("AI_MODULE", "MEDIUM", "RUN_AI_MODULE", risk_score=5)
    history = json.loads(isolated_history.read_text(encoding="utf-8"))
    assert len(history) == 1
    entry = history[0]
    for field in ("timestamp", "role", "resource_sensitivity", "action", "risk_score", "decision"):
        assert field in entry
    assert entry["role"] == "AI_MODULE"
    assert entry["resource_sensitivity"] == "MEDIUM"
    assert entry["action"] == "RUN_AI_MODULE"
    assert entry["risk_score"] == 5


def test_decide_access_appends_multiple_entries(isolated_history):
    pdp.decide_access("OWNER", "LOW", "READ_MEMORY")
    pdp.decide_access("GUEST", "CRITICAL", "DELETE_DATA")
    history = json.loads(isolated_history.read_text(encoding="utf-8"))
    assert len(history) == 2


def test_decide_access_verbose_also_logs(isolated_history):
    pdp.decide_access_verbose("OWNER", "LOW", "READ_MEMORY")
    history = json.loads(isolated_history.read_text(encoding="utf-8"))
    assert len(history) == 1


def test_history_capped_at_max_entries(isolated_history, monkeypatch):
    monkeypatch.setattr(pdp, "_MAX_HISTORY_ENTRIES", 3)
    for _ in range(5):
        pdp.decide_access("OWNER", "LOW", "READ_MEMORY")
    history = json.loads(isolated_history.read_text(encoding="utf-8"))
    assert len(history) == 3


def test_corrupted_history_file_resets_gracefully(isolated_history):
    isolated_history.write_text("not valid json", encoding="utf-8")
    pdp.decide_access("OWNER", "LOW", "READ_MEMORY")
    history = json.loads(isolated_history.read_text(encoding="utf-8"))
    assert len(history) == 1
