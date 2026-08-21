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
#
# UPDATED : 2026-06-10 — chemin _EPISODE_FILE ancré sur paths.PATHS
# STATUS  : VALIDATED (auto: tests/test_b02_b03.py OK le 2026-07-05 ; cwd réel encore à reconfirmer)
# ============================================================

import json
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

from src.security.security_logger import log_event
from paths import PATHS

# ── Stockage JSON (local-first) ───────────────────────────
# Ancré sur la racine du projet (paths.py, basé sur __file__) — ne dépend pas
# du répertoire de travail courant au lancement de main.py.
_EPISODE_FILE = PATHS.data_memory / "episodes.json"
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
        # Précision microseconde (pas seconde) : deux épisodes créés dans la
        # même seconde (tests, rafale d'échanges) ne doivent jamais partager
        # le même ID — trouvé le 17/08/2026 : 104 IDs en collision sur les
        # données existantes avec l'ancien format %Y%m%d_%H%M%S.
        "id":           f"ep_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}",
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
# Scoring d'importance (21/08/2026)
# ─────────────────────────────────────────────────────────
# Avant : main.py plafonnait chaque échange auto-enregistré à 0.3
# d'importance (0.5/0.6 seulement sur suggestion proactive/check-in).
# Constaté le 21/08/2026 : 55 épisodes réels, tous à 0.3 pile, 0 moment
# marquant dans la Vue Mémoire (seuil 0.6) — le plafond starvait les deux
# fonctionnalités livrées cette semaine (Vue Mémoire, rappel contextuel).

_IMPORTANCE_STOPWORDS = {
    "alfred", "celine", "céline", "bonjour", "bonsoir", "merci", "voila", "voilà",
    "comment", "pourquoi", "quand", "aujourd", "hui", "maintenant", "toujours",
    "jamais", "encore", "parce", "cette", "avec", "sans", "dans", "pour",
    "tres", "très", "bien", "faire", "fait", "dire", "dit", "vraiment", "besoin",
    "peux", "veux", "voudrais", "aimerais", "peut", "doit", "faut",
}


def _extract_topic_keywords(text: str, min_len: int = 4) -> list[str]:
    words = re.findall(r"[a-zàâäéèêëïîôöùûüç]+", text.lower())
    seen: list[str] = []
    for w in words:
        if len(w) >= min_len and w not in _IMPORTANCE_STOPWORDS and w not in seen:
            seen.append(w)
    return seen


def _is_recurring_topic(text: str, lookback_days: int = 7, min_occurrences: int = 2) -> bool:
    """
    True si au moins un mot-clé significatif du texte apparaît déjà dans
    ≥ min_occurrences épisodes récents — appelé AVANT l'enregistrement de
    l'épisode courant, donc pas d'auto-match.
    """
    keywords = _extract_topic_keywords(text)
    if not keywords:
        return False

    cutoff = (datetime.now() - timedelta(days=lookback_days)).isoformat()
    for kw in keywords[:3]:  # borne le coût — les mots-clés les plus tôt suffisent
        matches = [e for e in search_episodes(kw) if e.get("created_at", "") >= cutoff]
        if len(matches) >= min_occurrences:
            return True
    return False


def compute_turn_importance(
    text: str = "",
    emotion_intensity: float = 0.0,
    emotion_valence: str = "neutral",
    health_rumination: bool = False,
    health_bipolar_episode: bool = False,
    health_hyperfocus: bool = False,
    emotion_trend_concerning: bool = False,
    proactive_suggestion: bool = False,
    check_in: bool = False,
) -> float:
    """
    Score d'importance d'un échange à partir de vrais signaux — remplace
    le plafond fixe 0.3 (voir note ci-dessus).

    Args:
        text                     : Contenu de l'échange (titre/description),
                                    utilisé pour détecter un sujet récurrent
        emotion_intensity        : Intensité de l'émotion détectée (0.0-1.0)
        emotion_valence          : "negative" / "positive" / "neutral"
        health_rumination        : Signal rumination détecté (Bloc 13)
        health_bipolar_episode   : Signal épisode bipolaire possible détecté
        health_hyperfocus        : Signal hyperfocus détecté
        emotion_trend_concerning : Tendance émotionnelle soutenue difficile
                                    sur plusieurs jours (emotional_trend.py)
        proactive_suggestion     : Une suggestion proactive a été déclenchée
        check_in                 : Un check-in bien-être a été déclenché

    Returns:
        Score 0.0-1.0
    """
    base = 0.3

    if emotion_intensity >= 0.7:
        base = max(base, 0.7)
    elif emotion_intensity >= 0.5:
        base = max(base, 0.55)
    elif emotion_intensity >= 0.3:
        base = max(base, 0.4)

    # Émotion marquée (pas neutre) et pas juste de faible intensité —
    # ajout, pas un plancher, pour ne pas écraser un signal plus fort ailleurs.
    if emotion_valence in ("negative", "positive") and emotion_intensity >= 0.4:
        base += 0.05

    if health_rumination or health_bipolar_episode:
        base = max(base, 0.65)
    if health_hyperfocus:
        base = max(base, 0.55)
    if emotion_trend_concerning:
        base = max(base, 0.6)

    if text and _is_recurring_topic(text):
        base += 0.15

    if proactive_suggestion:
        base = max(base, 0.5)
    if check_in:
        base = max(base, 0.6)

    return min(1.0, round(base, 2))


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
    _index_episode_for_semantic_search(episode)
    return episode["id"]


def _index_episode_for_semantic_search(episode: dict) -> None:
    """
    Indexe l'épisode dans ChromaDB (src.memory.rag_stub) pour la recherche
    sémantique — best-effort, ne doit jamais faire échouer record_episode()
    (RAG optionnel : absent si chromadb non installé, ce qui reste un cas
    normal, voir rag_stub.is_rag_available()).
    """
    try:
        from src.memory.rag_stub import index_document
        text = f"{episode.get('title', '')}. {episode.get('description', '')}".strip()
        index_document(
            text=text,
            doc_id=episode["id"],
            metadata={
                "category":   episode.get("category"),
                "emotion":    episode.get("emotion"),
                "importance": episode.get("importance"),
                "created_at": episode.get("created_at"),
            },
        )
    except Exception:
        pass


def backfill_semantic_index() -> int:
    """
    Réindexe tous les épisodes existants dans ChromaDB — à lancer une fois
    après activation du RAG (session 6, 18/08/2026) pour couvrir l'historique
    déjà présent, les nouveaux épisodes s'indexant automatiquement via
    record_episode(). Idempotent (upsert) — relançable sans risque.

    Returns:
        Nombre d'épisodes indexés (0 si RAG indisponible).
    """
    from src.memory.rag_stub import is_rag_available

    if not is_rag_available():
        return 0

    count = 0
    for episode in _load_episodes():
        _index_episode_for_semantic_search(episode)
        count += 1
    return count


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


def get_episode_by_id(episode_id: str) -> dict | None:
    """Retourne un épisode complet (avec description) par son ID, ou None."""
    for e in _load_episodes():
        if e.get("id") == episode_id:
            return e
    return None


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
