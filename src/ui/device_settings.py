"""
PROJECT      : ALFRED
BLOCK        : B15 — Avatar & Interface
FILE         : src/ui/device_settings.py
ROLE         : Panneau de réglages devices — Caméra / Microphone / Sortie son

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-06-03
VERSION      : V1.0
STATUS       : ACTIVE

DESCRIPTION :
Popup Kivy "Réglages devices" à la Google Meet.
Permet de choisir :
  - Caméra active (parmi les index disponibles)
  - Microphone d'entrée (sounddevice)
  - Sortie audio (sounddevice)

Persistance JSON : data/settings/device_settings.json
Chargé au démarrage, appliqué immédiatement à WebcamWidget + sounddevice.
"""

from __future__ import annotations

import json
import logging
import threading
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)

# ── Chemins ───────────────────────────────────────────────────────────────────
try:
    from paths import PATHS
    _SETTINGS_FILE = PATHS.data / "settings" / "device_settings.json"
except Exception:
    _SETTINGS_FILE = Path(__file__).parents[2] / "data" / "settings" / "device_settings.json"


# =============================================================================
# Énumération des périphériques — indépendant de Kivy
# =============================================================================

def list_cameras() -> list[dict]:
    """
    Retourne la liste des caméras disponibles.
    Format : [{"index": 0, "name": "Caméra 0 (intégrée)"}, ...]
    """
    cameras = []
    try:
        import os as _os
        # Supprime les warnings obsensor/ffmpeg lors du scan des indices
        _os.environ.setdefault("OPENCV_LOG_LEVEL", "ERROR")
        import cv2
        # CAP_DSHOW : sur Windows, le backend par défaut (MSMF) peut "ouvrir"
        # un index sans caméra réelle (isOpened=True mais aucune image lue).
        # DSHOW énumère correctement les caméras USB branchées.
        backend = cv2.CAP_DSHOW if hasattr(cv2, "CAP_DSHOW") else cv2.CAP_ANY
        for i in range(6):
            cap = cv2.VideoCapture(i, backend)
            if cap.isOpened():
                ret, _frame = cap.read()
                if not ret:
                    cap.release()
                    continue
                w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                # Pas de label "(intégrée)" : l'ordre des index DSHOW n'est pas
                # garanti (l'index 0 n'est pas forcément la caméra intégrée).
                label = f"Caméra {i}"
                if w and h:
                    label += f"  {w}×{h}"
                cameras.append({"index": i, "name": label})
                cap.release()
    except ImportError:
        cameras.append({"index": 0, "name": "Caméra 0 (OpenCV non installé)"})
    except Exception as exc:
        logger.warning("list_cameras: %s", exc)

    if not cameras:
        cameras.append({"index": -1, "name": "Aucune caméra détectée"})

    return cameras


def list_audio_inputs() -> list[dict]:
    """
    Retourne la liste des microphones disponibles.
    Format : [{"index": 0, "name": "Microphone USB"}, ...]
    """
    devices = []
    try:
        import sounddevice as sd
        for i, dev in enumerate(sd.query_devices()):
            if dev["max_input_channels"] > 0:
                devices.append({"index": i, "name": dev["name"]})
    except ImportError:
        devices.append({"index": -1, "name": "sounddevice non installé"})
    except Exception as exc:
        logger.warning("list_audio_inputs: %s", exc)

    if not devices:
        devices.append({"index": -1, "name": "Aucun microphone détecté"})

    return devices


def list_audio_outputs() -> list[dict]:
    """
    Retourne la liste des sorties audio disponibles.
    Format : [{"index": 0, "name": "Haut-parleurs"}, ...]
    """
    devices = []
    try:
        import sounddevice as sd
        for i, dev in enumerate(sd.query_devices()):
            if dev["max_output_channels"] > 0:
                devices.append({"index": i, "name": dev["name"]})
    except ImportError:
        devices.append({"index": -1, "name": "sounddevice non installé"})
    except Exception as exc:
        logger.warning("list_audio_outputs: %s", exc)

    if not devices:
        devices.append({"index": -1, "name": "Aucune sortie détectée"})

    return devices


# =============================================================================
# Cache / pré-chargement asynchrone
# =============================================================================
# Le scan OpenCV des index caméra (cv2.VideoCapture(0..5)) bloque ~1-2s par
# index sur certains systèmes. Si on l'exécute dans le thread principal Kivy
# au clic sur "Réglages", l'UI freeze. On le pré-calcule donc dans un thread
# daemon au démarrage, et le popup utilise ce cache (avec fallback live si
# le scan n'est pas encore terminé).

_device_cache: dict[str, list[dict]] = {}
_device_cache_lock = threading.Lock()


