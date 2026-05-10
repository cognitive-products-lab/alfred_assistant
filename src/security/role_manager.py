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
