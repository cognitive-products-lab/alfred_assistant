"""
PROJECT      : ALFRED
BLOCK        : 03 / 13
FUNCTION     : 13.05 — Adaptation interaction / Chargement profils
FILE         : src/health/profile_loader.py
ROLE         : Pont entre les profils d'onboarding et les paramètres live du moteur de régulation

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-05-26
VERSION      : V1.0
STATUS       : TESTED

DESCRIPTION :
Charge les profils utilisateur (santé, personnalité, émotionnel) depuis data/profile/ et data/health/,
et produit un `UserAdaptationContext` exploitable par regulation_engine et personality_adapter.

Usage :
    from src.health.profile_loader import UserAdaptationContext, load_user_context
    ctx = load_user_context("user_001")
    ctx.mbti_type          # "INFJ"
    ctx.validate_first     # True
    ctx.humor_enabled      # False
    ctx.topics_avoid       # ["death_grief", "finances"]
"""

import json
from dataclasses import dataclass, field
from pathlib import Path

try:
    from paths import DATA_HEALTH, DATA_PROFILE
except ImportError:
    _base       = Path(__file__).resolve().parent.parent.parent
    DATA_HEALTH  = _base / "data" / "health"
    DATA_PROFILE = _base / "data" / "profile"


# ── Chargement fichiers ────────────────────────────────────────────────────────

def _load_json(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}


# ── Contexte d'adaptation utilisateur ─────────────────────────────────────────

@dataclass
class UserAdaptationContext:
    """
    Contexte complet d'adaptation personnalisée pour un utilisateur.
    Produit à partir des trois profils d'onboarding.
    Consommé par personality_adapter et regulation_engine.
    """
    user_id: str

    # ── MBTI & style cognitif ──────────────────────────────
    mbti_type:          str  = ""        # ex: "INFJ", "ESTP", "INFX"
    mbti_EI:            str  = "X"       # E / I / X
    mbti_SN:            str  = "X"       # S / N / X
    mbti_TF:            str  = "X"       # T / F / X
    mbti_JP:            str  = "X"       # J / P / X

    # ── Adaptations MBTI calculées ─────────────────────────
    proactivity_boost:  float = 0.0      # +/- delta sur proactivité
    initiate_conv:      bool  = False    # initier la conv ou attendre
    concrete_first:     bool  = False    # S → exemples concrets avant
    conceptual_first:   bool  = False    # N → vision globale avant
    validate_first:     bool  = True     # F → valider avant résoudre
    direct_feedback:    bool  = False    # T → feedback direct
    structured_resp:    bool  = False    # J → réponses structurées
    flexible_tone:      bool  = True     # P → ton flexible

    # ── Communication ─────────────────────────────────────
    formality_level:    int   = 2        # 1–5 (1=très familier, 5=formel)
    humor_enabled:      bool  = True
    challenge_pref:     str   = "ask_question"   # never/suggest/ask/direct
    validation_style:   str   = "validate_first"
    proactivity_pref:   str   = "moderately_proactive"
    decision_support:   str   = "pros_cons"
    processing_pref:    str   = "adapt"  # fast_scan / deep / interactive / adapt

    # ── Santé & fragilité ─────────────────────────────────
    health_active:      bool  = False
    conditions:         list[str] = field(default_factory=list)
    severity_level:     int   = 0        # 0–5
    fog_auto_activate:  bool  = True
    check_in_freq:      str   = "session_start"
    response_length_pref: str = "adapt"
    is_caregiver:       bool  = False

    # ── Profil émotionnel ──────────────────────────────────
    dominant_emotions:  list[str] = field(default_factory=list)
    stress_triggers:    list[str] = field(default_factory=list)
    rumination_tendency: str = "sometimes"  # never/sometimes/often/very_often
    overwhelm_pattern:  str  = "freeze"
    regulation_strategies: list[str] = field(default_factory=list)
    emotion_awareness:  int  = 3         # 1–5

    # ── Rôle ALFRED ───────────────────────────────────────
    alfred_emotional_roles:  list[str] = field(default_factory=list)
    when_distressed:    str   = "ask_once"
    crisis_pref:        str   = "resources_if_severe"
    post_crisis:        str   = "follow_my_lead"

    # ── Frontières ────────────────────────────────────────
    topics_avoid:       list[str] = field(default_factory=list)
    behaviors_avoid:    list[str] = field(default_factory=list)

    # ── Motivations & valeurs ─────────────────────────────
    primary_motivation: str   = ""
    alfred_roles:       list[str] = field(default_factory=list)

    # ── Meta ──────────────────────────────────────────────
    profile_complete:   bool  = False    # True si au moins 1 profil chargé
    profiles_loaded:    list[str] = field(default_factory=list)


