"""
PROJECT      : ALFRED
BLOCK        : GLOBAL
FUNCTION     : TESTS
FILE         : tests/test_tts_engine.py
ROLE         : Test du TTSEngine avec backend Piper

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-06-03
UPDATED      : 2026-06-13
VERSION      : V1.1
STATUS       : ACTIVE
"""

from __future__ import annotations

import sys
import time
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.conversation.output.tts_engine import TTSEngine
from src.conversation.output.tts_piper import PiperTTS, is_tts_available


def test_tts_engine_speak():
    if not is_tts_available():
        pytest.skip("Backend Piper indisponible")

    tts = TTSEngine(backend=PiperTTS())

    # Le périphérique audio peut être momentanément occupé par un test
    # précédent (sounddevice) — on retente avant de déclarer un échec.
    success = False
    for attempt in range(3):
        success = tts.speak("Bonjour Céline. Test du moteur vocal Alfred.")
        if success:
            break
        time.sleep(3)

    assert success is True
