"""
PROJECT      : ALFRED
BLOCK        : B15 -- Avatar & Interface
FUNCTION     : 15.02.001 -> 15.02.009
FILE         : src/ui/avatar_renderer.py
ROLE         : Renderer Kivy de l'avatar ALFRED -- sprites PNG + backgrounds + animations

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-05-14
UPDATED      : 2026-06-01 (V1.3 — fix position FloatLayout pos_hint, overflow zone, blink thinking)
VERSION      : V1.3
STATUS       : STABLE

DESCRIPTION :
Renderer visuel Kivy pour l'avatar ALFRED.
Implemente le contrat update_state(state_name) de AvatarController.

Architecture 6 calques :
  1. Background PNG (interieur/exterieur selon lieu + periode)
  2. Overlay sombre semi-transparent (lisibilite avatar)
  3. Halo glow colore (anime, ellipse positionnee sur avatar)
  4. Sprite PNG avatar (mouth + eyes)
  5. Label etat
  (6. Reserve -- overlay emotion V2)

Compatible headless : si Kivy absent, AvatarRenderer est un stub muet.
"""

from __future__ import annotations

import math
from pathlib import Path
from typing import Optional, Tuple


# ============================================================
# Chemins assets
# ============================================================

# Sprites base_normal (mouth+eyes) — utilisés pour l'animation bouche speaking
_ASSET_BASE = (
    Path(__file__).resolve().parents[2]
    / "assets" / "avatars" / "avatar_normal" / "base_normal"
)
_SPRITE_EXT = ".png.png"

# Sprites expressifs medium — priorité sur base_normal pour états non-animés
_ASSET_MEDIUM = (
    Path(__file__).resolve().parents[2]
    / "assets" / "avatars" / "avatar_medium" / "base_medium"
)

# Correspondance état → fichier PNG medium
_MEDIUM_SPRITES: dict[str, str] = {
    "idle":       "alfred_medium_neutral.png",   # working.png a un fond blanc — TODO: fix PNG
    "listening":  "alfred_medium_listening.png",
    "thinking":   "alfred_medium_thinking.png",
    "speaking":   "alfred_medium_explaining.png",
    "support":    "alfred_medium_love.png",
    "focus":      "alfred_medium_neutral.png",   # idem
    "challenge":  "alfred_medium_excited.png",
    "complicite": "alfred_medium_very_excited.png",
    "error":      "alfred_medium_cybersecurity.png",
    "offline":    "alfred_medium_neutral.png",
}


# ============================================================
# Tables de correspondance etat -> visuel (base_normal fallback)
# ============================================================

_STATE_SPRITE: dict[str, Tuple[str, str]] = {
    "idle":       ("idle", "half"),
    "listening":  ("idle", "open"),
    "thinking":   ("idle", "half"),
    "speaking":   ("a",    "open"),
    "support":    ("idle", "open"),
    "focus":      ("idle", "half"),
    "challenge":  ("idle", "open"),
    "complicite": ("idle", "open"),
    "error":      ("idle", "half"),
    "offline":    ("idle", "closed"),
}

# Frames animation bouche speaking — sprites medium expressifs
_SPEAKING_MEDIUM_FRAMES: list[str] = [
    "alfred_medium_neutral_a.png",
    "alfred_medium_neutral_e.png",
    "alfred_medium_neutral_i.png",
    "alfred_medium_neutral_o.png",
    "alfred_medium_neutral_u.png",
    "alfred_medium_neutral_m.png",
]

# Fallback base_normal si les fichiers medium sont absents
_SPEAKING_FRAMES_FALLBACK: list[Tuple[str, str]] = [
    ("a",    "open"),
    ("m",    "open"),
    ("o",    "open"),
    ("idle", "open"),
]

# Alias pour compatibilité (les tests importent _SPEAKING_FRAMES)
_SPEAKING_FRAMES = _SPEAKING_FRAMES_FALLBACK

_STATE_COLOR_HEX: dict[str, str] = {
    "idle":       "#8B9FD4",
    "listening":  "#5BC8F5",
    "thinking":   "#F5A623",
    "speaking":   "#7ED321",
    "support":    "#E8A87C",
    "focus":      "#4A90D9",
    "challenge":  "#F5A623",
    "complicite": "#7ED321",
    "error":      "#D0021B",
    "offline":    "#666666",
}

_STATE_ANIM: dict[str, Tuple[str, float]] = {
    "idle":       ("breathe", 3.0),
    "listening":  ("pulse",   0.8),
    "thinking":   ("pulse",   2.0),
    "speaking":   ("mouth",   0.12),
    "support":    ("breathe", 3.0),
    "focus":      ("static",  0.0),
    "challenge":  ("pulse",   0.4),
    "complicite": ("breathe", 4.0),
    "error":      ("flash",   0.25),
    "offline":    ("static",  0.0),
}

