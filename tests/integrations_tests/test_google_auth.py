"""
PROJECT      : ALFRED
BLOCK        : GLOBAL — Intégrations externes
FILE         : tests/integrations_tests/test_google_auth.py
ROLE         : Tests unitaires src/integrations/google_auth.py

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-07-23
VERSION      : V1.0
STATUS       : TESTED

DESCRIPTION :
Le chiffrement réel (Fernet) est monkeypatché par un simple encodage
réversible — ces tests vérifient la logique de google_auth.py (porte fermée
par défaut, roundtrip du jeton, déconnexion), pas cryptography elle-même
(déjà testée ailleurs, cf. tests/security/test_pentest_encryption.py).
"""

import json
import shutil
import tempfile
from pathlib import Path

import pytest

from src.integrations import google_auth as ga
from src.security import encryption_service


def _fake_encrypt(data: str) -> str:
    return "ENC:" + data


def _fake_decrypt(token: str) -> str:
    return token[len("ENC:"):] if token.startswith("ENC:") else ""


@pytest.fixture(autouse=True)
def _isolated_files(monkeypatch):
    tmp_dir = Path(tempfile.mkdtemp(prefix="alfred_google_auth_"))
    token_file = tmp_dir / "google_calendar_token.json"
    client_secret_file = tmp_dir / "google_client_secret.json"
    monkeypatch.setattr(ga, "_TOKEN_FILE", token_file)
    monkeypatch.setattr(ga, "_CLIENT_SECRET_FILE", client_secret_file)
    monkeypatch.setattr(encryption_service, "encrypt", _fake_encrypt)
    monkeypatch.setattr(encryption_service, "decrypt", _fake_decrypt)
    yield token_file, client_secret_file
    shutil.rmtree(tmp_dir, ignore_errors=True)


def test_is_connected_false_when_no_token_file():
    assert ga.is_connected() is False


def test_get_credentials_none_when_no_token_file():
    assert ga.get_credentials() is None


def test_write_and_read_encrypted_token_roundtrip(_isolated_files):
    info = {"token": "abc", "refresh_token": "def"}
    ga._write_encrypted_token(info)
    assert ga._read_encrypted_token() == info


def test_read_encrypted_token_returns_none_on_corrupted_file(_isolated_files):
    token_file, _ = _isolated_files
    token_file.parent.mkdir(parents=True, exist_ok=True)
    token_file.write_text("not-a-valid-token", encoding="utf-8")
    assert ga._read_encrypted_token() is None


def test_disconnect_removes_token_file(_isolated_files):
    token_file, _ = _isolated_files
    ga._write_encrypted_token({"token": "abc"})
    assert token_file.exists()
    ga.disconnect()
    assert not token_file.exists()


def test_disconnect_is_noop_when_no_token_file():
    ga.disconnect()  # ne doit pas lever d'exception


def test_start_auth_flow_fails_cleanly_without_client_secret_file():
    result = ga.start_auth_flow()
    assert result["success"] is False
    assert "google_client_secret.json" in result["error"]
