"""
PROJECT      : ALFRED
BLOCK        : B15 -- Avatar & Interface
FUNCTION     : 15.01.001 -> 15.01.008
FILE         : src/ui/avatar_controller.py
ROLE         : Controleur avatar ALFRED -- machine a etats visuels, hooks mode et TTS

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-05-14
UPDATED      : 2026-05-14
VERSION      : V1.0
STATUS       : VALIDATED

DESCRIPTION :
Controleur central de l'avatar ALFRED.
Gere l'etat visuel de l'avatar en fonction du mode ALFRED, de l'etat
emotionnel et de l'activite TTS (parole / ecoute / veille).

Architecture : machine a etats legere, sans dependance GPU.
Compatible Kivy (hook visuel) et mode terminal (headless).

Fonctions couvertes :
  15.01.001 Machine a etats avatar                  OK V1
  15.01.002 Synchronisation mode ALFRED -> avatar   OK V1
  15.01.003 Synchronisation TTS (parle/ecoute)      OK V1
  15.01.004 Animations par etat                     OK V1 (descriptor)
  15.01.005 Hook transition mode                    OK V1
  15.01.006 Mode headless (sans affichage)           OK V1
  15.01.007 Historique etats avatar                 OK V1
  15.01.008 Statut controleur                       OK V1
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Callable, Dict, List, Optional


# ============================================================
# Etats avatar
# ============================================================

AVATAR_STATES = {
    # Etats d'activite
    "idle":       "En veille -- avatar calme, lumiere douce",
    "listening":  "Ecoute active -- animation ondulation douce",
    "thinking":   "Traitement -- animation pulsation lente",
    "speaking":   "Parole TTS -- animation bouche/onde sonore",

    # Etats emotionnels / mode
    "support":    "Mode support -- couleur chaude, posture ouverte",
    "focus":      "Mode focus -- couleur bleue, posture concentree",
    "challenge":  "Mode challenge -- couleur vive, posture dynamique",
    "complicite": "Mode complicite -- couleur verte, posture decontractee",

    # Etats speciaux
    "error":      "Erreur -- indicateur visuel d'alerte",
    "offline":    "Hors ligne -- avatar en veille profonde",
}

DEFAULT_STATE = "idle"


# ============================================================
# Modele etat avatar
# ============================================================

@dataclass
class AvatarState:
    """Un etat avatar enregistre."""
    state:       str   = DEFAULT_STATE
    mode:        str   = "focus"        # Mode ALFRED courant
    is_speaking: bool  = False
    is_listening: bool = False
    emotion:     str   = "neutral"
    description: str   = ""
    timestamp:   str   = field(default_factory=lambda: datetime.now().isoformat())


# ============================================================
# AvatarController
# ============================================================

class AvatarController:
    """
    Controleur avatar ALFRED V1.

    Gere la machine a etats visuelle de l'avatar :
    - Synchronise avec le mode ALFRED (support/focus/challenge/complicite)
    - Synchronise avec l'activite TTS (parole / ecoute / veille)
    - Emet des hooks pour les renderers (Kivy, etc.)
    - Fonctionne en mode headless si aucun renderer n'est connecte

    Usage :
        ctrl = AvatarController()
        ctrl.set_mode("support")
        ctrl.set_speaking(True)
        state = ctrl.current_state
    """

    def __init__(self, headless: bool = False):
        """
        Args:
            headless : True = pas d'affichage graphique (mode serveur/test)
        """
        self.headless        = headless
        self._current_state  = AvatarState()
        self._history:       List[AvatarState] = []
        self._hooks:         List[Callable]    = []
        self._renderer       = None            # Renderer optionnel (Kivy, etc.)

        self._record_state(DEFAULT_STATE)

    # --------------------------------------------------------
    # Proprietes
    # --------------------------------------------------------

    @property
    def current_state(self) -> AvatarState:
        return self._current_state

    @property
    def state_name(self) -> str:
        return self._current_state.state

    @property
    def is_speaking(self) -> bool:
        return self._current_state.is_speaking

    @property
    def is_listening(self) -> bool:
        return self._current_state.is_listening

    # --------------------------------------------------------
    # Transition d'etats
    # --------------------------------------------------------

    def set_state(self, state_name: str, reason: str = "") -> bool:
        """
        Change l'etat avatar.

        Args:
            state_name : Nom de l'etat (voir AVATAR_STATES)
            reason     : Raison du changement (pour log)

        Returns:
            True si changement effectue, False si etat inconnu ou deja courant
        """
        if state_name not in AVATAR_STATES:
            return False
        if state_name == self._current_state.state:
            return False

        self._current_state.state = state_name
        self._current_state.description = AVATAR_STATES.get(state_name, "")
        self._current_state.timestamp = datetime.now().isoformat()
        self._record_state(state_name)
        self._fire_hooks(state_name)
        self._render(state_name)
        return True

    def set_mode(self, mode: str) -> bool:
        """
        Synchronise l'avatar avec le mode ALFRED.

        Args:
            mode : Mode ALFRED (support/focus/challenge/complicite)

        Returns:
            True si transition effectuee
        """
        valid_modes = {"support", "focus", "challenge", "complicite"}
        if mode not in valid_modes:
            return False

        self._current_state.mode = mode
        # Si pas en train de parler/ecouter, adopter l'etat mode
        if not self._current_state.is_speaking and not self._current_state.is_listening:
            return self.set_state(mode)
        return True

    def set_speaking(self, speaking: bool) -> None:
        """
        Synchronise l'avatar avec l'activite TTS.

        Args:
            speaking : True = ALFRED parle, False = ALFRED a fini
        """
        self._current_state.is_speaking = speaking
        if speaking:
            self.set_state("speaking")
        else:
            # Retour au mode courant
            self.set_state(self._current_state.mode or DEFAULT_STATE)

    def pause_speaking(self) -> None:
        """Suspend l'animation bouche entre deux phrases TTS (silence réel),
        sans changer l'état avatar — évite le flash idle/thinking."""
        if self.headless or self._renderer is None:
            return
        try:
            if hasattr(self._renderer, "pause_mouth"):
                self._renderer.pause_mouth()
        except Exception:
            pass

    def resume_speaking(self) -> None:
        """Relance l'animation bouche au début d'une nouvelle phrase TTS."""
        if self.headless or self._renderer is None:
            return
        try:
            if hasattr(self._renderer, "resume_mouth"):
                self._renderer.resume_mouth()
        except Exception:
            pass

    def set_listening(self, listening: bool) -> None:
        """
        Synchronise l'avatar avec l'ecoute microphone.

        Args:
            listening : True = ALFRED ecoute, False = fin ecoute
        """
        self._current_state.is_listening = listening
        if listening:
            self.set_state("listening")
        else:
            self.set_state(self._current_state.mode or DEFAULT_STATE)

    def set_thinking(self) -> None:
        """Avatar en mode traitement (entre ecoute et reponse)."""
        self._current_state.is_listening = False
        self.set_state("thinking")

    def set_emotion(self, emotion: str) -> None:
        """
        Met a jour l'emotion de l'avatar (affichage expressif V2).

        Args:
            emotion : Emotion ALFRED (neutral/happy/stressed/etc.)
        """
        self._current_state.emotion = emotion

    def set_idle(self) -> None:
        """Remet l'avatar en veille."""
        self._current_state.is_speaking = False
        self._current_state.is_listening = False
        self.set_state("idle")

    def set_error(self, message: str = "") -> None:
        """Active l'etat erreur."""
        self.set_state("error")

    # --------------------------------------------------------
    # Renderer & hooks
    # --------------------------------------------------------

    def register_hook(self, callback: Callable[[str], None]) -> None:
        """
        Enregistre un hook appele a chaque changement d'etat.

        Args:
            callback : Fonction(state_name: str) -> None
        """
        self._hooks.append(callback)

    def set_renderer(self, renderer) -> None:
        """
        Connecte un renderer graphique (Kivy widget, etc.).
        Le renderer doit implementer update_state(state_name: str).
        Desactive automatiquement le mode headless si un renderer reel est fourni.

        Args:
            renderer : Objet renderer avec methode update_state()
        """
        self._renderer = renderer
        # Ne pas overrider headless si déjà explicitement défini à True

    def _fire_hooks(self, state_name: str) -> None:
        for hook in self._hooks:
            try:
                hook(state_name)
            except Exception:
                pass

    def _render(self, state_name: str) -> None:
        if self.headless or self._renderer is None:
            return
        try:
            if hasattr(self._renderer, "update_state"):
                self._renderer.update_state(state_name)
        except Exception:
            pass

    # --------------------------------------------------------
    # Historique
    # --------------------------------------------------------

    def _record_state(self, state_name: str) -> None:
        snapshot = AvatarState(
            state       = state_name,
            mode        = self._current_state.mode,
            is_speaking = self._current_state.is_speaking,
            is_listening = self._current_state.is_listening,
            emotion     = self._current_state.emotion,
            description = AVATAR_STATES.get(state_name, ""),
        )
        self._history.append(snapshot)

    def get_history(self, n: int = 10) -> List[AvatarState]:
        """Retourne les N derniers etats."""
        return self._history[-n:]

    def clear_history(self) -> None:
        self._history = []

    # --------------------------------------------------------
    # Animation descriptors (V1 -- texte; V2 = Kivy animations)
    # --------------------------------------------------------

    def get_animation_descriptor(self, state_name: str = "") -> Dict[str, str]:
        """
        Retourne le descripteur d'animation pour un etat.
        V1 : texte seulement. V2 : parametres Kivy (couleur, vitesse, etc.)

        Args:
            state_name : Etat cible (courant si vide)

        Returns:
            dict avec description et parametres visuels V1
        """
        name = state_name or self._current_state.state
        descriptors = {
            "idle":       {"color": "#8B9FD4", "animation": "breathe_slow", "intensity": 0.3},
            "listening":  {"color": "#5BC8F5", "animation": "pulse_wave",   "intensity": 0.6},
            "thinking":   {"color": "#F5A623", "animation": "pulse_slow",   "intensity": 0.5},
            "speaking":   {"color": "#7ED321", "animation": "wave_mouth",   "intensity": 0.8},
            "support":    {"color": "#E8A87C", "animation": "breathe_warm", "intensity": 0.5},
            "focus":      {"color": "#4A90D9", "animation": "static",       "intensity": 0.4},
            "challenge":  {"color": "#F5A623", "animation": "pulse_fast",   "intensity": 0.7},
            "complicite": {"color": "#7ED321", "animation": "breathe_light","intensity": 0.4},
            "error":      {"color": "#D0021B", "animation": "flash",        "intensity": 1.0},
            "offline":    {"color": "#666666", "animation": "none",         "intensity": 0.1},
        }
        desc = descriptors.get(name, {"color": "#CCCCCC", "animation": "none", "intensity": 0.0})
        desc["state"] = name
        desc["description"] = AVATAR_STATES.get(name, "")
        return desc

    # --------------------------------------------------------
    # Statut
    # --------------------------------------------------------

    def status(self) -> dict:
        """Retourne l'etat complet du controleur."""
        return {
            "current_state":  self._current_state.state,
            "mode":           self._current_state.mode,
            "is_speaking":    self._current_state.is_speaking,
            "is_listening":   self._current_state.is_listening,
            "emotion":        self._current_state.emotion,
            "headless":       self.headless,
            "hooks_count":    len(self._hooks),
            "has_renderer":   self._renderer is not None,
            "history_count":  len(self._history),
            "version":        "avatar_v1",
        }


# ============================================================
# Singleton session
# ============================================================

_avatar_controller: Optional[AvatarController] = None


def get_avatar_controller(headless: bool = True) -> AvatarController:
    """
    Retourne l'instance singleton du controleur avatar.
    Cree a la premiere demande.
    Si headless=False est demande sur un singleton deja headless, l'upgrade.

    Args:
        headless : Mode sans affichage (True par defaut)
    """
    global _avatar_controller
    if _avatar_controller is None:
        _avatar_controller = AvatarController(headless=headless)
    elif not headless and _avatar_controller.headless:
        _avatar_controller.headless = False
    return _avatar_controller
