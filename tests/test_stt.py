import sounddevice as sd
import numpy as np
from faster_whisper import WhisperModel

samplerate = 16000
duration = 5

print("🎤 Parle pendant 5 secondes...")

audio = sd.rec(
    int(duration * samplerate),
    samplerate=samplerate,
    channels=1,
    dtype="float32"
)
sd.wait()

audio = np.squeeze(audio)

print("🧠 Transcription en cours...")

model = WhisperModel("base", compute_type="int8")

segments, _ = model.transcribe(audio, language="fr")

text = ""
for segment in segments:
    text += segment.text + " "

print(f"🧑 Toi : {text}")
