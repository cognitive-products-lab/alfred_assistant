"""
PROJECT      : ALFRED
BLOCK        : GLOBAL — Intégrations externes
FILE         : tests/integrations_tests/test_outlook_auth.py
ROLE         : Tests unitaires src/integrations/outlook_auth.py

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-07-24
VERSION      : V1.0
STATUS       : TESTED

DESCRIPTION :
Même approche que test_google_auth.py : chiffrement réel monkeypatché par un
encodage réversible. msal.PublicClientApplication est remplacé par un faux
client configurable — aucun appel réseau réel, aucune fenêtre de navigateur.
"""

import json
import shutil
import tempfile
from pathlib import Path

import msal
import pytest

from src.integrations import outlook_auth as oa
from src.security import encryption_service


def _fake_encrypt(data: str) -> str:
    return "ENC:" + data


def _fake_decrypt(token: str) -> str:
    return token[len("ENC:"):] if token.startswith("ENC:") else ""


class _FakeCache:
    def __init__(self):
        self.has_state_changed = False
        self._state = ""

    def deserialize(self, blob):
        self._state = blob

    def serialize(self):
        return self._state or "{}"


class _FakeApp:
    """Simule msal.PublicClientApplication — comportement configurable par test."""

    accounts: list = []
    silent_result: dict | None = None
    interactive_result: dict | None = None

    def __init__(self, client_id, authority=None, token_cache=None):
        self.client_id = client_id
        self.authority = authority
        self.token_cache = token_cache

    def get_accounts(self):
        return _FakeApp.accounts

    def acquire_token_silent(self, scopes, account):
        return _FakeApp.silent_result

    def acquire_token_interactive(self, scopes):
        return _FakeApp.interactive_result


@pytest.fixture(autouse=True)
def _isolated_files(monkeypatch):
    tmp_dir = Path(tempfile.mkdtemp(prefix="alfred_outlook_auth_"))
    token_file = tmp_dir / "outlook_calendar_token.json"
    config_file = tmp_dir / "outlook_client_config.json"
    monkeypatch.setattr(oa, "_TOKEN_CACHE_FILE", token_file)
    monkeypatch.setattr(oa, "_CLIENT_CONFIG_FILE", config_file)
    monkeypatch.setattr(encryption_service, "encrypt", _fake_encrypt)
    monkeypatch.setattr(encryption_service, "decrypt", _fake_decrypt)
    monkeypatch.setattr(msal, "PublicClientApplication", _FakeApp)
    monkeypatch.setattr(msal, "SerializableTokenCache", _FakeCache)
    _FakeApp.accounts = []
    _FakeApp.silent_result = None
    _FakeApp.interactive_result = None
    yield token_file, config_file
    shutil.rmtree(tmp_dir, ignore_errors=True)


def _write_config(config_file: Path, client_id="test-client-id", tenant="common"):
    config_file.parent.mkdir(parents=True, exist_ok=True)
    config_file.write_text(json.dumps({"client_id": client_id, "tenant": tenant}), encoding="utf-8")


def test_is_connected_false_when_no_client_config():
    assert oa.is_connected() is False


def test_get_credentials_none_when_no_client_config():
    assert oa.get_credentials() is None


def test_start_auth_flow_fails_cleanly_without_client_config():
    result = oa.start_auth_flow()
    assert result["success"] is False
    assert "outlook_client_config.json" in result["error"]


def test_get_credentials_none_when_no_accounts(_isolated_files):
    _, config_file = _isolated_files
    _write_config(config_file)
    _FakeApp.accounts = []
    assert oa.get_credentials() is None


def test_get_credentials_returns_access_token(_isolated_files):
    _, config_file = _isolated_files
    _write_config(config_file)
    _FakeApp.accounts = [{"username": "celine@example.com"}]
    _FakeApp.silent_result = {"access_token": "fake-token-123"}
    assert oa.get_credentials() == "fake-token-123"


def test_is_connected_true_with_valid_silent_token(_isolated_files):
    _, config_file = _isolated_files
    _write_config(config_file)
    _FakeApp.accounts = [{"username": "celine@example.com"}]
    _FakeApp.silent_result = {"access_token": "fake-token-123"}
    assert oa.is_connected() is True


def test_get_credentials_none_when_silent_result_has_no_token(_isolated_files):
    _, config_file = _isolated_files
    _write_config(config_file)
    _FakeApp.accounts = [{"username": "celine@example.com"}]
    _FakeApp.silent_result = {"error": "invalid_grant"}
    assert oa.get_credentials() is None


def test_start_auth_flow_success(_isolated_files):
    _, config_file = _isolated_files
    _write_config(config_file)
    _FakeApp.interactive_result = {"access_token": "fake-token-123"}
    result = oa.start_auth_flow()
    assert result["success"] is True
    assert result["error"] is None


def test_start_auth_flow_reports_graph_error(_isolated_files):
    _, config_file = _isolated_files
    _write_config(config_file)
    _FakeApp.interactive_result = {"error": "access_denied", "error_description": "L'utilisateur a refusé."}
    result = oa.start_auth_flow()
    assert result["success"] is False
    assert "refusé" in result["error"]


def test_disconnect_removes_token_file(_isolated_files):
    token_file, _ = _isolated_files
    token_file.parent.mkdir(parents=True, exist_ok=True)
    token_file.write_text("ENC:{}", encoding="utf-8")
    assert token_file.exists()
    oa.disconnect()
    assert not token_file.exists()


def test_disconnect_is_noop_when_no_token_file():
    oa.disconnect()  # ne doit pas lever d'exception
