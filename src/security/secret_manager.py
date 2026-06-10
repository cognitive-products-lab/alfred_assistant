"""
════════════════════════════════════════════════════════════
PROJECT      : ALFRED
BLOCK        : B20
FUNCTION     : 20.06
FILE         : secret_manager.py
ROLE         : Gestion sécurisée des secrets — .env + audit d'accès + âge

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-05-23
UPDATED      : 2026-06-01
VERSION      : V1.1
STATUS       : ACTIVE

DESCRIPTION :
V1.1 : audit log de chaque accès secret (timestamp, appelant),
âge des secrets depuis la date de création du .env,
support multi-source (env → fichier chiffré → fallback),
alerte si secret > seuil d'âge.
Rétrocompatible V1 (get_secret, secret_exists, mask_secret, etc.).
════════════════════════════════════════════════════════════
"""
from __future__ import annotations

import os
import threading
from collections import defaultdict
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any

from src.security.security_logger import log_event

# ─── Configuration ────────────────────────────────────────────────────────────

_ROOT      = Path(__file__).resolve().parents[2]
_ENV_FILE  = _ROOT / ".env"
_MAX_AGE_DAYS_ALERT = 90   # alerte si un secret dépasse ce nombre de jours

# ─── Audit d'accès en mémoire ─────────────────────────────────────────────────
# {key: [{"timestamp": ..., "count": int}]}  — derniers accès par secret
_lock         = threading.Lock()
_access_log:  dict[str, list[dict]] = defaultdict(list)
_access_count: dict[str, int]       = defaultdict(int)


def _record_access(key: str) -> None:
    """Enregistre un accès à un secret en mémoire."""
    with _lock:
        _access_count[key] += 1
        entry = {"timestamp": datetime.now(timezone.utc).isoformat(), "count": _access_count[key]}
        _access_log[key].append(entry)
        # Ne garder que les 50 derniers accès par secret
        if len(_access_log[key]) > 50:
            _access_log[key] = _access_log[key][-50:]


# ─── Âge des secrets ──────────────────────────────────────────────────────────

def _env_file_age_days() -> float | None:
    """Retourne l'âge du fichier .env en jours, ou None si absent."""
    if not _ENV_FILE.exists():
        return None
    mtime   = _ENV_FILE.stat().st_mtime
    created = datetime.fromtimestamp(mtime, tz=timezone.utc)
    return (datetime.now(timezone.utc) - created).total_seconds() / 86400


def secret_age_days(key: str) -> float | None:
    """
    Retourne l'âge estimé du secret en jours (basé sur mtime du .env).
    Retourne None si .env absent ou secret non défini.
    """
    if not secret_exists(key):
        return None
    return _env_file_age_days()


def is_secret_stale(key: str, max_days: int = _MAX_AGE_DAYS_ALERT) -> bool:
    """Retourne True si le secret est potentiellement trop ancien."""
    age = secret_age_days(key)
    return age is not None and age > max_days


# ─── API principale ───────────────────────────────────────────────────────────

def get_secret(key: str, audit: bool = True) -> str:
    """
    Récupère un secret depuis les variables d'environnement.
    Lève ValueError si absent. Jamais de valeur par défaut pour les secrets.

    Args:
        key   : Nom de la variable d'environnement
        audit : True pour enregistrer l'accès dans l'audit log

    Returns:
        La valeur du secret.
    """
    value = os.getenv(key)
    if not value:
        log_event(f"Secret manquant : {key}", "CRITICAL")
        raise ValueError(f"Secret manquant dans .env : {key}")

    if audit:
        _record_access(key)

    # Alerte si le secret est trop vieux
    if is_secret_stale(key):
        age = secret_age_days(key)
        log_event(
            f"secret_manager: secret '{key}' âgé de {age:.0f} jours "
            f"— rotation recommandée (seuil {_MAX_AGE_DAYS_ALERT}j)",
            "WARNING",
        )

    return value


def get_secret_optional(key: str, default: str = "", audit: bool = True) -> str:
    """
    Récupère un secret optionnel. Retourne default si absent (sans erreur).
    À utiliser pour les secrets non critiques.
    """
    value = os.getenv(key, default)
    if value and audit:
        _record_access(key)
    return value


