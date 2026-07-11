"""
════════════════════════════════════════════════════════════
PROJECT      : ALFRED
BLOCK        : B20
FUNCTION     : 20.01
FILE         : permission_manager.py
ROLE         : Table des permissions par rôle (RBAC)

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-05-23
UPDATED      : 2026-05-23
VERSION      : V1.0
STATUS       : ACTIVE

DESCRIPTION :
Définit la matrice de permissions OWNER/ADMIN/USER/GUEST/SERVICE/AI_MODULE/EMERGENCY.
════════════════════════════════════════════════════════════
"""
PERMISSIONS = {
    "OWNER": [
        "READ_MEMORY",
        "WRITE_MEMORY",
        "DELETE_DATA",
        "EXPORT_DATA",
        "ACCESS_SECURITY_LOGS",
        "CONTROL_DEVICE",
        "RUN_AI_MODULE",
    ],
    "ADMIN": [
        "READ_MEMORY",
        "WRITE_MEMORY",
        "ACCESS_SECURITY_LOGS",
        "CONTROL_DEVICE",
    ],
    "USER": [
        "READ_MEMORY",
        "WRITE_MEMORY",
        "RUN_AI_MODULE",
    ],
    "GUEST": [
        "RUN_AI_MODULE",
    ],
    "SERVICE": [
        "RUN_AI_MODULE",
    ],
    "AI_MODULE": [
        "RUN_AI_MODULE",
    ],
    "EMERGENCY": [
        "SEND_ALERT",
        "READ_EMERGENCY_CONTEXT",
    ],
    # Rôles métier ALFRED CPL (filtrage de connaissances : src/security/cpl_role_access.py)
    "CHEF_DE_PROJET": [
        "READ_MEMORY",
        "RUN_AI_MODULE",
    ],
    "RH": [
        "READ_MEMORY",
        "RUN_AI_MODULE",
    ],
}

def get_permissions(role: str) -> list[str]:
    """Retourne les permissions associées à un rôle."""
    return PERMISSIONS.get(role, [])

def list_permissions() -> dict:
    """Retourne toutes les permissions par rôle."""
    return PERMISSIONS.copy()


def all_permissions() -> list[str]:
    """Retourne la liste dédupliquée de toutes les permissions définies."""
    seen: set[str] = set()
    result: list[str] = []
    for perms in PERMISSIONS.values():
        for p in perms:
            if p not in seen:
                seen.add(p)
                result.append(p)
    return result

def summarize_permissions() -> dict:
    """Synthèse des permissions pour le dashboard sécurité."""
    permissions = list_permissions()
    unique = all_permissions()
    return {
        "roles_count": len(permissions),
        "permissions_total": sum(len(v) for v in permissions.values()),
        "unique_permissions_count": len(unique),
        "matrix": permissions,
    }


def permission_exists(permission: str) -> bool:
    """Retourne True si la permission est définie dans au moins un rôle."""
    return permission in all_permissions()


def role_has_permission(role: str, permission: str) -> bool:
    """Alias de has_access sans dépendance circulaire (insensible à la casse)."""
    return normalize_permission(permission) in get_permissions(normalize_role(role))


def add_permission_to_role(role: str, permission: str) -> bool:
    """Ajoute une permission à un rôle existant en mémoire. Retourne True si ajouté."""
    if role not in PERMISSIONS:
        return False
    if permission not in PERMISSIONS[role]:
        PERMISSIONS[role].append(permission)
    return True


def normalize_permission(permission: str) -> str:
    """Normalise une permission en majuscules."""
    return permission.strip().upper()


def normalize_role(role: str) -> str:
    """Normalise un rôle en majuscules. Retourne GUEST si vide ou inconnu."""
    normalized = role.strip().upper()
    return normalized if normalized in PERMISSIONS else "GUEST"