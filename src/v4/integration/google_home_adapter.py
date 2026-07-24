"""
PROJECT      : ALFRED
BLOCK        : 14.01/14.03/14.05 — Domotique, gestion des équipements
FILE         : src/v4/integration/google_home_adapter.py
ROLE         : Adapter Google Home / Nest — Smart Device Management API

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-07-23
VERSION      : V1.0
STATUS       : DRAFT

DESCRIPTION :
Implémente le pattern Adapter prévu au BACKLOG (B14/B19, à côté d'un futur
tuya_adapter.py) pour les appareils Google Home reliés via un compte Nest
(Device Access — projet "ALFRED_HOME"). Utilise google-api-python-client
comme src/integrations/google_calendar_client.py, avec le service Discovery
"smartdevicemanagement" plutôt que "calendar".

Périmètre réel du SDM API pour un compte Nest individuel : les commandes
structurées ne couvrent que le thermostat (mode, consignes de température).
Caméras/sonnettes exposent un état (en ligne, nom, pièce) mais pas de
commande de pilotage ici — le flux vidéo est un chantier distinct, plus
lourd, volontairement hors scope.

Ne connaît ni le consentement, ni l'authentification, ni la synchronisation
vers config/v4/home_devices.json ou data/v4/device_registry.json — ce module
prend des Credentials déjà valides en paramètre (voir
src/integrations/google_home_auth.py) et n'est appelé qu'après vérification
du consentement (src/ui/google_home_prefs.py) par l'appelant
(src/ui/google_home_data.py).
"""

from __future__ import annotations

_SDM_TYPE_MAP = {
    "sdm.devices.types.THERMOSTAT": "thermostat",
    "sdm.devices.types.CAMERA": "camera",
    "sdm.devices.types.DOORBELL": "doorbell",
    "sdm.devices.types.DISPLAY": "display",
}

_COMMAND_MAP = {
    "SetMode": "sdm.devices.commands.ThermostatMode.SetMode",
    "SetHeat": "sdm.devices.commands.ThermostatTemperatureSetpoint.SetHeat",
    "SetCool": "sdm.devices.commands.ThermostatTemperatureSetpoint.SetCool",
    "SetRange": "sdm.devices.commands.ThermostatTemperatureSetpoint.SetRange",
}

_CONNECTIVITY_TRAIT = "sdm.devices.traits.Connectivity"
_INFO_TRAIT = "sdm.devices.traits.Info"
_THERMOSTAT_MODE_TRAIT = "sdm.devices.traits.ThermostatMode"
_THERMOSTAT_SETPOINT_TRAIT = "sdm.devices.traits.ThermostatTemperatureSetpoint"


class HomeError(Exception):
    """Erreur d'appel Smart Device Management — message déjà en français, affichable tel quel."""


def _build_service(creds):
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError

    try:
        return build("smartdevicemanagement", "v1", credentials=creds, cache_discovery=False)
    except HttpError as exc:
        raise HomeError(f"Connexion à Google Home impossible : {exc}") from exc


def local_type_for(sdm_type: str) -> str:
    """Type local (config/v4/home_devices.json supported_types) pour un type SDM donné."""
    if sdm_type in _SDM_TYPE_MAP:
        return _SDM_TYPE_MAP[sdm_type]
    return sdm_type.rsplit(".", 1)[-1].lower()


def _normalize_device(device: dict) -> dict:
    traits = device.get("traits", {})
    parent_relations = device.get("parentRelations", [])
    room = parent_relations[0].get("displayName") if parent_relations else None
    custom_name = traits.get(_INFO_TRAIT, {}).get("customName") or room or device.get("name", "")
    online = traits.get(_CONNECTIVITY_TRAIT, {}).get("status") == "ONLINE"
    sdm_type = device.get("type", "")

    return {
        "id": device.get("name", "").rsplit("/", 1)[-1],
        "name": device.get("name", ""),
        "sdm_type": sdm_type,
        "local_type": local_type_for(sdm_type),
        "room": room,
        "custom_name": custom_name,
        "online": online,
        "traits": traits,
    }


def available_commands(device: dict) -> list[str]:
    """Dérive les commandes possibles selon les traits présents sur l'appareil."""
    traits = device.get("traits", {})
    commands: list[str] = []
    if _THERMOSTAT_MODE_TRAIT in traits:
        commands.append("SetMode")
    if _THERMOSTAT_SETPOINT_TRAIT in traits:
        commands.append("SetHeat")
        commands.append("SetCool")
    return commands


def list_devices(creds, project_id: str) -> list[dict]:
    """
    Liste les appareils Nest reliés au projet Device Access.

    Returns:
        Liste d'appareils normalisés {id, name, sdm_type, local_type, room,
        custom_name, online, traits}.

    Raises:
        HomeError en cas d'échec de l'appel API.
    """
    from googleapiclient.errors import HttpError

    service = _build_service(creds)
    parent = f"enterprises/{project_id}"

    try:
        response = service.enterprises().devices().list(parent=parent).execute()
    except HttpError as exc:
        raise HomeError(f"Lecture des appareils Google Home impossible : {exc}") from exc

    return [_normalize_device(d) for d in response.get("devices", [])]


def execute_command(creds, project_id: str, device_id: str, command: str, params: dict | None = None) -> dict:
    """
    Exécute une commande sur un appareil (thermostat uniquement pour l'instant).

    Args:
        device_id : identifiant court de l'appareil (dernier segment du "name" SDM)
        command   : une des clés de _COMMAND_MAP (ex. "SetMode", "SetHeat")
        params    : paramètres de la commande (ex. {"mode": "HEAT"} ou {"heatCelsius": 20.0})

    Raises:
        HomeError si la commande est inconnue ou si l'appel API échoue.
    """
    from googleapiclient.errors import HttpError

    sdm_command = _COMMAND_MAP.get(command)
    if not sdm_command:
        raise HomeError(f"Commande inconnue : {command}")

    service = _build_service(creds)
    name = f"enterprises/{project_id}/devices/{device_id}"
    body = {"command": sdm_command, "params": params or {}}

    try:
        return service.enterprises().devices().executeCommand(name=name, body=body).execute()
    except HttpError as exc:
        raise HomeError(f"Exécution de la commande impossible : {exc}") from exc
