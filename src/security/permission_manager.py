# ============================================================
# ALFRED — src/security/permission_manager.py
# Bloc 20.04 — Contrôle RBAC & permissions
#
# 📚 NOTION EXAM :
#   D41-2 — Capsule 2 : Matrice d'autorisations et contrôle d'accès RBAC
#
# 🎯 UTILITÉ ALFRED :
#   Mappe chaque rôle sur la liste de ses permissions autorisées
#   (READ_MEMORY, WRITE_MEMORY, DELETE_DATA, EXPORT_DATA, etc.).
#
# 🔐 BLOC SÉCURITÉ :
#   RBAC (Role-Based Access Control) — autorisation explicite par rôle
# ============================================================

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
