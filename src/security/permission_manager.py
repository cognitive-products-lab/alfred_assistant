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
}

def get_permissions(role: str) -> list[str]:
    """Retourne les permissions associées à un rôle."""
    return PERMISSIONS.get(role, [])

def list_permissions() -> dict:
    """Retourne toutes les permissions par rôle."""
    return PERMISSIONS.copy()
