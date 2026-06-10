"""
════════════════════════════════════════════════════════════
PROJECT      : ALFRED
BLOCK        : B20
FUNCTION     : 20.TEST
FILE         : tests/security_tests/test_behavioral_detector.py
ROLE         : Tests unitaires — behavioral_detector.py V2

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-06-01
UPDATED      : 2026-06-01
VERSION      : V2.0
STATUS       : ACTIVE
════════════════════════════════════════════════════════════
"""

import pytest
from src.security.behavioral_detector import (
    update_baseline, get_baseline, reset_baseline,
    detect_behavior_anomaly, detect_statistical_anomaly, record_and_detect,
    calculate_behavior_score, analyze_behavior_metric,
    calculate_weighted_behavior_score, assess_behavior_profile,
    record_event_rate, get_event_rate,
)


@pytest.fixture(autouse=True)
def clean_metric(request):
    name = f"test_{request.node.name}"
    reset_baseline(name)
    yield name
    reset_baseline(name)


# ─── Baseline persistée ───────────────────────────────────────────────────────

def test_baseline_starts_empty(clean_metric):
    assert get_baseline(clean_metric)["samples"] == 0

def test_update_single(clean_metric):
    update_baseline(clean_metric, 10.0)
    assert get_baseline(clean_metric)["mean"] == pytest.approx(10.0)
    assert get_baseline(clean_metric)["samples"] == 1

def test_welford_mean(clean_metric):
    for v in [10.0, 20.0, 30.0]:
        update_baseline(clean_metric, v)
    assert get_baseline(clean_metric)["mean"] == pytest.approx(20.0, abs=0.01)

def test_welford_std(clean_metric):
    for v in [10.0, 20.0, 30.0]:
        update_baseline(clean_metric, v)
    assert get_baseline(clean_metric)["std"] > 0.0

def test_reset_metric(clean_metric):
    update_baseline(clean_metric, 42.0)
    reset_baseline(clean_metric)
    assert get_baseline(clean_metric)["samples"] == 0


# ─── Détection statistique Z-score ───────────────────────────────────────────

def test_no_anomaly_few_samples(clean_metric):
    for v in [10.0] * 5:
        update_baseline(clean_metric, v)
    assert detect_statistical_anomaly(clean_metric, 1000.0)["is_anomaly"] is False

def test_anomaly_detected(clean_metric):
    for v in [10.0] * 20:
        update_baseline(clean_metric, v)
    r = detect_statistical_anomaly(clean_metric, 1000.0, sigma_threshold=3.0)
    assert r["is_anomaly"] is True
    assert r["z_score"] > 3.0

def test_no_anomaly_in_range(clean_metric):
    for v in [50.0 + i for i in range(20)]:
        update_baseline(clean_metric, v)
    assert detect_statistical_anomaly(clean_metric, 55.0)["is_anomaly"] is False

def test_result_structure(clean_metric):
    r = detect_statistical_anomaly(clean_metric, 42.0)
    for k in {"metric_name","current_value","baseline_mean","z_score","is_anomaly","severity"}:
        assert k in r

def test_record_and_detect_updates(clean_metric):
    r = record_and_detect(clean_metric, 50.0)
    assert get_baseline(clean_metric)["samples"] >= 1
    assert "is_anomaly" in r


# ─── Fenêtre temporelle ───────────────────────────────────────────────────────

def test_event_rate_structure():
    r = record_event_rate("evt_test_001", 60.0)
    assert "count_in_window" in r and "rate_per_minute" in r

def test_event_rate_increments():
    k = "evt_incr_001"
    r1 = record_event_rate(k, 60.0)
    r2 = record_event_rate(k, 60.0)
    assert r2["count_in_window"] > r1["count_in_window"]

def test_get_rate_non_destructive():
    k = "evt_get_001"
    record_event_rate(k, 60.0)
    assert get_event_rate(k)["count_in_window"] == get_event_rate(k)["count_in_window"]


# ─── API V1 compat ────────────────────────────────────────────────────────────

def test_detect_anomaly_above():
    assert detect_behavior_anomaly(100.0, 50.0, 20.0) is True

def test_detect_anomaly_below():
    assert detect_behavior_anomaly(55.0, 50.0, 20.0) is False

def test_analyze_metric():
    r = analyze_behavior_metric("cpu", 80.0, 50.0, 20.0)
    assert r["is_anomaly"] is True
    assert r["absolute_deviation"] == pytest.approx(30.0)

def test_calculate_score():
    assert calculate_behavior_score([True, False, True]) == 2

def test_weighted_score():
    a = [{"is_anomaly": True, "absolute_deviation": 60.0, "threshold": 20.0}]
    assert calculate_weighted_behavior_score(a) > 0

def test_assess_dict():
    m = {"a": {"current": 100.0, "baseline": 10.0, "threshold": 20.0}}
    p = assess_behavior_profile(m)
    assert p["anomalies_count"] == 1
    assert p["behavior_level"] in {"LOW","HIGH","CRITICAL"}
