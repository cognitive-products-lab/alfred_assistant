"""
════════════════════════════════════════════════════════════
PROJECT      : ALFRED
BLOCK        : B20 (support ALFRED CPL — B10)
FUNCTION     : 20.21
FILE         : src/security/human_validation.py
ROLE         : File d'approbation humaine pour les décisions REVIEW

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-07-11
VERSION      : V1.0
STATUS       : ACTIVE

DESCRIPTION :
Transforme une décision "REVIEW" du Policy Engine (B20) en une demande de
validation traçable et actionnable, plutôt qu'un simple refus silencieux.
Une demande REVIEW est enregistrée dans un registre persistant
(data/security/pending_approvals.json), peut être approuvée ou rejetée par
un humain habilité, et chaque étape est tracée dans la piste d'audit (B20).

Cycle de vie d'une demande : pending -> approved | rejected.
════════════════════════════════════════════════════════════
"""
from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone
from typing import Any

from paths import PATHS
from src.security.audit_trail import write_audit_event
from src.security.security_logger import log_event

APPROVALS_FILE = PATHS.data_security / "pending_approvals.json"
APPROVALS_FILE.parent.mkdir(parents=True, exist_ok=True)

_VALID_STATUSES = {"pending", "approved", "rejected"}


def _load_approvals() -> list[dict[str, Any]]:
    if not APPROVALS_FILE.exists():
        return []
    try:
        data = json.loads(APPROVALS_FILE.read_text(encoding="utf-8"))
        return data if isinstance(data, list) else []
    except json.JSONDecodeError:
        return []


def _save_approvals(approvals: list[dict[str, Any]]) -> None:
    APPROVALS_FILE.write_text(
        json.dumps(approvals, indent=2, ensure_ascii=False), encoding="utf-8"
    )


def submit_for_review(
    user_id: str,
    role: str,
    action: str,
    resource: str,
    resource_sensitivity: str = "MEDIUM",
    payload: dict[str, Any] | None = None,
    request_id: str = "",
) -> dict[str, Any]:
    """
    Enregistre une demande en attente de validation humaine (décision REVIEW).

    Args:
        payload : contenu associé à la demande (ex. brouillon de livrable) —
            reste en mode brouillon tant que la demande n'est pas approuvée.

    Returns:
        La demande créée (avec son approval_id).
    """
    approval_id = str(uuid.uuid4())
    now = datetime.now(timezone.utc).isoformat()

    entry: dict[str, Any] = {
        "approval_id": approval_id,
        "status": "pending",
        "user_id": user_id,
        "role": role,
        "action": action,
        "resource": resource,
        "resource_sensitivity": resource_sensitivity,
        "payload": payload or {},
        "request_id": request_id,
        "submitted_at": now,
        "decided_at": None,
        "decided_by": None,
        "decision_note": "",
    }

    approvals = _load_approvals()
    approvals.append(entry)
    _save_approvals(approvals)

    write_audit_event(
        user_id=user_id, action=action, resource=resource,
        decision="REVIEW", request_id=request_id, role=role,
    )
    log_event(f"Demande de validation créée : {approval_id} ({action} sur {resource})", "WARNING")

    return entry


def get_request(approval_id: str) -> dict[str, Any] | None:
    """Retourne une demande par son identifiant, ou None si absente."""
    for entry in _load_approvals():
        if entry.get("approval_id") == approval_id:
            return entry
    return None


def list_pending(role: str | None = None) -> list[dict[str, Any]]:
    """Liste les demandes en attente, filtrées par rôle demandeur si précisé."""
    approvals = [a for a in _load_approvals() if a.get("status") == "pending"]
    if role:
        approvals = [a for a in approvals if a.get("role") == role]
    return approvals


def list_all(status: str | None = None) -> list[dict[str, Any]]:
    """Liste toutes les demandes, avec filtre optionnel par statut."""
    approvals = _load_approvals()
    if status is None:
        return approvals
    return [a for a in approvals if a.get("status") == status]


def _decide(
    approval_id: str,
    new_status: str,
    decided_by: str,
    note: str,
    audit_decision: str,
) -> dict[str, Any] | None:
    approvals = _load_approvals()

    target = None
    for entry in approvals:
        if entry.get("approval_id") == approval_id:
            target = entry
            break

    if target is None:
        return None

    if target.get("status") != "pending":
        # Décision déjà rendue — ne pas écraser, retourner l'état actuel (idempotent).
        return target

    target["status"] = new_status
    target["decided_at"] = datetime.now(timezone.utc).isoformat()
    target["decided_by"] = decided_by
    target["decision_note"] = note

    _save_approvals(approvals)

    write_audit_event(
        user_id=target.get("user_id", ""),
        action=target.get("action", ""),
        resource=target.get("resource", ""),
        decision=audit_decision,
        request_id=target.get("request_id", ""),
        role=decided_by,
    )
    log_event(f"Demande {approval_id} : {new_status} par {decided_by}", "INFO")

    return target


def approve_request(approval_id: str, approved_by: str, note: str = "") -> dict[str, Any] | None:
    """Approuve une demande en attente. Retourne None si la demande n'existe pas."""
    return _decide(approval_id, "approved", approved_by, note, audit_decision="ALLOW_AFTER_REVIEW")


def reject_request(approval_id: str, rejected_by: str, note: str = "") -> dict[str, Any] | None:
    """Rejette une demande en attente. Retourne None si la demande n'existe pas."""
    return _decide(approval_id, "rejected", rejected_by, note, audit_decision="DENY_AFTER_REVIEW")


def summarize_approvals() -> dict[str, Any]:
    """Résumé statistique des demandes de validation — pour le dashboard sécurité."""
    approvals = _load_approvals()
    by_status: dict[str, int] = {"pending": 0, "approved": 0, "rejected": 0}
    for a in approvals:
        status = a.get("status", "pending")
        by_status[status] = by_status.get(status, 0) + 1
    return {
        "total": len(approvals),
        "by_status": by_status,
    }
