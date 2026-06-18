"""
════════════════════════════════════════════════════════════
PROJECT      : ALFRED
BLOCK        : B20
FUNCTION     : 20.15
FILE         : soc_monitor.py
ROLE         : SOC Monitor — agrégation des signaux et alertes sécurité

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-05-23
UPDATED      : 2026-05-23
VERSION      : V1.0
STATUS       : ACTIVE

DESCRIPTION :
Couche SOC finale : agrège incidents, corrélations réseau et API en alertes classifiées.
════════════════════════════════════════════════════════════
"""
from __future__ import annotations
"""
soc_monitor.py
Bloc 20.15 — SOC Monitor (Security Operations Center) pour ALFRED.

Rôle :
- agrégation de tous les signaux sécurité (incidents, corrélation, réseau, API) ;
- génération d'alertes SOC classifiées (LOW / MEDIUM / HIGH / CRITICAL) ;
- watchdog continu en thread daemon optionnel ;
- export d'un snapshot SOC exploitable par le dashboard B20.

Ce module est la couche d'orchestration finale du Bloc 20.
Il ne remplace pas un SIEM professionnel mais offre une visibilité SOC locale.
"""


import json
import threading
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from src.security.security_logger import log_event
from src.security.incident_manager import list_incidents
from src.security.incident_correlation import correlate_security_events
from src.security.behavioral_detector import detect_behavior_anomaly
from src.security.rate_limiter import get_status as get_rate_status
from src.security.network_security import get_network_status
from src.security.api_security import get_api_security_status

SOC_LOG_FILE = Path("logs/security/soc_alerts.jsonl")
SOC_LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

_watchdog_thread: threading.Thread | None = None
_watchdog_running = False
_watchdog_interval = 300  # secondes entre chaque cycle SOC

_last_snapshot: dict[str, Any] = {}
_snapshot_lock = threading.Lock()


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _write_soc_alert(alert: dict) -> None:
    """Persiste une alerte SOC en JSONL."""
    with SOC_LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(alert, ensure_ascii=False) + "\n")


def _classify_risk(score: int) -> str:
    if score >= 100:
        return "CRITICAL"
    if score >= 60:
        return "HIGH"
    if score >= 30:
        return "MEDIUM"
    return "LOW"


def run_soc_cycle() -> dict[str, Any]:
    """
    Exécute un cycle SOC complet.

    Agrège les signaux de tous les modules de sécurité,
    calcule un score SOC global et génère une alerte si nécessaire.

    Returns:
        Snapshot SOC complet.
    """
    alerts: list[dict] = []
    soc_score = 0

    # --- Corrélation incidents / audit ---
    try:
        correlation = correlate_security_events()
        risk_score = correlation.get("security_risk_score", 0)
        risk_level = correlation.get("security_risk_level", "LOW")
        soc_score += risk_score

        if risk_level in {"HIGH", "CRITICAL"}:
            alerts.append({
                "source": "incident_correlation",
                "level": risk_level,
                "message": f"Corrélation incidents : score={risk_score} niveau={risk_level}",
                "signals": correlation.get("signals", []),
            })
    except Exception as exc:
        log_event(f"SOC — erreur corrélation incidents : {exc}", "ERROR")
        correlation = {}

    # --- Incidents ouverts critiques ---
    try:
        incidents = list_incidents()
        open_critical = [i for i in incidents if i.get("level") == "CRITICAL" and i.get("status") in {"OPEN", "INVESTIGATING"}]
        if open_critical:
            soc_score += len(open_critical) * 40
            alerts.append({
                "source": "incident_manager",
                "level": "CRITICAL",
                "message": f"{len(open_critical)} incident(s) critique(s) ouverts",
                "incidents": [i.get("description", "") for i in open_critical[:5]],
            })
    except Exception as exc:
        log_event(f"SOC — erreur lecture incidents : {exc}", "ERROR")
        incidents = []

    # --- Anomalies réseau ---
    try:
        net_status = get_network_status()
        anomalous = net_status.get("anomalous_sources", [])
        if anomalous:
            soc_score += len(anomalous) * 15
            alerts.append({
                "source": "network_security",
                "level": "MEDIUM" if len(anomalous) < 3 else "HIGH",
                "message": f"Anomalies réseau détectées : {len(anomalous)} source(s)",
                "sources": anomalous[:5],
            })
    except Exception as exc:
        log_event(f"SOC — erreur réseau : {exc}", "ERROR")
        net_status = {}

    # --- API : clés verrouillées ---
    try:
        api_status = get_api_security_status()
        locked = api_status.get("locked_keys", 0)
        if locked > 0:
            soc_score += locked * 10
            alerts.append({
                "source": "api_security",
                "level": "MEDIUM" if locked < 5 else "HIGH",
                "message": f"{locked} clé(s) API en rate limit actif",
            })
    except Exception as exc:
        log_event(f"SOC — erreur API security : {exc}", "ERROR")
        api_status = {}

    # --- Analyse de risques EBIOS RM ---
    try:
        from src.security.risk_engine import build_risk_matrix
        risk_matrix = build_risk_matrix(adjust_for_posture=True)
        critical_risks = risk_matrix["by_level"].get("CRITICAL", 0) + risk_matrix["by_level"].get("CRITIQUE", 0)
        if critical_risks > 0:
            soc_score += critical_risks * 20
            alerts.append({
                "source":  "risk_engine",
                "level":   "HIGH",
                "message": f"{critical_risks} risque(s) résiduel(s) CRITIQUE — voir matrice EBIOS",
            })
    except Exception as exc:
        log_event(f"SOC — erreur risk_engine : {exc}", "ERROR")
        risk_matrix = {}

    overall_level = _classify_risk(soc_score)

    snapshot = {
        "timestamp": _now(),
        "soc_score": soc_score,
        "soc_level": overall_level,
        "alerts_count": len(alerts),
        "alerts": alerts,
        "correlation_summary": {
            "risk_score": correlation.get("security_risk_score", 0),
            "risk_level": correlation.get("security_risk_level", "UNKNOWN"),
            "signals": correlation.get("signals", []),
        },
        "incidents": {
            "total": len(incidents),
            "open_critical": len([i for i in incidents if i.get("level") == "CRITICAL" and i.get("status") in {"OPEN", "INVESTIGATING"}]),
        },
        "network":     net_status,
        "api":         api_status,
        "risk_matrix": {
            "global_level":    risk_matrix.get("global_level", "UNKNOWN"),
            "critical_count":  risk_matrix.get("by_level", {}).get("CRITIQUE", 0),
            "eleve_count":     risk_matrix.get("by_level", {}).get("ELEVE", 0),
        } if risk_matrix else {},
    }

    with _snapshot_lock:
        _last_snapshot.clear()
        _last_snapshot.update(snapshot)

    log_level = "CRITICAL" if overall_level == "CRITICAL" else ("ERROR" if overall_level == "HIGH" else ("WARNING" if overall_level == "MEDIUM" else "INFO"))
    log_event(
        f"SOC cycle — score={soc_score} niveau={overall_level} alertes={len(alerts)}",
        log_level,
    )

    if alerts:
        for alert in alerts:
            _write_soc_alert({**alert, "soc_score": soc_score, "soc_level": overall_level, "timestamp": snapshot["timestamp"]})

    return snapshot


