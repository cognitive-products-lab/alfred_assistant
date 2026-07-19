"""
PROJECT      : ALFRED
BLOCK        : B15
FUNCTION     : 15.10
FILE         : tests/b15_tests/test_desktop_mic.py
ROLE         : Tests unitaires src/ui/desktop_mic.py

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-07-19
VERSION      : V1.0
STATUS       : TESTED

DESCRIPTION :
Capture micro push-to-talk, sans dépendre de matériel audio réel ni de
sounddevice/Kivy installés (sounddevice est injecté en faux module dans
sys.modules ; les appels à src.ui.alfred_app sont déjà avalés par un
try/except dans le code testé — voir desktop_mic.py — donc l'absence de
Kivy dans l'environnement de test n'affecte pas ces tests).
"""

import sys
import types

import numpy as np
import pytest

from src.ui import desktop_mic as mic


@pytest.fixture(autouse=True)
def _reset_module_state():
    mic._stream = None
    mic._frames = []
    yield
    mic._stream = None
    mic._frames = []


class _FakeInputStream:
    """Simule sd.InputStream : capture le callback, déclenche des frames à la demande."""
    instances = []

    def __init__(self, samplerate, channels, dtype, callback):
        self.callback = callback
        self.started = False
        self.stopped = False
        self.closed = False
        _FakeInputStream.instances.append(self)

    def start(self):
        self.started = True

    def stop(self):
        self.stopped = True

    def close(self):
        self.closed = True

    def emit_frame(self, n=10):
        self.callback(np.zeros((n, 1), dtype=np.float32), n, None, None)


@pytest.fixture
def fake_sounddevice(monkeypatch):
    _FakeInputStream.instances = []
    fake_sd = types.SimpleNamespace(InputStream=_FakeInputStream)
    monkeypatch.setitem(sys.modules, "sounddevice", fake_sd)
    yield fake_sd


# =============================================================================
# start_recording
# =============================================================================

def test_start_recording_succeeds_and_starts_stream(fake_sounddevice):
    result = mic.start_recording()
    assert result == {"ok": True}
    assert len(_FakeInputStream.instances) == 1
    assert _FakeInputStream.instances[0].started is True


def test_start_recording_fails_when_sounddevice_missing(monkeypatch):
    monkeypatch.setitem(sys.modules, "sounddevice", None)
    result = mic.start_recording()
    assert result["ok"] is False
    assert "error" in result


def test_start_recording_fails_when_input_stream_raises(monkeypatch):
    class _BoomStream:
        def __init__(self, **kwargs):
            raise OSError("device busy")

    fake_sd = types.SimpleNamespace(InputStream=_BoomStream)
    monkeypatch.setitem(sys.modules, "sounddevice", fake_sd)
    result = mic.start_recording()
    assert result["ok"] is False
    assert "device busy" in result["error"]


# =============================================================================
# stop_recording
# =============================================================================

def test_stop_recording_without_prior_start_returns_no_audio_error():
    result = mic.stop_recording()
    assert result == {"ok": False, "error": "Aucun audio capturé"}


def test_stop_recording_with_no_frames_captured_returns_error(fake_sounddevice):
    mic.start_recording()
    # aucune frame émise avant l'arrêt
    result = mic.stop_recording()
    assert result["ok"] is False
    assert result["error"] == "Aucun audio capturé"
    assert _FakeInputStream.instances[0].stopped is True
    assert _FakeInputStream.instances[0].closed is True


def test_stop_recording_transcribes_captured_audio(fake_sounddevice, monkeypatch):
    mic.start_recording()
    _FakeInputStream.instances[0].emit_frame(16)

    monkeypatch.setattr("src.main._transcribe_audio", lambda audio: "rappelle-moi demain")
    result = mic.stop_recording()

    assert result == {"ok": True, "text": "rappelle-moi demain"}


def test_stop_recording_reports_empty_transcription(fake_sounddevice, monkeypatch):
    mic.start_recording()
    _FakeInputStream.instances[0].emit_frame(16)

    monkeypatch.setattr("src.main._transcribe_audio", lambda audio: "")
    result = mic.stop_recording()

    assert result == {"ok": False, "error": "empty"}


def test_stop_recording_handles_transcription_exception(fake_sounddevice, monkeypatch):
    mic.start_recording()
    _FakeInputStream.instances[0].emit_frame(16)

    def _boom(audio):
        raise RuntimeError("modèle Whisper indisponible")

    monkeypatch.setattr("src.main._transcribe_audio", _boom)
    result = mic.stop_recording()

    assert result["ok"] is False
    assert "modèle Whisper indisponible" in result["error"]


def test_stop_recording_resets_state_for_next_recording(fake_sounddevice, monkeypatch):
    mic.start_recording()
    _FakeInputStream.instances[0].emit_frame(16)
    monkeypatch.setattr("src.main._transcribe_audio", lambda audio: "premier message")
    mic.stop_recording()

    assert mic._stream is None
    assert mic._frames == []
