# ============================================================
# ALFRED — src/input/stt_whisper.py
# Bloc 01.01 V3 — Speech-to-Text avec Whisper local
#
# Fonctions couvertes :
#   01.01.001 Activation micro / wake word  ✅ V3
#   01.01.002 Capture flux audio            ✅ V3
#   01.01.003 Filtrage bruit                ✅ V3 (Whisper natif)
#   01.01.004 Détection fin de phrase       ✅ V3
#   01.01.005 Feedback signal reçu          ✅ V3
#
# Dépendances V3 :
#   pip install openai-whisper sounddevice numpy
#   (décommenter dans requirements.txt)
#
# Hardware : CPU suffisant pour tiny/base — GPU RTX 5080 pour large
# ============================================================

import os
import time

# ── Import conditionnel Whisper ────────────────────────────
try:
    import whisper
    import numpy as np
    import sounddevice as sd
    _WHISPER_AVAILABLE = True
except ImportError:
    _WHISPER_AVAILABLE = False


# ─────────────────────────────────────────────────────────
# Configuration
# ─────────────────────────────────────────────────────────

# Taille du modèle Whisper selon hardware :
#   tiny   → très rapide, qualité correcte, CPU
#   base   → bon équilibre, CPU
#   small  → qualité bonne, CPU ou GPU léger
#   medium → haute qualité, GPU recommandé
#   large  → meilleure qualité, RTX 5080 requis
WHISPER_MODEL_SIZE = os.getenv("WHISPER_MODEL_SIZE", "base")

SAMPLE_RATE    = 16000     # Hz — requis par Whisper
RECORD_SECONDS = 6         # Durée max d'enregistrement par défaut
SILENCE_THRESH = 0.01      # Seuil de silence pour détection fin de phrase
WAKE_WORD      = "alfred"  # Wake word de déclenchement


# ─────────────────────────────────────────────────────────
# Chargement du modèle (lazy — chargé une seule fois)
# ─────────────────────────────────────────────────────────

_model = None


def _load_model():
    """Charge le modèle Whisper en mémoire (lazy loading)."""
    global _model
    if _model is None:
        if not _WHISPER_AVAILABLE:
            raise ImportError(
                "Whisper non installé. Lance : pip install openai-whisper sounddevice numpy"
            )
        print(f"  [STT] Chargement modèle Whisper '{WHISPER_MODEL_SIZE}'...")
        _model = whisper.load_model(WHISPER_MODEL_SIZE)
        print("  [STT] Modèle Whisper prêt ✅")
    return _model


# ─────────────────────────────────────────────────────────
# API publique
# ─────────────────────────────────────────────────────────

def is_stt_available() -> bool:
    """
    Vérifie si Whisper est installé et disponible.

    Returns:
        True si Whisper + sounddevice + numpy sont présents
    """
    return _WHISPER_AVAILABLE


def record_audio(duration: float = RECORD_SECONDS) -> "np.ndarray | None":
    """
    Enregistre l'audio depuis le micro.

    Args:
        duration : Durée max en secondes

    Returns:
        Array numpy audio ou None si erreur
    """
    if not _WHISPER_AVAILABLE:
        return None

    try:
        print(f"  [STT] 🎙️  Écoute ({duration}s)...")
        audio = sd.rec(
            int(duration * SAMPLE_RATE),
            samplerate=SAMPLE_RATE,
            channels=1,
            dtype="float32"
        )
        sd.wait()
        return audio.flatten()
    except Exception as e:
        from src.security.security_logger import log_event
        log_event(f"STT erreur enregistrement : {e}", "ERROR")
        return None


def transcribe(audio: "np.ndarray", language: str = "fr") -> dict:
    """
    Transcrit un enregistrement audio en texte via Whisper.

    Args:
        audio    : Array numpy audio (float32, 16kHz)
        language : Langue cible ("fr" ou "en")

    Returns:
        dict avec text, language, segments, duration
    """
    model = _load_model()

    start = time.time()
    result = model.transcribe(
        audio,
        language=language,
        task="transcribe",
        fp16=False,           # False sur CPU, True si GPU disponible
        verbose=False,
    )
    elapsed = time.time() - start

    return {
        "text":     result.get("text", "").strip(),
        "language": result.get("language", language),
        "segments": result.get("segments", []),
        "duration": round(elapsed, 2),
        "model":    WHISPER_MODEL_SIZE,
    }


def listen_and_transcribe(
    duration: float = RECORD_SECONDS,
    language: str = "fr",
) -> str:
    """
    Pipeline complet : enregistre + transcrit.
    Point d'entrée principal pour le pipeline conversationnel.

    Args:
        duration : Durée d'écoute en secondes
        language : Langue cible

    Returns:
        Texte transcrit ou "" si erreur/silence
    """
    audio = record_audio(duration)
    if audio is None:
        return ""

    # Vérification silence
    if _WHISPER_AVAILABLE:
        import numpy as np
        if np.abs(audio).mean() < SILENCE_THRESH:
            print("  [STT] Silence détecté — aucune transcription")
            return ""

    result = transcribe(audio, language)
    text = result["text"]

    if text:
        print(f"  [STT] Transcrit ({result['duration']}s) : {text}")
    return text


def detect_wake_word(text: str) -> bool:
    """
    Détecte si le wake word est présent dans le texte transcrit.

    Args:
        text : Texte transcrit

    Returns:
        True si wake word détecté
    """
    return WAKE_WORD.lower() in text.lower()


def get_stt_status() -> dict:
    """Retourne l'état complet du système STT."""
    return {
        "available":   _WHISPER_AVAILABLE,
        "model_size":  WHISPER_MODEL_SIZE,
        "sample_rate": SAMPLE_RATE,
        "wake_word":   WAKE_WORD,
        "gpu_mode":    False,   # True quand RTX 5080 active
        "version":     "whisper_v3",
    }


# ─────────────────────────────────────────────────────────
# Test standalone
# ─────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=== Test STT Whisper ===")
    print(f"Disponible : {is_stt_available()}")
    print(f"Statut     : {get_stt_status()}")

    if is_stt_available():
        texte = listen_and_transcribe(duration=4)
        print(f"Résultat   : '{texte}'")
        print(f"Wake word  : {detect_wake_word(texte)}")
