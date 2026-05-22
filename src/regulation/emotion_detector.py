# ============================================================
# ALFRED — src/regulation/emotion_detector.py
# Bloc 03.01 — Détection émotionnelle
#
# 📚 NOTION EXAM :
#   D31-1 — Capsule 3 : Détection d'états émotionnels par signaux textuels
#
# 🎯 UTILITÉ ALFRED :
#   Détecte l'état émotionnel de l'utilisateur via signaux textuels,
#   classe l'émotion dominante et calcule un score d'intensité.
#
# 🏗️ DOMAINE :
#   Émotions & adaptation — détection V2, prosodie vocale V3
# ============================================================

import re
from datetime import datetime
from dataclasses import dataclass, field


# ─────────────────────────────────────────────────────────
# Modèle état émotionnel
# ─────────────────────────────────────────────────────────

@dataclass
class EmotionalState:
    """Représente l'état émotionnel détecté à un instant T."""
    emotion:   str   = "neutral"   # Émotion principale
    intensity: float = 0.0         # 0.0 (faible) → 1.0 (forte)
    valence:   str   = "neutral"   # positive / negative / neutral
    arousal:   str   = "medium"    # low / medium / high
    signals:   list  = field(default_factory=list)
    timestamp: str   = field(default_factory=lambda: datetime.now().isoformat())
    method:    str   = "keyword_v2"


# ─────────────────────────────────────────────────────────
# Catalogue émotions
# ─────────────────────────────────────────────────────────

_EMOTION_CATALOG: dict[str, dict] = {

    # ── Émotions négatives haute priorité ─────────────────
    "distress": {
        "valence": "negative", "arousal": "high", "base_intensity": 0.9,
        "priority": 5,
        "patterns_fr": [
            r"\bplus envie\b", r"\btout lâcher\b",
            r"\bje n'en peux plus\b", r"\bcraque\b", r"\bà bout\b",
        ],
        "patterns_en": [r"\bno point\b", r"\bgive up\b", r"\bcan't go on\b"],
        "keywords_fr": ["effondrée", "désespérée", "crisis", "détresse"],
        "keywords_en": ["crisis", "hopeless"],
    },
    "stressed": {
        "valence": "negative", "arousal": "high", "base_intensity": 0.7,
        "priority": 4,
        "patterns_fr": [], "patterns_en": [],
        "keywords_fr": [
            "stressée", "stressé", "anxieuse", "panique", "débordée",
            "overwhelmed", "sous pression", "angoissée", "inquiète",
        ],
        "keywords_en": ["stressed", "anxious", "panicking", "overwhelmed", "worried"],
    },
    "sad": {
        "valence": "negative", "arousal": "low", "base_intensity": 0.6,
        "priority": 3,
        "patterns_fr": [], "patterns_en": [],
        "keywords_fr": [
            "triste", "déprimée", "cafard", "moral à zéro",
            "pas bien", "pleure", "larmes", "chagrin",
        ],
        "keywords_en": ["sad", "depressed", "crying", "down", "unhappy"],
    },
    "tired": {
        "valence": "negative", "arousal": "low", "base_intensity": 0.5,
        "priority": 3,
        "patterns_fr": [r"\bplus d.énergie\b", r"\bn'en peux plus\b"],
        "patterns_en": [r"\bno energy\b", r"\bdrained\b"],
        "keywords_fr": [
            "fatiguée", "épuisée", "crevée", "lessivée",
            "vidée", "sans énergie", "exténuée",
        ],
        "keywords_en": ["tired", "exhausted", "drained", "worn out", "fatigued"],
    },
    "confused": {
        "valence": "negative", "arousal": "medium", "base_intensity": 0.4,
        "priority": 2,
        "patterns_fr": [], "patterns_en": [],
        "keywords_fr": [
            "perdue", "confuse", "ne comprends pas", "perdu",
            "pas clair", "bloquée", "coincée",
        ],
        "keywords_en": ["confused", "lost", "don't understand", "unclear", "stuck"],
    },

    # ── Émotions positives ────────────────────────────────
    "motivated": {
        "valence": "positive", "arousal": "high", "base_intensity": 0.7,
        "priority": 2,
        "patterns_fr": [], "patterns_en": [],
        "keywords_fr": [
            "motivée", "motivé", "enthousiaste", "envie",
            "on y va", "prête", "déterminée", "feu",
        ],
        "keywords_en": ["motivated", "enthusiastic", "ready", "pumped", "excited"],
    },
    "happy": {
        "valence": "positive", "arousal": "medium", "base_intensity": 0.6,
        "priority": 1,
        "patterns_fr": [r"\bbonne humeur\b", r"\btrès positif\b", r"\btrès bien\b"],
        "patterns_en": [],
        "keywords_fr": [
            "contente", "heureuse", "super", "géniale", "ravie",
            "top", "excellent", "bonheur", "bonne humeur",
        ],
        "keywords_en": ["happy", "great", "wonderful", "excellent"],
    },
    "focused": {
        "valence": "positive", "arousal": "medium", "base_intensity": 0.5,
        "priority": 1,
        "patterns_fr": [r"\ben mode focus\b", r"\bdans le flow\b", r"\bconcentrée\b"],
        "patterns_en": [r"\bin the zone\b", r"\bflow state\b"],
        "keywords_fr": ["concentrée", "focus", "dans le flux", "productif", "efficace"],
        "keywords_en": ["focused", "productive", "in the zone", "efficient"],
    },
    "curious": {
        "valence": "positive", "arousal": "medium", "base_intensity": 0.4,
        "priority": 1,
        "patterns_fr": [], "patterns_en": [],
        "keywords_fr": [
            "curieuse", "intéressée", "envie de savoir",
            "tu peux m'expliquer", "j'aimerais comprendre",
        ],
        "keywords_en": ["curious", "interested", "want to know", "explain"],
    },

    # ── Neutre / défaut ───────────────────────────────────
    "neutral": {
        "valence": "neutral", "arousal": "medium", "base_intensity": 0.0,
        "priority": 0,
        "patterns_fr": [], "patterns_en": [],
        "keywords_fr": [], "keywords_en": [],
    },
}


