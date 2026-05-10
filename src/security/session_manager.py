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
