"""
════════════════════════════════════════════════════════════
PROJECT      : ALFRED
BLOCK        : B13
FUNCTION     : 13.05
FILE         : src/health/interaction_adapter.py
ROLE         : Adaptation interaction pour profils fragilisés

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-05-10
UPDATED      : 2026-05-28
VERSION      : V1.0
STATUS       : ACTIVE
════════════════════════════════════════════════════════════
"""
# ============================================================
# ALFRED — src/health/interaction_adapter.py
# Bloc 13.05 — Interaction adaptée pour profils fragilisés
#
# Fonctions couvertes :
#   13.05.001 Adaptation longueur réponse selon contexte santé   ✅ V1
#   13.05.002 Réduction charge cognitive                         ✅ V1
#   13.05.003 Paramètres de ton adaptés fragilité                ✅ V1
#   13.05.004 Fusion adaptations Bloc 03 (émotion) + Bloc 13     ✅ V1
#   13.05.005 Validation langage interdit en contexte santé      ✅ V1
# ============================================================

import json
from dataclasses import dataclass, field

from paths import CONFIG_HEALTH
from src.security.security_logger import log_event

# ── Chargement JSON ──────────────────────────────────────

def _load(filename: str) -> dict:
    path = CONFIG_HEALTH / filename
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))

_ADAPTATION_RULES = _load("health_adaptation_rules.json")
_PROTOCOLS        = _load("health_protocols.json").get("protocols", {})

_GLOBAL_ADAPTATIONS = _ADAPTATION_RULES.get("global_adaptations_when_health_profile_active", {})
_BY_SEVERITY        = _ADAPTATION_RULES.get("adaptations_by_severity", {})
_FORBIDDEN_PATTERNS = _ADAPTATION_RULES.get("forbidden_patterns_health_context", [])
_COMM_PRINCIPLES    = _ADAPTATION_RULES.get("communication_principles", {})
_LENGTH_MAP = {
    "very_short":       "1-2 phrases",
    "very_short_cap":   "1-2 phrases",
    "short":            "2-4 phrases",
    "short_to_medium":  "3-5 phrases",
    "medium":           "4-8 phrases",
    "detailed":         "structure complète",
    "adaptive":         "selon la demande",
    "très_courte":      "1-2 phrases",
    "courte_à_moyenne": "3-5 phrases",
}


# ─────────────────────────────────────────────────────────
# Paramètres d'interaction adaptée
# ─────────────────────────────────────────────────────────

@dataclass
class AdaptedInteractionParams:
    """Paramètres d'interaction résultant de la fusion Bloc 03 + Bloc 13."""

    # Longueur et charge cognitive
    response_length:    str   = "medium"
    response_length_desc: str = "4-8 phrases"
    max_bullet_points:  int   = 5
    max_questions:      int   = 1
    simple_vocabulary:  bool  = False
    short_sentences:    bool  = False

    # Ton
    warmth:             float = 0.75
    patience:           float = 0.80
    directness:         float = 0.70
    humor_allowed:      bool  = True
    validation_rate:    float = 0.50

    # Comportement
    validate_first:     bool  = False
    offer_pause:        bool  = False
    avoid_advice:       bool  = False
    avoid_questions_chains: bool = False
    one_step_at_a_time: bool  = False
    check_in_frequency: str   = "every_4_turns"

    # Flags spéciaux
    fog_mode:           bool  = False
    pain_mode:          bool  = False
    health_active:      bool  = False

    # Guidelines LLM (à injecter dans le prompt)
    tone_description:   str   = ""
    llm_guidelines:     str   = ""

    # Interdits actifs
    forbidden_phrases:  list[str] = field(default_factory=list)


# ─────────────────────────────────────────────────────────
# Adaptation principale
# ─────────────────────────────────────────────────────────

