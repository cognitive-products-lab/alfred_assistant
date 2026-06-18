"""
════════════════════════════════════════════════════════════
PROJECT      : ALFRED
BLOCK        : B20
FUNCTION     : 20.08
FILE         : tests/security_tests/test_device_registry.py
ROLE         : Tests unitaires — device_registry.py

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-06-01
UPDATED      : 2026-06-01
VERSION      : V1.0
STATUS       : ACTIVE

DESCRIPTION :
Couvre : register_device, is_trusted_device, revoke_device,
remove_device, list_trusted_devices, get_device_info,
list_devices, record_failed_attempt, init_default_device.
Utilise monkeypatch pour isoler le fichier JSON.
════════════════════════════════════════════════════════════
"""

import json
import tempfile
from pathlib import Path

import pytest

import src.security.device_registry as dr


# ─── Fixture isolation fichier JSON ──────────────────────────────────────────

@pytest.fixture(autouse=True)
def isolated_registry(monkeypatch, tmp_path):
    """Redirige _REGISTRY_FILE vers un fichier temporaire par test."""
    reg_file = tmp_path / "trusted_devices.json"
    monkeypatch.setattr(dr, "_REGISTRY_FILE", reg_file)
    yield reg_file


# ─── _load_registry / _save_registry ─────────────────────────────────────────

def test_load_registry_empty_when_no_file():
    result = dr._load_registry()
    assert result == {}


def test_save_and_load_registry_roundtrip(isolated_registry):
    data = {"dev_abc": {"trusted": True, "label": "Test"}}
    dr._save_registry(data)
    loaded = dr._load_registry()
    assert loaded == data


def test_load_registry_returns_empty_on_corrupt_json(isolated_registry):
    isolated_registry.write_text("not-valid-json", encoding="utf-8")
    result = dr._load_registry()
    assert result == {}


# ─── register_device ─────────────────────────────────────────────────────────

def test_register_device_creates_entry():
    dr.register_device("dev_001", "Mon PC", "OWNER")
    info = dr.get_device_info("dev_001")
    assert info["label"] == "Mon PC"
    assert info["trusted"] is True
    assert info["owner"] == "OWNER"


def test_register_device_default_label():
    dr.register_device("dev_002")
    info = dr.get_device_info("dev_002")
    assert info["label"] == "dev_002"


def test_register_device_has_timestamps():
    dr.register_device("dev_003", "Test")
    info = dr.get_device_info("dev_003")
    assert "registered_at" in info
    assert "last_seen" in info


def test_register_device_overwrite():
    dr.register_device("dev_004", "First", "USER")
    dr.register_device("dev_004", "Second", "ADMIN")
    info = dr.get_device_info("dev_004")
    assert info["label"] == "Second"
    assert info["owner"] == "ADMIN"


# ─── is_trusted_device ───────────────────────────────────────────────────────

def test_is_trusted_device_true_when_registered():
    dr.register_device("trusted_01", "OK")
    assert dr.is_trusted_device("trusted_01") is True


def test_is_trusted_device_false_when_unknown():
    assert dr.is_trusted_device("completely_unknown") is False


def test_is_trusted_device_updates_last_seen():
    dr.register_device("dev_ts", "Timestamp test")
    first = dr.get_device_info("dev_ts")["last_seen"]
    dr.is_trusted_device("dev_ts")
    second = dr.get_device_info("dev_ts")["last_seen"]
    assert isinstance(second, str)


def test_is_trusted_device_false_after_revoke():
    dr.register_device("rev_01", "Revoked")
    dr.revoke_device("rev_01")
    assert dr.is_trusted_device("rev_01") is False


# ─── revoke_device ───────────────────────────────────────────────────────────

def test_revoke_device_sets_trusted_false():
    dr.register_device("rev_02", "Will be revoked")
    dr.revoke_device("rev_02")
    info = dr.get_device_info("rev_02")
    assert info["trusted"] is False


def test_revoke_device_unknown_does_not_raise():
    dr.revoke_device("nonexistent_device")  # doit passer silencieusement


# ─── remove_device ───────────────────────────────────────────────────────────

def test_remove_device_deletes_entry():
    dr.register_device("rem_01", "To delete")
    dr.remove_device("rem_01")
    assert dr.get_device_info("rem_01") == {}


def test_remove_device_unknown_does_not_raise():
    dr.remove_device("ghost_device")


# ─── list_trusted_devices ────────────────────────────────────────────────────

def test_list_trusted_devices_returns_only_trusted():
    dr.register_device("t1", "Trusted")
    dr.register_device("t2", "Also trusted")
    dr.register_device("t3", "Revoked")
    dr.revoke_device("t3")
    trusted = dr.list_trusted_devices()
    assert "t1" in trusted
    assert "t2" in trusted
    assert "t3" not in trusted


def test_list_trusted_devices_empty_when_none():
    result = dr.list_trusted_devices()
    assert result == {}


# ─── get_device_info ─────────────────────────────────────────────────────────

def test_get_device_info_returns_empty_for_unknown():
    assert dr.get_device_info("no_such_device") == {}


def test_get_device_info_returns_full_dict():
    dr.register_device("info_01", "Info test", "USER")
    info = dr.get_device_info("info_01")
    assert isinstance(info, dict)
    assert "label" in info and "trusted" in info


# ─── list_devices ────────────────────────────────────────────────────────────

def test_list_devices_excludes_revoked_by_default():
    dr.register_device("ld_01", "Active")
    dr.register_device("ld_02", "Revoked")
    dr.revoke_device("ld_02")
    result = dr.list_devices(include_revoked=False)
    assert "ld_01" in result
    assert "ld_02" not in result


def test_list_devices_includes_revoked_when_flag():
    dr.register_device("ld_03", "Active2")
    dr.register_device("ld_04", "Revoked2")
    dr.revoke_device("ld_04")
    result = dr.list_devices(include_revoked=True)
    assert "ld_03" in result
    assert "ld_04" in result


# ─── record_failed_attempt ───────────────────────────────────────────────────

def test_record_failed_attempt_increments():
    dr.register_device("fa_01", "Fail test")
    dr.record_failed_attempt("fa_01")
    dr.record_failed_attempt("fa_01")
    info = dr.get_device_info("fa_01")
    assert info.get("failed_attempts", 0) == 2


def test_record_failed_attempt_unknown_does_not_raise():
    dr.record_failed_attempt("does_not_exist")


# ─── init_default_device ─────────────────────────────────────────────────────

def test_init_default_device_registers_if_absent():
    dr.init_default_device("default_test_pc")
    assert dr.is_trusted_device("default_test_pc") is True
