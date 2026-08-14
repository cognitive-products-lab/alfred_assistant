"""
════════════════════════════════════════════════════════════
PROJECT      : ALFRED
BLOCK        : B03
FUNCTION     : 03.00
FILE         : src/regulation/regulation_engine.py
ROLE         : Orchestrateur pipeline émotionnel et santé

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-05-10
UPDATED      : 2026-05-28
VERSION      : V1.0
STATUS       : TESTED
════════════════════════════════════════════════════════════
"""
# ============================================================
# ALFRED — src/regulation/regulation_engine.py
# Bloc 03 / 13 — Orchestrateur pipeline émotionnel & santé
#
# Fonctions couvertes :
#   Bloc 03 : Chaîne détection émotion → bien-être → mode → personnalité
#   Bloc 13 : Détection signaux santé → protocole → adaptation interaction
#
# Pipeline complet :
#   1. NLP (Bloc 01)         → intent, langue, entités
#   2. Émotion (Bloc 03.01)  → état émotionnel enrichi
#   3. Bien-être (Bloc 03.05)→ énergie, fatigue, flow
#   4. Protection (Bloc 03.04)→ crise, garde-fous éthiques
#   5. Santé (Bloc 13)       → signaux fragilité, protocoles
#   6. Mode (Bloc 03.02/03)  → sélection mode dynamique
#   7. Adaptation (Bloc 13.05)→ fusion paramètres finaux
#   8. Retour PipelineContext → prêt pour response_generator
# ============================================================

import json
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from src.regulation.emotion_detector  import detect_emotion, EmotionalState
from src.regulation.mode_manager      import get_mode_manager, MODES
from src.regulation.protection_guard  import is_crisis, is_protection_needed, get_crisis_response, get_protection_response
from src.regulation.wellbeing_tracker import analyze_wellbeing, log_wellbeing_point, get_wellbeing_suggestion
from src.health.chronic_support       import detect_health_signals, detect_cognitive_patterns, get_cognitive_pattern_adaptation, get_condition_adaptations, get_adapted_response, HealthSignalResult
from src.health.interaction_adapter   import adapt_for_health_context, validate_health_response, get_check_in_message, AdaptedInteractionParams
from src.health.health_profile        import HealthProfile
from src.health.profile_loader        import UserAdaptationContext, get_user_context
from src.security.security_logger     import log_event

try:
    from src.conversation.input.nlp_engine_v2 import analyze_v2 as nlp_analyze
    _NLP_AVAILABLE = True
except ImportError:
    _NLP_AVAILABLE = False
    log_event("NLP V2 non disponible — mode dégradé", "WARNING")


# ─────────────────────────────────────────────────────────
# Résultat du pipeline
# ─────────────────────────────────────────────────────────

@dataclass
class PipelineContext:
    """
    Contexte complet produit par le pipeline émotionnel et santé.
    Transmis à response_generator pour construire la réponse d'ALFRED.
    """

    # ── Méta ─────────────────────────────────────────────
    timestamp:        str = field(default_factory=lambda: datetime.now().isoformat())
    raw_input:        str = ""
    pipeline_version: str = "V1.0"

    # ── NLP (Bloc 01) ─────────────────────────────────────
    intent:           str   = "general"
    intent_label:     str   = "Général"
    language:         str   = "fr"
    entities:         dict  = field(default_factory=dict)
    nlp_confidence:   float = 0.0

    # ── Émotion (Bloc 03.01) ──────────────────────────────
    emotion:          str   = "neutral"
    emotion_label:    str   = "neutre"
    emotion_intensity:float = 0.0
    emotion_valence:  str   = "neutral"
    emotion_arousal:  str   = "medium"
    emotion_signals:  list  = field(default_factory=list)

    # ── Bien-être (Bloc 03.05) ────────────────────────────
    energy_level:     str   = "medium"
    fatigue_score:    float = 0.0
    flow_detected:    bool  = False
    wellbeing_suggestion: Optional[str] = None

    # ── Protection (Bloc 03.04) ───────────────────────────
    protection_active:bool  = False
    crisis_detected:  bool  = False
    protection_response: Optional[str] = None

    # ── Mode (Bloc 03.02/03.03) ───────────────────────────
    mode:             str   = "focus"
    mode_label:       str   = "Mode travail & clarté"
    mode_prefix:      str   = ""
    mode_guidelines:  str   = ""

    # ── Santé (Bloc 13) ───────────────────────────────────
    health_active:          bool  = False
    health_signal_type:     Optional[str] = None
    health_protocol_id:     Optional[str] = None
    health_fog_mode:        bool  = False
    health_pain_mode:       bool  = False
    health_flare:           bool  = False
    health_bipolar_episode: bool  = False
    health_rumination:      bool  = False
    health_hyperfocus:      bool  = False
    health_conditions:      list  = field(default_factory=list)
    health_adapted_response: Optional[str] = None
    cognitive_patterns:     list  = field(default_factory=list)  # patterns cognitifs détectés

    # ── Profil utilisateur (Onboarding) ───────────────────
    user_mbti:             str   = ""
    user_validate_first:   bool  = False   # surcharge MBTI/profil émotionnel
    user_humor_pref:       bool  = True
    user_context_loaded:   bool  = False

    # ── Paramètres de réponse finaux (Bloc 13.05) ─────────
    response_length:       str   = "medium"
    response_length_desc:  str   = "4-8 phrases"
    max_bullet_points:     int   = 5
    tone:                  str   = ""
    warmth:                float = 0.75
    patience:              float = 0.80
    validation_first:      bool  = False
    avoid_advice:          bool  = False
    humor_allowed:         bool  = True
    check_in_message:      Optional[str] = None
    offer_pause:           bool  = False
    forbidden_phrases:     list  = field(default_factory=list)

    # ── Guidelines LLM ───────────────────────────────────
    llm_system_context:    str   = ""


