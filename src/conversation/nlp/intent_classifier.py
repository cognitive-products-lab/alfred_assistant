"""
PROJECT      : ALFRED
BLOCK        : B01
FUNCTION     : XX.XX
FILE         : src/conversation/nlp/intent_classifier.py
ROLE         : TO_DEFINE

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-06-03
UPDATED      : 2026-06-03
VERSION      : V1.0
STATUS       : DRAFT

DESCRIPTION :
NLP & Traitement langage — description a completer.
"""

class IntentClassifier:
    def __init__(self):
        self.rules = {
            "greeting": ["bonjour", "salut"],
            "task": ["rappelle", "planifie"],
            "question": ["quoi", "comment", "pourquoi"]
        }

    def classify(self, text: str) -> str:
        text = text.lower()

        for intent, keywords in self.rules.items():
            if any(k in text for k in keywords):
                return intent

        return "fallback"
