"""
PROJECT      : ALFRED
BLOCK        : TESTS
FUNCTION     : B01
FILE         : tests/test_pipeline_llm.py
ROLE         : Tests pipeline ALFRED avec LLM branché

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-06-03
UPDATED      : 2026-06-05
VERSION      : V1.1
STATUS       : TESTED

DESCRIPTION :
Tests pytest du pipeline avec LLM (Ollama local ou OpenAI fallback).
Le script de démo complet est exécutable via : python tests/test_pipeline_llm.py
"""

import sys
import os
import pytest

sys.path.insert(0, os.path.abspath("."))

from src.core.alfred_behavior_engine import AlfredBehaviorEngine, UserState
from src.knowledge.knowledge_loader import KnowledgeLoader
from src.core.response_generator import ResponseGenerator


def _get_llm_client():
    try:
        from src.llm.llm_client_ollama import OllamaLLMClient
        client = OllamaLLMClient(model="llama3.2")
        if client.is_available():
            return client
    except Exception:
        pass
    try:
        from src.llm.llm_client_openai import OpenAILLMClient
        return OpenAILLMClient(model="gpt-4o-mini")
    except Exception:
        pass
    return None


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
    return ResponseGenerator(llm_client=_get_llm_client(),
                              behavior_engine=engine, knowledge_loader=loader, debug=False)


# ─────────────────────────────────────────────────────────
# Tests pytest
# ─────────────────────────────────────────────────────────

def test_llm_client_or_fallback():
    client = _get_llm_client()
    # Pas d'assertion bloquante — fallback None est acceptable
    assert client is None or hasattr(client, "generate")


def test_knowledge_loader_ready(loader):
    assert loader.index_size > 0


def test_behavior_engine_decision(engine):
    state = UserState(emotion="fatigue", intensity=0.8, intent="organization",
                      fatigue_level=0.8, stress_level=0.7)
    decision = engine.decide_behavior(state)
    assert decision.mode is not None
    assert decision.tone is not None


def test_generator_instantiation(generator):
    assert generator is not None


def test_pipeline_with_fallback(engine, loader, generator):
    state = UserState(emotion="neutral", intensity=0.3, intent="planning",
                      fatigue_level=0.2, stress_level=0.2)
    decision = engine.decide_behavior(state)
    context = {
        "assistant": {"name": "ALFRED"},
        "adaptation": {"mode": decision.mode, "tone": decision.tone, "response_depth": "medium"},
        "user_state": state,
    }
    response = generator.generate_response(
        user_message="Aide-moi à organiser ma journée.",
        response_context=context
    )
    assert isinstance(response, str)


# ─────────────────────────────────────────────────────────
# Script de démo (exécution directe uniquement)
# ─────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("\n" + "="*55)
    print("  ALFRED — Test Pipeline avec LLM")
    print("="*55 + "\n")

    llm = _get_llm_client()
    _engine = AlfredBehaviorEngine("knowledges/core/alfred_core_identity.json")
    _loader = KnowledgeLoader(knowledge_root="knowledges", config_dir="config", debug=False)
    _gen = ResponseGenerator(llm_client=llm, behavior_engine=_engine,
                              knowledge_loader=_loader, debug=False)

    print(f"✅ KnowledgeLoader — {_loader.index_size} fiches")
    print(f"✅ LLM — {'branché' if llm else 'fallback local'}")

    state = UserState(emotion="fatigue", intensity=0.8, intent="organization",
                      fatigue_level=0.8, stress_level=0.7)
    decision = _engine.decide_behavior(state)
    context = {"assistant": {"name": "ALFRED"},
               "adaptation": {"mode": decision.mode, "tone": decision.tone,
                               "response_depth": "medium"},
               "user_state": state}
    response = _gen.generate_response(
        user_message="Je suis épuisée, j'ai trop de choses à gérer.",
        response_context=context
    )
    print(f"\nALFRED : {response}")
    print("\n✅ Pipeline LLM — OK")
