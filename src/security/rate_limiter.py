"""
════════════════════════════════════════════════════════════
PROJECT      : ALFRED
BLOCK        : B20
FUNCTION     : 20.07
FILE         : rate_limiter.py
ROLE         : Limiteur de taux avec backoff exponentiel

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-05-23
UPDATED      : 2026-05-23
VERSION      : V1.0
STATUS       : ACTIVE

DESCRIPTION :
Protège contre le brute-force et DoS local par fenêtre glissante configurable.
════════════════════════════════════════════════════════════
"""
from __future__ import annotations
"""
rate_limiter.py
Limiteur de taux avec backoff exponentiel — Bloc 20.

Protège contre le brute-force et les attaques par déni de service local.
Chaque clé (user_id, device_id, etc.) dispose d'une fenêtre glissante.
"""


import time
import threading

from src.security.security_logger import log_event

_lock = threading.Lock()
_attempts: dict[str, list[float]] = {}
_lockout_until: dict[str, float] = {}

MAX_ATTEMPTS = 5
WINDOW_SECONDS = 60
BASE_LOCKOUT_SECONDS = 30


def _cleanup_window(key: str) -> None:
    """Supprime les tentatives hors fenêtre glissante."""
    now = time.time()
    _attempts[key] = [t for t in _attempts.get(key, []) if now - t < WINDOW_SECONDS]


def is_rate_limited(key: str) -> tuple[bool, float]:
    """
    Vérifie si une clé est bloquée.

    Returns:
        (limited, retry_after_seconds)
    """
    with _lock:
        now = time.time()
        if key in _lockout_until and now < _lockout_until[key]:
            return True, _lockout_until[key] - now
        _cleanup_window(key)
        return len(_attempts.get(key, [])) >= MAX_ATTEMPTS, 0.0


def record_attempt(key: str, success: bool) -> None:
    """
    Enregistre une tentative d'authentification.

    En cas de succès, réinitialise les compteurs.
    En cas d'échec, incrémente et applique un backoff si MAX_ATTEMPTS atteint.
    """
    with _lock:
        if success:
            _attempts.pop(key, None)
            _lockout_until.pop(key, None)
            return

        now = time.time()
        _cleanup_window(key)
        _attempts.setdefault(key, []).append(now)

        count = len(_attempts[key])
        if count >= MAX_ATTEMPTS:
            # Backoff exponentiel : 30s, 60s, 120s, 240s…
            overflows = max(0, count - MAX_ATTEMPTS)
            lockout = BASE_LOCKOUT_SECONDS * (2 ** overflows)
            _lockout_until[key] = now + lockout
            log_event(
                f"Rate limit atteint pour [{key}] — blocage {lockout:.0f}s "
                f"({count} tentatives / {WINDOW_SECONDS}s)",
                "WARNING",
            )


def get_status(key: str) -> dict:
    """Retourne l'état courant du rate limiter pour une clé."""
    with _lock:
        now = time.time()
        _cleanup_window(key)
        count = len(_attempts.get(key, []))
        locked = key in _lockout_until and now < _lockout_until[key]
        retry_after = max(0.0, _lockout_until.get(key, 0) - now)
        return {
            "key": key,
            "attempts_in_window": count,
            "max_attempts": MAX_ATTEMPTS,
            "locked": locked,
            "retry_after": round(retry_after, 1),
        }


def reset(key: str) -> None:
    """Réinitialise les compteurs pour une clé (déverrouillage administrateur)."""
    with _lock:
        _attempts.pop(key, None)
        _lockout_until.pop(key, None)
        log_event(f"Rate limiter réinitialisé pour [{key}]", "INFO")
