"""
════════════════════════════════════════════════════════════
PROJECT      : ALFRED
BLOCK        : B20
FUNCTION     : 20.01
FILE         : role_manager.py
ROLE         : Registre et normalisation des rôles utilisateur (RBAC)

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-05-23
UPDATED      : 2026-05-23
VERSION      : V1.0
STATUS       : ACTIVE

DESCRIPTION :
Définit les rôles disponibles, vérifie leur existence et normalise les entrées.
════════════════════════════════════════════════════════════
"""
ROLES = {
    "OWNER": "Propriétaire — contrôle complet du système",
    "ADMIN": "Administrateur technique — accès privilégié",
    "USER": "Utilisateur standard — accès limité",
    "GUEST": "Invité restreint — accès minimal",
    "SERVICE": "Service interne — accès fonctionnel",
    "AI_MODULE": "Module IA contrôlé — accès restreint",
    "EMERGENCY": "Accès urgence encadré — alertes uniquement",
}

def role_exists(role: str) -> bool:
    """Vérifie si un rôle existe."""
    return role in ROLES

def list_roles() -> dict:
    """Retourne la liste des rôles disponibles."""
    return ROLES.copy()


def normalize_role(role: str) -> str:
    """Normalise un rôle en majuscules. Retourne 'GUEST' si le rôle est inconnu."""
    normalized = role.strip().upper()
    return normalized if normalized in ROLES else "GUEST"


def get_role_description(role: str) -> str:
    """Retourne la description d'un rôle ou 'Rôle inconnu.' si absent."""
    normalized = role.strip().upper()
    return ROLES.get(normalized, "Rôle inconnu.")


ROLE_LEVELS = {
    "OWNER": 100, "ADMIN": 80, "USER": 50,
    "SERVICE": 40, "AI_MODULE": 30, "EMERGENCY": 20, "GUEST": 0,
}


def get_role_level(role: str) -> int:
    """Retourne le niveau numérique d'un rôle (100 = max, 0 = GUEST)."""
    return ROLE_LEVELS.get(normalize_role(role), 0)


def is_role_at_least(role: str, min_role: str) -> bool:
    """Vérifie si role a un niveau >= min_role."""
    return get_role_level(role) >= get_role_level(min_role)


def list_role_details() -> list[dict]:
    """Retourne la liste des rôles avec description et niveau."""
    return [
        {"role": r, "description": d, "level": ROLE_LEVELS.get(r, 0)}
        for r, d in ROLES.items()
    ]
