"""
════════════════════════════════════════════════════════════
PROJECT      : ALFRED
BLOCK        : B20
FUNCTION     : 20.14
FILE         : quarantine_service.py
ROLE         : Mise en quarantaine des modules et ressources

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-05-23
UPDATED      : 2026-05-31
VERSION      : V1.1
STATUS       : ACTIVE

DESCRIPTION :
Isole les modules ou ressources compromis. Supporte deux modes :
- In-memory (QUARANTINE_FILE=None) : tests rapides
- File-backed (QUARANTINE_FILE=Path) : isolation complète par test
════════════════════════════════════════════════════════════
"""
import json
from pathlib import Path
from src.security.security_logger import log_event

# État in-memory (utilisé quand QUARANTINE_FILE is None)
QUARANTINED_MODULES: set[str] = set()
QUARANTINED_ITEMS: dict[str, dict] = {}  # item_name → entry dict

# Quand défini, le stockage passe par ce fichier JSON (patchable dans les tests)
QUARANTINE_FILE = None


def _load() -> dict:
    """Charge l'état quarantaine depuis QUARANTINE_FILE ou retourne l'in-memory."""
    if QUARANTINE_FILE is None:
        return {"modules": list(QUARANTINED_MODULES), "items": dict(QUARANTINED_ITEMS)}
    p = Path(QUARANTINE_FILE)
    if p.exists():
        try:
            return json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {"modules": [], "items": {}}


def _save(state: dict) -> None:
    """Sauvegarde l'état dans QUARANTINE_FILE ou met à jour l'in-memory."""
    if QUARANTINE_FILE is None:
        QUARANTINED_MODULES.clear()
        QUARANTINED_MODULES.update(state.get("modules", []))
        QUARANTINED_ITEMS.clear()
        QUARANTINED_ITEMS.update(state.get("items", {}))
        return
    p = Path(QUARANTINE_FILE)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")


def quarantine_module(module_name: str, reason: str) -> None:
    """Met un module en quarantaine."""
    state = _load()
    if module_name not in state["modules"]:
        state["modules"].append(module_name)
    _save(state)
    log_event(f"Module mis en quarantaine : {module_name} | raison={reason}", "CRITICAL")


def is_quarantined(module_name: str) -> bool:
    """Vérifie si un module ou item est en quarantaine."""
    state = _load()
    return module_name in state["modules"] or module_name in state["items"]


def release_module(module_name: str) -> None:
    """Sort un module de quarantaine."""
    state = _load()
    if module_name in state["modules"]:
        state["modules"].remove(module_name)
    _save(state)
    log_event(f"Module sorti de quarantaine : {module_name}")


def quarantine_item(
    item_name: str,
    reason: str,
    item_type: str = "generic",
    severity: str = "MEDIUM",
    source: str = "system",
) -> dict:
    """Met un élément en quarantaine et retourne un rapport."""
    entry = {
        "item_name": item_name,
        "reason": reason,
        "item_type": item_type,
        "severity": severity,
        "source": source,
        "status": "QUARANTINED",
    }
    state = _load()
    state["items"][item_name] = entry
    _save(state)
    log_event(f"Élément mis en quarantaine : {item_name} | raison={reason} | sévérité={severity}", "CRITICAL")
    return entry


def release_item(item_name: str, reason: str = "") -> bool:
    """Sort un élément de quarantaine. Retourne True si libéré, False si inconnu."""
    state = _load()
    was_present = item_name in state["modules"] or item_name in state["items"]
    state["modules"] = [m for m in state["modules"] if m != item_name]
    state["items"].pop(item_name, None)
    _save(state)
    if was_present:
        log_event(f"Élément sorti de quarantaine : {item_name} | raison={reason or 'N/A'}")
    return was_present


def list_quarantined(active_only: bool = False) -> list[dict]:
    """Retourne la liste des éléments en quarantaine sous forme de dicts."""
    state = _load()
    result = []
    for name in sorted(state["modules"]):
        result.append({"item_name": name, "item_type": "module", "severity": "HIGH", "reason": "quarantined"})
    for entry in state["items"].values():
        result.append(entry)
    return result


def summarize_quarantine() -> dict:
    """Synthèse de la quarantaine pour le dashboard sécurité."""
    all_items = list_quarantined()
    by_type: dict[str, int] = {}
    by_severity: dict[str, int] = {}
    for item in all_items:
        t = item.get("item_type", "generic")
        s = item.get("severity", "MEDIUM")
        by_type[t] = by_type.get(t, 0) + 1
        by_severity[s] = by_severity.get(s, 0) + 1
    state = _load()
    return {
        "active_total": len(all_items),
        "history_total": len(all_items),
        "by_type": by_type,
        "by_severity": by_severity,
        "active_items": all_items,
        "modules": sorted(state.get("modules", [])),
        "items": list(state.get("items", {}).values()),
    }
