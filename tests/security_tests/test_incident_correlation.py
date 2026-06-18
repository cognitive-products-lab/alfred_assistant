"""
PROJECT      : ALFRED
BLOCK        : B20
FUNCTION     : XX.XX
FILE         : test_incident_correlation.py
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
Tests B20 — incident_correlation.py
"""

from src.security.audit_trail import clear_audit_trail, write_audit_event
from src.security.incident_manager import register_incident, list_incidents
from src.security.incident_correlation import (
    correlate_security_events,
    has_active_security_alert,
    get_security_dashboard_snapshot,
)


def test_correlation_with_no_events():
    clear_audit_trail(confirm=True)

    result = correlate_security_events()

    assert "security_risk_score" in result
    assert "security_risk_level" in result
    assert "signals" in result


def test_correlation_detects_repeated_denied_user():
    clear_audit_trail(confirm=True)

    for _ in range(5):
        write_audit_event(
            user_id="guest",
            action="admin",
            resource="alfred_core",
            decision="DENY_PERMISSION",
            device_id="unknown_device",
            risk_score=30,
        )

    result = correlate_security_events()

    assert result["security_risk_score"] > 0
    assert any("utilisateur" in signal for signal in result["signals"])


def test_correlation_detects_repeated_denied_device():
    clear_audit_trail(confirm=True)

    for _ in range(3):
        write_audit_event(
            user_id="guest",
            action="chat",
            resource="alfred_core",
            decision="DENY_DEVICE",
            device_id="bad_device",
            risk_score=40,
        )

    result = correlate_security_events()

    assert any("appareil" in signal for signal in result["signals"])


def test_correlation_detects_repeated_threats():
    clear_audit_trail(confirm=True)

    for _ in range(3):
        write_audit_event(
            user_id="guest",
            action="chat",
            resource="alfred_core",
            decision="DENY_THREAT",
            device_id="unknown_device",
            risk_score=80,
        )

    result = correlate_security_events()

    assert "DENY_THREAT" in result["deny_decisions"]
    assert any("Menaces répétées" in signal for signal in result["signals"])


def test_dashboard_snapshot_contains_expected_fields():
    clear_audit_trail(confirm=True)

    write_audit_event(
        user_id="guest",
        action="admin",
        resource="alfred_core",
        decision="DENY_PERMISSION",
        risk_score=30,
    )

    snapshot = get_security_dashboard_snapshot()

    assert "risk_score" in snapshot
    assert "risk_level" in snapshot
    assert "signals_count" in snapshot
    assert "audit_total" in snapshot
    assert "incident_total" in snapshot


def test_active_security_alert_returns_boolean():
    result = has_active_security_alert()

    assert isinstance(result, bool)
    