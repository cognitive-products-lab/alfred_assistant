"""
PROJECT      : ALFRED
BLOCK        : B15 -- Avatar & Interface
FUNCTION     : 15.03.001 -> 15.03.008
FILE         : src/ui/alfred_app.py
ROLE         : Application Kivy ALFRED V1.4 — fenetre complete avec controles + webcam overlay

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-05-14
UPDATED      : 2026-06-15 (V1.7 — taille fenêtre par défaut agrandie)
VERSION      : V1.7
STATUS       : TO_TEST

DESCRIPTION :
Application graphique Kivy d'ALFRED, prototype complet.

Layout vertical (420 x 720) :
  ControlBar     ( 6%) -- Son | Micro | Caméra | Réglages
  AvatarRenderer (47%) -- 6 calques + background dynamique
  SoundWaveWidget( 7%) -- visualisation audio (speaking / listening)
  ConversationBox(26%) -- historique dialogue scrollable
  InputRow        (8%) -- TextInput + bouton micro (push-to-talk) + bouton envoi
  StatusBar       (6%) -- mode | émotion | état

NOTE 2026-06-15 : InputRow a désormais un bouton 🎤 type WhatsApp — clic pour
démarrer l'enregistrement (sd.InputStream, durée libre), clic pour l'arrêter
et transcrire via Whisper (_transcribe_audio de src/main.py) en arrière-plan ;
le texte transcrit est posé dans le champ de saisie pour relecture avant
envoi. Écoute continue volontairement non implémentée ici (cf. choix
confidentialité — [[feedback_alfred_voice_privacy]]). Testé en conditions
réelles : capture + transcription + envoi OK.

NOTE 2026-06-15 (bis) : fix affichage des icônes ControlBar (🔊🎤📷⚙️) et
InputRow (🎤⏹→), rendues en carrés ".notdef" car OpenDyslexic ne contient
pas ces glyphes. Ajout de _FONT_ICON (Segoe UI Emoji) + helper _icon_label()
qui wrap l'icône dans un tag markup [font=...] tandis que le libellé garde
OpenDyslexic. Étendu via _wrap_emoji_markup() (regex sur plages Unicode
emoji/symboles/flèches) appliqué dans ConversationBox._add_label() et
append_stream_phrase(), pour que les emoji du texte libre (réponses ALFRED,
ex. "👋 Première utilisation détectée !", préfixe "💭") s'affichent aussi
correctement.

NOTE 2026-06-15 (ter) : fix InputRow.set_enabled() — le bouton micro était
forcé disabled=True dès que _recording=True, quel que soit l'argument
`enabled`. Or set_input_enabled(False) est appelé pendant qu'ALFRED traite
la réponse, ce qui pouvait verrouiller le micro et empêcher le 2e clic
(arrêt d'enregistrement) si l'utilisateur démarrait l'enregistrement avant
la fin du cycle précédent. Le bouton micro reste désormais cliquable tant
qu'un enregistrement est en cours, indépendamment de `enabled`.

NOTE 2026-06-15 (quater) : taille de fenêtre par défaut passée de 420x720 à
740x830 — à 420px de large, les boutons de la ControlBar (Son | Micro |
Caméra | Réglages) se chevauchaient à l'ouverture. Fenêtre redimensionnable
(resizable=1) inchangée, l'utilisateur peut toujours ajuster.

Bridges thread-safe :
  UI -> Pipeline : ui_bridge.send_user_input()
  Pipeline -> UI : set_ui_response(), set_ui_thinking(), stream_ui_phrase()

Messages de réflexion ALFRED rotatifs (personnalisés, en français).
ControlBar envoie les commandes "son" et "vocal" au pipeline.
SoundWave synchronisé avec les états speaking/listening.
Auto-réactivation saisie après chaque réponse.

Usage :
  python src/ui/alfred_app.py            # demo standalone
  python src/alfred_with_ui.py           # prototype complet
"""

from __future__ import annotations

import math
import os
import random
import re
import sys
import textwrap
from pathlib import Path

os.environ.setdefault("KIVY_NO_ENV_CONFIG", "1")

from kivy.config import Config  # noqa: E402
Config.set("graphics", "width",  "740")
Config.set("graphics", "height", "830")
Config.set("graphics", "resizable", "1")
Config.set("graphics", "borderless", "0")
Config.set("graphics", "show_cursor", "1")
Config.set("input",    "mouse",  "mouse,multitouch_on_demand")

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from kivy.app import App                          # noqa: E402
from kivy.clock import Clock                      # noqa: E402
from kivy.core.window import Window               # noqa: E402
from kivy.graphics import Color, Rectangle        # noqa: E402
from kivy.uix.boxlayout import BoxLayout         # noqa: E402
from kivy.uix.button import Button                # noqa: E402
from kivy.uix.label import Label                  # noqa: E402
from kivy.uix.scrollview import ScrollView        # noqa: E402
from kivy.uix.textinput import TextInput          # noqa: E402
from kivy.uix.widget import Widget                # noqa: E402

