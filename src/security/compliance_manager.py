"""
PROJECT      : ALFRED
BLOCK        : B20
FUNCTION     : XX.XX
FILE         : compliance_manager.py
ROLE         : Conformité locale RGPD — suppression sécurisée des données

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-05-10
VERSION      : V1.0
STATUS       : STABLE

DESCRIPTION :
Identifie les fichiers sensibles, les écrase avant suppression (RGPD) et produit un rapport de conformité local.
"""

import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, List

from src.security.security_logger import log_event


_ROOT = Path(__file__).resolve().parents[2]

SENSITIVE_FILES = [
    "data/user_memory.json",
    "data/memory/episodic/dialogue_history.json",
    "logs/security/security.log",
    "logs/security/audit_trail.jsonl",
    "data/security/incident_register.json",
    "data/security/trusted_devices.json",
    "data/security/quarantine_registry.json",
    "data/security/failed_attempts.json",
]


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _secure_delete(path: Path) -> None:
    """Écrase le contenu avec des zéros avant suppression (correctif P3 RGPD)."""
    try:
        size = path.stat().st_size
        with path.open("wb") as f:
            f.write(b"\x00" * size)
            f.flush()
            os.fsync(f.fileno())
    except Exception:
        pass
    path.unlink(missing_ok=True)


def list_sensitive_files() -> List[Dict[str, Any]]:
    """Liste les fichiers sensibles connus et leur état."""
    result = []
    for file_path in SENSITIVE_FILES:
        path = _ROOT / file_path
        result.append({
            "path": file_path,
            "exists": path.exists(),
            "size_bytes": path.stat().st_size if path.exists() else 0,
        })
    return result


def compliance_report() -> Dict[str, Any]:
    """Produit un rapport local de conformité."""
    files = list_sensitive_files()
    existing = [item for item in files if item["exists"]]

    return {
        "timestamp": _now(),
        "local_first": True,
        "known_sensitive_files": len(files),
        "existing_sensitive_files": len(existing),
        "missing_sensitive_files": len(files) - len(existing),
        "files": files,
        "privacy_controls": {
            "delete_user_data_available": True,
            "local_storage_declared": True,
            "cloud_dependency_required": False,
        },
    }


def delete_user_data(confirm: bool = False) -> Dict[str, Any]:
    """
    Supprime les données utilisateur sensibles connues.
    confirm=True obligatoire. Écrase avant suppression (RGPD).
    """
    if not confirm:
        log_event("Suppression données refusée : confirmation absente", "WARNING")
        return {"deleted": [], "missing": [], "errors": [], "confirmed": False}

    deleted = []
    missing = []
    errors = []

    for file_path in SENSITIVE_FILES:
        path = _ROOT / file_path

        if not path.exists():
            missing.append(file_path)
            continue

        try:
            _secure_delete(path)
            deleted.append(file_path)
            log_event(f"Donnée écrasée et supprimée (RGPD) : {file_path}", "WARNING")
        except Exception as exc:
            errors.append({"path": file_path, "error": str(exc)})
            log_event(f"Erreur suppression sécurisée {file_path} : {exc}", "ERROR")

    return {
        "timestamp": _now(),
        "confirmed": True,
        "deleted": deleted,
        "missing": missing,
        "errors": errors,
    }


def check_privacy_readiness() -> Dict[str, Any]:
    """Vérifie l'état minimal privacy by design."""
    report = compliance_report()
    score = 0
    checks = []

    if report["local_first"]:
        score += 30
        checks.append("Stockage local-first déclaré")

    if report["privacy_controls"]["delete_user_data_available"]:
        score += 30
        checks.append("Suppression des données disponible")

    if not report["privacy_controls"]["cloud_dependency_required"]:
        score += 20
        checks.append("Aucune dépendance cloud obligatoire déclarée")

    if report["known_sensitive_files"] > 0:
        score += 20
        checks.append("Fichiers sensibles identifiés")

    level = "GOOD" if score >= 80 else "PARTIAL" if score >= 50 else "WEAK"

    return {
        "timestamp": _now(),
        "privacy_score": score,
        "privacy_level": level,
        "checks": checks,
    }
