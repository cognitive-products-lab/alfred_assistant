"""
mfa_manager.py
Gestionnaire MFA (Multi-Factor Authentication) — Bloc 20.

Implémente TOTP (RFC 6238) via pyotp.
Secrets chiffrés Fernet au repos.
Vérification cachée par session avec TTL.

Architecture :
  1. setup_totp(user_id)              → génère secret TOTP, retourne URI pour QR code
  2. verify_totp(user_id, token)      → vérifie le code à 6 chiffres
  3. mark_verified(user_id, session_id) → cache la vérification en session
  4. is_verified(user_id, session_id)   → vérifie si MFA valide pour la session
  5. is_mfa_required(role)            → consulte roles_permissions.json
"""

from __future__ import annotations

import json
import threading
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any

try:
    import pyotp
    _PYOTP_AVAILABLE = True
except ImportError:
    _PYOTP_AVAILABLE = False

from src.security.security_logger import log_event, log_auth
from src.security.data_protection import protect_field, expose_field

# ─── Configuration ────────────────────────────────────────────────────────────

_ROOT         = Path(__file__).resolve().parents[2]
_SECRETS_FILE = _ROOT / "data" / "security" / "mfa_secrets.json"
_ROLES_FILE   = _ROOT / "config" / "security" / "roles_permissions.json"
_SETTINGS_FILE = _ROOT / "config" / "security" / "security_settings.json"

_APP_NAME    = "ALFRED"
_TOTP_WINDOW = 1       # tolérance ±1 intervalle de 30s
_DEFAULT_TTL = 3600    # durée de vie MFA en session (secondes)

# Cache en mémoire : {user_id: {session_id: expires_at}}
_verified_sessions: dict[str, dict[str, datetime]] = {}
_lock = threading.Lock()


# ─── Persistance secrets ──────────────────────────────────────────────────────

def _load_secrets() -> dict[str, str]:
    if not _SECRETS_FILE.exists():
        return {}
    try:
        raw = json.loads(_SECRETS_FILE.read_text(encoding="utf-8"))
        return {uid: expose_field(secret) for uid, secret in raw.items()}
    except Exception:
        return {}


