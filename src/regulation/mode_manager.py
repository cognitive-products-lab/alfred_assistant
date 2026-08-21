"""
PROJECT      : ALFRED
BLOCK        : B03
FUNCTION     : XX.XX
FILE         : mode_manager.py
ROLE         : Émotions & Régulation — Bloc 03

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-05-10
P26-05-12
VERSION      : V1.0
STATUS       : VALIDATED

DESCRIPTION :
Détection émotions, machine à états modes, protection, bien-être — ALFRED B03.
"""

# ============================================================
# ALFRED — src/regulation/mode_manager.py
# Bloc 03.02 / 03.03 — Machine à états des 4 modes dynamiques
#
# Fonctions couvertes :
#   03.02.001 Adaptation ton & registre ALFRED   ✅ V2
#   03.02.002 Réassurance & soutien émotionnel   ✅ V2
#   03.02.003 Suggestion actions bien-être       ✅ V1/V2
#   03.03.001 Transition douce entre états       ✅ V2
#   03.03.002 Déclencheur changement mode        ✅ V2
#   03.03.003 Log transitions                    ✅ V2
#   03.03.004 Notification avatar (émotion)      ✅ V2 (hook)
#   03.03.005 Cohérence ton / état global        ✅ V2
#
# Les 4 modes ALFRED (définis dans personality_core.json) :
#   support     → présence rassurante, écoute, douceur
#   focus       → clarté, efficacité, structuré
#   challenge   → dynamique, assertif, motivant
#   complicite  → détendu, naturel, complice
# ============================================================

from dataclasses import dataclass, field
from datetime import datetime
from typing import Callable

from src.regulation.emotion_detector import EmotionalState, requires_support_mode
from src.security.security_logger import log_event


# ─────────────────────────────────────────────────────────
# Définition des 4 modes
# ─────────────────────────────────────────────────────────

@dataclass
class ModeConfig:
    """Configuration d'un mode dynamique ALFRED."""
    name:         str
    label_fr:     str
    tone:         str
    response_style: str
    voice_profile: str     # Correspond à voice_profile.py
    proactivity:  float    # 0.0 → 1.0
    warmth:       float    # 0.0 → 1.0
    directness:   float    # 0.0 → 1.0
    triggers:     list[str] = field(default_factory=list)  # Émotions déclencheuses


MODES: dict[str, ModeConfig] = {

    "support": ModeConfig(
        name          = "support",
        label_fr      = "Mode présence & soutien",
        tone          = "doux, chaleureux, rassurant, patient",
        response_style = "phrases courtes, validations émotionnelles, pas de pression",
        voice_profile  = "support",
        proactivity    = 0.3,
        warmth         = 1.0,
        directness     = 0.3,
        triggers       = ["distress", "stressed", "sad", "tired", "confused"],
    ),

    "focus": ModeConfig(
        name          = "focus",
        label_fr      = "Mode travail & clarté",
        tone          = "clair, structuré, précis, efficace",
        response_style = "réponses directes, étapes numérotées, livrables clairs",
        voice_profile  = "focus",
        proactivity    = 0.6,
        warmth         = 0.6,
        directness     = 0.9,
        triggers       = ["focused", "neutral"],
    ),

    "challenge": ModeConfig(
        name          = "challenge",
        label_fr      = "Mode dynamique & défi",
        tone          = "dynamique, assertif, motivant, ambitieux",
        response_style = "formulations actives, challenge, appel à l'action",
        voice_profile  = "challenge",
        proactivity    = 0.8,
        warmth         = 0.7,
        directness     = 0.95,
        triggers       = ["motivated"],
    ),

    "complicite": ModeConfig(
        name          = "complicite",
        label_fr      = "Mode complicité & légèreté",
        tone          = "détendu, naturel, complice, léger",
        response_style = "conversationnel, humour doux, spontané",
        voice_profile  = "complicite",
        proactivity    = 0.5,
        warmth         = 0.9,
        directness     = 0.5,
        triggers       = ["happy", "curious", "relaxed"],
    ),
}

DEFAULT_MODE = "focus"

# Intention détectée → mode. Vocabulaire aligné sur le catalogue réellement
# produit en production (src/input/nlp_engine.py::_INTENT_CATALOG, consommé
# via src/conversation/input/nlp_engine_v2.py par regulation_engine.py) —
# avant cette extension, la moitié des intentions réelles (farewell,
# organization, reminder, weather, music, information, project) n'avaient
# aucun effet sur le mode. wellbeing/knowledge_request/product_knowledge
# conservés pour compatibilité avec d'autres catalogues d'intention du
# projet (ex. multi_signal_fusion_engine.py::_INTENT_TO_MODE).
INTENT_TO_MODE: dict[str, str] = {
    "emotional_support": "support",
    "wellbeing":         "support",
    "engineering":       "focus",
    "knowledge_request": "focus",
    "information":       "focus",
    "organization":      "focus",
    "reminder":          "focus",
    "project":           "focus",
    "task":              "focus",
    "question":          "focus",
    "product_knowledge": "challenge",
    "greeting":          "complicite",
    "farewell":          "complicite",
    "weather":           "complicite",
    "music":             "complicite",
}


