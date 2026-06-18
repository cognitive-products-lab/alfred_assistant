"""
════════════════════════════════════════════════════════════
PROJECT      : ALFRED
BLOCK        : B20
FUNCTION     : 20.00
FILE         : security_config.py
ROLE         : Configuration globale de sécurité depuis .env

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-05-23
UPDATED      : 2026-05-23
VERSION      : V1.0
STATUS       : ACTIVE

DESCRIPTION :
Charge la configuration de sécurité (timeouts, limites, hôte API) depuis .env.
════════════════════════════════════════════════════════════
"""
import os
from pathlib import Path

try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = None

BASE_DIR = Path(__file__).resolve().parents[2]

if load_dotenv:
    load_dotenv(BASE_DIR / ".env")

def get_config(key: str, default=None):
    """Retourne une variable d'environnement ou une valeur par défaut."""
    return os.getenv(key, default)

def get_int_config(key: str, default: int = 0) -> int:
    """Retourne une variable d'environnement convertie en int, ou default."""
    try:
        return int(get_config(key, default))
    except (TypeError, ValueError):
        return default


APP_ENV = get_config("APP_ENV", "local")
API_HOST = get_config("API_HOST", "127.0.0.1")
SESSION_TIMEOUT = int(get_config("SESSION_TIMEOUT", 900))
MAX_LOGIN_ATTEMPTS = int(get_config("MAX_LOGIN_ATTEMPTS", 5))


def get_bool_config(key: str, default: bool = False) -> bool:
    """Retourne une variable d'environnement convertie en bool."""
    val = get_config(key, str(default)).lower()
    return val in ("1", "true", "yes", "on")


LOCAL_FIRST_MODE = get_bool_config("LOCAL_FIRST_MODE", True)
ZERO_TRUST_ENABLED = get_bool_config("ZERO_TRUST_ENABLED", True)


def get_security_config() -> dict:
    """Retourne la configuration de sécurité active."""
    return {
        "APP_ENV": APP_ENV,
        "API_HOST": API_HOST,
        "SESSION_TIMEOUT": SESSION_TIMEOUT,
        "MAX_LOGIN_ATTEMPTS": MAX_LOGIN_ATTEMPTS,
        "LOCAL_FIRST_MODE": LOCAL_FIRST_MODE,
        "ZERO_TRUST_ENABLED": ZERO_TRUST_ENABLED,
    }


def validate_security_config() -> dict:
    """Valide la cohérence de la configuration de sécurité."""
    issues = []
    if SESSION_TIMEOUT < 60:
        issues.append("SESSION_TIMEOUT trop court (< 60s)")
    if MAX_LOGIN_ATTEMPTS < 1:
        issues.append("MAX_LOGIN_ATTEMPTS invalide (< 1)")
    cfg = get_security_config()
    return {"valid": len(issues) == 0, "issues": issues, "config": cfg}


def summarize_security_config() -> dict:
    """Synthèse de la configuration pour le dashboard."""
    val = validate_security_config()
    return {
        "valid": val["valid"],
        "issues_count": len(val["issues"]),
        "issues": val["issues"],
        "zero_trust_enabled": ZERO_TRUST_ENABLED,
        "local_first_mode": LOCAL_FIRST_MODE,
        "app_env": APP_ENV,
        "session_timeout": SESSION_TIMEOUT,
    }
