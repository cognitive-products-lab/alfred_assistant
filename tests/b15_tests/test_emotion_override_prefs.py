"""
PROJECT      : ALFRED
BLOCK        : B15
FUNCTION     : 15.06
FILE         : tests/b15_tests/test_emotion_override_prefs.py
ROLE         : Tests unitaires src/ui/emotion_override_prefs.py

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-07-19
VERSION      : V1.0
STATUS       : TESTED

DESCRIPTION :
Persistance de la correction/désactivation manuelle du widget dashboard
"État émotionnel" — défauts, roundtrip, effet couplé enabled/manual_mood.
"""

import shutil
import tempfile
from pathlib import Path

import pytest

from src.ui import emotion_override_prefs as eop


@pytest.fixture(autouse=True)
def _isolated_file(monkeypatch):
    tmp_dir = Path(tempfile.mkdtemp(prefix="alfred_emotion_override_"))
    fake_file = tmp_dir / "emotion_override.json"
    monkeypatch.setattr(eop, "_OVERRIDE_FILE", fake_file)
    yield fake_file
    shutil.rmtree(tmp_dir, ignore_errors=True)


def test_defaults_when_file_absent():
    state = eop.load_emotion_override()
    assert state == {"enabled": True, "manual_mood": None, "manual_set_at": None}


def test_save_enabled_false_roundtrip():
    eop.save_emotion_override(enabled=False)
    state = eop.load_emotion_override()
    assert state["enabled"] is False


def test_manual_mood_implicitly_re_enables():
    eop.save_emotion_override(enabled=False)
    state = eop.save_emotion_override(manual_mood="Fatigué(e)")
    assert state["enabled"] is True
    assert state["manual_mood"] == "Fatigué(e)"
    assert state["manual_set_at"] is not None


def test_clear_manual_mood_keeps_enabled_state():
    eop.save_emotion_override(manual_mood="Calme")
    state = eop.clear_manual_mood()
    assert state["manual_mood"] is None
    assert state["manual_set_at"] is None
    assert state["enabled"] is True


def test_partial_file_merges_with_defaults(_isolated_file):
    _isolated_file.parent.mkdir(parents=True, exist_ok=True)
    _isolated_file.write_text('{"enabled": false}', encoding="utf-8")
    state = eop.load_emotion_override()
    assert state["enabled"] is False
    assert state["manual_mood"] is None


def test_corrupted_file_falls_back_to_defaults(_isolated_file):
    _isolated_file.parent.mkdir(parents=True, exist_ok=True)
    _isolated_file.write_text("not valid json{{{", encoding="utf-8")
    state = eop.load_emotion_override()
    assert state == dict(eop._DEFAULTS)
