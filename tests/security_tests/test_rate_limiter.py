"""
════════════════════════════════════════════════════════════
PROJECT      : ALFRED
BLOCK        : B20
FUNCTION     : 20.TEST
FILE         : tests/security_tests/test_rate_limiter.py
ROLE         : Tests unitaires — rate_limiter.py

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-06-01
UPDATED      : 2026-06-01
VERSION      : V1.0
STATUS       : ACTIVE

DESCRIPTION :
Couvre : fenêtre glissante, verrouillage au 5ème essai,
backoff exponentiel, réinitialisation admin, get_status.
════════════════════════════════════════════════════════════
"""

import pytest
from src.security.rate_limiter import (
    is_rate_limited,
    record_attempt,
    get_status,
    reset,
    MAX_ATTEMPTS,
    WINDOW_SECONDS,
    BASE_LOCKOUT_SECONDS,
)


@pytest.fixture(autouse=True)
def clean_key(request):
    """Garantit un état propre avant et après chaque test."""
    key = f"test_key_{request.node.name}"
    reset(key)
    yield key
    reset(key)


# ─── État initial ─────────────────────────────────────────────────────────────

def test_fresh_key_not_limited(clean_key):
    limited, retry = is_rate_limited(clean_key)
    assert limited is False
    assert retry == 0.0


def test_status_fresh_key(clean_key):
    st = get_status(clean_key)
    assert st["key"] == clean_key
    assert st["attempts_in_window"] == 0
    assert st["max_attempts"] == MAX_ATTEMPTS
    assert st["locked"] is False
    assert st["retry_after"] == 0.0


# ─── Fenêtre glissante ────────────────────────────────────────────────────────

def test_attempts_below_limit_not_blocked(clean_key):
    for _ in range(MAX_ATTEMPTS - 1):
        record_attempt(clean_key, success=False)
    limited, _ = is_rate_limited(clean_key)
    assert limited is False


def test_max_attempts_triggers_lockout(clean_key):
    for _ in range(MAX_ATTEMPTS):
        record_attempt(clean_key, success=False)
    st = get_status(clean_key)
    assert st["locked"] is True
    assert st["retry_after"] > 0


def test_blocked_after_max_attempts(clean_key):
    for _ in range(MAX_ATTEMPTS):
        record_attempt(clean_key, success=False)
    limited, retry = is_rate_limited(clean_key)
    assert limited is True
    assert retry > 0


# ─── Backoff exponentiel ──────────────────────────────────────────────────────

def test_first_lockout_duration(clean_key):
    """Premier verrouillage = BASE_LOCKOUT_SECONDS."""
    for _ in range(MAX_ATTEMPTS):
        record_attempt(clean_key, success=False)
    st = get_status(clean_key)
    # La durée de lockout doit être proche de BASE_LOCKOUT_SECONDS (marge 2s)
    assert abs(st["retry_after"] - BASE_LOCKOUT_SECONDS) <= 2


def test_second_lockout_doubles(clean_key):
    """Deuxième verrouillage = 2 × BASE_LOCKOUT_SECONDS."""
    for _ in range(MAX_ATTEMPTS + 1):   # +1 déclenche le 2ème backoff
        record_attempt(clean_key, success=False)
    st = get_status(clean_key)
    expected = BASE_LOCKOUT_SECONDS * 2
    assert abs(st["retry_after"] - expected) <= 2


# ─── Succès réinitialise le compteur ─────────────────────────────────────────

def test_success_resets_counter(clean_key):
    for _ in range(MAX_ATTEMPTS - 1):
        record_attempt(clean_key, success=False)
    record_attempt(clean_key, success=True)
    st = get_status(clean_key)
    assert st["attempts_in_window"] == 0
    assert st["locked"] is False


def test_success_after_partial_failure(clean_key):
    record_attempt(clean_key, success=False)
    record_attempt(clean_key, success=False)
    record_attempt(clean_key, success=True)
    limited, _ = is_rate_limited(clean_key)
    assert limited is False


# ─── Reset admin ──────────────────────────────────────────────────────────────

def test_admin_reset_unlocks(clean_key):
    for _ in range(MAX_ATTEMPTS):
        record_attempt(clean_key, success=False)
    assert is_rate_limited(clean_key)[0] is True
    reset(clean_key)
    limited, _ = is_rate_limited(clean_key)
    assert limited is False


def test_reset_clears_attempt_count(clean_key):
    for _ in range(MAX_ATTEMPTS - 1):
        record_attempt(clean_key, success=False)
    reset(clean_key)
    st = get_status(clean_key)
    assert st["attempts_in_window"] == 0


# ─── Isolation des clés ───────────────────────────────────────────────────────

def test_different_keys_independent():
    key_a = "rate_test_isolation_A"
    key_b = "rate_test_isolation_B"
    reset(key_a)
    reset(key_b)
    try:
        for _ in range(MAX_ATTEMPTS):
            record_attempt(key_a, success=False)
        # key_b doit être libre
        assert is_rate_limited(key_b)[0] is False
    finally:
        reset(key_a)
        reset(key_b)
