import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.conversation.output.tts_piper import get_tts_status, is_tts_available

print("TTS available:", is_tts_available())
print("TTS status:", get_tts_status())