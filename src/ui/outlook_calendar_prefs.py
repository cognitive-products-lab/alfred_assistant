"""
PROJECT      : ALFRED
BLOCK        : B15 — Avatar & Interface
FILE         : src/ui/outlook_calendar_prefs.py
ROLE         : Persistance du consentement Agenda Outlook

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-07-24
VERSION      : V1.0
STATUS       : DRAFT

DESCRIPTION :
Même rôle et même pattern que src/ui/google_calendar_prefs.py, pour le
second fournisseur d'agenda (Outlook/Microsoft Graph). L'état de connexion
OAuth lui-même n'est pas dupliqué ici : il vit dans
src/integrations/outlook_auth.py (is_connected()), ce module ne gère que le
consentement.

Persistance JSON : data/settings/outlook_calendar_prefs.json
"""

from __future__ import annotations

import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

try:
    from paths import PATHS
    _PREFS_FILE = PATHS.data / "settings" / "outlook_calendar_prefs.json"
except Exception:
    _PREFS_FILE = Path(__file__).parents[2] / "data" / "settings" / "outlook_calendar_prefs.json"

_DEFAULTS = {
    "consent": False,
}


def load_outlook_calendar_prefs() -> dict:
    """Charge les préférences Agenda Outlook (retourne les défauts si absent)."""
    try:
        if _PREFS_FILE.exists():
            data = json.loads(_PREFS_FILE.read_text(encoding="utf-8"))
            return {**_DEFAULTS, **data}
    except Exception as exc:
        logger.warning("load_outlook_calendar_prefs: %s", exc)
    return dict(_DEFAULTS)


def _save(prefs: dict) -> None:
    try:
        _PREFS_FILE.parent.mkdir(parents=True, exist_ok=True)
        _PREFS_FILE.write_text(
            json.dumps(prefs, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
    except Exception as exc:
        logger.error("save outlook_calendar_prefs: %s", exc)


def set_consent(enabled: bool) -> dict:
    prefs = load_outlook_calendar_prefs()
    prefs["consent"] = enabled
    _save(prefs)
    return prefs
