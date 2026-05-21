# ============================================================
# ALFRED — src/memory/memory_manager.py
# Bloc 02.01 — Mémoire courte
#
# 📚 NOTION EXAM :
#   D21-1 — Capsule 2 : Mémoire de travail et historique de session
#
# 🎯 UTILITÉ ALFRED :
#   Stocke l'historique de dialogue courant et le contexte actif
#   en RAM pendant la session ; persiste en JSON via long_term_memory.py.
#
# 🏗️ DOMAINE :
#   Mémoire & contexte — mémoire courte locale, flush fin de session
# ============================================================

import json
from datetime import datetime
from pathlib import Path
from typing import Any

from src.security.security_logger import log_event

# ── Chemins données ───────────────────────────────────────
_DATA_DIR      = Path("data/memory")
_SESSION_FILE  = _DATA_DIR / "current_session.json"
_DATA_DIR.mkdir(parents=True, exist_ok=True)

# ── Limites ───────────────────────────────────────────────
MAX_HISTORY    = 50   # Échanges max en mémoire vive
MAX_CONTEXT    = 100  # Entrées contexte actif


# ─────────────────────────────────────────────────────────
# Structure session
# ─────────────────────────────────────────────────────────

def _empty_session() -> dict:
    """Retourne une structure de session vide."""
    return {
        "session_id":  datetime.now().strftime("%Y%m%d_%H%M%S"),
        "started_at":  datetime.now().isoformat(),
        "user_name":   "Céline",
        "history":     [],       # Échanges dialogue
        "context":     {},       # Clés/valeurs contexte actif
        "intents":     [],       # Intentions détectées session
        "emotions":    [],       # États émotionnels session
        "topics":      [],       # Sujets abordés
        "exchange_count": 0,
    }


# ─────────────────────────────────────────────────────────
# Session en mémoire vive (singleton)
# ─────────────────────────────────────────────────────────

_session: dict = _empty_session()


def get_session() -> dict:
    """Retourne la session courante complète."""
    return _session.copy()


def get_session_id() -> str:
    """Retourne l'identifiant de session courant."""
    return _session["session_id"]


# ─────────────────────────────────────────────────────────
# Historique dialogue (02.01.001 / 02.01.002)
# ─────────────────────────────────────────────────────────

def add_exchange(
    user_input: str,
    alfred_response: str,
    intent: str = "general",
    emotion: str = "neutral",
) -> None:
    """
    Enregistre un échange complet dans l'historique session.

    Args:
        user_input      : Message de l'utilisateur
        alfred_response : Réponse d'ALFRED
        intent          : Intention détectée (NLP)
        emotion         : État émotionnel détecté
    """
    exchange = {
        "timestamp":  datetime.now().isoformat(),
        "user":       user_input,
        "alfred":     alfred_response,
        "intent":     intent,
        "emotion":    emotion,
        "turn":       _session["exchange_count"] + 1,
    }

    _session["history"].append(exchange)
    _session["exchange_count"] += 1

    # Tracking intent et émotion
    if intent not in _session["intents"]:
        _session["intents"].append(intent)
    if emotion not in _session["emotions"] and emotion != "neutral":
        _session["emotions"].append(emotion)

    # Limite mémoire vive
    if len(_session["history"]) > MAX_HISTORY:
        _session["history"] = _session["history"][-MAX_HISTORY:]
        log_event(f"Historique tronqué à {MAX_HISTORY} échanges", "INFO")


def get_history(n: int = 0) -> list[dict]:
    """
    Retourne l'historique session.

    Args:
        n : Nombre de derniers échanges (0 = tous)

    Returns:
        Liste des échanges
    """
    if n > 0:
        return _session["history"][-n:]
    return _session["history"].copy()


def get_last_user_message() -> str | None:
    """Retourne le dernier message utilisateur."""
    if _session["history"]:
        return _session["history"][-1]["user"]
    return None


def get_last_intent() -> str:
    """Retourne la dernière intention détectée."""
    if _session["history"]:
        return _session["history"][-1]["intent"]
    return "general"


# ─────────────────────────────────────────────────────────
# Contexte actif (02.01.003 / 02.01.004)
# ─────────────────────────────────────────────────────────

