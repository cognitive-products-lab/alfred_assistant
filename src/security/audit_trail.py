# ============================================================
# ALFRED — src/security/audit_trail.py
# Bloc 20.09 — Journalisation & audit
#
# 📚 NOTION EXAM :
#   D43-1 — Capsule 7 : Traçabilité et non-répudiation des événements
#
# 🎯 UTILITÉ ALFRED :
#   Écrit une piste d'audit immuable au format JSONL pour chaque
#   décision d'accès (who, what, where, when, decision).
#
# 🔐 BLOC SÉCURITÉ :
#   Non-répudiation et traçabilité — preuve horodatée de toute action sensible
# ============================================================

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
