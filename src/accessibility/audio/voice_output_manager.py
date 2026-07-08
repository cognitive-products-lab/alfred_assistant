"""
════════════════════════════════════════════════════════════
PROJECT      : ALFRED
BLOCK        : B22
FUNCTION     : 22.11
FILE         : voice_output_manager.py
ROLE         : Gestion du ton, rythme & voix — paramètres adaptatifs pour le TTS

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-05-22
UPDATED      : 2026-05-22
VERSION      : V1.0
UPDATED      : 2026-06-01
VERSION      : V1.1
STATUS       : VALIDATED

DEPENDENCIES :
- logging
- dataclasses
- typing

SECURITY :
- Local-first
- Security by Design

DESCRIPTION :
Adapte les paramètres du TTS Piper (rate, volume, pitch, pauses) selon l'état
émotionnel détecté (regulation/) et le profil AccessibilityProfile.
Fournit 6 presets prédéfinis : neutral, calm, clear, informative, alert, bedtime.
════════════════════════════════════════════════════════════
"""

# ============================================================
# ALFRED — VoiceOutputManager
# 22.11 Gestion du ton, rythme & voix
#
# Adapte les paramètres du TTS Piper selon :
# - l'état émotionnel détecté (regulation/)
# - le profil d'accessibilité (AccessibilityProfile)
# - le contexte de la réponse (informatif, réconfortant, alerte)
#
# Ne gère PAS la synthèse vocale elle-même — délègue à tts_piper.py.
# ============================================================

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Optional

logger = logging.getLogger(__name__)


# ── Preset voix ───────────────────────────────────────────

@dataclass
class VoicePreset:
    """Paramètres d'un preset de voix."""
    name: str
    rate: float          # 0.5 → 2.0
    volume: float        # 0.0 → 1.0
    pitch: float         # -10 → +10 semitones (si supporté)
    pause_factor: float  # multiplicateur de pauses (1.0 = normal)
    description: str = ""


# Presets prédéfinis
PRESETS: dict[str, VoicePreset] = {
    "neutral": VoicePreset("neutral", rate=1.0, volume=0.85, pitch=0.0, pause_factor=1.0,
                           description="Voix neutre, conversation normale"),
    "calm": VoicePreset("calm", rate=0.85, volume=0.75, pitch=-1.0, pause_factor=1.3,
                        description="Voix calme, pour états de stress ou fatigue"),
    "clear": VoicePreset("clear", rate=0.9, volume=0.9, pitch=0.0, pause_factor=1.5,
                         description="Diction lente et claire, pour accessibilité renforcée"),
    "informative": VoicePreset("informative", rate=1.0, volume=0.85, pitch=0.5, pause_factor=1.1,
                               description="Voix structurée pour contenu informatif"),
    "alert": VoicePreset("alert", rate=1.1, volume=1.0, pitch=1.0, pause_factor=0.8,
                         description="Voix urgente pour alertes ou rappels importants"),
    "bedtime": VoicePreset("bedtime", rate=0.75, volume=0.6, pitch=-2.0, pause_factor=1.8,
                           description="Voix très douce pour fin de journée"),
}


# ── Mapping état émotionnel → preset ─────────────────────

_EMOTION_PRESET_MAP: dict[str, str] = {
    "neutral":    "neutral",
    "calm":       "calm",
    "happy":      "neutral",
    "excited":    "informative",
    "sad":        "calm",
    "anxious":    "calm",
    "stressed":   "calm",
    "tired":      "clear",
    "alert":      "alert",
    "focused":    "informative",
}


