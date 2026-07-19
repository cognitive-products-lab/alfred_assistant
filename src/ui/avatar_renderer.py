"""
PROJECT      : ALFRED
BLOCK        : B15 -- Avatar & Interface
FUNCTION     : 15.02.001 -> 15.02.009
FILE         : src/ui/avatar_renderer.py
ROLE         : Renderer Kivy de l'avatar ALFRED -- sprites PNG + backgrounds + animations

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-05-14
UPDATED      : 2026-06-15 (V1.5 — fix bouche ouverte en pause + decalage frame "a")
VERSION      : V1.5
STATUS       : STABLE

NOTE 2026-06-15 : alfred_medium_neutral_e.png (frame "e" du cycle bouche
speaking) avait une échelle/position différente des 5 autres frames
(a,i,o,u,m) -- artefact du nettoyage rembg du 14/06 qui avait recadré le
personnage ~3% plus grand et décalé vers le haut, provoquant un "saut"
(saccade) visible chaque fois que cette frame apparaissait dans le cycle.
Recentré/redimensionné par script (scale 1362/1404, offset +65/+35 px) pour
aligner sa bounding box (alpha>128) sur celle des frames i/o/u/m
(y:86-1448). Backup pré-fix : alfred_medium_neutral_e.png.rembg_backup.

Rythme bouche (_tick_mouth) : remplace schedule_interval(period fixe) par
un schedule_once auto-replanifié avec gigue ±40% (_jittered_mouth_period)
-- évite le flap métronomique et donne un mouvement plus fluide/humain
pendant la lecture TTS, sans changer la logique de cycle déterministe
testée dans AvatarRendererLogic (next_speaking_frame).

NOTE 2026-06-15 (bis) : 2 fix lip-sync :
1) pause_mouth() affichait la frame "a" (bouche grande ouverte, index 0)
   pendant les silences entre phrases -> avatar visiblement bouche ouverte
   pendant la saisie de la phrase suivante par le TTS. Bascule désormais
   sur la frame "m" (bouche fermée, index 5 -- _MOUTH_CLOSED_IDX).
2) alfred_medium_neutral_a.png avait son contenu décalé de ~55px (5.4% de
   1024px) vers la gauche par rapport aux frames i/o/u/m (bbox alpha>128 :
   a x:236-701 vs i/o/u/m x:347-701, centres 468.5 vs 524) -> léger "saut"
   horizontal visible quand cette frame apparaît dans le cycle. Recentré
   par translation +56px vers la droite (nouveau centre ~524.5). Backup
   pré-fix : alfred_medium_neutral_a.png.shift_backup.

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

# Sprites expressifs medium — système d'avatar actif (base_normal archivé
# le 2026-07-18, cf. assets/_archive/README.md)
_ASSET_MEDIUM = (
    Path(__file__).resolve().parents[2]
    / "assets" / "avatars" / "avatar_medium" / "base_medium"
)

# Calques blink (yeux) du système layered avatar_no_mouth
_ASSET_BLINK = _ASSET_MEDIUM / "avatar_no_mouth"
_BLINK_HALF_FILE = "BL01.png"
_BLINK_CLOSED_FILE = "BL02.png"

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

# Frames animation bouche speaking — sprites medium expressifs
_SPEAKING_MEDIUM_FRAMES: list[str] = [
    "alfred_medium_neutral_a.png",
    "alfred_medium_neutral_e.png",
    "alfred_medium_neutral_i.png",
    "alfred_medium_neutral_o.png",
    "alfred_medium_neutral_u.png",
    "alfred_medium_neutral_m.png",
]

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
        """Retourne le sprite pour l'état donné (système medium).
        Ne pas appeler pour speaking (utiliser get_speaking_frame)."""
        name = state_name or self._state
        medium_file = _MEDIUM_SPRITES.get(name, _MEDIUM_SPRITES["idle"])
        return str(_ASSET_MEDIUM / medium_file)

    def get_speaking_frame(self) -> str:
        idx = self._speaking_idx % len(_SPEAKING_MEDIUM_FRAMES)
        return str(_ASSET_MEDIUM / _SPEAKING_MEDIUM_FRAMES[idx])

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
        for name in _MEDIUM_SPRITES:
            if name == "speaking":
                result[name] = all(
                    (_ASSET_MEDIUM / f).exists() for f in _SPEAKING_MEDIUM_FRAMES
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
            self._mouth_period: float = 0.12     # base rythme bouche (gigue ±40%)

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
                self._mouth_period = period
                # Premier tick programmé avec gigue (cf. _tick_mouth) pour un
                # rythme de bouche moins métronomique dès le départ.
                self._anim_clock = Clock.schedule_once(
                    self._tick_mouth, self._jittered_mouth_period()
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

        def _jittered_mouth_period(self) -> float:
            """Rythme bouche légèrement irrégulier (gigue ±40%) pour un effet
            de parole plus naturel qu'un flap métronomique à intervalle fixe."""
            import random
            base = getattr(self, "_mouth_period", 0.12)
            return random.uniform(base * 0.6, base * 1.4)

        def _tick_mouth(self, dt: float) -> None:
            if self._speaking_textures:
                # Swap texture directement — zéro reload, zéro flash noir
                self._avatar_img.texture = self._speaking_textures[self._speaking_tex_idx]
                self._speaking_tex_idx = (self._speaking_tex_idx + 1) % len(self._speaking_textures)
            else:
                self._load_avatar(self._logic.next_speaking_frame())

            # Auto-replanification avec gigue (remplace schedule_interval fixe)
            if self._logic.state == "speaking":
                self._anim_clock = Clock.schedule_once(
                    self._tick_mouth, self._jittered_mouth_period()
                )

        # Index de la frame bouche fermée (m) dans _SPEAKING_MEDIUM_FRAMES,
        # utilisée pendant les silences (pause_mouth) pour éviter que l'avatar
        # reste visuellement bouche ouverte (frame "a") entre deux phrases.
        _MOUTH_CLOSED_IDX: int = 5

        def pause_mouth(self) -> None:
            """Suspend l'animation bouche (silence TTS entre deux phrases),
            sans changer l'état/sprite — évite le flash idle/thinking."""
            if self._anim_clock and self._logic.state == "speaking":
                self._anim_clock.cancel()
                self._anim_clock = None
                # Bouche fermée pendant le silence (frame "m", pas "a")
                if self._speaking_textures:
                    idx = min(self._MOUTH_CLOSED_IDX, len(self._speaking_textures) - 1)
                    self._avatar_img.texture = self._speaking_textures[idx]
                    self._speaking_tex_idx = idx
                else:
                    self._load_avatar(self._logic.get_sprite("speaking"))

        # Amplitude RMS de référence (~niveau moyen d'une phrase TTS Piper
        # en float32 normalisé). Sert à mapper l'amplitude réelle de chaque
        # phrase sur une vitesse de bouche relative.
        _AMPLITUDE_REF: float = 0.12

        def _amplitude_to_period(self, amplitude: float) -> float:
            """Convertit une amplitude RMS en période de bouche (s).

            Phrase plus forte -> bouche plus rapide (période plus courte) ;
            phrase plus faible -> bouche plus lente. Borné pour rester
            crédible même sur des valeurs d'amplitude extrêmes/nulles.
            """
            if amplitude <= 0 or self._AMPLITUDE_REF <= 0:
                return 0.12
            factor = max(0.5, min(2.0, amplitude / self._AMPLITUDE_REF))
            return max(0.07, min(0.22, 0.12 / factor))

        def set_mouth_amplitude(self, amplitude: float) -> None:
            """Ajuste le rythme de base de la bouche selon l'amplitude RMS
            de la phrase TTS en cours (cf. PiperTTS.last_amplitude).

            N'interrompt pas une animation en cours -- prend effet à la
            prochaine replanification de _tick_mouth (gigue, cf.
            _jittered_mouth_period)."""
            self._mouth_period = self._amplitude_to_period(amplitude)

        def resume_mouth(self, amplitude: float = 1.0) -> None:
            """Relance l'animation bouche si l'état courant est 'speaking',
            avec un rythme adapté à l'amplitude (volume) de la phrase qui
            commence -- simple mesure de sync TTS/avatar (RMS par phrase)."""
            self.set_mouth_amplitude(amplitude)
            if self._logic.state == "speaking" and self._anim_clock is None:
                anim_type, _ = self._logic.get_anim("speaking")
                self._start_anim(anim_type, self._mouth_period)

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
            path_closed = str(_ASSET_BLINK / _BLINK_CLOSED_FILE)
            if Path(path_closed).exists():
                try:
                    ci = CoreImage(path_closed, nocache=True)
                    self._avatar_img.texture = ci.texture
                except Exception:
                    pass
            Clock.schedule_once(self._blink_half_open, 0.08)

        def _blink_half_open(self, dt: float = 0) -> None:
            """Étape 2 : yeux mi-clos (50ms)."""
            path_half = str(_ASSET_BLINK / _BLINK_HALF_FILE)
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
