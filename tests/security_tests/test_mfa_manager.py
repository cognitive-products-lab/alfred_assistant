"""
PROJECT      : ALFRED
BLOCK        : B20
FUNCTION     : XX.XX
FILE         : test_mfa_manager.py
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
Tests B20 — mfa_manager.py
Couvre : score biométrique, is_mfa_required (_ALWAYS_MFA_ROLES),
         TOTP session (mark_verified / is_verified / revoke).
"""

import pyotp
from src.security.mfa_manager import (
    calculate_mfa_score,
    evaluate_mfa,
    weighted_mfa,
    explain_mfa_result,
    is_mfa_required,
    setup_totp,
    verify_totp,
    mark_verified,
    is_verified,
    revoke,
)


def test_calculate_mfa_score_full_success():
    score = calculate_mfa_score(
        face=True,
        voice=True,
        device=True,
        pin=True,
    )

    assert score == 8


def test_calculate_mfa_score_device_pin_only():
    score = calculate_mfa_score(
        face=False,
        voice=False,
        device=True,
        pin=True,
    )

    assert score == 3


def test_evaluate_mfa_authenticated():
    result = evaluate_mfa(
        face=True,
        voice=False,
        device=True,
        pin=False,
        threshold=5,
        user_id="celine",
        request_id="req-mfa-001",
    )

    assert result["authenticated"] is True
    assert result["score"] == 5
    assert result["threshold"] == 5
    assert result["user_id"] == "celine"


def test_evaluate_mfa_refused():
    result = evaluate_mfa(
        face=False,
        voice=False,
        device=True,
        pin=True,
        threshold=5,
    )

    assert result["authenticated"] is False
    assert result["score"] == 3
    assert "face" in result["missing_factors"]
    assert "voice" in result["missing_factors"]


def test_weighted_mfa_legacy_true():
    assert weighted_mfa(
        face=True,
        voice=False,
        device=True,
        pin=False,
    ) is True


def test_weighted_mfa_legacy_false():
    assert weighted_mfa(
        face=False,
        voice=False,
        device=True,
        pin=True,
    ) is False


def test_explain_mfa_result_authenticated():
    result = evaluate_mfa(
        face=True,
        voice=True,
        device=False,
        pin=False,
        threshold=5,
    )

    explanation = explain_mfa_result(result)

    assert "MFA validé" in explanation


def test_explain_mfa_result_refused():
    result = evaluate_mfa(
        face=False,
        voice=False,
        device=True,
        pin=False,
        threshold=5,
    )

    explanation = explain_mfa_result(result)

    assert "MFA refusé" in explanation


# ─── is_mfa_required — _ALWAYS_MFA_ROLES ─────────────────────────────────────

def test_owner_always_requires_mfa():
    """OWNER doit toujours requérir le MFA indépendamment de la config globale."""
    assert is_mfa_required("OWNER") is True


def test_admin_always_requires_mfa():
    """ADMIN doit toujours requérir le MFA indépendamment de la config globale."""
    assert is_mfa_required("ADMIN") is True


def test_owner_case_insensitive():
    """La vérification doit être insensible à la casse."""
    assert is_mfa_required("owner") is True
    assert is_mfa_required("Owner") is True


# ─── Session TOTP — mark_verified / is_verified / revoke ─────────────────────

def test_totp_session_flow():
    """Cycle complet : setup → verify → mark → is_verified → revoke."""
    user    = "test_mfa_session_user"
    session = "test_session_abc123"

    info = setup_totp(user, force=True)
    assert "secret" in info

    token = pyotp.TOTP(info["secret"]).now()
    ok = verify_totp(user, token)
    assert ok, "Le token TOTP généré doit être valide"

    mark_verified(user, session, ttl_seconds=300)
    assert is_verified(user, session) is True

    revoke(user, session)
    assert is_verified(user, session) is False


def test_unverified_session_not_valid():
    """Une session non marquée comme vérifiée doit retourner False."""
    assert is_verified("ghost_user", "nonexistent_session") is False


def test_different_session_not_valid():
    """La vérification ne doit pas croiser les sessions."""
    user = "test_cross_session_user"
    setup_totp(user, force=True)
    mark_verified(user, "session_A", ttl_seconds=300)
    assert is_verified(user, "session_B") is False