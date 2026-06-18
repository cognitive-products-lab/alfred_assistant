"""
PROJECT      : ALFRED
BLOCK        : B20
FUNCTION     : XX.XX
FILE         : test_security_logger.py
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
Tests B20 — security_logger.py
"""

from src.security.security_logger import (
    log_event,
    log_structured_event,
    log_access,
    log_auth,
    log_incident,
    get_log_file_path,
    read_security_log_tail,
)


def test_log_event_writes_to_file():
    log_event("Test sécurité B20", "INFO")

    log_file = get_log_file_path()

    assert log_file.exists()
    assert "Test sécurité B20" in log_file.read_text(encoding="utf-8")


def test_log_structured_event():
    log_structured_event(
        "TEST_EVENT",
        "INFO",
        user_id="celine",
        result="ALLOW",
    )

    tail = read_security_log_tail(20)
    joined = "\n".join(tail)

    assert "TEST_EVENT" in joined
    assert "user_id=celine" in joined
    assert "result=ALLOW" in joined


def test_log_access():
    log_access(
        user_id="celine",
        action="chat",
        resource="alfred_core",
        result="ALLOW",
        request_id="req-001",
        device_id="local_pc",
        risk_score=0,
    )

    tail = read_security_log_tail(20)
    joined = "\n".join(tail)

    assert "ACCESS" in joined
    assert "user_id=celine" in joined
    assert "result=ALLOW" in joined


def test_log_auth():
    log_auth(
        user_id="celine",
        method="local_pin",
        success=True,
        request_id="req-auth",
        device_id="local_pc",
    )

    tail = read_security_log_tail(20)
    joined = "\n".join(tail)

    assert "AUTH" in joined
    assert "status=SUCCESS" in joined


def test_log_incident():
    log_incident(
        incident_id="inc-001",
        level="WARNING",
        description="Incident test",
        source="pytest",
    )

    tail = read_security_log_tail(20)
    joined = "\n".join(tail)

    assert "INCIDENT" in joined
    assert "inc-001" in joined
    assert "Incident test" in joined