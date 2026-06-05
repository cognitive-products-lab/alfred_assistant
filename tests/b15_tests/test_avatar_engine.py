"""
PROJECT      : ALFRED
BLOCK        : B15
FUNCTION     : 15.05
FILE         : tests/b15_tests/test_avatar_engine.py
ROLE         : Tests unitaires src/ui/avatar_engine.py

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-06-05
UPDATED      : 2026-06-05
VERSION      : V1.0
STATUS       : TESTED
"""

import importlib
import pytest
import src.ui.avatar_engine as _mod
from src.ui.avatar_engine import get_avatar_engine


@pytest.fixture(autouse=True)
def reset_engine():
    importlib.reload(_mod)
    yield


def test_singleton():
    e1 = _mod.get_avatar_engine()
    e2 = _mod.get_avatar_engine()
    assert e1 is e2


def test_start_does_not_raise():
    engine = _mod.get_avatar_engine()
    engine.start()
    engine.start(renderer=None)


def test_set_state():
    engine = _mod.get_avatar_engine()
    engine.set_state("speaking")
    assert engine._controller.current_state.mode == "speaking"


def test_set_emotion():
    engine = _mod.get_avatar_engine()
    engine.set_emotion("joie")
    assert engine._controller.current_state.emotion == "joie"


def test_set_listening():
    engine = _mod.get_avatar_engine()
    engine.set_listening(True)
    assert engine._controller.current_state.mode == "listening"


def test_set_speaking():
    engine = _mod.get_avatar_engine()
    engine.set_speaking(True)
    assert engine._controller.current_state.mode == "speaking"


def test_set_idle():
    engine = _mod.get_avatar_engine()
    engine.set_state("speaking")
    engine.set_idle()
    assert engine._controller.current_state.mode == "idle"


def test_begin_end_response():
    engine = _mod.get_avatar_engine()
    engine.begin_response()
    assert engine._controller.current_state.mode == "speaking"
    engine.end_response()
    assert engine._controller.current_state.mode == "idle"


def test_set_mode():
    engine = _mod.get_avatar_engine()
    engine.set_mode("focus")
    assert engine._controller.current_state.mode == "focus"


def test_register_hook_called():
    engine = _mod.get_avatar_engine()
    calls = []
    engine.register_hook(lambda s: calls.append(s))
    engine.set_state("thinking")
    assert "thinking" in calls


def test_set_background_does_not_raise():
    engine = _mod.get_avatar_engine()
    engine.set_background(location="salon", period="soir")
