"""
PROJECT      : ALFRED
BLOCK        : B01
FUNCTION     : XX.XX
FILE         : tts_piper.py
ROLE         : Synthese vocale Piper (lecture WAV + lissage audio)

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-05-10
UPDATED      : 2026-06-10
VERSION      : V1.1
STATUS       : TO_TEST

DESCRIPTION :
Ajout d'un fondu d'entree/sortie (~5ms) sur chaque buffer audio pour
supprimer le grésillement entre phrases en streaming. A re-valider en
conditions reelles avant de repasser en STABLE.
"""

# ============================================================
# ALFRED — src/conversation/output/tts_piper.py
# Bloc 01.03 V3 — Text-to-Speech avec Piper local
#
# Voix    : fr_FR-upmc-medium — Speaker ID 1 "Pierre"
# Qualité : 22 050 Hz — medium — CC BY-SA 4.0
#
# Fonctions couvertes :
#   01.03.001 Synthèse vocale locale (Piper)  ✅ V3
#   01.03.002 Ajustement débit & intonation   ✅ V3 (length_scale)
#   01.03.003 Adaptation voix / émotion       ✅ V3 (VOICE_PROFILES)
#   01.03.004 Sortie audio (sounddevice)      ✅ V3
#   01.03.005 Sync TTS / avatar               🔲 V3+ (lipSync)
#
# Dépendances V3 :
#   pip install piper-tts sounddevice numpy
#   Modèle : assets/voices/fr_FR-upmc-medium.onnx
#            assets/voices/fr_FR-upmc-medium.onnx.json
# ============================================================

import io
import os
import time
import wave
import subprocess
import tempfile

from pathlib import Path

# sounddevice et soundfile charges en lazy pour eviter les echecs d'init audio
# (pilote audio verrouille par une session precedente sur Windows)
sd = None
sf = None

def _apply_fade(audio, samplerate: int, fade_ms: float = 5.0):
    """Applique un fondu d'entrée/sortie linéaire de quelques ms.

    Évite le "clic"/grésillement audible quand sd.play() est appelé en rafale
    (une fois par phrase pendant le streaming) : sans fondu, chaque buffer
    démarre/termine sur une discontinuité d'amplitude brutale.
    """
    try:
        import numpy as _np
        n_fade = int(samplerate * fade_ms / 1000.0)
        if n_fade <= 0 or len(audio) <= 2 * n_fade:
            return audio
        fade_in  = _np.linspace(0.0, 1.0, n_fade, dtype=audio.dtype)
        fade_out = _np.linspace(1.0, 0.0, n_fade, dtype=audio.dtype)
        audio = audio.copy()
        if audio.ndim == 1:
            audio[:n_fade]  *= fade_in
            audio[-n_fade:] *= fade_out
        else:
            audio[:n_fade, :]  *= fade_in[:, None]
            audio[-n_fade:, :] *= fade_out[:, None]
        return audio
    except Exception:
        return audio


def _resample(audio, orig_sr: int, target_sr: int):
    """Resample audio (mono ou stereo) par interpolation lineaire.

    Le modele Piper genere a 22050 Hz, mais certains peripheriques de sortie
    (ex. Jabra SPEAK 510 en WASAPI) refusent ce sample rate avec
    PortAudioError -9997 "Invalid sample rate" et n'acceptent que leur
    default_samplerate (souvent 44100/48000 Hz).
    """
    if orig_sr == target_sr:
        return audio
    try:
        import numpy as _np
        n_in = audio.shape[0]
        n_out = int(round(n_in * target_sr / orig_sr))
        x_old = _np.linspace(0.0, 1.0, n_in, endpoint=False)
        x_new = _np.linspace(0.0, 1.0, n_out, endpoint=False)
        if audio.ndim == 1:
            return _np.interp(x_new, x_old, audio).astype(audio.dtype)
        return _np.stack(
            [_np.interp(x_new, x_old, audio[:, ch]) for ch in range(audio.shape[1])],
            axis=1,
        ).astype(audio.dtype)
    except Exception:
        return audio


