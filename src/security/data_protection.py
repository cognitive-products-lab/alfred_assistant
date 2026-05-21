"""
data_protection.py
Chiffrement des données sensibles au repos — Bloc 20.

Fournit des utilitaires pour lire/écrire des fichiers JSON
en chiffrant automatiquement les champs sensibles (dicts plats,
dicts imbriqués, listes de dicts).
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from src.security.encryption_service import encrypt, decrypt, is_available
from src.security.security_logger import log_event

# Champs considérés comme sensibles par défaut (dicts génériques)
DEFAULT_SENSITIVE_FIELDS: frozenset[str] = frozenset({
    "api_key", "password", "token", "secret", "pin", "fernet_key",
    "secret_key", "pin_salt", "private_key", "auth_token", "access_token",
    "refresh_token", "bearer_token", "passphrase",
})

# Jeux de champs spécifiques par type de fichier
PINS_FIELDS: frozenset[str] = frozenset({"hash", "salt"})
DIALOGUE_FIELDS: frozenset[str] = frozenset({"user", "alfred"})
PROFILE_PII_FIELDS: frozenset[str] = frozenset({"preferred_name", "context"})
CONTEXT_FIELDS: frozenset[str] = frozenset({"location"})


def protect_field(value: str) -> str:
    """Chiffre une valeur sensible. Retourne la valeur en clair si le chiffrement est indisponible."""
    if not is_available():
        log_event("data_protection: chiffrement indisponible", "ERROR")
        return value
    return encrypt(value)


def expose_field(value: str) -> str:
    """Déchiffre une valeur protégée. Retourne la valeur telle quelle si invalide."""
    if not is_available():
        return value
    result = decrypt(value)
    return result if result else value


def protect_dict(
    data: dict[str, Any],
    fields: frozenset[str] | set[str] | None = None,
) -> dict[str, Any]:
    """Retourne une copie du dict avec les champs sensibles (niveau 1) chiffrés."""
    target = fields if fields is not None else DEFAULT_SENSITIVE_FIELDS
    result = dict(data)
    for key, val in result.items():
        if key.lower() in target and isinstance(val, str) and val:
            result[key] = protect_field(val)
    return result


def expose_dict(
    data: dict[str, Any],
    fields: frozenset[str] | set[str] | None = None,
) -> dict[str, Any]:
    """Retourne une copie du dict avec les champs sensibles (niveau 1) déchiffrés."""
    target = fields if fields is not None else DEFAULT_SENSITIVE_FIELDS
    result = dict(data)
    for key, val in result.items():
        if key.lower() in target and isinstance(val, str) and val:
            result[key] = expose_field(val)
    return result


def protect_nested(
    data: Any,
    fields: frozenset[str] | set[str] | None = None,
) -> Any:
    """Chiffre récursivement les champs sensibles dans dict, list ou structure imbriquée."""
    target = fields if fields is not None else DEFAULT_SENSITIVE_FIELDS
    if isinstance(data, dict):
        result: dict[str, Any] = {}
        for key, val in data.items():
            if key.lower() in target and isinstance(val, str) and val:
                result[key] = protect_field(val)
            elif isinstance(val, (dict, list)):
                result[key] = protect_nested(val, target)
            else:
                result[key] = val
        return result
    if isinstance(data, list):
        return [protect_nested(item, target) for item in data]
    return data


def expose_nested(
    data: Any,
    fields: frozenset[str] | set[str] | None = None,
) -> Any:
    """Déchiffre récursivement les champs sensibles dans dict, list ou structure imbriquée."""
    target = fields if fields is not None else DEFAULT_SENSITIVE_FIELDS
    if isinstance(data, dict):
        result = {}
        for key, val in data.items():
            if key.lower() in target and isinstance(val, str) and val:
                result[key] = expose_field(val)
            elif isinstance(val, (dict, list)):
                result[key] = expose_nested(val, target)
            else:
                result[key] = val
        return result
    if isinstance(data, list):
        return [expose_nested(item, target) for item in data]
    return data


def write_protected_json(
    path: Path,
    data: Any,
    sensitive_fields: frozenset[str] | set[str] | None = None,
) -> None:
    """Écrit un fichier JSON (dict ou list) avec les champs sensibles chiffrés (récursif)."""
    protected = protect_nested(data, sensitive_fields)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(protected, indent=2, ensure_ascii=False), encoding="utf-8")
    log_event(f"Fichier protégé écrit : {path.name}")


def read_protected_json(
    path: Path,
    sensitive_fields: frozenset[str] | set[str] | None = None,
) -> Any:
    """Lit un fichier JSON (dict ou list) et déchiffre automatiquement les champs sensibles."""
    if not path.exists():
        return {}
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
        return expose_nested(raw, sensitive_fields)
    except json.JSONDecodeError as exc:
        log_event(f"data_protection: JSON corrompu {path.name} — {exc}", "ERROR")
        return {}
