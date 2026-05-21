# ============================================================
# ALFRED — src/input/nlp_engine_v2.py
# Bloc 01.04 V2 — NLP enrichi, prêt pour LLM local
#
# Évolution de nlp_engine.py V1 :
#   V1 → keywords uniquement
#   V2 → keywords + scoring émotion + détection langue + LLM-ready
#   V3 → LLM local (Mistral/llama-cpp) — hook prévu
#
# Usage : remplace nlp_engine.py quand V2 est actif.
# main.py choisit la version selon APP_VERSION dans .env.
# ============================================================

from datetime import datetime
from src.input.nlp_engine import (
    extract_entities,
    get_intent_label,
)


# ─────────────────────────────────────────────────────────
# Détection de langue (V2)
# ─────────────────────────────────────────────────────────

_FR_MARKERS = {"je", "tu", "il", "nous", "vous", "ils", "le", "la", "les",
               "un", "une", "des", "et", "ou", "mais", "donc", "car",
               "que", "qui", "quoi", "comment", "pourquoi", "bonjour"}

_EN_MARKERS = {"i", "you", "he", "she", "we", "they", "the", "a", "an",
               "and", "or", "but", "so", "because", "that", "what",
               "who", "how", "why", "hello", "please"}


def detect_language(text: str) -> str:
    """
    Détecte la langue dominante du message (FR / EN).
    Méthode simple par fréquence de marqueurs.

    Args:
        text : Texte utilisateur

    Returns:
        "fr" | "en" | "unknown"
    """
    words = set(text.lower().split())
    fr_score = len(words & _FR_MARKERS)
    en_score = len(words & _EN_MARKERS)

    if fr_score == 0 and en_score == 0:
        return "unknown"
    return "fr" if fr_score >= en_score else "en"


# ─────────────────────────────────────────────────────────
# Scoring émotionnel (V2)
# ─────────────────────────────────────────────────────────

_EMOTION_SIGNALS: dict[str, list[str]] = {
    "stressed": ["stressée", "anxieuse", "panique", "débordée",
                 "overwhelmed", "stressed", "anxious"],
    "tired":    ["fatiguée", "épuisée", "crevée", "plus d'énergie",
                 "tired", "exhausted", "no energy"],
    "sad":      ["triste", "déprimée", "mal", "pas bien", "pleure",
                 "sad", "depressed", "crying"],
    "motivated": ["motivée", "prête", "envie", "on y va", "ça marche",
                  "motivated", "ready", "let's go"],
    "happy":    ["contente", "heureuse", "super", "géniale", "top",
                 "happy", "great", "awesome", "excited"],
    "focused":  ["concentrée", "en mode focus", "dans le flux", "productif",
                 "focused", "in the zone", "flow"],
    "neutral":  [],  # état par défaut
}


def detect_emotion(text: str) -> dict:
    """
    Détecte l'état émotionnel dominant dans le message.

    Args:
        text : Texte utilisateur

    Returns:
        dict avec emotion détectée, score, et liste de signaux trouvés
    """
    text_lower = text.lower()
    best_emotion = "neutral"
    best_score = 0
    found_signals: list[str] = []

    for emotion, signals in _EMOTION_SIGNALS.items():
        matches = [s for s in signals if s in text_lower]
        if len(matches) > best_score:
            best_score = len(matches)
            best_emotion = emotion
            found_signals = matches

    return {
        "emotion": best_emotion,
        "score":   best_score,
        "signals": found_signals,
    }


# ─────────────────────────────────────────────────────────
# Hook LLM (V3 — à brancher)
# ─────────────────────────────────────────────────────────

def _analyze_with_llm(text: str) -> dict | None:
    """
    Hook pour analyse LLM local (V3 — Mistral/llama-cpp).

    V2 : retourne toujours None → fallback sur keywords.
    V3 : retourne un dict complet avec intent + émotion + entités.

    Args:
        text : Texte utilisateur

    Returns:
        None en V2, dict résultat LLM en V3
    """
    # TODO V3 : brancher llm_client_local.py ici
    # from src.llm.llm_client_local import query_llm
    # return query_llm(prompt=build_nlp_prompt(text))
    return None


# ─────────────────────────────────────────────────────────
# Analyse principale V2
# ─────────────────────────────────────────────────────────

def analyze_v2(user_input: str) -> dict:
    """
    Point d'entrée NLP V2 — agrège intent, émotion, langue, entités.

    Pipeline :
      1. Tentative LLM local (hook V3, None en V2)
      2. Si None → keywords V1 + émotion V2 + langue V2

    Args:
        user_input : Texte nettoyé de l'utilisateur

    Returns:
        dict enrichi avec intent, emotion, language, entities, confidence
    """
    text = user_input.strip()

    # ── Tentative LLM ─────────────────────────────────
    llm_result = _analyze_with_llm(text)
    if llm_result:
        return {**llm_result, "method": "llm_v3", "timestamp": datetime.now().isoformat()}

    # ── Fallback keywords + enrichissements V2 ────────
    # Intent (réutilise V1)
    from src.input.nlp_engine import detect_intent
    intent_result  = detect_intent(text)

    # Émotion (nouveau V2)
    emotion_result = detect_emotion(text)

    # Langue (nouveau V2)
    language       = detect_language(text)

    # Entités (réutilise V1)
    entities       = extract_entities(text)

    # Score de confiance global
    confidence = min(1.0, (intent_result["score"] * 0.2) +
                          (emotion_result["score"] * 0.15) +
                          (0.3 if intent_result["intent"] != "general" else 0.0))

    return {
        "raw_input":  user_input,
        "intent":     intent_result["intent"],
        "intent_label": get_intent_label(intent_result["intent"]),
        "intent_score": intent_result["score"],
        "emotion":    emotion_result["emotion"],
        "emotion_score": emotion_result["score"],
        "emotion_signals": emotion_result["signals"],
        "language":   language,
        "entities":   entities,
        "confidence": round(confidence, 3),
        "method":     "keyword_v2",
        "timestamp":  datetime.now().isoformat(),
    }


def get_vocal_mode_from_analysis(analysis: dict) -> str:
    """
    Déduit le mode vocal ALFRED depuis le résultat NLP.
    Utilisé par tts_piper.py pour choisir les paramètres de voix.

    Priority : émotion > intent > défaut

    Args:
        analysis : Résultat de analyze_v2()

    Returns:
        Mode vocal : support | focus | challenge | complicite | default
    """
    from src.input.voice_profile import EMOTION_TO_MODE

    emotion = analysis.get("emotion", "neutral")
    intent  = analysis.get("intent", "general")

    # Émotion détectée → mode support si négatif
    if emotion in EMOTION_TO_MODE:
        return EMOTION_TO_MODE[emotion]

    # Intent → mode
    intent_to_mode = {
        "emotional_support": "support",
        "wellbeing":         "support",
        "knowledge_request": "focus",
        "engineering":       "focus",
        "product_knowledge": "challenge",
        "greeting":          "complicite",
        "home_automation":   "focus",
    }
    return intent_to_mode.get(intent, "default")
