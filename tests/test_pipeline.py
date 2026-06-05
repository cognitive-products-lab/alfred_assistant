"""
PROJECT      : ALFRED
BLOCK        : TESTS
FUNCTION     : B01
FILE         : tests/test_pipeline.py
ROLE         : Tests pipeline complet ALFRED sans LLM

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-06-03
UPDATED      : 2026-06-05
VERSION      : V1.1
STATUS       : TESTED

DESCRIPTION :
Tests pytest du pipeline AlfredBehaviorEngine -> KnowledgeLoader -> ResponseGenerator.
Le script de démo complet est exécutable via : python tests/test_pipeline.py
"""

import sys
import os
import pytest

sys.path.insert(0, os.path.abspath("."))

from src.core.alfred_behavior_engine import AlfredBehaviorEngine, UserState
from src.knowledge.knowledge_loader import KnowledgeLoader
from src.core.response_generator import ResponseGenerator


# ─────────────────────────────────────────────────────────
# Fixtures
# ─────────────────────────────────────────────────────────

@pytest.fixture(scope="module")
def engine():
    return AlfredBehaviorEngine("knowledges/core/alfred_core_identity.json")


@pytest.fixture(scope="module")
def loader():
    return KnowledgeLoader(knowledge_root="knowledges", config_dir="config", debug=False)


@pytest.fixture(scope="module")
def generator(engine, loader):
    return ResponseGenerator(llm_client=None, behavior_engine=engine,
                              knowledge_loader=loader, debug=False)


# ─────────────────────────────────────────────────────────
# Tests pytest
# ─────────────────────────────────────────────────────────

def test_behavior_engine_loads(engine):
    assert engine is not None


def test_knowledge_loader_index(loader):
    assert loader.index_size > 0


def test_knowledge_loader_search(loader):
    result = loader.search("fatigue stress", top_k=3)
    assert hasattr(result, "units")
    assert isinstance(result.units, list)


def test_response_generator_instantiation(generator):
    assert generator is not None


def test_pipeline_scenario_support(engine, loader, generator):
    state = UserState(emotion="fatigue", intensity=0.8, intent="organization",
                      fatigue_level=0.8, stress_level=0.7)
    decision = engine.decide_behavior(state)
    assert decision.mode is not None
    result = loader.search("je suis épuisée", top_k=3)
    assert isinstance(result.units, list)


def test_pipeline_scenario_organisation(engine, loader, generator):
    state = UserState(emotion="neutral", intensity=0.3, intent="planning",
                      fatigue_level=0.2, stress_level=0.2)
    decision = engine.decide_behavior(state)
    assert decision.tone is not None


# ─────────────────────────────────────────────────────────
# Script de démo (exécution directe uniquement)
# ─────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("\n" + "="*55)
    print("  ALFRED — Test Pipeline Intégré")
    print("="*55)

    _engine = AlfredBehaviorEngine("knowledges/core/alfred_core_identity.json")
    _loader = KnowledgeLoader(knowledge_root="knowledges", config_dir="config", debug=False)
    _generator = ResponseGenerator(llm_client=None, behavior_engine=_engine,
                                   knowledge_loader=_loader, debug=False)

    print(f"\n✅ BehaviorEngine    — chargé")
    print(f"✅ KnowledgeLoader   — {_loader.index_size} fiches indexées")
    print(f"✅ ResponseGenerator — prêt (mode fallback local)")

    scenarios = [
        {"label": "SCÉNARIO 1 — Fatigue + stress",
         "message": "Je suis épuisée, j'ai trop de choses à gérer.",
         "user_state": UserState(emotion="fatigue", intensity=0.8, intent="organization",
                                 fatigue_level=0.8, stress_level=0.7), "mode": "support_mode"},
        {"label": "SCÉNARIO 2 — Organisation",
         "message": "Aide-moi à organiser ma journée, j'ai 5 tâches importantes.",
         "user_state": UserState(emotion="neutral", intensity=0.3, intent="planning",
                                 fatigue_level=0.2, stress_level=0.2), "mode": "execution_mode"},
    ]

    for scenario in scenarios:
        print(f"\n--- {scenario['label']} ---")
        decision = _engine.decide_behavior(scenario["user_state"])
        print(f"  Mode : {decision.mode} | Ton : {decision.tone}")
        result = _loader.search(scenario["message"], top_k=3)
        print(f"  RAG  : {[u.title for u in result.units]}")

    print("\n✅ Pipeline complet — OK")
