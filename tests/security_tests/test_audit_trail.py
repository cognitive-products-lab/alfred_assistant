"""
════════════════════════════════════════════════════════════
PROJECT      : ALFRED
BLOCK        : B20
FUNCTION     : 20.TEST
FILE         : tests/security_tests/test_audit_trail.py
ROLE         : Tests unitaires — audit_trail.py V1.2

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-06-01
VERSION      : V1.2
STATUS       : ACTIVE
════════════════════════════════════════════════════════════
"""

import json
import pytest
from src.security.audit_trail import (
    write_audit_event, read_audit_events,
    read_audit_events_since, read_audit_events_by_user,
    list_audit_events_by_decision, clear_audit_trail,
    summarize_audit_events, AUDIT_FILE,
)


@pytest.fixture(autouse=True)
def clean_audit():
    backup = AUDIT_FILE.read_text(encoding="utf-8") if AUDIT_FILE.exists() else ""
    AUDIT_FILE.write_text("", encoding="utf-8")
    yield
    AUDIT_FILE.write_text(backup, encoding="utf-8")


# ─── write / read ────────────────────────────────────────────────────────────

def test_write_returns_dict():
    e = write_audit_event("u", "read", "mem", "ALLOW")
    assert isinstance(e, dict) and e["decision"] == "ALLOW"

def test_write_jsonl():
    write_audit_event("u", "a", "r", "ALLOW")
    lines = AUDIT_FILE.read_text(encoding="utf-8").strip().splitlines()
    assert len(lines) == 1 and json.loads(lines[0])["decision"] == "ALLOW"

def test_read_empty():
    assert read_audit_events() == []

def test_read_events():
    write_audit_event("alice", "chat", "alfred", "ALLOW", role="OWNER")
    events = read_audit_events()
    assert len(events) == 1 and events[0]["user_id"] == "alice"

def test_read_multiple():
    for d in ["ALLOW", "DENY_INPUT", "DENY_DEVICE"]:
        write_audit_event("u", "a", "r", d)
    assert len(read_audit_events()) == 3


# ─── read_since ───────────────────────────────────────────────────────────────

def test_read_since_recent():
    write_audit_event("u", "a", "r", "ALLOW")
    assert len(read_audit_events_since(hours=1.0)) == 1

def test_read_since_zero():
    write_audit_event("u", "a", "r", "ALLOW")
    assert len(read_audit_events_since(hours=0.0)) == 0


# ─── read_by_user ────────────────────────────────────────────────────────────

def test_read_by_user():
    write_audit_event("alice", "r", "m", "ALLOW")
    write_audit_event("bob",   "r", "m", "DENY_INPUT")
    assert len(read_audit_events_by_user("alice")) == 1

def test_read_by_user_missing():
    write_audit_event("alice", "r", "m", "ALLOW")
    assert read_audit_events_by_user("charlie") == []


# ─── filter_by_decision ───────────────────────────────────────────────────────

def test_filter_allow():
    write_audit_event("u", "a", "r", "ALLOW")
    write_audit_event("u", "a", "r", "DENY_INPUT")
    assert len(list_audit_events_by_decision("ALLOW")) == 1

def test_filter_no_match():
    write_audit_event("u", "a", "r", "ALLOW")
    assert list_audit_events_by_decision("DENY_THREAT") == []


# ─── clear ────────────────────────────────────────────────────────────────────

def test_clear_no_confirm():
    write_audit_event("u", "a", "r", "ALLOW")
    assert clear_audit_trail(confirm=False) is False
    assert len(read_audit_events()) == 1

def test_clear_confirmed():
    write_audit_event("u", "a", "r", "ALLOW")
    assert clear_audit_trail(confirm=True) is True
    assert read_audit_events() == []


# ─── summarize ────────────────────────────────────────────────────────────────

def test_summarize_empty():
    s = summarize_audit_events()
    assert s["total"] == 0 and s["allow"] == 0

def test_summarize_counts():
    write_audit_event("u", "a", "r", "ALLOW")
    write_audit_event("u", "a", "r", "ALLOW")
    write_audit_event("u", "a", "r", "DENY_INPUT")
    s = summarize_audit_events()
    assert s["total"] == 3 and s["allow"] == 2 and s["deny"] == 1

def test_summarize_by_decision():
    write_audit_event("u", "a", "r", "DENY_THREAT")
    s = summarize_audit_events()
    assert "DENY_THREAT" in s["by_decision"]