class VoiceOutputManager:
    """
    22.11 Gestion du ton, rythme & voix.

    Maintient le preset actif et l'applique au TTS
    en fonction de l'état émotionnel et du profil utilisateur.
    """

    def __init__(self, tts_engine=None, default_preset: str = "neutral") -> None:
        self._tts = tts_engine
        self._current_preset = PRESETS.get(default_preset, PRESETS["neutral"])
        self._override: Optional[VoicePreset] = None
        self._stats = {"preset_changes": 0, "emotion_adaptations": 0}
        logger.info("VoiceOutputManager initialisé (preset=%s)", default_preset)

    # ── Preset actif ──────────────────────────────────────

    def set_preset(self, preset_name: str) -> VoicePreset:
        """Active un preset nommé."""
        if preset_name not in PRESETS:
            raise ValueError(f"Preset inconnu : {preset_name}. Disponibles : {list(PRESETS)}")
        self._current_preset = PRESETS[preset_name]
        self._override = None
        self._stats["preset_changes"] += 1
        self._apply_to_tts(self._current_preset)
        logger.debug("Preset voix : %s", preset_name)
        return self._current_preset

    def set_custom(self, rate: float, volume: float, pitch: float = 0.0, pause_factor: float = 1.0) -> None:
        """Applique des paramètres personnalisés sans écraser les presets."""
        self._override = VoicePreset(
            name="custom", rate=rate, volume=volume, pitch=pitch, pause_factor=pause_factor
        )
        self._apply_to_tts(self._override)

    def adapt_to_emotion(self, emotion: str) -> VoicePreset:
        """Adapte le preset à l'état émotionnel détecté."""
        preset_name = _EMOTION_PRESET_MAP.get(emotion, "neutral")
        self._stats["emotion_adaptations"] += 1
        return self.set_preset(preset_name)

    def adapt_to_profile(self, rate: float, volume: float) -> None:
        """Applique les préférences du profil AccessibilityProfile."""
        # Merge avec le preset actif : les préférences utilisateur priment
        preset = self.active_preset
        merged = VoicePreset(
            name="profile_merged",
            rate=rate,
            volume=volume,
            pitch=preset.pitch,
            pause_factor=preset.pause_factor,
        )
        self._override = merged
        self._apply_to_tts(merged)

    def reset(self) -> None:
        """Revient au preset actif (annule les overrides)."""
        self._override = None
        self._apply_to_tts(self._current_preset)

    # ── Preset courant ────────────────────────────────────

    @property
    def active_preset(self) -> VoicePreset:
        return self._override or self._current_preset

    # ── Application au TTS ───────────────────────────────

    def _apply_to_tts(self, preset: VoicePreset) -> None:
        """Envoie les paramètres au moteur TTS (gracieux si TTS absent)."""
        if self._tts is None:
            return
        try:
            if hasattr(self._tts, "set_rate"):
                self._tts.set_rate(max(0.5, min(2.0, preset.rate)))
            if hasattr(self._tts, "set_volume"):
                self._tts.set_volume(max(0.0, min(1.0, preset.volume)))
        except Exception as exc:
            logger.warning("VoiceOutputManager: impossible d'appliquer le preset TTS — %s", exc)

    # ── Diagnostic ────────────────────────────────────────

    def list_presets(self) -> list[dict]:
        return [
            {"name": p.name, "rate": p.rate, "volume": p.volume, "description": p.description}
            for p in PRESETS.values()
        ]

    def status(self) -> dict:
        preset = self.active_preset
        return {
            "tts_connected": self._tts is not None,
            "active_preset": preset.name,
            "rate": preset.rate,
            "volume": preset.volume,
            "pitch": preset.pitch,
            "pause_factor": preset.pause_factor,
            "override_active": self._override is not None,
            "stats": self._stats,
        }


# ─────────────────────────────────────────────────────────
# Test standalone
# ─────────────────────────────────────────────────────────
if __name__ == "__main__":
    vom = VoiceOutputManager()
    print(f"Status : {vom.status()}")
    print(f"Presets : {[p['name'] for p in vom.list_presets()]}")
    adapted = vom._current_preset  # accès direct sans TTS pour test
    print(f"Preset neutre : rate={adapted.rate}, volume={adapted.volume}")
    print("VoiceOutputManager skeleton OK.")
