"""
════════════════════════════════════════════════════════════
PROJECT      : ALFRED
BLOCK        : B24
FUNCTION     : 24.02 — Intégration API compagnon
FILE         : tests/dashboard_tests/test_companion_api.py
ROLE         : Tests de interface/companion_api.py (point C4-F du plan d'action)

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-07-13
VERSION      : V1.0
STATUS       : ACTIVE

DESCRIPTION :
Vérifie le contrat attendu par le client Android (CompanionApiService.kt) :
  - 401 sans jeton ou avec un jeton invalide
  - 200 avec le bon jeton, format de réponse conforme à Models.kt
  - /api/notifications reflète bien les rappels actifs de ReminderEngine
════════════════════════════════════════════════════════════
"""

import os

import pytest

pytest.importorskip("fastapi")

from fastapi.testclient import TestClient  # noqa: E402

os.environ["COMPANION_API_TOKEN"] = "test-token-companion-api"

from interface.companion_api import app  # noqa: E402

client = TestClient(app)
VALID_HEADER = {"Authorization": "Bearer test-token-companion-api"}


# ─── Authentification ──────────────────────────────────────────────────────

def test_status_without_token_returns_401():
    response = client.get("/api/status")
    assert response.status_code == 401


def test_status_with_wrong_token_returns_401():
    response = client.get("/api/status", headers={"Authorization": "Bearer wrong"})
    assert response.status_code == 401


def test_notifications_without_token_returns_401():
    response = client.get("/api/notifications")
    assert response.status_code == 401


# ─── /api/status ────────────────────────────────────────────────────────────

def test_status_with_valid_token_returns_200():
    response = client.get("/api/status", headers=VALID_HEADER)
    assert response.status_code == 200


def test_status_response_shape_matches_android_client():
    """Doit correspondre exactement à StatusResponse (Models.kt) : product, status, timestamp."""
    data = client.get("/api/status", headers=VALID_HEADER).json()
    assert set(data.keys()) == {"product", "status", "timestamp"}
    assert isinstance(data["product"], str)
    assert isinstance(data["status"], str)
    assert isinstance(data["timestamp"], str)


# ─── /api/notifications ─────────────────────────────────────────────────────

def test_notifications_with_valid_token_returns_200():
    response = client.get("/api/notifications", headers=VALID_HEADER)
    assert response.status_code == 200


def test_notifications_response_shape_matches_android_client():
    """Doit correspondre exactement à NotificationsResponse/Reminder (Models.kt)."""
    data = client.get("/api/notifications", headers=VALID_HEADER).json()
    assert set(data.keys()) == {"notifications"}
    assert isinstance(data["notifications"], list)
    for item in data["notifications"]:
        assert set(item.keys()) == {"id", "title", "due_at", "recurrent", "active"}


def test_notifications_reflects_real_reminder_engine_data():
    """Les rappels retournés doivent correspondre aux rappels actifs réels d'ALFRED_PC."""
    from src.v3.proactive.reminder_engine import ReminderEngine

    expected = {r.id for r in ReminderEngine().get_active()}
    data = client.get("/api/notifications", headers=VALID_HEADER).json()
    returned = {n["id"] for n in data["notifications"]}
    assert returned == expected
