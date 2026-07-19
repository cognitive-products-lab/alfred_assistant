# ============================================================
# ALFRED — src/conversation/nlp/nlp_engine.py
# Bloc 01.02 — Compréhension des intentions
#
# 📚 NOTION EXAM :
#   D12-2 — Capsule 2 : Détection d'intention par règles et mots-clés
#
# 🎯 UTILITÉ ALFRED :
#   Moteur NLP V1 — détecte l'intention (intent), extrait les entités
#   NER basiques et gère le fallback si aucune intention reconnue.
#
# 🏗️ DOMAINE :
#   Noyau conversationnel — NLP règles V1, stub STT → Whisper V3
#
# STATUS  : VALIDATED
# ============================================================

import re
from datetime import datetime

# ── Catalogue d'intentions ─────────────────────────────────
# Structure : intent_id → (mots-clés FR, mots-clés EN, priorité)
_INTENT_CATALOG: dict[str, dict] = {
    "organization": {
        "keywords_fr": ["organiser", "planning", "tâche", "priorité", "agenda",
                        "rappel", "todo", "liste", "planifier", "gérer"],
        "keywords_en": ["organize", "task", "priority", "schedule", "remind",
                        "todo", "list", "plan", "manage"],
        "priority": 2,
    },
    "emotional_support": {
        "keywords_fr": ["perdue", "stressée", "fatiguée", "mal", "triste",
                        "anxieuse", "overwhelmed", "débordée", "épuisée",
                        "inquiète", "peur", "angoisse", "difficile"],
        "keywords_en": ["stressed", "tired", "sad", "anxious", "overwhelmed",
                        "exhausted", "worried", "afraid", "hard", "difficult"],
        "priority": 3,  # Priorité haute — émotion avant tout
    },
    "wellbeing": {
        "keywords_fr": ["bien-être", "santé", "repos", "dormir", "sommeil",
                        "exercice", "manger", "énergie", "pause", "respirer"],
        "keywords_en": ["wellbeing", "health", "rest", "sleep", "exercise",
                        "eat", "energy", "break", "breathe"],
        "priority": 2,
    },
    "knowledge_request": {
        "keywords_fr": ["explique", "comment", "qu'est-ce", "pourquoi",
                        "définition", "aide-moi à comprendre", "dis-moi",
                        "c'est quoi", "apprendre", "formation"],
        "keywords_en": ["explain", "how", "what is", "why", "definition",
                        "help me understand", "tell me", "learn", "training"],
        "priority": 1,
    },
    "product_knowledge": {
        "keywords_fr": ["product management", "produit", "roadmap", "feature",
                        "backlog", "sprint", "user story", "kpi", "métrique",
                        "stratégie produit"],
        "keywords_en": ["product", "roadmap", "feature", "backlog", "sprint",
                        "user story", "kpi", "metric", "product strategy"],
        "priority": 1,
    },
    "engineering": {
        "keywords_fr": ["python", "code", "bug", "erreur", "fonction", "classe",
                        "module", "script", "développement", "programmer",
                        "algorithme", "base de données", "sql", "java"],
        "keywords_en": ["python", "code", "bug", "error", "function", "class",
                        "module", "script", "development", "algorithm",
                        "database", "sql", "java"],
        "priority": 1,
    },
    "home_automation": {
        "keywords_fr": ["lumière", "allume", "éteins", "chauffage", "musique",
                        "thermostat", "volet", "alarme", "domotique", "maison"],
        "keywords_en": ["light", "turn on", "turn off", "heating", "music",
                        "thermostat", "shutter", "alarm", "automation", "home"],
        "priority": 2,
    },
    "greeting": {
        "keywords_fr": ["bonjour", "salut", "hello", "bonsoir", "coucou",
                        "hey alfred", "alfred"],
        "keywords_en": ["hello", "hi", "good morning", "hey", "good evening"],
        "priority": 0,
    },
    "general": {
        "keywords_fr": [],
        "keywords_en": [],
        "priority": -1,  # Fallback
    },
}


# ─────────────────────────────────────────────────────────
# API publique
# ─────────────────────────────────────────────────────────

