# ============================================================
# ALFRED — src/memory/episodic_memory.py
# Bloc 02.03 — Historique utilisateur
#
# 📚 NOTION EXAM :
#   D21-3 — Capsule 2 : Mémoire épisodique et événements marquants
#
# 🎯 UTILITÉ ALFRED :
#   Enregistre les épisodes notables (percées, blocages, émotions fortes)
#   avec timeline chronologique et liens contextuels cause/effet.
#
# 🏗️ DOMAINE :
#   Mémoire & contexte — épisodique, différent de la mémoire ordinaire
# ============================================================

import json
from datetime import datetime
from pathlib import Path
from typing import Any

from src.security.security_logger import log_event

# ── Stockage JSON (local-first) ───────────────────────────
_EPISODE_FILE = Path("data/memory/episodes.json")
_EPISODE_FILE.parent.mkdir(parents=True, exist_ok=True)


# ─────────────────────────────────────────────────────────
# Structure épisode
# ─────────────────────────────────────────────────────────

def _empty_episode(
    title: str,
    description: str,
    category: str,
    emotion: str,
    importance: float,
    tags: list[str],
) -> dict:
    return {
        "id":           f"ep_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        "created_at":   datetime.now().isoformat(),
        "title":        title,
        "description":  description,
        "category":     category,      # project / emotion / learning / decision / daily
        "emotion":      emotion,       # émotion dominante au moment
        "importance":   importance,    # 0.0 → 1.0
        "tags":         tags,
        "linked_to":    [],            # IDs d'épisodes liés
    }


# ─────────────────────────────────────────────────────────
# Lecture / écriture JSON
# ─────────────────────────────────────────────────────────

def _load_episodes() -> list[dict]:
    if not _EPISODE_FILE.exists():
        return []
    try:
        return json.loads(_EPISODE_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, Exception) as e:
        log_event(f"Erreur lecture épisodes : {e}", "ERROR")
        return []


def _save_episodes(episodes: list[dict]) -> None:
    try:
        _EPISODE_FILE.write_text(
            json.dumps(episodes, indent=2, ensure_ascii=False),
            encoding="utf-8"
        )
    except Exception as e:
        log_event(f"Erreur sauvegarde épisodes : {e}", "ERROR")


# ─────────────────────────────────────────────────────────
# API publique
# ─────────────────────────────────────────────────────────

def record_episode(
    title: str,
    description: str,
    category: str = "general",
    emotion: str = "neutral",
    importance: float = 0.5,
    tags: list[str] | None = None,
) -> str:
    """
    Enregistre un épisode notable dans la mémoire épisodique.

    Args:
        title       : Titre court de l'épisode
        description : Description détaillée
        category    : project / emotion / learning / decision / daily
        emotion     : Émotion dominante (stressed / happy / motivated / etc.)
        importance  : Score 0.0 (anecdote) → 1.0 (moment clé)
        tags        : Mots-clés libres

    Returns:
        ID de l'épisode créé
    """
    episodes = _load_episodes()
    episode  = _empty_episode(title, description, category, emotion, importance, tags or [])
    episodes.append(episode)
    _save_episodes(episodes)
    log_event(f"Épisode enregistré : {episode['id']} — {title}")
    return episode["id"]


def record_from_session(
    session_summary: dict,
    session_highlight: str | None = None,
) -> str | None:
    """
    Crée automatiquement un épisode depuis un résumé de session.
    Appelé en fin de session si la session est significative.

    Args:
        session_summary  : Résultat de memory_manager.get_session_summary()
        session_highlight: Moment fort optionnel à mémoriser

    Returns:
        ID épisode créé ou None si session non significative
    """
    count = session_summary.get("exchange_count", 0)
    if count < 3:
        return None  # Session trop courte

    emotion   = session_summary.get("dominant_emotion", "neutral")
    intents   = session_summary.get("intents_seen", [])
    topics    = session_summary.get("topics", [])

    importance = min(1.0, count * 0.05)  # Plus la session est longue, plus c'est important

    title = session_highlight or f"Session {session_summary.get('session_id', 'inconnue')}"
    desc  = (f"Session de {count} échanges. "
             f"Sujets : {', '.join(topics[:3]) if topics else 'général'}. "
             f"Émotion dominante : {emotion}.")

    return record_episode(
        title=title,
        description=desc,
        category="daily",
        emotion=emotion,
        importance=importance,
        tags=intents[:5],
    )


def get_timeline(limit: int = 20, category: str | None = None) -> list[dict]:
    """
    Retourne la timeline chronologique des épisodes.

    Args:
        limit    : Nombre max d'épisodes
        category : Filtre optionnel

    Returns:
        Liste d'épisodes triés par date (plus récent en premier)
    """
    episodes = _load_episodes()
    if category:
        episodes = [e for e in episodes if e.get("category") == category]
    return sorted(episodes, key=lambda e: e["created_at"], reverse=True)[:limit]


def get_important_episodes(threshold: float = 0.7, limit: int = 10) -> list[dict]:
    """
    Retourne les épisodes les plus importants.

    Args:
        threshold : Seuil d'importance minimum
        limit     : Nombre max

    Returns:
        Épisodes triés par importance décroissante
    """
    episodes = _load_episodes()
    important = [e for e in episodes if e.get("importance", 0) >= threshold]
    return sorted(important, key=lambda e: e["importance"], reverse=True)[:limit]


def get_episodes_by_emotion(emotion: str, limit: int = 10) -> list[dict]:
    """
    Retourne les épisodes associés à une émotion.

    Args:
        emotion : Émotion cible
        limit   : Nombre max

    Returns:
        Épisodes filtrés
    """
    episodes = _load_episodes()
    filtered = [e for e in episodes if e.get("emotion") == emotion]
    return sorted(filtered, key=lambda e: e["created_at"], reverse=True)[:limit]


def link_episodes(episode_id_1: str, episode_id_2: str) -> bool:
    """
    Crée un lien contextuel entre deux épisodes (cause/effet).

    Args:
        episode_id_1 : ID premier épisode
        episode_id_2 : ID second épisode

    Returns:
        True si lien créé
    """
    episodes = _load_episodes()
    ep_index = {e["id"]: i for i, e in enumerate(episodes)}

    if episode_id_1 not in ep_index or episode_id_2 not in ep_index:
        return False

    for eid, linked in [(episode_id_1, episode_id_2), (episode_id_2, episode_id_1)]:
        idx = ep_index[eid]
        if linked not in episodes[idx]["linked_to"]:
            episodes[idx]["linked_to"].append(linked)

    _save_episodes(episodes)
    return True


def search_episodes(keyword: str) -> list[dict]:
    """
    Recherche textuelle dans les épisodes.

    Args:
        keyword : Terme à chercher dans titre, description, tags

    Returns:
        Épisodes correspondants
    """
    kw = keyword.lower()
    episodes = _load_episodes()
    return [
        e for e in episodes
        if kw in e.get("title", "").lower()
        or kw in e.get("description", "").lower()
        or any(kw in t.lower() for t in e.get("tags", []))
    ]


def get_episode_stats() -> dict:
    """Statistiques mémoire épisodique."""
    episodes = _load_episodes()
    categories: dict[str, int] = {}
    emotions: dict[str, int] = {}

    for e in episodes:
        c = e.get("category", "general")
        em = e.get("emotion", "neutral")
        categories[c] = categories.get(c, 0) + 1
        emotions[em] = emotions.get(em, 0) + 1

    return {
        "total_episodes": len(episodes),
        "categories":     categories,
        "emotions":       emotions,
        "file":           str(_EPISODE_FILE),
    }
