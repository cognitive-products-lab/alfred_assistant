# ============================================================
# ALFRED — src/security/backup_security.py
# Bloc 20.12 — Sauvegarde & reprise
#
# 📚 NOTION EXAM :
#   D53-1 — Capsule 8 : Sauvegarde et continuité des données sensibles
#
# 🎯 UTILITÉ ALFRED :
#   Crée des sauvegardes horodatées des fichiers critiques dans
#   un répertoire dédié backup/security/.
#
# 🔐 BLOC SÉCURITÉ :
#   Résilience et disponibilité (RTO/RPO) — protection contre la perte de données
# ============================================================

import shutil
from datetime import datetime
from pathlib import Path
from src.security.security_logger import log_event

BACKUP_DIR = Path("backup/security")
BACKUP_DIR.mkdir(parents=True, exist_ok=True)

def secure_backup(source_path: str) -> str:
    """Crée une sauvegarde locale d'un fichier sensible."""
    source = Path(source_path)

    if not source.exists():
        raise FileNotFoundError(f"Fichier introuvable : {source_path}")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    destination = BACKUP_DIR / f"{source.name}.{timestamp}.bak"

    shutil.copy2(source, destination)
    log_event(f"Backup créé : {destination}")

    return str(destination)