def get_last_snapshot() -> dict[str, Any]:
    """Retourne le dernier snapshot SOC sans relancer un cycle complet."""
    with _snapshot_lock:
        if _last_snapshot:
            return dict(_last_snapshot)
    return run_soc_cycle()


def is_soc_critical() -> bool:
    """Retourne True si le dernier snapshot est en niveau CRITICAL ou HIGH."""
    snap = get_last_snapshot()
    return snap.get("soc_level") in {"CRITICAL", "HIGH"}


def get_soc_summary() -> dict[str, Any]:
    """Résumé court pour le dashboard B20."""
    snap = get_last_snapshot()
    return {
        "soc_score": snap.get("soc_score", 0),
        "soc_level": snap.get("soc_level", "UNKNOWN"),
        "alerts_count": snap.get("alerts_count", 0),
        "top_alerts": [a.get("message", "") for a in snap.get("alerts", [])[:3]],
        "timestamp": snap.get("timestamp", _now()),
    }


def _watchdog_loop() -> None:
    """Boucle interne du watchdog SOC."""
    global _watchdog_running
    log_event("SOC watchdog démarré", "INFO")
    while _watchdog_running:
        try:
            run_soc_cycle()
        except Exception as exc:
            log_event(f"SOC watchdog — erreur cycle : {exc}", "ERROR")
        for _ in range(_watchdog_interval):
            if not _watchdog_running:
                break
            time.sleep(1)
    log_event("SOC watchdog arrêté", "INFO")


def start_watchdog(interval_seconds: int = 300) -> None:
    """
    Lance le watchdog SOC en thread daemon.

    Args:
        interval_seconds : Intervalle entre chaque cycle (défaut 5 min).
    """
    global _watchdog_thread, _watchdog_running, _watchdog_interval
    if _watchdog_thread and _watchdog_thread.is_alive():
        log_event("SOC watchdog déjà actif", "WARNING")
        return
    _watchdog_interval = max(60, interval_seconds)
    _watchdog_running = True
    _watchdog_thread = threading.Thread(target=_watchdog_loop, daemon=True, name="soc-watchdog")
    _watchdog_thread.start()


def stop_watchdog() -> None:
    """Arrête le watchdog SOC proprement."""
    global _watchdog_running
    _watchdog_running = False