def _save_secrets(secrets: dict[str, str]) -> None:
    _SECRETS_FILE.parent.mkdir(parents=True, exist_ok=True)
    encrypted = {uid: protect_field(secret) for uid, secret in secrets.items()}
    _SECRETS_FILE.write_text(
        json.dumps(encrypted, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    log_event("mfa_manager: secrets MFA mis à jour")


# ─── Configuration rôles ─────────────────────────────────────────────────────

def _load_role_config(role: str) -> dict[str, Any]:
    if not _ROLES_FILE.exists():
        return {}
    try:
        data = json.loads(_ROLES_FILE.read_text(encoding="utf-8"))
        return data.get("roles", {}).get(role.upper(), {})
    except Exception:
        return {}


def _global_mfa_required() -> bool:
    if not _SETTINGS_FILE.exists():
        return False
    try:
        data = json.loads(_SETTINGS_FILE.read_text(encoding="utf-8"))
        return bool(data.get("mfa_required", False))
    except Exception:
        return False


# ─── API publique ─────────────────────────────────────────────────────────────

def is_mfa_required(role: str) -> bool:
    """Retourne True si le MFA est requis pour ce rôle (global + rôle)."""
    if not _global_mfa_required():
        return False
    return bool(_load_role_config(role).get("mfa_required", False))


def has_mfa_setup(user_id: str) -> bool:
    """Retourne True si un secret TOTP est enregistré pour cet utilisateur."""
    return user_id in _load_secrets()


def setup_totp(user_id: str, force: bool = False) -> dict[str, str]:
    """
    Génère un secret TOTP pour l'utilisateur et le stocke chiffré.

    Returns:
        {
          "secret": str,            # secret base32 (à conserver)
          "provisioning_uri": str,  # URI pour QR code (otpauth://)
          "manual_entry": str,      # code formaté pour saisie manuelle
        }
    """
    if not _PYOTP_AVAILABLE:
        return {"error": "pyotp non installé — pip install pyotp"}

    secrets = _load_secrets()
    if user_id in secrets and not force:
        secret = secrets[user_id]
    else:
        secret = pyotp.random_base32()
        secrets[user_id] = secret
        _save_secrets(secrets)
        log_auth(user_id, "MFA_SETUP", True)

    totp = pyotp.TOTP(secret)
    uri  = totp.provisioning_uri(name=user_id, issuer_name=_APP_NAME)
    formatted = "-".join(secret[i:i+4] for i in range(0, min(len(secret), 16), 4))

    return {
        "secret": secret,
        "provisioning_uri": uri,
        "manual_entry": formatted,
    }


def verify_totp(user_id: str, token: str) -> bool:
    """
    Vérifie un code TOTP à 6 chiffres.

    Returns:
        True si le token est valide, False sinon.
    """
    if not _PYOTP_AVAILABLE:
        return False

    secret = _load_secrets().get(user_id)
    if not secret:
        log_auth(user_id, "MFA_VERIFY", False)
        return False

    valid = pyotp.TOTP(secret).verify(str(token).strip(), valid_window=_TOTP_WINDOW)
    log_auth(user_id, "MFA_VERIFY", valid)
    return valid


def mark_verified(user_id: str, session_id: str, ttl_seconds: int | None = None) -> None:
    """Marque le MFA comme vérifié pour cette session (TTL en mémoire)."""
    ttl = ttl_seconds or _DEFAULT_TTL
    expires_at = datetime.now(timezone.utc) + timedelta(seconds=ttl)
    with _lock:
        if user_id not in _verified_sessions:
            _verified_sessions[user_id] = {}
        _verified_sessions[user_id][session_id] = expires_at
    log_event(f"mfa_manager: MFA vérifié — user={user_id} session={session_id[:8]}…")


def is_verified(user_id: str, session_id: str) -> bool:
    """Retourne True si le MFA a été vérifié pour cette session et n'a pas expiré."""
    with _lock:
        expires_at = _verified_sessions.get(user_id, {}).get(session_id)
    if not expires_at:
        return False
    if datetime.now(timezone.utc) > expires_at:
        revoke(user_id, session_id)
        return False
    return True


def revoke(user_id: str, session_id: str) -> None:
    """Révoque la vérification MFA d'une session."""
    with _lock:
        _verified_sessions.get(user_id, {}).pop(session_id, None)
    log_event(f"mfa_manager: MFA révoqué — user={user_id} session={session_id[:8]}…")


def revoke_all(user_id: str) -> None:
    """Révoque toutes les sessions MFA d'un utilisateur."""
    with _lock:
        _verified_sessions.pop(user_id, None)
    log_event(f"mfa_manager: toutes sessions MFA révoquées — user={user_id}")


def get_status(user_id: str) -> dict[str, Any]:
    """Retourne l'état MFA complet d'un utilisateur."""
    with _lock:
        active = len(_verified_sessions.get(user_id, {}))
    return {
        "user_id": user_id,
        "totp_configured": has_mfa_setup(user_id),
        "active_mfa_sessions": active,
        "pyotp_available": _PYOTP_AVAILABLE,
    }


# ─── Standalone ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=== Test MFA Manager ===\n")

    info = setup_totp("demo_user", force=True)
    print(f"Secret     : {info['manual_entry']}")
    print(f"URI        : {info['provisioning_uri'][:70]}…\n")

    token = pyotp.TOTP(info["secret"]).now()
    print(f"Token TOTP : {token}")
    ok = verify_totp("demo_user", token)
    print(f"Vérif TOTP : {'✓ OK' if ok else '✗ ECHEC'}\n")

    mark_verified("demo_user", "session_demo_abc", ttl_seconds=60)
    print(f"Vérifié    : {is_verified('demo_user', 'session_demo_abc')}")
    revoke("demo_user", "session_demo_abc")
    print(f"Après révoc: {is_verified('demo_user', 'session_demo_abc')}")
    print(f"\nStatut     : {get_status('demo_user')}")
