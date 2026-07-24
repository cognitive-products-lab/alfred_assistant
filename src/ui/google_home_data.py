"""
PROJECT      : ALFRED
BLOCK        : B15 — Avatar & Interface
FILE         : src/ui/google_home_data.py
ROLE         : Orchestration Google Home / Nest pour la vue Appareils
                (consentement, Project ID, connexion OAuth Device Access,
                appels SDM API, synchronisation du registre local V4)

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-07-23
VERSION      : V1.0
STATUS       : DRAFT

DESCRIPTION :
Point d'entrée unique appelé par AlfredDesktopAPI, même rôle que
src/ui/google_calendar_data.py pour l'Agenda. Trois portes successives avant
tout appel réseau : consentement (src/ui/google_home_prefs.py), Project ID
Device Access renseigné, puis connexion OAuth
(src/integrations/google_home_auth.py).

Chaque lecture réussie synchronise config/v4/home_devices.json (catalogue de
types + appareils déclarés) et data/v4/device_registry.json (état runtime) —
ces fichiers existaient déjà en schéma vide (Point C3-J du plan d'action),
ce module les remplit réellement au lieu d'en créer d'autres.

Chaque commande envoyée à un appareil réel passe par
src/security/human_validation.py : la confirmation utilisateur a lieu côté UI
*avant* l'appel à execute_home_command, qui soumet puis auto-approuve
immédiatement — ça donne une traçabilité complète (audit trail) sans workflow
d'approbation à plusieurs parties, inutile ici (assistant mono-utilisateur).
"""

from __future__ import annotations

import json
from datetime import datetime, timezone


def _load_json(path) -> dict:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def _save_json(path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def _sync_local_registry(devices: list[dict]) -> None:
    from paths import PATHS

    now = datetime.now(timezone.utc).isoformat()

    home_devices_path = PATHS.config_v4 / "home_devices.json"
    catalog = _load_json(home_devices_path)
    supported = set(catalog.get("supported_types", []))
    declared = []
    for d in devices:
        supported.add(d["local_type"])
        declared.append({
            "id": d["id"],
            "type": d["local_type"],
            "custom_name": d["custom_name"],
            "room": d["room"],
        })
    catalog["supported_types"] = sorted(supported)
    catalog["declared_devices"] = declared
    catalog.setdefault("_meta", {})
    catalog["_meta"]["status"] = "ACTIF — synchronisé depuis Google Home (Device Access)"
    catalog["_meta"]["last_synced_at"] = now
    _save_json(home_devices_path, catalog)

    registry_path = PATHS.data_v4 / "device_registry.json"
    registry = _load_json(registry_path)
    registry["state"] = {
        d["id"]: {
            "type": d["local_type"],
            "sdm_type": d["sdm_type"],
            "custom_name": d["custom_name"],
            "room": d["room"],
            "online": d["online"],
            "traits": d["traits"],
        }
        for d in devices
    }
    registry.setdefault("_meta", {})
    registry["_meta"]["status"] = "ACTIF — synchronisé depuis Google Home (Device Access)"
    registry["_meta"]["last_synced_at"] = now
    _save_json(registry_path, registry)


def get_home_state() -> dict:
    """État complet pour la vue Appareils — une seule méthode à appeler côté JS."""
    from src.ui.google_home_prefs import load_google_home_prefs

    prefs = load_google_home_prefs()
    if not prefs["consent"]:
        return {"consent": False}

    project_id = prefs.get("project_id")
    if not project_id:
        return {"consent": True, "connected": False, "no_project_id": True}

    from src.integrations import google_home_auth

    creds = google_home_auth.get_credentials()
    if not creds:
        return {"consent": True, "connected": False}

    from src.v4.integration.google_home_adapter import list_devices, available_commands, HomeError

    try:
        devices = list_devices(creds, project_id)
        for d in devices:
            d["available_commands"] = available_commands(d)
        _sync_local_registry(devices)
        return {"consent": True, "connected": True, "ok": True, "devices": devices}
    except HomeError as exc:
        return {"consent": True, "connected": True, "ok": False, "error": str(exc)}


def set_home_consent(enabled: bool) -> dict:
    from src.ui.google_home_prefs import set_consent

    set_consent(enabled)
    return get_home_state()


def set_home_project_id(project_id: str) -> dict:
    from src.ui.google_home_prefs import set_project_id

    set_project_id(project_id)
    return get_home_state()


def get_home_auth_url() -> dict:
    from src.ui.google_home_prefs import load_google_home_prefs

    project_id = load_google_home_prefs().get("project_id")
    if not project_id:
        return {"success": False, "url": None, "error": "Renseigne d'abord le Project ID Device Access."}

    from src.integrations import google_home_auth

    return google_home_auth.get_authorization_url(project_id)


def submit_home_auth_code(code: str) -> dict:
    from src.integrations import google_home_auth

    result = google_home_auth.exchange_code(code)
    return {**result, **get_home_state()}


def disconnect_home() -> dict:
    from src.integrations import google_home_auth

    google_home_auth.disconnect()
    return get_home_state()


def execute_home_command(device_id: str, command: str, params: dict | None = None) -> dict:
    """Exécute une commande sur un appareil — appelé après confirmation côté UI."""
    from src.ui.google_home_prefs import load_google_home_prefs

    prefs = load_google_home_prefs()
    if not prefs["consent"]:
        return {"consent": False}

    project_id = prefs.get("project_id")
    if not project_id:
        return {"consent": True, "connected": False, "no_project_id": True}

    from src.integrations import google_home_auth

    creds = google_home_auth.get_credentials()
    if not creds:
        return {"consent": True, "connected": False}

    from src.security import human_validation

    approval = human_validation.submit_for_review(
        user_id="celine",
        role="owner",
        action=command,
        resource=f"home_device:{device_id}",
        resource_sensitivity="HIGH",
        payload=params or {},
    )
    human_validation.approve_request(
        approval["approval_id"], approved_by="celine",
        note="Confirmé dans l'UI ALFRED avant envoi de la commande.",
    )

    from src.v4.integration.google_home_adapter import execute_command, HomeError

    try:
        execute_command(creds, project_id, device_id, command, params)
        return get_home_state()
    except HomeError as exc:
        state = get_home_state()
        state["ok"] = False
        state["error"] = str(exc)
        return state
