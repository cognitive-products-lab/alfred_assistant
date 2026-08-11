"""
PROJECT      : ALFRED
BLOCK        : GLOBAL — Intégrations externes
FILE         : tests/integrations_tests/test_tool_calling_calendar_provider.py
ROLE         : Tests unitaires du routage multi-fournisseur (Google/Outlook)
                dans src/core/tool_calling.py

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-07-24
VERSION      : V1.0
STATUS       : TESTED

DESCRIPTION :
src.ui.google_calendar_data et src.ui.outlook_calendar_data sont monkeypatchés
— ces tests vérifient uniquement le ROUTAGE (quel module est appelé selon le
paramètre "provider" et le fournisseur par défaut configuré), pas les clients
réels (voir test_google_calendar_client.py / test_outlook_calendar_client.py).
"""

from datetime import datetime

import src.ui.calendar_provider_prefs as cpp
import src.ui.google_calendar_data as gcd
import src.ui.outlook_calendar_data as ocd
from src.core import tool_calling


def _ok_event(summary="Titre", event_id="evt1"):
    return {"consent": True, "connected": True, "ok": True,
            "event": {"id": event_id, "summary": summary, "start": "", "end": "", "location": None, "all_day": False}}


# =============================================================================
# _resolve_calendar_provider
# =============================================================================

def test_resolve_provider_defaults_to_configured_pref(monkeypatch):
    monkeypatch.setattr(cpp, "load_default_calendar_provider", lambda: "outlook")
    assert tool_calling._resolve_calendar_provider({}) == "outlook"


def test_resolve_provider_uses_explicit_argument_over_default(monkeypatch):
    monkeypatch.setattr(cpp, "load_default_calendar_provider", lambda: "google")
    assert tool_calling._resolve_calendar_provider({"provider": "outlook"}) == "outlook"


def test_resolve_provider_ignores_invalid_explicit_value(monkeypatch):
    monkeypatch.setattr(cpp, "load_default_calendar_provider", lambda: "google")
    assert tool_calling._resolve_calendar_provider({"provider": "yahoo"}) == "google"


# =============================================================================
# create_calendar_event — routage
# =============================================================================

def test_create_calendar_event_routes_to_google_by_default(monkeypatch):
    monkeypatch.setattr(cpp, "load_default_calendar_provider", lambda: "google")
    called = {}
    monkeypatch.setattr(gcd, "create_calendar_event", lambda **kw: called.update(kw) or _ok_event())
    monkeypatch.setattr(ocd, "create_calendar_event", lambda **kw: (_ for _ in ()).throw(AssertionError("outlook ne doit pas être appelé")))

    result = tool_calling.execute_tool("create_calendar_event", {"summary": "Test", "time": "10:00"})

    assert result["ok"] is True
    assert called["summary"] == "Test"


def test_create_calendar_event_routes_to_outlook_when_explicit(monkeypatch):
    monkeypatch.setattr(cpp, "load_default_calendar_provider", lambda: "google")
    called = {}
    monkeypatch.setattr(ocd, "create_calendar_event", lambda **kw: called.update(kw) or _ok_event())
    monkeypatch.setattr(gcd, "create_calendar_event", lambda **kw: (_ for _ in ()).throw(AssertionError("google ne doit pas être appelé")))

    result = tool_calling.execute_tool("create_calendar_event", {"summary": "Test", "time": "10:00", "provider": "outlook"})

    assert result["ok"] is True
    assert called["summary"] == "Test"


def test_create_calendar_event_routes_to_outlook_when_configured_default(monkeypatch):
    monkeypatch.setattr(cpp, "load_default_calendar_provider", lambda: "outlook")
    called = {}
    monkeypatch.setattr(ocd, "create_calendar_event", lambda **kw: called.update(kw) or _ok_event())

    result = tool_calling.execute_tool("create_calendar_event", {"summary": "Test", "time": "10:00"})

    assert result["ok"] is True
    assert called["summary"] == "Test"


def test_create_calendar_event_builds_google_rrule_for_daily(monkeypatch):
    monkeypatch.setattr(cpp, "load_default_calendar_provider", lambda: "google")
    captured = {}
    monkeypatch.setattr(gcd, "create_calendar_event", lambda **kw: captured.update(kw) or _ok_event())

    tool_calling.execute_tool("create_calendar_event", {"summary": "Manger", "time": "19:00", "recurrence": "daily"})

    assert captured["recurrence"] == ["RRULE:FREQ=DAILY"]


