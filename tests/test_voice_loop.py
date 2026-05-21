import sounddevice as sd
import numpy as np
from faster_whisper import WhisperModel

from src.conversation.output.tts_engine import TTSEngine
from src.conversation.output.tts_piper import PiperTTS

samplerate = 16000
duration = 5

print("🧪 TEST BOUCLE VOCALE ALFRED")
print("🎤 Parle pendant 5 secondes...")

audio = sd.rec(
    int(duration * samplerate),
    samplerate=samplerate,
    channels=1,
    dtype="float32"
)
sd.wait()

audio = np.squeeze(audio)

print("🧠 Transcription...")
model = WhisperModel("base", compute_type="int8")
segments, _ = model.transcribe(audio, language="fr")

user_text = " ".join(segment.text.strip() for segment in segments).strip()

print(f"🧑 Toi : {user_text}")

if not user_text:
    print("⚠️ Aucun texte détecté.")
    raise SystemExit

response = f"Oui Céline, je t'entends parfaitement. Tu as dit : {user_text}"

print(f"🤖 ALFRED : {response}")

tts = TTSEngine(backend=PiperTTS(mode="complicite", blocking=True))
tts.speak(response)

print("✅ Boucle vocale STT → réponse → TTS validée")
