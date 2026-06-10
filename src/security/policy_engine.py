"""
════════════════════════════════════════════════════════════
PROJECT      : ALFRED
BLOCK        : B20
FUNCTION     : 20.13
FILE         : policy_engine.py
ROLE         : Moteur d'évaluation des politiques d'accès

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-05-23
UPDATED      : 2026-05-31
VERSION      : V1.1
STATUS       : ACTIVE

DESCRIPTION :
Évalue les règles d'accès Zero Trust selon le rôle, la sensibilité
de la ressource, l'action, le score de risque et le contexte de session.
Codes de décision : ALLOW | DENY_POLICY | DENY_PERMISSION | DENY_RISK | REVIEW
════════════════════════════════════════════════════════════
"""
from src.security.permission_manager import get_permissions

# Niveaux de sensibilité des ressources (ordonnés)
_SENSITIVITY_LEVEL = {"LOW": 0, "MEDIUM": 1, "HIGH": 2, "CRITICAL": 3}

# Accès maximal autorisé par rôle (sensibilité max inclusif)
_ROLE_MAX_SENSITIVITY = {
    "OWNER":     3,  # CRITICAL
    "ADMIN":     3,  # CRITICAL
    "USER":      1,  # MEDIUM
    "SERVICE":   1,  # MEDIUM
    "AI_MODULE": 1,  # MEDIUM
    "EMERGENCY": 0,  # LOW
    "GUEST":     0,  # LOW
}

# Actions restreintes : {action → liste des rôles autorisés}
_RESTRICTED_ACTIONS = {
    "DELETE_DATA":  ["OWNER"],
    "EXPORT_DATA":  ["OWNER"],
    "SEND_ALERT":   ["OWNER", "ADMIN", "EMERGENCY"],
}


def evaluate_policy(
    role: str,
    resource_sensitivity: str,
    action: str,
    risk_score: int = 0,
    context: dict | None = None,
) -> str:
    """
    Évalue une politique d'accès Zero Trust.

    Returns:
        ALLOW | DENY_POLICY | DENY_PERMISSION | DENY_RISK | REVIEW
    """
    role = role.upper()
    resource_sensitivity = resource_sensitivity.upper()

    # 1. Risque élevé → rejet immédiat
    if risk_score >= 80:
        return "DENY_RISK"

    # 2. Risque moyen + ressource sensible → révision
    if risk_score >= 50 and _SENSITIVITY_LEVEL.get(resource_sensitivity, 0) >= 2:
        return "REVIEW"

    # 3. Contexte de session à risque → révision
    if context and context.get("session_risk") in ("HIGH", "CRITICAL"):
        return "REVIEW"

    # 4. Sensibilité dépassant le niveau max du rôle
    max_level = _ROLE_MAX_SENSITIVITY.get(role, 0)
    resource_level = _SENSITIVITY_LEVEL.get(resource_sensitivity, 0)
    if resource_level > max_level:
        # CRITICAL → DENY_POLICY (politique explicite), MEDIUM/HIGH → DENY_PERMISSION
        if resource_level >= 3:
            return "DENY_POLICY"
        return "DENY_PERMISSION"

    # 5. Action restreinte non autorisée pour ce rôle → DENY_PERMISSION
    action_upper = action.upper()
    if action_upper in _RESTRICTED_ACTIONS:
        if role not in _RESTRICTED_ACTIONS[action_upper]:
            return "DENY_PERMISSION"

    return "ALLOW"


def explain_policy_decision(decision: str, **kwargs) -> str:
    """Retourne une explication textuelle d'un code de décision."""
    explanations = {
        "ALLOW":            "Accès autorisé — toutes les politiques validées.",
        "DENY_POLICY":      "Accès refusé — sensibilité de la ressource trop élevée pour ce rôle.",
        "DENY_PERMISSION":  "Accès refusé — permission ou action non accordée à ce rôle.",
        "DENY_RISK":        "Accès refusé — score de risque trop élevé.",
        "REVIEW":           "Accès en révision — risque modéré sur ressource sensible.",
    }
    return explanations.get(decision, f"Décision inconnue : {decision}")


def get_policy_matrix() -> dict:
    """Retourne la matrice de politiques Zero Trust pour le dashboard."""
    return {
        "role_levels": _ROLE_MAX_SENSITIVITY,
        "resource_sensitivity_levels": _SENSITIVITY_LEVEL,
        "action_requirements": _RESTRICTED_ACTIONS,
    }
