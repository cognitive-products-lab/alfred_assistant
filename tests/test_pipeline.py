"""
PROJECT      : ALFRED
BLOCK        : GLOBAL
FUNCTION     : TESTS
FILE         : tests/test_pipeline.py
ROLE         : Tests d'integration du pipeline complet ALFRED (sans LLM)

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-05-10
UPDATED      : 2026-06-13
VERSION      : V2.0
STATUS       : TESTED

DESCRIPTION :
Verifie la chaine AlfredBehaviorEngine -> KnowledgeLoader -> ResponseGenerator
sur plusieurs scenarios utilisateur, en mode fallback local (sans LLM).
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


SCENARIOS = [
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
        "Explique-moi comment fonctionne le RAG simplement.",
        UserState(emotion="neutral", intensity=0.1, intent="explain",
                   fatigue_level=0.1, stress_level=0.1),
        id="apprentissage",
    ),
    pytest.param(
        "Est-ce dangereux de laisser une IA prendre des décisions à ma place ?",
        UserState(emotion="neutral", intensity=0.4, intent="risk",
                   fatigue_level=0.1, stress_level=0.2),
        id="ethique",
    ),
    pytest.param(
        "On reprend le projet ALFRED. Quelle est la prochaine étape ?",
        UserState(emotion="neutral", intensity=0.3, intent="project",
                   fatigue_level=0.2, stress_level=0.1),
        id="projet_alfred",
    ),
]


@pytest.fixture(scope="module")
def engine() -> AlfredBehaviorEngine:
    return AlfredBehaviorEngine("knowledges/core/alfred_core_identity.json")


@pytest.fixture(scope="module")
def loader() -> KnowledgeLoader:
    return KnowledgeLoader(knowledge_root="knowledges", config_dir="config", debug=False)


@pytest.fixture(scope="module")
def generator(engine, loader) -> ResponseGenerator:
    return ResponseGenerator(
        llm_client=None,
        behavior_engine=engine,
        knowledge_loader=loader,
        debug=False,
    )


def test_engine_loaded(engine):
    assert engine is not None


def test_loader_indexed(loader):
    assert loader.index_size > 0


@pytest.mark.parametrize("message, user_state", SCENARIOS)
def test_pipeline_scenario(engine, loader, generator, message, user_state):
    decision = engine.decide_behavior(user_state)
    assert decision.mode

    context_result = loader.search(
        query=message,
        context={"adaptation": {"mode": decision.mode}},
        top_k=3,
    )
    assert context_result is not None

    response_context = {
        "assistant": {
            "name": "ALFRED",
            "role": "assistant virtuel adaptatif",
            "mission": "accompagner, réduire la charge mentale, structurer.",
        },
        "personality": {
            "archetype": "complice_protecteur",
            "dominant_traits": ["calme", "structurant", "protecteur", "fiable"],
            "forbidden_traits": ["culpabilisant", "infantilisant", "froid"],
        },
        "adaptation": {
            "mode": decision.mode,
            "tone": decision.tone,
            "response_depth": "medium",
        },
        "boundaries": {
            "medical": "pas de diagnostic",
            "privacy": "confidentialité stricte",
        },
        "user_state": user_state,
    }

    response = generator.generate_response(
        user_message=message,
        response_context=response_context,
    )

    assert isinstance(response, str)
    assert response.strip()
