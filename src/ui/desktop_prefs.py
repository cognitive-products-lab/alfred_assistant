"""
PROJECT      : ALFRED
BLOCK        : B15 — Avatar & Interface
FILE         : src/ui/desktop_prefs.py
ROLE         : Persistance des préférences d'affichage de l'interface desktop HTML

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-07-18
VERSION      : V1.0
STATUS       : DRAFT

DESCRIPTION :
Réglages d'apparence/accessibilité de src/alfred_desktop.py (thème, taille de
texte, contraste renforcé, animations réduites, sous-titres, police dyslexie).
Distinct de device_settings.py (caméra/micro/sortie son) — préoccupation
différente, même pattern de persistance JSON simple.

Persistance JSON : data/settings/desktop_ui_prefs.json
"""

from __future__ import annotations

import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

try:
    from paths import PATHS
    _PREFS_FILE = PATHS.data / "settings" / "desktop_ui_prefs.json"
except Exception:
    _PREFS_FILE = Path(__file__).parents[2] / "data" / "settings" / "desktop_ui_prefs.json"

_DEFAULTS = {
    "theme": "system",       # system | light | dark
    "fontsize": "md",        # sm | md | lg | xl
    "high_contrast": False,
    "reduced_motion": False,
    "captions": True,
    "dyslexia_font": False,
}


def load_desktop_prefs() -> dict:
    """Charge les préférences depuis JSON (retourne les défauts si absent)."""
    try:
        if _PREFS_FILE.exists():
            data = json.loads(_PREFS_FILE.read_text(encoding="utf-8"))
            return {**_DEFAULTS, **data}
    except Exception as exc:
        logger.warning("load_desktop_prefs: %s", exc)
    return dict(_DEFAULTS)


def save_desktop_pref(key: str, value) -> dict:
    """Met à jour une préférence et sauvegarde le fichier complet. Retourne l'état à jour."""
    prefs = load_desktop_prefs()
    prefs[key] = value
    try:
        _PREFS_FILE.parent.mkdir(parents=True, exist_ok=True)
        _PREFS_FILE.write_text(
            json.dumps(prefs, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
    except Exception as exc:
        logger.error("save_desktop_pref: %s", exc)
    return prefs
