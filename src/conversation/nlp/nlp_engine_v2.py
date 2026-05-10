# ============================================================
# ALFRED — NLP Engine V2 (stub temporaire)
# Encodage : UTF-8
# ============================================================

from __future__ import annotations


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

    return {
        "intent": "conversation",
        "emotion": emotion,
        "confidence": 0.5,
        "entities": [],
        "time_context": time_context or {},
    }
