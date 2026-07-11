"""
════════════════════════════════════════════════════════════
PROJECT      : ALFRED
BLOCK        : B20
FUNCTION     : 20.00
FILE         : zero_trust_orchestrator.py
ROLE         : Orchestrateur Zero Trust — pipeline d'autorisation complet

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-05-23
UPDATED      : 2026-05-23
VERSION      : V1.0
STATUS       : ACTIVE

DESCRIPTION :
Pipeline Zero Trust : validation input → menaces → device → MFA → permissions → politique → audit.
════════════════════════════════════════════════════════════
"""
import uuid
from datetime import datetime, timezone
from src.security.input_validator import sanitize_input
from src.security.threat_detector import detect_threat
from src.security.access_control import has_access
from src.security.device_registry import is_trusted_device
from src.security.policy_decision_point import decide_access
from src.security.policy_enforcement_point import enforce_decision, explain_decision
from src.security.audit_trail import write_audit_event
from src.security.security_logger import log_event
from src.security.mfa_manager import is_mfa_required, is_verified as mfa_is_verified, evaluate_mfa
from src.security.session_manager import register_failed_attempt, reset_failed_attempts
from src.security.human_validation import submit_for_review

# Alias pour monkeypatch dans les tests
record_failed_attempt = register_failed_attempt

def authorize_request(
    user_id: str,
    role: str,
    permission: str,
    action: str,
    resource: str,
    resource_sensitivity: str,
    device_id: str,
    user_input: str,
    session_id: str | None = None,
    payload: dict | None = None,
    request_id: str = "",
) -> dict:
    """
    Orchestrateur Zero Trust V1 :
    - valide l'input
    - détecte les menaces
    - vérifie l'appareil
    - vérifie les permissions
    - applique les politiques
    - trace la décision

    Si la politique renvoie REVIEW (ex. action GENERATE_DELIVERABLE), la requête
    n'est ni autorisée ni refusée : elle est mise en file d'attente de validation
    humaine (src.security.human_validation) et l'approval_id est retourné.
    """
    _sanitized = sanitize_input(user_input)
    cleaned_input = _sanitized["cleaned_input"]

    if not _sanitized["valid"]:
        write_audit_event(user_id, action, resource, "DENY_INPUT")
        return {"authorized": False, "decision": "DENY_INPUT", "reason": "Input invalide"}

    threat = detect_threat(cleaned_input)

    if threat["is_threat"]:
        log_event(f"Menace détectée : {threat['reasons']}", "ERROR")
        write_audit_event(user_id, action, resource, "DENY_THREAT")
        return {"authorized": False, "decision": "DENY_THREAT", "reason": "Menace détectée", "details": threat}

    device_trusted = is_trusted_device(device_id)
    if not device_trusted:
        write_audit_event(user_id, action, resource, "DENY_DEVICE")
        return {"authorized": False, "decision": "DENY_DEVICE", "reason": "Appareil non reconnu"}

    # MFA TOTP par session — requis pour OWNER/ADMIN (et selon config globale)
    # is_mfa_required() vérifie _ALWAYS_MFA_ROLES puis la config security_settings.json
    if is_mfa_required(role):
        if not session_id or not mfa_is_verified(user_id, session_id):
            write_audit_event(user_id, action, resource, "DENY_MFA")
            return {"authorized": False, "decision": "DENY_MFA", "reason": "MFA requis"}

    if not has_access(role, permission):
        write_audit_event(user_id, action, resource, "DENY_PERMISSION")
        return {"authorized": False, "decision": "DENY_PERMISSION", "reason": "Permission refusée"}

    decision = decide_access(role, resource_sensitivity, action)

    if decision == "REVIEW":
        entry = submit_for_review(
            user_id=user_id,
            role=role,
            action=action,
            resource=resource,
            resource_sensitivity=resource_sensitivity,
            payload=payload,
            request_id=request_id,
        )
        return {
            "authorized": False,
            "decision": "REVIEW",
            "pending": True,
            "approval_id": entry["approval_id"],
            "reason": explain_decision(decision),
        }

    if not enforce_decision(decision):
        write_audit_event(user_id, action, resource, decision)
        return {"authorized": False, "decision": decision, "reason": explain_decision(decision)}

    write_audit_event(user_id, action, resource, "ALLOW")
    return {"authorized": True, "cleaned_input": cleaned_input, "decision": "ALLOW"}


def build_security_context(
    user_id: str,
    role: str,
    device_id: str,
    session_id: str | None = None,
    permission: str = "",
    action: str = "",
    resource: str = "",
    resource_sensitivity: str = "LOW",
    risk_score: int = 0,
) -> dict:
    """
    Construit un contexte de sécurité Zero Trust pour une requête entrante.
    """
    from src.security.device_registry import is_trusted_device
    from src.security.permission_manager import get_permissions
    from src.security.mfa_manager import is_mfa_required, is_verified as mfa_is_verified

    trusted = is_trusted_device(device_id)
    mfa_required = is_mfa_required(role)
    mfa_verified = mfa_is_verified(user_id, session_id) if session_id else False

    return {
        "user_id": user_id,
        "role": role,
        "device_id": device_id,
        "permission": permission,
        "action": action,
        "resource": resource,
        "resource_sensitivity": resource_sensitivity,
        "risk_score": risk_score,
        "device_trusted": trusted,
        "mfa_required": mfa_required,
        "mfa_verified": mfa_verified,
        "permissions": get_permissions(role),
        "session_id": session_id,
        "request_id": str(uuid.uuid4()),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


def quick_authorize_owner_local(user_input: str) -> dict:
    """
    Raccourci : autorise une requête du propriétaire depuis l'appareil local.
    Crée une session locale et marque le MFA comme vérifié (appareil de confiance).
    """
    from src.security.session_manager import create_session
    from src.security.mfa_manager import mark_verified

    user_id  = "celine"
    role     = "OWNER"
    device   = "local_pc"

    # Session locale + MFA vérifié via appareil de confiance
    session_id = create_session(user_id=user_id, device_id=device, role=role)
    mark_verified(user_id, session_id)

    return authorize_request(
        user_id=user_id,
        role=role,
        permission="RUN_AI_MODULE",
        action="chat",
        resource="alfred_assistant",
        resource_sensitivity="LOW",
        device_id=device,
        user_input=user_input,
        session_id=session_id,
    )
