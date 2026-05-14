"""
PROJECT      : ALFRED
BLOCK        : B20
FUNCTION     : XX.XX
FILE         : session_manager.py
ROLE         : Sessions utilisateur avec FAILED_ATTEMPTS persisté JSON

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-05-10
P26-05-12
VERSION      : V1.0
STATUS       : STABLE

DESCRIPTION :
Gère les sessions utilisateur. Persiste FAILED_ATTEMPTS en JSON pour résistance aux redémarrages.
"""

import json
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any
from uuid import uuid4

from src.security.security_config import SESSION_TIMEOUT, MAX_LOGIN_ATTEMPTS
from src.security.security_logger import log_event


_DATA_DIR = Path(__file__).resolve().parents[2] / "data" / "security"
_FAILED_ATTEMPTS_FILE = _DATA_DIR / "failed_attempts.json"

SESSIONS: Dict[str, Dict[str, Any]] = {}
USER_ACTIVE_SESSION: Dict[str, str] = {}
FAILED_ATTEMPTS: Dict[str, int] = {}


def _load_failed_attempts() -> None:
    """Charge les tentatives échouées depuis le disque au démarrage."""
    global FAILED_ATTEMPTS
    try:
        _DATA_DIR.mkdir(parents=True, exist_ok=True)
        if _FAILED_ATTEMPTS_FILE.exists():
            data = json.loads(_FAILED_ATTEMPTS_FILE.read_text(encoding="utf-8"))
            FAILED_ATTEMPTS = {k: int(v) for k, v in data.items()}
    except Exception:
        FAILED_ATTEMPTS = {}


def _save_failed_attempts() -> None:
    """Persiste les tentatives échouées sur disque."""
    try:
        _DATA_DIR.mkdir(parents=True, exist_ok=True)
        _FAILED_ATTEMPTS_FILE.write_text(
            json.dumps(FAILED_ATTEMPTS, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
    except Exception:
        pass


_load_failed_attempts()


def _now() -> str:
    """Retourne un timestamp UTC ISO."""
    return datetime.now(timezone.utc).isoformat()


def create_session(user_id: str, device_id: str = "", role: str = "USER") -> str:
    """Crée une session utilisateur. Retourne le session_id."""
    clean_user = user_id or "unknown_user"
    session_id = str(uuid4())
    created_at = time.time()

    SESSIONS[session_id] = {
        "session_id": session_id,
        "user_id": clean_user,
        "device_id": device_id,
        "role": role,
        "created_at": created_at,
        "last_seen": created_at,
        "created_at_iso": _now(),
        "active": True,
    }

    USER_ACTIVE_SESSION[clean_user] = session_id
    FAILED_ATTEMPTS[clean_user] = 0
    _save_failed_attempts()

    log_event(f"Session créée user={clean_user} session_id={session_id} device={device_id}")
    return session_id


def get_session(session_id: str) -> Dict[str, Any]:
    """Retourne une session par son identifiant."""
    return SESSIONS.get(session_id, {})


def get_user_session_id(user_id: str) -> str:
    """Retourne la session active connue d'un utilisateur."""
    return USER_ACTIVE_SESSION.get(user_id, "")


def is_session_id_valid(session_id: str) -> bool:
    """Vérifie si une session_id est valide et non expirée."""
    session = SESSIONS.get(session_id)

    if not session:
        return False

    if not session.get("active", False):
        return False

    elapsed = time.time() - float(session.get("last_seen", 0))

    if elapsed > SESSION_TIMEOUT:
        session["active"] = False
        log_event(f"Session expirée session_id={session_id}", "WARNING")
        return False

    session["last_seen"] = time.time()
    return True


def is_session_valid(user_id: str) -> bool:
    """Vérifie la session active d'un utilisateur (compatibilité historique)."""
    session_id = USER_ACTIVE_SESSION.get(user_id)

    if not session_id:
        return False

    return is_session_id_valid(session_id)


def register_failed_attempt(user_id: str) -> None:
    """Enregistre une tentative d'authentification échouée — persistée sur disque."""
    clean_user = user_id or "unknown_user"
    FAILED_ATTEMPTS[clean_user] = FAILED_ATTEMPTS.get(clean_user, 0) + 1
    _save_failed_attempts()

    log_event(
        f"Tentative échouée user={clean_user} count={FAILED_ATTEMPTS[clean_user]}",
        "WARNING",
    )


def reset_failed_attempts(user_id: str) -> None:
    """Réinitialise les tentatives échouées."""
    clean_user = user_id or "unknown_user"
    FAILED_ATTEMPTS[clean_user] = 0
    _save_failed_attempts()
    log_event(f"Tentatives échouées réinitialisées user={clean_user}")


def is_blocked(user_id: str) -> bool:
    """Indique si un utilisateur est bloqué après trop d'échecs."""
    clean_user = user_id or "unknown_user"
    return FAILED_ATTEMPTS.get(clean_user, 0) >= MAX_LOGIN_ATTEMPTS


def close_session(user_id: str) -> None:
    """Ferme la session active d'un utilisateur (compatibilité historique)."""
    session_id = USER_ACTIVE_SESSION.pop(user_id, "")

    if session_id and session_id in SESSIONS:
        SESSIONS[session_id]["active"] = False

    log_event(f"Session fermée user={user_id}")


def close_session_by_id(session_id: str) -> bool:
    """Ferme une session par son identifiant."""
    session = SESSIONS.get(session_id)

    if not session:
        return False

    session["active"] = False
    user_id = session.get("user_id")

    if user_id and USER_ACTIVE_SESSION.get(user_id) == session_id:
        USER_ACTIVE_SESSION.pop(user_id, None)

    log_event(f"Session fermée session_id={session_id}")
    return True


def list_active_sessions() -> Dict[str, Dict[str, Any]]:
    """Retourne les sessions actives."""
    return {
        session_id: session
        for session_id, session in SESSIONS.items()
        if session.get("active", False)
    }


def summarize_sessions() -> Dict[str, Any]:
    """Résumé sessions pour dashboard sécurité."""
    active_sessions = list_active_sessions()

    return {
        "active_sessions": len(active_sessions),
        "known_sessions": len(SESSIONS),
        "blocked_users": [
            user_id for user_id, count in FAILED_ATTEMPTS.items()
            if count >= MAX_LOGIN_ATTEMPTS
        ],
        "failed_attempts": FAILED_ATTEMPTS.copy(),
    }
