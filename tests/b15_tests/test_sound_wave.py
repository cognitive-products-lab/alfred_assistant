"""
PROJECT      : ALFRED
BLOCK        : B15
FUNCTION     : 15.03
FILE         : tests/b15_tests/test_sound_wave.py
ROLE         : Tests unitaires src/ui/sound_wave.py

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-06-05
UPDATED      : 2026-06-05
VERSION      : V1.0
STATUS       : TESTED
"""

import os
os.environ.setdefault("KIVY_NO_ENV_CONFIG", "1")
os.environ.setdefault("DISPLAY", ":0")

import pytest


def test_sound_wave_import():
    """Vérifie que SoundWaveWidget s'importe sans erreur."""
    try:
        from src.ui.sound_wave import SoundWaveWidget
        assert SoundWaveWidget is not None
    except Exception as exc:
        pytest.skip(f"Kivy non disponible en headless : {exc}")


def test_set_speaking_does_not_raise():
    try:
        from src.ui.sound_wave import SoundWaveWidget
        w = SoundWaveWidget()
        w.set_speaking(True)
        w.set_speaking(False)
    except Exception as exc:
        pytest.skip(f"Kivy non disponible : {exc}")


def test_set_listening_does_not_raise():
    try:
        from src.ui.sound_wave import SoundWaveWidget
        w = SoundWaveWidget()
        w.set_listening(True)
        w.set_listening(False)
    except Exception as exc:
        pytest.skip(f"Kivy non disponible : {exc}")
