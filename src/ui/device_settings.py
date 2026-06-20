"""
PROJECT      : ALFRED
BLOCK        : B15 — Avatar & Interface
FILE         : src/ui/device_settings.py
ROLE         : Panneau de réglages devices — Caméra / Microphone / Sortie son

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-06-03
UPDATED      : 2026-06-20
VERSION      : V1.1
STATUS       : VALIDATED

DESCRIPTION :
Popup Kivy "Réglages devices" à la Google Meet.
Permet de choisir :
  - Caméra active (parmi les index disponibles) — nommage réel par hostname
  - Microphone d'entrée (sounddevice)
  - Sortie audio (sounddevice)

Nommage caméras (V1.1) :
  - Priorité 1 : labels utilisateur (data/settings/camera_labels.json, par hostname)
  - Priorité 2 : noms Windows PnP via PowerShell
  - Priorité 3 : "Caméra N WxH" générique
  - Bouton ✏️ Renommer dans le popup pour nommer sans éditer le JSON

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
# Labels caméra — identification par hostname + override manuel
# =============================================================================

try:
    from paths import PATHS
    _LABELS_FILE = PATHS.data / "settings" / "camera_labels.json"
except Exception:
    _LABELS_FILE = Path(__file__).parents[2] / "data" / "settings" / "camera_labels.json"


def _get_windows_camera_names() -> list[str]:
    """
    Récupère les noms réels des caméras via PowerShell (PnP Device Class=Camera).
    Retourne une liste ordonnée correspondant aux index DirectShow/cv2.
    Silencieux en cas d'échec.
    """
    try:
        import subprocess
        result = subprocess.run(
            [
                "powershell", "-NoProfile", "-NonInteractive", "-Command",
                "Get-PnpDevice -Class Camera -Status OK "
                "| Sort-Object InstanceId "
                "| Select-Object -ExpandProperty FriendlyName",
            ],
            capture_output=True, text=True, timeout=6, encoding="utf-8",
            errors="replace",
        )
        if result.returncode == 0:
            names = [l.strip() for l in result.stdout.strip().splitlines() if l.strip()]
            return names
    except Exception:
        pass
    return []


def load_camera_labels() -> dict[str, str]:
    """
    Charge les labels utilisateur depuis camera_labels.json.
    Format : {"hostname": {"0": "Caméra IA ALFRED", "1": "Intégrée PC", ...}}
    Retourne le dict index→label pour l'hostname courant.
    """
    import socket
    hostname = socket.gethostname().lower()
    try:
        if _LABELS_FILE.exists():
            data = json.loads(_LABELS_FILE.read_text(encoding="utf-8"))
            return {str(k): v for k, v in data.get(hostname, {}).items()}
    except Exception as exc:
        logger.warning("load_camera_labels: %s", exc)
    return {}


def save_camera_label(index: int, label: str) -> None:
    """Sauvegarde un label caméra pour l'hostname courant."""
    import socket
    hostname = socket.gethostname().lower()
    try:
        data: dict = {}
        if _LABELS_FILE.exists():
            data = json.loads(_LABELS_FILE.read_text(encoding="utf-8"))
        data.setdefault(hostname, {})[str(index)] = label
        _LABELS_FILE.parent.mkdir(parents=True, exist_ok=True)
        _LABELS_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    except Exception as exc:
        logger.warning("save_camera_label: %s", exc)


def _build_camera_label(index: int, w: int, h: int,
                        user_labels: dict[str, str],
                        win_names: list[str]) -> str:
    """
    Construit le label final d'une caméra dans cet ordre de priorité :
      1. Label utilisateur (camera_labels.json)
      2. Nom Windows PnP (PowerShell)
      3. "Caméra N  WxH" générique
    """
    # 1. Label utilisateur
    if str(index) in user_labels:
        label = user_labels[str(index)]
        if w and h:
            label += f"  {w}×{h}"
        return label

    # 2. Nom Windows (index dans la liste PnP ≈ index DSHOW)
    if index < len(win_names) and win_names[index]:
        label = win_names[index]
        if w and h:
            label += f"  {w}×{h}"
        return label

    # 3. Fallback générique
    label = f"Caméra {index}"
    if w and h:
        label += f"  {w}×{h}"
    return label


