from src.security.input_validator import sanitize_input
from src.security.threat_detector import detect_threat
from src.security.access_control import has_access
from src.security.device_registry import is_trusted_device
from src.security.policy_decision_point import decide_access
from src.security.policy_enforcement_point import enforce_decision, explain_decision
from src.security.audit_trail import write_audit_event
from src.security.security_logger import log_event
from src.security.mfa_manager import is_mfa_required, is_verified as mfa_is_verified

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
) -> dict:
    """
    Orchestrateur Zero Trust V1 :
    - valide l'input
    - détecte les menaces
    - vérifie l'appareil
    - vérifie les permissions
    - applique les politiques
    - trace la décision
    """
    cleaned_input = sanitize_input(user_input)

    if not cleaned_input:
        write_audit_event(user_id, action, resource, "DENY_INPUT")
        return {
            "authorized": False,
            "reason": "Input invalide",
        }

    threat = detect_threat(cleaned_input)

    if threat["is_threat"]:
        log_event(f"Menace détectée : {threat['reasons']}", "ERROR")
        write_audit_event(user_id, action, resource, "DENY_THREAT")
        return {
            "authorized": False,
            "reason": "Menace détectée",
            "details": threat,
        }

    if not is_trusted_device(device_id):
        write_audit_event(user_id, action, resource, "DENY_DEVICE")
        return {
            "authorized": False,
            "reason": "Appareil non reconnu ou non fiable",
        }

    # Étape MFA — requis pour OWNER et ADMIN
    if is_mfa_required(role):
        if not session_id or not mfa_is_verified(user_id, session_id):
            write_audit_event(user_id, action, resource, "DENY_MFA")
            return {
                "authorized": False,
                "reason": "MFA requis — vérification à deux facteurs nécessaire",
            }

    if not has_access(role, permission):
        write_audit_event(user_id, action, resource, "DENY_PERMISSION")
        return {
            "authorized": False,
            "reason": "Permission refusée",
        }

    decision = decide_access(role, resource_sensitivity, action)

    if not enforce_decision(decision):
        write_audit_event(user_id, action, resource, decision)
        return {
            "authorized": False,
            "reason": explain_decision(decision),
        }

    write_audit_event(user_id, action, resource, "ALLOW")

    return {
        "authorized": True,
        "cleaned_input": cleaned_input,
        "decision": "ALLOW",
    }
