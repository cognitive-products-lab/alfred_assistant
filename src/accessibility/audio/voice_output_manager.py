# ============================================================
# ALFRED — src/accessibility/audio/voice_output_manager.py
# Bloc 22.02 — Lecture vocale & restitution audio
#
# 📚 NOTION EXAM :
#   D41-3 — Capsule 3 : Accessibilité, inclusion et adaptation cognitive
#
# 🎯 UTILITÉ ALFRED :
#   Gère la sortie vocale pour le Bloc 22 — applique la vitesse,
#   le ton et la langue choisis par l'utilisateur, puis délègue
#   au moteur TTS existant (src/conversation/output/).
#
# 🔐 BLOC SÉCURITÉ / DOMAINE :
#   Accessibilité & assistance cognitive (22.02)
# ============================================================

from __future__ import annotations

_DEFAULT_SPEED = 1.0
_DEFAULT_TONE = "neutral"
_ALLOWED_TONES = {"neutral", "soft", "motivating", "professional"}


class VoiceOutputManager:
    def __init__(self, speed: float = _DEFAULT_SPEED, tone: str = _DEFAULT_TONE):
        self.speed = max(0.5, min(speed, 2.0))
        self.tone = tone if tone in _ALLOWED_TONES else _DEFAULT_TONE

    def set_speed(self, speed: float) -> None:
        self.speed = max(0.5, min(speed, 2.0))

    def set_tone(self, tone: str) -> None:
        if tone in _ALLOWED_TONES:
            self.tone = tone

    def speak(self, text: str, tts_fn: callable) -> None:
        tts_fn(text, speed=self.speed, tone=self.tone)

    @classmethod
    def from_settings(cls, settings: dict) -> "VoiceOutputManager":
        return cls(
            speed=settings.get("voice_speed", _DEFAULT_SPEED),
            tone=settings.get("voice_tone", _DEFAULT_TONE),
        )
