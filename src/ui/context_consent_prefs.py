"""
PROJECT      : ALFRED
BLOCK        : B15 — Avatar & Interface
FILE         : src/ui/context_consent_prefs.py
ROLE         : Consentement par catégorie pour les "données utilisées" du dashboard

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-07-19
VERSION      : V1.0
STATUS       : DRAFT

DESCRIPTION :
Le widget "3 données contextuelles utilisées" du dashboard affichait 3
toggles ("Agenda du jour", "5 dernières tâches", "Préférences vocales")
purement décoratifs — aucun concept de consentement par catégorie n'existait
côté backend. Même pattern de persistance que weather_prefs.py/
emotion_override_prefs.py.

Portée honnête (voir header de desktop_dashboard_data.py pour le détail) :
ces toggles filtrent ce qui est montré dans les WIDGETS du dashboard
desktop — pas d'injection agenda/tâches dans le prompt LLM aujourd'hui
(src/conversation/input/context_builder.py ne construit que temps/appareil/
historique de conversation, aucune de ces 3 catégories n'y entre). Étendre
ce gate à l'injection LLM est un chantier séparé, plus large.

Persistance JSON : data/settings/context_consent.json
"""

from __future__ import annotations

import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

try:
    from paths import PATHS
    _PREFS_FILE = PATHS.data / "settings" / "context_consent.json"
except Exception:
    _PREFS_FILE = Path(__file__).parents[2] / "data" / "settings" / "context_consent.json"

_DEFAULTS = {
    "agenda": True,
    "taches": True,
    "voice_prefs": True,
}


def load_context_consent() -> dict:
    """Charge les 3 consentements par catégorie (retourne les défauts si absent)."""
    try:
        if _PREFS_FILE.exists():
            data = json.loads(_PREFS_FILE.read_text(encoding="utf-8"))
            return {**_DEFAULTS, **data}
    except Exception as exc:
        logger.warning("load_context_consent: %s", exc)
    return dict(_DEFAULTS)


def set_context_consent(category: str, enabled: bool) -> dict:
    """Met à jour un consentement de catégorie et sauvegarde le fichier complet."""
    if category not in _DEFAULTS:
        raise ValueError(f"Catégorie inconnue : {category}")
    prefs = load_context_consent()
    prefs[category] = enabled
    try:
        _PREFS_FILE.parent.mkdir(parents=True, exist_ok=True)
        _PREFS_FILE.write_text(
            json.dumps(prefs, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
    except Exception as exc:
        logger.error("save context_consent: %s", exc)
    return prefs