def _output_samplerate(sd_module, fallback: int) -> int:
    """Determine le sample rate par defaut du peripherique de sortie courant."""
    try:
        device = sd_module.default.device[1]
        info = sd_module.query_devices(device)
        rate = info.get("default_samplerate")
        if rate:
            return int(rate)
    except Exception:
        pass
    return fallback


def _ensure_audio_libs() -> bool:
    """Charge sounddevice et soundfile a la premiere utilisation."""
    global sd, sf
    if sd is not None:
        return True
    try:
        import sounddevice as _sd
        import soundfile as _sf
        sd = _sd
        sf = _sf
        return True
    except Exception:
        return False

from src.conversation.input.voice_profile import (
    ALFRED_VOICE,
    VoiceParams,
    get_voice_params,
    get_mode_from_energy,
)
from src.security.security_logger import log_event

# ── Import conditionnel Piper ──────────────────────────────
try:
    from piper import PiperVoice
    import sounddevice as sd
    import numpy as np
    _PIPER_AVAILABLE = True
except ImportError:
    _PIPER_AVAILABLE = False


# ─────────────────────────────────────────────────────────
# Chemins modèle
# ─────────────────────────────────────────────────────────

_BASE_DIR    = Path(__file__).resolve().parents[3]   # ALFRED_PC/ (src/conversation/output/ → +3)
_MODEL_PATH  = _BASE_DIR / ALFRED_VOICE["model_file"]
_CONFIG_PATH = _BASE_DIR / ALFRED_VOICE["config_file"]


# ─────────────────────────────────────────────────────────
# Chargement modèle (lazy)
# ─────────────────────────────────────────────────────────

_voice_instance = None


def _load_voice() -> "PiperVoice | None":
    """
    Charge la voix Piper en mémoire (lazy loading).
    Ne charge qu'une seule fois — conservé pour toute la session.
    """
    global _voice_instance
    if _voice_instance is None:
        if not _PIPER_AVAILABLE:
            log_event("Piper non installé — TTS vocal non disponible", "WARNING")
            return None

        if not _MODEL_PATH.exists():
            log_event(f"Modèle Piper absent : {_MODEL_PATH}", "ERROR")
            return None

        if not _CONFIG_PATH.exists():
            log_event(f"Config Piper absente : {_CONFIG_PATH}", "ERROR")
            return None

        try:
            print(f"  [TTS] Chargement voix Piper '{ALFRED_VOICE['model']}'...")
            _voice_instance = PiperVoice.load(
                str(_MODEL_PATH),
                config_path=str(_CONFIG_PATH),
                use_cuda=False,       # True quand RTX 5080 active en V3+
            )
            print(f"  [TTS] Voix Pierre (upmc-medium) prête ✅")
            log_event("Voix Piper chargée : fr_FR-upmc-medium speaker=1")
        except Exception as e:
            log_event(f"Erreur chargement Piper : {e}", "ERROR")
            return None

    return _voice_instance


# ─────────────────────────────────────────────────────────
# API publique
# ─────────────────────────────────────────────────────────

def is_tts_available() -> bool:
    """
    Vérifie si Piper TTS est disponible et le modèle présent.

    Returns:
        True si Piper installé + modèle .onnx présent
    """
    return _PIPER_AVAILABLE and _MODEL_PATH.exists() and _CONFIG_PATH.exists()


def synthesize(
    text: str,
    params: VoiceParams | None = None,
) -> "np.ndarray | None":
    """
    Synthétise un texte en signal audio numpy via fichier WAV temporaire.
    Plus fiable que BytesIO avec certaines versions Piper.
    """
    voice = _load_voice()
    if voice is None:
        return None

    try:
        import tempfile

        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
            tmp_path = tmp.name

        with wave.open(tmp_path, "wb") as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)
            wav_file.setframerate(ALFRED_VOICE["sample_rate"])
            voice.synthesize(text, wav_file)

        with wave.open(tmp_path, "rb") as wav_file:
            frames = wav_file.readframes(wav_file.getnframes())
            n_channels = wav_file.getnchannels()

        try:
            os.remove(tmp_path)
        except OSError:
            pass

        audio = np.frombuffer(frames, dtype=np.int16).astype(np.float32)
        audio /= 32768.0

        if n_channels > 1:
            audio = audio.reshape(-1, n_channels).mean(axis=1)

        if audio.size == 0:
            print("❌ DEBUG TTS : audio généré vide")
            return None

        return audio

    except Exception as e:
        print(f"❌ DEBUG TTS synthèse erreur : {type(e).__name__} — {e}")
        log_event(f"TTS synthèse erreur : {e}", "ERROR")
        return None


