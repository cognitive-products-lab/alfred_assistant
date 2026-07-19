"""
PROJECT      : ALFRED
BLOCK        : B15
FUNCTION     : 15.12
FILE         : tests/b15_tests/test_desktop_tts_control.py
ROLE         : Tests unitaires src/ui/desktop_tts_control.py

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-07-19
VERSION      : V1.0
STATUS       : TESTED

DESCRIPTION :
Interruption réelle du TTS — sd.stop() (mock, pas de matériel audio requis),
levée du drapeau components["_interrupted"], reset de l'état visuel avatar.
sounddevice est injecté en faux module (voir test_desktop_mic.py) ; l'appel
à src.ui.alfred_app.set_ui_speaking échoue silencieusement sans Kivy
installé, ce qui est le comportement attendu (try/except déjà dans le code
testé) — non re-vérifié ici, déjà couvert par la conception du module.
"""

import sys
import types

import pytest

import src.main as main_module
from src.ui import desktop_tts_control as tts_control


@pytest.fixture
def fake_sounddevice(monkeypatch):
    calls = {"stop": 0}
    fake_sd = types.SimpleNamespace(stop=lambda: calls.__setitem__("stop", calls["stop"] + 1))
    monkeypatch.setitem(sys.modules, "sounddevice", fake_sd)
    return calls


def test_interrupt_speech_calls_sd_stop(fake_sounddevice, monkeypatch):
    monkeypatch.setattr(main_module, "get_live_components", lambda: None)
    result = tts_control.interrupt_speech()
    assert result == {"ok": True}
    assert fake_sounddevice["stop"] == 1


def test_interrupt_speech_survives_missing_sounddevice(monkeypatch):
    monkeypatch.setitem(sys.modules, "sounddevice", None)
    monkeypatch.setattr(main_module, "get_live_components", lambda: None)
    result = tts_control.interrupt_speech()
    assert result == {"ok": True}


def test_interrupt_speech_sets_interrupted_flag_on_live_components():
    components = {}
    import types as _types
    import unittest.mock as mock

    with mock.patch.object(main_module, "get_live_components", return_value=components):
        tts_control.interrupt_speech()

    assert components["_interrupted"] is True


def test_interrupt_speech_resets_avatar_end_response():
    calls = {"end_response": 0}
    avatar = types.SimpleNamespace(end_response=lambda: calls.__setitem__("end_response", 1))
    components = {"avatar": avatar}
    import unittest.mock as mock

    with mock.patch.object(main_module, "get_live_components", return_value=components):
        tts_control.interrupt_speech()

    assert calls["end_response"] == 1


def test_interrupt_speech_survives_avatar_end_response_exception():
    avatar = types.SimpleNamespace(end_response=lambda: (_ for _ in ()).throw(RuntimeError("boom")))
    components = {"avatar": avatar}
    import unittest.mock as mock

    with mock.patch.object(main_module, "get_live_components", return_value=components):
        result = tts_control.interrupt_speech()

    assert result == {"ok": True}


def test_interrupt_speech_handles_no_live_components(monkeypatch):
    monkeypatch.setattr(main_module, "get_live_components", lambda: None)
    result = tts_control.interrupt_speech()
    assert result == {"ok": True}
