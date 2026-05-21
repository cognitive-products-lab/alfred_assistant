# ============================================================
# ALFRED — src/security/policy_decision_point.py
# Bloc 20.13 — Zero Trust
#
# 📚 NOTION EXAM :
#   D51-2 — Capsule 4 : PDP — Policy Decision Point (architecture XACML)
#
# 🎯 UTILITÉ ALFRED :
#   Point centralisé qui délègue au policy engine et retourne
#   la décision d'accès (ALLOW/DENY) à l'orchestrateur.
#
# 🔐 BLOC SÉCURITÉ :
#   Architecture Zero Trust — séparation décision (PDP) / application (PEP)
# ============================================================

from src.security.policy_engine import evaluate_policy

def decide_access(role: str, resource_sensitivity: str, action: str) -> str:
    """PDP : prend une décision d'accès."""
    return evaluate_policy(role, resource_sensitivity, action)
