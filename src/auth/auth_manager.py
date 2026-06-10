"""
════════════════════════════════════════════════════════════
PROJECT      : ALFRED
BLOCK        : B05
FUNCTION     : 05.01
FILE         : src/auth/auth_manager.py
ROLE         : Gestionnaire authentification utilisateur ALFRED

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-05-31
UPDATED      : 2026-05-31
VERSION      : V1.0
STATUS       : ACTIVE

DESCRIPTION :
Authentification locale utilisateur — PIN, rôle, session.
S'appuie sur B20 (session_manager, mfa_manager) pour les mécanismes bas niveau.
Interface simplifiée pour main.py et alfred_with_ui.py.

Fonctions couvertes :
  05.01.001 Login utilisateur (PIN local)              V1
  05.01.002 Logout et fermeture session                V1
  05.01.003 Vérification session active                V1
  05.01.004 Rôle utilisateur courant                   V1
════════════════════════════════════════════════════════════
"""
from __future__ import annotations

import hashlib
import os
from pathlib import Path

from src.security.session_manager import (
    create_session, is_session_valid, close_session, get_session, FAILED_ATTEMPTS
)
from src.security.security_logger import log_event

# ─── Configuration ───────────────────────────────────────────────────────────
_DEFAULT_USER_ID = "celine"
_DEFAULT_ROLE    = "OWNER"

# PIN haché depuis .env (PIN_HASH) ou fallback None (pas d'auth PIN)
def _get_pin_hash() -> str | None:
    raw = os.getenv("PIN_HASH") or os.getenv("PIN_SALT")
    return raw if raw else None


# ─── État global ─────────────────────────────────────────────────────────────
_current_session_id: str | None = None
_current_user_id:    str        = ""


# ─── API publique ─────────────────────────────────────────────────────────────

def login(user_id: str = _DEFAULT_USER_ID, role: str = _DEFAULT_ROLE, pin: str = "") -> dict:
    """
    Crée une session utilisateur.

    Args:
        user_id : Identifiant utilisateur
        role    : Rôle RBAC (OWNER, USER, GUEST…)
        pin     : PIN optionnel (ignoré si PIN_HASH absent de .env)

    Returns:
        {"success": bool, "session_id": str | None, "reason": str}
    """
    global _current_session_id, _current_user_id

    pin_hash = _get_pin_hash()
    if pin_hash and pin:
        entered_hash = hashlib.sha256(pin.encode()).hexdigest()
        if entered_hash != pin_hash:
            log_event(f"auth_manager: login échoué pour {user_id} (PIN incorrect)", "WARNING")
            return {"success": False, "session_id": None, "reason": "PIN incorrect"}

    session_id = create_session(user_id=user_id, device_id="local_pc", role=role)
    _current_session_id = session_id
    _current_user_id    = user_id
    log_event(f"auth_manager: login OK — user={user_id} role={role}")
    return {"success": True, "session_id": session_id, "reason": "Authentification réussie"}


def logout(user_id: str = "") -> bool:
    """Ferme la session courante. Retourne True si fermée."""
    global _current_session_id, _current_user_id
    uid = user_id or _current_user_id
    if uid:
        close_session(uid)
        log_event(f"auth_manager: logout — user={uid}")
    _current_session_id = None
    _current_user_id    = ""
    return True


def is_authenticated() -> bool:
    """Retourne True si une session valide est active."""
    if not _current_user_id:
        return False
    return is_session_valid(_current_user_id)


def get_current_user() -> dict:
    """Retourne les infos de l'utilisateur courant."""
    if not _current_session_id or not _current_user_id:
        return {"user_id": "", "role": "", "authenticated": False}
    session = get_session(_current_session_id)
    if not session or not session.get("valid"):
        return {"user_id": "", "role": "", "authenticated": False}
    return {
        "user_id": session.get("user_id", _current_user_id),
        "role":    session.get("role", _DEFAULT_ROLE),
        "session_id": _current_session_id,
        "authenticated": True,
    }


def get_current_role() -> str:
    """Retourne le rôle de l'utilisateur courant ou 'GUEST' si non connecté."""
    info = get_current_user()
    return info.get("role") or "GUEST"


def auto_login(user_id: str = _DEFAULT_USER_ID, role: str = _DEFAULT_ROLE) -> str:
    """
    Login automatique sans PIN — pour démarrage ALFRED en mode local.
    Retourne le session_id.
    """
    result = login(user_id=user_id, role=role)
    return result.get("session_id") or ""