# Layout par état : (scale_hauteur, y_offset_fraction)
# scale × renderer.height = hauteur du widget avatar
# y_offset × renderer.height ajouté à renderer.y pour le positionnement bas
#
# Règle : scale + y_offset <= 1.0 → aucun débordement sous la zone
#         y_offset >= 0            → aucun débordement au-dessus du bas de zone
#
# Valeurs 1.0 / 0.0 : widget = zone exacte, zéro overflow.
# Les sprites medium (fit_mode="fill") s'étendent au widget complet sans bandes.
_STATE_LAYOUT: dict[str, Tuple[float, float]] = {
    # (scale, y_offset)
    "idle":       (1.0, 0.0),
    "thinking":   (1.0, 0.0),
    "speaking":   (1.0, 0.0),
    "listening":  (1.0, 0.0),
    "support":    (1.0, 0.0),
    "focus":      (1.0, 0.0),
    "challenge":  (1.0, 0.0),
    "complicite": (1.0, 0.0),
    "error":      (1.0, 0.0),
    "offline":    (1.0, 0.0),
}


# ============================================================
# Utilitaires
# ============================================================

def _hex_to_rgb(hex_color: str) -> Tuple[float, float, float]:
    """Convertit #RRGGBB en (r, g, b) float 0.0-1.0."""
    h = hex_color.lstrip("#")
    return tuple(int(h[i:i+2], 16) / 255.0 for i in (0, 2, 4))  # type: ignore[return-value]


def _sprite_path(mouth: str, eyes: str) -> str:
    """Retourne le chemin absolu du sprite PNG."""
    return str(_ASSET_BASE / f"avatar_mouth_{mouth}_eyes_{eyes}{_SPRITE_EXT}")


# ============================================================
# Logique pure -- testable sans Kivy
# ============================================================

class AvatarRendererLogic:
    """
    Logique sprite/couleur/animation -- pure Python, sans dependance Kivy.

    Testable directement depuis pytest.
    """

    def __init__(self) -> None:
        self._state:        str = "idle"
        self._speaking_idx: int = 0

    def get_sprite(self, state_name: str = "") -> str:
        """Retourne le sprite pour l'état donné.
        Priorité : medium expressif > base_normal fallback.
        Ne pas appeler pour speaking (utiliser get_speaking_frame)."""
        name = state_name or self._state
        medium_file = _MEDIUM_SPRITES.get(name)
        if medium_file:
            medium_path = str(_ASSET_MEDIUM / medium_file)
            if Path(medium_path).exists():
                return medium_path
        # Fallback base_normal
        mouth, eyes = _STATE_SPRITE.get(name, ("idle", "half"))
        return _sprite_path(mouth, eyes)

    def get_speaking_frame(self) -> str:
        idx = self._speaking_idx % len(_SPEAKING_MEDIUM_FRAMES)
        path = str(_ASSET_MEDIUM / _SPEAKING_MEDIUM_FRAMES[idx])
        if Path(path).exists():
            return path
        # Fallback base_normal
        fi = idx % len(_SPEAKING_FRAMES_FALLBACK)
        mouth, eyes = _SPEAKING_FRAMES_FALLBACK[fi]
        return _sprite_path(mouth, eyes)

    def next_speaking_frame(self) -> str:
        self._speaking_idx = (self._speaking_idx + 1) % len(_SPEAKING_MEDIUM_FRAMES)
        return self.get_speaking_frame()

    def sprite_exists(self, state_name: str = "") -> bool:
        return Path(self.get_sprite(state_name)).exists()

    def get_color_hex(self, state_name: str = "") -> str:
        name = state_name or self._state
        return _STATE_COLOR_HEX.get(name, "#8B9FD4")

    def get_color_rgb(self, state_name: str = "") -> Tuple[float, float, float]:
        return _hex_to_rgb(self.get_color_hex(state_name))

    def get_anim(self, state_name: str = "") -> Tuple[str, float]:
        name = state_name or self._state
        return _STATE_ANIM.get(name, ("static", 0.0))

    def set_state(self, state_name: str) -> None:
        self._state = state_name
        if state_name != "speaking":
            self._speaking_idx = 0

    @property
    def state(self) -> str:
        return self._state

    @property
    def is_speaking(self) -> bool:
        return self._state == "speaking"

    def all_sprites_exist(self) -> dict[str, bool]:
        result = {}
        for name in _STATE_SPRITE:
            if name == "speaking":
                # speaking utilise les frames base_normal
                result[name] = all(
                    Path(_sprite_path(m, e)).exists() for m, e in _SPEAKING_FRAMES
                )
            else:
                result[name] = Path(self.get_sprite(name)).exists()
        return result


