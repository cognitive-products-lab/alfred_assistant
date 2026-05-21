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

def evaluate_policy(role: str, resource_sensitivity: str, action: str) -> str:
    """Évalue une politique d'accès simple."""
    if resource_sensitivity == "CRITICAL" and role not in ["OWNER", "ADMIN"]:
        return "DENY"

    if action in ["DELETE_DATA", "EXPORT_DATA"] and role != "OWNER":
        return "DENY"

    return "ALLOW"
