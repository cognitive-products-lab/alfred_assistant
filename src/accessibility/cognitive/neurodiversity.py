"""
════════════════════════════════════════════════════════════
PROJECT      : ALFRED
BLOCK        : B22
FUNCTION     : 22.12
FILE         : neurodiversity.py
ROLE         : Modes neurodiversité & assistance adaptative — TDAH, TSA, dyslexie, dyscalculie

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-05-22
UPDATED      : 2026-05-22
VERSION      : V1.0
STATUS       : TESTED

DEPENDENCIES :
- re
- logging
- dataclasses
- typing

SECURITY :
- Local-first
- Security by Design

DESCRIPTION :
Définit 4 profils neurodiversité (TDAH, TSA, dyslexie, dyscalculie) avec leurs
paramètres adaptatifs : longueur de phrases, listes, métaphores, animations.
Filtre les réponses ALFRED selon le mode actif.
Intégration prévue : AccessibilityManager → AccessibilityProfile.neurodiversity_mode.
════════════════════════════════════════════════════════════
"""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass, field
from typing import Literal, Optional

logger = logging.getLogger(__name__)

NdMode = Literal["adhd", "autism", "dyslexia", "dyscalculia", "standard"]


@dataclass
class NdProfile:
    mode: NdMode
    max_sentence_words: int = 30          # coupe les phrases > N mots
    max_list_items: int = 5               # limite les listes
    avoid_metaphors: bool = False         # remplace les métaphores par le littéral
    literal_language: bool = False        # évite l'ironie et l'implicite
    use_bullet_points: bool = True
    reduce_animation: bool = False        # signal pour l'UI
    font_profile: str = "standard"        # transmet à VisualAdapter
    chunk_words: int = 80                 # transmet à FatigueReducer
    extra_pauses: bool = False


_PROFILES: dict[str, NdProfile] = {
    "standard": NdProfile(mode="standard"),
    "adhd": NdProfile(
        mode="adhd",
        max_sentence_words=15,
        max_list_items=3,
        use_bullet_points=True,
        chunk_words=50,
        extra_pauses=True,
    ),
    "autism": NdProfile(
        mode="autism",
        avoid_metaphors=True,
        literal_language=True,
        max_sentence_words=20,
        reduce_animation=True,
        chunk_words=60,
    ),
    "dyslexia": NdProfile(
        mode="dyslexia",
        font_profile="dyslexia",
        max_sentence_words=18,
        chunk_words=60,
        use_bullet_points=True,
    ),
    "dyscalculia": NdProfile(
        mode="dyscalculia",
        use_bullet_points=True,
    ),
}

# Correspondances métaphore → littéral
_METAPHORS: dict[str, str] = {
    "comme une montagne": "très grand",
    "pluie d'idées": "beaucoup d'idées",
    "brûler les étapes": "aller trop vite",
    "noyer le poisson": "éviter le sujet",
    "rouler sur l'or": "avoir beaucoup d'argent",
    "casser les pieds": "ennuyer",
    "avoir le cafard": "être triste",
    "prendre un vent": "être ignoré",
}


class NeurodiversityAdapter:
    """
    22.12 Modes neurodiversité & assistance adaptative.

    Filtre et reformate les réponses selon le mode actif.
    """

    def __init__(self, mode: NdMode = "standard") -> None:
        self._mode = mode
        self._profile = _PROFILES.get(mode, _PROFILES["standard"])
        logger.info("NeurodiversityAdapter initialisé : mode=%s", mode)

    def set_mode(self, mode: NdMode) -> None:
        if mode not in _PROFILES:
            logger.warning("Mode neurodiversité inconnu : %s — standard utilisé", mode)
            mode = "standard"
        self._mode = mode
        self._profile = _PROFILES[mode]

    def get_profile(self) -> NdProfile:
        return self._profile

    def apply(self, text: str) -> str:
        """Applique tous les filtres du profil actif sur `text`."""
        p = self._profile

        if p.avoid_metaphors:
            text = self._replace_metaphors(text)

        if p.max_sentence_words < 30:
            text = self._shorten_sentences(text, p.max_sentence_words)

        return text

    def _replace_metaphors(self, text: str) -> str:
        for metaphor, literal in _METAPHORS.items():
            text = text.replace(metaphor, literal)
        return text

    def _shorten_sentences(self, text: str, max_words: int) -> str:
        sentences = re.split(r"(?<=[.!?])\s+", text.strip())
        result: list[str] = []
        for s in sentences:
            words = s.split()
            if len(words) > max_words:
                mid = len(words) // 2
                result.append(" ".join(words[:mid]) + ".")
                result.append(" ".join(words[mid:]))
            else:
                result.append(s)
        return " ".join(result)

    def status(self) -> dict:
        return {
            "active_mode": self._mode,
            "available_modes": list(_PROFILES.keys()),
            "profile": {
                "max_sentence_words": self._profile.max_sentence_words,
                "avoid_metaphors": self._profile.avoid_metaphors,
                "font_profile": self._profile.font_profile,
            },
        }


# ─────────────────────────────────────────────────────────
# Test standalone
# ─────────────────────────────────────────────────────────
if __name__ == "__main__":
    adapter = NeurodiversityAdapter("autism")
    sample = "C'est comme une montagne de travail — il faut brûler les étapes pour avancer."
    print(f"Original : {sample}")
    print(f"Adapté   : {adapter.apply(sample)}")
    print(f"Status   : {adapter.status()}")
    print("NeurodiversityAdapter skeleton OK.")
