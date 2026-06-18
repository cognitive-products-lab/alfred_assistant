"""
PROJECT      : ALFRED
BLOCK        : B15 -- Avatar & Interface
FILE         : src/ui/sound_wave.py
ROLE         : Widget Kivy de visualisation audio (barres animees)

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-05-15
VERSION      : V1.0
STATUS       : STABLE

DESCRIPTION :
SoundWaveWidget : barre de visualisation audio animee.
- Actif (speaking / ecoute microphone) : barres verticales pulsantes
- Inactif : ligne plate subtile

Compatible headless : stub muet si Kivy absent.
"""

from __future__ import annotations

import math
import random
from typing import Optional

# ============================================================
# Constantes visuelles
# ============================================================

_N_BARS     = 24          # nombre de barres
_FPS        = 30          # refresh animation
_CLR_ALFRED = (0.54, 0.62, 0.83)   # bleu ALFRED (speaking)
_CLR_MIC    = (0.36, 0.82, 0.56)   # vert (écoute microphone)
_CLR_IDLE   = (0.14, 0.14, 0.22)   # gris sombre (inactif)


# ============================================================
# Widget Kivy
# ============================================================

try:
    from kivy.uix.widget import Widget
    from kivy.graphics import Color, Rectangle, RoundedRectangle
    from kivy.clock import Clock
    _KIVY_OK = True
except ImportError:
    _KIVY_OK = False


if _KIVY_OK:

    class SoundWaveWidget(Widget):  # type: ignore[misc]
        """
        Visualisation audio ALFRED.

        Usage :
            wave = SoundWaveWidget(size_hint=(1, 1))
            wave.set_speaking(True)   # ALFRED parle -> barres bleues
            wave.set_listening(True)  # microphone  -> barres vertes
            wave.set_idle()           # repos       -> ligne plate
        """

        def __init__(self, **kwargs: object) -> None:
            super().__init__(**kwargs)
            self._mode          = "idle"           # idle | speaking | listening
            self._anim_clock: Optional[object] = None
            self._t             = 0.0
            # Paramètres par barre (generés une fois, fixes)
            self._phases = [random.uniform(0, 2 * math.pi) for _ in range(_N_BARS)]
            self._speeds = [random.uniform(0.7, 2.2)       for _ in range(_N_BARS)]
            self._amps   = [random.uniform(0.6, 1.0)       for _ in range(_N_BARS)]

            self.bind(size=self._draw, pos=self._draw)
            self._draw()

        # --------------------------------------------------------
        # API publique
        # --------------------------------------------------------

        def set_speaking(self, active: bool) -> None:
            """ALFRED parle (TTS actif)."""
            if active:
                self._mode = "speaking"
                self._start_anim()
            else:
                self.set_idle()

        def set_listening(self, active: bool) -> None:
            """Microphone actif (STT ecoute)."""
            if active:
                self._mode = "listening"
                self._start_anim()
            else:
                self.set_idle()

        def set_idle(self) -> None:
            """Repos — ligne plate."""
            self._mode = "idle"
            self._stop_anim()
            self._draw()

        @property
        def is_active(self) -> bool:
            return self._mode != "idle"

        # --------------------------------------------------------
        # Animation
        # --------------------------------------------------------

        def _start_anim(self) -> None:
            if self._anim_clock is None:
                self._anim_clock = Clock.schedule_interval(
                    self._tick, 1 / _FPS
                )

        def _stop_anim(self) -> None:
            if self._anim_clock:
                self._anim_clock.cancel()
                self._anim_clock = None
            self._t = 0.0

        def _tick(self, dt: float) -> None:
            self._t += dt
            self._draw()

        # --------------------------------------------------------
        # Rendu
        # --------------------------------------------------------

        def _draw(self, *_: object) -> None:
            self.canvas.clear()
            w, h = self.width, self.height
            if w < 2 or h < 2:
                return

            bar_w   = max(2, w / (_N_BARS * 1.6))
            spacing = w / _N_BARS

            if self._mode == "speaking":
                base_r, base_g, base_b = _CLR_ALFRED
            elif self._mode == "listening":
                base_r, base_g, base_b = _CLR_MIC
            else:
                base_r, base_g, base_b = _CLR_IDLE

            with self.canvas:
                # Fond
                Color(0.04, 0.04, 0.08, 0.92)
                Rectangle(pos=self.pos, size=self.size)

                for i in range(_N_BARS):
                    x = self.x + i * spacing + (spacing - bar_w) / 2

                    if self._mode == "speaking":
                        # Barres dynamiques larges — ALFRED parle
                        amp   = self._amps[i]
                        phase = self._t * self._speeds[i] * 3.5 + self._phases[i]
                        ratio = (math.sin(phase) * 0.5 + 0.5) * amp
                        bar_h = max(3, h * (0.08 + 0.82 * ratio))
                        alpha = 0.55 + 0.45 * ratio
                    elif self._mode == "listening":
                        # Barres subtiles lentes — microphone actif (pas de parole)
                        phase = self._t * self._speeds[i] * 0.9 + self._phases[i]
                        ratio = (math.sin(phase) * 0.5 + 0.5) * 0.35
                        bar_h = max(3, h * (0.06 + 0.16 * ratio))
                        alpha = 0.20 + 0.15 * ratio
                    else:
                        bar_h = max(3, h * 0.06)
                        alpha = 0.35

                    y = self.y + (h - bar_h) / 2
                    Color(base_r, base_g, base_b, alpha)
                    radius = min(bar_w / 2, bar_h / 2, 4)
                    RoundedRectangle(
                        pos=(x, y),
                        size=(bar_w, bar_h),
                        radius=[radius],
                    )

        # --------------------------------------------------------
        # Statut
        # --------------------------------------------------------

        def status(self) -> dict:
            return {
                "mode":    self._mode,
                "active":  self.is_active,
                "n_bars":  _N_BARS,
                "version": "sound_wave_v1.0",
            }

else:

    class SoundWaveWidget:  # type: ignore[no-redef]
        """Stub muet quand Kivy est absent."""

        def __init__(self, **kwargs: object) -> None:
            self._mode = "idle"

        def set_speaking(self, active: bool) -> None:
            self._mode = "speaking" if active else "idle"

        def set_listening(self, active: bool) -> None:
            self._mode = "listening" if active else "idle"

        def set_idle(self) -> None:
            self._mode = "idle"

        @property
        def is_active(self) -> bool:
            return self._mode != "idle"

        def status(self) -> dict:
            return {"mode": self._mode, "kivy": False}