def detect_intent(user_input: str) -> dict:
    """
    Détecte l'intention principale dans le message utilisateur.

    Méthode V1 : correspondance par mots-clés avec score et priorité.
    V2 : remplacée par classification LLM local.

    Args:
        user_input : Texte nettoyé de l'utilisateur

    Returns:
        dict avec :
            intent    : identifiant intention détectée
            score     : nombre de mots-clés matchés
            priority  : niveau de priorité de l'intention
            method    : "keyword_v1" (remplacé par "llm_v2" plus tard)
    """
    text = user_input.lower().strip()
    best_intent = "general"
    best_score = 0
    best_priority = -1

    for intent_id, config in _INTENT_CATALOG.items():
        if intent_id == "general":
            continue

        all_keywords = config["keywords_fr"] + config["keywords_en"]
        score = sum(1 for kw in all_keywords if kw in text)

        if score == 0:
            continue

        # Priorité à l'intention avec le meilleur score,
        # puis à la priorité la plus haute en cas d'égalité
        if score > best_score or (score == best_score and config["priority"] > best_priority):
            best_score = score
            best_intent = intent_id
            best_priority = config["priority"]

    return {
        "intent":   best_intent,
        "score":    best_score,
        "priority": best_priority,
        "method":   "keyword_v1",
    }


def extract_entities(user_input: str) -> dict:
    """
    Extraction basique d'entités nommées (NER V1).

    Entités extraites :
        - dates    : aujourd'hui, demain, lundi, ...
        - times    : heures au format HHh, HH:MM
        - numbers  : nombres isolés

    V2+ : remplacé par spaCy ou LLM local.

    Args:
        user_input : Texte de l'utilisateur

    Returns:
        dict avec les entités trouvées
    """
    text = user_input.lower()
    entities: dict = {}

    # ── Dates relatives ──────────────────────────────────
    date_patterns = {
        "aujourd'hui": r"\baujourd'hui\b",
        "demain":      r"\bdemain\b",
        "hier":        r"\bhier\b",
        "lundi":       r"\blundi\b",
        "mardi":       r"\bmardi\b",
        "mercredi":    r"\bmercredi\b",
        "jeudi":       r"\bjeudi\b",
        "vendredi":    r"\bvendredi\b",
        "samedi":      r"\bsamedi\b",
        "dimanche":    r"\bdimanche\b",
        "cette semaine": r"\bcette semaine\b",
        "ce soir":     r"\bce soir\b",
        "ce matin":    r"\bce matin\b",
    }
    found_dates = [label for label, pattern in date_patterns.items()
                   if re.search(pattern, text)]
    if found_dates:
        entities["dates"] = found_dates

    # ── Heures ──────────────────────────────────────────
    time_matches = re.findall(r'\b(\d{1,2})[h:](\d{0,2})\b', text)
    if time_matches:
        entities["times"] = [f"{h}h{m if m else '00'}" for h, m in time_matches]

    # ── Nombres ─────────────────────────────────────────
    numbers = re.findall(r'\b\d+\b', text)
    if numbers:
        entities["numbers"] = [int(n) for n in numbers]

    return entities


def analyze(user_input: str) -> dict:
    """
    Point d'entrée principal NLP — agrège intent + entités.

    Args:
        user_input : Texte nettoyé de l'utilisateur

    Returns:
        dict complet avec intent, score, entities, timestamp
    """
    intent_result = detect_intent(user_input)
    entities      = extract_entities(user_input)

    return {
        "raw_input": user_input,
        "intent":    intent_result["intent"],
        "score":     intent_result["score"],
        "priority":  intent_result["priority"],
        "entities":  entities,
        "method":    intent_result["method"],
        "timestamp": datetime.now().isoformat(),
    }


def get_intent_label(intent_id: str) -> str:
    """Retourne un label lisible pour l'intention."""
    labels = {
        "organization":      "Organisation & planification",
        "emotional_support": "Soutien émotionnel",
        "wellbeing":         "Bien-être",
        "knowledge_request": "Demande d'information",
        "product_knowledge": "Product management",
        "engineering":       "Développement & code",
        "home_automation":   "Domotique",
        "greeting":          "Salutation",
        "general":           "Général",
    }
    return labels.get(intent_id, intent_id)
