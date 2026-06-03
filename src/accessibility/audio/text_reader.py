"""
════════════════════════════════════════════════════════════
PROJECT      : ALFRED
BLOCK        : B22
FUNCTION     : 22.02
FILE         : text_reader.py
ROLE         : Lecture vocale & restitution audio — pilote le TTS existant (Piper)

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-05-22
UPDATED      : 2026-05-22
VERSION      : V1.0
UPDATED      : 2026-06-01
VERSION      : V1.1
STATUS       : ACTIVE

DEPENDENCIES :
- logging
- typing

SECURITY :
- Local-first
- Security by Design

DESCRIPTION :
Pont entre le module accessibilité et le moteur TTS Piper déjà utilisé par ALFRED.
Expose une API de lecture adaptative (vitesse, volume, pause entre phrases) sans
dupliquer la logique TTS — délègue à tts_piper.py.
════════════════════════════════════════════════════════════
"""

# ============================================================
# ALFRED — TextReader
# Pont entre le module accessibilité et le TTS Piper existant.
# Ne duplique pas la logique TTS — délègue à tts_piper.py.
# ============================================================

from __future__ import annotations

import logging
import time
from typing import Optional, Callable

logger = logging.getLogger(__name__)


class TextReader:
    """
    22.02 Lecture vocale & restitution audio.

    Pilote le TTS existant (Piper/Coqui) avec paramètres
    d'accessibilité : vitesse, volume, pause entre phrases.
    """

    def __init__(
        self,
        tts_engine=None,
        rate: float = 1.0,
        volume: float = 1.0,
        pause_between_sentences: float = 0.3,
    ) -> None:
        self._tts = tts_engine          # instance de TTSPiper ou compatible
        self.rate = rate
        self.volume = volume
        self.pause_ms = int(pause_between_sentences * 1000)
        self._reading = False
        logger.info("TextReader initialisé (rate=%.1f, volume=%.1f)", rate, volume)

    # ── API principale ────────────────────────────────────

    def read(self, text: str, on_done: Optional[Callable] = None) -> None:
        """
        Lit le texte via TTS (découpage en phrases + pauses).

        Args:
            text    : Texte à lire
            on_done : Callback appelé quand la lecture est terminée
        """
        if not text or not text.strip():
            if on_done:
                on_done()
            return

        self._reading = True
        sentences = self._split_sentences(text)

        try:
            for i, sentence in enumerate(sentences):
                if not self._reading:
                    break
                self.read_sentence(sentence)
                # Pause entre phrases (sauf après la dernière)
                if self.pause_ms > 0 and i < len(sentences) - 1 and self._reading:
                    time.sleep(self.pause_ms / 1000.0)
        finally:
            self._reading = False
            if on_done:
                on_done()

    def read_sentence(self, sentence: str) -> None:
        """Lit une phrase unique via le moteur TTS connecté."""
        if not sentence.strip():
            return
        if self._tts is None:
            # Mode headless : log la phrase sans TTS
            logger.debug("TextReader [headless]: %s", sentence)
            return
        try:
            # Compatible tts_piper.py (speak) et tts_output.py (output)
            if hasattr(self._tts, "speak"):
                self._tts.speak(sentence)
            elif hasattr(self._tts, "output"):
                self._tts.output(sentence)
            else:
                logger.warning("TextReader: moteur TTS incompatible (pas de speak/output)")
        except Exception as exc:
            logger.error("TextReader.read_sentence: %s", exc)

    def stop(self) -> None:
        """Interrompt la lecture en cours."""
        self._reading = False
        if self._tts and hasattr(self._tts, "stop"):
            try:
                self._tts.stop()
            except Exception:
                pass

    def _split_sentences(self, text: str) -> list[str]:
        """Découpe le texte en phrases pour la lecture adaptative."""
        import re
        sentences = re.split(r"(?<=[.!?])\s+", text)
        return [s.strip() for s in sentences if s.strip()]

    def is_reading(self) -> bool:
        return self._reading

    # ── Paramètres dynamiques ─────────────────────────────

    def set_rate(self, rate: float) -> None:
        """Vitesse de lecture : 0.5 (lent) → 2.0 (rapide)."""
        self.rate = max(0.5, min(2.0, rate))

    def set_volume(self, volume: float) -> None:
        """Volume : 0.0 → 1.0."""
        self.volume = max(0.0, min(1.0, volume))

    def set_pause(self, seconds: float) -> None:
        """Pause entre phrases en secondes."""
        self.pause_ms = int(max(0.0, seconds) * 1000)

    # ── Diagnostic ────────────────────────────────────────

    def status(self) -> dict:
        return {
            "tts_connected": self._tts is not None,
            "rate": self.rate,
            "volume": self.volume,
            "pause_ms": self.pause_ms,
            "reading": self._reading,
        }


# ─────────────────────────────────────────────────────────
# Test standalone
# ─────────────────────────────────────────────────────────
if __name__ == "__main__":
    reader = TextReader(rate=0.9, volume=0.8)
    print(f"Status : {reader.status()}")
    print("TextReader skeleton OK.")