# =============================================================================
# Énumération des périphériques — indépendant de Kivy
# =============================================================================

def list_cameras() -> list[dict]:
    """
    Retourne la liste des caméras disponibles avec leurs vrais noms.
    Format : [{"index": 0, "name": "Trollino USB  640×480"}, ...]

    Priorité du nom :
      1. Label utilisateur (data/settings/camera_labels.json)
      2. Nom Windows PnP (PowerShell, automatique)
      3. "Caméra N  WxH" générique
    """
    user_labels = load_camera_labels()
    win_names   = _get_windows_camera_names()

    cameras = []
    try:
        import os as _os
        _os.environ.setdefault("OPENCV_LOG_LEVEL", "ERROR")
        import cv2
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
                label = _build_camera_label(i, w, h, user_labels, win_names)
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

    # Bouton "Renommer" — ouvre un TextInput pour labelliser la caméra sélectionnée
    def _on_rename(_inst) -> None:
        from kivy.uix.popup import Popup
        from kivy.uix.textinput import TextInput
        from kivy.uix.button import Button as _Btn
        from kivy.uix.boxlayout import BoxLayout as _Box

        # Retrouver l'index de la caméra sélectionnée
        sel_name = sp_cam.text
        sel_idx = next((c["index"] for c in cams if c["name"] == sel_name), -1)
        if sel_idx < 0:
            return

        # Nom actuel (sans la résolution)
        current_label = sel_name.split("  ")[0].strip()

        ti = TextInput(
            text=current_label,
            multiline=False,
            size_hint=(1, None), height=44,
            font_size="18sp",
            foreground_color=(0.9, 0.9, 0.95, 1),
            background_color=(0.08, 0.10, 0.18, 1),
            cursor_color=(0.54, 0.62, 0.83, 1),
        )
        btn_ok  = _Btn(text="✅ Sauvegarder", size_hint=(0.6, None), height=44,
                       background_color=(0.12, 0.30, 0.18, 1))
        btn_ann = _Btn(text="Annuler", size_hint=(0.4, None), height=44,
                       background_color=(0.10, 0.12, 0.20, 1))
        row  = _Box(orientation="horizontal", size_hint=(1, None), height=44, spacing=8)
        row.add_widget(btn_ok)
        row.add_widget(btn_ann)
        box = _Box(orientation="vertical", padding=16, spacing=10)
        box.add_widget(Label(
            text=f"Nouveau nom pour la caméra {sel_idx} :",
            size_hint=(1, None), height=36,
            color=(0.54, 0.62, 0.83, 1), font_size="16sp",
        ))
        box.add_widget(ti)
        box.add_widget(row)

        rename_popup = Popup(
            title="Renommer la caméra",
            content=box,
            size_hint=(0.85, None), height=220,
        )

        def _do_save(_i):
            new_label = ti.text.strip()
            if new_label:
                save_camera_label(sel_idx, new_label)
                # Rafraîchir l'entrée dans sp_cam visuellement
                new_name = new_label
                # Retrouver la résolution dans le nom original
                parts = sel_name.split("  ")
                if len(parts) > 1:
                    new_name += "  " + parts[-1]
                for cam in cams:
                    if cam["index"] == sel_idx:
                        cam["name"] = new_name
                        break
                new_cam_names = [c["name"] for c in cams]
                sp_cam.values = new_cam_names
                sp_cam.text   = new_name
            rename_popup.dismiss()

        btn_ok.bind(on_release=_do_save)
        btn_ann.bind(on_release=lambda *_: rename_popup.dismiss())
        rename_popup.open()

    btn_rename = Button(
        text="✏️ Renommer",
        size_hint=(1, None), height=36,
        background_color=(0.10, 0.12, 0.20, 1),
        color=_ACCENT,
        font_size="16sp",
    )
    btn_rename.bind(on_release=_on_rename)
    root.add_widget(btn_rename)

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
