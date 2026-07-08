"""
PROJECT      : ALFRED
BLOCK        : GLOBAL
FUNCTION     : TESTS
FILE         : tests/test_stt.py
ROLE         : Test du moteur STT (faster-whisper)

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-06-03
UPDATED      : 2026-06-13
VERSION      : V2.0
STATUS       : TESTED

DESCRIPTION :
Verifie que le modele Whisper se charge et transcrit un signal audio
synthetique sans erreur, sans enregistrement micro reel (signal
synthetique pour rester compatible CI / environnements non interactifs).
Skip si le modele n'est pas disponible localement (pas de connexion /
droits insuffisants pour le telecharger).
"""

from __future__ import annotations

import numpy as np
import pytest

SAMPLERATE = 16000
DURATION = 1


@pytest.fixture(scope="module")
def whisper_model():
    from faster_whisper import WhisperModel

    try:
        return WhisperModel("base", compute_type="int8")
    except Exception as exc:
        pytest.skip(f"Modèle Whisper indisponible : {exc}")


def test_whisper_transcribe_runs(whisper_model):
    audio = np.zeros(int(DURATION * SAMPLERATE), dtype="float32")

    segments, info = whisper_model.transcribe(audio, language="fr")

    assert info is not None
    assert list(segments) is not None
