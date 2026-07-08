"""
PROJECT      : ALFRED
BLOCK        : B01
FUNCTION     : 01.03
FILE         : src/input/nlp_engine.py
ROLE         : NLP engine — détection intent, entités, analyse complète

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-06-05
UPDATED      : 2026-06-05
VERSION      : V1.2
STATUS       : VALIDATED
"""

from __future__ import annotations

from datetime import datetime
import re

# Catalogue d'intents — noms alignés sur les tests
_INTENT_CATALOG: dict[str, list[str]] = {
    "greeting":          ["bonjour", "salut", "bonsoir", "coucou", "hey", "hello", "bonne nuit"],
    "farewell":          ["au revoir", "bye", "à bientôt", "ciao"],
    "emotional_support": ["fatiguée", "fatigue", "stressée", "stress", "épuisé", "anxieux", "débordée", "débordé"],
    "organization":      ["organiser", "planning", "agenda", "calendrier", "réunion", "rendez-vous", "tâche", "semaine"],
    "engineering":       ["bug", "code", "python", "erreur", "programme", "script", "développement", "debug"],
    "reminder":          ["rappel", "rappelle", "reminder", "n'oublie pas", "souviens"],
    "weather":           ["météo", "temps", "pluie", "soleil", "température"],
    "music":             ["musique", "chanson", "joue", "écoute"],
    "information":       ["quoi", "qui", "quand", "où", "comment", "pourquoi", "explique"],
    "project":           ["projet", "travail", "faire", "terminer", "finir"],
    "general":           [],
}

_DATE_KEYWORDS = ["cette semaine", "ce matin", "ce soir", "ce midi",
                  "lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche",
                  "demain", "aujourd'hui", "hier", "matin", "soir", "midi", "nuit"]


def get_intent_label(intent_key: str) -> str:
    labels = {
        "aide": "Demande d'aide", "rappel": "Rappel", "agenda": "Agenda",
        "meteo": "Météo", "musique": "Musique", "information": "Demande d'information",
        "salutation": "Salutation", "au_revoir": "Au revoir", "etat": "État émotionnel",
        "projet": "Projet / tâche", "general": "Général",
    }
    return labels.get(intent_key, intent_key)


def detect_intent(text: str) -> dict:
    """Détecte l'intent principal — retourne un dict {intent, score, label}."""
    text_lower = text.lower()
    for intent, keywords in _INTENT_CATALOG.items():
        if intent == "general":
            continue
        if any(kw in text_lower for kw in keywords):
            return {"intent": intent, "score": 0.8, "label": get_intent_label(intent)}
    return {"intent": "general", "score": 0.3, "label": get_intent_label("general")}


def extract_entities(text: str) -> dict:
    """Extrait les entités — retourne un dict {dates, times, numbers}."""
    text_lower = text.lower()
    dates = [kw for kw in _DATE_KEYWORDS if kw in text_lower]
    times = re.findall(r"\b\d{1,2}h\d{0,2}\b", text, re.IGNORECASE)
    numbers = [int(n) for n in re.findall(r"\b\d+\b", text)]
    return {"dates": dates, "times": times, "numbers": numbers}


def analyze(text: str) -> dict:
    """Analyse NLP complète."""
    intent_result = detect_intent(text)
    return {
        "text": text,
        "intent": intent_result["intent"],
        "intent_score": intent_result["score"],
        "entities": extract_entities(text),
        "timestamp": datetime.now().isoformat(),
        "language": "fr",
        "method": "keyword_v1",
    }
