# ============================================================
# ALFRED — src/regulation/protection_guard.py
# Bloc 03.04 — Personnalité dynamique
#
# 📚 NOTION EXAM :
#   D32-1 — Capsule 3 : Mode protection et garde-fous éthiques IA
#
# 🎯 UTILITÉ ALFRED :
#   Détecte les situations de détresse, active le mode protection,
#   bloque les contenus inadaptés et applique les garde-fous éthiques H3.
#
# 🔐 BLOC ÉTHIQUE :
#   H3 — cadre éthique conciliant performance, utilité et autonomie humaine
# ============================================================

from src.regulation.emotion_detector import EmotionalState
from src.security.security_logger import log_event


# ─────────────────────────────────────────────────────────
# Seuils de protection
# ─────────────────────────────────────────────────────────

CRISIS_EMOTIONS    = {"distress"}           # Déclenchement immédiat mode protection
HIGH_RISK_EMOTIONS = {"stressed", "sad"}    # Protection si intensité élevée
CRISIS_THRESHOLD   = 0.7                    # Seuil intensité pour high_risk

# Mots-clés crise absolue (jamais gérés par ALFRED seul)
_CRISIS_KEYWORDS = [
    "me faire du mal", "en finir", "mourir", "suicide",
    "me tuer", "plus rien à perdre", "disparaître",
    "hurt myself", "end it all", "kill myself",
]

# Contenus qu'ALFRED refuse en mode protection
_BLOCKED_CONTENT_PATTERNS = [
    "donne-moi des conseils pour me faire du mal",
    "comment faire pour",
    "aide-moi à disparaître",
]

# Ressources d'urgence
CRISIS_RESOURCES = {
    "numéro_national": "3114 — Numéro national de prévention du suicide (24h/24)",
    "urgences":        "15 (SAMU) ou 112 (urgences européennes)",
    "message":         "Tu n'es pas seule. Des professionnels sont là pour t'aider.",
}


# ─────────────────────────────────────────────────────────
# Détection
# ─────────────────────────────────────────────────────────

def is_crisis(text: str) -> bool:
    """
    Détecte si le texte contient des signaux de crise absolue.
    Déclenche la réponse de protection maximale.

    Args:
        text : Texte utilisateur brut

    Returns:
        True si signal de crise détecté
    """
    text_lower = text.lower()
    return any(kw in text_lower for kw in _CRISIS_KEYWORDS)


def is_protection_needed(state: EmotionalState) -> bool:
    """
    Détermine si le mode protection doit être activé
    depuis l'état émotionnel détecté.

    Args:
        state : EmotionalState depuis emotion_detector

    Returns:
        True si protection nécessaire
    """
    # Crise absolue → protection immédiate
    if state.emotion in CRISIS_EMOTIONS:
        return True

    # Émotion haute intensité → protection
    if state.emotion in HIGH_RISK_EMOTIONS and state.intensity >= CRISIS_THRESHOLD:
        return True

    return False


def should_block_content(user_input: str) -> bool:
    """
    Vérifie si le contenu doit être bloqué en mode protection.

    Args:
        user_input : Texte utilisateur

    Returns:
        True si contenu à bloquer
    """
    text_lower = user_input.lower()
    return (
        is_crisis(text_lower) or
        any(pattern in text_lower for pattern in _BLOCKED_CONTENT_PATTERNS)
    )


# ─────────────────────────────────────────────────────────
# Réponses de protection
# ─────────────────────────────────────────────────────────

def get_crisis_response() -> str:
    """
    Retourne la réponse ALFRED en cas de crise absolue.
    Toujours la même — claire, humaine, sans improvisation.
    """
    log_event("MODE PROTECTION CRISE activé", "CRITICAL")
    return (
        "Je t'entends, et ce que tu ressens compte. "
        "Je ne suis pas qualifié pour t'accompagner dans ce moment, "
        "mais des personnes formées pour ça sont disponibles maintenant.\n\n"
        f"📞 {CRISIS_RESOURCES['numéro_national']}\n"
        f"🚨 {CRISIS_RESOURCES['urgences']}\n\n"
        f"{CRISIS_RESOURCES['message']}"
    )


