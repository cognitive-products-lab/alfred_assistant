"""
════════════════════════════════════════════════════════════
PROJECT      : ALFRED
BLOCK        : B20
FUNCTION     : 20.TEST
FILE         : tests/security_tests/test_data_protection.py
ROLE         : Tests unitaires — data_protection.py

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-06-01
UPDATED      : 2026-06-01
VERSION      : V1.0
STATUS       : ACTIVE

DESCRIPTION :
Couvre : protect_field/expose_field (round-trip), DEFAULT_SENSITIVE_FIELDS,
champs spécifiques par type de fichier, disponibilité chiffrement.
════════════════════════════════════════════════════════════
"""

import pytest
from src.security.data_protection import (
    protect_field,
    expose_field,
    DEFAULT_SENSITIVE_FIELDS,
    PINS_FIELDS,
    DIALOGUE_FIELDS,
    PROFILE_PII_FIELDS,
)
from src.security.encryption_service import is_available


# ─── protect_field / expose_field — round-trip ────────────────────────────────

@pytest.mark.skipif(not is_available(), reason="Chiffrement Fernet non disponible")
def test_protect_expose_roundtrip():
    plaintext = "super_secret_value_123"
    protected = protect_field(plaintext)
    assert protected != plaintext, "Le champ protégé ne doit pas être en clair"
    recovered = expose_field(protected)
    assert recovered == plaintext


@pytest.mark.skipif(not is_available(), reason="Chiffrement Fernet non disponible")
def test_protect_field_differs_from_plaintext():
    value = "mon_mot_de_passe"
    protected = protect_field(value)
    assert protected != value


@pytest.mark.skipif(not is_available(), reason="Chiffrement Fernet non disponible")
def test_protect_short_string():
    """Une valeur courte doit survivre au round-trip (évite le cas edge vide → falsy)."""
    value = "x"
    protected = protect_field(value)
    assert protected != value
    recovered = expose_field(protected)
    assert recovered == value


@pytest.mark.skipif(not is_available(), reason="Chiffrement Fernet non disponible")
def test_protect_unicode_string():
    value = "Mêlée générale — données médicales 👨‍⚕️"
    protected = protect_field(value)
    recovered = expose_field(protected)
    assert recovered == value


@pytest.mark.skipif(not is_available(), reason="Chiffrement Fernet non disponible")
def test_expose_invalid_token_returns_empty():
    """Un token corrompu ne doit pas déclencher d'exception — retourne '' ou la valeur."""
    result = expose_field("not_a_valid_fernet_token")
    # Doit retourner une chaîne (vide ou valeur d'erreur), pas lever d'exception
    assert isinstance(result, str)


@pytest.mark.skipif(not is_available(), reason="Chiffrement Fernet non disponible")
def test_two_protections_differ():
    """Deux chiffrements du même texte doivent donner des tokens différents (IV aléatoire)."""
    value = "same_value"
    t1 = protect_field(value)
    t2 = protect_field(value)
    assert t1 != t2


# ─── Champs sensibles par défaut ─────────────────────────────────────────────

def test_default_sensitive_fields_contains_common_names():
    assert "password" in DEFAULT_SENSITIVE_FIELDS
    assert "api_key" in DEFAULT_SENSITIVE_FIELDS
    assert "token" in DEFAULT_SENSITIVE_FIELDS
    assert "secret" in DEFAULT_SENSITIVE_FIELDS
    assert "pin" in DEFAULT_SENSITIVE_FIELDS


def test_pins_fields_defined():
    assert "hash" in PINS_FIELDS
    assert "salt" in PINS_FIELDS


def test_dialogue_fields_defined():
    assert "user" in DIALOGUE_FIELDS
    assert "alfred" in DIALOGUE_FIELDS


def test_profile_pii_fields_defined():
    assert "preferred_name" in PROFILE_PII_FIELDS


# ─── Disponibilité du chiffrement ────────────────────────────────────────────

def test_is_available_returns_bool():
    result = is_available()
    assert isinstance(result, bool)


def test_protect_field_without_encryption_returns_value(monkeypatch):
    """Sans chiffrement disponible, protect_field retourne la valeur en clair."""
    monkeypatch.setattr("src.security.data_protection.is_available", lambda: False)
    result = protect_field("valeur_test")
    assert result == "valeur_test"
