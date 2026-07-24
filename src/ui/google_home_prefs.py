"""
PROJECT      : ALFRED
BLOCK        : B15 — Avatar & Interface
FILE         : src/ui/google_home_prefs.py
ROLE         : Persistance du consentement Google Home + Project ID Device Access

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-07-23
VERSION      : V1.0
STATUS       : DRAFT

DESCRIPTION :
Même pattern que src/ui/weather_prefs.py / google_calendar_prefs.py.
Le Project ID Device Access ("ALFRED_HOME") n'est pas un secret Google Cloud
classique (pas de risque à le stocker en clair ici) — c'est un identifiant
que l'utilisateur saisit une fois dans l'UI Paramètres, nécessaire pour
construire l'URL d'autorisation et interroger le SDM API (voir
src/integrations/google_home_auth.py, src/v4/integration/google_home_adapter.py).
L'état de connexion OAuth lui-même n'est pas dupliqué ici : il vit dans
google_home_auth.is_connected().

Persistance JSON : data/settings/google_home_prefs.json
"""

from __future__ import annotations

import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

try:
    from paths import PATHS
    _PREFS_FILE = PATHS.data / "settings" / "google_home_prefs.json"
except Exception:
    _PREFS_FILE = Path(__file__).parents[2] / "data" / "settings" / "google_home_prefs.json"

_DEFAULTS = {
    "consent": False,
    "project_id": None,
}


def load_google_home_prefs() -> dict:
    """Charge les préférences Google Home (retourne les défauts si absent)."""
    try:
        if _PREFS_FILE.exists():
            data = json.loads(_PREFS_FILE.read_text(encoding="utf-8"))
            return {**_DEFAULTS, **data}
    except Exception as exc:
        logger.warning("load_google_home_prefs: %s", exc)
    return dict(_DEFAULTS)


def _save(prefs: dict) -> None:
    try:
        _PREFS_FILE.parent.mkdir(parents=True, exist_ok=True)
        _PREFS_FILE.write_text(
            json.dumps(prefs, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
    except Exception as exc:
        logger.error("save google_home_prefs: %s", exc)


def set_consent(enabled: bool) -> dict:
    prefs = load_google_home_prefs()
    prefs["consent"] = enabled
    _save(prefs)
    return prefs


def set_project_id(project_id: str | None) -> dict:
    prefs = load_google_home_prefs()
    prefs["project_id"] = (project_id or "").strip() or None
    _save(prefs)
    return prefs
