"""
════════════════════════════════════════════════════════════
PROJECT      : ALFRED
BLOCK        : B20
FUNCTION     : 20.07
FILE         : security_logger.py
ROLE         : Logger dédié aux événements de sécurité

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-05-23
UPDATED      : 2026-05-23
VERSION      : V1.0
STATUS       : ACTIVE

DESCRIPTION :
Enregistre tous les événements de sécurité dans logs/security/security.log.
════════════════════════════════════════════════════════════
"""
# ============================================================
# ALFRED â€" src/security/security_logger.py
# Bloc 20.07 â€" Logs securite
# Logger dedie a tous les evenements de securite
# ============================================================

import logging
from pathlib import Path

# ── Configuration du logger ────────────────────────────────
_ROOT     = Path(__file__).resolve().parents[2]  # ALFRED_PC/
_LOG_DIR  = _ROOT / "logs" / "security"
_LOG_DIR.mkdir(parents=True, exist_ok=True)
_LOG_FILE = _LOG_DIR / "security.log"

_logger = logging.getLogger("alfred.security")
if not _logger.handlers:
    _handler = logging.FileHandler(str(_LOG_FILE), encoding="utf-8")
    _handler.setFormatter(logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    ))
    _logger.addHandler(_handler)
    _logger.setLevel(logging.INFO)
    _logger.propagate = False


def _flush() -> None:
    for h in _logger.handlers:
        h.flush()


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
    _flush()


def log_access(
    user_id: str, action: str, resource: str, result: str,
    request_id: str = "", device_id: str = "", risk_score: int = 0, **kwargs
) -> None:
    """Log structuré pour les tentatives d'accès."""
    parts = [f"user_id={user_id}", f"action={action}", f"resource={resource}", f"result={result}"]
    if request_id: parts.append(f"request_id={request_id}")
    if device_id: parts.append(f"device_id={device_id}")
    if risk_score: parts.append(f"risk_score={risk_score}")
    log_event("ACCESS | " + " | ".join(parts), "INFO" if result == "ALLOW" else "WARNING")


def log_structured_event(event_type: str, level: str = "INFO", **kwargs) -> None:
    """Log structuré avec type d'événement et kwargs arbitraires."""
    pairs = " | ".join(f"{k}={v}" for k, v in kwargs.items())
    log_event(f"{event_type} | {pairs}", level)


def log_auth(
    user_id: str, method: str, success: bool,
    request_id: str = "", device_id: str = "", **kwargs
) -> None:
    """Log structuré pour les tentatives d'authentification."""
    status = "SUCCESS" if success else "FAILURE"
    parts = [f"user_id={user_id}", f"method={method}", f"status={status}"]
    if request_id: parts.append(f"request_id={request_id}")
    if device_id: parts.append(f"device_id={device_id}")
    log_event("AUTH | " + " | ".join(parts), "INFO" if success else "WARNING")


def log_incident(
    incident_id: str = "",
    level: str = "WARNING",
    description: str = "",
    incident_type: str = "SECURITY",
    severity: str = "MEDIUM",
    details: dict | None = None,
    **kwargs
) -> None:
    """Enregistre un incident de sécurité structuré."""
    extra = {**(details or {}), **kwargs}
    if incident_id:
        extra["incident_id"] = incident_id
    if description:
        extra["description"] = description
    log_structured_event("INCIDENT", level, type=incident_type, severity=severity, **extra)


def get_log_file_path() -> "Path":
    """Retourne le Path absolu du fichier de log sécurité."""
    return _LOG_FILE.resolve()


def read_security_log_tail(n: int = 20) -> list[str]:
    """Retourne les n dernières lignes du fichier de log sécurité."""
    if not _LOG_FILE.exists():
        return []
    lines = _LOG_FILE.read_text(encoding="utf-8", errors="replace").splitlines()
    return lines[-n:]