# ─────────────────────────────────────────────────────────
# Moteur d'orchestration
# ─────────────────────────────────────────────────────────

class RegulationEngine:
    """
    Orchestrateur central du pipeline émotionnel et santé d'ALFRED.

    Chaîne Bloc 01 (NLP) → Bloc 03 (émotion/mode) → Bloc 13 (santé)
    et produit un PipelineContext unifié prêt pour la génération de réponse.

    Usage :
        engine  = RegulationEngine()
        profile = HealthProfile(user_id="default")
        context = engine.process(user_input="je suis épuisée", health_profile=profile)
    """

    def __init__(self):
        self._mode_manager = get_mode_manager()
        log_event("RegulationEngine initialisé (Bloc 03 + Bloc 13)")

    # ─────────────────────────────────────────────────────
    # Pipeline principal
    # ─────────────────────────────────────────────────────

    def process(
        self,
        user_input:      str,
        time_context:    dict | None               = None,
        health_profile:  HealthProfile | None      = None,
        user_context:    UserAdaptationContext | None = None,
        user_id:         str | None                = None,
    ) -> PipelineContext:
        """
        Traitement complet d'un message utilisateur.

        Args:
            user_input     : Message brut de l'utilisateur
            time_context   : Contexte temporel (heure, énergie, période)
            health_profile : Profil santé optionnel (Bloc 13)
            user_context   : Contexte d'adaptation utilisateur (onboarding)
            user_id        : Identifiant utilisateur — charge le user_context si absent

        Returns:
            PipelineContext — contexte complet pour la génération de réponse
        """
        ctx = PipelineContext(raw_input=user_input)

        if health_profile is None:
            health_profile = HealthProfile()
        health_profile.increment_turn()

        # ── 0. Profil utilisateur (onboarding) ────────────
        if user_context is None and user_id:
            try:
                user_context = get_user_context(user_id)
            except Exception:
                user_context = None
        if user_context and user_context.profile_complete:
            self._apply_user_context(ctx, user_context)

        # ── 1. NLP ────────────────────────────────────────
        self._run_nlp(ctx, user_input)

        # ── 2. Émotion ────────────────────────────────────
        emotion_state = detect_emotion(user_input)
        self._apply_emotion(ctx, emotion_state)

        # ── 3. Bien-être ──────────────────────────────────
        self._run_wellbeing(ctx, user_input, time_context)

        # ── 4. Protection ─────────────────────────────────
        self._run_protection(ctx, user_input, emotion_state)
        if ctx.protection_active:
            # Court-circuit : mode support forcé, réponse de protection fournie
            self._finalize_protection(ctx, health_profile)
            return ctx

        # ── 5. Santé & patterns cognitifs (Bloc 13) ──────
        health_signals = detect_health_signals(user_input)
        self._apply_health(ctx, health_signals, health_profile)

        # ── 6. Mode ───────────────────────────────────────
        self._run_mode(ctx, emotion_state, health_signals)

        # ── 7. Adaptation interaction ──────────────────────
        mode_config = MODES.get(ctx.mode, {})
        mode_dict   = {
            "personality":             vars(mode_config) if hasattr(mode_config, '__dict__') else {},
            "tone":                    getattr(mode_config, "tone", ""),
            "response_guidelines_llm": getattr(mode_config, "voice_profile", ""),
        }
        adapted = adapt_for_health_context(
            signal_result  = health_signals,
            health_profile = health_profile,
            emotion_state  = emotion_state,
            mode_config    = mode_dict,
        )
        self._apply_adaptation(ctx, adapted, health_profile)

        # ── 8. Guidelines LLM finales ─────────────────────
        self._build_llm_context(ctx, health_signals, health_profile)

        log_event(
            f"Pipeline terminé — émotion: {ctx.emotion}, mode: {ctx.mode}, "
            f"santé: {ctx.health_active}, fog: {ctx.health_fog_mode}"
        )

        return ctx

    # ─────────────────────────────────────────────────────
    # Étapes internes
    # ─────────────────────────────────────────────────────

    def _apply_user_context(self, ctx: PipelineContext, uc: UserAdaptationContext) -> None:
        """Applique le profil d'onboarding utilisateur au PipelineContext."""
        ctx.user_mbti          = uc.mbti_type
        ctx.user_validate_first = uc.validate_first
        ctx.user_humor_pref    = uc.humor_enabled
        ctx.user_context_loaded = True

        # Pré-remplissage des paramètres de réponse depuis le profil
        if uc.validate_first:
            ctx.validation_first = True
        if not uc.humor_enabled:
            ctx.humor_allowed = False
        if uc.topics_avoid:
            ctx.forbidden_phrases.extend(uc.topics_avoid)

    def _run_nlp(self, ctx: PipelineContext, text: str) -> None:
        if not _NLP_AVAILABLE:
            ctx.intent    = "general"
            ctx.language  = "fr"
            return
        try:
            result            = nlp_analyze(text)
            ctx.intent        = result.get("intent", "general")
            ctx.intent_label  = result.get("intent_label", "Général")
            ctx.language      = result.get("language", "fr")
            ctx.entities      = result.get("entities", {})
            ctx.nlp_confidence = result.get("confidence", 0.0)
        except Exception as e:
            log_event(f"Erreur NLP : {e}", "WARNING")

    def _apply_emotion(self, ctx: PipelineContext, state: EmotionalState) -> None:
        ctx.emotion           = state.emotion
        ctx.emotion_intensity = state.intensity
        ctx.emotion_valence   = state.valence
        ctx.emotion_arousal   = state.arousal
        ctx.emotion_signals   = state.signals

        _labels = {
            "distress": "détresse", "stressed": "stress", "anxious": "anxiété",
            "sad": "tristesse", "grieving": "deuil", "tired": "fatigue",
            "confused": "confusion", "frustrated": "frustration",
            "motivated": "motivation", "happy": "joie", "focused": "concentration",
            "curious": "curiosité", "content": "sérénité", "neutral": "neutre",
        }
        ctx.emotion_label = _labels.get(state.emotion, state.emotion)

    def _run_wellbeing(self, ctx: PipelineContext, text: str, time_context: dict | None) -> None:
        try:
            wb_state              = analyze_wellbeing(text, time_context)
            ctx.energy_level      = wb_state.energy_level
            ctx.fatigue_score     = wb_state.fatigue_score
            ctx.flow_detected     = wb_state.flow_detected
            ctx.wellbeing_suggestion = get_wellbeing_suggestion(wb_state)
            log_wellbeing_point(wb_state)
        except Exception as e:
            log_event(f"Erreur wellbeing : {e}", "WARNING")

    def _run_protection(self, ctx: PipelineContext, text: str, emotion_state: EmotionalState) -> None:
        if is_crisis(text):
            ctx.protection_active   = True
            ctx.crisis_detected     = True
            ctx.protection_response = get_crisis_response()
            log_event("CRISE ABSOLUE détectée — pipeline interrompu", "CRITICAL")
            return

        if is_protection_needed(emotion_state):
            ctx.protection_active   = True
            ctx.protection_response = get_protection_response(
                emotion_state.emotion, emotion_state.intensity
            )
            log_event(f"Mode protection activé — {emotion_state.emotion}", "WARNING")

    def _finalize_protection(self, ctx: PipelineContext, health_profile: HealthProfile) -> None:
        ctx.mode          = "support"
        ctx.mode_label    = "Mode présence & soutien"
        ctx.response_length = "very_short"
        ctx.validation_first = True
        ctx.avoid_advice    = True
        ctx.tone            = "doux, présent, rassurant"
        ctx.warmth          = 1.0
        ctx.patience        = 1.0
        ctx.humor_allowed   = False
        self._build_llm_context(ctx, HealthSignalResult(), health_profile)

    def _apply_health(
        self,
        ctx:            PipelineContext,
        signals:        HealthSignalResult,
        health_profile: HealthProfile,
    ) -> None:
        ctx.health_active          = signals.detected or health_profile.is_active
        ctx.health_signal_type     = signals.signal_type
        ctx.health_protocol_id     = signals.protocol_id
        ctx.health_fog_mode        = signals.fog_detected
        ctx.health_pain_mode       = signals.pain_detected
        ctx.health_flare           = signals.flare_detected
        ctx.health_bipolar_episode = signals.bipolar_episode
        ctx.health_rumination      = signals.rumination_active
        ctx.health_hyperfocus      = signals.hyperfocus_active
        ctx.cognitive_patterns     = signals.cognitive_patterns
        ctx.health_conditions      = health_profile.conditions + signals.condition_hints

        # Activer l'état de session santé
        if signals.fog_detected and health_profile.fog_auto_activate:
            health_profile.activate_fog_mode()
        if signals.flare_detected:
            health_profile.activate_flare()
        if signals.pain_detected:
            health_profile.activate_pain_mode()
        if signals.pacing_detected:
            health_profile.activate_energy_pacing()
        if signals.protocol_id:
            health_profile.set_protocol(signals.protocol_id)

        # Réponse adaptée Bloc 13
        ctx.health_adapted_response = get_adapted_response(signals, ctx.emotion)

    def _run_mode(
        self,
        ctx:     PipelineContext,
        emotion: EmotionalState,
        health:  HealthSignalResult,
    ) -> None:
        # Santé critique → force support
        if health.crisis_health or health.flare_detected:
            self._mode_manager.set_mode("support", reason="health_signal")
        else:
            # Émotion + énergie + intent combinés avec priorité explicite
            # (docs/architecture/vision_architecture_cognitive_alfred.md,
            # section P4) — remplace deux appels séquentiels
            # (update_from_emotion puis update_from_context) où le second
            # pouvait écraser silencieusement une décision d'émotion plus
            # prioritaire.
            self._mode_manager.update_from_signals(
                emotion=emotion, energy_level=ctx.energy_level, intent=ctx.intent,
            )

        mode_cfg         = self._mode_manager.get_current_config()
        ctx.mode         = self._mode_manager.current_mode
        ctx.mode_label   = mode_cfg.label_fr
        ctx.mode_prefix  = self._mode_manager.get_mode_prefix()
        ctx.mode_guidelines = self._mode_manager.get_response_guidelines()

    def _apply_adaptation(
        self,
        ctx:            PipelineContext,
        adapted:        AdaptedInteractionParams,
        health_profile: HealthProfile,
    ) -> None:
        ctx.response_length      = adapted.response_length
        ctx.response_length_desc = adapted.response_length_desc
        ctx.max_bullet_points    = adapted.max_bullet_points
        ctx.tone                 = adapted.tone_description
        ctx.warmth               = adapted.warmth
        ctx.patience             = adapted.patience
        ctx.validation_first     = adapted.validate_first
        ctx.avoid_advice         = adapted.avoid_advice
        ctx.humor_allowed        = adapted.humor_allowed
        ctx.offer_pause          = adapted.offer_pause
        ctx.forbidden_phrases    = adapted.forbidden_phrases

        # Check-in Bloc 13
        ctx.check_in_message = get_check_in_message(
            frequency  = adapted.check_in_frequency,
            turn_count = health_profile.session.turn_count,
        )

    def _build_llm_context(
        self,
        ctx:            PipelineContext,
        health_signals: HealthSignalResult,
        health_profile: HealthProfile,
    ) -> None:
        """Construit les directives système à injecter dans le prompt LLM."""
        lines = [
            f"[Mode ALFRED : {ctx.mode_label}]",
            f"Ton : {ctx.tone or ctx.mode_guidelines}",
            f"Longueur de réponse : {ctx.response_length_desc}",
            f"Émotion utilisateur détectée : {ctx.emotion_label} (intensité {ctx.emotion_intensity:.1f})",
        ]

        if ctx.validation_first:
            lines.append("IMPÉRATIF : valider l'émotion ou l'expérience AVANT toute information ou conseil.")

        if ctx.avoid_advice:
            lines.append("Ne donner aucun conseil non sollicité dans cette réponse.")

        if ctx.health_fog_mode:
            lines.append(
                "BROUILLARD COGNITIF ACTIF : réponse en 3 phrases MAX, "
                "vocabulaire simple, une idée par phrase, pas de listes complexes."
            )

        if ctx.health_pain_mode:
            lines.append("L'utilisateur est en douleur — valider, ne jamais minimiser, ne pas suggérer d'effort.")

        if ctx.health_flare:
            lines.append("POUSSÉE CHRONIQUE DÉTECTÉE — douceur maximale, rythme lent, aucune pression.")

        if ctx.health_conditions:
            conds = ", ".join(ctx.health_conditions[:3])
            lines.append(f"Contexte de santé chronique : {conds} — adapter le comportement sans jamais diagnostiquer.")

        if ctx.forbidden_phrases:
            lines.append(f"Formulations interdites dans ce contexte : {'; '.join(ctx.forbidden_phrases[:5])}")

        if not ctx.humor_allowed:
            lines.append("Aucun humour dans cette réponse.")

        if ctx.health_bipolar_episode:
            lines.append(
                "ÉPISODE BIPOLAIRE POSSIBLE — ton stable et ancré, "
                "ne pas amplifier l'euphorie ni la dépression, proposer d'ancrer dans le présent."
            )

        if ctx.health_rumination:
            lines.append(
                "RUMINATIONS DÉTECTÉES — ne pas alimenter le contenu des pensées en boucle. "
                "Nommer doucement le phénomène, proposer un ancrage présent."
            )

        if ctx.health_hyperfocus:
            lines.append(
                "HYPERFOCUS PROBABLE — ne pas interrompre brusquement. "
                "Si interruption nécessaire : signal doux, préavis court."
            )

        if ctx.cognitive_patterns:
            pattern_labels = {
                "stress_chronique": "stress chronique",
                "anxiete_chronique": "anxiété chronique",
                "fibro_fog": "fibro fog",
                "ruminations": "ruminations",
                "hyperfocus_dissociatif": "hyperfocus",
                "surcharge_sensorielle": "surcharge sensorielle",
            }
            detected = [pattern_labels.get(p, p) for p in ctx.cognitive_patterns]
            lines.append(f"Patterns cognitifs actifs : {', '.join(detected)}.")

        if ctx.user_mbti:
            mbti_directives = {
                "I": "Attendre que l'utilisateur initie — ne pas sur-solliciter.",
                "E": "L'utilisateur apprécie les échanges proactifs.",
                "F": "Priorité à la validation émotionnelle avant toute solution.",
                "T": "Réponses directes et logiques bienvenues.",
                "S": "Exemples concrets et étapes pratiques privilégiés.",
                "N": "Vision globale et connexions conceptuelles bienvenues.",
                "J": "Réponses structurées avec étapes claires.",
                "P": "Ton flexible, éviter la rigidité dans les plans.",
            }
            mbti_hints = [mbti_directives[l] for l in ctx.user_mbti if l in mbti_directives]
            if mbti_hints:
                lines.append(f"Adaptation MBTI ({ctx.user_mbti}) : {' '.join(mbti_hints)}")

        if ctx.protection_active and ctx.protection_response:
            lines.append("\n[MODE PROTECTION ACTIF]\n" + ctx.protection_response)

        ctx.llm_system_context = "\n".join(lines)


