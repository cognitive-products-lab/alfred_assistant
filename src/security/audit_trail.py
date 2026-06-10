"""
════════════════════════════════════════════════════════════
PROJECT      : ALFRED
BLOCK        : B20
FUNCTION     : 20.02
FILE         : audit_trail.py
ROLE         : Piste d'audit JSONL des événements de sécurité

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-05-23
UPDATED      : 2026-06-01
VERSION      : V1.2
STATUS       : ACTIVE

DESCRIPTION :
Enregistre, lit et résume les événements d'audit au format JSONL.
V1.2 : rotation automatique (taille max + archive horodatée),
filtrage par décision/user/fenêtre temporelle.
════════════════════════════════════════════════════════════
"""
import json
import shutil
from collections import Counter
from datetime import datetime, timezone, timedelta
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[2]
AUDIT_FILE  = _ROOT / "logs" / "security" / "audit_trail.jsonl"
ARCHIVE_DIR = _ROOT / "logs" / "security" / "archives"
AUDIT_FILE.parent.mkdir(parents=True, exist_ok=True)
ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)

MAX_AUDIT_LINES = 10_000   # rotation déclenchée au-delà de ce seuil
MAX_AUDIT_BYTES = 5 * 1024 * 1024  # 5 Mo


def _rotate_if_needed() -> None:
    """Rotation du fichier d'audit si dépassement de taille."""
    if not AUDIT_FILE.exists():
        return
    size  = AUDIT_FILE.stat().st_size
    lines = sum(1 for _ in AUDIT_FILE.open(encoding="utf-8"))
    if size < MAX_AUDIT_BYTES and lines < MAX_AUDIT_LINES:
        return
    ts   = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    dest = ARCHIVE_DIR / f"audit_trail_{ts}.jsonl"
    shutil.copy2(AUDIT_FILE, dest)
    AUDIT_FILE.write_text("", encoding="utf-8")


def write_audit_event(
    user_id: str, action: str, resource: str, decision: str,
    request_id: str = "", device_id: str = "", role: str = "", risk_score: int = 0,
) -> dict:
    """Écrit un événement d'audit au format JSONL. Retourne l'événement."""
    event = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "user_id": user_id,
        "action": action,
        "resource": resource,
        "decision": decision,
        "request_id": request_id,
        "device_id": device_id,
        "role": role,
        "risk_score": risk_score,
    }
    _rotate_if_needed()
    with AUDIT_FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")
    return event


def read_audit_events() -> list:
    """Retourne tous les événements d'audit sous forme de liste de dicts."""
    if not AUDIT_FILE.exists():
        return []
    events = []
    try:
        for line in AUDIT_FILE.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line:
                try:
                    events.append(json.loads(line))
                except json.JSONDecodeError:
                    pass
    except OSError:
        pass
    return events


def read_audit_events_since(hours: float = 24.0) -> list:
    """Retourne les événements d'audit des dernières N heures."""
    cutoff = datetime.now(timezone.utc) - timedelta(hours=hours)
    result = []
    for e in read_audit_events():
        try:
            ts = datetime.fromisoformat(e.get("timestamp", ""))
            if ts.tzinfo is None:
                ts = ts.replace(tzinfo=timezone.utc)
            if ts >= cutoff:
                result.append(e)
        except (ValueError, TypeError):
            pass
    return result


def read_audit_events_by_user(user_id: str) -> list:
    """Retourne les événements d'audit pour un utilisateur spécifique."""
    return [e for e in read_audit_events() if e.get("user_id") == user_id]


def list_audit_events_by_decision(decision: str) -> list:
    """Retourne les événements filtrés par décision."""
    return [e for e in read_audit_events() if e.get("decision") == decision]


def clear_audit_trail(confirm: bool = False) -> bool:
    """Efface le fichier d'audit si confirm=True. Retourne True si effacé."""
    if not confirm:
        return False
    if AUDIT_FILE.exists():
        AUDIT_FILE.write_text("", encoding="utf-8")
    return True


def summarize_audit_events() -> dict:
    """Résumé statistique des événements d'audit."""
    events = read_audit_events()
    decisions = Counter(e.get("decision", "UNKNOWN") for e in events)
    risk_scores = [e.get("risk_score", 0) for e in events]
    avg_risk = round(sum(risk_scores) / len(risk_scores), 2) if risk_scores else 0.0
    return {
        "total": len(events),
        "allow": decisions.get("ALLOW", 0),
        "deny": sum(v for k, v in decisions.items() if "DENY" in k),
        "review": decisions.get("REVIEW", 0),
        "average_risk_score": avg_risk,
        "by_decision": dict(decisions),
    }
