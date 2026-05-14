"""
PROJECT      : ALFRED
BLOCK        : B20
FUNCTION     : XX.XX
FILE         : zero_trust_orchestrator.py
ROLE         : Orchestrateur Zero Trust — chaîne complète autorisation avec MFA

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-05-10
P26-05-12
VERSION      : V1.0
STATUS       : STABLE

DESCRIPTION :
Orchestre la chaîne complète Zero Trust : input → threat → device → MFA → permission → PDP → PEP → audit.
"""

from datetime import datetime, timezone
from typing import Dict, Any
from uuid import uuid4

from src.security.input_validator import sanitize_input
from src.security.threat_detector import detect_threat
from src.security.access_control import has_access
from src.security.device_registry import is_trusted_device, record_failed_attempt
from src.security.mfa_manager import evaluate_mfa
from src.security.policy_decision_point import decide_access
from src.security.policy_enforcement_point import enforce_decision, explain_decision
from src.security.audit_trail import write_audit_event
from src.security.security_logger import log_event

# Seuil MFA par rôle — local-first ALFRED V1
_MFA_THRESHOLD_BY_ROLE: Dict[str, int] = {
    "OWNER":      2,   # device fiable suffit
    "ADMIN":      3,   # device + 1 facteur
    "USER":       3,
    "SERVICE":    1,
    "AI_MODULE":  1,
    "EMERGENCY":  1,
    "GUEST":      5,   # tous les facteurs requis
}


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def build_security_context(
    user_id: str,
    role: str,
    permission: str,
    action: str,
    resource: str,
    resource_sensitivity: str,
    device_id: str,
) -> Dict[str, Any]:
    """Construit le contexte sécurité standard."""
    return {
        "request_id": str(uuid4()),
        "timestamp": _now(),
        "user_id": user_id or "unknown_user",
        "role": role or "GUEST",
        "permission": permission or "",
        "action": action or "unknown_action",
        "resource": resource or "unknown_resource",
        "resource_sensitivity": resource_sensitivity or "LOW",
        "device_id": device_id or "unknown_device",
        "risk_score": 0,
        "security_level": "ZERO_TRUST_V1",
    }


def _deny(
    context: Dict[str, Any],
    decision: str,
    reason: str,
    details: Dict[str, Any] | None = None,
) -> Dict[str, Any]:
    write_audit_event(
        context.get("user_id", "unknown_user"),
        context.get("action", "unknown_action"),
        context.get("resource", "unknown_resource"),
        decision,
    )
    log_event(
        f"ZeroTrust DENY request_id={context.get('request_id')} "
        f"user={context.get('user_id')} reason={reason}",
        "WARNING",
    )
    return {
        "authorized": False,
        "decision": decision,
        "reason": reason,
        "explanation": explain_decision(decision),
        "context": context,
        "details": details or {},
    }


def _allow(context: Dict[str, Any], cleaned_input: str) -> Dict[str, Any]:
    write_audit_event(
        context.get("user_id", "unknown_user"),
        context.get("action", "unknown_action"),
        context.get("resource", "unknown_resource"),
        "ALLOW",
    )
    log_event(
        f"ZeroTrust ALLOW request_id={context.get('request_id')} "
        f"user={context.get('user_id')} action={context.get('action')}"
    )
    return {
        "authorized": True,
        "decision": "ALLOW",
        "reason": "Accès autorisé",
        "cleaned_input": cleaned_input,
        "context": context,
    }


def authorize_request(
    user_id: str,
    role: str,
    permission: str,
    action: str,
    resource: str,
    resource_sensitivity: str,
    device_id: str,
    user_input: str,
) -> Dict[str, Any]:
    """
    Autorise ou refuse une requête selon la chaîne Zero Trust.

    Étapes : input → threat → device → MFA → permission → PDP → PEP → audit.
    """
    context = build_security_context(
        user_id=user_id,
        role=role,
        permission=permission,
        action=action,
        resource=resource,
        resource_sensitivity=resource_sensitivity,
        device_id=device_id,
    )

    validation = sanitize_input(user_input)
    cleaned_input = validation["cleaned_input"]

    if not validation["valid"]:
        context["risk_score"] += validation.get("risk_score", 20)
        return _deny(
            context=context,
            decision="DENY_INPUT",
            reason="Input invalide ou dangereux",
            details={
                "validation_reasons": validation.get("reasons", []),
                "validation_risk_score": validation.get("risk_score", 0),
            },
        )

    threat = detect_threat(cleaned_input)

    if threat.get("is_threat", False):
        context["risk_score"] += 60
        log_event(
            f"Menace détectée request_id={context['request_id']} "
            f"reasons={threat.get('reasons')}",
            "ERROR",
        )
        return _deny(context=context, decision="DENY_THREAT", reason="Menace détectée dans la requête", details=threat)

    if not is_trusted_device(device_id):
        context["risk_score"] += 40
        record_failed_attempt(device_id)
        return _deny(context=context, decision="DENY_DEVICE", reason="Appareil non reconnu ou non fiable")

    # Étape MFA — correctif P2 : evaluate_mfa() intégré avec seuil par rôle
    mfa_threshold = _MFA_THRESHOLD_BY_ROLE.get(role.upper(), 3)
    mfa_result = evaluate_mfa(
        device=True,
        threshold=mfa_threshold,
        user_id=user_id,
        request_id=context["request_id"],
    )

    if not mfa_result["authenticated"]:
        context["risk_score"] += 25
        return _deny(
            context=context,
            decision="DENY_MFA",
            reason="Authentification multi-facteurs insuffisante",
            details=mfa_result,
        )

    if not has_access(role, permission):
        context["risk_score"] += 30
        return _deny(context=context, decision="DENY_PERMISSION", reason="Permission insuffisante")

    decision = decide_access(role=role, resource_sensitivity=resource_sensitivity, action=action)

    enforcement_context = {
        "request_id": context["request_id"],
        "user_id": context["user_id"],
        "action": context["action"],
        "resource": context["resource"],
        "device_id": context["device_id"],
        "risk_score": context["risk_score"],
    }

    if not enforce_decision(decision, context=enforcement_context):
        return _deny(context=context, decision=decision, reason=explain_decision(decision))

    return _allow(context=context, cleaned_input=cleaned_input)


def quick_authorize_owner_local(user_input: str) -> Dict[str, Any]:
    """Autorisation rapide pour usage local propriétaire (tests ALFRED V1)."""
    return authorize_request(
        user_id="celine",
        role="OWNER",
        permission="RUN_AI_MODULE",
        action="chat",
        resource="alfred_core",
        resource_sensitivity="LOW",
        device_id="local_pc",
        user_input=user_input,
    )