# ─────────────────────────────────────────────────────────
# Singleton session
# ─────────────────────────────────────────────────────────

_engine: RegulationEngine | None = None


def get_regulation_engine() -> RegulationEngine:
    """Retourne l'instance singleton du moteur de régulation."""
    global _engine
    if _engine is None:
        _engine = RegulationEngine()
    return _engine


def process_message(
    user_input:     str,
    time_context:   dict | None               = None,
    health_profile: HealthProfile | None      = None,
    user_context:   UserAdaptationContext | None = None,
    user_id:        str | None                = None,
) -> PipelineContext:
    """
    Point d'entrée simplifié — traitement complet d'un message.

    Args:
        user_input     : Message de l'utilisateur
        time_context   : Contexte temporel (optionnel)
        health_profile : Profil santé (optionnel — Bloc 13)
        user_context   : Contexte d'adaptation utilisateur (onboarding)
        user_id        : Identifiant utilisateur — charge le contexte auto si fourni

    Returns:
        PipelineContext prêt pour response_generator

    Exemples :
        # Usage minimal
        ctx = process_message("je suis épuisée")

        # Avec profil complet
        ctx = process_message("j'ai un fog terrible", user_id="user_001")
        ctx.user_mbti           # "INFJ"
        ctx.health_fog_mode     # True
        ctx.cognitive_patterns  # ["fibro_fog"]
        ctx.llm_system_context  # directives LLM fusionnées
    """
    return get_regulation_engine().process(
        user_input, time_context, health_profile, user_context, user_id
    )
