"""
PROJECT      : ALFRED
BLOCK        : B15
FILE         : tests/integrations_tests/test_google_home_data.py
ROLE         : Tests unitaires src/ui/google_home_data.py

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-07-23
VERSION      : V1.0
STATUS       : TESTED

DESCRIPTION :
Vérifie les trois portes (consentement -> project_id -> connexion) avant
tout appel, la synchronisation réelle de config/v4/home_devices.json et
data/v4/device_registry.json (isolée en tmp_path — jamais les vrais fichiers
du projet), et l'intégration avec src/security/human_validation.py (chaque
commande exécutée doit laisser une trace "approved" dans
data/security/pending_approvals.json).
"""

import json

import paths
from src.security import human_validation
from src.ui import google_home_data as ghd
from src.ui import google_home_prefs
from src.integrations import google_home_auth
from src.v4.integration import google_home_adapter


def _patch_v4_paths(monkeypatch, tmp_path):
    monkeypatch.setattr(paths.PATHS, "config_v4", tmp_path / "config_v4")
    monkeypatch.setattr(paths.PATHS, "data_v4", tmp_path / "data_v4")


# =============================================================================
# get_home_state — gates
# =============================================================================

def test_get_home_state_no_consent(monkeypatch):
    monkeypatch.setattr(google_home_prefs, "load_google_home_prefs", lambda: {"consent": False, "project_id": None})
    assert ghd.get_home_state() == {"consent": False}


def test_get_home_state_no_project_id(monkeypatch):
    monkeypatch.setattr(google_home_prefs, "load_google_home_prefs", lambda: {"consent": True, "project_id": None})
    result = ghd.get_home_state()
    assert result == {"consent": True, "connected": False, "no_project_id": True}


def test_get_home_state_not_connected(monkeypatch):
    monkeypatch.setattr(google_home_prefs, "load_google_home_prefs", lambda: {"consent": True, "project_id": "proj-1"})
    monkeypatch.setattr(google_home_auth, "get_credentials", lambda: None)
    result = ghd.get_home_state()
    assert result == {"consent": True, "connected": False}


# =============================================================================
# get_home_state — succès, synchronisation du registre local
# =============================================================================

def test_get_home_state_success_syncs_registry(monkeypatch, tmp_path):
    _patch_v4_paths(monkeypatch, tmp_path)
    monkeypatch.setattr(google_home_prefs, "load_google_home_prefs", lambda: {"consent": True, "project_id": "proj-1"})
    monkeypatch.setattr(google_home_auth, "get_credentials", lambda: object())

    fake_devices = [{
        "id": "device-1", "name": "enterprises/proj-1/devices/device-1",
        "sdm_type": "sdm.devices.types.THERMOSTAT", "local_type": "thermostat",
        "room": "Salon", "custom_name": "Salon", "online": True,
        "traits": {"sdm.devices.traits.ThermostatMode": {"mode": "HEAT"}},
    }]
    monkeypatch.setattr(google_home_adapter, "list_devices", lambda creds, project_id: fake_devices)

    result = ghd.get_home_state()

    assert result["consent"] is True
    assert result["connected"] is True
    assert result["ok"] is True
    assert result["devices"][0]["available_commands"] == ["SetMode"]

    catalog = json.loads((tmp_path / "config_v4" / "home_devices.json").read_text(encoding="utf-8"))
    assert "thermostat" in catalog["supported_types"]
    assert catalog["declared_devices"][0]["id"] == "device-1"

    registry = json.loads((tmp_path / "data_v4" / "device_registry.json").read_text(encoding="utf-8"))
    assert registry["state"]["device-1"]["online"] is True


def test_get_home_state_reports_home_error(monkeypatch, tmp_path):
    _patch_v4_paths(monkeypatch, tmp_path)
    monkeypatch.setattr(google_home_prefs, "load_google_home_prefs", lambda: {"consent": True, "project_id": "proj-1"})
    monkeypatch.setattr(google_home_auth, "get_credentials", lambda: object())

    def raise_home_error(creds, project_id):
        raise google_home_adapter.HomeError("panne simulée")

    monkeypatch.setattr(google_home_adapter, "list_devices", raise_home_error)

    result = ghd.get_home_state()
    assert result["ok"] is False
    assert result["error"] == "panne simulée"


# =============================================================================
# execute_home_command — audit trail human_validation
# =============================================================================

def test_execute_home_command_writes_approved_audit_entry(monkeypatch, tmp_path):
    _patch_v4_paths(monkeypatch, tmp_path)
    monkeypatch.setattr(human_validation, "APPROVALS_FILE", tmp_path / "pending_approvals.json")
    monkeypatch.setattr(google_home_prefs, "load_google_home_prefs", lambda: {"consent": True, "project_id": "proj-1"})
    monkeypatch.setattr(google_home_auth, "get_credentials", lambda: object())
    monkeypatch.setattr(google_home_adapter, "execute_command", lambda creds, project_id, device_id, command, params: {"ok": True})
    monkeypatch.setattr(google_home_adapter, "list_devices", lambda creds, project_id: [])

    ghd.execute_home_command("device-1", "SetMode", {"mode": "HEAT"})

    approvals = human_validation.list_all()
    assert len(approvals) == 1
    assert approvals[0]["status"] == "approved"
    assert approvals[0]["action"] == "SetMode"
    assert approvals[0]["resource"] == "home_device:device-1"


def test_execute_home_command_no_consent_skips_everything(monkeypatch):
    monkeypatch.setattr(google_home_prefs, "load_google_home_prefs", lambda: {"consent": False, "project_id": None})
    result = ghd.execute_home_command("device-1", "SetMode", {"mode": "HEAT"})
    assert result == {"consent": False}
