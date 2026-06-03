# ============================================================
# ALFRED — src/security/quarantine_service.py
# Bloc 20.11 — Réponse à incident
#
# 📚 NOTION EXAM :
#   D42-3 — Capsule 10 : Containment et isolation des composants suspects
#
# 🎯 UTILITÉ ALFRED :
#   Met en quarantaine les modules IA ou composants suspects,
#   trace l'isolation et permet la réhabilitation contrôlée.
#
# 🔐 BLOC SÉCURITÉ :
#   Containment Zero Trust — isolation des composants pour stopper la propagation
# ============================================================

from src.security.security_logger import log_event

QUARANTINED_MODULES: set[str] = set()

def quarantine_module(module_name: str, reason: str) -> None:
    """Met un module en quarantaine."""
    QUARANTINED_MODULES.add(module_name)
    log_event(f"Module mis en quarantaine : {module_name} | raison={reason}", "CRITICAL")

def is_quarantined(module_name: str) -> bool:
    """Vérifie si un module est en quarantaine."""
    return module_name in QUARANTINED_MODULES

def release_module(module_name: str) -> None:
    """Sort un module de quarantaine."""
    QUARANTINED_MODULES.discard(module_name)
    log_event(f"Module sorti de quarantaine : {module_name}")


def summarize_quarantine() -> dict:
    """Retourne un résumé anonymisé de la quarantaine — pour le dashboard public."""
    active_total = len(QUARANTINED_MODULES)
    return {
        "active_total":    active_total,
        "modules_list":    sorted(QUARANTINED_MODULES),   # noms techniques OK (pas de user_id)
        "status":          "CLEAN" if active_total == 0 else "ACTIVE",
    }
