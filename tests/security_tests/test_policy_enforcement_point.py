"""
PROJECT      : ALFRED
BLOCK        : B20
FUNCTION     : 20.13
FILE         : tests/security_tests/test_policy_enforcement_point.py
ROLE         : Tests unitaires policy_enforcement_point.py
AUTHOR       : Cognitive Products Lab
CREATED      : 2026-06-01
VERSION      : V1.0
STATUS       : ACTIVE
"""
import pytest
from src.security.policy_enforcement_point import enforce_decision, enforce_or_raise, explain_decision


def test_enforce_allow_returns_true():
    assert enforce_decision("ALLOW") is True

def test_enforce_deny_returns_false():
    assert enforce_decision("DENY") is False
    assert enforce_decision("DENY_POLICY") is False
    assert enforce_decision("DENY_PERMISSION") is False
    assert enforce_decision("DENY_RISK") is False
    assert enforce_decision("DENY_THREAT") is False

def test_enforce_review_returns_false():
    assert enforce_decision("REVIEW") is False

def test_enforce_unknown_returns_false():
    assert enforce_decision("UNKNOWN_DECISION") is False

def test_enforce_or_raise_allow_no_exception():
    enforce_or_raise("ALLOW")  # ne doit pas lever

def test_enforce_or_raise_deny_raises():
    with pytest.raises(PermissionError):
        enforce_or_raise("DENY_PERMISSION")

def test_explain_decision_allow():
    explanation = explain_decision("ALLOW")
    assert isinstance(explanation, str) and len(explanation) > 0

def test_explain_decision_deny_policy():
    explanation = explain_decision("DENY_POLICY")
    assert isinstance(explanation, str)

def test_explain_decision_deny_risk():
    explanation = explain_decision("DENY_RISK")
    assert isinstance(explanation, str)

def test_explain_all_codes():
    for code in ("ALLOW", "DENY", "DENY_POLICY", "DENY_PERMISSION", "DENY_RISK", "DENY_THREAT", "REVIEW"):
        result = explain_decision(code)
        assert isinstance(result, str)
