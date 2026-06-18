"""
════════════════════════════════════════════════════════════
PROJECT      : ALFRED
BLOCK        : B20
FUNCTION     : 20.TEST
FILE         : tests/security_tests/test_session_anomaly_detector.py
ROLE         : Tests unitaires — session_anomaly_detector.py

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-06-01
VERSION      : V1.0
STATUS       : ACTIVE
════════════════════════════════════════════════════════════
"""

import pytest
from src.security.session_anomaly_detector import (
    record_session_start, record_request, clear_user_state,
    detect_session_hopping, detect_request_flooding,
    detect_device_switching, detect_unusual_hour,
    analyze_session,
    MAX_SESSIONS_PER_HOUR, MAX_REQUESTS_PER_MINUTE,
)


@pytest.fixture(autouse=True)
def clean_user():
    uid = "test_user_anomaly"
    clear_user_state(uid)
    yield uid
    clear_user_state(uid)


# ─── session hopping ──────────────────────────────────────────────────────────

def test_no_hopping_single_session(clean_user):
    record_session_start(clean_user, "sess_001")
    r = detect_session_hopping(clean_user)
    assert r["is_anomaly"] is False

def test_hopping_detected_above_threshold(clean_user):
    for i in range(MAX_SESSIONS_PER_HOUR + 1):
        record_session_start(clean_user, f"sess_{i:03d}")
    r = detect_session_hopping(clean_user)
    assert r["is_anomaly"] is True
    assert r["severity"] == "HIGH"

def test_hopping_structure(clean_user):
    r = detect_session_hopping(clean_user)
    for k in {"user_id","sessions_count","max_allowed","is_anomaly","severity"}:
        assert k in r


# ─── request flooding ────────────────────────────────────────────────────────

def test_no_flood_single_request(clean_user):
    record_request(clean_user, "s001")
    r = detect_request_flooding(clean_user)
    assert r["is_flooding"] is False

def test_flood_detected(clean_user):
    for i in range(MAX_REQUESTS_PER_MINUTE + 5):
        record_request(clean_user, "s001")
    r = detect_request_flooding(clean_user)
    assert r["is_flooding"] is True

def test_flooding_structure(clean_user):
    r = detect_request_flooding(clean_user)
    for k in {"user_id","requests_in_window","rate_per_minute","is_flooding","is_bot_like","is_anomaly"}:
        assert k in r


# ─── device switching ────────────────────────────────────────────────────────

def test_no_device_switch_single_device(clean_user):
    record_request(clean_user, "s001", device_id="device_A")
    record_request(clean_user, "s001", device_id="device_A")
    r = detect_device_switching(clean_user)
    assert r["is_anomaly"] is False
    assert r["device_count"] == 1

def test_device_switch_detected(clean_user):
    record_request(clean_user, "s001", device_id="device_A")
    record_request(clean_user, "s001", device_id="device_B")
    r = detect_device_switching(clean_user)
    assert r["is_anomaly"] is True
    assert r["device_count"] == 2

def test_device_switch_severity(clean_user):
    for dev in ["A", "B", "C"]:
        record_request(clean_user, "s001", device_id=dev)
    r = detect_device_switching(clean_user)
    assert r["severity"] == "HIGH"


# ─── unusual hour ────────────────────────────────────────────────────────────

def test_unusual_hour_structure(clean_user):
    r = detect_unusual_hour(clean_user)
    for k in {"user_id","hour_utc","is_unusual","range","severity"}:
        assert k in r

def test_unusual_hour_returns_bool(clean_user):
    r = detect_unusual_hour(clean_user)
    assert isinstance(r["is_unusual"], bool)

def test_unusual_hour_range_valid(clean_user):
    r = detect_unusual_hour(clean_user)
    assert 0 <= r["hour_utc"] <= 23


# ─── analyze_session ─────────────────────────────────────────────────────────

def test_analyze_clean_session(clean_user):
    record_session_start(clean_user, "sess_001")
    record_request(clean_user, "sess_001", device_id="device_A")
    r = analyze_session(clean_user, "sess_001", "device_A")
    assert r["risk_score"] >= 0
    assert r["risk_level"] in {"LOW","MEDIUM","HIGH","CRITICAL"}

def test_analyze_structure(clean_user):
    r = analyze_session(clean_user)
    for k in {"user_id","risk_score","risk_level","anomalies","is_suspicious","timestamp","details"}:
        assert k in r

def test_analyze_high_risk_on_flood(clean_user):
    for i in range(MAX_REQUESTS_PER_MINUTE + 10):
        record_request(clean_user, "s001")
    r = analyze_session(clean_user)
    assert r["risk_score"] >= 25

def test_analyze_anomalies_list(clean_user):
    r = analyze_session(clean_user)
    assert isinstance(r["anomalies"], list)

def test_clear_user_resets_state(clean_user):
    record_request(clean_user, "s001")
    clear_user_state(clean_user)
    r = detect_request_flooding(clean_user)
    assert r["requests_in_window"] == 0


# ─── Isolation des utilisateurs ───────────────────────────────────────────────

def test_different_users_isolated():
    uid_a = "user_iso_A_test"
    uid_b = "user_iso_B_test"
    clear_user_state(uid_a)
    clear_user_state(uid_b)
    try:
        for _ in range(MAX_SESSIONS_PER_HOUR + 1):
            record_session_start(uid_a, "s")
        r_b = detect_session_hopping(uid_b)
        assert r_b["is_anomaly"] is False
    finally:
        clear_user_state(uid_a)
        clear_user_state(uid_b)