def adapt_for_health_context(
    signal_result,          # HealthSignalResult depuis chronic_support
    health_profile,         # HealthProfile depuis health_profile
    emotion_state=None,     # EmotionalState depuis emotion_detector (optionnel)
    mode_config: dict | None = None,  # Config du mode Bloc 03 (optionnel)
) -> AdaptedInteractionParams:
    """
    Calcule les paramètres d'interaction adaptés en fusionnant :
    - Context Bloc 03 (émotion, mode)
    - Context Bloc 13 (santé, fragilité, conditions)

    La couche santé est toujours prioritaire sur la couche émotionnelle
    quand les deux sont actives.

    Args:
        signal_result  : Résultat de chronic_support.detect_health_signals()
        health_profile : Profil santé de l'utilisateur
        emotion_state  : État émotionnel Bloc 03 (optionnel, pour fusion)
        mode_config    : Config du mode actif Bloc 03 (optionnel)

    Returns:
        AdaptedInteractionParams fusionnés
    """
    params = AdaptedInteractionParams()

    # ── Base : paramètres depuis le mode Bloc 03 ─────────
    if mode_config:
        personality = mode_config.get("personality", {})
        params.warmth      = personality.get("warmth", 0.75)
        params.patience    = 0.80
        params.directness  = personality.get("directness", 0.70)
        params.humor_allowed = personality.get("humor", 1.0) > 0.0
        params.validation_rate = personality.get("validation_rate", 0.50)
        params.tone_description = mode_config.get("tone", "")
        params.llm_guidelines   = mode_config.get("response_guidelines_llm", "")

    # ── Couche santé : active si profil ou signal détecté ─
    health_active = health_profile.is_active or signal_result.detected
    params.health_active = health_active

    if not health_active:
        return params

    # ── Adaptations globales profil santé ────────────────
    severity  = health_profile.severity if health_profile.is_active else "moderate"
    severity_cfg = _BY_SEVERITY.get(severity, _BY_SEVERITY.get("moderate", {}))

    # Longueur de réponse
    length_cap = _GLOBAL_ADAPTATIONS.get("response_length", {})
    if signal_result.fog_detected:
        params.response_length = length_cap.get("fog_cap", "very_short")
    elif signal_result.crisis_health:
        params.response_length = length_cap.get("crisis_cap", "very_short")
    elif signal_result.flare_detected:
        params.response_length = "short"
    else:
        params.response_length = length_cap.get("stable_cap", "medium")

    params.response_length_desc = _LENGTH_MAP.get(params.response_length, "adaptif")

    # Charge cognitive
    cog = _GLOBAL_ADAPTATIONS.get("cognitive_load", {})
    if signal_result.fog_detected:
        params.max_bullet_points  = cog.get("max_bullet_points_fog", 3)
        params.simple_vocabulary  = True
        params.short_sentences    = True
        params.fog_mode           = True
    else:
        params.max_bullet_points = cog.get("max_bullet_points_default", 5)

    params.max_questions = cog.get("max_questions_per_turn", 1)

    # Ton
    tone_baseline = _GLOBAL_ADAPTATIONS.get("tone_baseline", {})
    params.warmth          = max(params.warmth, tone_baseline.get("warmth", 0.95))
    params.patience        = tone_baseline.get("patience", 1.0)
    params.validation_rate = max(params.validation_rate, tone_baseline.get("validation_rate", 0.80))
    params.humor_allowed   = tone_baseline.get("humor", 0.10) > 0.5

    # Proactivité
    proactivity = _GLOBAL_ADAPTATIONS.get("proactivity", {})
    params.check_in_frequency = proactivity.get("check_in_frequency", "every_2_turns")
    params.offer_pause         = proactivity.get("offer_pause_regularly", True)

    # ── Protocole actif ──────────────────────────────────
    if signal_result.protocol_id and signal_result.protocol_id in _PROTOCOLS:
        protocol     = _PROTOCOLS[signal_result.protocol_id]
        proto_rules  = protocol.get("response_rules", {})

        params.validate_first        = proto_rules.get("validate_immediately", False) \
                                    or proto_rules.get("validate_first", False) \
                                    or proto_rules.get("validate_experience", False)
        params.avoid_advice          = proto_rules.get("never_give_advice", False) \
                                    or proto_rules.get("avoid_immediate_advice", False)
        params.one_step_at_a_time    = proto_rules.get("reduce_cognitive_demand", False)
        params.avoid_questions_chains = signal_result.fog_detected or signal_result.crisis_health

        # Override longueur si protocole plus restrictif
        proto_length = proto_rules.get("max_sentences") or proto_rules.get("max_length")
        if proto_length in ("very_short", "very_short_cap"):
            params.response_length      = "very_short"
            params.response_length_desc = "1-2 phrases"

        # Guidelines LLM enrichies avec le protocole
        tone_override = protocol.get("tone", "")
        if tone_override:
            params.tone_description = tone_override
            params.llm_guidelines   = (
                f"[Protocole santé actif : {protocol.get('label', '')}]\n"
                f"Ton : {tone_override}\n"
                + params.llm_guidelines
            )

    # ── Flags de session ─────────────────────────────────
    params.pain_mode = signal_result.pain_detected

    # ── Phrases interdites ───────────────────────────────
    params.forbidden_phrases = list(_FORBIDDEN_PATTERNS)
    if signal_result.protocol_id and signal_result.protocol_id in _PROTOCOLS:
        params.forbidden_phrases += _PROTOCOLS[signal_result.protocol_id].get("never_say", [])

    log_event(
        f"Interaction adaptée — santé: {health_active}, "
        f"fog: {params.fog_mode}, pain: {params.pain_mode}, "
        f"longueur: {params.response_length}"
    )

    return params


# ─────────────────────────────────────────────────────────
# Validation éthique
# ─────────────────────────────────────────────────────────

def validate_health_response(response_text: str, params: AdaptedInteractionParams) -> dict:
    """
    Vérifie qu'une réponse ne contient pas de formulations interdites
    en contexte de santé.

    Args:
        response_text : Réponse générée par ALFRED
        params        : Paramètres d'interaction actifs

    Returns:
        dict avec passed (bool) et alerts (list)
    """
    text_lower = response_text.lower()
    alerts     = []

    for phrase in params.forbidden_phrases:
        if phrase.lower() in text_lower:
            alerts.append(f"Formulation interdite en contexte santé : '{phrase}'")

    # Vérification anti-diagnostic
    diagnostic_markers = ["tu souffres de", "tu as un trouble", "diagnostic", "pathologie"]
    for marker in diagnostic_markers:
        if marker in text_lower:
            alerts.append(f"Possible diagnostic médical détecté : '{marker}'")

    return {
        "passed":  len(alerts) == 0,
        "alerts":  alerts,
    }


def get_check_in_message(frequency: str, turn_count: int) -> str | None:
    """
    Retourne un message de check-in si le moment est venu.

    Args:
        frequency  : Fréquence définie dans les paramètres
        turn_count : Nombre de tours depuis le dernier check-in

    Returns:
        Message ou None
    """
    import random

    freq_map = {
        "every_turn":    1,
        "every_2_turns": 2,
        "every_3_turns": 3,
        "every_4_turns": 4,
        "natural":       0,
    }
    threshold = freq_map.get(frequency, 3)
    if threshold == 0 or turn_count % threshold != 0:
        return None

    messages = _GLOBAL_ADAPTATIONS.get("proactivity", {}).get("check_in_templates", [
        "Comment tu tiens ?",
        "Tu veux qu'on continue ou tu préfères faire une pause ?",
        "Est-ce que le rythme te convient ?"
    ])
    return random.choice(messages)
