"""
════════════════════════════════════════════════════════════
PROJECT      : ALFRED
BLOCK        : B20
FUNCTION     : 20.08
FILE         : session_manager.py
ROLE         : Gestion des sessions utilisateur avec timeout

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-05-23
UPDATED      : 2026-05-31
VERSION      : V1.1
STATUS       : ACTIVE

DESCRIPTION :
Crée, valide et ferme les sessions. Stockage dual : par UUID et par user_id.
Gère les tentatives d'authentification échouées et les blocages.
════════════════════════════════════════════════════════════
"""
import time
import uuid
from src.security.security_config import SESSION_TIMEOUT, MAX_LOGIN_ATTEMPTS
from src.security.security_logger import log_event

# Index principal : session_id (UUID) → infos session
SESSIONS: dict[str, dict] = {}
# Index secondaire : user_id → session_id actif
_USER_TO_SESSION: dict[str, str] = {}
# Tentatives échouées par user_id
FAILED_ATTEMPTS: dict[str, int] = {}
# Alias legacy pour les tests
USER_ACTIVE_SESSION = _USER_TO_SESSION


def create_session(user_id: str, device_id: str = "", role: str = "") -> str:
    """Crée une session utilisateur et retourne l'UUID de session."""
    session_id = str(uuid.uuid4())
    now = time.time()
    SESSIONS[session_id] = {
        "session_id": session_id,
        "user_id": user_id,
        "device_id": device_id,
        "role": role,
        "started_at": now,
    }
    _USER_TO_SESSION[user_id] = session_id
    FAILED_ATTEMPTS[user_id] = 0
    log_event(f"Session créée pour {user_id} (device={device_id or 'N/A'}, role={role or 'N/A'})")
    return session_id


def get_session(session_id: str) -> dict | None:
    """Retourne les informations de session par UUID ou None si absente/expirée."""
    entry = SESSIONS.get(session_id)
    if not entry:
        return None
    elapsed = time.time() - entry["started_at"]
    valid = elapsed <= SESSION_TIMEOUT
    return {**entry, "elapsed_seconds": round(elapsed, 2), "valid": valid, "active": valid}


def get_user_session_id(user_id: str) -> str | None:
    """Retourne l'UUID de session actif pour un utilisateur, ou None si absent/expiré."""
    session_id = _USER_TO_SESSION.get(user_id)
    if session_id and is_session_id_valid(session_id):
        return session_id
    return None


def is_session_id_valid(session_id: str) -> bool:
    """Vérifie si un UUID de session correspond à une session active."""
    entry = SESSIONS.get(session_id)
    if not entry:
        return False
    return time.time() - entry["started_at"] <= SESSION_TIMEOUT


def is_session_valid(user_id: str) -> bool:
    """Legacy : vérifie si l'utilisateur a une session active (par user_id)."""
    session_id = _USER_TO_SESSION.get(user_id)
    return bool(session_id and is_session_id_valid(session_id))


def register_failed_attempt(user_id: str) -> None:
    """Enregistre une tentative d'authentification échouée."""
    FAILED_ATTEMPTS[user_id] = FAILED_ATTEMPTS.get(user_id, 0) + 1
    log_event(f"Tentative échouée pour {user_id}", "WARNING")


def reset_failed_attempts(user_id: str) -> None:
    """Remet à zéro le compteur de tentatives échouées."""
    FAILED_ATTEMPTS[user_id] = 0
    log_event(f"Tentatives réinitialisées pour {user_id}")


def is_blocked(user_id: str) -> bool:
    """Indique si un utilisateur est bloqué après trop d'échecs."""
    return FAILED_ATTEMPTS.get(user_id, 0) >= MAX_LOGIN_ATTEMPTS


def invalidate_session(session_id_or_user: str) -> None:
    """Invalide une session par session_id (UUID) ou user_id."""
    if not close_session_by_id(session_id_or_user):
        close_session(session_id_or_user)


def close_session(user_id: str) -> None:
    """Legacy : ferme la session active d'un utilisateur par user_id."""
    session_id = _USER_TO_SESSION.pop(user_id, None)
    if session_id:
        SESSIONS.pop(session_id, None)
    log_event(f"Session fermée pour {user_id}")


def close_session_by_id(session_id: str) -> bool:
    """Ferme une session par son UUID. Retourne True si trouvée et fermée."""
    entry = SESSIONS.pop(session_id, None)
    if entry:
        _USER_TO_SESSION.pop(entry["user_id"], None)
        log_event(f"Session {session_id} fermée")
        return True
    return False


def list_active_sessions() -> dict:
    """Retourne un dict des sessions actives {session_id: infos}."""
    now = time.time()
    return {
        sid: {**info, "elapsed_seconds": round(now - info["started_at"], 2)}
        for sid, info in SESSIONS.items()
        if now - info["started_at"] <= SESSION_TIMEOUT
    }


def summarize_sessions() -> dict:
    """Retourne une synthèse des sessions pour le dashboard sécurité."""
    now = time.time()
    active = expired = blocked = 0
    sessions = []

    for sid, info in SESSIONS.items():
        elapsed = now - info["started_at"]
        valid = elapsed <= SESSION_TIMEOUT
        user_id = info["user_id"]
        b = is_blocked(user_id)

        if valid: active += 1
        else: expired += 1
        if b: blocked += 1

        sessions.append({
            "session_id": sid,
            "user_id": user_id,
            "elapsed_seconds": round(elapsed, 2),
            "valid": valid,
            "blocked": b,
            "failed_attempts": FAILED_ATTEMPTS.get(user_id, 0),
        })

    return {
        "active_sessions": active,
        "expired_sessions": expired,
        "blocked_users": blocked,
        "known_sessions": len(SESSIONS),
        "total_sessions": len(SESSIONS),
        "failed_attempts": dict(FAILED_ATTEMPTS),
        "sessions": sessions,
    }
