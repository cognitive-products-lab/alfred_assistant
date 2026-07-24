"""
PROJECT      : ALFRED
BLOCK        : GLOBAL — Intégrations externes
FILE         : tests/integrations_tests/test_google_calendar_client.py
ROLE         : Tests unitaires src/integrations/google_calendar_client.py

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-07-23
VERSION      : V1.0
STATUS       : TESTED

DESCRIPTION :
Aucun test ne touche le réseau réel ni l'API Google — _build_service (seul
point d'entrée vers googleapiclient) est monkeypatché partout, avec un faux
service imitant la chaîne .events().list(...).execute() / .insert(...).execute().
"""

from unittest.mock import MagicMock

import pytest

from src.integrations import google_calendar_client as gcc


def _fake_service(list_return=None, insert_return=None):
    service = MagicMock()
    if list_return is not None:
        service.events.return_value.list.return_value.execute.return_value = list_return
    if insert_return is not None:
        service.events.return_value.insert.return_value.execute.return_value = insert_return
    return service


# =============================================================================
# list_upcoming_events
# =============================================================================

def test_list_upcoming_events_normalizes_timed_event(monkeypatch):
    raw = {"items": [{
        "id": "evt1",
        "summary": "Réunion design",
        "start": {"dateTime": "2026-07-24T15:00:00+02:00"},
        "end": {"dateTime": "2026-07-24T16:00:00+02:00"},
        "location": "Bureau",
    }]}
    monkeypatch.setattr(gcc, "_build_service", lambda creds: _fake_service(list_return=raw))

    result = gcc.list_upcoming_events(creds=object())

    assert result == [{
        "id": "evt1",
        "summary": "Réunion design",
        "start": "2026-07-24T15:00:00+02:00",
        "end": "2026-07-24T16:00:00+02:00",
        "location": "Bureau",
        "all_day": False,
        "recurring_event_id": None,
    }]


def test_list_upcoming_events_normalizes_all_day_event(monkeypatch):
    raw = {"items": [{
        "id": "evt2",
        "summary": "Anniversaire",
        "start": {"date": "2026-07-25"},
        "end": {"date": "2026-07-26"},
    }]}
    monkeypatch.setattr(gcc, "_build_service", lambda creds: _fake_service(list_return=raw))

    result = gcc.list_upcoming_events(creds=object())

    assert result[0]["all_day"] is True
    assert result[0]["location"] is None


def test_list_upcoming_events_returns_empty_list_when_no_items(monkeypatch):
    monkeypatch.setattr(gcc, "_build_service", lambda creds: _fake_service(list_return={}))
    assert gcc.list_upcoming_events(creds=object()) == []


def test_list_upcoming_events_wraps_http_error(monkeypatch):
    from googleapiclient.errors import HttpError

    def fake_service_raising(creds):
        service = MagicMock()
        service.events.return_value.list.return_value.execute.side_effect = HttpError(
            resp=MagicMock(status=403), content=b"forbidden"
        )
        return service

    monkeypatch.setattr(gcc, "_build_service", fake_service_raising)
    with pytest.raises(gcc.CalendarError):
        gcc.list_upcoming_events(creds=object())


# =============================================================================
# create_event
# =============================================================================

def test_create_event_normalizes_result(monkeypatch):
    created = {
        "id": "evt3",
        "summary": "Nouveau rendez-vous",
        "start": {"dateTime": "2026-07-24T09:00:00Z"},
        "end": {"dateTime": "2026-07-24T10:00:00Z"},
        "location": "Salle A",
    }
    monkeypatch.setattr(gcc, "_build_service", lambda creds: _fake_service(insert_return=created))

    result = gcc.create_event(
        creds=object(),
        summary="Nouveau rendez-vous",
        start_iso="2026-07-24T09:00:00Z",
        end_iso="2026-07-24T10:00:00Z",
        location="Salle A",
    )

    assert result["id"] == "evt3"
    assert result["summary"] == "Nouveau rendez-vous"
    assert result["location"] == "Salle A"


def test_create_event_wraps_http_error(monkeypatch):
    from googleapiclient.errors import HttpError

    def fake_service_raising(creds):
        service = MagicMock()
        service.events.return_value.insert.return_value.execute.side_effect = HttpError(
            resp=MagicMock(status=400), content=b"bad request"
        )
        return service

    monkeypatch.setattr(gcc, "_build_service", fake_service_raising)
    with pytest.raises(gcc.CalendarError):
        gcc.create_event(object(), "Titre", "2026-07-24T09:00:00Z", "2026-07-24T10:00:00Z")


