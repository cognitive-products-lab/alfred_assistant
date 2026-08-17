"""
PROJECT      : ALFRED
BLOCK        : B15 — Avatar & Interface
FILE         : src/ui/desktop_dashboard_data.py
ROLE         : Agrège les données réelles du pipeline pour les widgets du tableau de bord desktop

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-07-19
UPDATED      : 2026-07-19
VERSION      : V1.1
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
  - Planning du jour : components["reminder_engine"] (ReminderEngine.get_active),
    filtré par context_consent_prefs.py (toggle "Agenda du jour").
  - Appareils connectés : device_settings.py (inventaire local réel uniquement —
    pas d'appareils réseau fictifs, cf. décision du 19/07/2026).
  - Activité récente : src.memory.episodic_memory.get_timeline()
  - KPI (V1.1) : "Confiance" via ConfidenceEngine (instancié paresseusement sur
    components), "Mémoire" via ltm.get_memory_stats() (décompte réel, pas un
    pourcentage fabriqué), "Tâches" à 0 tant qu'aucun TaskEngine n'existe.
  - Notifications (V1.1) : agrégation recommandations + rappels en retard —
    aucun système de notification dédié n'existe côté backend.
"""

from __future__ import annotations

# ── Textes de justification par trigger (ProactiveSuggestion.trigger n'est
#    qu'un code court — le "Basé sur : ..." affiché par le widget est
#    reconstruit ici) ─────────────────────────────────────────────────────
TRIGGER_JUSTIFICATIONS = {
    "high_fatigue":          "Basé sur : signaux de fatigue élevés détectés dans tes derniers échanges",
    "flow_state":            "Basé sur : rythme d'échanges soutenu et concentré (état de flow détecté)",
    "emotion_stressed":      "Basé sur : ton stressé détecté dans tes derniers échanges",
    "emotion_sad":           "Basé sur : ton triste détecté dans tes derniers échanges",
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
    "nlp":     "Analyse du texte de tes derniers échanges",
    "emotion": "Ton détecté dans tes derniers échanges",
    "context": "Horaire et rythme de la journée",
    "memory":  "Cohérence avec ton historique récent",
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
            "why": TRIGGER_JUSTIFICATIONS.get(s.trigger, "Basé sur ton contexte actuel"),
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
            "mood_label": f"{override['manual_mood']} — corrigé par toi",
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
    from src.ui.context_consent_prefs import load_context_consent

    if not load_context_consent()["agenda"]:
        return []

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


# ============================================================
# KPI grid
# ============================================================
# "État du système" et "Confiance" ont un vrai signal ; "Mémoire" est
# remplacé par un décompte réel (pas de notion de "%" qui existerait déjà
# côté backend) ; "Tâches" reste à 0 tant qu'aucun TaskEngine n'existe
# (backlog séparé) — pas de nombre fabriqué à la place.

CONFIDENCE_FR = {"high": "Élevée", "medium": "Moyenne", "low": "Faible"}


def get_kpis() -> dict:
    from src.main import get_live_components

    components = get_live_components()
    if components is None:
        return {
            "system_status": "Hors ligne",
            "memory_count": None,
            "task_count": 0,
            "confidence_label": None,
        }

    system_status = "Opérationnel" if components.get("llm") is not None else "Dégradé"

    memory_count = None
    ltm = components.get("ltm")
    if ltm and components.get("ltm_ok"):
        try:
            memory_count = ltm.get_memory_stats().get("memories_active")
        except Exception:
            pass

    confidence_label = None
    fused = components.get("_last_fused")
    if fused is not None:
        try:
            from src.v3.fusion.confidence_engine import ConfidenceEngine

            engine = components.get("confidence_engine")
            if engine is None:
                engine = ConfidenceEngine()
                components["confidence_engine"] = engine
            decision = engine.evaluate(fused)
            confidence_label = CONFIDENCE_FR.get(decision.level, decision.level)
        except Exception:
            pass

    return {
        "system_status": system_status,
        "memory_count": memory_count,
        "task_count": 0,  # TaskEngine pas encore implémenté
        "confidence_label": confidence_label,
    }


# ============================================================
# Notifications — agrège recommandations + rappels du jour,
# aucun système de notification distinct n'existe côté backend.
# ============================================================

def get_notifications(limit: int = 8) -> list[dict]:
    items = []

    for reco in get_recommandations(limit=5):
        items.append({
            "kind": "recommandation",
            "text": reco["content"],
            "timestamp": reco["timestamp"],
        })

    for plan in get_planning():
        if plan["overdue"]:
            items.append({
                "kind": "rappel",
                "text": f"Rappel en retard : {plan['title']}",
                "timestamp": plan["due_at"],
            })

    items.sort(key=lambda n: n["timestamp"], reverse=True)
    return items[:limit]


# ============================================================
# Vue Mémoire — agrégats uniquement, jamais le contenu brut
# des échanges sans double authentification (contrainte actée
# le 24/07/2026). Voir src/ui/memoire_lock.py pour le gate PIN.
# ============================================================

# État de déverrouillage — process-local, remis à False à chaque
# redémarrage de l'app (cohérent avec "double authentification" : se
# reperd volontairement, ce n'est pas un souvenir persistant du choix).
_memoire_unlocked = False


def is_memoire_unlocked() -> bool:
    return _memoire_unlocked


def unlock_memoire(pin: str) -> dict:
    """
    Deuxième authentification (en plus du login déjà fait au démarrage de
    l'app) avant d'exposer le contenu brut des échanges dans la Vue
    Mémoire. Réutilise le même PIN bcrypt + rate-limiter que le login
    principal (src.auth.authenticator) — pas un second secret à gérer.
    """
    global _memoire_unlocked
    from src.auth.authenticator import authenticate

    result = authenticate("celine", pin)
    if result.get("success"):
        _memoire_unlocked = True
    return {"success": bool(result.get("success")), "reason": result.get("reason", "")}


def lock_memoire() -> dict:
    global _memoire_unlocked
    _memoire_unlocked = False
    return {"locked": True}


CATEGORY_FR = {
    "project":  "Projet",
    "emotion":  "Émotionnel",
    "learning": "Apprentissage",
    "decision": "Décision",
    "daily":    "Quotidien",
    "general":  "Général",
}

_USER_INSTANCE_PATH = "data/users/instances/user_celine_instance.json"


def _get_since_date() -> str | None:
    """Date de création du profil utilisateur — sert d'ancrage 'depuis quand'."""
    import json
    from pathlib import Path

    path = Path(__file__).resolve().parents[2] / _USER_INSTANCE_PATH
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return data.get("user_profile", {}).get("created_at")
    except Exception:
        return None


def get_memoire_summary() -> dict:
    """
    Agrégats mémoire uniquement (nombres, jamais de contenu) — vue par
    défaut de la Vue Mémoire, visible sans authentification.
    """
    from src.memory import episodic_memory
    from src.memory import long_term_memory as ltm_module
    from src.main import get_live_components

    summary = {
        "total_exchanges":   None,
        "memories_active":   None,
        "facts":             None,
        "patterns":          None,
        "total_episodes":    0,
        "categories":        {},
        "since":             _get_since_date(),
        "ltm_available":     False,
    }

    components = get_live_components()
    if components is not None:
        memory = components.get("memory")
        if memory is not None:
            try:
                summary["total_exchanges"] = memory.stats().get("total_exchanges")
            except Exception:
                pass

        ltm = components.get("ltm")
        if ltm is not None and components.get("ltm_ok"):
            try:
                stats = ltm_module.get_memory_stats()
                summary["memories_active"] = stats.get("memories_active")
                summary["facts"] = stats.get("facts")
                summary["patterns"] = stats.get("patterns")
                summary["ltm_available"] = True
            except Exception:
                pass

    try:
        ep_stats = episodic_memory.get_episode_stats()
        summary["total_episodes"] = ep_stats.get("total_episodes", 0)
        summary["categories"] = {
            CATEGORY_FR.get(cat, cat): count
            for cat, count in ep_stats.get("categories", {}).items()
        }
    except Exception:
        pass

    return summary


def get_memoire_moments(limit: int = 8) -> list[dict]:
    """
    Frise "moments marquants" — titre, catégorie, émotion, date UNIQUEMENT.
    Jamais `description` (contenu brut de l'échange) : réservé à la vue
    déverrouillée par PIN (src/ui/memoire_lock.py).
    """
    from src.memory.episodic_memory import get_important_episodes

    episodes = get_important_episodes(threshold=0.6, limit=limit)
    return [
        {
            "id":         ep.get("id"),
            "title":      ep.get("title"),
            "category":   CATEGORY_FR.get(ep.get("category", "general"), ep.get("category")),
            "emotion":    EMOTION_FR.get(ep.get("emotion", "neutral"), ep.get("emotion")),
            "importance": ep.get("importance"),
            "date":       ep.get("created_at"),
        }
        for ep in episodes
    ]


def get_memoire_moment_detail(episode_id: str) -> dict | None:
    """
    Détail complet d'un épisode (description brute incluse) — nécessite
    un déverrouillage préalable via unlock_memoire(pin) ci-dessous.
    Retourne {"error": "locked"} tant que ce n'est pas fait.
    """
    if not _memoire_unlocked:
        return {"error": "locked"}

    from src.memory.episodic_memory import get_episode_by_id

    ep = get_episode_by_id(episode_id)
    if ep is None:
        return None
    return {
        "id":          ep.get("id"),
        "title":       ep.get("title"),
        "description": ep.get("description"),
        "category":    CATEGORY_FR.get(ep.get("category", "general"), ep.get("category")),
        "emotion":     EMOTION_FR.get(ep.get("emotion", "neutral"), ep.get("emotion")),
        "importance":  ep.get("importance"),
        "date":        ep.get("created_at"),
        "tags":        ep.get("tags", []),
    }
