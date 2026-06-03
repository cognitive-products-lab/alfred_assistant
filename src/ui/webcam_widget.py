"""
PROJECT      : ALFRED
BLOCK        : B01 — Interaction & Présence / B04 Vision
FILE         : src/ui/webcam_widget.py
ROLE         : Widget Kivy flux webcam — miniature overlay temps réel

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-06-01
UPDATED      : 2026-06-03 (fix pos_hint renderer dans WebcamOverlay)
VERSION      : V1.1
STATUS       : STABLE

DESCRIPTION :
Overlay webcam léger, affiché dans le coin inférieur-droit de l'AvatarRenderer.
Capture les frames via CameraManager (B04) dans un thread daemon,
les convertit en texture Kivy (BGR→RGB + flip vertical) et les affiche à ~10 fps.

Intégration :
  - Utilisé par alfred_app.py via WebcamOverlay (FloatLayout wrappant AvatarRenderer)
  - Activé / désactivé par le bouton 📷 Caméra de ControlBar
  - Fonctionne sans caméra (masqué avec message d'erreur)

Dépendances :
  pip install opencv-python-headless numpy
  (kivy déjà présent)
"""

from __future__ import annotations

import threading
import time
from typing import Optional

# ── Imports conditionnels ─────────────────────────────────
try:
    import numpy as np
    _NP_OK = True
except ImportError:
    _NP_OK = False

try:
    import cv2
    _CV2_OK = True
except ImportError:
    _CV2_OK = False

from kivy.clock import Clock
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.graphics.texture import Texture
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.widget import Widget


# ─────────────────────────────────────────────────────────
# Configuration
# ─────────────────────────────────────────────────────────

_CAM_FPS        = 10          # images/seconde capturées
_THUMB_W        = 120         # largeur thumbnail (px)
_THUMB_H        = 90          # hauteur thumbnail (px)
_THUMB_MARGIN   = 8           # marge bord droit/bas (dp)
_CORNER_RADIUS  = 6
_BORDER_COLOR   = (0.54, 0.62, 0.83, 0.85)   # bleu ALFRED
_BG_COLOR       = (0.02, 0.02, 0.06, 0.92)


class WebcamWidget(Widget):
    """
    Widget qui affiche un flux webcam en miniature.

    Usage::

        cam = WebcamWidget(size=(120, 90), pos=(x, y))
        layout.add_widget(cam)
        cam.start()
        # …
        cam.stop()
    """

    def __init__(self, camera_index: int = 0, **kwargs: object) -> None:
        kwargs.setdefault("size", (_THUMB_W, _THUMB_H))
        kwargs.setdefault("size_hint", (None, None))
        super().__init__(**kwargs)

        self._cam_index  = camera_index
        self._cap        = None       # cv2.VideoCapture
        self._running    = False
        self._thread: Optional[threading.Thread] = None
        self._lock       = threading.Lock()
        self._latest_rgb: Optional[bytes] = None
        self._frame_size = (0, 0)     # (w, h) de la dernière frame
        self._texture: Optional[Texture] = None

        # ── Canvas ────────────────────────────────────────
        with self.canvas:
            # Fond opaque
            Color(*_BG_COLOR)
            self._bg_rect = Rectangle(pos=self.pos, size=self.size)
            # Texture vidéo
            Color(1, 1, 1, 1)
            self._vid_rect = Rectangle(pos=self.pos, size=self.size)

        self.bind(pos=self._update_canvas, size=self._update_canvas)

        # Label "Pas de caméra"
        self._no_cam_lbl = Label(
            text="[color=6688cc]📷[/color]\npas de caméra",
            markup=True,
            font_size="11sp",
            color=(0.55, 0.55, 0.65, 1),
            halign="center",
            valign="middle",
            size_hint=(None, None),
            size=self.size,
            pos=self.pos,
        )
        self.add_widget(self._no_cam_lbl)

        # Rafraîchissement texture depuis thread captur
        Clock.schedule_interval(self._push_texture, 1.0 / _CAM_FPS)

    # ── Cycle de vie ──────────────────────────────────────

    def start(self) -> bool:
        """Démarre la capture. Retourne True si caméra disponible."""
        if not _CV2_OK or not _NP_OK:
            return False
        if self._running:
            return True
        cap = cv2.VideoCapture(self._cam_index)
        if not cap.isOpened():
            cap.release()
            return False
        cap.set(cv2.CAP_PROP_FRAME_WIDTH,  _THUMB_W * 2)   # capture native plus large
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, _THUMB_H * 2)
        self._cap     = cap
        self._running = True

        self._thread = threading.Thread(target=self._capture_loop, daemon=True)
        self._thread.start()

        self._no_cam_lbl.opacity = 0
        return True

    def stop(self) -> None:
        """Arrête la capture et libère la caméra."""
        self._running = False
        if self._cap is not None:
            try:
                self._cap.release()
            except Exception:
                pass
            self._cap = None
        self._no_cam_lbl.opacity = 1
        self._vid_rect.texture   = None
        self._latest_rgb         = None

    @property
    def is_active(self) -> bool:
        return self._running

    # ── Thread de capture ─────────────────────────────────

    def _capture_loop(self) -> None:
        interval = 1.0 / _CAM_FPS
        while self._running and self._cap is not None:
            t0 = time.monotonic()
            try:
                ret, frame = self._cap.read()
                if not ret or frame is None:
                    time.sleep(0.05)
                    continue
                # Redimensionner + BGR→RGB + flip vertical (origine Kivy = bas-gauche)
                frame = cv2.resize(frame, (_THUMB_W, _THUMB_H), interpolation=cv2.INTER_LINEAR)
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame_rgb = np.flipud(frame_rgb)   # flip pour Kivy
                data = frame_rgb.tobytes()
                with self._lock:
                    self._latest_rgb = data
                    self._frame_size = (_THUMB_W, _THUMB_H)
            except Exception:
                time.sleep(0.1)
                continue
            elapsed = time.monotonic() - t0
            wait    = max(0.0, interval - elapsed)
            if wait > 0:
                time.sleep(wait)

    # ── Push texture (thread principal Kivy) ──────────────

    def _push_texture(self, dt: float) -> None:
        """Appelé par Clock — met à jour la texture Kivy depuis le thread Kivy."""
        if not self._running:
            return
        with self._lock:
            data  = self._latest_rgb
            fsize = self._frame_size

        if data is None or fsize[0] == 0:
            return

        w, h = fsize
        if self._texture is None or self._texture.size != (w, h):
            self._texture = Texture.create(size=(w, h), colorfmt="rgb")
            self._texture.flip_vertical = False

        self._texture.blit_buffer(data, colorfmt="rgb", bufferfmt="ubyte")
        self._vid_rect.texture = self._texture

    # ── Mise à jour canvas ────────────────────────────────

    def _update_canvas(self, *_: object) -> None:
        self._bg_rect.pos  = self.pos
        self._bg_rect.size = self.size
        self._vid_rect.pos = self.pos
        self._vid_rect.size = self.size
        self._no_cam_lbl.pos  = self.pos
        self._no_cam_lbl.size = self.size


