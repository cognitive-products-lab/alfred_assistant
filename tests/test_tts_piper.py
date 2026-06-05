"""
PROJECT      : ALFRED
BLOCK        : TESTS
FUNCTION     : B04
FILE         : tests/test_tts_piper.py
ROLE         : Tests unitaires Piper TTS CLI

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-06-03
UPDATED      : 2026-06-05
VERSION      : V1.1
STATUS       : TESTED

DESCRIPTION :
Vérifie que piper.exe est accessible, que le modèle vocal existe
et qu'une synthèse simple génère un fichier audio.
"""

import subprocess
from pathlib import Path
import pytest

PIPER_PATH  = Path("D:/PROJET_ALFRED/ALFRED_PC/tools/piper/piper.exe")
MODEL_PATH  = Path("D:/PROJET_ALFRED/ALFRED_PC/tools/piper/models/fr_FR-upmc-medium.onnx")
OUTPUT_FILE = Path("D:/PROJET_ALFRED/ALFRED_PC/tools/piper/output_python.wav")


def test_piper_executable_exists():
    assert PIPER_PATH.exists(), f"Piper introuvable : {PIPER_PATH}"


def test_piper_model_exists():
    assert MODEL_PATH.exists(), f"Modèle vocal introuvable : {MODEL_PATH}"


def test_piper_voice():
    if not PIPER_PATH.exists() or not MODEL_PATH.exists():
        pytest.skip("Piper ou modèle absent — test ignoré")

    text = "Bonjour, je suis ALFRED."
    command = [
        str(PIPER_PATH),
        "-m", str(MODEL_PATH),
        "-f", str(OUTPUT_FILE),
    ]
    process = subprocess.run(
        command,
        input=text,
        text=True,
        capture_output=True,
        check=False,
    )
    assert process.returncode == 0, f"Piper erreur : {process.stderr}"
    assert OUTPUT_FILE.exists(), "Fichier audio non généré"
