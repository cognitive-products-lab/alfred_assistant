"""
PROJECT      : ALFRED
BLOCK        : B15 — Avatar & Interface
FILE         : src/ui/desktop_tts_control.py
ROLE         : Interruption réelle du TTS en cours depuis l'interface desktop HTML

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-07-19
VERSION      : V1.0
STATUS       : DRAFT

DESCRIPTION :
Le bouton "Interrompre" du mode vocal ne coupait auparavant que l'état
visuel (setVState('interrupted') côté JS) — le TTS Piper continuait de
jouer la phrase en cours jusqu'au bout, et enchaînait sur les phrases
suivantes déjà en file.

Coupure réelle en deux temps, nécessaire car `PiperTTS.speak()` (voir
src/conversation/output/tts_piper.py) joue chaque phrase de façon
synchrone/bloquante (sd.play() + sd.wait()) dans le thread du pipeline :
  1. `sd.stop()` coupe l'audio de la phrase EN COURS de lecture — sd.wait()
     dans le thread pipeline retourne alors immédiatement.
  2. Un drapeau `components["_interrupted"]` est levé pour empêcher les
     phrases SUIVANTES (déjà générées ou en cours de génération côté LLM)
     d'être jouées — sans ce drapeau, sd.stop() ne couperait qu'une seule
     phrase avant que la suivante ne reprenne la lecture. Le drapeau est
     lu dans main.py (on_sentence + boucle de repli non-streamée) et remis
     à False au début du traitement de chaque nouvelle saisie utilisateur.

sd.stop() est un appel global sounddevice qui n'affecte que le flux de
sortie actif (sd.play()) — pas les flux d'entrée créés indépendamment
(sd.InputStream, utilisé par src/ui/desktop_mic.py pour le micro), donc
sans risque d'interrompre un enregistrement en cours.
"""

from __future__ import annotations


def interrupt_speech() -> dict:
    """Coupe le TTS en cours et réinitialise l'état visuel de l'avatar."""
    try:
        import sounddevice as sd
        sd.stop()
    except Exception:
        pass

    try:
        from src.main import get_live_components
        components = get_live_components()
    except Exception:
        components = None

    if components is not None:
        components["_interrupted"] = True
        avatar = components.get("avatar")
        if avatar:
            try:
                avatar.end_response()
            except Exception:
                pass

    try:
        from src.ui.alfred_app import set_ui_speaking
        set_ui_speaking(False)
    except Exception:
        pass

    return {"ok": True}