def speak(
    text: str,
    mode: str = "default",
    blocking: bool = True,
) -> bool:
    """
    Synthétise et joue un texte vocalement.
    Point d'entrée principal pour le pipeline conversationnel.

    Args:
        text     : Texte à prononcer
        mode     : Mode ALFRED (support/focus/challenge/complicite)
                   ou état émotionnel (stressed/happy/etc.)
        blocking : Attend la fin de lecture si True

    Returns:
        True si lecture réussie, False sinon
    """
    if not _PIPER_AVAILABLE:
        # Fallback terminal si Piper absent
        from src.conversation.output.tts_output import display_response
        display_response(text)
        return False

    params = get_voice_params(mode)
    audio  = synthesize(text, params)

    if audio is None:
        print("❌ DEBUG TTS : synthesize() a retourné None")
        from src.conversation.output.tts_output import display_response
        display_response(text)
        return False

    try:
        sample_rate = ALFRED_VOICE["sample_rate"]

        import numpy as np
        audio = audio.astype(np.float32)

        sd.play(audio, samplerate=sample_rate)

        if blocking:
            sd.wait()

        log_event(f"TTS lecture OK — mode={mode} — {len(text)} chars")
        return True

    except Exception as e:
        print(f"❌ DEBUG TTS lecture erreur : {type(e).__name__} — {e}")
        log_event(f"TTS lecture erreur : {e}", "ERROR")

        from src.conversation.output.tts_output import display_response
        display_response(text)

        return False


def speak_with_context(
    text: str,
    energy_level: str = "medium",
    emotion: str = "neutral",
) -> bool:
    """
    Parle en déduisant automatiquement le mode depuis le contexte.
    Utilisé par speech_manager.py — interface haut niveau.

    Args:
        text         : Texte à prononcer
        energy_level : Niveau d'énergie (high/medium/low) du context_builder
        emotion      : État émotionnel détecté par nlp_engine_v2

    Returns:
        True si succès
    """
    from src.conversation.input.voice_profile import EMOTION_TO_MODE
    # Émotion prioritaire sur énergie
    if emotion != "neutral" and emotion in EMOTION_TO_MODE:
        mode = EMOTION_TO_MODE[emotion]
    else:
        mode = get_mode_from_energy(energy_level)

    return speak(text, mode=mode)


def save_to_file(
    text: str,
    output_path: str | Path,
    mode: str = "default",
) -> bool:
    """
    Synthétise et sauvegarde en fichier WAV.
    Utile pour tests, lipSync ou archivage.

    Args:
        text        : Texte à synthétiser
        output_path : Chemin du fichier WAV de sortie
        mode        : Mode vocal

    Returns:
        True si sauvegarde réussie
    """
    voice = _load_voice()
    if voice is None:
        return False

    params = get_voice_params(mode)
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        with wave.open(str(output_path), "wb") as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)
            wav_file.setframerate(ALFRED_VOICE["sample_rate"])

            voice.synthesize(text, wav_file)

        log_event(f"TTS sauvegardé : {output_path}")
        return True
    except Exception as e:
        log_event(f"TTS sauvegarde erreur : {e}", "ERROR")
        return False


def get_tts_status() -> dict:
    """Retourne l'état complet du système TTS."""
    return {
        "available":   is_tts_available(),
        "piper_ready": _PIPER_AVAILABLE,
        "model":       ALFRED_VOICE["model"],
        "speaker":     "pierre",
        "speaker_id":  ALFRED_VOICE["speaker_id"],
        "sample_rate": ALFRED_VOICE["sample_rate"],
        "model_file":  str(_MODEL_PATH),
        "gpu_mode":    False,   # True en V3+ avec RTX 5080
        "version":     "piper_v3",
    }


