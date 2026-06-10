"""
════════════════════════════════════════════════════════════
PROJECT      : ALFRED
BLOCK        : B20
FUNCTION     : 20.01
FILE         : access_control.py
ROLE         : Contrôle d'accès basé sur les rôles (RBAC)

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-05-23
UPDATED      : 2026-05-23
VERSION      : V1.0
STATUS       : ACTIVE

DESCRIPTION :
Vérifie si un rôle dispose d'une permission donnée. Couche RBAC du pipeline Zero Trust.
════════════════════════════════════════════════════════════
"""
from src.security.permission_manager import get_permissions
from src.security.security_logger import log_event

def has_access(role: str, permission: str) -> bool:
    """Vérifie si un rôle dispose d'une permission."""
    allowed = permission in get_permissions(role)

    if not allowed:
        log_event(f"Accès refusé | rôle={role} | permission={permission}", "WARNING")

    return allowed


def check_access(
    role: str = "", permission: str = "",
    user_id: str = "", request_id: str = "",
) -> dict:
    """Vérifie l'accès et retourne un dict structuré."""
    from src.security.role_manager import role_exists
    from src.security.permission_manager import all_permissions
    if not role or not role_exists(role.upper()):
        reason = "ROLE_UNKNOWN"
        allowed = False
    elif not permission:
        reason = "PERMISSION_EMPTY"
        allowed = False
    elif permission not in all_permissions():
        reason = "PERMISSION_UNKNOWN"
        allowed = False
    elif not has_access(role, permission):
        reason = "PERMISSION_DENIED"
        allowed = False
    else:
        reason = "ALLOW"
        allowed = True
    log_event(f"check_access | user={user_id} | role={role} | permission={permission} | result={reason}")
    return {"allowed": allowed, "role": role, "permission": permission, "user_id": user_id, "reason": reason}


def require_access(role: str, permission: str) -> bool:
    """Vérifie l'accès et lève PermissionError si refusé."""
    if not has_access(role, permission):
        raise PermissionError(f"Accès refusé : rôle '{role}' n'a pas la permission '{permission}'")
    return True
