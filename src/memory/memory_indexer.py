# ============================================================
# ALFRED — src/memory/memory_indexer.py
# Bloc 02.04 — Contextualisation intelligente
#
# 📚 NOTION EXAM :
#   D22-1 — Capsule 3 : Indexation et recherche mémoire multi-sources
#
# 🎯 UTILITÉ ALFRED :
#   Agrège mémoire courte, longue et épisodique dans un index unifié ;
#   gère l'ingestion, les doublons et le scoring de pertinence.
#
# 🏗️ DOMAINE :
#   Mémoire & contexte — indexation unifiée, RAG-ready
#
# STATUS  : VALIDATED
# ============================================================

import re
from datetime import datetime
from src.memory.memory_manager    import get_session_summary, get_history, get_dominant_emotion
from src.memory.long_term_memory  import search_memories, get_top_patterns, get_fact, get_all_facts
from src.memory.episodic_memory   import search_episodes, get_important_episodes, get_episode_stats
from src.security.security_logger import log_event


# Mots trop génériques pour déclencher une recherche de rappel contextuel
# (sinon toute phrase banale ferait remonter un souvenir sans rapport réel).
_RECALL_STOPWORDS = {
    "alfred", "celine", "céline", "bonjour", "bonsoir", "merci", "voila", "voilà",
    "comment", "pourquoi", "quand", "aujourd", "hui", "maintenant", "toujours",
    "jamais", "encore", "parce", "cette", "avec", "sans", "dans", "pour",
    "tres", "très", "bien", "faire", "fait", "dire", "dit", "vraiment", "besoin",
    "peux", "veux", "voudrais", "aimerais", "peut", "doit", "faut",
}


def _extract_recall_keywords(text: str, min_len: int = 4) -> list[str]:
    words = re.findall(r"[a-zàâäéèêëïîôöùûüç]+", text.lower())
    seen: list[str] = []
    for w in words:
        if len(w) >= min_len and w not in _RECALL_STOPWORDS and w not in seen:
            seen.append(w)
    return seen


def get_contextual_recall(
    user_input: str,
    exclude_ids: "set[str] | None" = None,
    threshold: float = 0.6,
    semantic_distance_max: float = 0.8,
) -> "dict | None":
    """
    Cherche, parmi la mémoire épisodique, un souvenir réellement pertinent
    par rapport au message courant — pour un rappel spontané et ponctuel,
    pas un scan qui ferait remonter systématiquement quelque chose à
    chaque tour (ce qui deviendrait vite envahissant).

    D'abord une recherche par mot-clé (rapide, exacte). Si rien d'assez
    important n'en ressort, repli sur la recherche sémantique (ChromaDB,
    session 6 du 18/08/2026) — utile quand le message ne partage aucun mot
    avec l'épisode (ex. "présentation orale" ↔ épisode sur "soutenance").
    Le repli sémantique est silencieusement absent si RAG indisponible
    (chromadb non installé) — pas une erreur, juste moins de portée.

    Args:
        user_input             : Message courant de l'utilisateur
        exclude_ids            : IDs d'épisodes déjà rappelés dans la
                                  session (pour ne pas ressasser en boucle)
        threshold               : Importance minimale de l'épisode pour
                                  être rappelé
        semantic_distance_max  : Distance ChromaDB max pour considérer un
                                  résultat sémantique comme pertinent (plus
                                  bas = plus proche/pertinent)

    Returns:
        {"kind": "episode", "id", "title", "date", "category"} ou None
    """
    exclude_ids = exclude_ids or set()
    keywords = _extract_recall_keywords(user_input)

    best: "dict | None" = None
    best_score = 0.0

    for kw in keywords[:5]:  # borne le coût — les mots-clés significatifs les plus tôt dans le message suffisent
        for ep in search_episodes(kw):
            if ep.get("id") in exclude_ids:
                continue
            importance = ep.get("importance", 0) or 0
            if importance <= best_score:
                continue
            best_score = importance
            best = {
                "kind":     "episode",
                "id":       ep.get("id"),
                "title":    ep.get("title", ""),
                "date":     ep.get("created_at", ""),
                "category": ep.get("category", ""),
            }

    if best is not None and best_score >= threshold:
        return best

    try:
        from src.memory.rag_stub import semantic_search
        for hit in semantic_search(user_input, n_results=3):
            hit_id = hit.get("id")
            if not hit_id or hit_id in exclude_ids:
                continue
            distance = hit.get("distance")
            if distance is None or distance > semantic_distance_max:
                continue
            meta = hit.get("metadata") or {}
            importance = meta.get("importance", 0) or 0
            if importance < threshold:
                continue
            title = (hit.get("text") or "").split(". ", 1)[0]
            return {
                "kind":     "episode",
                "id":       hit_id,
                "title":    title,
                "date":     meta.get("created_at", ""),
                "category": meta.get("category", ""),
            }
    except Exception:
        pass

    return None


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