# ============================================================
# Widget Kivy -- 6 calques
# ============================================================

try:
    from kivy.uix.floatlayout import FloatLayout
    from kivy.uix.image import Image as KivyImage
    from kivy.uix.label import Label
    from kivy.graphics import Color, Ellipse, Rectangle
    from kivy.clock import Clock
    from kivy.core.window import Window
    from kivy.core.image import Image as CoreImage
    _KIVY_OK = True
except ImportError:
    _KIVY_OK = False


if _KIVY_OK:

    class AvatarRenderer(FloatLayout):  # type: ignore[misc]
        """
        Renderer Kivy 6 calques pour l'avatar ALFRED.

        Calques (bas -> haut) :
          1. Background PNG (KivyImage plein ecran)
          2. Overlay sombre (canvas.before, Rectangle semi-transparent)
          3. Halo glow anime (canvas.before, Ellipse coloree)
          4. Sprite avatar PNG (KivyImage centree)
          5. Label etat
          (6. Reserve V2)

        Contrat AvatarController :
            renderer.update_state(state_name: str)
            renderer.update_background(path: str)   # optionnel
        """

        def __init__(self, **kwargs: object) -> None:
            super().__init__(**kwargs)
            self._logic       = AvatarRendererLogic()
            self._glow_alpha  = 0.18
            self._anim_clock  = None
            self._anim_time   = 0.0
            self._bg_path     = ""
            self._speaking_textures: list = []   # textures pré-chargées (pas de reload)
            self._speaking_tex_idx: int = 0

            # Blink automatique
            self._blink_clock       = None
            self._blink_tex_open    = None   # texture yeux ouverts (cache)
            self._blink_active      = False  # True pendant la séquence blink

            Window.clearcolor = (0.06, 0.06, 0.10, 1)

            self._build_layers()
            self._preload_speaking_textures()
            # size ET pos déclenchent le recalcul du sprite (position absolue)
            self.bind(size=self._on_renderer_resize, pos=self._on_renderer_resize)
            Clock.schedule_once(lambda dt: self._apply_state("idle"), 0.1)
            self._schedule_blink()

        # --------------------------------------------------------
        # Construction des calques
        # --------------------------------------------------------

        # Ratio natif des sprites avatar (1024 × 1536 px)
        _IMG_RATIO: float = 1024 / 1536   # ≈ 0.667 (largeur / hauteur)

        def _build_layers(self) -> None:
            # Calque 4 -- sprite avatar
            # size_hint=(None, None) : taille calculée depuis la hauteur du renderer
            # → hauteur maximale quelle que soit la largeur de fenêtre.
            # center_x=0.70 : avatar dans le tiers droit, TOUJOURS visible
            # (contrairement à right=1.02 qui place le bord à 102% de la largeur —
            #  hors champ sur les fenêtres larges).
            # pos_hint retiré volontairement : le FloatLayout calcule pos_hint
            # quand self.y=0 (avant positionnement BoxLayout) → avatar mal placé.
            # Position calculée directement dans _sync_avatar_size via self.x/self.y.
            self._avatar_img = KivyImage(
                source="",
                fit_mode="fill",
                size_hint=(None, None),
            )
            self.add_widget(self._avatar_img)
            # Pas de _sync ici : self.height=1 tant que le renderer n'est pas dimensionné.

            # Calque 5 -- label etat (bas gauche)
            self._lbl = Label(
                text="",
                font_size="11sp",
                color=(0.90, 0.90, 0.90, 0.65),
                size_hint=(0.45, 0.07),
                pos_hint={"x": 0.02, "y": 0.02},
                halign="left",
                valign="middle",
            )
            self.add_widget(self._lbl)

        def _preload_speaking_textures(self) -> None:
            """Charge toutes les textures speaking en mémoire pour éviter le flash noir."""
            self._speaking_textures = []
            for fname in _SPEAKING_MEDIUM_FRAMES:
                path = str(_ASSET_MEDIUM / fname)
                try:
                    if Path(path).exists():
                        ci = CoreImage(path, nocache=True)
                        self._speaking_textures.append(ci.texture)
                except Exception:
                    pass
            # Fallback base_normal si aucune texture medium chargée
            if not self._speaking_textures:
                for mouth, eyes in _SPEAKING_FRAMES_FALLBACK:
                    path = _sprite_path(mouth, eyes)
                    try:
                        if Path(path).exists():
                            ci = CoreImage(path, nocache=True)
                            self._speaking_textures.append(ci.texture)
                    except Exception:
                        pass

        # --------------------------------------------------------
        # Canvas (calques 1 + 2 + 3)
        # --------------------------------------------------------

        def _redraw_canvas(self, *_: object) -> None:
            """Redessine fond (cal. 1), overlay sombre (cal. 1b) et halo glow (cal. 2)."""
            self.canvas.before.clear()
            r, g, b = self._logic.get_color_rgb()
            cx = self.x + self.width  * 0.78
            cy = self.y + self.height * 0.35
            glow_d = min(self.width, self.height) * 0.68

            with self.canvas.before:
                if self._bg_path and Path(self._bg_path).exists():
                    # Calque 1 -- fond PNG (stretch simple, pas de stencil en V1)
                    Color(1, 1, 1, 1)
                    Rectangle(source=self._bg_path, pos=self.pos, size=self.size)
                    # Calque 1b -- overlay sombre pour lisibilite avatar
                    Color(0.04, 0.04, 0.08, 0.55)
                    Rectangle(pos=self.pos, size=self.size)
                else:
                    # Fallback couleur sombre si pas de fond image
                    Color(0.06, 0.06, 0.10, 1)
                    Rectangle(pos=self.pos, size=self.size)

                # Calque 2 -- halo glow anime
                Color(r, g, b, self._glow_alpha)
                Ellipse(
                    pos=(cx - glow_d / 2, cy - glow_d / 2),
                    size=(glow_d, glow_d),
                )

        # --------------------------------------------------------
        # API publique
        # --------------------------------------------------------

        def update_state(self, state_name: str) -> None:
            """Appele par AvatarController a chaque transition."""
            Clock.schedule_once(lambda dt: self._apply_state(state_name))

        def update_background(self, path: str) -> None:
            """Met a jour le fond PNG et redessine le canvas."""
            self._bg_path = path
            Clock.schedule_once(lambda dt: self._redraw_canvas())

        # --------------------------------------------------------
        # Application etat
        # --------------------------------------------------------

        def _apply_state(self, state_name: str) -> None:
            self._logic.set_state(state_name)
            self._stop_anim()

            sprite = (
                self._logic.get_speaking_frame()
                if state_name == "speaking"
                else self._logic.get_sprite(state_name)
            )
            self._load_avatar(sprite)
            self._apply_layout(state_name)
            self._lbl.text = state_name
            self._redraw_canvas()

            anim_type, period = self._logic.get_anim(state_name)
            self._start_anim(anim_type, period)

        def _sync_avatar_size(self, *_) -> None:
            """
            Calcule taille ET position du sprite depuis les dimensions courantes du renderer.

            Hauteur  = sh × renderer.height
            Largeur  = hauteur × _IMG_RATIO  (1024/1536 ≈ 0.667)
            center_x = renderer.x + 0.70 × renderer.width  (tiers droit, toujours visible)
            y        = renderer.y + y_correction × renderer.height  (alignement bas)

            Calcul direct via self.x/self.y → pas de dépendance au timing du FloatLayout.
            """
            if self.height <= 1:      # renderer pas encore dimensionné
                return
            sh, y_corr = _STATE_LAYOUT.get(self._logic.state, (1.05, -0.07))
            h = self.height * sh
            w = h * self._IMG_RATIO
            self._avatar_img.size = (w, h)
            self._avatar_img.center_x = self.x + 0.70 * self.width
            self._avatar_img.y       = self.y + y_corr * self.height

        def _apply_layout(self, state_name: str) -> None:
            """Déclenche le recalcul taille+position pour l'état donné."""
            self._sync_avatar_size()

        def _on_renderer_resize(self, *_) -> None:
            """Appelé sur resize OU repositionnement du renderer."""
            self._redraw_canvas()
            self._sync_avatar_size()

        def _load_avatar(self, path: str) -> None:
            """Charge un sprite via texture directe — sans flash noir (pas de reload)."""
            if Path(path).exists():
                try:
                    ci = CoreImage(path, nocache=True)
                    self._avatar_img.texture = ci.texture
                except Exception:
                    # Fallback source+reload si CoreImage échoue
                    self._avatar_img.source = path
                    self._avatar_img.reload()

        # --------------------------------------------------------
        # Animations
        # --------------------------------------------------------

        def _stop_anim(self) -> None:
            if self._anim_clock:
                self._anim_clock.cancel()
                self._anim_clock = None
            self._anim_time = 0.0

        def _start_anim(self, anim_type: str, period: float) -> None:
            if anim_type == "mouth":
                self._anim_clock = Clock.schedule_interval(
                    self._tick_mouth, period
                )
            elif anim_type == "breathe":
                self._anim_clock = Clock.schedule_interval(
                    lambda dt: self._tick_glow(dt, period, lo=0.08, hi=0.28),
                    1 / 30,
                )
            elif anim_type == "pulse":
                self._anim_clock = Clock.schedule_interval(
                    lambda dt: self._tick_glow(dt, period, lo=0.05, hi=0.44),
                    1 / 30,
                )
            elif anim_type == "flash":
                self._anim_clock = Clock.schedule_interval(
                    lambda dt: self._tick_glow(dt, period, lo=0.03, hi=0.58),
                    1 / 30,
                )

        def _tick_glow(self, dt: float, period: float, lo: float, hi: float) -> None:
            self._anim_time += dt
            phase = math.sin(2 * math.pi * self._anim_time / max(period, 0.01))
            self._glow_alpha = lo + (hi - lo) * (phase * 0.5 + 0.5)
            self._redraw_canvas()

        def _tick_mouth(self, dt: float) -> None:
            if self._speaking_textures:
                # Swap texture directement — zéro reload, zéro flash noir
                self._avatar_img.texture = self._speaking_textures[self._speaking_tex_idx]
                self._speaking_tex_idx = (self._speaking_tex_idx + 1) % len(self._speaking_textures)
            else:
                self._load_avatar(self._logic.next_speaking_frame())

        # --------------------------------------------------------
        # Blink automatique (3-6 secondes, 150 ms)
        # --------------------------------------------------------

        def _schedule_blink(self) -> None:
            """Planifie le prochain blink dans 3-6 secondes."""
            import random
            delay = random.uniform(3.0, 6.0)
            self._blink_clock = Clock.schedule_once(self._do_blink, delay)

        def _do_blink(self, dt: float = 0) -> None:
            """Exécute une séquence blink : open → closed (80ms) → half (50ms) → open → reschedule."""
            state = self._logic.state
            # Pas de blink en speaking, thinking, listening, offline, erreur
            # (thinking : personnage concentré ; listening : attentif)
            if state in ("speaking", "thinking", "listening", "offline", "error") or self._blink_active:
                self._schedule_blink()
                return

            self._blink_active = True
            # Sauvegarder la texture actuelle
            self._blink_tex_open = self._avatar_img.texture

            # Étape 1 : yeux fermés (80ms)
            path_closed = _sprite_path("idle", "closed")
            if Path(path_closed).exists():
                try:
                    ci = CoreImage(path_closed, nocache=True)
                    self._avatar_img.texture = ci.texture
                except Exception:
                    pass
            Clock.schedule_once(self._blink_half_open, 0.08)

        def _blink_half_open(self, dt: float = 0) -> None:
            """Étape 2 : yeux mi-clos (50ms)."""
            path_half = _sprite_path("idle", "half")
            if Path(path_half).exists():
                try:
                    ci = CoreImage(path_half, nocache=True)
                    self._avatar_img.texture = ci.texture
                except Exception:
                    pass
            Clock.schedule_once(self._blink_open, 0.05)

        def _blink_open(self, dt: float = 0) -> None:
            """Étape 3 : restaurer texture yeux ouverts, planifier prochain blink."""
            if self._blink_tex_open is not None:
                self._avatar_img.texture = self._blink_tex_open
                self._blink_tex_open = None
            self._blink_active = False
            self._schedule_blink()

        # --------------------------------------------------------
        # Statut debug
        # --------------------------------------------------------

        def status(self) -> dict:
            anim_type, period = self._logic.get_anim()
            return {
                "state":       self._logic.state,
                "color_hex":   self._logic.get_color_hex(),
                "glow_alpha":  round(self._glow_alpha, 3),
                "anim_type":   anim_type,
                "anim_period": period,
                "sprite_ok":   self._logic.sprite_exists(),
                "bg_path":     self._bg_path,
                "version":     "renderer_v1.1",
            }

else:

    class AvatarRenderer:  # type: ignore[no-redef]
        """Stub silencieux quand Kivy n'est pas disponible."""

        def __init__(self, **kwargs: object) -> None:
            self._logic   = AvatarRendererLogic()
            self._bg_path = ""

        def update_state(self, state_name: str) -> None:
            self._logic.set_state(state_name)

        def update_background(self, path: str) -> None:
            self._bg_path = path

        def status(self) -> dict:
            return {"state": self._logic.state, "kivy": False, "bg_path": self._bg_path}
