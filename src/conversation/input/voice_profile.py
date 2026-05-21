# ============================================================
# ALFRED — src/input/voice_profile.py
# Bloc 01 V2 — Profils vocaux
#
# Centralise tous les paramètres de voix d'ALFRED.
# Utilisé par tts_piper.py (V3) et tts_output.py (V1 terminal).
#
# Voix validée : fr_FR-upmc-medium — Speaker ID 1 "Pierre"
# Modèle       : ONNX Piper — 22 050 Hz — medium quality
# Licence      : CC BY-SA 4.0
# ============================================================

from dataclasses import dataclass


# ─────────────────────────────────────────────────────────
# Paramètres d'une voix
# ─────────────────────────────────────────────────────────

@dataclass
class VoiceParams:
    """
    Paramètres Piper TTS pour un profil vocal donné.

    length_scale  : vitesse (1.0 = normal, >1 = plus lent, <1 = plus rapide)
    noise_scale   : variabilité naturelle (0 = robot, 1 = très variable)
    noise_w       : variation inter-phonèmes (expressivité fine)
    speaker_id    : identifiant speaker dans le modèle multi-speaker
    """
    length_scale : float = 1.0
    noise_scale  : float = 0.667
    noise_w      : float = 0.8
    speaker_id   : int   = 1      # Pierre (upmc-medium)


# ─────────────────────────────────────────────────────────
# Voix ALFRED — Modèle principal
# ─────────────────────────────────────────────────────────

ALFRED_VOICE = {
    "model":      "fr_FR-upmc-medium",
    "speaker_id": 1,  # Pierre — masculin, posé, 25-40 ans
    "sample_rate": 22050,
    "language":   "fr_FR",
    "model_file": "../tools/piper/models/fr_FR-upmc-medium.onnx",
    "config_file": "../tools/piper/models/fr_FR-upmc-medium.onnx.json",
}


# ─────────────────────────────────────────────────────────
# Profils vocaux par mode dynamique ALFRED
# ─────────────────────────────────────────────────────────
# Correspondent aux 4 modes de personality_core.json :
# support | focus | challenge | complicite

VOICE_PROFILES: dict[str, VoiceParams] = {

    # Mode SUPPORT — présence rassurante, chaleureux
    # Voix plus lente, plus douce, très naturelle
    "support": VoiceParams(
        length_scale=1.25,
        noise_scale=0.55,
        noise_w=0.85,
    ),

    # Mode FOCUS — travail, concentration, clarté
    # Voix neutre, débit normal, articulée
    "focus": VoiceParams(
        length_scale=1.0,
        noise_scale=0.45,
        noise_w=0.75,
    ),

    # Mode CHALLENGE — dynamique, assertif, motivant
    # Voix légèrement plus rapide, plus affirmée
    "challenge": VoiceParams(
        length_scale=0.88,
        noise_scale=0.55,
        noise_w=0.70,
    ),

    # Mode COMPLICITE — détendu, naturel, complice
    # Voix la plus proche d'une conversation ordinaire
    "complicite": VoiceParams(
        length_scale=1.10,
        noise_scale=0.70,
        noise_w=0.90,
    ),

    # Mode par défaut (fallback)
    "default": VoiceParams(
        length_scale=1.0,
        noise_scale=0.667,
        noise_w=0.8,
    ),
}


# ─────────────────────────────────────────────────────────
# Mapping émotion → mode vocal
# ─────────────────────────────────────────────────────────

EMOTION_TO_MODE: dict[str, str] = {
    # Émotions négatives → mode support
    "stressed":      "support",
    "sad":           "support",
    "anxious":       "support",
    "overwhelmed":   "support",
    "tired":         "support",

    # État neutre/actif → mode focus
    "neutral":       "focus",
    "focused":       "focus",
    "working":       "focus",

    # État positif/dynamique → mode challenge ou complicité
    "motivated":     "challenge",
    "energized":     "challenge",
    "happy":         "complicite",
    "relaxed":       "complicite",
}


def get_voice_params(mode: str) -> VoiceParams:
    """
    Retourne les paramètres vocaux pour un mode donné.

    Args:
        mode : Mode ALFRED (support/focus/challenge/complicite)
               ou état émotionnel (stressed/happy/etc.)

    Returns:
        VoiceParams correspondant
    """
    # Résolution directe par mode
    if mode in VOICE_PROFILES:
        return VOICE_PROFILES[mode]

    # Résolution par émotion → mode
    resolved_mode = EMOTION_TO_MODE.get(mode, "default")
    return VOICE_PROFILES.get(resolved_mode, VOICE_PROFILES["default"])


def get_mode_from_energy(energy_level: str) -> str:
    """
    Déduit le mode vocal depuis le niveau d'énergie du contexte.

    Args:
        energy_level : high / medium / low (depuis context_builder)

    Returns:
        Mode vocal correspondant
    """
    mapping = {
        "high":   "focus",
        "medium": "complicite",
        "low":    "support",
    }
    return mapping.get(energy_level, "default")
