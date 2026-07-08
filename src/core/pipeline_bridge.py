"""
PROJECT      : ALFRED
BLOCK        : 03 / 13 — Bridge pipeline
FUNCTION     : Core bridge
FILE         : src/core/pipeline_bridge.py
ROLE         : Pont entre PipelineContext (Blocs 03+13) et ResponseGenerator (core)

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-06-01
VERSION      : V1.0
STATUS       : TESTED

DESCRIPTION :
Fusionne le PipelineContext produit par regulation_engine avec le response_context
attendu par ResponseGenerator. Permet d'intégrer l'IA émotionnelle/santé (Blocs 03+13)
dans la boucle conversationnelle existante (main.py V1.2) sans réécrire le générateur.

Usage dans build_response() :
    from src.core.pipeline_bridge import enrich_context_with_pipeline, get_pipeline_mode_guidelines

    pipeline_ctx = process_message(user_input, user_id=user_id)
    enrich_context_with_pipeline(response_context, pipeline_ctx)
    guidelines   = get_pipeline_mode_guidelines(pipeline_ctx)
    # Passer guidelines à generator.generate_response(mode_guidelines=guidelines)
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from src.regulation.regulation_engine import PipelineContext


# ── Mapping longueur de réponse → profondeur ResponseGenerator ─────────────

_LENGTH_TO_DEPTH = {
    "very_short": "minimal",
    "short":      "short",
    "medium":     "medium",
    "long":       "detailed",
    "adaptive":   "medium",
}

# Modes pipeline B03 → modes behavior_engine
_PIPELINE_MODE_TO_BEHAVIOR = {
    "support":    "support_mode",
    "focus":      "execution_mode",
    "challenge":  "execution_mode",
    "complicite": "hybrid_mode",
}


def enrich_context_with_pipeline(
    response_context: dict[str, Any],
    pipeline_ctx: "PipelineContext",
) -> None:
    """
    Enrichit le response_context (format ResponseGenerator) avec les données
    issues de PipelineContext (Blocs 03+13).

    Modifie response_context en place.
    Priorité : le pipeline prend le dessus sur les heuristiques mode/ton
    quand il a détecté un signal fort (protection, santé, MBTI explicite).

    Args:
        response_context : Dict produit par PersonalityAdapter.build_response_context()
        pipeline_ctx     : PipelineContext produit par process_message()
    """
    adaptation = response_context.setdefault("adaptation", {})
    rules      = response_context.setdefault("response_rules", {})
    boundaries = response_context.setdefault("boundaries", {})

    # ── Mode & ton (pipeline prioritaire si signal fort) ──────────────────────
    if pipeline_ctx.protection_active:
        adaptation["mode"] = "support_mode"
        adaptation["tone"] = "doux, présent, rassurant"
    elif pipeline_ctx.health_active and pipeline_ctx.health_fog_mode:
        adaptation["mode"] = "support_mode"
        adaptation["tone"] = "simple, lent, sans pression"
    elif pipeline_ctx.mode:
        behavior_mode = _PIPELINE_MODE_TO_BEHAVIOR.get(pipeline_ctx.mode)
        if behavior_mode:
            adaptation["mode"] = behavior_mode
        if pipeline_ctx.tone:
            adaptation["tone"] = pipeline_ctx.tone

    # ── Profondeur de réponse ─────────────────────────────────────────────────
    if pipeline_ctx.response_length:
        depth = _LENGTH_TO_DEPTH.get(pipeline_ctx.response_length, "medium")
        adaptation["response_depth"] = depth

    # ── Niveau émotionnel ─────────────────────────────────────────────────────
    intensity = pipeline_ctx.emotion_intensity
    if intensity >= 0.7:
        adaptation["emotional_level"] = 3
    elif intensity >= 0.4:
        adaptation["emotional_level"] = 2
    elif intensity >= 0.2:
        adaptation["emotional_level"] = 1
    else:
        adaptation["emotional_level"] = 0

    adaptation["detected_emotion"] = pipeline_ctx.emotion

    # ── Règles de réponse ─────────────────────────────────────────────────────
    if pipeline_ctx.validation_first:
        rules["use_empathy"]   = True
        rules["validate_first"] = True

    rules["use_humor"] = pipeline_ctx.humor_allowed
    rules["avoid_advice"] = pipeline_ctx.avoid_advice

    if pipeline_ctx.health_fog_mode:
        rules["avoid_overload"]    = True
        rules["use_step_by_step"]  = False
        rules["be_structured"]     = False

    # ── Frontières et phrases interdites ─────────────────────────────────────
    if pipeline_ctx.forbidden_phrases:
        existing = boundaries.get("forbidden_phrases", [])
        boundaries["forbidden_phrases"] = list(set(existing + pipeline_ctx.forbidden_phrases))

    # ── Santé (Bloc 13) — section dédiée ─────────────────────────────────────
    response_context["health_context"] = {
        "active":         pipeline_ctx.health_active,
        "fog_mode":       pipeline_ctx.health_fog_mode,
        "pain_mode":      pipeline_ctx.health_pain_mode,
        "flare":          pipeline_ctx.health_flare,
        "bipolar":        pipeline_ctx.health_bipolar_episode,
        "rumination":     pipeline_ctx.health_rumination,
        "hyperfocus":     pipeline_ctx.health_hyperfocus,
        "conditions":     pipeline_ctx.health_conditions,
        "signal_type":    pipeline_ctx.health_signal_type,
        "protocol_id":    pipeline_ctx.health_protocol_id,
        "adapted_response": pipeline_ctx.health_adapted_response,
        "cognitive_patterns": pipeline_ctx.cognitive_patterns,
    }

    # ── Check-in Bloc 13 ──────────────────────────────────────────────────────
    if pipeline_ctx.check_in_message:
        response_context["check_in_message"] = pipeline_ctx.check_in_message

    # ── Pause suggérée ────────────────────────────────────────────────────────
    if pipeline_ctx.offer_pause:
        response_context["offer_pause"] = True

    # ── Profil onboarding (MBTI + préférences) ────────────────────────────────
    if pipeline_ctx.user_context_loaded:
        onboarding = response_context.setdefault("onboarding", {})
        onboarding["mbti"]          = pipeline_ctx.user_mbti
        onboarding["loaded"]        = True
        onboarding["validate_first"] = pipeline_ctx.user_validate_first
        onboarding["humor_pref"]    = pipeline_ctx.user_humor_pref

    # ── Protection (Bloc 03.04) ────────────────────────────────────────────────
    if pipeline_ctx.protection_active and pipeline_ctx.protection_response:
        response_context["protection_active"]   = True
        response_context["protection_response"] = pipeline_ctx.protection_response


def get_pipeline_mode_guidelines(pipeline_ctx: "PipelineContext") -> str:
    """
    Retourne les guidelines LLM du pipeline sous forme de chaîne,
    à injecter comme mode_guidelines dans ResponseGenerator.generate_response().

    Contient : mode, santé, MBTI, patterns cognitifs, directives spéciales.

    Args:
        pipeline_ctx : PipelineContext produit par process_message()

    Returns:
        String à passer à generate_response(mode_guidelines=...)
    """
    return pipeline_ctx.llm_system_context or ""


def build_session_summary_from_pipeline(
    pipeline_ctx:   "PipelineContext",
    exchange_count: int,
) -> dict[str, Any]:
    """
    Construit un session_summary compatible ResponseGenerator depuis PipelineContext.

    Args:
        pipeline_ctx   : PipelineContext courant
        exchange_count : Nombre d'échanges de la session

    Returns:
        Dict session_summary pour ResponseGenerator._build_system_prompt()
    """
    return {
        "exchange_count":  exchange_count,
        "dominant_emotion": pipeline_ctx.emotion,
        "emotions_seen":   [pipeline_ctx.emotion],
        "topics":          [pipeline_ctx.intent] if pipeline_ctx.intent else [],
        "energy_level":    pipeline_ctx.energy_level,
        "health_active":   pipeline_ctx.health_active,
        "fog_mode":        pipeline_ctx.health_fog_mode,
    }


def should_use_health_adapted_response(pipeline_ctx: "PipelineContext") -> bool:
    """
    Détermine si on doit court-circuiter le LLM avec la réponse adaptée
    santé (ex: crise, fog sévère avec template défini).

    Args:
        pipeline_ctx : PipelineContext courant

    Returns:
        True si la réponse adaptée santé doit être utilisée directement
    """
    if pipeline_ctx.protection_active and pipeline_ctx.protection_response:
        return True
    # Crise santé avec réponse template définie
    if pipeline_ctx.health_active and pipeline_ctx.health_signal_type == "crisis_health_signals":
        if pipeline_ctx.health_adapted_response:
            return True
    return False


def get_forced_response(pipeline_ctx: "PipelineContext") -> str | None:
    """
    Retourne la réponse forcée (protection ou crise santé) si applicable,
    sinon None → le LLM prend le relais.

    Args:
        pipeline_ctx : PipelineContext courant

    Returns:
        Réponse texte forcée ou None
    """
    if pipeline_ctx.protection_active and pipeline_ctx.protection_response:
        return pipeline_ctx.protection_response

    if should_use_health_adapted_response(pipeline_ctx):
        return pipeline_ctx.health_adapted_response

    return None
