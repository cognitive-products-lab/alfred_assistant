# ============================================================
# ALFRED — src/conversation/nlp/nlp_engine_v2.py
# Bloc 01.02 — Compréhension des intentions
#
# 📚 NOTION EXAM :
#   D12-2 — Capsule 2 : NLP enrichi — scoring émotion et détection langue
#
# 🎯 UTILITÉ ALFRED :
#   Moteur NLP V2 — étend V1 avec scoring émotionnel, détection langue,
#   classification d'intention (IntentNet, cf. intent_classifier.py) et
#   hook LLM local (Mistral/llama-cpp) prévu pour V3.
#
# 🏗️ DOMAINE :
#   Noyau conversationnel — NLP enrichi V2, LLM-ready
#
# STATUS  : VALIDATED
# ============================================================

from __future__ import annotations

from src.conversation.nlp.intent_classifier import IntentClassifier

_intent_classifier = IntentClassifier()


def analyze_v2(text: str, time_context: dict | None = None) -> dict:
    """
    Analyse NLP simplifiee temporaire.
    Retourne une structure compatible avec le pipeline ALFRED.
    """

    text_lower = text.lower()

    if any(word in text_lower for word in ["fatigue", "stress", "marre"]):
        emotion = "stressed"
    elif any(word in text_lower for word in ["content", "super", "cool"]):
        emotion = "happy"
    else:
        emotion = "neutral"

    intent = _intent_classifier.classify(text)
    confidence = 0.8 if intent != "fallback" else 0.3

    return {
        "intent": intent,
        "emotion": emotion,
        "confidence": confidence,
        "entities": [],
        "time_context": time_context or {},
    }
