"""
════════════════════════════════════════════════════════════
PROJECT      : ALFRED
BLOCK        : B20
FUNCTION     : 20.13
FILE         : policy_decision_point.py
ROLE         : PDP — Point de décision d'accès (Zero Trust)

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-05-23
UPDATED      : 2026-07-13
VERSION      : V1.1
STATUS       : ACTIVE

DESCRIPTION :
Prend la décision d'accès en déléguant au Policy Engine. Interface PDP du pipeline Zero Trust.
Journalise chaque décision dans data/security/access_decisions_history.json (point C4-C du
plan d'action du 13/07/2026 — ce fichier était attendu par le manifest mais jamais alimenté
par aucun module).
════════════════════════════════════════════════════════════
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from src.security.policy_engine import evaluate_policy, explain_policy_decision

try:
    from paths import PATHS
    _HISTORY_FILE = PATHS.data_security / "access_decisions_history.json"
except ImportError:
    _HISTORY_FILE = Path("data/security/access_decisions_history.json")

_MAX_HISTORY_ENTRIES = 5000  # évite une croissance illimitée du fichier (local-first, pas de rotation externe)


def _load_history() -> list:
    if not _HISTORY_FILE.exists():
        return []
    try:
        data = json.loads(_HISTORY_FILE.read_text(encoding="utf-8"))
        return data if isinstance(data, list) else []
    except json.JSONDecodeError:
        return []


def _log_decision(role: str, resource_sensitivity: str, action: str, risk_score: int, decision: str) -> None:
    """Journalise une décision d'accès Zero Trust (append-only, best-effort)."""
    try:
        history = _load_history()
        history.append({
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "role": role,
            "resource_sensitivity": resource_sensitivity,
            "action": action,
            "risk_score": risk_score,
            "decision": decision,
        })
        if len(history) > _MAX_HISTORY_ENTRIES:
            history = history[-_MAX_HISTORY_ENTRIES:]
        _HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)
        _HISTORY_FILE.write_text(json.dumps(history, indent=2, ensure_ascii=False), encoding="utf-8")
    except OSError:
        pass  # journalisation best-effort — ne doit jamais bloquer une décision d'accès


def decide_access(
    role: str, resource_sensitivity: str, action: str,
    risk_score: int = 0, context: dict | None = None
) -> str:
    """PDP : prend une décision d'accès (délègue au Policy Engine), journalisée."""
    decision = evaluate_policy(role, resource_sensitivity, action, risk_score=risk_score, context=context)
    _log_decision(role, resource_sensitivity, action, risk_score, decision)
    return decision


def is_access_allowed(
    role: str, resource_sensitivity: str, action: str,
    risk_score: int = 0
) -> bool:
    """Version booléenne — True si ALLOW."""
    return decide_access(role, resource_sensitivity, action, risk_score=risk_score) == "ALLOW"


def decide_access_verbose(
    role: str, resource_sensitivity: str, action: str,
    risk_score: int = 0, context: dict | None = None
) -> dict:
    """PDP verbose : retourne la décision avec justification et flag allowed (journalisée)."""
    decision = decide_access(role, resource_sensitivity, action, risk_score=risk_score, context=context)
    return {
        "decision": decision,
        "allowed": decision == "ALLOW",
        "role": role,
        "resource_sensitivity": resource_sensitivity,
        "action": action,
        "risk_score": risk_score,
        "reason": explain_policy_decision(decision),
        "explanation": explain_policy_decision(decision),
    }