def test_create_calendar_event_builds_outlook_pattern_for_daily(monkeypatch):
    monkeypatch.setattr(cpp, "load_default_calendar_provider", lambda: "outlook")
    captured = {}
    monkeypatch.setattr(ocd, "create_calendar_event", lambda **kw: captured.update(kw) or _ok_event())

    tool_calling.execute_tool("create_calendar_event", {"summary": "Manger", "time": "19:00", "date": "2026-07-24", "recurrence": "daily"})

    assert captured["recurrence"]["pattern"] == {"type": "daily", "interval": 1}
    assert captured["recurrence"]["range"]["startDate"] == "2026-07-24"


# =============================================================================
# list_calendar_events — routage
# =============================================================================

def test_list_calendar_events_routes_to_outlook_when_explicit(monkeypatch):
    monkeypatch.setattr(cpp, "load_default_calendar_provider", lambda: "google")
    monkeypatch.setattr(ocd, "get_calendar_state", lambda max_results=10: {"consent": True, "connected": True, "ok": True, "events": [{"summary": "Outlook event"}]})
    monkeypatch.setattr(gcd, "get_calendar_state", lambda max_results=10: (_ for _ in ()).throw(AssertionError("google ne doit pas être appelé")))

    result = tool_calling.execute_tool("list_calendar_events", {"provider": "outlook"})

    assert result["ok"] is True
    assert result["events"] == [{"summary": "Outlook event"}]


# =============================================================================
# update_calendar_event / delete_calendar_event — résolution provider-consciente
# =============================================================================

def test_update_calendar_event_resolves_via_correct_provider(monkeypatch):
    monkeypatch.setattr(cpp, "load_default_calendar_provider", lambda: "google")
    monkeypatch.setattr(
        ocd, "find_calendar_events",
        lambda hint: {"consent": True, "connected": True, "ok": True,
                      "events": [{"id": "evt1", "summary": "Dentiste", "start": "2026-07-24T10:00:00", "end": "2026-07-24T10:30:00"}]},
    )
    updated = {}
    monkeypatch.setattr(ocd, "update_calendar_event", lambda **kw: updated.update(kw) or _ok_event(summary="Dentiste"))
    monkeypatch.setattr(gcd, "find_calendar_events", lambda hint: (_ for _ in ()).throw(AssertionError("google ne doit pas être appelé")))

    result = tool_calling.execute_tool("update_calendar_event", {"summary_hint": "dentiste", "new_time": "11:00", "provider": "outlook"})

    assert result["ok"] is True
    assert updated["event_id"] == "evt1"


def test_delete_calendar_event_resolves_via_correct_provider(monkeypatch):
    monkeypatch.setattr(cpp, "load_default_calendar_provider", lambda: "outlook")
    monkeypatch.setattr(
        ocd, "find_calendar_events",
        lambda hint: {"consent": True, "connected": True, "ok": True,
                      "events": [{"id": "evt2", "summary": "Manger", "start": "2026-07-24T19:00:00", "end": "2026-07-24T19:15:00"}]},
    )
    monkeypatch.setattr(ocd, "delete_calendar_event", lambda event_id: {"consent": True, "connected": True, "ok": True})

    result = tool_calling.execute_tool("delete_calendar_event", {"summary_hint": "manger"})

    assert result == {"ok": True, "deleted_summary": "Manger"}


# =============================================================================
# _consent_gated_error — texte spécifique au fournisseur
# =============================================================================

def test_consent_gated_error_mentions_google_by_default():
    error = tool_calling._consent_gated_error({"consent": False})
    assert "Google Agenda" in error["error"]


def test_consent_gated_error_mentions_outlook_when_requested():
    error = tool_calling._consent_gated_error({"consent": False}, provider="outlook")
    assert "Outlook" in error["error"]


def test_consent_gated_error_none_when_both_gates_open():
    assert tool_calling._consent_gated_error({"consent": True, "connected": True}, provider="outlook") is None


# =============================================================================
# _build_outlook_recurrence
# =============================================================================

def test_build_outlook_recurrence_none_returns_none():
    assert tool_calling._build_outlook_recurrence("none", datetime(2026, 7, 24)) is None


def test_build_outlook_recurrence_weekly():
    result = tool_calling._build_outlook_recurrence("weekly", datetime(2026, 7, 24))
    assert result["pattern"] == {"type": "weekly", "interval": 1}
    assert result["range"] == {"type": "noEnd", "startDate": "2026-07-24"}
