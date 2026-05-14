"""
PROJECT      : ALFRED
BLOCK        : B20
FILE         : security_logger.py
ROLE         : Logging sécurité centralisé — fichier + console

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-05-10
VERSION      : V1.0
STATUS       : STABLE

DESCRIPTION :
Logger sécurité unique. Écrit dans logs/security/security.log et console selon le niveau.
"""

import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# Chemin absolu depuis la racine du module — indépendant du CWD
_MODULE_ROOT = Path(__file__).resolve().parent.parent.parent
LOG_DIR = _MODULE_ROOT / "logs" / "security"
LOG_FILE = LOG_DIR / "security.log"

_logger = logging.getLogger("alfred.security")
_logger.setLevel(logging.INFO)
_logger.propagate = False


class _SilentFileHandler(logging.FileHandler):
    """FileHandler qui absorbe silencieusement les erreurs d'écriture (fichier verrouillé)."""
    def handleError(self, record: logging.LogRecord) -> None:
        pass


def _ensure_handler() -> None:
    """Configure le handler fichier une seule fois."""
    if _logger.handlers:
        return
    try:
        LOG_DIR.mkdir(parents=True, exist_ok=True)
        handler = _SilentFileHandler(LOG_FILE, encoding="utf-8", delay=True)
        handler.setLevel(logging.INFO)
        handler.setFormatter(logging.Formatter(
            "%(asctime)s | %(levelname)-8s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        ))
        _logger.addHandler(handler)
    except Exception:
        _logger.addHandler(logging.NullHandler())


_ensure_handler()


def _normalize_level(level: str) -> str:
    clean = level.upper() if level else "INFO"
    if clean not in {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}:
        return "INFO"
    return clean


def log_event(event: str, level: str = "INFO") -> None:
    """
    Enregistre un événement de sécurité.

    Args:
        event: description de l'événement.
        level: DEBUG | INFO | WARNING | ERROR | CRITICAL.
    """
    clean_level = _normalize_level(level)
    message = str(event)

    if clean_level == "CRITICAL":
        _logger.critical(message)
    elif clean_level == "ERROR":
        _logger.error(message)
    elif clean_level == "WARNING":
        _logger.warning(message)
    elif clean_level == "DEBUG":
        _logger.debug(message)
    else:
        _logger.info(message)


def log_structured_event(event_type: str, level: str = "INFO", **fields: Any) -> None:
    """Log structuré sous forme clé=valeur."""
    parts = [event_type.upper()]
    parts.append(f"timestamp={datetime.now(timezone.utc).isoformat()}")
    for key, value in fields.items():
        parts.append(f"{key}={value}")
    log_event(" | ".join(parts), level)


def log_access(
    user_id: str,
    action: str,
    resource: str,
    result: str,
    request_id: str = "",
    device_id: str = "",
    risk_score: int = 0,
) -> None:
    """Log structuré pour les tentatives d'accès."""
    result_upper = result.upper() if result else "UNKNOWN"
    log_structured_event(
        "ACCESS",
        "INFO" if result_upper == "ALLOW" else "WARNING",
        request_id=request_id,
        user_id=user_id,
        device_id=device_id,
        action=action,
        resource=resource,
        result=result_upper,
        risk_score=risk_score,
    )


def log_auth(
    user_id: str,
    method: str,
    success: bool,
    request_id: str = "",
    device_id: str = "",
) -> None:
    """Log structuré pour les tentatives d'authentification."""
    status = "SUCCESS" if success else "FAILURE"
    log_structured_event(
        "AUTH",
        "INFO" if success else "WARNING",
        request_id=request_id,
        user_id=user_id,
        device_id=device_id,
        method=method,
        status=status,
    )


def log_incident(
    incident_id: str,
    level: str,
    description: str,
    source: str = "unknown",
) -> None:
    """Log structuré pour les incidents de sécurité."""
    log_structured_event(
        "INCIDENT",
        level,
        incident_id=incident_id,
        source=source,
        description=description,
    )


def get_log_file_path() -> Path:
    """Retourne le chemin du fichier de log sécurité."""
    return LOG_FILE


def read_security_log_tail(lines: int = 50) -> list[str]:
    """Lit les dernières lignes du fichier de log sécurité."""
    if not LOG_FILE.exists():
        return []
    content = LOG_FILE.read_text(encoding="utf-8").splitlines()
    return content[-lines:]
