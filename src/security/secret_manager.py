"""
PROJECT      : ALFRED
BLOCK        : B20
FILE         : secret_manager.py
ROLE         : Gestion secrets locaux — lecture .env, validation, résumé

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-05-10
VERSION      : V1.0
STATUS       : STABLE

DESCRIPTION :
Lit et valide les secrets depuis .env. Indique les secrets manquants sans exposer leurs valeurs.
"""

import os
from pathlib import Path
from typing import Dict, Any

from src.security.security_logger import log_event

try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = None


BASE_DIR = Path(__file__).resolve().parents[2]
ENV_FILE = BASE_DIR / ".env"

if load_dotenv:
    load_dotenv(ENV_FILE)


REQUIRED_SECRETS = [
    "SECRET_KEY",
    "FERNET_KEY",
    "PIN_SALT",
]


def get_secret(key: str) -> str:
    """
    Récupère un secret depuis les variables d'environnement.

    Raises:
        ValueError si le secret est absent.
    """
    clean_key = str(key).strip() if key else ""

    if not clean_key:
        log_event("Secret demandé avec clé vide", "CRITICAL")
        raise ValueError("Nom de secret vide")

    value = os.getenv(clean_key)

    if not value:
        log_event(f"Secret manquant : {clean_key}", "CRITICAL")
        raise ValueError(f"Secret manquant dans .env : {clean_key}")

    return value


def secret_exists(key: str) -> bool:
    """Vérifie si un secret est défini sans le révéler."""
    clean_key = str(key).strip() if key else ""
    return bool(clean_key and os.getenv(clean_key))


def mask_secret(value: str, visible_chars: int = 4) -> str:
    """Masque un secret pour affichage sécurisé."""
    if not value:
        return ""
    if len(value) <= visible_chars:
        return "*" * len(value)
    return value[:visible_chars] + "*" * (len(value) - visible_chars)


def get_secret_masked(key: str) -> str:
    """Retourne un secret masqué."""
    return mask_secret(get_secret(key))


def validate_env_secrets(required: list[str] | None = None) -> Dict[str, str]:
    """
    Vérifie que les secrets critiques sont présents.

    Returns:
        dict: {"SECRET_KEY": "OK", "FERNET_KEY": "MANQUANT"}
    """
    required_secrets = required or REQUIRED_SECRETS
    result: Dict[str, str] = {}
    all_ok = True

    for key in required_secrets:
        present = secret_exists(key)
        result[key] = "OK" if present else "MANQUANT"

        if not present:
            all_ok = False
            log_event(f"Secret requis absent au démarrage : {key}", "CRITICAL")

    if all_ok:
        log_event("Tous les secrets critiques sont présents", "INFO")

    return result


def summarize_secrets(required: list[str] | None = None) -> Dict[str, Any]:
    """Résumé sécurisé des secrets pour dashboard. Ne retourne jamais les valeurs."""
    validation = validate_env_secrets(required=required)
    missing = [key for key, status in validation.items() if status != "OK"]

    return {
        "required_count": len(validation),
        "present_count": len(validation) - len(missing),
        "missing_count": len(missing),
        "missing": missing,
        "all_ok": len(missing) == 0,
    }


def require_all_secrets(required: list[str] | None = None) -> None:
    """Lève une exception si un secret critique manque."""
    summary = summarize_secrets(required=required)

    if not summary["all_ok"]:
        raise RuntimeError(f"Secrets manquants : {', '.join(summary['missing'])}")
