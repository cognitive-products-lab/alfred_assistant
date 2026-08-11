"""
PROJECT      : ALFRED
BLOCK        : GLOBAL — Intégrations externes
FILE         : tests/integrations_tests/test_outlook_calendar_client.py
ROLE         : Tests unitaires src/integrations/outlook_calendar_client.py

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-07-24
VERSION      : V1.0
STATUS       : TESTED

DESCRIPTION :
Aucun test ne touche le réseau réel — requests.get/post/patch/delete sont
monkeypatchés avec une fausse réponse HTTP. Même esprit que
test_google_calendar_client.py (qui monkeypatche googleapiclient), adapté à
l'appel REST direct utilisé ici.
"""

from unittest.mock import MagicMock

import pytest
import requests

from src.integrations import outlook_calendar_client as occ


class _FakeResponse:
    def __init__(self, json_data, status_code=200, raise_exc=None):
        self._json_data = json_data
        self.status_code = status_code
        self._raise_exc = raise_exc

    def json(self):
        return self._json_data

    def raise_for_status(self):
        if self._raise_exc:
            raise self._raise_exc


# =============================================================================
# list_upcoming_events
# =============================================================================

def test_list_upcoming_events_normalizes_timed_event(monkeypatch):
    raw = {"value": [{
        "id": "evt1",
        "subject": "Réunion design",
        "start": {"dateTime": "2026-07-24T15:00:00.0000000"},
        "end": {"dateTime": "2026-07-24T16:00:00.0000000"},
        "location": {"displayName": "Bureau"},
        "isAllDay": False,
    }]}
    monkeypatch.setattr(requests, "get", lambda *a, **kw: _FakeResponse(raw))

    result = occ.list_upcoming_events(access_token="fake-token")

    assert result == [{
        "id": "evt1",
        "summary": "Réunion design",
        "start": "2026-07-24T15:00:00.0000000",
        "end": "2026-07-24T16:00:00.0000000",
        "location": "Bureau",
        "all_day": False,
        "recurring_event_id": None,
    }]


def test_list_upcoming_events_normalizes_all_day_event(monkeypatch):
    raw = {"value": [{
        "id": "evt2",
        "subject": "Anniversaire",
        "start": {"dateTime": "2026-07-25T00:00:00.0000000"},
        "end": {"dateTime": "2026-07-26T00:00:00.0000000"},
        "isAllDay": True,
    }]}
    monkeypatch.setattr(requests, "get", lambda *a, **kw: _FakeResponse(raw))

    result = occ.list_upcoming_events(access_token="fake-token")

    assert result[0]["all_day"] is True
    assert result[0]["location"] is None


def test_list_upcoming_events_returns_empty_list_when_no_items(monkeypatch):
    monkeypatch.setattr(requests, "get", lambda *a, **kw: _FakeResponse({"value": []}))
    assert occ.list_upcoming_events(access_token="fake-token") == []


def test_list_upcoming_events_wraps_request_exception(monkeypatch):
    def fake_get(*a, **kw):
        raise requests.RequestException("boom")
    monkeypatch.setattr(requests, "get", fake_get)

    with pytest.raises(occ.OutlookCalendarError):
        occ.list_upcoming_events(access_token="fake-token")


def test_list_upcoming_events_wraps_http_error(monkeypatch):
    def fake_get(*a, **kw):
        return _FakeResponse({}, status_code=401, raise_exc=requests.HTTPError("unauthorized"))
    monkeypatch.setattr(requests, "get", fake_get)

    with pytest.raises(occ.OutlookCalendarError):
        occ.list_upcoming_events(access_token="fake-token")


# =============================================================================
# create_event
# =============================================================================

def test_create_event_normalizes_result(monkeypatch):
    created = {
        "id": "evt3",
        "subject": "Nouveau rendez-vous",
        "start": {"dateTime": "2026-07-24T09:00:00.0000000"},
        "end": {"dateTime": "2026-07-24T10:00:00.0000000"},
        "location": {"displayName": "Salle A"},
    }
    monkeypatch.setattr(requests, "post", lambda *a, **kw: _FakeResponse(created))

    result = occ.create_event(
        access_token="fake-token",
        summary="Nouveau rendez-vous",
        start_iso="2026-07-24T09:00:00",
        end_iso="2026-07-24T10:00:00",
        location="Salle A",
    )

    assert result["id"] == "evt3"
    assert result["summary"] == "Nouveau rendez-vous"
    assert result["location"] == "Salle A"