from src.ui.avatar_renderer import AvatarRenderer  # noqa: E402
from src.ui.background_manager import BackgroundManager  # noqa: E402
from src.ui.sound_wave import SoundWaveWidget      # noqa: E402
from src.ui.avatar_controller import AVATAR_STATES  # noqa: E402
from src.ui.avatar_engine import get_avatar_engine  # noqa: E402
from src.ui.webcam_widget import WebcamOverlay     # noqa: E402
from src.ui.device_settings import (              # noqa: E402
    open_settings_popup,
    load_device_settings,
    apply_audio_settings,
    prefetch_devices_async,
    settings_file_exists,
)


# ============================================================
# Typographie — accessibilité dyslexie
# ============================================================
# Tailles x2 vs baseline. Pour activer OpenDyslexic :
#   1. Télécharger OpenDyslexic.ttf dans assets/fonts/
#   2. Remplacer _FONT par str(ROOT / "assets/fonts/OpenDyslexic.ttf")
_FONT        = str(ROOT / "assets" / "fonts" / "OpenDyslexic3-Regular.ttf")

# OpenDyslexic ne contient pas les glyphes emoji/symboles (🎤 ⏹ →) -> rendus
# en carrés ".notdef". Police système dédiée aux icônes des boutons.
_FONT_ICON = "C:/Windows/Fonts/seguiemj.ttf"
if not Path(_FONT_ICON).exists():
    _FONT_ICON = _FONT


def _icon_label(icon: str, label: str) -> str:
    """Texte markup bouton : icône via _FONT_ICON, libellé via la police par défaut."""
    return f"[font={_FONT_ICON}]{icon}[/font] {label}"


# Plages Unicode emoji/symboles courantes (mêmes glyphes absents d'OpenDyslexic
# que pour les boutons, ex. 👋 💭 🔊 🎤). Regroupe les séquences consécutives
# pour minimiser le nombre de balises [font=...].
_EMOJI_RE = re.compile(
    "["
    "\U0001F300-\U0001FAFF"
    "\U00002600-\U000027BF"
    "\U0001F1E6-\U0001F1FF"
    "←-⇿"
    "⌀-⏿"
    "️"
    "]+"
)


def _wrap_emoji_markup(text: str) -> str:
    """Enrobe les séquences emoji/symboles d'un texte markup avec _FONT_ICON
    pour éviter qu'elles s'affichent en carrés ".notdef" (police OpenDyslexic)."""
    return _EMOJI_RE.sub(lambda m: f"[font={_FONT_ICON}]{m.group(0)}[/font]", text)

_FS_MENU     = "22sp"     # ControlBar boutons  (était 11sp)
_FS_STATUS   = "20sp"     # StatusBar labels    (était 10sp)
_FS_CHAT     = "26sp"     # ConversationBox     (était 13sp)
_FS_INPUT    = "26sp"     # TextInput saisie    (était 13sp)
_FS_SEND     = "26sp"     # Bouton →            (était 20sp)
_FS_AVATAR   = "14sp"     # Label état avatar   (inchangé)


# ============================================================
# Palette ALFRED
# ============================================================

_FG_TEXT  = (0.88, 0.88, 0.92, 1)
_FG_DIM   = (0.55, 0.55, 0.62, 1)
_ACCENT   = (0.54, 0.62, 0.83, 1)
_CLR_USER = (0.70, 0.82, 1.00, 1)
_CLR_ALF  = (0.88, 0.88, 0.92, 1)
_CLR_BTN  = (0.10, 0.12, 0.20, 1)
_CLR_BTN_ON = (0.18, 0.34, 0.22, 1)   # bouton actif (vert sombre)
_CLR_BTN_OFF= (0.30, 0.12, 0.12, 1)   # bouton muet/off (rouge sombre)


# ============================================================
# Messages de réflexion personnalisés ALFRED
# ============================================================

