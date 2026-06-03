"""
════════════════════════════════════════════════════════════
PROJECT      : ALFRED
BLOCK        : B20
FUNCTION     : 20.08
FILE         : incident_correlation.py
ROLE         : Corrélation incidents/audit/anomalies pour score de risque SOC

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-05-10
UPDATED      : 2026-06-01
VERSION      : V1.1
STATUS       : STABLE

DESCRIPTION :
Corrèle incidents, événements d'audit et anomalies comportementales
sur une fenêtre temporelle configurable. V1.1 : filtrage temporel,
intégration behavioral_detector, score cumulatif multi-sources.
════════════════════════════════════════════════════════════
"""
from collections import Counter
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, List

from src.security.audit_trail import read_audit_events_since, summarize_audit_events
from src.security.incident_manager import list_incidents, summarize_incidents
from src.security.security_logger import log_event


DENY_DECISIONS = {
    "DENY",
    "DENY_INPUT",
    "DENY_THREAT",
    "DENY_DEVICE",
    "DENY_PERMISSION",
    "DENY_POLICY",
    "DENY_RISK",
}


def _now() -> str:
    """Retourne un timestamp UTC ISO."""
    return datetime.now(timezone.utc).isoformat()


def _level_score(level: str) -> int:
    """Convertit un niveau incident en score."""
    mapping = {
        "LOW": 5,
        "MEDIUM": 15,
        "HIGH": 30,
        "CRITICAL": 50,
    }

    return mapping.get(str(level).upper(), 0)


def _risk_level(score: int) -> str:
    """Convertit un score global en niveau lisible."""
    if score >= 100:
        return "CRITICAL"
    if score >= 70:
        return "HIGH"
    if score >= 35:
        return "MEDIUM"
    return "LOW"


def correlate_security_events(lookback_hours: float = 24.0) -> Dict[str, Any]:
    """
    Corrèle les incidents et événements d'audit sur une fenêtre temporelle.

    Args:
        lookback_hours : fenêtre d'analyse en heures (défaut 24h)

    Returns:
        dict exploitable par dashboard B20 et SOC monitor.
    """
    audit_events = read_audit_events_since(lookback_hours)
    incidents    = list_incidents()

    denied_events = [
        event for event in audit_events
        if str(event.get("decision", "")).upper() in DENY_DECISIONS
    ]

    open_incidents = [
        incident for incident in incidents
        if incident.get("status") in {"OPEN", "INVESTIGATING"}
    ]

    users_denied = Counter(
        event.get("user_id", "unknown_user")
        for event in denied_events
    )

    devices_denied = Counter(
        event.get("device_id", "unknown_device")
        for event in denied_events
        if event.get("device_id")
    )

    resources_denied = Counter(
        event.get("resource", "unknown_resource")
        for event in denied_events
    )

    decisions = Counter(
        event.get("decision", "UNKNOWN")
        for event in denied_events
    )

    signals: List[str] = []
    score = 0

    # Score basé sur les incidents ouverts.
    for incident in open_incidents:
        score += _level_score(incident.get("level", "LOW"))

    # Score basé sur les refus.
    score += len(denied_events) * 2

    # Répétitions utilisateur.
    for user_id, count in users_denied.items():
        if count >= 5:
            signals.append(f"Refus répétés pour utilisateur : {user_id} ({count})")
            score += 15

    # Répétitions appareil.
    for device_id, count in devices_denied.items():
        if count >= 3:
            signals.append(f"Refus répétés pour appareil : {device_id} ({count})")
            score += 20

    # Ressources sensibles souvent refusées.
    for resource, count in resources_denied.items():
        if count >= 5:
            signals.append(f"Ressource fréquemment ciblée : {resource} ({count})")
            score += 15

    # Trop de DENY_THREAT.
    if decisions.get("DENY_THREAT", 0) >= 3:
        signals.append(
            f"Menaces répétées détectées : {decisions.get('DENY_THREAT')} DENY_THREAT"
        )
        score += 25

    # Incident critique ouvert.
    critical_open = [
        incident for incident in open_incidents
        if incident.get("level") == "CRITICAL"
    ]

    if critical_open:
        signals.append(f"Incident critique ouvert : {len(critical_open)}")
        score += 40

    # ── Intégration behavioral_detector (si disponible) ───────────────────────
    try:
        from src.security.behavioral_detector import get_event_rate
        deny_rate = get_event_rate("audit_deny_events", window_seconds=300.0)
        if deny_rate["rate_per_minute"] > 10:
            signals.append(
                f"Taux de refus élevé : {deny_rate['rate_per_minute']:.1f}/min"
            )
            score += 20
    except Exception:
        pass

    score = min(score, 200)   # pas de cap à 100 — le SOC monitor gère la normalisation

    result = {
        "timestamp": _now(),
        "lookback_hours": lookback_hours,
        "security_risk_score": score,
        "security_risk_level": _risk_level(score),
        "signals": signals,
        "audit_summary": summarize_audit_events(),
        "incident_summary": summarize_incidents(),
        "top_denied_users": users_denied.most_common(5),
        "top_denied_devices": devices_denied.most_common(5),
        "top_denied_resources": resources_denied.most_common(5),
        "deny_decisions": dict(decisions),
    }

    log_event(
        f"Incident correlation executed risk_score={score} "
        f"risk_level={result['security_risk_level']}",
        "WARNING" if score >= 35 else "INFO",
    )

    return result


def has_active_security_alert() -> bool:
    """Indique si la corrélation détecte une alerte active."""
    result = correlate_security_events()
    return result["security_risk_level"] in {"HIGH", "CRITICAL"}


def get_security_dashboard_snapshot() -> Dict[str, Any]:
    """
    Retourne une synthèse courte pour dashboard B20.
    """
    correlation = correlate_security_events()

    return {
        "risk_score": correlation["security_risk_score"],
        "risk_level": correlation["security_risk_level"],
        "signals_count": len(correlation["signals"]),
        "signals": correlation["signals"][:5],
        "audit_total": correlation["audit_summary"].get("total", 0),
        "incident_total": correlation["incident_summary"].get("total", 0),
        "open_critical": correlation["incident_summary"].get("open_critical", 0),
    }