# ============================================================
# ALFRED — src/security/policy_engine.py
# Bloc 20.13 — Zero Trust
#
# 📚 NOTION EXAM :
#   D51-2 — Capsule 4 : Moteur de politiques Zero Trust (Policy Engine)
#
# 🎯 UTILITÉ ALFRED :
#   Évalue les règles d'accès selon le rôle, la sensibilité de la
#   ressource et l'action demandée ; retourne ALLOW ou DENY.
#
# 🔐 BLOC SÉCURITÉ :
#   Zero Trust Policy Engine — règles dynamiques et contextuelles
# ============================================================

ROLES = ["OWNER", "ADMIN", "USER", "GUEST"]
SENSITIVITIES = ["PUBLIC", "INTERNAL", "CONFIDENTIAL", "CRITICAL"]
ACTIONS = ["READ", "WRITE", "DELETE_DATA", "EXPORT_DATA", "ADMIN_ACTION"]


def evaluate_policy(role: str, resource_sensitivity: str, action: str) -> str:
    """Évalue une politique d'accès simple."""
    if resource_sensitivity == "CRITICAL" and role not in ["OWNER", "ADMIN"]:
        return "DENY"

    if action in ["DELETE_DATA", "EXPORT_DATA"] and role != "OWNER":
        return "DENY"

    if action == "ADMIN_ACTION" and role not in ["OWNER", "ADMIN"]:
        return "DENY"

    if resource_sensitivity == "CONFIDENTIAL" and role == "GUEST":
        return "DENY"

    if action == "WRITE" and role == "GUEST":
        return "DENY"

    return "ALLOW"


def get_policy_matrix() -> dict:
    """Retourne la matrice complète des décisions d'accès (rôle × sensibilité × action)."""
    matrix = {}
    for role in ROLES:
        matrix[role] = {}
        for sensitivity in SENSITIVITIES:
            matrix[role][sensitivity] = {}
            for action in ACTIONS:
                matrix[role][sensitivity][action] = evaluate_policy(role, sensitivity, action)

    return {
        "roles": ROLES,
        "sensitivities": SENSITIVITIES,
        "actions": ACTIONS,
        "matrix": matrix,
        "rules_summary": [
            "CRITICAL → OWNER/ADMIN uniquement",
            "DELETE_DATA / EXPORT_DATA → OWNER uniquement",
            "ADMIN_ACTION → OWNER/ADMIN uniquement",
            "CONFIDENTIAL → interdit aux GUEST",
            "WRITE → interdit aux GUEST",
        ],
    }
