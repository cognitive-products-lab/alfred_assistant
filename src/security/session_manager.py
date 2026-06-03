# ============================================================
# ALFRED — src/security/session_manager.py
# Bloc 20.03 — Authentification & MFA
#
# 📚 NOTION EXAM :
#   D41-3 — Capsule 3 : Gestion des sessions et verrouillage sur échecs
#
# 🎯 UTILITÉ ALFRED :
#   Gère le cycle de vie des sessions : création, expiration automatique
#   et blocage après N tentatives d'authentification échouées.
#
# 🔐 BLOC SÉCURITÉ :
#   Session management Zero Trust — expiration et lockout anti-brute-force
# ============================================================

import time
from src.security.security_config import SESSION_TIMEOUT, MAX_LOGIN_ATTEMPTS
from src.security.security_logger import log_event

SESSIONS: dict[str, float] = {}
FAILED_ATTEMPTS: dict[str, int] = {}

def create_session(user_id: str) -> None:
    """Crée une session utilisateur."""
    SESSIONS[user_id] = time.time()
    FAILED_ATTEMPTS[user_id] = 0
    log_event(f"Session créée pour {user_id}")

def is_session_valid(user_id: str) -> bool:
    """Vérifie si la session est encore valide."""
    if user_id not in SESSIONS:
        return False

    return time.time() - SESSIONS[user_id] <= SESSION_TIMEOUT

def register_failed_attempt(user_id: str) -> None:
    """Enregistre une tentative d'authentification échouée."""
    FAILED_ATTEMPTS[user_id] = FAILED_ATTEMPTS.get(user_id, 0) + 1
    log_event(f"Tentative échouée pour {user_id}", "WARNING")

def is_blocked(user_id: str) -> bool:
    """Indique si un utilisateur est bloqué après trop d'échecs."""
    return FAILED_ATTEMPTS.get(user_id, 0) >= MAX_LOGIN_ATTEMPTS

def close_session(user_id: str) -> None:
    """Ferme une session utilisateur."""
    SESSIONS.pop(user_id, None)
    log_event(f"Session fermée pour {user_id}")


def summarize_sessions() -> dict:
    """Retourne un résumé anonymisé des sessions — pour le dashboard public."""
    now = time.time()
    active = sum(1 for ts in SESSIONS.values() if now - ts <= SESSION_TIMEOUT)
    expired = len(SESSIONS) - active
    blocked = sum(1 for uid in FAILED_ATTEMPTS if FAILED_ATTEMPTS.get(uid, 0) >= MAX_LOGIN_ATTEMPTS)
    return {
        "active_sessions": active,
        "expired_sessions": expired,
        "total_tracked": len(SESSIONS),
        "blocked_users": blocked,
        "session_timeout_s": SESSION_TIMEOUT,
    }
