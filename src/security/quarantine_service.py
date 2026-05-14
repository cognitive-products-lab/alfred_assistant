"""
PROJECT      : ALFRED
BLOCK        : B20
FUNCTION     : XX.XX
FILE         : quarantine_service.py
ROLE         : Quarantaine des modules et ressources suspects — persisté JSON

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-05-10
P26-05-12
VERSION      : V1.0
STATUS       : STABLE

DESCRIPTION :
Met en quarantaine modules et ressources suspects. Registre persisté JSON. Rebuild set RAM au démarrage.
"""

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, List
from uuid import uuid4

from src.security.security_logger import log_event


_ROOT = Path(__file__).resolve().parents[2]
QUARANTINE_FILE = _ROOT / "data" / "security" / "quarantine_registry.json"
QUARANTINE_FILE.parent.mkdir(parents=True, exist_ok=True)

QUARANTINED_MODULES: set[str] = set()


def _rebuild_quarantined_modules() -> None:
    """Reconstruit le set en mémoire depuis le registre persisté."""
    registry = _load_registry()
    for entry in registry:
        if entry.get("status") == "QUARANTINED" and entry.get("item_type") == "module":
            QUARANTINED_MODULES.add(entry["item_name"])


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _load_registry() -> List[Dict[str, Any]]:
    if not QUARANTINE_FILE.exists():
        return []
    try:
        return json.loads(QUARANTINE_FILE.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        log_event("Registre quarantaine corrompu — réinitialisé", "ERROR")
        return []


_rebuild_quarantined_modules()


def _save_registry(registry: List[Dict[str, Any]]) -> None:
    QUARANTINE_FILE.parent.mkdir(parents=True, exist_ok=True)
    QUARANTINE_FILE.write_text(
        json.dumps(registry, indent=4, ensure_ascii=False),
        encoding="utf-8",
    )


def quarantine_item(
    item_name: str,
    reason: str,
    item_type: str = "module",
    severity: str = "HIGH",
    source: str = "security",
) -> Dict[str, Any]:
    """Met un élément en quarantaine. item_type: module | device | file | resource | unknown"""
    if not item_name:
        raise ValueError("item_name ne peut pas être vide")

    registry = _load_registry()

    for entry in registry:
        if entry.get("item_name") == item_name and entry.get("status") == "QUARANTINED":
            entry["reason"] = reason
            entry["severity"] = severity
            entry["updated_at"] = _now()
            _save_registry(registry)
            QUARANTINED_MODULES.add(item_name)
            return entry

    entry = {
        "quarantine_id": str(uuid4()),
        "timestamp": _now(),
        "updated_at": _now(),
        "item_name": item_name,
        "item_type": item_type,
        "reason": reason,
        "severity": severity.upper(),
        "source": source,
        "status": "QUARANTINED",
    }

    registry.append(entry)
    _save_registry(registry)

    if item_type == "module":
        QUARANTINED_MODULES.add(item_name)

    log_event(f"Quarantaine : {item_type}={item_name} raison={reason}", "CRITICAL")
    return entry


def quarantine_module(module_name: str, reason: str) -> None:
    """Compatibilité historique : met un module en quarantaine."""
    quarantine_item(item_name=module_name, reason=reason, item_type="module", severity="CRITICAL")


def is_quarantined(item_name: str) -> bool:
    """Vérifie si un élément est actuellement en quarantaine (lecture disque)."""
    registry = _load_registry()
    return any(
        entry.get("item_name") == item_name and entry.get("status") == "QUARANTINED"
        for entry in registry
    )


def release_item(item_name: str, reason: str = "Libération manuelle") -> bool:
    """Sort un élément de quarantaine."""
    registry = _load_registry()
    updated = False

    for entry in registry:
        if entry.get("item_name") == item_name and entry.get("status") == "QUARANTINED":
            entry["status"] = "RELEASED"
            entry["release_reason"] = reason
            entry["updated_at"] = _now()
            updated = True

    if updated:
        _save_registry(registry)
        QUARANTINED_MODULES.discard(item_name)
        log_event(f"Sortie de quarantaine : {item_name} raison={reason}")
        return True

    log_event(f"Sortie quarantaine impossible : élément introuvable {item_name}", "WARNING")
    return False


def release_module(module_name: str) -> None:
    """Compatibilité historique : sort un module de quarantaine."""
    release_item(module_name)


def list_quarantined(active_only: bool = True) -> List[Dict[str, Any]]:
    """Liste les éléments en quarantaine."""
    registry = _load_registry()
    if active_only:
        return [entry for entry in registry if entry.get("status") == "QUARANTINED"]
    return registry


def summarize_quarantine() -> Dict[str, Any]:
    """Retourne un résumé de la quarantaine pour dashboard."""
    registry = _load_registry()
    active = [entry for entry in registry if entry.get("status") == "QUARANTINED"]

    by_type: Dict[str, int] = {}
    by_severity: Dict[str, int] = {}

    for entry in active:
        item_type = entry.get("item_type", "unknown")
        severity = entry.get("severity", "UNKNOWN")
        by_type[item_type] = by_type.get(item_type, 0) + 1
        by_severity[severity] = by_severity.get(severity, 0) + 1

    return {
        "active_total": len(active),
        "history_total": len(registry),
        "by_type": by_type,
        "by_severity": by_severity,
        "active_items": active,
    }