_THINKING_MESSAGES = [
    "Je te demande un instant pendant que je réfléchis pour te donner la réponse la plus adaptée...",
    "Hmm, laisse-moi chercher la meilleure façon de t'aider...",
    "Un moment, je consulte mes données pour trouver quelque chose d'utile pour toi...",
    "Je prends le temps de bien réfléchir à ta question...",
    "Je traite ta demande avec attention, une seconde...",
    "Bonne question — je cherche la réponse la plus pertinente pour toi...",
    "Je réfléchis... je veux m'assurer de te donner quelque chose de vraiment utile.",
    "Un instant — je synthétise les informations pour toi...",
]


def _get_thinking_message() -> str:
    return random.choice(_THINKING_MESSAGES)


# ============================================================
# Bridge thread-safe : pipeline -> UI Kivy
# ============================================================

_app_instance: "AlfredApp | None" = None


def set_ui_response(text: str) -> None:
    """
    Met a jour la zone dialogue depuis n'importe quel thread.
    Si un stream est en cours, le finalise. Sinon ajoute le message complet.
    Re-active le champ de saisie.
    """
    if _app_instance is not None and _app_instance._layout is not None:
        def _update(dt: float) -> None:
            layout = _app_instance._layout
            if layout is None:
                return
            conv = layout.conv_box
            if conv.is_streaming:
                conv.finalize_stream()
            else:
                conv.add_alfred_message(text)
            layout.set_input_enabled(True)
            layout.wave.set_speaking(False)
        Clock.schedule_once(_update)


def set_ui_thinking(thinking: bool = True) -> None:
    """Affiche / masque l'indicateur de réflexion ALFRED dans la ConversationBox."""
    if _app_instance is not None and _app_instance._layout is not None:
        msg = _get_thinking_message() if thinking else ""
        Clock.schedule_once(
            lambda dt: _app_instance._layout.set_thinking_indicator(thinking, msg)
        )


def set_ui_input_enabled(enabled: bool) -> None:
    """Active ou desactive le champ de saisie."""
    if _app_instance is not None and _app_instance._layout is not None:
        Clock.schedule_once(
            lambda dt: _app_instance._layout.set_input_enabled(enabled)
        )


def stream_ui_phrase(phrase: str) -> None:
    """
    Affiche une phrase en streaming dans la ConversationBox.
    Thread-safe — appele depuis le thread pipeline pendant generate().
    """
    if _app_instance is not None and _app_instance._layout is not None:
        p = phrase
        Clock.schedule_once(
            lambda dt: _app_instance._layout.conv_box.append_stream_phrase(p)
        )


def set_ui_speaking(active: bool) -> None:
    """Synchronise le SoundWaveWidget avec l'etat TTS."""
    if _app_instance is not None and _app_instance._layout is not None:
        Clock.schedule_once(
            lambda dt: _app_instance._layout.wave.set_speaking(active)
        )


def set_ui_listening(active: bool) -> None:
    """Synchronise le SoundWaveWidget avec l'etat microphone."""
    if _app_instance is not None and _app_instance._layout is not None:
        Clock.schedule_once(
            lambda dt: _app_instance._layout.wave.set_listening(active)
        )


def is_camera_active() -> bool:
    """Indique si la caméra est actuellement activée (overlay webcam)."""
    if _app_instance is not None and _app_instance._layout is not None:
        return _app_instance._layout.avatar_area.camera_active
    return False


def get_camera_snapshot_b64(quality: int = 80) -> Optional[str]:
    """
    Capture la dernière frame caméra (pleine résolution) en JPEG base64.
    Thread-safe — ne nécessite pas le thread Kivy (lecture sous verrou).

    Returns:
        Chaîne base64 ou None si caméra inactive / aucune frame disponible.
    """
    if _app_instance is None or _app_instance._layout is None:
        return None
    return _app_instance._layout.avatar_area.capture_snapshot_jpeg_b64(quality=quality)


def set_ui_location(location: str) -> None:
    """Change le fond selon le lieu (salon, cuisine, bureau...) — thread-safe."""
    if _app_instance is not None:
        Clock.schedule_once(lambda dt: _app_instance.set_location(location))


# ============================================================
# ControlBar (Son | Micro | Caméra | Réglages)
# ============================================================

