# ============================================================
# ALFRED — src/security/incident_manager.py
# Bloc 20.11 — Réponse à incident
#
# 📚 NOTION EXAM :
#   D42-3 — Capsule 10 : Gestion des incidents de sécurité (IRP / CSIRT)
#
# 🎯 UTILITÉ ALFRED :
#   Enregistre et trace les incidents dans un registre JSON persistant
#   et horodaté pour investigation et escalade.
#
# 🔐 BLOC SÉCURITÉ :
#   Réponse aux incidents — registre structuré OPEN/CLOSED pour le CSIRT
# ============================================================

import json
from datetime import datetime, timezone
from pathlib import Path
from src.security.security_logger import log_event

INCIDENT_FILE = Path("data/security/incident_register.json")
INCIDENT_FILE.parent.mkdir(parents=True, exist_ok=True)

def register_incident(level: str, description: str, source: str = "unknown") -> None:
    """Enregistre un incident de sécurité."""
    incident = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "level": level,
        "description": description,
        "source": source,
        "status": "OPEN",
    }

    incidents = []

    if INCIDENT_FILE.exists():
        try:
            incidents = json.loads(INCIDENT_FILE.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            incidents = []

    incidents.append(incident)
    INCIDENT_FILE.write_text(json.dumps(incidents, indent=4, ensure_ascii=False), encoding="utf-8")

    log_event(f"Incident enregistré : {description}", level)


def _load_incidents() -> list:
    """Charge les incidents depuis le fichier JSON."""
    if not INCIDENT_FILE.exists():
        return []
    try:
        return json.loads(INCIDENT_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return []


def list_incidents(status: str | None = None) -> list:
    """Retourne la liste des incidents (anonymisée — sans source ni user_id).
    status : 'OPEN' | 'CLOSED' | None (tous)
    """
    incidents = _load_incidents()
    if status:
        incidents = [i for i in incidents if i.get("status") == status]
    # Anonymisation : on supprime 'source' pour le dashboard public
    return [
        {
            "timestamp": i.get("timestamp", ""),
            "level":     i.get("level", "UNKNOWN"),
            "status":    i.get("status", "OPEN"),
            "description": i.get("description", "")[:120],  # tronqué
        }
        for i in incidents
    ]


def summarize_incidents() -> dict:
    """Retourne un résumé anonymisé des incidents — pour le dashboard public."""
    incidents = _load_incidents()
    total       = len(incidents)
    open_count  = sum(1 for i in incidents if i.get("status") == "OPEN")
    closed      = total - open_count
    by_level: dict[str, int] = {}
    open_critical = 0
    for i in incidents:
        lvl = i.get("level", "UNKNOWN")
        by_level[lvl] = by_level.get(lvl, 0) + 1
        if i.get("status") == "OPEN" and lvl in ("CRITICAL", "ERROR"):
            open_critical += 1
    return {
        "total":          total,
        "open":           open_count,
        "closed":         closed,
        "open_critical":  open_critical,
        "by_level":       by_level,
    }