# ── Chargeur principal ────────────────────────────────────────────────────────

def load_user_context(user_id: str) -> UserAdaptationContext:
    """
    Charge et fusionne les trois profils utilisateur en un UserAdaptationContext.

    Args:
        user_id : Identifiant unique de l'utilisateur

    Returns:
        UserAdaptationContext peuplé — champs par défaut si profil absent
    """
    ctx = UserAdaptationContext(user_id=user_id)

    health_data  = _load_json(DATA_HEALTH  / f"health_{user_id}.json")
    pers_data    = _load_json(DATA_PROFILE / f"personality_{user_id}.json")
    emo_data     = _load_json(DATA_PROFILE / f"emotional_{user_id}.json")

    if health_data:
        _apply_health(ctx, health_data)
        ctx.profiles_loaded.append("health")

    if pers_data:
        _apply_personality(ctx, pers_data)
        ctx.profiles_loaded.append("personality")

    if emo_data:
        _apply_emotional(ctx, emo_data)
        ctx.profiles_loaded.append("emotional")

    ctx.profile_complete = bool(ctx.profiles_loaded)
    return ctx


# ── Application profil santé ──────────────────────────────────────────────────

def _apply_health(ctx: UserAdaptationContext, data: dict) -> None:
    meta = data.get("metadata", {})
    ctx.health_active = (
        meta.get("consent_given", False)
        and data.get("alfred_adaptations_active", False)
    )

    conditions = data.get("conditions", {})
    ctx.conditions = (
        conditions.get("primary", [])
        + conditions.get("secondary", [])
        + conditions.get("self_declared", [])
    )

    status = data.get("profile_status", {})
    ctx.severity_level = int(status.get("severity_level", 0))

    prefs = data.get("interaction_preferences", {})
    ctx.fog_auto_activate   = prefs.get("fog_mode_auto_activate", True)
    ctx.check_in_freq       = prefs.get("check_in_frequency", "session_start")
    ctx.response_length_pref = prefs.get("response_length_preference", "adapt")

    caregiver = data.get("caregiver_mode", {})
    ctx.is_caregiver = caregiver.get("is_caregiver", False)


# ── Application profil personnalité ──────────────────────────────────────────

def _apply_personality(ctx: UserAdaptationContext, data: dict) -> None:
    mbti = data.get("mbti", {})

    ctx.mbti_EI   = mbti.get("EI", {}).get("letter", "X")
    ctx.mbti_SN   = mbti.get("SN", {}).get("letter", "X")
    ctx.mbti_TF   = mbti.get("TF", {}).get("letter", "X")
    ctx.mbti_JP   = mbti.get("JP", {}).get("letter", "X")
    ctx.mbti_type = mbti.get("full_type", "")

    # Adaptations MBTI calculées
    adaptations = data.get("alfred_adaptations", {})
    ctx.proactivity_boost = float(adaptations.get("proactivity", "+0.0").replace("+", "")) if isinstance(adaptations.get("proactivity"), str) else 0.0
    ctx.initiate_conv    = adaptations.get("initiate_conversation", False)
    ctx.concrete_first   = adaptations.get("concrete_examples", False)
    ctx.conceptual_first = adaptations.get("conceptual_first", False)
    ctx.validate_first   = adaptations.get("validate_then_solve", True)
    ctx.direct_feedback  = adaptations.get("direct_feedback", False)
    ctx.structured_resp  = adaptations.get("structured_responses", False)
    ctx.flexible_tone    = adaptations.get("flexible_tone", True)

    comm = data.get("communication", {})
    ctx.formality_level  = int(comm.get("formality_level", 2))
    ctx.humor_enabled    = comm.get("humor_preference", "light") not in ("none",)
    ctx.validation_style = comm.get("validation_style", "validate_first")
    ctx.proactivity_pref = comm.get("proactivity_preference", "moderately_proactive")
    ctx.challenge_pref   = comm.get("challenge_preference", "ask_question")

    cog = data.get("cognitive_style", {})
    ctx.processing_pref  = cog.get("processing_speed", "adapt")
    ctx.decision_support = cog.get("decision_support_preference", "pros_cons")

    values = data.get("values", {})
    ctx.primary_motivation = values.get("primary_motivation", "")
    ctx.alfred_roles       = values.get("alfred_role", [])