class ControlBar(BoxLayout):
    """
    Barre de controle superieure.
    Boutons : Son (toggle TTS) | Micro (toggle STT) | Caméra (V2) | Réglages (V2)
    Les commandes son/vocal sont envoyees au pipeline via ui_bridge.
    """

    def __init__(self, on_command=None, **kwargs: object) -> None:
        kwargs.setdefault("orientation", "horizontal")
        kwargs.setdefault("size_hint",   (1, 1))
        kwargs.setdefault("padding",     [6, 2])
        kwargs.setdefault("spacing",     4)
        super().__init__(**kwargs)

        self._on_cmd      = on_command
        self._sound_muted = False
        self._mic_active  = False

        with self.canvas.before:
            Color(0.03, 0.03, 0.07, 0.97)
            self._bg = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self._upd_bg, size=self._upd_bg)

        self._btn_son = self._make_btn("🔊", "Son",     self._toggle_son)
        self._btn_mic = self._make_btn("🎤", "Micro",   self._toggle_mic)
        self._btn_cam = self._make_btn("📷", "Caméra",  self._toggle_cam)
        self._btn_cfg = self._make_btn("⚙️", "Réglages", self._toggle_cfg)

        for b in [self._btn_son, self._btn_mic, self._btn_cam, self._btn_cfg]:
            self.add_widget(b)

    def _make_btn(self, icon: str, label: str, cb) -> Button:
        b = Button(
            text=_icon_label(icon, label),
            markup=True,
            font_size=_FS_MENU,
            font_name=_FONT,
            size_hint=(0.25, 1),
            background_color=_CLR_BTN,
            color=_FG_TEXT,
            bold=False,
        )
        b.bind(on_release=lambda _, c=cb: c())
        return b

    def _upd_bg(self, *_: object) -> None:
        self._bg.pos  = self.pos
        self._bg.size = self.size

    def _toggle_son(self) -> None:
        self._sound_muted = not self._sound_muted
        if self._sound_muted:
            self._btn_son.text             = _icon_label("🔇", "Muet")
            self._btn_son.background_color = _CLR_BTN_OFF
        else:
            self._btn_son.text             = _icon_label("🔊", "Son")
            self._btn_son.background_color = _CLR_BTN
        if self._on_cmd:
            self._on_cmd("son")

    def _toggle_mic(self) -> None:
        self._mic_active = not self._mic_active
        if self._mic_active:
            self._btn_mic.text             = _icon_label("🎤", "ON")
            self._btn_mic.background_color = _CLR_BTN_ON
            if _app_instance and _app_instance._layout:
                _app_instance._layout.wave.set_listening(True)
        else:
            self._btn_mic.text             = _icon_label("🎤", "Micro")
            self._btn_mic.background_color = _CLR_BTN
            if _app_instance and _app_instance._layout:
                _app_instance._layout.wave.set_listening(False)
        if self._on_cmd:
            self._on_cmd("vocal")

    def _toggle_cam(self) -> None:
        # Déléguer au WebcamOverlay si disponible
        if _app_instance and _app_instance._layout:
            overlay = _app_instance._layout.avatar_area
            active  = overlay.toggle_camera()
            if active:
                self._btn_cam.text             = _icon_label("📷", "ON")
                self._btn_cam.background_color = _CLR_BTN_ON
            else:
                self._btn_cam.text             = _icon_label("📷", "Caméra")
                self._btn_cam.background_color = _CLR_BTN
        else:
            # Fallback : pas encore prêt
            self._btn_cam.text = _icon_label("📷", "...")
            Clock.schedule_once(
                lambda dt: setattr(self._btn_cam, "text", _icon_label("📷", "Caméra")), 1.5
            )

    def _toggle_cfg(self) -> None:
        """Ouvre le popup de réglages périphériques (Caméra / Micro / Son)."""
        self._btn_cfg.background_color = _CLR_BTN_ON

        def _on_apply(new_settings: dict) -> None:
            """Appelé quand l'utilisateur clique Appliquer."""
            # ── Caméra : changer l'index si la webcam est active ─────────────
            if _app_instance and _app_instance._layout:
                overlay = _app_instance._layout.avatar_area
                new_cam = new_settings.get("camera_index", 0)
                if overlay.camera_active:
                    # Redémarrer avec le nouvel index
                    overlay.stop_camera()
                    overlay._cam_widget._cam_index = new_cam
                    ok = overlay._cam_widget.start()
                    overlay._cam_widget.opacity = 1 if ok else 0
                else:
                    # Juste mettre à jour l'index pour le prochain start()
                    overlay._cam_widget._cam_index = new_cam

            self._btn_cfg.background_color = _CLR_BTN
            self._btn_cfg.text = _icon_label("⚙️", "Réglages")

        def _on_dismiss() -> None:
            self._btn_cfg.background_color = _CLR_BTN
            self._btn_cfg.text = _icon_label("⚙️", "Réglages")

        open_settings_popup(on_apply=_on_apply)


# ============================================================
# StatusBar
# ============================================================

