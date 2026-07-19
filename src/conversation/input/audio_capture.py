# ============================================================
# ALFRED — src/conversation/input/audio_capture.py
# Bloc 04.03 — Détection sonore
#
# 📚 NOTION EXAM :
#   D13-1 — Capsule 4 : Capture audio et gestion du flux microphone
#
# 🎯 UTILITÉ ALFRED :
#   Capture le flux audio brut depuis le microphone ;
#   stub V1 avec interface définie, implémentation complète V3.
#
# 🏗️ DOMAINE :
#   Interaction vocale — capture audio bas niveau, sounddevice
#
# STATUS  : VALIDATED
# ============================================================

class AudioCaptureNotAvailable(Exception):
    """Levée quand le système audio n'est pas disponible."""
    pass


def is_audio_available() -> bool:
    """
    Vérifie si la capture audio est disponible.
    V1 : toujours False (terminal only).
    V3 : vérifiera Whisper + micro.

    Returns:
        False en V1, True en V3 si Whisper chargé
    """
    return False


def capture_audio(timeout: float = 5.0) -> str:
    """
    Capture un message vocal et le transcrit en texte.

    V1 STUB → lève AudioCaptureNotAvailable.
    V3 : intégration Whisper local.

    Args:
        timeout : Durée max d'écoute en secondes

    Returns:
        Texte transcrit

    Raises:
        AudioCaptureNotAvailable : en V1 (fonctionnalité non disponible)
    """
    raise AudioCaptureNotAvailable(
        "Capture audio non disponible en V1. "
        "Active la saisie texte. "
        "Whisper local prévu en V3."
    )


def activate_wake_word_detection() -> bool:
    """
    Active la détection du wake word ("Hey Alfred").

    V1 STUB → retourne False.
    V3 : actif avec Whisper ou Porcupine.

    Returns:
        False en V1
    """
    return False


def get_audio_status() -> dict:
    """
    Retourne l'état du système audio.

    Returns:
        dict avec statut et version
    """
    return {
        "available":    False,
        "stt_engine":   None,
        "wake_word":    False,
        "version":      "stub_v1",
        "planned":      "whisper_v3",
        "message":      "Audio STT prévu en V3 (Whisper local + RTX 5080)",
    }
