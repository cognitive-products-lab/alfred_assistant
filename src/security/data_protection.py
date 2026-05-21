"""
data_protection.py
Chiffrement des données sensibles au repos — Bloc 20.

Fournit des utilitaires pour lire/écrire des fichiers JSON
en chiffrant automatiquement les champs sensibles.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from src.security.encryption_service import encrypt, decrypt, is_available
from src.security.security_logger import log_event

# Champs considérés comme sensibles par défaut
DEFAULT_SENSITIVE_FIELDS: frozenset[str] = frozenset({
    "api_key", "password", "token", "secret", "pin", "fernet_key",
    "secret_key", "pin_salt", "private_key", "auth_token", "access_token",
    "refresh_token", "bearer_token", "passphrase",
})


def protect_field(value: str) -> str:
    """Chiffre une valeur sensible. Retourne la valeur en clair si le chiffrement est indisponible."""
    if not is_available():
        log_event("data_protection: chiffrement indisponible", "ERROR")
        return value
    return encrypt(value)


def expose_field(value: str) -> str:
    """Déchiffre une valeur protégée. Retourne '' si invalide."""
    if not is_available():
        return value
    return decrypt(value)


def protect_dict(
    data: dict[str, Any],
    fields: frozenset[str] | set[str] | None = None,
) -> dict[str, Any]:
    """Retourne une copie du dict avec les champs sensibles chiffrés."""
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
    """Retourne une copie du dict avec les champs sensibles déchiffrés."""
    target = fields if fields is not None else DEFAULT_SENSITIVE_FIELDS
    result = dict(data)
    for key, val in result.items():
        if key.lower() in target and isinstance(val, str) and val:
            result[key] = expose_field(val)
    return result


def write_protected_json(
    path: Path,
    data: dict[str, Any],
    sensitive_fields: frozenset[str] | set[str] | None = None,
) -> None:
    """Écrit un fichier JSON avec les champs sensibles chiffrés."""
    protected = protect_dict(data, sensitive_fields)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(protected, indent=2, ensure_ascii=False), encoding="utf-8")
    log_event(f"Fichier protégé écrit : {path.name}")


def read_protected_json(
    path: Path,
    sensitive_fields: frozenset[str] | set[str] | None = None,
) -> dict[str, Any]:
    """Lit un fichier JSON et déchiffre automatiquement les champs sensibles."""
    if not path.exists():
        return {}
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
        return expose_dict(raw, sensitive_fields)
    except json.JSONDecodeError as exc:
        log_event(f"data_protection: JSON corrompu {path.name} — {exc}", "ERROR")
        return {}
