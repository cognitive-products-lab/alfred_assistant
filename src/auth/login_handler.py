"""
════════════════════════════════════════════════════════════
PROJECT      : ALFRED
BLOCK        : B05
FUNCTION     : 05.03
FILE         : src/auth/login_handler.py
ROLE         : Handler connexion/déconnexion ALFRED (CLI + UI)

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-05-31
UPDATED      : 2026-05-31
VERSION      : V1.0
STATUS       : ACTIVE

DESCRIPTION :
Point d'entrée unifié pour le login/logout ALFRED.
Orchestre auth_manager + user_session + device_registry.

Fonctions couvertes :
  05.03.001 Login interactif (terminal/UI)          V1
  05.03.002 Login automatique (démarrage ALFRED)    V1
  05.03.003 Logout propre                           V1
  05.03.004 Statut de connexion                     V1
════════════════════════════════════════════════════════════
"""
from __future__ import annotations

from src.auth.auth_manager import login, logout, is_authenticated, get_current_user, auto_login
from src.auth.user_session import load_profile, get_session_profile
from src.security.device_registry import init_default_device
from src.security.security_logger import log_event


def start_session(
    user_id: str = "celine",
    role: str = "OWNER",
    device_id: str = "local_pc",
    pin: str = "",
) -> dict:
    """
    Démarre une session ALFRED complète :
      1. Enregistre l'appareil local
      2. Authentifie l'utilisateur
      3. Charge son profil

    Returns:
        {"success": bool, "session_id": str, "user": dict, "profile": dict}
    """
    # 1. Appareil local
    init_default_device(device_id)

    # 2. Authentification
    auth_result = login(user_id=user_id, role=role, pin=pin)
    if not auth_result["success"]:
        return {
            "success": False,
            "session_id": None,
            "user": {},
            "profile": {},
            "reason": auth_result.get("reason", "Échec connexion"),
        }

    # 3. Profil
    profile = load_profile(user_id)
    user    = get_current_user()

    log_event(f"login_handler: session démarrée — user={user_id} role={role}")
    return {
        "success": True,
        "session_id": auth_result["session_id"],
        "user": user,
        "profile": profile,
        "reason": "OK",
    }


def start_auto_session(user_id: str = "celine", role: str = "OWNER") -> str:
    """
    Login automatique sans PIN (démarrage ALFRED).
    Retourne le session_id ou '' si échec.
    """
    init_default_device("local_pc")
    session_id = auto_login(user_id=user_id, role=role)
    if session_id:
        load_profile(user_id)
        log_event(f"login_handler: auto-session — user={user_id}")
    return session_id


def end_session(user_id: str = "") -> bool:
    """Ferme proprement la session courante."""
    result = logout(user_id=user_id)
    log_event(f"login_handler: session fermée — user={user_id or 'courant'}")
    return result


def session_status() -> dict:
    """Retourne le statut de connexion courant."""
    authenticated = is_authenticated()
    user = get_current_user() if authenticated else {}
    return {
        "authenticated": authenticated,
        "user": user,
        "profile": get_session_profile() if authenticated else {},
    }
