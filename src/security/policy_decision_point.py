"""
════════════════════════════════════════════════════════════
PROJECT      : ALFRED
BLOCK        : B20
FUNCTION     : 20.13
FILE         : policy_decision_point.py
ROLE         : PDP — Point de décision d'accès (Zero Trust)

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-05-23
UPDATED      : 2026-05-23
VERSION      : V1.0
STATUS       : ACTIVE

DESCRIPTION :
Prend la décision d'accès en déléguant au Policy Engine. Interface PDP du pipeline Zero Trust.
════════════════════════════════════════════════════════════
"""
from src.security.policy_engine import evaluate_policy, explain_policy_decision

def decide_access(
    role: str, resource_sensitivity: str, action: str,
    risk_score: int = 0, context: dict | None = None
) -> str:
    """PDP : prend une décision d'accès (délègue au Policy Engine)."""
    return evaluate_policy(role, resource_sensitivity, action, risk_score=risk_score, context=context)


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
    """PDP verbose : retourne la décision avec justification et flag allowed."""
    decision = evaluate_policy(role, resource_sensitivity, action, risk_score=risk_score, context=context)
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