class StatusBar(BoxLayout):
    """Barre basse : mode | émotion | état courant."""

    def __init__(self, **kwargs: object) -> None:
        kwargs.setdefault("orientation", "horizontal")
        kwargs.setdefault("size_hint",   (1, 1))
        kwargs.setdefault("padding",     [10, 3])
        kwargs.setdefault("spacing",     6)
        super().__init__(**kwargs)

        with self.canvas.before:
            Color(0.04, 0.04, 0.08, 0.94)
            self._bg = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self._upd_bg, size=self._upd_bg)

        self._lbl_mode  = self._lbl("mode: –")
        self._lbl_emot  = self._lbl("émotion: –")
        self._lbl_state = self._lbl("idle", color=_ACCENT)

        for l in [self._lbl_mode, self._lbl_emot, self._lbl_state]:
            self.add_widget(l)

    def _lbl(self, text: str, color: tuple = _FG_DIM) -> Label:
        return Label(text=text, font_size=_FS_STATUS, font_name=_FONT,
                     color=color, halign="center", valign="middle")

    def _upd_bg(self, *_: object) -> None:
        self._bg.pos  = self.pos
        self._bg.size = self.size

    def update(self, state: str, mode: str, emotion: str) -> None:
        self._lbl_mode.text  = f"mode: {mode}"
        self._lbl_emot.text  = f"émotion: {emotion}"
        self._lbl_state.text = state


# ============================================================
# ConversationBox (scrollable)
# ============================================================

class ConversationBox(ScrollView):
    """Zone de dialogue scrollable avec streaming phrase par phrase."""

    _MAX_MSGS    = 30
    _THINKING_PFX = "💭 "

    def __init__(self, **kwargs: object) -> None:
        kwargs.setdefault("size_hint",   (1, 1))
        kwargs.setdefault("do_scroll_x", False)
        kwargs.setdefault("do_scroll_y", True)
        kwargs.setdefault("bar_width",   3)
        kwargs.setdefault("scroll_type", ["bars", "content"])
        super().__init__(**kwargs)

        with self.canvas.before:
            Color(0.04, 0.04, 0.08, 0.90)
            self._bg = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self._upd_bg, size=self._upd_bg)

        self._inner = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            spacing=5,
            padding=[10, 6, 10, 6],
        )
        self._inner.bind(minimum_height=self._inner.setter("height"))
        self.add_widget(self._inner)

        self._thinking_lbl: Label | None = None
        self._stream_lbl:   Label | None = None
        self._stream_text:  str          = ""
        self._msg_count     = 0

        self._add_label("En attente de ta question...", color=_FG_DIM, italic=True)

    def _upd_bg(self, *_: object) -> None:
        self._bg.pos  = self.pos
        self._bg.size = self.size

    def _add_label(
        self,
        text:   str,
        color:  tuple  = _FG_TEXT,
        italic: bool   = False,
        prefix: str    = "",
    ) -> Label:
        display = _wrap_emoji_markup(f"{prefix}{text}")
        display = f"[i]{display}[/i]" if italic else display
        lbl = Label(
            text=display,
            markup=True,
            font_size=_FS_CHAT,
            font_name=_FONT,
            color=color,
            halign="left",
            valign="top",
            size_hint_y=None,
            text_size=(max(self.width - 24, 360), None),
            line_height=1.4,
        )
        lbl.bind(texture_size=lambda l, ts: setattr(l, "height", ts[1] + 10))
        self.bind(width=lambda _, w: setattr(lbl, "text_size", (w - 24, None)))
        self._inner.add_widget(lbl)
        self._msg_count += 1
        if self._msg_count > self._MAX_MSGS:
            self._inner.remove_widget(self._inner.children[-1])
            self._msg_count -= 1
        Clock.schedule_once(lambda dt: setattr(self, "scroll_y", 0), 0.04)
        return lbl

    # ── Messages ─────────────────────────────────────────────

    def add_user_message(self, text: str) -> None:
        self._remove_thinking()
        self.finalize_stream()
        short = textwrap.shorten(text, width=200, placeholder="...")
        self._add_label(short, color=_CLR_USER, prefix="Toi : ")

    def add_alfred_message(self, text: str) -> None:
        self._remove_thinking()
        self.finalize_stream()
        self._add_label(text, color=_CLR_ALF, prefix="ALFRED : ")

    def set_thinking_indicator(self, show: bool, message: str = "") -> None:
        self._remove_thinking()
        if show:
            msg = message or "Je réfléchis..."
            self._thinking_lbl = self._add_label(
                msg, color=_FG_DIM, italic=True, prefix=self._THINKING_PFX
            )

    # ── Streaming phrase par phrase ───────────────────────────

    @property
    def is_streaming(self) -> bool:
        return self._stream_lbl is not None

    def append_stream_phrase(self, phrase: str) -> None:
        sep = " " if self._stream_text and not self._stream_text.endswith("\n") else ""
        self._stream_text += sep + phrase

        if self._stream_lbl is None:
            self._stream_lbl = self._add_label(
                self._stream_text, color=_CLR_ALF, prefix="ALFRED : "
            )
        else:
            self._stream_lbl.text = _wrap_emoji_markup("ALFRED : " + self._stream_text)
        Clock.schedule_once(lambda dt: setattr(self, "scroll_y", 0), 0.02)

    def finalize_stream(self) -> None:
        self._remove_thinking()
        self._stream_lbl  = None
        self._stream_text = ""

    def _remove_thinking(self) -> None:
        if self._thinking_lbl and self._thinking_lbl in self._inner.children:
            self._inner.remove_widget(self._thinking_lbl)
            self._msg_count -= 1
        self._thinking_lbl = None


