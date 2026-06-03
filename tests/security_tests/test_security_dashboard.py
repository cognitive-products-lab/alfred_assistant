"""
PROJECT      : ALFRED  |  BLOCK : B20  |  FUNCTION : 20.15
FILE         : tests/security_tests/test_security_dashboard.py
AUTHOR       : Cognitive Products Lab  |  CREATED : 2026-06-01  |  STATUS : ACTIVE
"""
import pytest
from src.security.security_dashboard import get_dashboard, SecurityDashboard


def test_get_dashboard_returns_object():
    result = get_dashboard()
    assert result is not None

def test_security_dashboard_instantiable():
    dash = SecurityDashboard()
    assert isinstance(dash, SecurityDashboard)

def test_security_dashboard_has_public_methods():
    dash = SecurityDashboard()
    methods = [m for m in dir(dash) if not m.startswith("_") and callable(getattr(dash, m))]
    assert len(methods) >= 1

def test_get_dashboard_twice_consistent():
    r1 = get_dashboard()
    r2 = get_dashboard()
    assert type(r1) == type(r2)

def test_security_dashboard_str_or_repr():
    dash = SecurityDashboard()
    s = str(dash) or repr(dash)
    assert isinstance(s, str)


# ─── get_audit_summary ───────────────────────────────────────────────────────

def test_audit_summary_returns_dict():
    assert isinstance(get_dashboard().get_audit_summary(), dict)

def test_audit_summary_required_keys():
    result = get_dashboard().get_audit_summary()
    for k in ("period_hours", "total_events", "decisions", "top_actions",
              "top_users", "total_denials", "denial_rate"):
        assert k in result, f"Clé manquante : {k}"

def test_audit_summary_period_matches_lookback():
    assert SecurityDashboard(lookback_hours=12).get_audit_summary()["period_hours"] == 12

def test_audit_summary_denial_rate_is_float():
    assert isinstance(get_dashboard().get_audit_summary()["denial_rate"], float)

def test_audit_summary_total_events_non_negative():
    assert get_dashboard().get_audit_summary()["total_events"] >= 0


# ─── get_threat_summary ──────────────────────────────────────────────────────

def test_threat_summary_required_keys():
    result = get_dashboard().get_threat_summary()
    assert "total_threats" in result and "threats_by_user" in result

def test_threat_summary_total_non_negative():
    assert get_dashboard().get_threat_summary()["total_threats"] >= 0

def test_threat_summary_by_user_is_dict():
    assert isinstance(get_dashboard().get_threat_summary()["threats_by_user"], dict)


# ─── get_incident_summary ────────────────────────────────────────────────────

def test_incident_summary_required_keys():
    result = get_dashboard().get_incident_summary()
    for k in ("total_incidents", "by_level", "by_status", "open_critical"):
        assert k in result

def test_incident_summary_open_critical_non_negative():
    assert get_dashboard().get_incident_summary()["open_critical"] >= 0


# ─── get_device_summary ──────────────────────────────────────────────────────

def test_device_summary_required_keys():
    result = get_dashboard().get_device_summary()
    for k in ("total_devices", "trusted", "revoked"):
        assert k in result

def test_device_summary_counts_non_negative():
    result = get_dashboard().get_device_summary()
    assert result["total_devices"] >= 0 and result["trusted"] >= 0


# ─── get_security_score ──────────────────────────────────────────────────────

def test_security_score_required_keys():
    result = get_dashboard().get_security_score()
    for k in ("score", "grade", "max_score", "deductions"):
        assert k in result

def test_security_score_in_range():
    assert 0 <= get_dashboard().get_security_score()["score"] <= 100

def test_security_score_max_is_100():
    assert get_dashboard().get_security_score()["max_score"] == 100

def test_security_grade_valid():
    assert get_dashboard().get_security_score()["grade"] in {"A", "B", "C", "D", "F"}

def test_security_deductions_is_list():
    assert isinstance(get_dashboard().get_security_score()["deductions"], list)


# ─── get_compliance_status ───────────────────────────────────────────────────

def test_compliance_status_required_keys():
    result = get_dashboard().get_compliance_status()
    for k in ("total", "passed", "failed", "compliance_rate", "checks"):
        assert k in result

def test_compliance_passed_plus_failed_equals_total():
    result = get_dashboard().get_compliance_status()
    assert result["passed"] + result["failed"] == result["total"]

def test_compliance_checks_status_valid():
    for chk in get_dashboard().get_compliance_status()["checks"]:
        assert chk["status"] in ("OK", "KO")


# ─── get_iso27001_status ─────────────────────────────────────────────────────

def test_iso27001_has_10_controls():
    assert get_dashboard().get_iso27001_status()["total"] == 10

def test_iso27001_checks_have_control_field():
    for chk in get_dashboard().get_iso27001_status()["checks"]:
        assert "control" in chk and chk["control"].startswith("A.")


# ─── get_rgpd_status ─────────────────────────────────────────────────────────

def test_rgpd_has_8_articles():
    assert get_dashboard().get_rgpd_status()["total"] == 8

def test_rgpd_checks_have_article_field():
    for chk in get_dashboard().get_rgpd_status()["checks"]:
        assert "article" in chk and "Art." in chk["article"]


# ─── generate_report ─────────────────────────────────────────────────────────

def test_generate_report_returns_string():
    assert isinstance(get_dashboard().generate_report(), str)

def test_generate_report_not_empty():
    assert len(get_dashboard().generate_report()) > 100

def test_generate_report_contains_alfred():
    assert "ALFRED" in get_dashboard().generate_report()
