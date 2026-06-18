"""
PROJECT      : ALFRED
BLOCK        : B20
FUNCTION     : XX.XX
FILE         : test_policy_decision_point.py
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
Tests B20 — policy_decision_point.py
"""

from src.security.policy_decision_point import (
    decide_access,
    decide_access_verbose,
    is_access_allowed,
)


def test_decide_access_allow():
    decision = decide_access(
        role="OWNER",
        resource_sensitivity="LOW",
        action="chat",
    )

    assert decision == "ALLOW"


def test_decide_access_deny_policy():
    decision = decide_access(
        role="GUEST",
        resource_sensitivity="CRITICAL",
        action="read",
    )

    assert decision == "DENY_POLICY"


def test_decide_access_deny_risk():
    decision = decide_access(
        role="OWNER",
        resource_sensitivity="LOW",
        action="chat",
        risk_score=90,
    )

    assert decision == "DENY_RISK"


def test_decide_access_verbose():
    result = decide_access_verbose(
        role="OWNER",
        resource_sensitivity="LOW",
        action="chat",
    )

    assert result["decision"] == "ALLOW"
    assert result["allowed"] is True
    assert "explanation" in result


def test_is_access_allowed_true():
    assert is_access_allowed(
        role="OWNER",
        resource_sensitivity="LOW",
        action="chat",
    ) is True


def test_is_access_allowed_false():
    assert is_access_allowed(
        role="GUEST",
        resource_sensitivity="CRITICAL",
        action="read",
    ) is False