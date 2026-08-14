"""
════════════════════════════════════════════════════════════
PROJECT      : ALFRED
BLOCK        : B01
FUNCTION     : 01.02
FILE         : test_intent_net_wiring.py
ROLE         : Tests du câblage IntentNet dans le pipeline conversationnel

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-08-14
UPDATED      : 2026-08-14
VERSION      : V1.0
STATUS       : ACTIVE

DESCRIPTION :
Avant ce chantier, src/conversation/nlp/nlp_engine_v2.py::analyze_v2()
retournait un intent hardcodé à "conversation" quel que soit le texte —
IntentClassifier (src/conversation/nlp/intent_classifier.py) existait mais
n'était jamais appelé. Vérifie que analyze_v2() délègue maintenant
réellement à IntentClassifier, que la confiance reflète un match réel vs
un fallback, et que les catégories produites recoupent le vocabulaire déjà
consommé par src/v3/fusion/multi_signal_fusion_engine.py::_INTENT_TO_MODE
(greeting, task, question, emotional_support, engineering) — sinon
l'intention détectée n'aurait toujours aucun effet sur le mode ALFRED
recommandé.
════════════════════════════════════════════════════════════
"""

from src.conversation.nlp.nlp_engine_v2 import analyze_v2
from src.conversation.nlp.intent_classifier import IntentClassifier
from src.v3.fusion.multi_signal_fusion_engine import _INTENT_TO_MODE


def test_analyze_v2_no_longer_hardcodes_conversation():
    result = analyze_v2("écris le fichier Python pour corriger le bug")

    assert result["intent"] == "engineering"


def test_analyze_v2_confidence_high_on_match_low_on_fallback():
    matched = analyze_v2("bonjour, comment vas-tu ?")
    unmatched = analyze_v2("azerty qwerty ipsum lorem sans rien de particulier")

    assert matched["confidence"] > unmatched["confidence"]
    assert unmatched["intent"] == "fallback"


def test_intent_categories_are_known_to_fusion_engine():
    clf = IntentClassifier()
    for category in clf.rules:
        assert category in _INTENT_TO_MODE, (
            f"'{category}' n'a pas d'entrée dans _INTENT_TO_MODE : "
            "l'intention détectée n'influencera jamais le mode ALFRED recommandé."
        )


def test_task_and_greeting_still_detected_end_to_end():
    assert analyze_v2("rappelle-moi d'appeler")["intent"] == "task"
    assert analyze_v2("bonjour Alfred")["intent"] == "greeting"