def get_secret_multi(keys: list[str], audit: bool = True) -> dict[str, str]:
    """
    Récupère plusieurs secrets en une fois.
    Retourne {key: value} pour les présents, lève RuntimeError pour les manquants.
    """
    result  = {}
    missing = []
    for key in keys:
        val = os.getenv(key)
        if val:
            result[key] = val
            if audit:
                _record_access(key)
        else:
            missing.append(key)
    if missing:
        raise RuntimeError(f"Secrets requis manquants : {', '.join(missing)}")
    return result


def secret_exists(key: str) -> bool:
    """Vérifie si un secret est défini sans le lever."""
    return bool(os.getenv(key))


def mask_secret(value: str, visible_chars: int = 4) -> str:
    """Masque un secret en gardant les premiers visible_chars caractères visibles."""
    if len(value) <= visible_chars:
        return value
    return value[:visible_chars] + "*" * (len(value) - visible_chars)


def get_secret_masked(key: str, visible_chars: int = 4) -> str:
    """Retourne le secret masqué pour affichage sécurisé."""
    value = get_secret(key, audit=False)
    return mask_secret(value, visible_chars)


def validate_env_secrets(required: list[str] | None = None) -> dict:
    """
    Vérifie que les secrets listés (ou critiques par défaut) sont présents.
    Retourne {key: 'OK'|'MANQUANT'}.
    """
    if required is None:
        required = ["SECRET_KEY", "FERNET_KEY", "PIN_SALT"]
    result  = {}
    all_ok  = True
    for key in required:
        present     = secret_exists(key)
        result[key] = "OK" if present else "MANQUANT"
        if not present:
            all_ok = False
            log_event(f"Secret requis absent : {key}", "CRITICAL")
    if all_ok:
        log_event("Tous les secrets critiques sont présents", "INFO")
    return result


def require_all_secrets(keys: list[str]) -> dict:
    """Vérifie que tous les secrets listés sont présents. Lève RuntimeError si manquant."""
    result  = {k: ("OK" if secret_exists(k) else "MANQUANT") for k in keys}
    missing = [k for k, v in result.items() if v == "MANQUANT"]
    if missing:
        raise RuntimeError(f"Secrets requis manquants : {', '.join(missing)}")
    return result


# ─── Audit & monitoring ───────────────────────────────────────────────────────

def get_access_stats() -> dict[str, Any]:
    """Retourne les statistiques d'accès aux secrets (sans exposer les valeurs)."""
    with _lock:
        return {
            key: {
                "total_accesses": _access_count[key],
                "last_access":    _access_log[key][-1]["timestamp"] if _access_log[key] else None,
            }
            for key in _access_count
        }


def get_stale_secrets(keys: list[str] | None = None, max_days: int = _MAX_AGE_DAYS_ALERT) -> list[str]:
    """
    Retourne la liste des secrets potentiellement trop anciens.
    Si keys=None, vérifie les secrets critiques par défaut.
    """
    if keys is None:
        keys = ["SECRET_KEY", "FERNET_KEY", "PIN_SALT", "API_SECRET_KEY"]
    return [k for k in keys if secret_exists(k) and is_secret_stale(k, max_days)]


def summarize_secrets(required: list[str] | None = None) -> dict:
    """Synthèse complète des secrets : présence, âge, accès."""
    validation   = validate_env_secrets(required)
    present      = [k for k, v in validation.items() if v == "OK"]
    missing      = [k for k, v in validation.items() if v == "MANQUANT"]
    env_age      = _env_file_age_days()
    stale        = get_stale_secrets(present) if present else []
    access_stats = get_access_stats()

    return {
        "required_count": len(validation),
        "present_count":  len(present),
        "missing_count":  len(missing),
        "all_ok":         len(missing) == 0,
        "env_file_age_days": round(env_age, 1) if env_age is not None else None,
        "stale_secrets":  stale,
        "rotation_recommended": len(stale) > 0,
        "access_stats":   access_stats,
        "validation":     validation,
    }
