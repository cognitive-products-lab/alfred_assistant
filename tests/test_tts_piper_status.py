"""
PROJECT      : ALFRED
BLOCK        : GLOBAL
FUNCTION     : TESTS
FILE         : tests/test_tts_piper_status.py
ROLE         : Test du statut du backend Piper TTS

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-06-03
UPDATED      : 2026-06-13
VERSION      : V1.1
STATUS       : TESTED
"""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.conversation.output.tts_piper import get_tts_status, is_tts_available


def test_tts_available_is_bool():
    assert isinstance(is_tts_available(), bool)


def test_tts_status_structure():
    status = get_tts_status()

    assert isinstance(status, dict)
    for key in ("available", "piper_ready", "model", "sample_rate"):
        assert key in status


def test_tts_status_consistent_with_availability():
    status = get_tts_status()
    assert status["available"] == is_tts_available()