def set_context(key: str, value: Any) -> None:
    """
    Définit une valeur dans le contexte actif de session.

    Args:
        key   : Clé contexte (ex: "current_topic", "last_emotion")
        value : Valeur à stocker
    """
    _session["context"][key] = {
        "value":     value,
        "updated_at": datetime.now().isoformat(),
    }


def get_context(key: str, default: Any = None) -> Any:
    """
    Récupère une valeur du contexte actif.

    Args:
        key     : Clé contexte
        default : Valeur par défaut si absente

    Returns:
        Valeur stockée ou default
    """
    entry = _session["context"].get(key)
    if entry is None:
        return default
    return entry["value"]


def update_context_from_analysis(analysis: dict) -> None:
    """
    Met à jour le contexte depuis un résultat NLP V2.
    Appelé automatiquement après chaque analyse.

    Args:
        analysis : Résultat de nlp_engine_v2.analyze_v2()
    """
    set_context("last_intent",  analysis.get("intent", "general"))
    set_context("last_emotion", analysis.get("emotion", "neutral"))
    set_context("last_language", analysis.get("language", "fr"))

    # Tracking topics
    intent = analysis.get("intent", "general")
    if intent != "general" and intent not in _session["topics"]:
        _session["topics"].append(intent)


def get_dominant_emotion() -> str:
    """
    Retourne l'émotion dominante de la session.
    Basé sur la fréquence des émotions détectées.
    """
    if not _session["emotions"]:
        return "neutral"

    # Comptage depuis l'historique
    emotion_counts: dict[str, int] = {}
    for exchange in _session["history"]:
        e = exchange.get("emotion", "neutral")
        if e != "neutral":
            emotion_counts[e] = emotion_counts.get(e, 0) + 1

    if not emotion_counts:
        return "neutral"
    return max(emotion_counts, key=emotion_counts.get)


# ─────────────────────────────────────────────────────────
# Reset session (02.01.005)
# ─────────────────────────────────────────────────────────

def reset_session(user_name: str = "Céline") -> str:
    """
    Réinitialise la session courante.
    Déclenche la sauvegarde en long terme avant reset.

    Args:
        user_name : Prénom utilisateur

    Returns:
        Nouvel ID de session
    """
    global _session

    # Sauvegarder avant reset si des échanges ont eu lieu
    if _session["exchange_count"] > 0:
        _save_session_snapshot()

    _session = _empty_session()
    _session["user_name"] = user_name
    log_event(f"Nouvelle session démarrée : {_session['session_id']}")
    return _session["session_id"]


def _save_session_snapshot() -> None:
    """Sauvegarde un snapshot JSON de la session courante."""
    try:
        snapshot_dir = _DATA_DIR / "sessions"
        snapshot_dir.mkdir(parents=True, exist_ok=True)
        path = snapshot_dir / f"session_{_session['session_id']}.json"
        path.write_text(
            json.dumps(_session, indent=2, ensure_ascii=False),
            encoding="utf-8"
        )
        log_event(f"Session sauvegardée : {path.name}")
    except Exception as e:
        log_event(f"Erreur sauvegarde session : {e}", "ERROR")


# ─────────────────────────────────────────────────────────
# Résumé session
# ─────────────────────────────────────────────────────────

def get_session_summary() -> dict:
    """
    Retourne un résumé de la session courante.
    Utilisé pour l'injection contexte dans les prompts.
    """
    return {
        "session_id":      _session["session_id"],
        "exchange_count":  _session["exchange_count"],
        "intents_seen":    _session["intents"],
        "emotions_seen":   _session["emotions"],
        "topics":          _session["topics"],
        "dominant_emotion": get_dominant_emotion(),
        "last_user_msg":   get_last_user_message(),
        "last_intent":     get_last_intent(),
        "started_at":      _session["started_at"],
    }


def format_history_for_prompt(n: int = 5) -> str:
    """
    Formate les derniers échanges pour injection dans un prompt LLM.

    Args:
        n : Nombre d'échanges à inclure

    Returns:
        Texte formaté pour le prompt système
    """
    exchanges = get_history(n)
    if not exchanges:
        return "[Début de conversation]"

    lines = []
    for ex in exchanges:
        lines.append(f"Céline : {ex['user']}")
        lines.append(f"ALFRED : {ex['alfred']}")
    return "\n".join(lines)
