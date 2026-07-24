"""
PROJECT      : ALFRED
BLOCK        : 14.01/14.03/14.05 — Domotique, gestion des équipements
FILE         : tests/integrations_tests/test_google_home_adapter.py
ROLE         : Tests unitaires src/v4/integration/google_home_adapter.py

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-07-23
VERSION      : V1.0
STATUS       : TESTED

DESCRIPTION :
Aucun test ne touche le réseau réel ni l'API Google — _build_service (seul
point d'entrée vers googleapiclient) est monkeypatché, même approche que
tests/integrations_tests/test_google_calendar_client.py.
"""

from unittest.mock import MagicMock

import pytest

from src.v4.integration import google_home_adapter as gha


def _fake_service(list_return=None, command_return=None):
    service = MagicMock()
    if list_return is not None:
        service.enterprises.return_value.devices.return_value.list.return_value.execute.return_value = list_return
    if command_return is not None:
        service.enterprises.return_value.devices.return_value.executeCommand.return_value.execute.return_value = command_return
    return service


# =============================================================================
# local_type_for
# =============================================================================

def test_local_type_for_known_sdm_type():
    assert gha.local_type_for("sdm.devices.types.THERMOSTAT") == "thermostat"


def test_local_type_for_unknown_sdm_type_falls_back_to_suffix():
    assert gha.local_type_for("sdm.devices.types.SPEAKER") == "speaker"


# =============================================================================
# list_devices / normalisation
# =============================================================================

def test_list_devices_normalizes_online_thermostat(monkeypatch):
    raw = {"devices": [{
        "name": "enterprises/proj-1/devices/device-1",
        "type": "sdm.devices.types.THERMOSTAT",
        "traits": {
            "sdm.devices.traits.Info": {"customName": "Salon"},
            "sdm.devices.traits.Connectivity": {"status": "ONLINE"},
            "sdm.devices.traits.ThermostatMode": {"mode": "HEAT", "availableModes": ["HEAT", "COOL", "OFF"]},
            "sdm.devices.traits.ThermostatTemperatureSetpoint": {"heatCelsius": 20.0},
        },
        "parentRelations": [{"parent": "enterprises/proj-1/structures/s1/rooms/r1", "displayName": "Salon"}],
    }]}
    monkeypatch.setattr(gha, "_build_service", lambda creds: _fake_service(list_return=raw))

    result = gha.list_devices(creds=object(), project_id="proj-1")

    assert len(result) == 1
    d = result[0]
    assert d["id"] == "device-1"
    assert d["local_type"] == "thermostat"
    assert d["room"] == "Salon"
    assert d["custom_name"] == "Salon"
    assert d["online"] is True


def test_list_devices_normalizes_offline_device_without_parent(monkeypatch):
    raw = {"devices": [{
        "name": "enterprises/proj-1/devices/device-2",
        "type": "sdm.devices.types.CAMERA",
        "traits": {"sdm.devices.traits.Connectivity": {"status": "OFFLINE"}},
    }]}
    monkeypatch.setattr(gha, "_build_service", lambda creds: _fake_service(list_return=raw))

    result = gha.list_devices(creds=object(), project_id="proj-1")

    assert result[0]["online"] is False
    assert result[0]["room"] is None
    assert result[0]["local_type"] == "camera"


def test_list_devices_returns_empty_list_when_no_devices(monkeypatch):
    monkeypatch.setattr(gha, "_build_service", lambda creds: _fake_service(list_return={}))
    assert gha.list_devices(creds=object(), project_id="proj-1") == []


def test_list_devices_wraps_http_error(monkeypatch):
    from googleapiclient.errors import HttpError

    def fake_service_raising(creds):
        service = MagicMock()
        service.enterprises.return_value.devices.return_value.list.return_value.execute.side_effect = HttpError(
            resp=MagicMock(status=403), content=b"forbidden"
        )
        return service

    monkeypatch.setattr(gha, "_build_service", fake_service_raising)
    with pytest.raises(gha.HomeError):
        gha.list_devices(creds=object(), project_id="proj-1")


# =============================================================================
# available_commands
# =============================================================================

def test_available_commands_thermostat_with_both_traits():
    device = {"traits": {
        "sdm.devices.traits.ThermostatMode": {"mode": "HEAT"},
        "sdm.devices.traits.ThermostatTemperatureSetpoint": {"heatCelsius": 20.0},
    }}
    assert gha.available_commands(device) == ["SetMode", "SetHeat", "SetCool"]


def test_available_commands_camera_has_no_commands():
    device = {"traits": {"sdm.devices.traits.Connectivity": {"status": "ONLINE"}}}
    assert gha.available_commands(device) == []


# =============================================================================
# execute_command
# =============================================================================

def test_execute_command_unknown_command_raises():
    with pytest.raises(gha.HomeError):
        gha.execute_command(object(), "proj-1", "device-1", "TurnPurple", {})


def test_execute_command_success(monkeypatch):
    monkeypatch.setattr(gha, "_build_service", lambda creds: _fake_service(command_return={"result": "ok"}))
    result = gha.execute_command(object(), "proj-1", "device-1", "SetMode", {"mode": "HEAT"})
    assert result == {"result": "ok"}


def test_execute_command_wraps_http_error(monkeypatch):
    from googleapiclient.errors import HttpError

    def fake_service_raising(creds):
        service = MagicMock()
        service.enterprises.return_value.devices.return_value.executeCommand.return_value.execute.side_effect = HttpError(
            resp=MagicMock(status=400), content=b"bad request"
        )
        return service

    monkeypatch.setattr(gha, "_build_service", fake_service_raising)
    with pytest.raises(gha.HomeError):
        gha.execute_command(object(), "proj-1", "device-1", "SetMode", {"mode": "HEAT"})
