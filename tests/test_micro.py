import sounddevice as sd
import numpy as np

duration = 5
samplerate = 16000

print("🎤 Test micro : parle pendant 5 secondes...")
audio = sd.rec(
    int(duration * samplerate),
    samplerate=samplerate,
    channels=1,
    dtype="float32"
)
sd.wait()

volume = float(np.abs(audio).mean())

print(f"Volume moyen détecté : {volume:.6f}")

if volume > 0.001:
    print("✅ Micro détecté et signal audio reçu.")
else:
    print("⚠️ Signal très faible ou aucun son détecté.")
