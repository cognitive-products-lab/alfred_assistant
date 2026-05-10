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