def test_create_event_includes_recurrence_and_timezone(monkeypatch):
    captured = {}

    def fake_service(creds):
        service = MagicMock()

        def fake_insert(calendarId, body):
            captured["body"] = body
            m = MagicMock()
            m.execute.return_value = {
                "id": "evt4", "summary": "Manger",
                "start": {"dateTime": "2026-07-24T19:00:00+02:00"},
                "end": {"dateTime": "2026-07-24T19:15:00+02:00"},
            }
            return m

        service.events.return_value.insert.side_effect = fake_insert
        return service

    monkeypatch.setattr(gcc, "_build_service", fake_service)

    gcc.create_event(
        object(), "Manger", "2026-07-24T19:00:00+02:00", "2026-07-24T19:15:00+02:00",
        recurrence=["RRULE:FREQ=DAILY"],
    )

    assert captured["body"]["start"]["timeZone"] == "Europe/Paris"
    assert captured["body"]["end"]["timeZone"] == "Europe/Paris"
    assert captured["body"]["recurrence"] == ["RRULE:FREQ=DAILY"]


# =============================================================================
# update_event
# =============================================================================

def test_update_event_sends_only_provided_fields(monkeypatch):
    captured = {}

    def fake_service(creds):
        service = MagicMock()

        def fake_patch(calendarId, eventId, body):
            captured["event_id"] = eventId
            captured["body"] = body
            m = MagicMock()
            m.execute.return_value = {
                "id": eventId, "summary": body.get("summary", "Manger"),
                "start": {"dateTime": "2026-07-25T20:00:00+02:00"},
                "end": {"dateTime": "2026-07-25T20:15:00+02:00"},
            }
            return m

        service.events.return_value.patch.side_effect = fake_patch
        return service

    monkeypatch.setattr(gcc, "_build_service", fake_service)

    result = gcc.update_event(object(), "evt5", start_iso="2026-07-25T20:00:00+02:00", end_iso="2026-07-25T20:15:00+02:00")

    assert captured["event_id"] == "evt5"
    assert "summary" not in captured["body"]
    assert captured["body"]["start"]["dateTime"] == "2026-07-25T20:00:00+02:00"
    assert result["id"] == "evt5"


def test_update_event_wraps_http_error(monkeypatch):
    from googleapiclient.errors import HttpError

    def fake_service_raising(creds):
        service = MagicMock()
        service.events.return_value.patch.return_value.execute.side_effect = HttpError(
            resp=MagicMock(status=404), content=b"not found"
        )
        return service

    monkeypatch.setattr(gcc, "_build_service", fake_service_raising)
    with pytest.raises(gcc.CalendarError):
        gcc.update_event(object(), "evt6", summary="Nouveau titre")


# =============================================================================
# delete_event
# =============================================================================

def test_delete_event_calls_api(monkeypatch):
    captured = {}

    def fake_service(creds):
        service = MagicMock()

        def fake_delete(calendarId, eventId):
            captured["event_id"] = eventId
            return MagicMock()

        service.events.return_value.delete.side_effect = fake_delete
        return service

    monkeypatch.setattr(gcc, "_build_service", fake_service)

    gcc.delete_event(object(), "evt7")
    assert captured["event_id"] == "evt7"


def test_delete_event_wraps_http_error(monkeypatch):
    from googleapiclient.errors import HttpError

    def fake_service_raising(creds):
        service = MagicMock()
        service.events.return_value.delete.return_value.execute.side_effect = HttpError(
            resp=MagicMock(status=404), content=b"not found"
        )
        return service

    monkeypatch.setattr(gcc, "_build_service", fake_service_raising)
    with pytest.raises(gcc.CalendarError):
        gcc.delete_event(object(), "evt8")


# =============================================================================
# find_event
# =============================================================================

def test_find_event_matches_case_insensitive_and_dedupes_recurring_series(monkeypatch):
    raw = {"items": [
        {"id": "s1_20260724", "recurringEventId": "s1", "summary": "Manger",
         "start": {"dateTime": "2026-07-24T19:00:00+02:00"}, "end": {"dateTime": "2026-07-24T19:15:00+02:00"}},
        {"id": "s1_20260725", "recurringEventId": "s1", "summary": "Manger",
         "start": {"dateTime": "2026-07-25T19:00:00+02:00"}, "end": {"dateTime": "2026-07-25T19:15:00+02:00"}},
        {"id": "evt9", "summary": "Dentiste",
         "start": {"dateTime": "2026-07-26T10:00:00+02:00"}, "end": {"dateTime": "2026-07-26T10:30:00+02:00"}},
    ]}
    monkeypatch.setattr(gcc, "_build_service", lambda creds: _fake_service(list_return=raw))

    matches = gcc.find_event(object(), "manger")

    assert len(matches) == 1
    assert matches[0]["id"] == "s1"


def test_find_event_returns_empty_for_no_match(monkeypatch):
    monkeypatch.setattr(gcc, "_build_service", lambda creds: _fake_service(list_return={"items": []}))
    assert gcc.find_event(object(), "inexistant") == []
