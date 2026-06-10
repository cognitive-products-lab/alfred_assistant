"""
PROJECT      : ALFRED
BLOCK        : B20
FUNCTION     : XX.XX
FILE         : test_policy_engine.py
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
Tests B20 — policy_engine.py
"""

from src.security.policy_engine import (
    evaluate_policy,
    explain_policy_decision,
    get_policy_matrix,
)


def test_owner_can_access_critical_resource():
    decision = evaluate_policy(
        role="OWNER",
        resource_sensitivity="CRITICAL",
        action="read",
    )

    assert decision == "ALLOW"


def test_guest_cannot_access_critical_resource():
    decision = evaluate_policy(
        role="GUEST",
        resource_sensitivity="CRITICAL",
        action="read",
    )

    assert decision == "DENY_POLICY"


def test_only_owner_can_delete_data():
    decision = evaluate_policy(
        role="ADMIN",
        resource_sensitivity="LOW",
        action="DELETE_DATA",
    )

    assert decision == "DENY_PERMISSION"


def test_high_risk_is_denied():
    decision = evaluate_policy(
        role="OWNER",
        resource_sensitivity="LOW",
        action="chat",
        risk_score=90,
    )

    assert decision == "DENY_RISK"


def test_medium_high_risk_on_sensitive_resource_requires_review():
    decision = evaluate_policy(
        role="OWNER",
        resource_sensitivity="HIGH",
        action="read",
        risk_score=60,
    )

    assert decision == "REVIEW"


def test_user_can_access_medium_resource():
    decision = evaluate_policy(
        role="USER",
        resource_sensitivity="MEDIUM",
        action="read",
    )

    assert decision == "ALLOW"


def test_guest_cannot_access_medium_resource():
    decision = evaluate_policy(
        role="GUEST",
        resource_sensitivity="MEDIUM",
        action="read",
    )

    assert decision == "DENY_PERMISSION"


def test_session_high_risk_requires_review():
    decision = evaluate_policy(
        role="OWNER",
        resource_sensitivity="LOW",
        action="chat",
        context={"session_risk": "HIGH"},
    )

    assert decision == "REVIEW"


def test_explain_policy_decision():
    assert "autorisé" in explain_policy_decision("ALLOW")


def test_get_policy_matrix():
    matrix = get_policy_matrix()

    assert "role_levels" in matrix
    assert "resource_sensitivity_levels" in matrix
    assert "action_requirements" in matrix