def test_create_event_includes_recurrence_in_body(monkeypatch):
    captured = {}

    def fake_post(url, headers, json, timeout):
        captured["body"] = json
        return _FakeResponse({"id": "evt4", "subject": "Manger", "start": {}, "end": {}})

    monkeypatch.setattr(requests, "post", fake_post)

    recurrence = {"pattern": {"type": "daily", "interval": 1}, "range": {"type": "noEnd", "startDate": "2026-07-24"}}
    occ.create_event(
        access_token="fake-token", summary="Manger",
        start_iso="2026-07-24T19:00:00", end_iso="2026-07-24T19:15:00",
        recurrence=recurrence,
    )

    assert captured["body"]["recurrence"] == recurrence


def test_create_event_wraps_request_exception(monkeypatch):
    def fake_post(*a, **kw):
        raise requests.RequestException("boom")
    monkeypatch.setattr(requests, "post", fake_post)

    with pytest.raises(occ.OutlookCalendarError):
        occ.create_event(access_token="fake-token", summary="Titre", start_iso="2026-07-24T09:00:00", end_iso="2026-07-24T10:00:00")


# =============================================================================
# update_event
# =============================================================================

def test_update_event_sends_only_provided_fields(monkeypatch):
    captured = {}

    def fake_patch(url, headers, json, timeout):
        captured["url"] = url
        captured["body"] = json
        return _FakeResponse({"id": "evt5", "subject": "Manger", "start": {"dateTime": "2026-07-25T20:00:00"}, "end": {"dateTime": "2026-07-25T20:15:00"}})

    monkeypatch.setattr(requests, "patch", fake_patch)

    result = occ.update_event(access_token="fake-token", event_id="evt5", start_iso="2026-07-25T20:00:00", end_iso="2026-07-25T20:15:00")

    assert "evt5" in captured["url"]
    assert "subject" not in captured["body"]
    assert captured["body"]["start"]["dateTime"] == "2026-07-25T20:00:00"
    assert result["id"] == "evt5"


def test_update_event_wraps_request_exception(monkeypatch):
    def fake_patch(*a, **kw):
        raise requests.RequestException("boom")
    monkeypatch.setattr(requests, "patch", fake_patch)

    with pytest.raises(occ.OutlookCalendarError):
        occ.update_event(access_token="fake-token", event_id="evt6", summary="Nouveau titre")


# =============================================================================
# delete_event
# =============================================================================

def test_delete_event_calls_api(monkeypatch):
    captured = {}

    def fake_delete(url, headers, timeout):
        captured["url"] = url
        return _FakeResponse({})

    monkeypatch.setattr(requests, "delete", fake_delete)

    occ.delete_event(access_token="fake-token", event_id="evt7")
    assert "evt7" in captured["url"]


def test_delete_event_wraps_request_exception(monkeypatch):
    def fake_delete(*a, **kw):
        raise requests.RequestException("boom")
    monkeypatch.setattr(requests, "delete", fake_delete)

    with pytest.raises(occ.OutlookCalendarError):
        occ.delete_event(access_token="fake-token", event_id="evt8")


# =============================================================================
# find_event
# =============================================================================

def test_find_event_matches_case_insensitive_and_dedupes_recurring_series(monkeypatch):
    raw = {"value": [
        {"id": "s1_20260724", "seriesMasterId": "s1", "subject": "Manger",
         "start": {"dateTime": "2026-07-24T19:00:00"}, "end": {"dateTime": "2026-07-24T19:15:00"}},
        {"id": "s1_20260725", "seriesMasterId": "s1", "subject": "Manger",
         "start": {"dateTime": "2026-07-25T19:00:00"}, "end": {"dateTime": "2026-07-25T19:15:00"}},
        {"id": "evt9", "subject": "Dentiste",
         "start": {"dateTime": "2026-07-26T10:00:00"}, "end": {"dateTime": "2026-07-26T10:30:00"}},
    ]}
    monkeypatch.setattr(requests, "get", lambda *a, **kw: _FakeResponse(raw))

    matches = occ.find_event(access_token="fake-token", summary_hint="manger")

    assert len(matches) == 1
    assert matches[0]["id"] == "s1"


def test_find_event_returns_empty_for_no_match(monkeypatch):
    monkeypatch.setattr(requests, "get", lambda *a, **kw: _FakeResponse({"value": []}))
    assert occ.find_event(access_token="fake-token", summary_hint="inexistant") == []


def test_find_event_returns_empty_for_blank_hint(monkeypatch):
    assert occ.find_event(access_token="fake-token", summary_hint="   ") == []
