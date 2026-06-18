"""
PROJECT      : ALFRED
BLOCK        : B20
FUNCTION     : XX.XX
FILE         : test_session_manager.py
ROLE         : TO_DEFINE

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-05-10
UPDATED      : 2026-05-10
VERSION      : V1.0
STATUS       : DRAFT

DESCRIPTION :
TO_COMPLETE
"""

"""
Tests B20 — session_manager.py
"""

from src.security.session_manager import (
    create_session,
    get_session,
    get_user_session_id,
    is_session_id_valid,
    is_session_valid,
    register_failed_attempt,
    reset_failed_attempts,
    is_blocked,
    close_session,
    close_session_by_id,
    list_active_sessions,
    summarize_sessions,
    FAILED_ATTEMPTS,
)


def test_create_session_returns_session_id():
    session_id = create_session(
        user_id="celine",
        device_id="local_pc",
        role="OWNER",
    )

    assert session_id
    assert get_session(session_id)["user_id"] == "celine"


def test_get_user_session_id():
    session_id = create_session("user_session_test")

    assert get_user_session_id("user_session_test") == session_id


def test_is_session_id_valid_true():
    session_id = create_session("valid_session_user")

    assert is_session_id_valid(session_id) is True


def test_is_session_valid_legacy_true():
    create_session("legacy_user")

    assert is_session_valid("legacy_user") is True


def test_register_failed_attempt_and_blocked():
    user_id = "blocked_user_test"
    reset_failed_attempts(user_id)

    for _ in range(10):
        register_failed_attempt(user_id)

    assert is_blocked(user_id) is True


def test_reset_failed_attempts():
    user_id = "reset_user_test"
    register_failed_attempt(user_id)
    reset_failed_attempts(user_id)

    assert FAILED_ATTEMPTS[user_id] == 0


def test_close_session_by_user():
    user_id = "close_user_test"
    create_session(user_id)

    close_session(user_id)

    assert is_session_valid(user_id) is False


def test_close_session_by_id():
    session_id = create_session("close_by_id_user")

    result = close_session_by_id(session_id)

    assert result is True
    assert is_session_id_valid(session_id) is False


def test_close_unknown_session_id_false():
    assert close_session_by_id("unknown-session-id") is False


def test_list_active_sessions_returns_dict():
    create_session("active_user_test")

    sessions = list_active_sessions()

    assert isinstance(sessions, dict)


def test_summarize_sessions():
    create_session("summary_user_test")

    summary = summarize_sessions()

    assert "active_sessions" in summary
    assert "known_sessions" in summary
    assert "blocked_users" in summary
    assert "failed_attempts" in summary
    