from src.security.permission_manager import get_permissions
from src.security.security_logger import log_event

def has_access(role: str, permission: str) -> bool:
    """Vérifie si un rôle dispose d'une permission."""
    allowed = permission in get_permissions(role)

    if not allowed:
        log_event(f"Accès refusé | rôle={role} | permission={permission}", "WARNING")

    return allowed
