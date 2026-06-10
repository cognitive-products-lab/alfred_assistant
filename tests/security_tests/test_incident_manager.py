"""
════════════════════════════════════════════════════════════
PROJECT      : ALFRED
BLOCK        : B20
FUNCTION     : 20.TEST
FILE         : tests/security_tests/test_incident_manager.py
ROLE         : Tests unitaires — incident_manager.py

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-06-01
UPDATED      : 2026-06-01
VERSION      : V1.0
STATUS       : ACTIVE

DESCRIPTION :
Couvre : register_incident, list_incidents (filtre statut),
summarize_incidents (comptage CRITICAL/WARNING).
════════════════════════════════════════════════════════════
"""

import json
import pytest
from pathlib import Path
from src.security.incident_manager import (
    register_incident,
    list_incidents,
    summarize_incidents,
    INCIDENT_FILE,
)


@pytest.fixture(autouse=True)
def clean_incident_file():
    """Sauvegarde et restaure le registre d'incidents autour de chaque test."""
    backup = None
    if INCIDENT_FILE.exists():
        backup = INCIDENT_FILE.read_text(encoding="utf-8")
    INCIDENT_FILE.write_text("[]", encoding="utf-8")
    yield
    if backup is not None:
        INCIDENT_FILE.write_text(backup, encoding="utf-8")
    else:
        INCIDENT_FILE.write_text("[]", encoding="utf-8")


# ─── register_incident ────────────────────────────────────────────────────────

def test_register_creates_incident():
    register_incident("WARNING", "Test incident 1", source="test")
    incidents = list_incidents()
    assert len(incidents) == 1
    assert incidents[0]["level"] == "WARNING"
    assert incidents[0]["description"] == "Test incident 1"
    assert incidents[0]["source"] == "test"
    assert incidents[0]["status"] == "OPEN"


def test_register_multiple_incidents():
    register_incident("CRITICAL", "Incident critique", source="test")
    register_incident("WARNING", "Incident warning", source="test")
    register_incident("INFO", "Incident info", source="test")
    incidents = list_incidents()
    assert len(incidents) == 3


def test_register_sets_timestamp():
    register_incident("WARNING", "Timestamp test", source="test")
    incidents = list_incidents()
    assert "timestamp" in incidents[0]
    assert len(incidents[0]["timestamp"]) > 10


# ─── list_incidents ───────────────────────────────────────────────────────────

def test_list_all_incidents():
    register_incident("WARNING", "W1", source="test")
    register_incident("CRITICAL", "C1", source="test")
    assert len(list_incidents()) == 2


def test_list_incidents_filter_open():
    register_incident("WARNING", "Open incident", source="test")
    incidents = list_incidents(status="OPEN")
    assert all(i["status"] == "OPEN" for i in incidents)


def test_list_incidents_filter_nonexistent_status():
    register_incident("WARNING", "Test", source="test")
    result = list_incidents(status="RESOLVED")
    assert result == []


def test_list_incidents_empty_file():
    incidents = list_incidents()
    assert incidents == []


# ─── summarize_incidents ─────────────────────────────────────────────────────

def test_summarize_empty():
    summary = summarize_incidents()
    assert summary["total"] == 0
    assert summary["open_critical"] == 0


def test_summarize_counts_total():
    register_incident("WARNING", "W1", source="test")
    register_incident("WARNING", "W2", source="test")
    register_incident("CRITICAL", "C1", source="test")
    summary = summarize_incidents()
    assert summary["total"] == 3


def test_summarize_open_critical():
    register_incident("CRITICAL", "Critical open", source="test")
    register_incident("CRITICAL", "Critical open 2", source="test")
    register_incident("WARNING", "Warning only", source="test")
    summary = summarize_incidents()
    assert summary["open_critical"] == 2


def test_summarize_by_level():
    register_incident("CRITICAL", "C1", source="test")
    register_incident("WARNING", "W1", source="test")
    register_incident("WARNING", "W2", source="test")
    summary = summarize_incidents()
    assert summary["by_level"]["CRITICAL"] == 1
    assert summary["by_level"]["WARNING"] == 2


# ─── Persistance JSON ─────────────────────────────────────────────────────────

def test_incidents_persisted_to_file():
    register_incident("WARNING", "Persisted", source="test")
    raw = json.loads(INCIDENT_FILE.read_text(encoding="utf-8"))
    assert len(raw) == 1
    assert raw[0]["description"] == "Persisted"


def test_source_field_stored():
    register_incident("INFO", "Source test", source="unit_test_module")
    incidents = list_incidents()
    assert incidents[0]["source"] == "unit_test_module"
