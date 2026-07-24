"""
PROJECT      : ALFRED
BLOCK        : GLOBAL — Intégrations externes
FILE         : tests/integrations_tests/test_google_home_auth.py
ROLE         : Tests unitaires src/integrations/google_home_auth.py

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-07-23
VERSION      : V1.0
STATUS       : TESTED

DESCRIPTION :
Le flux Device Access ne peut pas être testé via un vrai navigateur/serveur
local (redirection fixe vers https://www.google.com) — ces tests vérifient
la construction de l'URL d'autorisation et l'échange de code avec
urllib.request.urlopen monkeypatché (même technique que
tests/b15_tests/test_weather_client.py::test_get_json_wraps_url_error_as_weather_error).
Le chiffrement réel (Fernet) est monkeypatché par un encodage réversible
simple, comme tests/integrations_tests/test_google_auth.py.
"""

import json
import shutil
import tempfile
import urllib.error
from pathlib import Path

import pytest

from src.integrations import google_home_auth as gha
from src.security import encryption_service


def _fake_encrypt(data: str) -> str:
    return "ENC:" + data


def _fake_decrypt(token: str) -> str:
    return token[len("ENC:"):] if token.startswith("ENC:") else ""


@pytest.fixture(autouse=True)
def _isolated_files(monkeypatch):
    tmp_dir = Path(tempfile.mkdtemp(prefix="alfred_ghome_auth_"))
    token_file = tmp_dir / "google_home_token.json"
    client_secret_file = tmp_dir / "google_home_client_secret.json"
    monkeypatch.setattr(gha, "_TOKEN_FILE", token_file)
    monkeypatch.setattr(gha, "_CLIENT_SECRET_FILE", client_secret_file)
    monkeypatch.setattr(encryption_service, "encrypt", _fake_encrypt)
    monkeypatch.setattr(encryption_service, "decrypt", _fake_decrypt)
    yield token_file, client_secret_file
    shutil.rmtree(tmp_dir, ignore_errors=True)


def _write_client_secret(path, client_id="cid-123", client_secret="csecret-456"):
    path.write_text(json.dumps({"web": {"client_id": client_id, "client_secret": client_secret}}), encoding="utf-8")


# =============================================================================
# get_authorization_url
# =============================================================================

def test_get_authorization_url_fails_cleanly_without_client_secret_file():
    result = gha.get_authorization_url("proj-1")
    assert result["success"] is False
    assert result["url"] is None
    assert "google_home_client_secret.json" in result["error"]


def test_get_authorization_url_contains_project_id_and_client_id(_isolated_files):
    _, client_secret_file = _isolated_files
    _write_client_secret(client_secret_file, client_id="my-client-id")

    result = gha.get_authorization_url("proj-xyz")

    assert result["success"] is True
    assert "nestservices.google.com/partnerconnections/proj-xyz/auth" in result["url"]
    assert "client_id=my-client-id" in result["url"]
    assert "redirect_uri=https%3A%2F%2Fwww.google.com" in result["url"]
    assert "sdm.service" in result["url"]


# =============================================================================
# exchange_code
# =============================================================================

def test_exchange_code_fails_cleanly_without_client_secret_file():
    result = gha.exchange_code("some-code")
    assert result["success"] is False
    assert "google_home_client_secret.json" in result["error"]


def test_exchange_code_requires_non_empty_code(_isolated_files):
    _, client_secret_file = _isolated_files
    _write_client_secret(client_secret_file)
    result = gha.exchange_code("  ")
    assert result["success"] is False


def test_exchange_code_success_writes_token(monkeypatch, _isolated_files):
    token_file, client_secret_file = _isolated_files
    _write_client_secret(client_secret_file)

    class _FakeResponse:
        def read(self):
            return json.dumps({
                "access_token": "atok",
                "refresh_token": "rtok",
                "expires_in": 3600,
            }).encode("utf-8")

        def __enter__(self):
            return self

        def __exit__(self, *a):
            return False

    monkeypatch.setattr(gha.urllib.request, "urlopen", lambda req, timeout=10: _FakeResponse())

    result = gha.exchange_code("auth-code-123")

    assert result["success"] is True
    assert token_file.exists()
    assert gha.is_connected() is True


def test_exchange_code_missing_refresh_token_is_reported(monkeypatch, _isolated_files):
    _, client_secret_file = _isolated_files
    _write_client_secret(client_secret_file)

    class _FakeResponse:
        def read(self):
            return json.dumps({"access_token": "atok"}).encode("utf-8")

        def __enter__(self):
            return self

        def __exit__(self, *a):
            return False

    monkeypatch.setattr(gha.urllib.request, "urlopen", lambda req, timeout=10: _FakeResponse())

    result = gha.exchange_code("auth-code-123")

    assert result["success"] is False
    assert "rafraîchissement" in result["error"]


def test_exchange_code_wraps_url_error(monkeypatch, _isolated_files):
    _, client_secret_file = _isolated_files
    _write_client_secret(client_secret_file)

    def raise_url_error(req, timeout=10):
        raise urllib.error.URLError("no connection")

    monkeypatch.setattr(gha.urllib.request, "urlopen", raise_url_error)

    result = gha.exchange_code("auth-code-123")
    assert result["success"] is False


# =============================================================================
# is_connected / disconnect
# =============================================================================

def test_is_connected_false_when_no_token_file():
    assert gha.is_connected() is False


def test_disconnect_removes_token_file(_isolated_files):
    token_file, client_secret_file = _isolated_files
    _write_client_secret(client_secret_file)
    gha._write_encrypted_token({
        "token": "atok", "refresh_token": "rtok", "token_uri": gha._TOKEN_URI,
        "client_id": "cid-123", "client_secret": "csecret-456", "scopes": gha.SCOPES,
    })
    assert token_file.exists()
    gha.disconnect()
    assert not token_file.exists()


def test_disconnect_is_noop_when_no_token_file():
    gha.disconnect()  # ne doit pas lever d'exception