# ─────────────────────────────────────────────────────────
# Test standalone
# ─────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=== Test TTS Piper — Voix Pierre ===\n")

    print(f"Disponible : {is_tts_available()}")
    print(f"Statut     : {get_tts_status()}\n")

    if is_tts_available():
        tests = [
            ("Bonjour. Je suis ALFRED, votre assistant.", "complicite"),
            ("Je comprends que tu te sens débordée. On va avancer ensemble.", "support"),
            ("Voici les trois points essentiels à traiter aujourd'hui.", "focus"),
            ("Allez, on y va. Tu as tout ce qu'il faut pour réussir.", "challenge"),
        ]

        for text, mode in tests:
            print(f"  [{mode.upper()}] {text}")
            speak(text, mode=mode)
            time.sleep(0.5)

    else:
        print("  Piper non disponible — installe : pip install piper-tts sounddevice numpy")


# ─────────────────────────────────────────────────────────
# Adapter pour TTSEngine
# ─────────────────────────────────────────────────────────

class PiperTTS:
    """
    Backend TTS robuste via Piper CLI.
    Contourne le bug Piper Python qui génère un audio vide sous Windows/Python 3.13.
    """

    def __init__(self, mode: str = "default", blocking: bool = True) -> None:
        self.mode = mode
        self.blocking = blocking
        # Callbacks déclenchés en synchronisation avec la lecture audio réelle
        self.on_play_start: "callable | None" = None  # juste après sd.play()
        self.on_play_stop:  "callable | None" = None  # juste après sd.wait()

    def speak(self, text: str) -> bool:
        import os
        import subprocess
        import tempfile
        import sounddevice as sd
        import soundfile as sf

        if not text or not text.strip():
            return False

        try:
            tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
            tmp_wav_path = tmp_file.name
            tmp_file.close()

            command = [
                "piper",
                "--model", str(_MODEL_PATH),
                "--config", str(_CONFIG_PATH),
                "--output_file", tmp_wav_path,
                "--speaker", str(ALFRED_VOICE["speaker_id"]),
            ]

            subprocess.run(
                command,
                input=text.strip(),
                text=True,
                encoding="utf-8",
                errors="replace",
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            import sounddevice as sd
            import soundfile as sf

            audio, samplerate = sf.read(tmp_wav_path, dtype="float32")

            # Fondu d'entrée/sortie (~5 ms) — évite le "clic"/grésillement entendu
            # entre chaque phrase quand sd.play() est appelé en rafale (streaming).
            audio = _apply_fade(audio, samplerate)

            # Resample si le device de sortie n'accepte pas le sample rate Piper
            # (ex. PaErrorCode -9997 "Invalid sample rate" sur Jabra SPEAK 510 USB
            # qui n'accepte que son default_samplerate, 44100 Hz)
            target_rate = _output_samplerate(sd, samplerate)
            if target_rate != samplerate:
                audio = _resample(audio, samplerate, target_rate)
                samplerate = target_rate

            # Sortie sur le device par défaut système (ne pas forcer un index)
            # PaErrorCode -9998 = device 3 est input-only sur cette machine
            sd.play(audio, samplerate)

            # Callback début lecture — synchronisé avec le démarrage audio réel
            if self.on_play_start:
                try:
                    self.on_play_start()
                except Exception:
                    pass

            if self.blocking:
                sd.wait()

            # Callback fin lecture — synchronisé avec la fin audio réelle
            if self.on_play_stop:
                try:
                    self.on_play_stop()
                except Exception:
                    pass

            return True

        except Exception as e:
            print(f"❌ Erreur Piper CLI : {type(e).__name__} — {e}")
            # Garantit que on_play_stop est appelé même en cas d'erreur
            if self.on_play_stop:
                try:
                    self.on_play_stop()
                except Exception:
                    pass
            return False


