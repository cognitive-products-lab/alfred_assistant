"""
PROJECT      : ALFRED
BLOCK        : B15 — Avatar & Interface
FILE         : src/ui/calendar_provider_prefs.py
ROLE         : Fournisseur d'agenda par défaut (Google ou Outlook)

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-07-24
VERSION      : V1.0
STATUS       : DRAFT

DESCRIPTION :
Décidé par Céline le 24/07/2026 : quand une demande d'agenda en chat/vocal
ne précise pas explicitement le fournisseur ("ajoute un rendez-vous
Outlook..."), ALFRED utilise ce réglage — Google par défaut. Consommé par
src/core/tool_calling.py (résolution du fournisseur pour les 4 outils
agenda) et par le sélecteur dans Paramètres (pas encore câblé côté UI —
chantier interface en pause, voir mémoire de session).

Persistance JSON : data/settings/calendar_provider_prefs.json
"""

from __future__ import annotations

import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

try:
    from paths import PATHS
    _PREFS_FILE = PATHS.data / "settings" / "calendar_provider_prefs.json"
except Exception:
    _PREFS_FILE = Path(__file__).parents[2] / "data" / "settings" / "calendar_provider_prefs.json"

VALID_PROVIDERS = ("google", "outlook")

_DEFAULTS = {
    "default_provider": "google",
}


def load_default_calendar_provider() -> str:
    """Fournisseur d'agenda par défaut ("google" ou "outlook") — retombe
    toujours sur "google" si le fichier est absent ou contient une valeur
    invalide (fail-safe : Google est le seul fournisseur vérifié en
    conditions réelles à ce jour)."""
    try:
        if _PREFS_FILE.exists():
            data = json.loads(_PREFS_FILE.read_text(encoding="utf-8"))
            provider = data.get("default_provider", "google")
            if provider in VALID_PROVIDERS:
                return provider
    except Exception as exc:
        logger.warning("load_default_calendar_provider: %s", exc)
    return "google"


def set_default_calendar_provider(provider: str) -> dict:
    if provider not in VALID_PROVIDERS:
        raise ValueError(f"Fournisseur d'agenda invalide : {provider!r} (attendu : {VALID_PROVIDERS})")
    prefs = {"default_provider": provider}
    try:
        _PREFS_FILE.parent.mkdir(parents=True, exist_ok=True)
        _PREFS_FILE.write_text(json.dumps(prefs, indent=2, ensure_ascii=False), encoding="utf-8")
    except Exception as exc:
        logger.error("set_default_calendar_provider: %s", exc)
    return prefs