# ─────────────────────────────────────────────────────────
# Machine à états (singleton session)
# ─────────────────────────────────────────────────────────

class ModeManager:
    """
    Gestionnaire des modes dynamiques ALFRED.
    Gère les transitions, les logs et les hooks avatar.

    Usage :
        manager = ModeManager()
        mode = manager.current_mode
        manager.update_from_emotion(emotional_state)
        config = manager.get_current_config()
    """

    def __init__(self, initial_mode: str = DEFAULT_MODE):
        self._current_mode  = initial_mode
        self._previous_mode = None
        self._transition_log: list[dict] = []
        self._on_transition: list[Callable] = []  # Hooks (avatar, TTS, etc.)
        log_event(f"ModeManager initialisé — mode: {initial_mode}")

    @property
    def current_mode(self) -> str:
        return self._current_mode

    @property
    def current_config(self) -> ModeConfig:
        return MODES.get(self._current_mode, MODES[DEFAULT_MODE])

    def get_current_config(self) -> ModeConfig:
        return self.current_config

    # ─────────────────────────────────────────────────────
    # Transition de mode
    # ─────────────────────────────────────────────────────

    def set_mode(self, new_mode: str, reason: str = "manual") -> bool:
        """
        Change le mode courant.

        Args:
            new_mode : Nouveau mode (support/focus/challenge/complicite)
            reason   : Raison du changement (pour log)

        Returns:
            True si changement effectué
        """
        if new_mode not in MODES:
            log_event(f"Mode inconnu : {new_mode}", "WARNING")
            return False

        if new_mode == self._current_mode:
            return False  # Pas de changement inutile

        self._previous_mode = self._current_mode
        self._current_mode  = new_mode

        # Log transition
        transition = {
            "timestamp": datetime.now().isoformat(),
            "from":      self._previous_mode,
            "to":        new_mode,
            "reason":    reason,
        }
        self._transition_log.append(transition)
        log_event(f"Mode → {new_mode} (raison: {reason})")

        # Déclencher hooks enregistrés (avatar, TTS, etc.)
        for hook in self._on_transition:
            try:
                hook(self._previous_mode, new_mode)
            except Exception as e:
                log_event(f"Erreur hook transition : {e}", "WARNING")

        return True

    def update_from_emotion(self, state: EmotionalState) -> str:
        """
        Met à jour le mode selon l'état émotionnel détecté.
        Transitions automatiques basées sur les déclencheurs de chaque mode.

        Args:
            state : EmotionalState depuis emotion_detector

        Returns:
            Mode résultant
        """
        # Priorité haute : mode protection si détresse
        from src.regulation.protection_guard import is_protection_needed
        if is_protection_needed(state):
            self.set_mode("support", reason=f"protection_{state.emotion}")
            return self._current_mode

        # Résolution mode depuis émotion
        target_mode = self._resolve_mode_from_emotion(state.emotion)
        if target_mode and target_mode != self._current_mode:
            self.set_mode(target_mode, reason=f"emotion_{state.emotion}")

        return self._current_mode

    def update_from_context(self, energy_level: str, intent: str) -> str:
        """
        Met à jour le mode depuis le contexte (énergie + intention).

        Args:
            energy_level : high / medium / low
            intent       : Intention NLP détectée

        Returns:
            Mode résultant
        """
        # Énergie basse → support
        if energy_level == "low":
            self.set_mode("support", reason="low_energy")
            return self._current_mode

        # Intent → mode
        target = INTENT_TO_MODE.get(intent)
        if target and target != self._current_mode:
            self.set_mode(target, reason=f"intent_{intent}")

        return self._current_mode

    def update_from_signals(
        self,
        emotion: EmotionalState | None = None,
        energy_level: str | None = None,
        intent: str | None = None,
        trend_concerning: bool = False,
    ) -> str:
        """
        Résout le mode à partir de plusieurs signaux combinés, avec un ordre
        de priorité explicite plutôt que des appels séquentiels qui
        s'écrasent silencieusement l'un l'autre (bug corrigé le 14/08/2026 :
        regulation_engine.py appelait update_from_emotion() PUIS
        update_from_context(), et l'intent pouvait annuler une décision
        d'émotion pourtant plus prioritaire — ex. émotion "stressed"→support
        écrasé par intent "engineering"→focus sur la même requête).

        Ordre de priorité :
            1. Protection / détresse (absolu)
            2. Énergie basse
            3. Émotion dominante (si elle résout vers un mode connu)
            4. Tendance émotionnelle préoccupante sur plusieurs jours (session 4,
               18/08/2026 — voir emotional_trend.py) : seulement si l'émotion
               instantanée n'a rien résolu, sinon l'instant présent garde priorité.
            5. Intention (utilisée seulement si rien au-dessus n'a résolu)

        Args:
            emotion          : EmotionalState depuis emotion_detector (optionnel)
            energy_level     : high / medium / low (optionnel)
            intent           : Intention NLP détectée (optionnel)
            trend_concerning : True si emotional_trend.get_emotion_trend() détecte
                               un motif négatif soutenu sur plusieurs jours (pas
                               l'instant présent — un signal plus lent, orthogonal
                               à `emotion`)

        Returns:
            Mode résultant
        """
        from src.regulation.protection_guard import is_protection_needed

        if emotion is not None and is_protection_needed(emotion):
            self.set_mode("support", reason=f"protection_{emotion.emotion}")
            return self._current_mode

        if energy_level == "low":
            self.set_mode("support", reason="low_energy")
            return self._current_mode

        # "neutral" est l'état par défaut du détecteur d'émotion (absence de
        # signal), pas une émotion dominante réelle — le laisser prioritaire
        # sur l'intent masquerait systématiquement l'intent dès qu'aucune
        # émotion marquée n'est détectée (cas majoritaire en usage réel,
        # constaté lors de la vérification manuelle du 14/08/2026).
        if emotion is not None and emotion.emotion not in (None, "", "neutral"):
            target = self._resolve_mode_from_emotion(emotion.emotion)
            if target:
                if target != self._current_mode:
                    self.set_mode(target, reason=f"emotion_{emotion.emotion}")
                return self._current_mode

        # Émotion instantanée neutre/absente, mais tendance soutenue négative
        # sur plusieurs jours : pencher vers "complicite" (présence chaleureuse,
        # pas "support" qui reste réservé à une détresse réellement détectée
        # maintenant — la nuance entre "ça ne va pas là, maintenant" et "elle
        # semble éprouvée ces derniers temps" compte).
        if trend_concerning and "complicite" != self._current_mode:
            self.set_mode("complicite", reason="emotion_trend_concerning")
            return self._current_mode
        elif trend_concerning:
            return self._current_mode

        if intent:
            target = INTENT_TO_MODE.get(intent)
            if target and target != self._current_mode:
                self.set_mode(target, reason=f"intent_{intent}")

        return self._current_mode

    def _resolve_mode_from_emotion(self, emotion: str) -> str | None:
        """Résout le mode cible depuis une émotion."""
        for mode_id, config in MODES.items():
            if emotion in config.triggers:
                return mode_id
        return None

    # ─────────────────────────────────────────────────────
    # Contenu adapté au mode
    # ─────────────────────────────────────────────────────

    def get_mode_prefix(self) -> str:
        """
        Retourne un préfixe de réponse adapté au mode courant.
        Utilisé au début des réponses ALFRED pour ancrer le ton.
        """
        prefixes = {
            "support":    [
                "Je t'entends.",
                "Je suis là.",
                "On prend le temps.",
                "Dis-moi.",
            ],
            "focus":      [
                "Voilà ce qu'on fait.",
                "Concrètement :",
                "En trois points :",
                "Voici l'essentiel :",
            ],
            "challenge":  [
                "Allez, on y va.",
                "Tu as tout ce qu'il faut.",
                "Maintenant :",
                "C'est le moment.",
            ],
            "complicite": [
                "Bonne question.",
                "Ah, ça c'est intéressant.",
                "",
                "Tiens,",
            ],
        }
        import random
        options = prefixes.get(self._current_mode, [""])
        return random.choice(options)

    def get_response_guidelines(self) -> str:
        """
        Retourne les directives de réponse pour le mode courant.
        Injectées dans le prompt système du LLM.
        """
        config = self.current_config
        return (
            f"[Mode ALFRED : {config.label_fr}]\n"
            f"Ton : {config.tone}\n"
            f"Style : {config.response_style}"
        )

    # ─────────────────────────────────────────────────────
    # Hooks & callbacks
    # ─────────────────────────────────────────────────────

    def register_transition_hook(self, callback: Callable) -> None:
        """
        Enregistre un hook appelé à chaque transition de mode.
        Utilisé pour notifier l'avatar, changer la voix, etc.

        Args:
            callback : Fonction(mode_from: str, mode_to: str) → None
        """
        self._on_transition.append(callback)

    # ─────────────────────────────────────────────────────
    # Status & historique
    # ─────────────────────────────────────────────────────

    def get_status(self) -> dict:
        """Retourne l'état complet du gestionnaire de mode."""
        config = self.current_config
        return {
            "current_mode":   self._current_mode,
            "previous_mode":  self._previous_mode,
            "tone":           config.tone,
            "voice_profile":  config.voice_profile,
            "transitions":    len(self._transition_log),
            "last_transition": self._transition_log[-1] if self._transition_log else None,
        }

    def get_transition_log(self) -> list[dict]:
        """Retourne l'historique des transitions de mode."""
        return self._transition_log.copy()


# ─────────────────────────────────────────────────────────
# Singleton session
# ─────────────────────────────────────────────────────────

_mode_manager: ModeManager | None = None


def get_mode_manager() -> ModeManager:
    """
    Retourne l'instance singleton du ModeManager.
    Créé à la première demande, conservé pour la session.
    """
    global _mode_manager
    if _mode_manager is None:
        _mode_manager = ModeManager()
    return _mode_manager