# ─────────────────────────────────────────────────────────
# Détection
# ─────────────────────────────────────────────────────────

def detect_emotion(text: str) -> EmotionalState:
    """
    Détecte l'état émotionnel dominant dans un texte.
    Méthode V2.1 : keywords + patterns regex + scoring intensité.

    Règle de sélection (CORRIGÉE) :
        1. Le score total prime TOUJOURS.
        2. La priorité ne départage QUE les égalités à score > 0.
        3. Si score == 0 pour toutes les émotions → "neutral".

    Args:
        text : Texte de l'utilisateur (brut ou nettoyé)

    Returns:
        EmotionalState avec émotion, intensité, valence, arousal
    """
    text_lower = text.lower().strip()

    best_emotion  = "neutral"
    best_score    = 0          # 0 signifie : aucun signal détecté
    best_priority = -1
    found_signals: list[str] = []

    for emotion_id, config in _EMOTION_CATALOG.items():
        if emotion_id == "neutral":
            continue

        score: int = 0
        signals: list[str] = []

        # Keywords (+1 par occurrence)
        for kw in config["keywords_fr"] + config["keywords_en"]:
            if kw in text_lower:
                score += 1
                signals.append(kw)

        # Patterns regex (+2 par match — signal plus fort)
        for pattern in config.get("patterns_fr", []) + config.get("patterns_en", []):
            if re.search(pattern, text_lower, re.IGNORECASE):
                score += 2
                signals.append(pattern)

        # ── Sélection corrigée ────────────────────────────
        # Le score prime. La priorité ne joue QUE si score == best_score > 0.
        if score > best_score:
            best_score    = score
            best_emotion  = emotion_id
            best_priority = config["priority"]
            found_signals = signals
        elif score == best_score and score > 0 and config["priority"] > best_priority:
            best_emotion  = emotion_id
            best_priority = config["priority"]
            found_signals = signals

    # Si aucun signal → neutral
    if best_score == 0:
        best_emotion = "neutral"

    config = _EMOTION_CATALOG[best_emotion]

    # Calcul intensité
    intensity = 0.0
    if best_score > 0:
        base = config.get("base_intensity", 0.5)
        intensity = min(1.0, base + (best_score - 1) * 0.1)

    return EmotionalState(
        emotion   = best_emotion,
        intensity = round(intensity, 2),
        valence   = config.get("valence", "neutral"),
        arousal   = config.get("arousal", "medium"),
        signals   = found_signals,
        method    = "keyword_v2.1",
    )


# ─────────────────────────────────────────────────────────
# Fonctions utilitaires
# ─────────────────────────────────────────────────────────

def detect_emotion_from_audio_stub() -> EmotionalState:
    """
    Détection émotion via prosodie vocale.
    V3 STUB → retourne toujours neutral.
    V3+ : analyse pitch, débit, énergie via librosa.
    """
    return EmotionalState(emotion="neutral", method="audio_stub_v3")


def is_negative_emotion(state: EmotionalState) -> bool:
    """Retourne True si l'émotion est négative."""
    return state.valence == "negative"


def is_high_intensity(state: EmotionalState, threshold: float = 0.6) -> bool:
    """Retourne True si l'intensité dépasse le seuil."""
    return state.intensity >= threshold


def requires_support_mode(state: EmotionalState) -> bool:
    """
    Détermine si l'état émotionnel nécessite le mode support.
    Utilisé par mode_manager.py pour les transitions automatiques.
    """
    return (
        state.emotion in ["distress", "stressed", "sad", "tired", "confused"]
        and state.intensity >= 0.4
    )


def get_emotion_label_fr(emotion: str) -> str:
    """Retourne un label français lisible pour l'émotion."""
    labels = {
        "distress":  "détresse",
        "stressed":  "stress",
        "sad":       "tristesse",
        "tired":     "fatigue",
        "confused":  "confusion",
        "motivated": "motivation",
        "happy":     "joie",
        "focused":   "concentration",
        "curious":   "curiosité",
        "neutral":   "neutre",
    }
    return labels.get(emotion, emotion)


# ─────────────────────────────────────────────────────────
# Test local
# ─────────────────────────────────────────────────────────

if __name__ == "__main__":
    tests = [
        ("je suis de bonne humeur aujourd'hui, il fait beau",          "happy"),
        ("je vais parfaitement bien, moral très positif",              "happy"),
        ("je suis motivée, on y va !",                                 "motivated"),
        ("je suis perdue, je ne comprends pas",                        "confused"),
        ("je suis épuisée, plus d'énergie",                            "tired"),
        ("je n'en peux plus, je craque",                               "distress"),
        ("aide-moi à structurer mon projet",                           "neutral"),
    ]

    print("=== TEST emotion_detector V2.1 ===\n")
    ok = 0
    for text, expected in tests:
        result = detect_emotion(text)
        status = "✅" if result.emotion == expected else f"❌ (attendu: {expected})"
        print(f"{status} [{result.emotion}] score-signals={result.signals} | \"{text[:50]}\"")
        if result.emotion == expected:
            ok += 1

    print(f"\n{ok}/{len(tests)} tests passés")