# ============================================================
# InputRow
# ============================================================

class InputRow(BoxLayout):
    """TextInput + bouton micro (push-to-talk) + bouton Envoyer."""

    def __init__(self, on_submit_cb=None, **kwargs: object) -> None:
        kwargs.setdefault("orientation", "horizontal")
        kwargs.setdefault("size_hint",   (1, 1))
        kwargs.setdefault("padding",     [8, 3])
        kwargs.setdefault("spacing",     5)
        super().__init__(**kwargs)

        self._on_submit = on_submit_cb
        self._recording   = False
        self._mic_stream  = None
        self._mic_frames: list = []

        with self.canvas.before:
            Color(0.05, 0.05, 0.11, 0.97)
            self._bg = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self._upd_bg, size=self._upd_bg)

        self._txt = TextInput(
            hint_text="Écris à ALFRED...",
            hint_text_color=(0.40, 0.40, 0.50, 1),
            foreground_color=_FG_TEXT,
            background_color=(0.09, 0.09, 0.16, 1),
            cursor_color=(*_ACCENT[:3], 1),
            font_size=_FS_INPUT,
            font_name=_FONT,
            multiline=False,
            size_hint=(0.66, 1),
            padding=[10, 8],
        )
        self._txt.bind(on_text_validate=self._submit)

        self._btn_mic = Button(
            text="🎤",
            font_size=_FS_SEND,
            font_name=_FONT_ICON,
            size_hint=(0.16, 1),
            background_color=_CLR_BTN,
            color=_FG_TEXT,
            bold=True,
        )
        self._btn_mic.bind(on_release=lambda _: self._toggle_mic())

        self._btn = Button(
            text="→",
            font_size=_FS_SEND,
            font_name=_FONT_ICON,
            size_hint=(0.18, 1),
            background_color=(0.28, 0.36, 0.58, 1),
            color=_FG_TEXT,
            bold=True,
        )
        self._btn.bind(on_release=lambda _: self._submit())

        self.add_widget(self._txt)
        self.add_widget(self._btn_mic)
        self.add_widget(self._btn)

    def _upd_bg(self, *_: object) -> None:
        self._bg.pos  = self.pos
        self._bg.size = self.size

    def _submit(self, *_: object) -> None:
        text = self._txt.text.strip()
        if not text:
            return
        self._txt.text = ""
        self.set_enabled(False)
        if self._on_submit:
            self._on_submit(text)

    def set_enabled(self, enabled: bool) -> None:
        self._txt.disabled  = not enabled
        self._btn.disabled  = not enabled
        # Le micro reste cliquable pendant un enregistrement actif (clic
        # d'arret), meme si enabled=False (ALFRED en cours de reponse).
        self._btn_mic.disabled = (not enabled) and (not self._recording)
        self._btn.background_color = (
            (0.28, 0.36, 0.58, 1) if enabled else (0.14, 0.14, 0.22, 1)
        )

    def focus_input(self) -> None:
        self._txt.focus = True

    # ── Micro push-to-talk (clic pour démarrer, clic pour arrêter) ─────────
    #
    # Comme la commande CLI "ecoute" (cf. main.py listen_voice_until_enter) :
    # 1er clic démarre l'enregistrement (sd.InputStream, durée libre),
    # 2e clic l'arrête et lance la transcription Whisper en arrière-plan.
    # Le texte transcrit est posé dans le champ de saisie pour relecture
    # avant envoi — pas d'écoute continue (cf. choix confidentialité B20).

    def _toggle_mic(self) -> None:
        if self._recording:
            self._stop_recording()
        else:
            self._start_recording()

    def _start_recording(self) -> None:
        try:
            import sounddevice as sd
        except Exception as exc:
            print(f"  [AVERT micro UI] {exc}")
            return

        self._mic_frames = []

        def _callback(indata, frame_count, time_info, status) -> None:
            self._mic_frames.append(indata.copy())

        try:
            self._mic_stream = sd.InputStream(
                samplerate=16000,
                channels=1,
                dtype="float32",
                callback=_callback,
            )
            self._mic_stream.start()
        except Exception as exc:
            print(f"  [AVERT micro UI] {exc}")
            self._mic_stream = None
            return

        self._recording = True
        self._btn_mic.text = "⏹"
        self._btn_mic.background_color = _CLR_BTN_ON
        self._txt.hint_text = "Écoute... clique sur ⏹ pour terminer"
        set_ui_listening(True)

    def _stop_recording(self) -> None:
        stream = self._mic_stream
        self._mic_stream = None
        self._recording  = False
        self._btn_mic.text = "🎤"
        self._btn_mic.background_color = _CLR_BTN
        self._txt.hint_text = "Écris à ALFRED..."
        set_ui_listening(False)

        if stream is not None:
            try:
                stream.stop()
                stream.close()
            except Exception:
                pass

        frames = self._mic_frames
        self._mic_frames = []
        if not frames:
            return

        import threading
        threading.Thread(target=self._transcribe_async, args=(frames,), daemon=True).start()

    def _transcribe_async(self, frames: list) -> None:
        import numpy as np

        audio = np.concatenate(frames, axis=0)
        try:
            from src.main import _transcribe_audio
            text = _transcribe_audio(audio)
        except Exception as exc:
            print(f"  [AVERT transcription UI] {exc}")
            return

        if text:
            Clock.schedule_once(lambda dt: self._fill_transcription(text))

    def _fill_transcription(self, text: str) -> None:
        self._txt.text = text
        self._txt.focus = True


