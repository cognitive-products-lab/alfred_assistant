"""
PROJECT      : ALFRED
BLOCK        : B20 - Cybersecurite Zero Trust
FUNCTION     : 20.15
FILE         : tools/dashboard_tools/dashboard_security/dashboard_security.py
ROLE         : Genere dashboard_security.json a partir des donnees de securite live

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-05-15
UPDATED      : 2026-06-20
VERSION      : V1.2
STATUS       : STABLE

DESCRIPTION :
Collecte les donnees de securite en temps reel (incidents, acces, SOC, audit),
les formate et les ecrit dans dashboard/dashboard_security/dashboard_security.json
consomme par dashboard_security.html.

Usage :
    cd D:/PROJET_ALFRED/ALFRED_PC
    python tools/dashboard_tools/dashboard_security/dashboard_security.py
"""

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

OUTPUT_FILE = ROOT / "dashboard" / "dashboard_security" / "dashboard_security.json"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def collect_sessions() -> dict:
    try:
        from src.security.session_manager import summarize_sessions
        return summarize_sessions()
    except Exception as exc:
        return {"error": str(exc)}


def collect_devices() -> dict:
    try:
        from src.security.device_registry import list_devices, get_device_info
        trusted = list_devices(include_revoked=False)
        all_devices = list_devices(include_revoked=True)
        return {
            "trusted_count": len(trusted),
            "total_count": len(all_devices),
            "devices": [
                {
                    "device_id": k,
                    "label": v.get("label", k),
                    "owner": v.get("owner", "?"),
                    "trusted": v.get("trusted", False),
                    "risk_level": v.get("risk_level", "UNKNOWN"),
                    "trust_score": v.get("trust_score", 0),
                    "failed_attempts": v.get("failed_attempts", 0),
                    "last_seen": v.get("last_seen", ""),
                }
                for k, v in all_devices.items()
            ],
        }
    except Exception as exc:
        return {"error": str(exc)}


def collect_incidents() -> dict:
    try:
        from src.security.incident_manager import summarize_incidents, list_incidents
        summary = summarize_incidents()
        open_incidents = list_incidents(status="OPEN")
        return {
            **summary,
            "recent_open": open_incidents[-5:] if open_incidents else [],
        }
    except Exception as exc:
        return {"error": str(exc)}


def collect_quarantine() -> dict:
    try:
        from src.security.quarantine_service import summarize_quarantine
        return summarize_quarantine()
    except Exception as exc:
        return {"error": str(exc)}


def collect_secrets() -> dict:
    try:
        from src.security.secret_manager import summarize_secrets
        return summarize_secrets()
    except Exception as exc:
        return {"error": str(exc)}


def collect_encryption() -> dict:
    try:
        from src.security.encryption_service import is_available
        return {"available": is_available()}
    except Exception as exc:
        return {"available": False, "error": str(exc)}


def collect_audit_stats() -> dict:
    try:
        audit_file = ROOT / "logs" / "security" / "audit_trail.jsonl"
        if not audit_file.exists():
            return {"total_events": 0, "last_event": None}

        lines = [l for l in audit_file.read_text(encoding="utf-8").strip().split("\n") if l]
        events = []
        for line in lines:
            try:
                events.append(json.loads(line))
            except Exception:
                pass

        decisions: dict = {}
        for event in events:
            d = event.get("decision", "UNKNOWN")
            decisions[d] = decisions.get(d, 0) + 1

        return {
            "total_events": len(events),
            "by_decision": decisions,
            "last_event": events[-1] if events else None,
        }
    except Exception as exc:
        return {"error": str(exc)}


def collect_permissions() -> dict:
    try:
        from src.security.permission_manager import summarize_permissions
        return summarize_permissions()
    except Exception as exc:
        return {"error": str(exc)}


def collect_roles() -> dict:
    try:
        from src.security.role_manager import list_roles
        return {"roles": list_roles()}
    except Exception as exc:
        return {"error": str(exc)}


def collect_policy_matrix() -> dict:
    try:
        from src.security.policy_engine import get_policy_matrix
        return get_policy_matrix()
    except Exception as exc:
        return {"error": str(exc)}


def compute_security_score(data: dict) -> int:
    """Score de sécurité global 0-100."""
    score = 100

    secrets = data.get("secrets", {})
    if not secrets.get("all_ok", True):
        score -= 30

    encryption = data.get("encryption", {})
    if not encryption.get("available", True):
        score -= 20

    incidents = data.get("incidents", {})
    open_critical = incidents.get("open_critical", 0)
    if open_critical > 0:
        score -= min(30, open_critical * 10)

    quarantine = data.get("quarantine", {})
    active_q = quarantine.get("active_total", 0)
    if active_q > 0:
        score -= min(15, active_q * 5)

    devices = data.get("devices", {})
    risky = sum(
        1 for d in devices.get("devices", [])
        if d.get("risk_level") in {"HIGH", "REVOKED"}
    )
    if risky > 0:
        score -= min(10, risky * 5)

    return max(0, score)


def build_dashboard() -> dict:
    data: dict = {
        "_meta": {
            "project": "ALFRED",
            "block": "B20",
            "file": "dashboard_security.json",
            "generated_at": _now(),
            "version": "V1.0",
        },
        "sessions": collect_sessions(),
        "devices": collect_devices(),
        "incidents": collect_incidents(),
        "quarantine": collect_quarantine(),
        "secrets": collect_secrets(),
        "encryption": collect_encryption(),
        "audit": collect_audit_stats(),
        "permissions": collect_permissions(),
        "roles": collect_roles(),
        "policy_matrix": collect_policy_matrix(),
    }

    data["security_score"] = compute_security_score(data)
    return data


if __name__ == "__main__":
    print("Génération dashboard_security.json...")
    dashboard = build_dashboard()
    OUTPUT_FILE.write_text(
        json.dumps(dashboard, indent=4, ensure_ascii=False),
        encoding="utf-8",
    )
    score = dashboard.get("security_score", 0)
    print(f"Score sécurité global : {score}/100")
    print(f"Fichier : {OUTPUT_FILE}")
