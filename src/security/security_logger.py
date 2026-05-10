# ============================================================
# ALFRED â€” src/security/security_logger.py
# Bloc 20.07 â€” Logs securite
# Logger dedie a tous les evenements de securite
# ============================================================

import logging
from pathlib import Path

# â”€â”€ Configuration du logger â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
_LOG_DIR  = Path("logs/security")
_LOG_DIR.mkdir(parents=True, exist_ok=True)
_LOG_FILE = _LOG_DIR / "security.log"

logging.basicConfig(
    filename=str(_LOG_FILE),
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    encoding="utf-8",
)

_logger = logging.getLogger("alfred.security")


def log_event(event: str, level: str = "INFO") -> None:
    """
    Enregistre un evenement de securite dans le fichier de log.

    Args:
        event : Description de l'evenement
        level : INFO | WARNING | ERROR | CRITICAL
    """
    level = level.upper()
    if level == "CRITICAL":
        _logger.critical(event)
    elif level == "ERROR":
        _logger.error(event)
    elif level == "WARNING":
        _logger.warning(event)
    else:
        _logger.info(event)


def log_access(user_id: str, action: str, resource: str, result: str) -> None:
    """Log structure pour les tentatives d'acces."""
    msg = f"ACCESS | user={user_id} | action={action} | resource={resource} | result={result}"
    log_event(msg, "INFO" if result == "ALLOW" else "WARNING")


def log_auth(user_id: str, method: str, success: bool) -> None:
    """Log structure pour les tentatives d'authentification."""
    status = "SUCCESS" if success else "FAILURE"
    msg = f"AUTH | user={user_id} | method={method} | status={status}"
    log_event(msg, "INFO" if success else "WARNING")