# ============================================================
# Layout principal
# ============================================================

class AlfredLayout(BoxLayout):
    """
    Layout V1.3 :
      ControlBar      ( 6%) -- Son | Micro | Caméra | Réglages
      AvatarRenderer  (47%) -- 6 calques + background
      SoundWaveWidget ( 7%) -- barres audio animees
      ConversationBox (26%) -- historique dialogue
      InputRow         (8%) -- saisie utilisateur
      StatusBar        (6%) -- mode | émotion | état
    """

    def __init__(self, on_user_input=None, on_command=None, **kwargs: object) -> None:
        kwargs.setdefault("orientation", "vertical")
        super().__init__(**kwargs)

        self.ctrl_bar   = ControlBar(on_command=on_command, size_hint=(1, 0.06))
        self.renderer   = AvatarRenderer(size_hint=(1, 1))
        self.avatar_area = WebcamOverlay(renderer=self.renderer, size_hint=(1, 0.47))
        self.wave        = SoundWaveWidget(size_hint=(1, 0.07))
        self.conv_box    = ConversationBox(size_hint=(1, 0.26))
        self.input_row   = InputRow(on_submit_cb=on_user_input, size_hint=(1, 0.08))
        self.status_bar  = StatusBar(size_hint=(1, 0.06))

        for w in [self.ctrl_bar, self.avatar_area, self.wave,
                  self.conv_box, self.input_row, self.status_bar]:
            self.add_widget(w)

    def add_user_message(self, text: str) -> None:
        self.conv_box.add_user_message(text)

    def add_alfred_message(self, text: str) -> None:
        self.conv_box.add_alfred_message(text)

    def set_thinking_indicator(self, show: bool, message: str = "") -> None:
        self.conv_box.set_thinking_indicator(show, message)

    def set_input_enabled(self, enabled: bool) -> None:
        self.input_row.set_enabled(enabled)
        if enabled:
            Clock.schedule_once(lambda dt: self.input_row.focus_input(), 0.1)

    def set_status(self, state: str, mode: str, emotion: str) -> None:
        self.status_bar.update(state, mode, emotion)

    # Compat V1.1
    def set_response(self, text: str) -> None:
        self.add_alfred_message(text)


# ============================================================
# Application principale
# ============================================================

