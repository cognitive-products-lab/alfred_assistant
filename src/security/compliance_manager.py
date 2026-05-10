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