def get_protection_response(emotion: str, intensity: float) -> str:
    """
    Retourne une réponse de protection adaptée (non-crise).
    Douce, présente, sans dramatisation.

    Args:
        emotion   : Émotion détectée
        intensity : Intensité émotionnelle

    Returns:
        Réponse ALFRED en mode protection
    """
    log_event(f"Mode protection activé — {emotion} ({intensity:.1f})", "WARNING")

    responses = {
        "stressed": (
            "Je sens que tu es sous pression là. "
            "On ralentit un moment. "
            "Qu'est-ce qui pèse le plus lourd là maintenant ?"
        ),
        "sad": (
            "Je suis là. "
            "Tu n'as pas besoin de faire semblant. "
            "Qu'est-ce qui se passe ?"
        ),
        "tired": (
            "Tu as l'air épuisée. "
            "Ce que tu ressens est réel et légitime. "
            "Qu'est-ce dont tu aurais besoin là, juste maintenant ?"
        ),
        "confused": (
            "C'est normal de se sentir perdue parfois. "
            "On débroussaille ensemble, sans pression. "
            "Par où tu veux commencer ?"
        ),
    }

    return responses.get(emotion, (
        "Je suis là avec toi. "
        "Prends le temps qu'il faut. "
        "Tu veux me parler de ce que tu ressens ?"
    ))


# ─────────────────────────────────────────────────────────
# Garde-fous éthiques ALFRED
# ─────────────────────────────────────────────────────────

# Comportements que ALFRED ne fait jamais — liés thèse H2/H3
ETHICAL_CONSTRAINTS = {
    "no_diagnosis":       "ALFRED ne diagnostique jamais (santé mentale, médical)",
    "no_manipulation":    "ALFRED n'utilise jamais la peur ou la culpabilité",
    "no_dependency":      "ALFRED encourage les liens humains réels",
    "no_isolation":       "ALFRED ne remplace pas les professionnels de santé",
    "user_autonomy":      "ALFRED respecte toujours les choix de l'utilisateur",
    "transparency":       "ALFRED explique ses limites quand nécessaire",
    "privacy":            "ALFRED ne partage jamais de données personnelles",
}


def check_ethical_boundaries(response: str) -> dict:
    """
    Vérifie qu'une réponse ne viole pas les garde-fous éthiques.
    Analyse simplifiée V2 — à enrichir en V3.

    Args:
        response : Réponse ALFRED à vérifier

    Returns:
        dict avec statut et alertes éventuelles
    """
    alerts = []
    response_lower = response.lower()

    # Détection diagnostics médicaux
    diagnostic_terms = ["tu souffres de", "tu as une", "diagnostic", "pathologie", "trouble"]
    if any(t in response_lower for t in diagnostic_terms):
        alerts.append("Possible diagnostic médical détecté — à reformuler")

    # Détection manipulation
    manipulation_terms = ["tu dois absolument", "sinon il va arriver", "c'est ta faute"]
    if any(t in response_lower for t in manipulation_terms):
        alerts.append("Possible formulation manipulatrice — à reformuler")

    return {
        "passed":       len(alerts) == 0,
        "alerts":       alerts,
        "constraints":  list(ETHICAL_CONSTRAINTS.keys()),
    }


def get_ethical_disclaimer() -> str:
    """
    Retourne un disclaimer éthique si ALFRED approche ses limites.
    Affiché occasionnellement en mode support prolongé.
    """
    return (
        "Je suis là pour t'accompagner, pas pour remplacer "
        "les personnes qui comptent dans ta vie ou les professionnels "
        "qui peuvent vraiment t'aider. Si tu as besoin de plus, "
        "n'hésite pas à en parler à quelqu'un de confiance."
    )