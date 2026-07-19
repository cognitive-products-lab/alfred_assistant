"""
PROJECT      : ALFRED
BLOCK        : B15 — Avatar & Interface
FILE         : src/ui/desktop_dashboard_data.py
ROLE         : Agrège les données réelles du pipeline pour les widgets du tableau de bord desktop

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-07-19
VERSION      : V1.0
STATUS       : DRAFT

DESCRIPTION :
src/alfred_desktop.py::AlfredDesktopAPI reste un simple relais JS-facing ;
la logique de mise en forme (libellés français, justification des
recommandations, repli sur l'override émotionnel) vit ici, dans un module
pur sans dépendance pywebview — même séparation que desktop_prefs.py /
device_settings.py.

Sources réelles utilisées (aucune donnée fabriquée) :
  - Recommandations : components["proactive_engine"] (ProactiveEngine.get_history)
  - État émotionnel : components["_last_fused"] (MultiSignalFusionEngine) +
    wellbeing_tracker.get_daily_energy_summary(), avec repli sur
    emotion_override_prefs si l'utilisateur a désactivé/corrigé l'estimation.
  - Planning du jour : components["reminder_engine"] (ReminderEngine.get_active)
  - Appareils connectés : device_settings.py (inventaire local réel uniquement —
    pas d'appareils réseau fictifs, cf. décision du 19/07/2026).
  - Activité récente : src.memory.episodic_memory.get_timeline()
"""

from __future__ import annotations

# ── Textes de justification par trigger (ProactiveSuggestion.trigger n'est
#    qu'un code court — le "Basé sur : ..." affiché par le widget est
#    reconstruit ici) ─────────────────────────────────────────────────────
TRIGGER_JUSTIFICATIONS = {
    "high_fatigue":          "Basé sur : signaux de fatigue élevés détectés dans vos derniers échanges",
    "flow_state":            "Basé sur : rythme d'échanges soutenu et concentré (état de flow détecté)",
    "emotion_stressed":      "Basé sur : ton stressé détecté dans vos derniers échanges",
    "emotion_sad":           "Basé sur : ton triste détecté dans vos derniers échanges",
    "late_night_low_energy": "Basé sur : horaire tardif et niveau d'énergie bas",
    "forced":                "Suggestion déclenchée manuellement",
}

EMOTION_FR = {
    "neutral":   "Neutre",
    "happy":     "Content(e)",
    "sad":       "Triste",
    "stressed":  "Stressé(e)",
    "tired":     "Fatigué(e)",
    "motivated": "Motivé(e)",
    "calm":      "Calme",
    "focused":   "Concentré(e)",
}

SOURCE_FR = {
    "nlp":     "Analyse du texte de vos derniers échanges",
    "emotion": "Ton détecté dans vos derniers échanges",
    "context": "Horaire et rythme de la journée",
    "memory":  "Cohérence avec votre historique récent",
}


# ============================================================
# Recommandations
# ============================================================

def get_recommandations(limit: int = 5) -> list[dict]:
    from src.main import get_live_components

    components = get_live_components()
    engine = components.get("proactive_engine") if components else None
    if not engine:
        return []

    suggestions = engine.get_history(limit)
    return [
        {
            "content": s.content,
            "category": s.category,
            "priority": s.priority,
            "can_dismiss": s.can_dismiss,
            "trigger": s.trigger,
            "why": TRIGGER_JUSTIFICATIONS.get(s.trigger, "Basé sur votre contexte actuel"),
            "timestamp": s.timestamp,
        }
        for s in reversed(suggestions)  # plus récent en premier
    ]


# ============================================================
# État émotionnel
# ============================================================

def get_emotion_state() -> dict:
    from src.ui.emotion_override_prefs import load_emotion_override

    override = load_emotion_override()

    if not override["enabled"]:
        return {"enabled": False}

    if override.get("manual_mood"):
        return {
            "enabled": True,
            "manual": True,
            "mood_label": f"{override['manual_mood']} — corrigé par vous",
            "corrected_at": override.get("manual_set_at"),
        }

    from src.main import get_live_components

    components = get_live_components()
    fused = components.get("_last_fused") if components else None

    if fused is None:
        return {"enabled": True, "manual": False, "no_data": True}

    try:
        from src.regulation.wellbeing_tracker import get_daily_energy_summary
        energy = get_daily_energy_summary()
        energy_dominant = energy.get("dominant")
    except Exception:
        energy_dominant = None

    mood_label = EMOTION_FR.get(fused.dominant_emotion, fused.dominant_emotion.capitalize())
    confidence_pct = round(fused.confidence * 100)
    sources = [SOURCE_FR.get(s, s) for s in fused.sources_used]

    return {
        "enabled": True,
        "manual": False,
        "no_data": False,
        "mood_label": mood_label,
        "confidence_pct": confidence_pct,
        "bar_pct": confidence_pct,
        "sources": sources,
        "energy_dominant": energy_dominant,
    }


def set_emotion_override(enabled: bool) -> dict:
    from src.ui.emotion_override_prefs import save_emotion_override, clear_manual_mood

    save_emotion_override(enabled=enabled)
    if enabled:
        # Réactiver l'estimation efface une éventuelle correction manuelle
        # précédente : on repart sur le signal live, pas sur le dernier mood
        # corrigé avant la désactivation.
        clear_manual_mood()
    return get_emotion_state()


def correct_emotion(mood_label: str) -> dict:
    from src.ui.emotion_override_prefs import save_emotion_override

    save_emotion_override(manual_mood=mood_label)
    return get_emotion_state()


# ============================================================
# Planning du jour
# ============================================================

def get_planning() -> list[dict]:
    from src.main import get_live_components

    components = get_live_components()
    engine = components.get("reminder_engine") if components else None

    if not engine:
        # ReminderEngine n'a pas d'état de session — une instance fraîche lit
        # le même data/memory/reminders.json en toute sécurité si le pipeline
        # n'est pas encore démarré.
        from src.v3.proactive.reminder_engine import ReminderEngine
        engine = ReminderEngine()

    reminders = sorted(engine.get_active(), key=lambda r: r.due_at)
    return [
        {
            "id": r.id,
            "title": r.title,
            "due_at": r.due_at,
            "recurrent": r.recurrent,
            "overdue": r.is_due(),
        }
        for r in reminders
    ]


# ============================================================
# Appareils connectés (inventaire local réel uniquement)
# ============================================================

def get_devices() -> dict:
    from src.ui.device_settings import (
        get_cached_cameras,
        get_cached_audio_inputs,
        get_cached_audio_outputs,
        load_device_settings,
    )

    cameras = get_cached_cameras()
    audio_inputs = get_cached_audio_inputs()
    audio_outputs = get_cached_audio_outputs()
    active = load_device_settings()

    return {
        "cameras": cameras,
        "audio_inputs": audio_inputs,
        "audio_outputs": audio_outputs,
        "active": active,
    }


# ============================================================
# Activité récente
# ============================================================

def get_activite(limit: int = 10) -> list[dict]:
    from src.memory.episodic_memory import get_timeline

    return get_timeline(limit=limit)
