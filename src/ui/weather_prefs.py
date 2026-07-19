"""
PROJECT      : ALFRED
BLOCK        : B15 — Avatar & Interface
FILE         : src/ui/weather_prefs.py
ROLE         : Persistance du consentement météo + dernier code postal consulté

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-07-19
VERSION      : V1.0
STATUS       : DRAFT

DESCRIPTION :
La météo est le premier appel réseau réellement externe du pipeline ALFRED
(voir src/integrations/weather_client.py) — le bandeau de confidentialité du
dashboard affiche en permanence "Aucune connexion extérieure", donc aucun
appel n'est fait tant que `consent` n'est pas explicitement activé ici.
Même pattern de persistance JSON simple que desktop_prefs.py/device_settings.py.

Persistance JSON : data/settings/weather_prefs.json
"""

from __future__ import annotations

import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

try:
    from paths import PATHS
    _PREFS_FILE = PATHS.data / "settings" / "weather_prefs.json"
except Exception:
    _PREFS_FILE = Path(__file__).parents[2] / "data" / "settings" / "weather_prefs.json"

_DEFAULTS = {
    "consent": False,
    "last_postal_code": None,  # None = utiliser la localisation du profil
}


def load_weather_prefs() -> dict:
    """Charge les préférences météo (retourne les défauts si absent)."""
    try:
        if _PREFS_FILE.exists():
            data = json.loads(_PREFS_FILE.read_text(encoding="utf-8"))
            return {**_DEFAULTS, **data}
    except Exception as exc:
        logger.warning("load_weather_prefs: %s", exc)
    return dict(_DEFAULTS)


def _save(prefs: dict) -> None:
    try:
        _PREFS_FILE.parent.mkdir(parents=True, exist_ok=True)
        _PREFS_FILE.write_text(
            json.dumps(prefs, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
    except Exception as exc:
        logger.error("save weather_prefs: %s", exc)


def set_consent(enabled: bool) -> dict:
    prefs = load_weather_prefs()
    prefs["consent"] = enabled
    _save(prefs)
    return prefs


def set_last_postal_code(postal_code: str | None) -> dict:
    prefs = load_weather_prefs()
    prefs["last_postal_code"] = postal_code
    _save(prefs)
    return prefs
