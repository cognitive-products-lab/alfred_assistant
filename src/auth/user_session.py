"""
════════════════════════════════════════════════════════════
PROJECT      : ALFRED
BLOCK        : B05
FUNCTION     : 05.02
FILE         : src/auth/user_session.py
ROLE         : Gestion du profil et des préférences session utilisateur

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-05-31
UPDATED      : 2026-06-15
VERSION      : V1.0
STATUS       : VALIDATED

DESCRIPTION :
Charge et expose le profil utilisateur depuis data/users/.
Offre un accès centralisé aux préférences pendant la session courante.

Fonctions couvertes :
  05.02.001 Chargement profil utilisateur          V1
  05.02.002 Préférences de session (langue, mode)  V1
  05.02.003 Mise à jour préférences                V1
════════════════════════════════════════════════════════════
"""
from __future__ import annotations

import copy
import json
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[2]
_PROFILES_DIR = _ROOT / "data" / "users" / "instances"

# État session en mémoire
_session_profile: dict = {}


def load_profile(user_id: str) -> dict:
    """Charge le profil JSON de l'utilisateur. Retourne {} si absent."""
    global _session_profile
    profile_path = _PROFILES_DIR / f"{user_id}.json"
    if profile_path.exists():
        try:
            _session_profile = json.loads(profile_path.read_text(encoding="utf-8"))
        except Exception:
            _session_profile = {}
    else:
        _session_profile = {"user_id": user_id, "preferences": {}}
    return _session_profile


def get_preference(key: str, default=None):
    """Retourne une préférence de la session courante."""
    return _session_profile.get("preferences", {}).get(key, default)


def set_preference(key: str, value) -> None:
    """Met à jour une préférence en mémoire (non persisté)."""
    if "preferences" not in _session_profile:
        _session_profile["preferences"] = {}
    _session_profile["preferences"][key] = value


def get_session_profile() -> dict:
    """Retourne le profil complet de la session courante."""
    return copy.deepcopy(_session_profile)


def get_preferred_language() -> str:
    """Langue préférée de l'utilisateur (défaut : 'fr')."""
    return get_preference("language", "fr")


def get_preferred_mode() -> str:
    """Mode ALFRED préféré (défaut : 'complicite')."""
    return get_preference("mode", "complicite")
