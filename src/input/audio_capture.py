"""
PROJECT      : ALFRED
BLOCK        : B04
FUNCTION     : 04.01
FILE         : src/input/audio_capture.py
ROLE         : Stub audio capture — vérifie la disponibilité du micro

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-06-05
UPDATED      : 2026-06-05
VERSION      : V1.0
STATUS       : VALIDATED
"""


def is_audio_available() -> bool:
    """Retourne True si sounddevice est disponible et un micro est détecté."""
    try:
        import sounddevice as sd
        devices = sd.query_devices()
        return any(d.get("max_input_channels", 0) > 0 for d in devices)
    except Exception:
        return False
