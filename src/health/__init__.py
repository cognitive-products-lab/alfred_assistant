# ============================================================
# ALFRED — src/health/__init__.py
# Bloc 13 — Santé & soutien émotionnel (ALFRED + ARTHUR)
#
# API publique :
#   detect_health_signals()   -> HealthSignalResult
#   adapt_for_health_context() -> AdaptedInteractionParams
#   HealthProfile             -> classe profil santé session
#   OnboardingSession         -> orchestrateur questionnaires
#   run_full_onboarding()     -> parcours complet console
# ============================================================

from src.health.chronic_support import (
    detect_health_signals,
    detect_cognitive_patterns,
    get_cognitive_pattern_adaptation,
    get_condition_adaptations,
    get_adapted_response,
    HealthSignalResult,
)
from src.health.interaction_adapter import (
    adapt_for_health_context,
    validate_health_response,
    AdaptedInteractionParams,
)
from src.health.health_profile import HealthProfile
from src.health.onboarding import (
    OnboardingSession,
    run_full_onboarding,
)
from src.health.profile_loader import (
    UserAdaptationContext,
    load_user_context,
    get_user_context,
    invalidate_cache,
    summarize_context,
)

__all__ = [
    # chronic_support
    "detect_health_signals",
    "detect_cognitive_patterns",
    "get_cognitive_pattern_adaptation",
    "get_condition_adaptations",
    "get_adapted_response",
    "HealthSignalResult",
    # interaction_adapter
    "adapt_for_health_context",
    "validate_health_response",
    "AdaptedInteractionParams",
    # health_profile
    "HealthProfile",
    # onboarding
    "OnboardingSession",
    "run_full_onboarding",
    # profile_loader
    "UserAdaptationContext",
    "load_user_context",
    "get_user_context",
    "invalidate_cache",
    "summarize_context",
]
