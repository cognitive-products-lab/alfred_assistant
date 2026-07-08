"""
PROJECT      : ALFRED
BLOCK        : GLOBAL
FUNCTION     : TESTS
FILE         : tests/test_micro.py
ROLE         : Tests de la chaine d'acquisition micro (volume / device)

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-06-03
UPDATED      : 2026-06-13
VERSION      : V2.0
STATUS       : TESTED

DESCRIPTION :
Verifie que sounddevice expose des peripheriques audio et que le calcul
de volume moyen fonctionne, sans enregistrement micro reel (signal
synthetique pour rester compatible CI / environnements non interactifs).
"""

from __future__ import annotations

import numpy as np
import sounddevice as sd

SAMPLERATE = 16000
DURATION = 1


def _mean_volume(audio: np.ndarray) -> float:
    return float(np.abs(audio).mean())


def test_sounddevice_lists_devices():
    devices = sd.query_devices()
    assert devices is not None
    assert len(devices) > 0


def test_volume_detection_on_silence():
    audio = np.zeros(int(DURATION * SAMPLERATE), dtype="float32")
    assert _mean_volume(audio) == 0.0


def test_volume_detection_on_signal():
    t = np.linspace(0, DURATION, int(DURATION * SAMPLERATE), endpoint=False)
    audio = (0.5 * np.sin(2 * np.pi * 440 * t)).astype("float32")
    assert _mean_volume(audio) > 0.001
