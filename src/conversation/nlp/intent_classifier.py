"""
PROJECT      : ALFRED
BLOCK        : B01
FUNCTION     : 01.02
FILE         : src/conversation/nlp/intent_classifier.py
ROLE         : IntentNet — classification d'intention par mots-clés (règles)

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-06-03
UPDATED      : 2026-08-14
VERSION      : V1.1
STATUS       : VALIDATED

DESCRIPTION :
Classifieur d'intention niveau 0 (règles, pas de ML — principe de sobriété
cognitive, docs/architecture/vision_architecture_cognitive_alfred.md).
Les catégories reprennent le vocabulaire déjà consommé par
src/v3/fusion/multi_signal_fusion_engine.py::_INTENT_TO_MODE (greeting,
task, question, emotional_support, engineering) pour que l'intention
détectée influence réellement le mode ALFRED recommandé. Les listes de
mots-clés emotional_support/engineering reprennent celles déjà rédigées
dans config/intents_catalog.json (intent_emotional_support, intent_coding)
plutôt que d'en réinventer.
"""

class IntentClassifier:
    def __init__(self):
        self.rules = {
            "greeting": ["bonjour", "salut"],
            "task": ["rappelle", "planifie"],
            "question": ["quoi", "comment", "pourquoi"],
            "emotional_support": [
                "fatigu", "épuisé", "epuise", "découragé", "decourage",
                "j'en peux plus", "j'en ai marre", "marre", "à bout", "a bout",
                "stress", "panique", "submergé", "submerge", "vidée", "videe",
            ],
            "engineering": [
                "écris le fichier", "ecris le fichier", "corrige le bug",
                "debug", "développe le module", "developpe le module",
                "optimise le code", "crée le script", "cree le script",
            ],
        }

    def classify(self, text: str) -> str:
        text = text.lower()

        for intent, keywords in self.rules.items():
            if any(k in text for k in keywords):
                return intent

        return "fallback"
