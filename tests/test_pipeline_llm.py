"""
PROJECT      : ALFRED
BLOCK        : GLOBAL
FUNCTION     : TESTS
FILE         : tests/test_pipeline_llm.py
ROLE         : Tests d'integration du pipeline ALFRED avec LLM branche

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-05-10
UPDATED      : 2026-06-13
VERSION      : V2.0
STATUS       : ACTIVE

DESCRIPTION :
Verifie la chaine AlfredBehaviorEngine -> KnowledgeLoader -> ResponseGenerator
avec un LLM Ollama reellement branche. Ignore (skip) si Ollama / le modele
ne sont pas disponibles. Test lent (appels LLM reels) -> groupe "slow",
exclu par tests/run_all_tests.py --fast.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.core.alfred_behavior_engine import AlfredBehaviorEngine, UserState
from src.core.response_generator import ResponseGenerator
from src.knowledge.knowledge_loader import KnowledgeLoader
from src.llm.llm_client_ollama import OllamaLLMClient


TEST_CASES = [
    pytest.param(
        "Je suis épuisée, j'ai trop de choses à gérer et je ne sais pas par où commencer.",
        UserState(emotion="fatigue", intensity=0.8, intent="organization",
                   fatigue_level=0.8, stress_level=0.7),
        id="fatigue_stress",
    ),
    pytest.param(
        "Aide-moi à organiser ma journée, j'ai 5 tâches importantes.",
        UserState(emotion="neutral", intensity=0.3, intent="planning",
                   fatigue_level=0.2, stress_level=0.2),
        id="organisation",
    ),
    pytest.param(
        "Explique-moi simplement ce qu'est le RAG.",
        UserState(emotion="neutral", intensity=0.1, intent="explain",
                   fatigue_level=0.1, stress_level=0.1),
        id="explication_rag",
    ),
]


@pytest.fixture(scope="module")
def llm_client():
    client = OllamaLLMClient(model="llama3.2", stream=False)
    if not client.is_available():
        pytest.skip("Ollama indisponible ou modèle llama3.2 absent")
    return client


@pytest.fixture(scope="module")
def engine() -> AlfredBehaviorEngine:
    return AlfredBehaviorEngine("knowledges/core/alfred_core_identity.json")


@pytest.fixture(scope="module")
def loader() -> KnowledgeLoader:
    return KnowledgeLoader(knowledge_root="knowledges", config_dir="config", debug=False)


@pytest.fixture(scope="module")
def generator(llm_client, engine, loader) -> ResponseGenerator:
    return ResponseGenerator(
        llm_client=llm_client,
        behavior_engine=engine,
        knowledge_loader=loader,
        debug=False,
    )


@pytest.mark.parametrize("message, user_state", TEST_CASES)
def test_pipeline_llm_case(engine, generator, message, user_state):
    decision = engine.decide_behavior(user_state)
    assert decision.mode

    response_context = {
        "assistant": {
            "name": "ALFRED",
            "role": "assistant virtuel adaptatif",
            "mission": "accompagner, réduire la charge mentale, structurer.",
        },
        "personality": {
            "archetype": "complice_protecteur",
            "dominant_traits": ["calme", "structurant", "protecteur", "fiable", "chaleureux"],
            "forbidden_traits": ["culpabilisant", "infantilisant", "froid", "robotique"],
        },
        "boundaries": {
            "medical": "pas de diagnostic, pas de remplacement professionnel",
            "privacy": "confidentialité stricte",
        },
        "rag_top_k": 2,
        "adaptation": {
            "mode": decision.mode,
            "tone": decision.tone,
            "response_depth": "medium",
        },
        "user_state": user_state,
    }

    response = generator.generate_response(
        user_message=message,
        response_context=response_context,
    )

    assert isinstance(response, str)
    assert response.strip()
