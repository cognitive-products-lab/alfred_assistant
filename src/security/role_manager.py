# ============================================================
# ALFRED — src/security/role_manager.py
# Bloc 20.02 — Gestion des identités & accès
#
# 📚 NOTION EXAM :
#   D41-2 — Capsule 2 : Gestion des identités et des rôles (IAM)
#
# 🎯 UTILITÉ ALFRED :
#   Définit le référentiel des rôles ALFRED : OWNER, ADMIN, USER,
#   GUEST, SERVICE, AI_MODULE, EMERGENCY — source de vérité unique.
#
# 🔐 BLOC SÉCURITÉ :
#   Principe du moindre privilège — chaque rôle n'accède qu'au strict nécessaire
# ============================================================

ROLES = {
    "OWNER": "Utilisatrice principale",
    "ADMIN": "Administrateur technique",
    "USER": "Utilisateur standard",
    "GUEST": "Invité limité",
    "SERVICE": "Service interne",
    "AI_MODULE": "Module IA contrôlé",
    "EMERGENCY": "Accès urgence encadré",
}

def role_exists(role: str) -> bool:
    """Vérifie si un rôle existe."""
    return role in ROLES

def list_roles() -> dict:
    """Retourne la liste des rôles disponibles."""
    return ROLES.copy()
