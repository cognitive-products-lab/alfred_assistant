"""
PROJECT      : ALFRED
BLOCK        : B13
FUNCTION     : SMOKE
FILE         : tests/b13_tests/test_smoke_health_batch1.py
ROLE         : Smoke tests (lot 1) pour les 5 modules src/health/ sans
               couverture de test existante.

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-07-05
UPDATED      : 2026-07-05
VERSION      : V1.0
STATUS       : TESTED

DESCRIPTION :
Verifie import + comportement de base des modules de gestion santé/fragilité
(chronic_support, health_profile, interaction_adapter, profile_loader,
onboarding). Utilise des identifiants utilisateur synthétiques inexistants
pour ne pas dépendre de vraies données ni en créer sans nettoyage.
"""

import pytest

from src.health import chronic_support
from src.health.health_profile import HealthProfile
from src.health import interaction_adapter
from src.health import profile_loader
from src.health import onboarding


# ── chronic_support.py ───────────────────────────────────────

def test_detect_health_signals_fog():
    result = chronic_support.detect_health_signals("j'ai un gros brouillard cognitif aujourd'hui")
    assert result.detected is True
    assert result.fog_detected is True


def test_detect_health_signals_crisis():
    result = chronic_support.detect_health_signals("je suis en poussée sévère, je ne peux pas me lever")
    assert result.detected is True
    assert result.flare_detected is True or result.crisis_health is True


def test_detect_health_signals_no_signal():
    result = chronic_support.detect_health_signals("il fait beau aujourd'hui, tout va bien")
    assert result.detected is False


def test_detect_cognitive_patterns_returns_list():
    patterns = chronic_support.detect_cognitive_patterns("je rumine sans arrêt sur cette erreur")
    assert isinstance(patterns, list)


def test_get_condition_adaptations_known_condition():
    adaptations = chronic_support.get_condition_adaptations(["fibromyalgie"])
    assert "response_length" in adaptations
    assert "forbidden_phrases" in adaptations


def test_get_condition_adaptations_empty_list():
    assert chronic_support.get_condition_adaptations([]) == {}


def test_get_condition_profile_known_and_unknown():
    profile = chronic_support.get_condition_profile("fibromyalgie")
    assert isinstance(profile, dict) and profile
    assert chronic_support.get_condition_profile("condition_inexistante_xyz") == {}


# ── health_profile.py ────────────────────────────────────────

def test_health_profile_defaults_for_unknown_user():
    profile = HealthProfile(user_id="test_ci_nonexistent_user_9999")
    assert profile.is_active is False
    assert profile.conditions == []
    assert profile.severity == "mild"


def test_health_profile_session_state_transitions():
    profile = HealthProfile(user_id="test_ci_nonexistent_user_9999")
    profile.activate_fog_mode()
    assert profile.session.fog_mode_active is True
    profile.deactivate_fog_mode()
    assert profile.session.fog_mode_active is False

    profile.activate_flare()
    assert profile.session.flare_detected is True
    assert profile.severity == "severe"

    profile.increment_turn()
    assert profile.session.turn_count == 1
    profile.reset_session()
    assert profile.session.turn_count == 0


def test_health_profile_create_from_template_requires_consent():
    with pytest.raises(ValueError):
        HealthProfile.create_from_template(
            user_id="test_ci_nonexistent_user_9999", consent=False
        )


def test_health_profile_repr_contains_user_id():
    profile = HealthProfile(user_id="test_ci_nonexistent_user_9999")
    assert "test_ci_nonexistent_user_9999" in repr(profile)


# ── interaction_adapter.py ───────────────────────────────────

def test_adapt_for_health_context_inactive_when_no_signal():
    profile = HealthProfile(user_id="test_ci_nonexistent_user_9999")
    signal = chronic_support.detect_health_signals("il fait beau aujourd'hui")
    params = interaction_adapter.adapt_for_health_context(signal, profile)
    assert params.health_active is False


def test_adapt_for_health_context_active_on_fog_signal():
    profile = HealthProfile(user_id="test_ci_nonexistent_user_9999")
    signal = chronic_support.detect_health_signals("gros brouillard cognitif, fibro fog")
    params = interaction_adapter.adapt_for_health_context(signal, profile)
    assert params.health_active is True
    assert params.fog_mode is True


