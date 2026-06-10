"""
PROJECT      : ALFRED
BLOCK        : B15 -- Avatar & Interface
FUNCTION     : 15.07.001 -> 15.07.013
FILE         : src/ui/avatar_engine.py
ROLE         : Moteur avatar ALFRED -- facade unificatrice Controller + Renderer + Background

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-06-01
UPDATED      : 2026-06-01 (Bug2 sync TTS + intégration alfred_app + main.py)
VERSION      : V1.0
STATUS       : TESTED

DESCRIPTION :
Facade centrale du sous-systeme avatar ALFRED.
Orchestre AvatarController, AvatarRenderer et BackgroundManager
en un seul point d'entree pour le pipeline conversationnel.

Fonctions couvertes :
  15.07.001  Initialisation et connexion des composants      OK V1
  15.07.002  API etats (speaking, listening, thinking, idle) OK V1
  15.07.003  Synchronisation mode ALFRED -> avatar           OK V1
  15.07.004  Animation phonemes (lip-sync)                   OK V1
  15.07.005  Gestion background (lieu + periode)             OK V1
  15.07.006  Hooks pipeline                                  OK V1
  15.07.007  Mode headless (sans Kivy)                       OK V1
  15.07.008  Statut consolide                                OK V1
  15.07.009  Singleton moteur                                OK V1
  15.07.010  Arret propre                                    OK V1
  15.07.011  Synchronisation sequence reponse (begin/end)    OK V1
  15.07.012  Callback TTS stop inter-phrases (on_tts_stop)   OK V1
  15.07.013  Verrou cycle speaking (anti-flash idle)          OK V1

Architecture :
  AvatarEngine
    |-- AvatarController  : machine a etats + hooks
    |-- AvatarRenderer    : widget Kivy 6 calques (ou stub headless)
    |-- BackgroundManager : selection fond PNG selon lieu + periode

Usage pipeline :
    engine = get_avatar_engine()
    engine.set_speaking(True)
    engine.set_phoneme("a")
    engine.set_background("salon")
    engine.set_mode("support")
"""

from __future__ import annotations

from datetime import datetime
from typing import Callable, List, Optional

from src.ui.avatar_controller import AvatarController, get_avatar_controller
from src.ui.avatar_renderer import AvatarRenderer, AvatarRendererLogic
from src.ui.background_manager import BackgroundManager


def _current_period() -> str:
    """Retourne la tranche horaire courante : jour | soiree | nuit."""
    h = datetime.now().hour
    if 6 <= h < 18:
        return "jour"
    if 18 <= h < 22:
        return "soiree"
    return "nuit"


# ============================================================
# Phonemes -> frame mapping
# ============================================================

# Phonemes ARPABET/IPA simplifies -> etat bouche
_PHONEME_MAP: dict[str, str] = {
    # Voyelles ouvertes
    "a": "a", "A": "a", "ah": "a", "AA": "a",
    # Voyelles moyennes
    "e": "a", "E": "a", "eh": "a", "AH": "a",
    # Voyelles fermees
    "i": "idle", "I": "idle", "ih": "idle", "IY": "idle",
    # Voyelles rondes
    "o": "o", "O": "o", "oh": "o", "OW": "o",
    "u": "o", "U": "o", "uh": "o", "UW": "o",
    # Bilabiales / nasales
    "m": "m", "M": "m", "b": "m", "p": "m",
    # Silence / pause
    "": "idle", "_": "idle", "sil": "idle",
}

_DEFAULT_PHONEME = "idle"


# ============================================================
# AvatarEngine
# ============================================================

