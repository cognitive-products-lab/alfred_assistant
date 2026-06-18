"""
════════════════════════════════════════════════════════════
PROJECT      : ALFRED
BLOCK        : B20
FUNCTION     : 20.09
FILE         : incident_manager.py
ROLE         : Registre et gestion des incidents de sécurité

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-05-23
UPDATED      : 2026-05-23
VERSION      : V1.0
STATUS       : ACTIVE

DESCRIPTION :
Enregistre, liste et résume les incidents dans data/security/incident_register.json.
════════════════════════════════════════════════════════════
"""
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from src.security.security_logger import log_event
from paths import PATHS

INCIDENT_FILE = PATHS.data_security / "incident_register.json"
INCIDENT_FILE.parent.mkdir(parents=True, exist_ok=True)


def _load_incidents() -> list:
    if not INCIDENT_FILE.exists():
        return []
    try:
        data = json.loads(INCIDENT_FILE.read_text(encoding="utf-8"))
        return data if isinstance(data, list) else []
    except json.JSONDecodeError:
        return []


def register_incident(level: str, description: str, source: str = "unknown") -> None:
    """Enregistre un incident de sécurité."""
    incident = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "level": level,
        "description": description,
        "source": source,
        "status": "OPEN",
    }

    incidents = _load_incidents()
    incidents.append(incident)
    INCIDENT_FILE.write_text(json.dumps(incidents, indent=4, ensure_ascii=False), encoding="utf-8")

    log_event(f"Incident enregistré : {description}", level)


def list_incidents(status: str | None = None) -> list:
    """Retourne les incidents enregistrés, avec filtre optionnel par statut."""
    incidents = _load_incidents()

    if status is None:
        return incidents

    return [
        incident for incident in incidents
        if str(incident.get("status", "")).upper() == status.upper()
    ]


def summarize_incidents() -> dict:
    """Résumé statistique des incidents pour le dashboard."""
    incidents = _load_incidents()
    levels = Counter(i.get("level", "UNKNOWN") for i in incidents)
    open_critical = sum(
        1 for i in incidents
        if i.get("level") == "CRITICAL" and i.get("status") in {"OPEN", "INVESTIGATING"}
    )
    return {
        "total": len(incidents),
        "by_level": dict(levels),
        "open_critical": open_critical,
    }
