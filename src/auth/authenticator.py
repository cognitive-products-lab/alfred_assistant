"""
authenticator.py
Authentification locale par code PIN — Bloc 20.

Utilise bcrypt pour le hachage sécurisé des PINs.
Intègre le rate limiter pour se protéger du brute-force.
"""

from __future__ import annotations

import json
import os
import hashlib
from pathlib import Path

try:
    import bcrypt
    _BCRYPT_AVAILABLE = True
except ImportError:
    _BCRYPT_AVAILABLE = False

from src.security.security_logger import log_event, log_auth
from src.security.rate_limiter import is_rate_limited, record_attempt
from src.security.session_manager import create_session, is_blocked, register_failed_attempt

_PIN_STORE = Path("data/security/pins.json")
_PIN_STORE.parent.mkdir(parents=True, exist_ok=True)

_MIN_PIN_LENGTH = 4
_MAX_PIN_LENGTH = 32


def _hash_pin(pin: str, salt: str) -> str:
    if _BCRYPT_AVAILABLE:
        combined = (pin + salt).encode("utf-8")
        return bcrypt.hashpw(combined, bcrypt.gensalt(rounds=12)).decode("utf-8")
    # Fallback PBKDF2 si bcrypt absent
    return hashlib.pbkdf2_hmac("sha256", pin.encode(), salt.encode(), 200_000).hex()


def _verify_pin(pin: str, hashed: str, salt: str) -> bool:
    if _BCRYPT_AVAILABLE:
        try:
            return bcrypt.checkpw((pin + salt).encode("utf-8"), hashed.encode("utf-8"))
        except Exception:
            return False
    return hashlib.pbkdf2_hmac("sha256", pin.encode(), salt.encode(), 200_000).hex() == hashed


def _load_pins() -> dict:
    if not _PIN_STORE.exists():
        return {}
    try:
        return json.loads(_PIN_STORE.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        log_event("PIN store corrompu — réinitialisé", "ERROR")
        return {}


def _save_pins(pins: dict) -> None:
    _PIN_STORE.write_text(json.dumps(pins, indent=2, ensure_ascii=False), encoding="utf-8")


def register_pin(user_id: str, pin: str) -> bool:
    """
    Enregistre ou remplace le PIN d'un utilisateur.

    Returns:
        True si l'enregistrement a réussi.
    """
    if not pin or not (_MIN_PIN_LENGTH <= len(pin) <= _MAX_PIN_LENGTH):
        log_event(f"PIN invalide pour {user_id} (longueur hors limites)", "WARNING")
        return False

    salt = os.urandom(16).hex()
    hashed = _hash_pin(pin, salt)

    pins = _load_pins()
    pins[user_id] = {"hash": hashed, "salt": salt}
    _save_pins(pins)

    log_auth(user_id, "PIN_REGISTER", True)
    return True


def authenticate(user_id: str, pin: str) -> dict:
    """
    Authentifie un utilisateur par PIN.

    Returns:
        {"success": bool, "reason": str}
    """
    # Rate limiting
    limited, retry_after = is_rate_limited(user_id)
    if limited:
        log_auth(user_id, "PIN", False)
        return {"success": False, "reason": f"Trop de tentatives — réessayez dans {retry_after:.0f}s"}

    # Blocage session manager
    if is_blocked(user_id):
        log_auth(user_id, "PIN", False)
        return {"success": False, "reason": "Compte bloqué — contactez l'administrateur"}

    pins = _load_pins()
    user_data = pins.get(user_id)

    if not user_data:
        record_attempt(user_id, success=False)
        register_failed_attempt(user_id)
        log_auth(user_id, "PIN", False)
        return {"success": False, "reason": "Utilisateur inconnu"}

    if not _verify_pin(pin, user_data["hash"], user_data.get("salt", "")):
        record_attempt(user_id, success=False)
        register_failed_attempt(user_id)
        log_auth(user_id, "PIN", False)
        return {"success": False, "reason": "PIN incorrect"}

    record_attempt(user_id, success=True)
    create_session(user_id)
    log_auth(user_id, "PIN", True)
    return {"success": True, "reason": "Authentification réussie"}


def change_pin(user_id: str, old_pin: str, new_pin: str) -> bool:
    """Change le PIN après vérification de l'ancien."""
    result = authenticate(user_id, old_pin)
    if not result["success"]:
        log_event(f"Changement PIN refusé pour {user_id} : {result['reason']}", "WARNING")
        return False
    return register_pin(user_id, new_pin)


def has_pin(user_id: str) -> bool:
    """Indique si un PIN est enregistré pour cet utilisateur."""
    return user_id in _load_pins()
