import json
from datetime import datetime, timezone
from pathlib import Path

AUDIT_FILE = Path("logs/security/audit_trail.jsonl")
AUDIT_FILE.parent.mkdir(parents=True, exist_ok=True)

def write_audit_event(user_id: str, action: str, resource: str, decision: str) -> None:
    """Écrit un événement d'audit au format JSONL."""
    event = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "user_id": user_id,
        "action": action,
        "resource": resource,
        "decision": decision,
    }

    with AUDIT_FILE.open("a", encoding="utf-8") as file:
        file.write(json.dumps(event, ensure_ascii=False) + "\n")
