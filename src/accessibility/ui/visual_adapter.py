"""
════════════════════════════════════════════════════════════
PROJECT      : ALFRED
BLOCK        : B22
FUNCTION     : 22.06
FILE         : visual_adapter.py
ROLE         : Accessibilité visuelle & typographie dyslexie — profils CSS et paramètres d'affichage

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
Fournit des profils typographiques adaptés à la dyslexie (OpenDyslexic, espacement augmenté)
et à la basse vision. Génère des overrides CSS injectables dans le dashboard Kivy/web.
4 profils prédéfinis : standard, dyslexia, low_vision, high_contrast.
════════════════════════════════════════════════════════════
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Literal

logger = logging.getLogger(__name__)

FontProfile = Literal["standard", "dyslexia", "low_vision", "high_contrast"]


@dataclass
class VisualProfile:
    name: FontProfile
    font_family: str
    font_size_px: int
    line_height: float
    letter_spacing_em: float
    word_spacing_em: float
    background: str
    foreground: str
    bold_labels: bool = False


_PROFILES: dict[str, VisualProfile] = {
    "standard": VisualProfile(
        name="standard",
        font_family="JetBrains Mono, monospace",
        font_size_px=13,
        line_height=1.6,
        letter_spacing_em=0.0,
        word_spacing_em=0.0,
        background="#07090f",
        foreground="#b8c4d8",
    ),
    "dyslexia": VisualProfile(
        name="dyslexia",
        font_family="OpenDyslexic, Arial, sans-serif",
        font_size_px=16,
        line_height=2.0,
        letter_spacing_em=0.12,
        word_spacing_em=0.25,
        background="#fffde7",
        foreground="#1a1a1a",
        bold_labels=True,
    ),
    "low_vision": VisualProfile(
        name="low_vision",
        font_family="Arial, sans-serif",
        font_size_px=20,
        line_height=2.2,
        letter_spacing_em=0.08,
        word_spacing_em=0.15,
        background="#000000",
        foreground="#ffffff",
    ),
    "high_contrast": VisualProfile(
        name="high_contrast",
        font_family="Arial, sans-serif",
        font_size_px=16,
        line_height=1.8,
        letter_spacing_em=0.05,
        word_spacing_em=0.1,
        background="#000000",
        foreground="#ffff00",
    ),
}


class VisualAdapter:
    """
    22.06 Accessibilité visuelle & typographie dyslexie.

    Adapte l'affichage selon le profil visuel actif.
    """

    def __init__(self, profile: FontProfile = "standard") -> None:
        self._profile = _PROFILES.get(profile, _PROFILES["standard"])
        logger.info("VisualAdapter initialisé : profil=%s", profile)

    def set_profile(self, profile: FontProfile) -> None:
        """Change le profil visuel actif."""
        if profile not in _PROFILES:
            logger.warning("Profil visuel inconnu : %s — standard utilisé", profile)
            profile = "standard"
        self._profile = _PROFILES[profile]

    def get_profile(self) -> VisualProfile:
        return self._profile

    def to_css(self) -> str:
        """Génère un bloc CSS injectable dans le dashboard web."""
        p = self._profile
        return (
            f"body {{"
            f" font-family: {p.font_family};"
            f" font-size: {p.font_size_px}px;"
            f" line-height: {p.line_height};"
            f" letter-spacing: {p.letter_spacing_em}em;"
            f" word-spacing: {p.word_spacing_em}em;"
            f" background: {p.background};"
            f" color: {p.foreground};"
            f" }}"
        )

    def adapt_text_for_dyslexia(self, text: str) -> str:
        """Reformate le texte avec des paragraphes courts pour la dyslexie."""
        return text.replace(". ", ".\n").replace("? ", "?\n").replace("! ", "!\n").strip()

    def status(self) -> dict:
        return {
            "active_profile": self._profile.name,
            "available_profiles": list(_PROFILES.keys()),
        }


# ─────────────────────────────────────────────────────────
# Test standalone
# ─────────────────────────────────────────────────────────
if __name__ == "__main__":
    adapter = VisualAdapter("dyslexia")
    print(f"Profil : {adapter.get_profile()}")
    print(f"CSS : {adapter.to_css()}")
    print("VisualAdapter skeleton OK.")