class AlfredApp(App):
    """
    Application Kivy ALFRED V1.3.

    - Background dynamique (lieu + periode)
    - Avatar 6 calques + alfred_thinking.png
    - ControlBar : Son / Micro / Caméra / Réglages
    - SoundWave synchronisé TTS/STT
    - Messages de réflexion ALFRED personnalisés
    - ConversationBox scrollable avec streaming
    - InputRow intégré (plus besoin du terminal)
    """

    title = "ALFRED — V1"

    _BG_REFRESH_INTERVAL = 600

    def __init__(
        self,
        demo_mode: bool = True,
        location:  str  = "salon",
        **kwargs: object,
    ) -> None:
        global _app_instance
        super().__init__(**kwargs)
        self._demo        = demo_mode
        self._demo_idx    = 0
        self._demo_states = list(AVATAR_STATES.keys())
        self._layout: AlfredLayout | None = None
        self._location    = location
        _app_instance     = self

    def build(self) -> AlfredLayout:
        # Pré-charge la liste des caméras/audio en arrière-plan pour que le
        # popup ⚙️ Réglages s'ouvre instantanément (évite le freeze du scan
        # OpenCV dans le thread principal Kivy)
        prefetch_devices_async()

        self._layout = AlfredLayout(
            on_user_input=self._handle_user_input,
            on_command=self._handle_command,
        )

        engine = get_avatar_engine(headless=False)
        engine.start(renderer=self._layout.renderer)

        def _on_state(state_name: str) -> None:
            if not self._layout:
                return
            # Sync SoundWave avec états avatar
            def _sync(dt: float) -> None:
                if not self._layout:
                    return
                wave = self._layout.wave
                if state_name == "speaking":
                    wave.set_speaking(True)
                elif state_name == "listening":
                    wave.set_listening(True)
                else:
                    wave.set_idle()
                ctrl = engine._controller
                self._layout.set_status(
                    state_name,
                    ctrl.current_state.mode,
                    ctrl.current_state.emotion,
                )
            Clock.schedule_once(_sync)

        engine.register_hook(_on_state)

        Window.bind(on_resize=lambda win, w, h: Clock.schedule_once(
            lambda dt: self._layout.renderer._redraw_canvas() if self._layout else None
        ))

        self._refresh_background()
        Clock.schedule_interval(
            lambda dt: self._refresh_background(),
            self._BG_REFRESH_INTERVAL,
        )

        # Appliquer les réglages audio sauvegardés (micro + sortie son)
        _first_launch = False
        try:
            _first_launch = not settings_file_exists()
            _saved = load_device_settings()
            apply_audio_settings(_saved)
            # Pré-charger l'index caméra sauvegardé dans le widget
            if self._layout and hasattr(self._layout, "avatar_area"):
                cam_idx = _saved.get("camera_index", 0)
                self._layout.avatar_area._cam_widget._cam_index = cam_idx
        except Exception:
            pass

        # Première utilisation : ouvrir le popup Réglages devices automatiquement
        if _first_launch and not self._demo and self._layout:
            Clock.schedule_once(lambda dt: self._layout.ctrl_bar._toggle_cfg(), 1.0)

        if self._demo:
            Clock.schedule_interval(self._demo_tick, 2.5)
            self._layout.add_alfred_message(
                "Mode démo — cycle des états avatar.\n"
                "Lance alfred_with_ui.py pour le prototype complet."
            )
        else:
            Clock.schedule_once(lambda dt: self._layout.set_input_enabled(True), 0.5)

        return self._layout

    def _handle_user_input(self, text: str) -> None:
        """Appelé quand l'utilisateur valide dans InputRow."""
        if self._layout:
            self._layout.add_user_message(text)
            msg = _get_thinking_message()
            self._layout.set_thinking_indicator(True, msg)

        try:
            from src.ui.ui_bridge import send_user_input
            send_user_input(text)
        except Exception:
            pass

    def _handle_command(self, cmd: str) -> None:
        """Envoie une commande système au pipeline (son, vocal…)."""
        try:
            from src.ui.ui_bridge import send_user_input
            send_user_input(cmd)
        except Exception:
            pass

    def _refresh_background(self) -> None:
        engine = get_avatar_engine()
        engine.set_background(location=self._location)

    def set_location(self, location: str) -> None:
        self._location = location
        engine = get_avatar_engine()
        engine.set_background(location=location)

    def on_stop(self) -> None:
        """Libère la caméra à la fermeture de l'app."""
        if self._layout:
            self._layout.avatar_area.stop_camera()

    def _demo_tick(self, dt: float) -> None:
        state = self._demo_states[self._demo_idx % len(self._demo_states)]
        self._demo_idx += 1

        engine = get_avatar_engine()
        engine.set_state(state)

        if self._layout:
            desc = engine._controller.get_animation_descriptor(state)
            self._layout.add_alfred_message(
                f"[{state}] {desc.get('description', '')}"
            )


# ============================================================
# Entrée standalone
# ============================================================

if __name__ == "__main__":
    AlfredApp(demo_mode=True, location="salon").run()
