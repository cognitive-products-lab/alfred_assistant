"""
Test TTSEngine avec backend Piper
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.conversation.output.tts_engine import TTSEngine
from src.conversation.output.tts_piper import PiperTTS


def run_test():
    print("🧪 TEST TTSEngine + Piper")

    tts = TTSEngine(backend=PiperTTS())

    success = tts.speak("Bonjour Céline. Test du moteur vocal Alfred.")

    if success:
        print("✅ TTSEngine fonctionne correctement")
    else:
        print("❌ TTSEngine a échoué")


if __name__ == "__main__":
    run_test()