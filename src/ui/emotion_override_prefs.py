"""
PROJECT      : ALFRED
BLOCK        : B15 — Avatar & Interface
FILE         : src/ui/emotion_override_prefs.py
ROLE         : Persistance de la correction/désactivation manuelle du widget "État émotionnel"

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-07-19
VERSION      : V1.0
STATUS       : DRAFT

DESCRIPTION :
Le widget dashboard "État émotionnel" affiche normalement l'estimation live
(MultiSignalFusionEngine). L'utilisateur peut soit la désactiver complètement,
soit la corriger manuellement (auquel cas la correction manuelle prime sur
l'estimation live jusqu'à la prochaine désactivation/réactivation).
Même pattern de persistance JSON simple que desktop_prefs.py/device_settings.py.

Persistance JSON : data/settings/emotion_override.json
"""

from __future__ import annotations

import json
import logging
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)

try:
    from paths import PATHS
    _OVERRIDE_FILE = PATHS.data / "settings" / "emotion_override.json"
except Exception:
    _OVERRIDE_FILE = Path(__file__).parents[2] / "data" / "settings" / "emotion_override.json"

_DEFAULTS = {
    "enabled": True,
    "manual_mood": None,
    "manual_set_at": None,
}


def load_emotion_override() -> dict:
    """Charge l'état de correction/désactivation (retourne les défauts si absent)."""
    try:
        if _OVERRIDE_FILE.exists():
            data = json.loads(_OVERRIDE_FILE.read_text(encoding="utf-8"))
            return {**_DEFAULTS, **data}
    except Exception as exc:
        logger.warning("load_emotion_override: %s", exc)
    return dict(_DEFAULTS)


def save_emotion_override(*, enabled: bool | None = None, manual_mood: str | None = None) -> dict:
    """
    Met à jour l'état (uniquement les champs passés) et sauvegarde le fichier complet.
    Une correction manuelle (manual_mood) réactive implicitement l'estimation (enabled=True) :
    corriger une estimation désactivée n'aurait pas de sens.
    """
    state = load_emotion_override()
    if enabled is not None:
        state["enabled"] = enabled
    if manual_mood is not None:
        state["manual_mood"] = manual_mood
        state["manual_set_at"] = datetime.now().isoformat()
        state["enabled"] = True
    try:
        _OVERRIDE_FILE.parent.mkdir(parents=True, exist_ok=True)
        _OVERRIDE_FILE.write_text(
            json.dumps(state, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
    except Exception as exc:
        logger.error("save_emotion_override: %s", exc)
    return state


def clear_manual_mood() -> dict:
    """Efface la correction manuelle pour revenir à l'estimation live."""
    state = load_emotion_override()
    state["manual_mood"] = None
    state["manual_set_at"] = None
    try:
        _OVERRIDE_FILE.parent.mkdir(parents=True, exist_ok=True)
        _OVERRIDE_FILE.write_text(
            json.dumps(state, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
    except Exception as exc:
        logger.error("clear_manual_mood: %s", exc)
    return state