def prefetch_devices_async() -> None:
    """Lance le scan caméra/audio dans un thread daemon et remplit le cache."""

    def _scan() -> None:
        cams = list_cameras()
        inputs = list_audio_inputs()
        outputs = list_audio_outputs()
        with _device_cache_lock:
            _device_cache["cameras"] = cams
            _device_cache["audio_inputs"] = inputs
            _device_cache["audio_outputs"] = outputs
        logger.info("prefetch_devices_async : cache rempli")

    threading.Thread(target=_scan, name="device-scan", daemon=True).start()


def get_cached_cameras() -> list[dict]:
    """Retourne les caméras du cache si dispo, sinon scan synchrone (fallback)."""
    with _device_cache_lock:
        cached = _device_cache.get("cameras")
    return cached if cached is not None else list_cameras()


def get_cached_audio_inputs() -> list[dict]:
    """Retourne les micros du cache si dispo, sinon scan synchrone (fallback)."""
    with _device_cache_lock:
        cached = _device_cache.get("audio_inputs")
    return cached if cached is not None else list_audio_inputs()


def get_cached_audio_outputs() -> list[dict]:
    """Retourne les sorties audio du cache si dispo, sinon scan synchrone (fallback)."""
    with _device_cache_lock:
        cached = _device_cache.get("audio_outputs")
    return cached if cached is not None else list_audio_outputs()


# =============================================================================
# Persistance
# =============================================================================

_DEFAULTS = {
    "camera_index": 0,
    "audio_input_index": -1,   # -1 = défaut système
    "audio_output_index": -1,  # -1 = défaut système
}


def settings_file_exists() -> bool:
    """True si le fichier device_settings.json existe déjà (réglages déjà faits)."""
    return _SETTINGS_FILE.exists()


def load_device_settings() -> dict:
    """Charge les réglages depuis JSON (crée avec défauts si absent)."""
    try:
        if _SETTINGS_FILE.exists():
            data = json.loads(_SETTINGS_FILE.read_text(encoding="utf-8"))
            return {**_DEFAULTS, **data}
    except Exception as exc:
        logger.warning("load_device_settings: %s", exc)
    return dict(_DEFAULTS)


