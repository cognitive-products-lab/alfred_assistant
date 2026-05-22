# ============================================================
# ALFRED — src/accessibility/accessibility_manager.py
# Bloc 22.01 — Politique d'accessibilité
#
# 📚 NOTION EXAM :
#   D41-3 — Capsule 3 : Accessibilité, inclusion et adaptation cognitive
#
# 🎯 UTILITÉ ALFRED :
#   Point d'entrée central du Bloc 22 — orchestre les fonctions
#   d'accessibilité (lecture vocale, traduction, assistance cognitive)
#   selon le profil et les préférences de l'utilisateur.
#
# 🔐 BLOC SÉCURITÉ / DOMAINE :
#   Accessibilité & assistance cognitive (22.01)
# ============================================================

import json
import os

_SETTINGS_PATH = os.path.join(os.path.dirname(__file__), "accessibility_settings.json")


def load_settings() -> dict:
    if os.path.exists(_SETTINGS_PATH):
        with open(_SETTINGS_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return _default_settings()


def _default_settings() -> dict:
    return {
        "voice_reading_enabled": False,
        "translation_enabled": False,
        "cognitive_assistance_enabled": False,
        "simplification_mode": False,
        "voice_speed": 1.0,
        "voice_tone": "neutral",
        "preferred_language": "fr",
        "dyslexia_font": False,
        "high_contrast": False,
    }


def get_active_features(settings: dict) -> list:
    active = []
    if settings.get("voice_reading_enabled"):
        active.append("voice_reading")
    if settings.get("translation_enabled"):
        active.append("translation")
    if settings.get("cognitive_assistance_enabled"):
        active.append("cognitive_assistance")
    if settings.get("simplification_mode"):
        active.append("simplification")
    return active


def is_feature_enabled(feature: str, settings: dict | None = None) -> bool:
    if settings is None:
        settings = load_settings()
    return bool(settings.get(f"{feature}_enabled", False))
