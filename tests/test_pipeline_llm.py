"""
PROJECT      : ALFRED
BLOCK        : TESTS
FUNCTION     : XX.XX
FILE         : tests/test_pipeline_llm.py
ROLE         : TO_DEFINE

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-06-03
UPDATED      : 2026-06-03
VERSION      : V1.0
STATUS       : DRAFT

DESCRIPTION :
Suite de tests — description a completer.
"""

"""
test_pipeline_llm.py
Test du pipeline ALFRED avec LLM branché.
Tente Ollama en priorité (local), bascule sur OpenAI si absent.

Usage :
    cd D:/PROJET_ALFRED/ALFRED_PC
    python tests/test_pipeline_llm.py
"""

import sys
import os

sys.path.insert(0, os.path.abspath("."))

from src.core.alfred_behavior_engine import AlfredBehaviorEngine, UserState
from src.knowledge.knowledge_loader import KnowledgeLoader
from src.core.response_generator import ResponseGenerator


# ─────────────────────────────────────────────────────────
# Sélection automatique du client LLM
# ─────────────────────────────────────────────────────────
def get_llm_client():
    """Tente Ollama d'abord, bascule sur OpenAI sinon."""

    # Tentative Ollama (local, gratuit)
    try:
        from src.llm.llm_client_ollama import OllamaLLMClient
        client = OllamaLLMClient(model="llama3.2")
        if client.is_available():
            print("✅ LLM : Ollama (llama3.2) — local")
            return client
        else:
            print("⚠️  Ollama disponible mais modèle llama3.2 absent.")
            print("   Lance : ollama pull llama3.2")
    except Exception as e:
        print(f"⚠️  Ollama non disponible : {e}")

    # Tentative OpenAI (cloud)
    try:
        from src.llm.llm_client_openai import OpenAILLMClient
        client = OpenAILLMClient(model="gpt-4o-mini")
        print("✅ LLM : OpenAI (gpt-4o-mini)")
        return client
    except ValueError as e:
        print(f"⚠️  OpenAI non disponible : {e}")

    print("ℹ️  Aucun LLM disponible — mode fallback local activé.")
    return None


# ─────────────────────────────────────────────────────────
# Initialisation
# ─────────────────────────────────────────────────────────
print("\n" + "="*55)
print("  ALFRED — Test Pipeline avec LLM")
print("="*55 + "\n")

llm_client = get_llm_client()

engine = AlfredBehaviorEngine(
    "knowledges/core/alfred_core_identity.json"
)
loader = KnowledgeLoader(
    knowledge_root="knowledges",
    config_dir="config",
    debug=False
)
generator = ResponseGenerator(
    llm_client=llm_client,
    behavior_engine=engine,
    knowledge_loader=loader,
    debug=False
)

print(f"✅ BehaviorEngine  — chargé")
print(f"✅ KnowledgeLoader — {loader.index_size} fiches")
print(f"✅ LLM             — {'branché' if llm_client else 'fallback local'}")


# ─────────────────────────────────────────────────────────
# Scénario de test
# ─────────────────────────────────────────────────────────
test_cases = [
    {
        "message": "Je suis épuisée, j'ai trop de choses à gérer et je ne sais pas par où commencer.",
        "user_state": UserState(
            emotion="fatigue",
            intensity=0.8,
            intent="organization",
            fatigue_level=0.8,
            stress_level=0.7
        )
    },
    {
        "message": "Aide-moi à organiser ma journée, j'ai 5 tâches importantes.",
        "user_state": UserState(
            emotion="neutral",
            intensity=0.3,
            intent="planning",
            fatigue_level=0.2,
            stress_level=0.2
        )
    },
    {
        "message": "Explique-moi simplement ce qu'est le RAG.",
        "user_state": UserState(
            emotion="neutral",
            intensity=0.1,
            intent="explain",
            fatigue_level=0.1,
            stress_level=0.1
        )
    }
]

context_base = {
    "assistant": {
        "name": "ALFRED",
        "role": "assistant virtuel adaptatif",
        "mission": "accompagner, réduire la charge mentale, structurer."
    },
    "personality": {
        "archetype": "complice_protecteur",
        "dominant_traits": ["calme", "structurant", "protecteur", "fiable", "chaleureux"],
        "forbidden_traits": ["culpabilisant", "infantilisant", "froid", "robotique"]
    },
    "boundaries": {
        "medical": "pas de diagnostic, pas de remplacement professionnel",
        "privacy": "confidentialité stricte"
    }
}

for i, case in enumerate(test_cases, 1):
    decision = engine.decide_behavior(case["user_state"])
    context = {
        **context_base,
        "rag_top_k": 2,
        "adaptation": {
            "mode": decision.mode,
            "tone": decision.tone,
            "response_depth": "medium"
        },
        "user_state": case["user_state"]
    }

    print(f"\n{'─'*55}")
    print(f"  TEST {i} — Mode : {decision.mode} | Ton : {decision.tone}")
    print(f"  Message : {case['message'][:70]}...")
    print(f"{'─'*55}")

    response = generator.generate_response(
        user_message=case["message"],
        response_context=context
    )

    print(f"\nALFRED :\n{response}\n")

print("="*55)
print("  Tests terminés")
print("="*55 + "\n")