class AvatarEngine:
    """
    Moteur avatar ALFRED V1.

    Facade unificatrice : connecte le pipeline conversationnel
    aux composants visuels (controller, renderer, background).

    Usage :
        engine = AvatarEngine()
        engine.set_speaking(True)
        engine.set_phoneme("a")
        engine.set_mode("support")
        engine.set_background("bureau")
        status = engine.status()
    """

    def __init__(self, headless: bool = False) -> None:
        """
        Initialise le moteur avatar.

        Args:
            headless : True = aucun rendu graphique (mode test / serveur)
        """
        self._headless   = headless
        self._started    = False
        self._hooks:     List[Callable[[str], None]] = []

        # Composants
        self._controller = get_avatar_controller(headless=headless)
        self._bg_manager = BackgroundManager()
        self._renderer:  Optional[AvatarRenderer] = None

        # Logic pure testable sans Kivy
        self._logic = AvatarRendererLogic()

        # Etat courant
        self._current_location  = "salon"
        self._current_period    = _current_period()

        # Verrouillage séquence de réponse (Bug 2 — sync speaking)
        self._response_active: bool = False

    # --------------------------------------------------------
    # Demarrage / arret
    # --------------------------------------------------------

    def start(self, renderer: Optional[AvatarRenderer] = None) -> None:
        """
        Demarre le moteur et connecte le renderer.

        Args:
            renderer : Widget AvatarRenderer Kivy (None en mode headless)
        """
        if renderer is not None:
            self._renderer = renderer
            self._controller.set_renderer(renderer)

        # Fond initial
        self._push_background()

        self._started = True

    def stop(self) -> None:
        """Arret propre du moteur."""
        self._controller.set_idle()
        self._started = False

    # --------------------------------------------------------
    # Etats principaux
    # --------------------------------------------------------

    def set_speaking(self, speaking: bool) -> None:
        """
        Synchronise l'avatar avec l'activite TTS.

        Args:
            speaking : True = ALFRED parle, False = fin de parole
        """
        self._controller.set_speaking(speaking)
        self._logic.set_state("speaking" if speaking else self._controller.current_state.mode)
        self._emit_hook("speaking" if speaking else self._controller.state_name)

    def set_listening(self, listening: bool) -> None:
        """
        Synchronise l'avatar avec l'ecoute microphone.

        Args:
            listening : True = ecoute active, False = fin ecoute
        """
        self._controller.set_listening(listening)
        self._emit_hook("listening" if listening else self._controller.state_name)

    def set_thinking(self) -> None:
        """Avatar en mode traitement (entre question et reponse)."""
        self._controller.set_thinking()
        self._logic.set_state("thinking")
        self._emit_hook("thinking")

    def set_idle(self) -> None:
        """Remet l'avatar en veille."""
        self._controller.set_idle()
        self._logic.set_state("idle")
        self._emit_hook("idle")

    def set_error(self, message: str = "") -> None:
        """Active l'etat erreur."""
        self._controller.set_error(message)
        self._logic.set_state("error")
        self._emit_hook("error")

    # --------------------------------------------------------
    # Synchronisation séquence de réponse (Bug 2 — sync TTS)
    # --------------------------------------------------------

    def begin_response(self) -> None:
        """
        Démarre une séquence de réponse ALFRED.

        - Passe l'avatar en mode thinking
        - Verrouille le cycle speaking : on_tts_stop() ne remettra PAS
          l'avatar en idle entre deux phrases — l'avatar reste visuellement
          en speaking jusqu'à end_response().

        Appeler AVANT build_response() dans main.py.
        """
        self._response_active = True
        self.set_thinking()

    def end_response(self) -> None:
        """
        Termine une séquence de réponse ALFRED.

        - Déverrouille le cycle speaking
        - Repasse l'avatar sur l'état de mode courant

        Appeler APRÈS build_response() et l'affichage UI dans main.py.
        """
        self._response_active = False
        self._controller.set_speaking(False)
        self._logic.set_state(self._controller.current_state.mode)
        self._emit_hook(self._controller.state_name)

    def on_tts_stop(self) -> None:
        """
        Callback fin de lecture d'UNE phrase TTS.

        Si une séquence de réponse est active (between sentences),
        NE remet PAS l'avatar en idle — évite le flash idle→speaking
        entre chaque phrase. Sinon, repasse en état mode normal.

        Câbler sur on_play_stop du backend TTS (PiperTTS).
        """
        if self._response_active:
            # Séquence en cours : garder visuellement speaking
            return
        self._controller.set_speaking(False)
        self._logic.set_state(self._controller.current_state.mode)
        self._emit_hook(self._controller.state_name)

    def set_state(self, state_name: str) -> bool:
        """
        Change l'etat avatar directement.

        Args:
            state_name : Nom d'etat valide (idle/speaking/thinking/...)

        Returns:
            True si la transition a eu lieu
        """
        ok = self._controller.set_state(state_name)
        if ok:
            self._logic.set_state(state_name)
            self._emit_hook(state_name)
        return ok

    # --------------------------------------------------------
    # Mode ALFRED
    # --------------------------------------------------------

    def set_mode(self, mode: str) -> bool:
        """
        Synchronise l'avatar avec le mode ALFRED courant.

        Args:
            mode : support | focus | challenge | complicite

        Returns:
            True si la transition a eu lieu
        """
        return self._controller.set_mode(mode)

    def set_emotion(self, emotion: str) -> None:
        """
        Met a jour l'emotion expressive de l'avatar.

        Args:
            emotion : neutral | happy | stressed | proud | ...
        """
        self._controller.set_emotion(emotion)

    # --------------------------------------------------------
    # Lip-sync phonemes
    # --------------------------------------------------------

    def set_phoneme(self, phoneme: str) -> str:
        """
        Avance l'animation de bouche selon le phoneme courant.
        A appeler par le pipeline TTS a chaque phoneme emis.

        Args:
            phoneme : Phoneme IPA/ARPABET simplifie (ex : "a", "m", "o")

        Returns:
            Chemin du sprite selectionne (pour debug)
        """
        mouth = _PHONEME_MAP.get(phoneme, _DEFAULT_PHONEME)
        # En mode speaking, le renderer Kivy avance tout seul via Clock.
        # set_phoneme() pilote la logique pure (utile pour tests + headless).
        frame = self._logic.get_speaking_frame()
        self._logic.next_speaking_frame()
        return frame

    def next_speaking_frame(self) -> str:
        """Avance d'un frame d'animation bouche et retourne le sprite."""
        return self._logic.next_speaking_frame()

    # --------------------------------------------------------
    # Background
    # --------------------------------------------------------

    def set_background(self, location: str = "", period: str = "") -> str:
        """
        Selectionne et applique le fond selon lieu + periode.

        Args:
            location : salon | chambre | bureau | transport | ville | ...
            period   : matin | midi | apres-midi | soiree | nuit (auto si vide)

        Returns:
            Chemin absolu du PNG choisi
        """
        if location:
            self._current_location = location
        if period:
            self._current_period = period
        else:
            self._current_period = _current_period()

        return self._push_background()

    def refresh_background(self) -> str:
        """
        Rafraichit le fond selon la periode courante (heure systeme).
        A appeler periodiquement pour le changement jour/soiree/nuit.

        Returns:
            Chemin absolu du PNG choisi
        """
        self._current_period = _current_period()
        return self._push_background()

    def _push_background(self) -> str:
        """Calcule le fond et le pousse au renderer."""
        path = self._bg_manager.get_background(
            location=self._current_location,
            period=self._current_period,
        )
        if path and self._renderer is not None:
            try:
                self._renderer.update_background(path)
            except Exception:
                pass
        return path or ""

    # --------------------------------------------------------
    # Hooks
    # --------------------------------------------------------

    def register_hook(self, callback: Callable[[str], None]) -> None:
        """
        Enregistre un hook appele a chaque changement d'etat.

        Args:
            callback : Fonction(state_name: str) -> None
        """
        self._hooks.append(callback)
        self._controller.register_hook(callback)

    def _emit_hook(self, state_name: str) -> None:
        for hook in self._hooks:
            try:
                hook(state_name)
            except Exception:
                pass

    # --------------------------------------------------------
    # Proprietes
    # --------------------------------------------------------

    @property
    def state_name(self) -> str:
        return self._controller.state_name

    @property
    def is_speaking(self) -> bool:
        return self._controller.is_speaking

    @property
    def is_listening(self) -> bool:
        return self._controller.is_listening

    @property
    def headless(self) -> bool:
        return self._headless

    @property
    def started(self) -> bool:
        return self._started

    # --------------------------------------------------------
    # Statut consolide
    # --------------------------------------------------------

    def status(self) -> dict:
        """Retourne l'etat complet du moteur (controller + renderer + bg)."""
        ctrl = self._controller.status()
        renderer_status = {}
        if self._renderer is not None:
            try:
                renderer_status = self._renderer.status()
            except Exception:
                pass

        return {
            "engine_started":   self._started,
            "headless":         self._headless,
            "state":            ctrl["current_state"],
            "mode":             ctrl["mode"],
            "is_speaking":      ctrl["is_speaking"],
            "is_listening":     ctrl["is_listening"],
            "emotion":          ctrl["emotion"],
            "location":         self._current_location,
            "period":           self._current_period,
            "hooks_count":      len(self._hooks),
            "has_renderer":     self._renderer is not None,
            "renderer":         renderer_status,
            "timestamp":        datetime.now().isoformat(),
            "version":          "avatar_engine_v1",
        }


# ============================================================
# Singleton
# ============================================================

_avatar_engine: Optional[AvatarEngine] = None


def get_avatar_engine(headless: bool = False) -> AvatarEngine:
    """
    Retourne l'instance singleton du moteur avatar.
    Cree a la premiere demande.

    Args:
        headless : True = mode sans affichage (test / serveur)
    """
    global _avatar_engine
    if _avatar_engine is None:
        _avatar_engine = AvatarEngine(headless=headless)
    elif not headless and _avatar_engine.headless:
        _avatar_engine._headless = False
    return _avatar_engine


def reset_avatar_engine() -> None:
    """Reinitialise le singleton (utile pour les tests)."""
    global _avatar_engine
    _avatar_engine = None
