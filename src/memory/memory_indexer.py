# ============================================================
# ALFRED — src/memory/memory_indexer.py
# Bloc 02.05 — Indexation & recherche mémoire
#
# Fonctions couvertes :
#   02.05.001 Pipeline ingestion               ✅ V2
#   02.05.002 Mise à jour incrémentale         ✅ V2
#   02.05.003 Gestion doublons                 ✅ V2
#   02.05.004 Scoring pertinence résultats     ✅ V2
#   02.05.005 Export / sauvegarde index        ✅ V2
#
# Agrège court terme + long terme + épisodique
# dans une interface unique pour le pipeline principal.
# ============================================================

from datetime import datetime
from src.memory.memory_manager    import get_session_summary, get_history, get_dominant_emotion
from src.memory.long_term_memory  import search_memories, get_top_patterns, get_fact, get_all_facts
from src.memory.episodic_memory   import search_episodes, get_important_episodes, get_episode_stats
from src.security.security_logger import log_event


def search_all_memory(keyword: str, limit: int = 10) -> dict:
    """
    Recherche unifiée dans toutes les couches mémoire.

    Args:
        keyword : Terme à chercher
        limit   : Nombre max de résultats par couche

    Returns:
        dict avec résultats par couche + score global
    """
    results = {
        "keyword":   keyword,
        "timestamp": datetime.now().isoformat(),
        "long_term": search_memories(keyword, limit),
        "episodes":  search_episodes(keyword)[:limit],
        "facts":     {},
    }

    # Faits contenant le keyword
    all_facts = get_all_facts()
    results["facts"] = {
        k: v for k, v in all_facts.items()
        if keyword.lower() in str(k).lower() or keyword.lower() in str(v).lower()
    }

    results["total_found"] = (
        len(results["long_term"]) +
        len(results["episodes"]) +
        len(results["facts"])
    )

    return results


def build_memory_context(max_memories: int = 5) -> dict:
    """
    Construit le contexte mémoire complet à injecter dans le prompt LLM.
    Point d'entrée principal pour le pipeline de génération de réponse.

    Args:
        max_memories : Nombre max de mémoires récentes à inclure

    Returns:
        dict contexte mémoire prêt pour injection prompt
    """
    session   = get_session_summary()
    patterns  = get_top_patterns(3)
    important = get_important_episodes(threshold=0.6, limit=3)
    facts     = get_all_facts(category="profil")

    return {
        "session":           session,
        "top_patterns":      patterns,
        "important_episodes": important,
        "user_facts":        facts,
        "dominant_emotion":  get_dominant_emotion(),
        "generated_at":      datetime.now().isoformat(),
    }


def format_memory_for_prompt(max_exchanges: int = 3) -> str:
    """
    Formate le contexte mémoire en texte injectable dans un prompt.

    Args:
        max_exchanges : Nombre d'échanges récents à inclure

    Returns:
        Bloc texte structuré
    """
    ctx     = build_memory_context()
    session = ctx["session"]
    facts   = ctx["user_facts"]
    history = get_history(max_exchanges)

    lines = ["[Mémoire ALFRED]"]

    # Faits utilisateur connus
    if facts:
        lines.append(f"Utilisatrice : {facts.get('prénom', 'Céline')}")
        if "projet_actuel" in facts:
            lines.append(f"Projet actuel : {facts['projet_actuel']}")

    # Émotion dominante session
    emotion = session.get("dominant_emotion", "neutral")
    if emotion != "neutral":
        lines.append(f"État émotionnel : {emotion}")

    # Échanges récents
    if history:
        lines.append(f"Derniers échanges ({len(history)}) :")
        for ex in history:
            lines.append(f"  › {ex['user'][:80]}")

    # Patterns
    patterns = ctx.get("top_patterns", [])
    if patterns:
        top = patterns[0]
        lines.append(f"Pattern récurrent : {top['pattern_key']} ({top['count']}×)")

    return "\n".join(lines)


def score_memory_relevance(memory: dict, current_intent: str) -> float:
    """
    Calcule un score de pertinence pour une mémoire donnée.

    Facteurs :
        - correspondance intent
        - importance stockée
        - récence (pénalité si trop vieille)

    Args:
        memory         : Dict mémoire (depuis long_term_memory)
        current_intent : Intent courant

    Returns:
        Score float 0.0 → 1.0
    """
    score = memory.get("importance", 0.5)

    # Bonus intent correspondant
    if memory.get("intent") == current_intent:
        score += 0.3

    # Pénalité ancienneté
    try:
        mem_date = datetime.fromisoformat(memory.get("timestamp", ""))
        days_old = (datetime.now() - mem_date).days
        if days_old > 30:
            score *= 0.7
        elif days_old > 7:
            score *= 0.9
    except (ValueError, TypeError):
        pass

    return min(1.0, round(score, 3))


def get_memory_stats() -> dict:
    """Statistiques complètes de toutes les couches mémoire."""
    from src.memory.long_term_memory import get_memory_stats as lt_stats
    ep_stats = get_episode_stats()
    lt       = lt_stats()
    session  = get_session_summary()

    return {
        "session":    {"exchanges": session["exchange_count"]},
        "long_term":  lt,
        "episodic":   ep_stats,
        "version":    "memory_indexer_v2",
    }
