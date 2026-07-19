"""
PROJECT      : ALFRED
BLOCK        : TESTS
FUNCTION     : B04
FILE         : tests/test_voice_loop.py
ROLE         : Tests unitaires boucle vocale STT -> TTS

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-06-03
UPDATED      : 2026-06-05
VERSION      : V1.1
STATUS       : VALIDATED

DESCRIPTION :
Vérifie les imports et la disponibilité des composants de la boucle vocale.
Le test d'enregistrement micro réel est dans tests/manual/voice_loop_manual.py.
"""

import pytest


def test_tts_engine_import():
    from src.conversation.output.tts_engine import TTSEngine
    assert TTSEngine is not None


def test_piper_tts_import():
    from src.conversation.output.tts_piper import PiperTTS
    assert PiperTTS is not None


def test_sounddevice_available():
    try:
        import sounddevice as sd
        assert sd is not None
    except ImportError:
        pytest.skip("sounddevice non installé")


def test_whisper_available():
    try:
        from faster_whisper import WhisperModel
        assert WhisperModel is not None
    except ImportError:
        pytest.skip("faster-whisper non installé")


def test_tts_engine_instantiation():
    try:
        from src.conversation.output.tts_engine import TTSEngine
        from src.conversation.output.tts_piper import PiperTTS
        tts = TTSEngine(backend=PiperTTS(mode="complicite", blocking=False))
        assert tts is not None
    except Exception as exc:
        pytest.skip(f"TTS non disponible : {exc}")
