"""
PROJECT      : ALFRED
BLOCK        : TESTS
FUNCTION     : B11
FILE         : tests/test_response_generator_time_context.py
ROLE         : Tests injection du contexte temporel réel dans le prompt système

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-07-23
UPDATED      : 2026-07-23
VERSION      : V1.0
STATUS       : TESTED

DESCRIPTION :
Vérifie que _build_system_prompt()/_build_research_system_prompt() injectent
bien la date/heure réelle (context["time"], produit par
context_builder.get_time_context()) dans le prompt envoyé au LLM — sans ça,
le LLM n'a aucune base pour répondre à "quelle heure est-il ?" et le dit
honnêtement (comportement observé en usage réel le 23/07/2026).
"""

import sys
import os

sys.path.insert(0, os.path.abspath("."))

from src.core.response_generator import ResponseGenerator

_SAMPLE_TIME = {
    "datetime": "2026-07-23T10:14:00+02:00",
    "time": "10:14",
    "date": "jeudi 23 juillet 2026",
    "day_of_week": "jeudi",
    "period": "matin",
    "greeting": "Bonjour",
    "energy_level": "high",
    "is_weekend": False,
    "hour": 10,
}


def test_time_block_present_when_time_context_given():
    gen = ResponseGenerator()
    prompt = gen._build_system_prompt(context={"time": _SAMPLE_TIME})
    assert "CONTEXTE TEMPOREL RÉEL" in prompt
    assert "jeudi 23 juillet 2026" in prompt
    assert "10:14" in prompt


def test_no_time_block_when_time_context_absent():
    gen = ResponseGenerator()
    prompt = gen._build_system_prompt(context={})
    assert "CONTEXTE TEMPOREL RÉEL" not in prompt


def test_time_block_present_in_research_mode():
    gen = ResponseGenerator()
    prompt = gen._build_system_prompt(context={"time": _SAMPLE_TIME, "research_mode": True})
    assert "CONTEXTE TEMPOREL RÉEL" in prompt
    assert "10:14" in prompt


def test_time_block_instructs_no_denial():
    gen = ResponseGenerator()
    prompt = gen._build_system_prompt(context={"time": _SAMPLE_TIME, "user": {"preferred_name": "Céline"}})
    assert "ne dis jamais que tu n'y as pas accès" in prompt
