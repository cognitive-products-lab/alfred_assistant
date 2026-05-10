"""
test_tts_piper.py
-----------------

Test isolé de Piper depuis Python.

Objectif :
- vérifier que Python peut appeler piper.exe
- générer un fichier output_python.wav
- ouvrir automatiquement le fichier audio
"""

from pathlib import Path
import subprocess
import os


PIPER_PATH = Path("D:/PROJET_ALFRED/ALFRED_PC/tools/piper/piper.exe")
MODEL_PATH = Path("D:/PROJET_ALFRED/ALFRED_PC/tools/piper/models/fr_FR-upmc-medium.onnx")
OUTPUT_FILE = Path("D:/PROJET_ALFRED/ALFRED_PC/tools/piper/output_python.wav")


def test_piper_voice(text: str) -> bool:
    if not PIPER_PATH.exists():
        print(f"❌ Piper introuvable : {PIPER_PATH}")
        return False

    if not MODEL_PATH.exists():
        print(f"❌ Modèle vocal introuvable : {MODEL_PATH}")
        return False

    if not text.strip():
        print("❌ Texte vide.")
        return False

    try:
        command = [
            str(PIPER_PATH),
            "-m",
            str(MODEL_PATH),
            "-f",
            str(OUTPUT_FILE),
        ]

        process = subprocess.run(
            command,
            input=text,
            text=True,
            capture_output=True,
            check=False,
        )

        if process.returncode != 0:
            print("❌ Erreur Piper")
            print(process.stderr)
            return False

        print(f"✅ Fichier audio généré : {OUTPUT_FILE}")

        os.startfile(OUTPUT_FILE)
        return True

    except Exception as error:
        print(f"❌ Erreur test_piper_voice : {error}")
        return False


if __name__ == "__main__":
    test_piper_voice("Bonjour Céline. Test Python réussi. Alfred peut parler depuis le code.")
