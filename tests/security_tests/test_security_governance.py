"""
════════════════════════════════════════════════════════════
PROJECT      : ALFRED
BLOCK        : B20
FUNCTION     : 20.15
FILE         : tests/security_tests/test_security_governance.py
ROLE         : Tests unitaires — security_governance.py

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-06-01
UPDATED      : 2026-06-01
VERSION      : V1.0
STATUS       : ACTIVE

DESCRIPTION :
Couvre : SecurityGovernance — run_hardening_checks,
get_risk_matrix, get_recommendations, generate_governance_report.
════════════════════════════════════════════════════════════
"""

import pytest
from src.security.security_governance import SecurityGovernance


# ─── Fixture ─────────────────────────────────────────────────────────────────

@pytest.fixture
def gov():
    return SecurityGovernance()


# ─── run_hardening_checks ────────────────────────────────────────────────────

def test_hardening_checks_returns_list(gov):
    result = gov.run_hardening_checks()
    assert isinstance(result, list)


def test_hardening_checks_not_empty(gov):
    result = gov.run_hardening_checks()
    assert len(result) > 0


def test_hardening_checks_finding_structure(gov):
    findings = gov.run_hardening_checks()
    required = {"title", "passed", "severity", "recommendation", "category"}
    for f in findings:
        assert required.issubset(f.keys()), f"Clés manquantes dans : {f}"


def test_hardening_checks_passed_is_bool(gov):
    findings = gov.run_hardening_checks()
    for f in findings:
        assert isinstance(f["passed"], bool)


def test_hardening_checks_severity_valid(gov):
    valid = {"CRITICAL", "HIGH", "MEDIUM", "LOW"}
    findings = gov.run_hardening_checks()
    for f in findings:
        assert f["severity"] in valid, f"Sévérité invalide : {f['severity']}"


def test_hardening_checks_resets_on_each_call(gov):
    first = gov.run_hardening_checks()
    second = gov.run_hardening_checks()
    assert len(first) == len(second)


def test_hardening_checks_has_auth_check(gov):
    findings = gov.run_hardening_checks()
    categories = {f["category"] for f in findings}
    assert "AUTHENTIFICATION" in categories


def test_hardening_checks_has_encryption_check(gov):
    findings = gov.run_hardening_checks()
    categories = {f["category"] for f in findings}
    assert "CHIFFREMENT" in categories


def test_hardening_checks_has_rbac_check(gov):
    findings = gov.run_hardening_checks()
    categories = {f["category"] for f in findings}
    assert "AUTORISATION" in categories


# ─── get_risk_matrix ─────────────────────────────────────────────────────────

def test_risk_matrix_returns_list(gov):
    gov.run_hardening_checks()
    result = gov.get_risk_matrix()
    assert isinstance(result, list)


def test_risk_matrix_only_failed_items(gov):
    gov.run_hardening_checks()
    risks = gov.get_risk_matrix()
    for r in risks:
        assert "risk" in r
        assert "risk_score" in r


def test_risk_matrix_sorted_by_score_desc(gov):
    gov.run_hardening_checks()
    risks = gov.get_risk_matrix()
    if len(risks) >= 2:
        scores = [r["risk_score"] for r in risks]
        assert scores == sorted(scores, reverse=True)


def test_risk_matrix_risk_score_positive(gov):
    gov.run_hardening_checks()
    risks = gov.get_risk_matrix()
    for r in risks:
        assert r["risk_score"] > 0


def test_risk_matrix_required_keys(gov):
    gov.run_hardening_checks()
    risks = gov.get_risk_matrix()
    required = {"risk", "category", "severity", "likelihood", "impact", "risk_score", "recommendation"}
    for r in risks:
        assert required.issubset(r.keys())


def test_risk_matrix_triggers_checks_if_not_run():
    gov = SecurityGovernance()
    risks = gov.get_risk_matrix()
    assert isinstance(risks, list)


# ─── get_recommendations ─────────────────────────────────────────────────────

def test_recommendations_returns_list(gov):
    result = gov.get_recommendations()
    assert isinstance(result, list)


def test_recommendations_required_keys(gov):
    recs = gov.get_recommendations()
    required = {"priority", "category", "finding", "action"}
    for r in recs:
        assert required.issubset(r.keys())


def test_recommendations_sorted_by_priority(gov):
    recs = gov.get_recommendations()
    order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}
    priorities = [order.get(r["priority"], 99) for r in recs]
    assert priorities == sorted(priorities)


def test_recommendations_filter_by_priority(gov):
    gov.run_hardening_checks()
    recs = gov.get_recommendations(priority="HIGH")
    for r in recs:
        assert r["priority"] == "HIGH"


def test_recommendations_filter_unknown_priority_empty(gov):
    gov.run_hardening_checks()
    recs = gov.get_recommendations(priority="NONEXISTENT")
    assert recs == []


def test_recommendations_triggers_checks_if_not_run():
    gov = SecurityGovernance()
    recs = gov.get_recommendations()
    assert isinstance(recs, list)


# ─── generate_governance_report ──────────────────────────────────────────────

def test_governance_report_returns_string(gov):
    result = gov.generate_governance_report()
    assert isinstance(result, str)


def test_governance_report_not_empty(gov):
    result = gov.generate_governance_report()
    assert len(result) > 50


def test_governance_report_contains_header(gov):
    result = gov.generate_governance_report()
    assert "GOUVERNANCE" in result or "gouvernance" in result.lower()


def test_governance_report_contains_score(gov):
    result = gov.generate_governance_report()
    assert "%" in result


def test_governance_report_lists_findings(gov):
    result = gov.generate_governance_report()
    assert "[+" in result or "[-" in result
