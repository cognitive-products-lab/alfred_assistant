"""
PROJECT      : ALFRED
BLOCK        : B02
FUNCTION     : Rappel contextuel spontané (session 3, plan semaine 17-24/08/2026)
FILE         : tests/test_response_generator_contextual_recall.py
ROLE         : Vérifie que context["contextual_recall"] (produit par
               src.memory.memory_indexer.get_contextual_recall, appelé dans
               main.py) est bien injecté dans le prompt système — en mode
               normal et en mode recherche — sans jamais forcer le LLM à
               le mentionner.

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-08-17
VERSION      : V1.0
STATUS       : TESTED
"""

import sys
import os

sys.path.insert(0, os.path.abspath("."))

from src.core.response_generator import ResponseGenerator

_SAMPLE_RECALL = "Le 2026-08-11, il a été noté : « Décision de reprendre le projet ALFRED » (catégorie : decision)."


def test_recall_block_present_when_contextual_recall_given():
    gen = ResponseGenerator()
    prompt = gen._build_system_prompt(context={"contextual_recall": _SAMPLE_RECALL})
    assert "SOUVENIR PERTINENT" in prompt
    assert _SAMPLE_RECALL in prompt


def test_recall_block_absent_when_no_contextual_recall():
    gen = ResponseGenerator()
    prompt = gen._build_system_prompt(context={})
    assert "SOUVENIR PERTINENT" not in prompt


def test_recall_block_absent_when_contextual_recall_empty_string():
    gen = ResponseGenerator()
    prompt = gen._build_system_prompt(context={"contextual_recall": ""})
    assert "SOUVENIR PERTINENT" not in prompt


def test_recall_block_present_in_research_mode():
    gen = ResponseGenerator()
    prompt = gen._build_system_prompt(context={"contextual_recall": _SAMPLE_RECALL, "research_mode": True})
    assert "SOUVENIR PERTINENT" in prompt
    assert _SAMPLE_RECALL in prompt


def test_recall_instructs_discernment_not_obligation():
    gen = ResponseGenerator()
    prompt = gen._build_system_prompt(context={"contextual_recall": _SAMPLE_RECALL})
    assert "jamais comme une obligation" in prompt
    assert "tu l'ignores complètement" in prompt
