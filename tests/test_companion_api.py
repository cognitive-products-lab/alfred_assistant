"""
PROJECT : ALFRED
BLOCK   : Client compagnon Android (PoC)
FILE    : tests/test_companion_api.py
ROLE    : Tests de l'API compagnon locale (interface/companion_api.py)
          consommée par ALFRED_ANDROID.
"""

from __future__ import annotations

import json
import os

import pytest
from fastapi.testclient import TestClient

os.environ.setdefault("COMPANION_API_TOKEN", "test-token-do-not-use-in-prod")

from interface.companion_api import COMPANION_API_TOKEN, app  # noqa: E402

client = TestClient(app)


def test_status_without_token_is_rejected():
    response = client.get("/api/status")
    assert response.status_code == 401


def test_status_with_wrong_token_is_rejected():
    response = client.get("/api/status", headers={"Authorization": "Bearer wrong-token"})
    assert response.status_code == 401


def test_status_with_valid_token_returns_online():
    response = client.get(
        "/api/status", headers={"Authorization": f"Bearer {COMPANION_API_TOKEN}"}
    )
    assert response.status_code == 200
    body = response.json()
    assert body["product"] == "ALFRED"
    assert body["status"] == "online"
    assert "timestamp" in body


def test_notifications_requires_token():
    response = client.get("/api/notifications")
    assert response.status_code == 401


def test_notifications_returns_active_reminders(tmp_path, monkeypatch):
    reminders_dir = tmp_path / "memory"
    reminders_dir.mkdir()
    reminders_file = reminders_dir / "reminders.json"
    reminders_file.write_text(
        json.dumps(
            [
                {"id": "1", "title": "Actif", "due_at": "2026-08-01T00:00:00", "active": True},
                {"id": "2", "title": "Inactif", "due_at": "2026-08-02T00:00:00", "active": False},
            ]
        ),
        encoding="utf-8",
    )

    import interface.companion_api as companion_api

    monkeypatch.setattr(companion_api.PATHS, "data_memory", tmp_path / "memory")

    response = client.get(
        "/api/notifications", headers={"Authorization": f"Bearer {COMPANION_API_TOKEN}"}
    )
    assert response.status_code == 200
    notifications = response.json()["notifications"]
    assert len(notifications) == 1
    assert notifications[0]["title"] == "Actif"