# ── Application profil émotionnel ─────────────────────────────────────────────

def _apply_emotional(ctx: UserAdaptationContext, data: dict) -> None:
    baseline = data.get("emotional_baseline", {})
    ctx.dominant_emotions = baseline.get("dominant_emotions", [])
    ctx.stress_triggers   = baseline.get("stress_triggers", [])

    regulation = data.get("regulation", {})
    ctx.rumination_tendency    = regulation.get("rumination_tendency", "sometimes")
    ctx.overwhelm_pattern      = regulation.get("overwhelm_pattern", "freeze")
    ctx.regulation_strategies  = regulation.get("preferred_strategies", [])
    ctx.emotion_awareness      = int(regulation.get("emotion_awareness_level", 3))

    alfred_role = data.get("alfred_role", {})
    ctx.alfred_emotional_roles = alfred_role.get("emotional_functions", [])
    ctx.when_distressed        = alfred_role.get("when_distressed", "ask_once")
    ctx.crisis_pref            = alfred_role.get("crisis_response_preference", "resources_if_severe")
    ctx.post_crisis            = alfred_role.get("post_crisis_follow_up", "follow_my_lead")

    boundaries = data.get("boundaries", {})
    ctx.topics_avoid    = boundaries.get("sensitive_topics_avoid", [])
    ctx.behaviors_avoid = boundaries.get("behaviors_to_avoid", [])


# ── Serialisation résumé lisible ──────────────────────────────────────────────

def summarize_context(ctx: UserAdaptationContext) -> str:
    """Produit un résumé court du contexte pour les logs ou le debug."""
    lines = [
        f"UserAdaptationContext [{ctx.user_id}]",
        f"  Profils chargés : {', '.join(ctx.profiles_loaded) or 'aucun'}",
        f"  MBTI            : {ctx.mbti_type or '?'}  (E/I={ctx.mbti_EI}, S/N={ctx.mbti_SN}, T/F={ctx.mbti_TF}, J/P={ctx.mbti_JP})",
        f"  Santé active    : {ctx.health_active} | Conditions : {', '.join(ctx.conditions) or 'aucune'}",
        f"  Sévérité        : {ctx.severity_level}/5 | Fog auto : {ctx.fog_auto_activate}",
        f"  Valider d'abord : {ctx.validate_first} | Humour    : {ctx.humor_enabled}",
        f"  Formalité       : {ctx.formality_level}/5 | Défi     : {ctx.challenge_pref}",
        f"  Rumination      : {ctx.rumination_tendency} | Débordement : {ctx.overwhelm_pattern}",
        f"  Sujets évités   : {', '.join(ctx.topics_avoid) or 'aucun'}",
    ]
    return "\n".join(lines)


# ── Cache session (singleton par user_id) ────────────────────────────────────

_context_cache: dict[str, UserAdaptationContext] = {}


def get_user_context(user_id: str, force_reload: bool = False) -> UserAdaptationContext:
    """
    Retourne le contexte utilisateur depuis le cache ou le charge si absent.

    Args:
        user_id      : Identifiant utilisateur
        force_reload : Recharge depuis les fichiers même si en cache

    Returns:
        UserAdaptationContext (mis en cache)
    """
    if user_id not in _context_cache or force_reload:
        _context_cache[user_id] = load_user_context(user_id)
    return _context_cache[user_id]


def invalidate_cache(user_id: str) -> None:
    """Invalide le cache d'un utilisateur (à appeler après mise à jour du profil)."""
    _context_cache.pop(user_id, None)
