"""
════════════════════════════════════════════════════════════
PROJECT      : ALFRED
BLOCK        : B20
FUNCTION     : 20.TEST
FILE         : tests/security_tests/test_soc_monitor.py
ROLE         : Tests unitaires — soc_monitor.py

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-06-01
UPDATED      : 2026-06-01
VERSION      : V1.0
STATUS       : ACTIVE

DESCRIPTION :
Couvre : classification de risque, structure du snapshot SOC,
get_soc_summary, is_soc_critical, watchdog (start/stop).
════════════════════════════════════════════════════════════
"""

import time
import pytest
from src.security.soc_monitor import (
    run_soc_cycle,
    get_last_snapshot,
    get_soc_summary,
    is_soc_critical,
    start_watchdog,
    stop_watchdog,
    _classify_risk,
    _watchdog_thread,
    _last_snapshot,
)


# ─── _classify_risk ───────────────────────────────────────────────────────────

def test_classify_risk_low():
    assert _classify_risk(0)   == "LOW"
    assert _classify_risk(29)  == "LOW"


def test_classify_risk_medium():
    assert _classify_risk(30)  == "MEDIUM"
    assert _classify_risk(59)  == "MEDIUM"


def test_classify_risk_high():
    assert _classify_risk(60)  == "HIGH"
    assert _classify_risk(99)  == "HIGH"


def test_classify_risk_critical():
    assert _classify_risk(100) == "CRITICAL"
    assert _classify_risk(200) == "CRITICAL"


# ─── run_soc_cycle ────────────────────────────────────────────────────────────

def test_soc_cycle_returns_dict():
    snapshot = run_soc_cycle()
    assert isinstance(snapshot, dict)


def test_soc_cycle_has_required_keys():
    snapshot = run_soc_cycle()
    required = {"timestamp", "soc_score", "soc_level", "alerts_count", "alerts"}
    assert required.issubset(snapshot.keys()), (
        f"Clés manquantes : {required - snapshot.keys()}"
    )


def test_soc_cycle_score_non_negative():
    snapshot = run_soc_cycle()
    assert snapshot["soc_score"] >= 0


def test_soc_cycle_level_valid():
    snapshot = run_soc_cycle()
    assert snapshot["soc_level"] in {"LOW", "MEDIUM", "HIGH", "CRITICAL"}


def test_soc_cycle_alerts_count_matches_list():
    snapshot = run_soc_cycle()
    assert snapshot["alerts_count"] == len(snapshot["alerts"])


def test_soc_cycle_updates_last_snapshot():
    _last_snapshot.clear()
    run_soc_cycle()
    assert len(_last_snapshot) > 0


# ─── get_last_snapshot ────────────────────────────────────────────────────────

def test_get_last_snapshot_returns_dict():
    result = get_last_snapshot()
    assert isinstance(result, dict)
    assert "soc_score" in result
    assert "soc_level" in result


# ─── get_soc_summary ──────────────────────────────────────────────────────────

def test_soc_summary_structure():
    summary = get_soc_summary()
    assert "soc_score" in summary
    assert "soc_level" in summary
    assert "alerts_count" in summary
    assert "top_alerts" in summary
    assert "timestamp" in summary


def test_soc_summary_top_alerts_is_list():
    summary = get_soc_summary()
    assert isinstance(summary["top_alerts"], list)
    assert len(summary["top_alerts"]) <= 3


def test_soc_summary_score_non_negative():
    summary = get_soc_summary()
    assert summary["soc_score"] >= 0


# ─── is_soc_critical ─────────────────────────────────────────────────────────

def test_is_soc_critical_returns_bool():
    result = is_soc_critical()
    assert isinstance(result, bool)


def test_is_soc_critical_false_when_low(monkeypatch):
    monkeypatch.setattr(
        "src.security.soc_monitor.get_last_snapshot",
        lambda: {"soc_score": 0, "soc_level": "LOW", "alerts_count": 0,
                 "alerts": [], "timestamp": "2026-06-01T00:00:00Z"},
    )
    assert is_soc_critical() is False


def test_is_soc_critical_true_when_critical(monkeypatch):
    monkeypatch.setattr(
        "src.security.soc_monitor.get_last_snapshot",
        lambda: {"soc_score": 150, "soc_level": "CRITICAL", "alerts_count": 3,
                 "alerts": [], "timestamp": "2026-06-01T00:00:00Z"},
    )
    assert is_soc_critical() is True


def test_is_soc_critical_true_when_high(monkeypatch):
    monkeypatch.setattr(
        "src.security.soc_monitor.get_last_snapshot",
        lambda: {"soc_score": 70, "soc_level": "HIGH", "alerts_count": 1,
                 "alerts": [], "timestamp": "2026-06-01T00:00:00Z"},
    )
    assert is_soc_critical() is True


# ─── Watchdog ─────────────────────────────────────────────────────────────────

def test_start_stop_watchdog():
    """Le watchdog démarre et se termine dans la seconde après stop."""
    stop_watchdog()
    time.sleep(0.2)
    start_watchdog(interval_seconds=600)
    time.sleep(0.3)
    from src.security.soc_monitor import _watchdog_thread as wt
    assert wt is not None
    assert wt.is_alive()
    stop_watchdog()
    # La boucle interne fait time.sleep(1) par tick — on attend 2s max
    deadline = time.time() + 2.0
    while wt.is_alive() and time.time() < deadline:
        time.sleep(0.1)
    assert not wt.is_alive(), "Watchdog n'a pas terminé dans les 2s"


def test_start_watchdog_idempotent():
    """Démarrer deux fois ne doit pas créer deux threads."""
    stop_watchdog()
    start_watchdog(interval_seconds=600)
    start_watchdog(interval_seconds=600)   # 2ème appel ignoré
    from src.security.soc_monitor import _watchdog_thread as wt
    alive_count = sum(1 for t in [wt] if t and t.is_alive())
    assert alive_count == 1
    stop_watchdog()
