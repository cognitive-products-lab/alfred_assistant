# ============================================================
# ALFRED — src/security/compliance_manager.py
# Bloc 20.14 — Conformité & réglementation
#
# 📚 NOTION EXAM :
#   D43-2 — Capsule 7 : Conformité RGPD — droit à l'oubli (Art. 17)
#
# 🎯 UTILITÉ ALFRED :
#   Implémente le droit à l'effacement RGPD en supprimant les
#   fichiers de données utilisateur sensibles sur demande.
#
# 🔐 BLOC SÉCURITÉ :
#   Conformité réglementaire (RGPD) — minimisation et suppression des données personnelles
# ============================================================

from pathlib import Path
from src.security.security_logger import log_event

SENSITIVE_FILES = [
    "data/user_memory.json",
    "data/memory/episodic/dialogue_history.json",
    "logs/security/security.log",
]

def delete_user_data() -> None:
    """Supprime les données utilisateur sensibles connues."""
    for file_path in SENSITIVE_FILES:
        path = Path(file_path)

        if path.exists():
            path.unlink()
            log_event(f"Donnée supprimée : {file_path}", "WARNING")