def test_validate_health_response_detects_forbidden_phrase():
    params = interaction_adapter.AdaptedInteractionParams(forbidden_phrases=["fais un effort"])
    result = interaction_adapter.validate_health_response("Allez, fais un effort !", params)
    assert result["passed"] is False
    assert result["alerts"]


def test_validate_health_response_detects_diagnostic_marker():
    params = interaction_adapter.AdaptedInteractionParams()
    result = interaction_adapter.validate_health_response("Tu as un trouble anxieux.", params)
    assert result["passed"] is False


def test_validate_health_response_clean_text_passes():
    params = interaction_adapter.AdaptedInteractionParams()
    result = interaction_adapter.validate_health_response("Comment puis-je t'aider aujourd'hui ?", params)
    assert result["passed"] is True
    assert result["alerts"] == []


def test_get_check_in_message_threshold_logic():
    assert interaction_adapter.get_check_in_message("every_2_turns", 1) is None
    msg = interaction_adapter.get_check_in_message("every_2_turns", 2)
    assert msg is None or isinstance(msg, str)


# ── profile_loader.py ────────────────────────────────────────

def test_load_user_context_defaults_for_unknown_user():
    ctx = profile_loader.load_user_context("test_ci_nonexistent_user_9999")
    assert ctx.profile_complete is False
    assert ctx.profiles_loaded == []
    assert ctx.mbti_type == ""


def test_get_user_context_cache_and_invalidate():
    profile_loader.invalidate_cache("test_ci_nonexistent_user_9999")
    ctx1 = profile_loader.get_user_context("test_ci_nonexistent_user_9999")
    ctx2 = profile_loader.get_user_context("test_ci_nonexistent_user_9999")
    assert ctx1 is ctx2  # même instance depuis le cache

    ctx3 = profile_loader.get_user_context("test_ci_nonexistent_user_9999", force_reload=True)
    assert ctx3 is not ctx1
    profile_loader.invalidate_cache("test_ci_nonexistent_user_9999")


def test_summarize_context_returns_readable_string():
    ctx = profile_loader.load_user_context("test_ci_nonexistent_user_9999")
    summary = profile_loader.summarize_context(ctx)
    assert isinstance(summary, str)
    assert "test_ci_nonexistent_user_9999" in summary


# ── onboarding.py (fonctions pures uniquement) ───────────────

def test_set_and_get_nested_helpers():
    d = {}
    onboarding._set_nested(d, "a.b.c", 42)
    assert d == {"a": {"b": {"c": 42}}}
    assert onboarding._get_nested(d, "a.b.c") == 42
    assert onboarding._get_nested(d, "a.b.missing", "default") == "default"


def test_compute_mbti_basic():
    scoring_config = {
        "mbti_compute": {
            "EI": {
                "fields": ["q1", "q2"],
                "interpretation": {"range": [1, 3], "result": "I"},
                "interpretation_2": {"range": [4, 5], "result": "E"},
                "neutral_result": "X",
            }
        }
    }
    answers = {"q1": 1, "q2": 2}
    result = onboarding._compute_mbti(answers, scoring_config)
    assert result["EI"]["letter"] == "I"
    assert result["full_type"] == "I"


def test_apply_personality_matrix():
    mbti = {"EI": {"letter": "I"}, "full_type": "I"}
    matrix = {"EI": {"I": {"initiate_conversation": False}, "E": {"initiate_conversation": True}}}
    adaptations = onboarding._apply_personality_matrix(mbti, matrix)
    assert adaptations == {"initiate_conversation": False}


def test_onboarding_session_get_communication_params_defaults():
    session = onboarding.OnboardingSession(user_id="test_ci_nonexistent_user_9999")
    params = session.get_communication_params()
    assert isinstance(params, dict)


def test_onboarding_load_profile_returns_empty_for_unknown_user():
    assert onboarding.OnboardingSession.load_personality_profile("test_ci_nonexistent_user_9999") == {}
    assert onboarding.OnboardingSession.load_emotional_profile("test_ci_nonexistent_user_9999") == {}
