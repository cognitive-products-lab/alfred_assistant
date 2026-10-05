"""
════════════════════════════════════════════════════════════
PROJECT      : ALFRED
BLOCK        : B20
FUNCTION     : 20.TEST
FILE         : tests/security_tests/test_secure_json.py
ROLE         : Tests unitaires — secure_json.py (chiffrement JSON au repos)

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-10-05
VERSION      : V1.0
STATUS       : ACTIVE

DESCRIPTION :
Clé Fernet de test injectée via monkeypatch (jamais la vraie FERNET_KEY),
fichiers dans tmp_path uniquement.
Couvre : aller-retour chiffré, absence de clair sur disque, fail-closed
(écriture sans clé, clé différente), préservation du chiffrement à la
réécriture, migration in-place, rotation de clé des enveloppes.
════════════════════════════════════════════════════════════
"""
import json

import pytest
from cryptography.fernet import Fernet

from src.security import encryption_service, secure_json, key_rotation_scheduler
from src.security.secure_json import (
    SecureJsonError, encrypt_file_in_place, is_encrypted_file, load_json, save_json,
)

PROFILE = {"user_profile": {"display_name": "Test", "note": "donnée sensible é"}}


@pytest.fixture
def test_key(monkeypatch):
    key = Fernet.generate_key()
    monkeypatch.setattr(encryption_service, "_cipher", Fernet(key))
    return key


def test_roundtrip_encrypted(tmp_path, test_key):
    path = tmp_path / "p.json"
    save_json(path, PROFILE, encrypt=True)
    assert load_json(path) == PROFILE


def test_no_plaintext_on_disk(tmp_path, test_key):
    path = tmp_path / "p.json"
    save_json(path, PROFILE, encrypt=True)
    raw = path.read_text(encoding="utf-8")
    assert "sensible" not in raw and "display_name" not in raw
    assert json.loads(raw)["_alfred_encrypted"] == "fernet-v1"


def test_write_without_key_refuses_plaintext(tmp_path, monkeypatch):
    monkeypatch.setattr(encryption_service, "_cipher", None)
    path = tmp_path / "p.json"
    with pytest.raises(RuntimeError):
        save_json(path, PROFILE, encrypt=True)
    assert not path.exists()


def test_wrong_key_raises_instead_of_empty_profile(tmp_path, test_key, monkeypatch):
    path = tmp_path / "p.json"
    save_json(path, PROFILE, encrypt=True)
    monkeypatch.setattr(encryption_service, "_cipher", Fernet(Fernet.generate_key()))
    with pytest.raises(SecureJsonError):
        load_json(path)


def test_rewrite_keeps_encryption(tmp_path, test_key):
    """Un fichier déjà chiffré ne redevient jamais clair par réécriture (encrypt=None)."""
    path = tmp_path / "p.json"
    save_json(path, PROFILE, encrypt=True)
    save_json(path, {"x": 1})
    assert is_encrypted_file(path)
    assert load_json(path) == {"x": 1}


def test_plain_file_still_readable(tmp_path, test_key):
    path = tmp_path / "plain.json"
    path.write_text(json.dumps(PROFILE), encoding="utf-8")
    assert load_json(path) == PROFILE


def test_migration_in_place(tmp_path, test_key):
    path = tmp_path / "plain.json"
    path.write_text(json.dumps(PROFILE, ensure_ascii=False), encoding="utf-8")
    assert encrypt_file_in_place(path) == "encrypted"
    assert is_encrypted_file(path)
    assert load_json(path) == PROFILE
    assert encrypt_file_in_place(path) == "already"
    assert encrypt_file_in_place(tmp_path / "absent.json") == "missing"


def test_sensitive_paths_declared():
    assert secure_json.is_sensitive_path(secure_json._ROOT / "data/health/health_celine.json")
    assert secure_json.is_sensitive_path(secure_json._ROOT / "private_data/user_profiles/seb_profile.json")
    assert not secure_json.is_sensitive_path(secure_json._ROOT / "config/features.json")


def test_key_rotation_reencrypts_envelopes(tmp_path, test_key, monkeypatch):
    rel = "private_data/user_profiles/celine_profile.json"
    monkeypatch.setattr(key_rotation_scheduler, "_ROOT", tmp_path)
    monkeypatch.setattr(secure_json, "SENSITIVE_FILES", (rel,))
    path = tmp_path / rel
    save_json(path, PROFILE, encrypt=True)

    new_key = Fernet.generate_key()
    result = key_rotation_scheduler.rotate_encrypted_files(test_key, new_key)
    assert str(path) in result["success"]

    monkeypatch.setattr(encryption_service, "_cipher", Fernet(new_key))
    assert load_json(path) == PROFILE