# ─────────────────────────────────────────────────────────
# Overlay FloatLayout — wrapper d'AvatarRenderer
# ─────────────────────────────────────────────────────────

class WebcamOverlay(FloatLayout):
    """
    FloatLayout qui contient l'AvatarRenderer + la miniature WebcamWidget.

    La miniature est positionnée en bas à droite et suit les redimensionnements.

    Usage dans AlfredLayout::

        self.avatar_area = WebcamOverlay(
            renderer=AvatarRenderer(...),
            size_hint=(1, 0.47),
        )
    """

    def __init__(self, renderer: Widget, **kwargs: object) -> None:
        super().__init__(**kwargs)

        self._renderer = renderer
        renderer.size_hint = (1, 1)
        # pos_hint indispensable : sans lui FloatLayout ne repositionne pas le renderer
        # → renderer.pos reste (0,0) même si WebcamOverlay est au milieu du BoxLayout.
        renderer.pos_hint = {"x": 0, "y": 0}
        self.add_widget(renderer)

        # Widget webcam positionné en bas à droite
        self._cam_widget = WebcamWidget(
            size=(_THUMB_W, _THUMB_H),
            size_hint=(None, None),
        )
        self._cam_widget.opacity = 0   # caché jusqu'à activation
        self.add_widget(self._cam_widget)

        self.bind(pos=self._reposition, size=self._reposition)

    def _reposition(self, *_: object) -> None:
        """Repositionne le thumbnail en bas à droite."""
        x = self.x + self.width  - _THUMB_W - _THUMB_MARGIN
        y = self.y + _THUMB_MARGIN
        self._cam_widget.pos = (x, y)

    # ── API publique ──────────────────────────────────────

    def toggle_camera(self) -> bool:
        """
        Active / désactive la miniature webcam.

        Returns:
            True si la caméra est maintenant active, False sinon.
        """
        if self._cam_widget.is_active:
            self._cam_widget.stop()
            self._cam_widget.opacity = 0
            return False
        else:
            ok = self._cam_widget.start()
            self._cam_widget.opacity = 1 if ok else 0
            return ok

    @property
    def camera_active(self) -> bool:
        return self._cam_widget.is_active

    def stop_camera(self) -> None:
        self._cam_widget.stop()
        self._cam_widget.opacity = 0
