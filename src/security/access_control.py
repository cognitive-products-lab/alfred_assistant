# ============================================================
# ALFRED — src/security/access_control.py
# Bloc 20.04 — Contrôle RBAC & permissions
#
# 📚 NOTION EXAM :
#   D41-2 / D51-1 — Capsule 3 : Contrôle d'accès basé sur les rôles (RBAC)
#
# 🎯 UTILITÉ ALFRED :
#   Vérifie qu'un rôle dispose d'une permission avant toute action ;
#   rejette et trace chaque refus d'accès via le security logger.
#
# 🔐 BLOC SÉCURITÉ :
#   Zero Trust — vérification systématique (never trust, always verify)
# ============================================================

from src.security.permission_manager import get_permissions
from src.security.security_logger import log_event

def has_access(role: str, permission: str) -> bool:
    """Vérifie si un rôle dispose d'une permission."""
    allowed = permission in get_permissions(role)

    if not allowed:
        log_event(f"Accès refusé | rôle={role} | permission={permission}", "WARNING")

    return allowed
