"""
PROJECT      : ALFRED
BLOCK        : B15 — Avatar & Interface
FILE         : src/ui/desktop_mic.py
ROLE         : Capture micro push-to-talk pour le mode vocal de l'interface desktop HTML

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-07-19
VERSION      : V1.0
STATUS       : DRAFT

DESCRIPTION :
Reprend le pattern déjà fonctionnel de InputRow._start_recording/_stop_recording
dans src/ui/alfred_app.py (Kivy) : sd.InputStream 16kHz mono, durée libre,
transcription via src.main._transcribe_audio (faster-whisper) à l'arrêt.
Push-to-talk uniquement (pas d'écoute continue) — même choix de
confidentialité que la version Kivy.

Ce module ne connaît rien de pywebview : il parle uniquement à
src.ui.alfred_app (set_ui_listening / set_ui_voice_error), exactement comme
tout autre module UI-facing du projet. AlfredDesktopAPI (alfred_desktop.py)
l'appelle depuis le thread pywebview via start_recording()/stop_recording().
"""

from __future__ import annotations

import threading

_stream = None
_frames: list = []
_lock = threading.Lock()


def _set_ui_listening(active: bool) -> None:
    try:
        from src.ui.alfred_app import set_ui_listening
        set_ui_listening(active)
    except Exception:
        pass


def _emit_error(message: str) -> None:
    try:
        from src.ui.alfred_app import set_ui_voice_error
        set_ui_voice_error(message)
    except Exception:
        pass


def start_recording() -> dict:
    """Démarre la capture micro. Retourne {"ok": bool, "error"?: str}."""
    global _stream, _frames
    try:
        import sounddevice as sd
    except Exception as exc:
        _emit_error(f"Micro indisponible : {exc}")
        return {"ok": False, "error": str(exc)}

    with _lock:
        _frames = []

        def _callback(indata, frame_count, time_info, status) -> None:
            with _lock:
                _frames.append(indata.copy())

        try:
            stream = sd.InputStream(
                samplerate=16000,
                channels=1,
                dtype="float32",
                callback=_callback,
            )
            stream.start()
        except Exception as exc:
            _emit_error(f"Micro indisponible : {exc}")
            return {"ok": False, "error": str(exc)}
        _stream = stream

    _set_ui_listening(True)
    return {"ok": True}


def stop_recording() -> dict:
    """
    Arrête la capture et transcrit l'audio (synchrone — faster-whisper "small"
    int8 est assez rapide pour ne pas bloquer notablement l'appel JS→Python).
    Retourne {"ok": True, "text": str} ou {"ok": False, "error": str}.
    """
    global _stream, _frames

    with _lock:
        stream, _stream = _stream, None
        frames, _frames = _frames, []

    _set_ui_listening(False)

    if stream is not None:
        try:
            stream.stop()
            stream.close()
        except Exception:
            pass

    if not frames:
        _emit_error("Aucun audio capturé.")
        return {"ok": False, "error": "Aucun audio capturé"}

    import numpy as np
    audio = np.concatenate(frames, axis=0)

    try:
        from src.main import _transcribe_audio
        text = _transcribe_audio(audio)
    except Exception as exc:
        _emit_error(f"Transcription impossible : {exc}")
        return {"ok": False, "error": str(exc)}

    if not text:
        _emit_error("Rien n'a été compris, réessayez.")
        return {"ok": False, "error": "empty"}

    return {"ok": True, "text": text}
