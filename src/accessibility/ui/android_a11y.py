"""
════════════════════════════════════════════════════════════
PROJECT      : ALFRED
BLOCK        : B22
FUNCTION     : 22.13
FILE         : android_a11y.py
ROLE         : Accessibilité Android — TalkBack, cibles tactiles, contrastes, font scale

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-05-22
UPDATED      : 2026-05-22
VERSION      : V1.0
STATUS       : SKELETON

DEPENDENCIES :
- dataclasses
- typing

SECURITY :
- Local-first
- Security by Design

DESCRIPTION :
Configuration d'accessibilité pour l'app Android ALFRED (V4 futur).
3 profils : standard, low_vision, motor.
Génère les labels TalkBack, vérifie les cibles tactiles (min 48dp) et les contrastes.
Intégration future : buildscript Android / Kivy-Android.
════════════════════════════════════════════════════════════
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Literal

logger = logging.getLogger(__name__)

AndroidProfile = Literal["standard", "low_vision", "motor"]


@dataclass
class AndroidA11yConfig:
    profile: AndroidProfile
    min_touch_target_dp: int = 48
    min_contrast_ratio: float = 4.5
    talkback_enabled: bool = True
    font_scale: float = 1.0
    display_size_scale: float = 1.0
    reduce_motion: bool = False
    high_contrast_text: bool = False


_CONFIGS: dict[str, AndroidA11yConfig] = {
    "standard": AndroidA11yConfig(profile="standard"),
    "low_vision": AndroidA11yConfig(
        profile="low_vision",
        font_scale=1.4,
        display_size_scale=1.3,
        high_contrast_text=True,
        min_contrast_ratio=7.0,
    ),
    "motor": AndroidA11yConfig(
        profile="motor",
        min_touch_target_dp=64,
        reduce_motion=True,
    ),
}

_TALKBACK_LABELS: dict[str, str] = {
    "btn_send": "Envoyer le message",
    "btn_mic": "Activer ou désactiver le microphone",
    "btn_sound": "Activer ou désactiver le son",
    "btn_settings": "Ouvrir les paramètres",
    "avatar_alfred": "Avatar ALFRED — assistant personnel",
    "input_text": "Zone de saisie — entrez votre message ici",
    "chat_history": "Historique de la conversation avec ALFRED",
    "btn_camera": "Activer ou désactiver la caméra",
    "status_bar": "Barre d'état — affiche l'état du système",
}


class AndroidA11y:
    """
    22.13 Accessibilité Android.

    Fournit la configuration et les labels TalkBack pour l'app Android.
    """

    def __init__(self, profile: AndroidProfile = "standard") -> None:
        self._config = _CONFIGS.get(profile, _CONFIGS["standard"])
        logger.info("AndroidA11y initialisé : profil=%s", profile)

    def set_profile(self, profile: AndroidProfile) -> None:
        self._config = _CONFIGS.get(profile, _CONFIGS["standard"])

    def get_config(self) -> dict:
        """Retourne la configuration sous forme de dict sérialisable."""
        c = self._config
        return {
            "profile": c.profile,
            "min_touch_target_dp": c.min_touch_target_dp,
            "min_contrast_ratio": c.min_contrast_ratio,
            "talkback_enabled": c.talkback_enabled,
            "font_scale": c.font_scale,
            "display_size_scale": c.display_size_scale,
            "reduce_motion": c.reduce_motion,
            "high_contrast_text": c.high_contrast_text,
        }

    def talkback_label(self, element_id: str) -> str:
        """Retourne le label TalkBack pour un élément d'interface."""
        return _TALKBACK_LABELS.get(element_id, element_id.replace("_", " ").title())

    def register_label(self, element_id: str, label: str) -> None:
        """Enregistre un label TalkBack personnalisé pour la session."""
        _TALKBACK_LABELS[element_id] = label

    def check_touch_target(self, size_dp: int) -> bool:
        """Vérifie si une taille de cible tactile respecte le minimum."""
        return size_dp >= self._config.min_touch_target_dp

    def status(self) -> dict:
        return {
            "active_profile": self._config.profile,
            "available_profiles": list(_CONFIGS.keys()),
            "talkback_labels_count": len(_TALKBACK_LABELS),
        }


# ─────────────────────────────────────────────────────────
# Test standalone
# ─────────────────────────────────────────────────────────
if __name__ == "__main__":
    a11y = AndroidA11y("low_vision")
    print(f"Config : {a11y.get_config()}")
    print(f"Label btn_send : {a11y.talkback_label('btn_send')}")
    print(f"Touch 44dp OK : {a11y.check_touch_target(44)}")
    print("AndroidA11y skeleton OK.")