def save_device_settings(settings: dict) -> None:
    """Sauvegarde les réglages dans JSON."""
    try:
        _SETTINGS_FILE.parent.mkdir(parents=True, exist_ok=True)
        _SETTINGS_FILE.write_text(
            json.dumps(settings, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        logger.info("Réglages devices sauvegardés : %s", settings)
    except Exception as exc:
        logger.error("save_device_settings: %s", exc)


def apply_audio_settings(settings: dict) -> None:
    """
    Applique les réglages audio à sounddevice (micro + sortie).
    Index -1 = défaut système → ne pas toucher.
    """
    try:
        import sounddevice as sd
        in_idx  = settings.get("audio_input_index",  -1)
        out_idx = settings.get("audio_output_index", -1)
        if in_idx >= 0:
            sd.default.device[0] = in_idx
        if out_idx >= 0:
            sd.default.device[1] = out_idx
    except ImportError:
        pass
    except Exception as exc:
        logger.warning("apply_audio_settings: %s", exc)


# =============================================================================
# Popup Kivy
# =============================================================================

def _build_popup(on_apply) -> "Popup":  # type: ignore[name-defined]
    """Construit et retourne le popup Kivy de réglages devices."""
    from kivy.uix.popup import Popup
    from kivy.uix.boxlayout import BoxLayout
    from kivy.uix.label import Label
    from kivy.uix.button import Button
    from kivy.uix.spinner import Spinner
    from kivy.uix.widget import Widget
    from kivy.graphics import Color, RoundedRectangle

    # Charger les périphériques (cache pré-calculé si dispo) et les réglages courants
    cams    = get_cached_cameras()
    inputs  = get_cached_audio_inputs()
    outputs = get_cached_audio_outputs()
    current = load_device_settings()

    # Couleurs palette ALFRED
    _CLR_BG      = (0.05, 0.06, 0.12, 1)
    _CLR_BTN     = (0.10, 0.12, 0.20, 1)
    _CLR_BTN_OK  = (0.12, 0.30, 0.18, 1)
    _FG          = (0.88, 0.88, 0.92, 1)
    _ACCENT      = (0.54, 0.62, 0.83, 1)

    # ── Helpers ───────────────────────────────────────────────────────────────
    def _find_name(lst: list[dict], idx: int) -> str:
        for item in lst:
            if item["index"] == idx:
                return item["name"]
        return lst[0]["name"] if lst else "—"

    def _make_spinner(values: list[str], current_val: str) -> Spinner:
        sp = Spinner(
            text=current_val,
            values=values,
            size_hint=(1, None),
            height=44,
            background_color=_CLR_BTN,
            color=_FG,
            font_size="18sp",
        )
        return sp

    def _make_label(text: str) -> Label:
        return Label(
            text=text,
            size_hint=(1, None),
            height=32,
            color=_ACCENT,
            font_size="17sp",
            halign="left",
            text_size=(None, None),
        )

    # ── Layout principal ──────────────────────────────────────────────────────
    root = BoxLayout(
        orientation="vertical",
        padding=[16, 12],
        spacing=8,
    )

    with root.canvas.before:
        Color(*_CLR_BG)
        _bg = RoundedRectangle(pos=root.pos, size=root.size, radius=[10])
    root.bind(
        pos=lambda *_: setattr(_bg, "pos", root.pos),
        size=lambda *_: setattr(_bg, "size", root.size),
    )

    # Titre
    root.add_widget(Label(
        text="Réglages — Périphériques",
        size_hint=(1, None), height=40,
        color=_FG, font_size="20sp", bold=True,
    ))

    # ── Caméra ────────────────────────────────────────────────────────────────
    root.add_widget(_make_label("📷  Caméra"))
    cam_names = [c["name"] for c in cams]
    sp_cam = _make_spinner(cam_names, _find_name(cams, current["camera_index"]))
    root.add_widget(sp_cam)

    # ── Microphone ────────────────────────────────────────────────────────────
    root.add_widget(_make_label("🎤  Microphone"))
    in_names = [d["name"] for d in inputs]
    sp_in = _make_spinner(in_names, _find_name(inputs, current["audio_input_index"]))
    root.add_widget(sp_in)

    # ── Sortie son ────────────────────────────────────────────────────────────
    root.add_widget(_make_label("🔊  Sortie son"))
    out_names = [d["name"] for d in outputs]
    sp_out = _make_spinner(out_names, _find_name(outputs, current["audio_output_index"]))
    root.add_widget(sp_out)

    # ── Séparateur ───────────────────────────────────────────────────────────
    root.add_widget(Widget(size_hint=(1, 1)))   # spacer flexible

    # ── Boutons ───────────────────────────────────────────────────────────────
    btn_row = BoxLayout(
        orientation="horizontal",
        size_hint=(1, None), height=48, spacing=8,
    )

    popup_ref: list = []   # référence au popup pour le fermer depuis les callbacks

    def _on_apply(_inst) -> None:
        """Lit les spinners, construit le dict settings, applique + sauvegarde."""
        def _idx_from_name(lst: list[dict], name: str) -> int:
            for item in lst:
                if item["name"] == name:
                    return item["index"]
            return -1

        new_settings = {
            "camera_index":       _idx_from_name(cams,    sp_cam.text),
            "audio_input_index":  _idx_from_name(inputs,  sp_in.text),
            "audio_output_index": _idx_from_name(outputs, sp_out.text),
        }
        save_device_settings(new_settings)
        apply_audio_settings(new_settings)
        if on_apply:
            on_apply(new_settings)
        if popup_ref:
            popup_ref[0].dismiss()

    def _on_cancel(_inst) -> None:
        if popup_ref:
            popup_ref[0].dismiss()

    btn_apply = Button(
        text="✅ Appliquer",
        size_hint=(0.6, 1),
        background_color=_CLR_BTN_OK,
        color=_FG, font_size="18sp",
    )
    btn_apply.bind(on_release=_on_apply)

    btn_cancel = Button(
        text="Annuler",
        size_hint=(0.4, 1),
        background_color=_CLR_BTN,
        color=_FG, font_size="18sp",
    )
    btn_cancel.bind(on_release=_on_cancel)

    btn_row.add_widget(btn_apply)
    btn_row.add_widget(btn_cancel)
    root.add_widget(btn_row)

    # ── Popup ─────────────────────────────────────────────────────────────────
    popup = Popup(
        title="",
        content=root,
        size_hint=(None, None),
        size=(400, 440),
        separator_height=0,
        background="",
        background_color=(0, 0, 0, 0),   # fond transparent (notre canvas)
        overlay_color=(0, 0, 0, 0.65),
        auto_dismiss=True,
    )
    popup_ref.append(popup)
    return popup


def open_settings_popup(on_apply=None) -> None:
    """
    Ouvre le popup de réglages devices.
    Doit être appelé depuis le thread principal Kivy (ou via Clock.schedule_once).

    Args:
        on_apply : callback(settings_dict) appelé quand l'utilisateur clique Appliquer
    """
    try:
        popup = _build_popup(on_apply=on_apply)
        popup.open()
    except Exception as exc:
        logger.error("open_settings_popup: %s", exc)
