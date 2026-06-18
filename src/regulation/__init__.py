# ============================================================
# ALFRED — src/regulation/__init__.py
# Bloc 03 / 13 — Régulation émotionnelle, modes de protection, santé
#
# API publique du module :
#   process_message()         -> pipeline complet en une ligne
#   get_regulation_engine()   -> instance singleton
#   PipelineContext           -> dataclass résultat du pipeline
#   UserAdaptationContext     -> profil onboarding utilisateur
#   get_user_context()        -> charge/cache le profil utilisateur
# ============================================================

from src.regulation.regulation_engine import (
    process_message,
    get_regulation_engine,
    PipelineContext,
)
from src.regulation.emotion_detector import detect_emotion, EmotionalState
from src.regulation.mode_manager     import get_mode_manager
from src.regulation.protection_guard import is_crisis, get_crisis_response
from src.health.profile_loader import (
    UserAdaptationContext,
    load_user_context,
    get_user_context,
    invalidate_cache as invalidate_user_cache,
)

__all__ = [
    # Pipeline principal
    "process_message",
    "get_regulation_engine",
    "PipelineContext",
    # Émotion
    "detect_emotion",
    "EmotionalState",
    # Mode
    "get_mode_manager",
    # Protection
    "is_crisis",
    "get_crisis_response",
    # Profil utilisateur (onboarding)
    "UserAdaptationContext",
    "load_user_context",
    "get_user_context",
    "invalidate_user_cache",
]
