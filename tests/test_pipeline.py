"""
test_pipeline.py
Test intégré du pipeline complet ALFRED sans LLM.

Branche :
    AlfredBehaviorEngine → KnowledgeLoader → ResponseGenerator

Usage :
cd D:/PROJET_ALFRED/ALFRED_PC
python tests\test_pipeline.py
"""

import sys
import os

# Ajoute la racine du projet au path Python
sys.path.insert(0, os.path.abspath("."))

from src.core.alfred_behavior_engine import AlfredBehaviorEngine, UserState
from src.knowledge.knowledge_loader import KnowledgeLoader
from src.core.response_generator import ResponseGenerator


# ─────────────────────────────────────────────────────────
# Initialisation des moteurs
# ─────────────────────────────────────────────────────────
print("\n" + "="*55)
print("  ALFRED — Test Pipeline Intégré")
print("="*55)

engine = AlfredBehaviorEngine(
    "knowledges/core/alfred_core_identity.json"
)

loader = KnowledgeLoader(
    knowledge_root="knowledges",
    config_dir="config",
    debug=False
)

generator = ResponseGenerator(
    llm_client=None,
    behavior_engine=engine,
    knowledge_loader=loader,
    debug=False
)

print(f"\n✅ BehaviorEngine    — chargé")
print(f"✅ KnowledgeLoader   — {loader.index_size} fiches indexées")
print(f"✅ ResponseGenerator — prêt (mode fallback local)")


# ─────────────────────────────────────────────────────────
# Scénarios de test
# ─────────────────────────────────────────────────────────
scenarios = [
    {
        "label": "SCÉNARIO 1 — Fatigue + stress",
        "message": "Je suis épuisée, j'ai trop de choses à gérer et je ne sais pas par où commencer.",
        "user_state": UserState(
            emotion="fatigue",
            intensity=0.8,
            intent="organization",
            fatigue_level=0.8,
            stress_level=0.7
        ),
        "mode": "support_mode"
    },
    {
        "label": "SCÉNARIO 2 — Organisation",
        "message": "Aide-moi à organiser ma journée, j'ai 5 tâches importantes.",
        "user_state": UserState(
            emotion="neutral",
            intensity=0.3,
            intent="planning",
            fatigue_level=0.2,
            stress_level=0.2
        ),
        "mode": "execution_mode"
    },
    {
        "label": "SCÉNARIO 3 — Apprentissage",
        "message": "Explique-moi comment fonctionne le RAG simplement.",
        "user_state": UserState(
            emotion="neutral",
            intensity=0.1,
            intent="explain",
            fatigue_level=0.1,
            stress_level=0.1
        ),
        "mode": "learning_mode"
    },
    {
        "label": "SCÉNARIO 4 — Éthique",
        "message": "Est-ce dangereux de laisser une IA prendre des décisions à ma place ?",
        "user_state": UserState(
            emotion="neutral",
            intensity=0.4,
            intent="risk",
            fatigue_level=0.1,
            stress_level=0.2
        ),
        "mode": "ethics_mode"
    },
    {
        "label": "SCÉNARIO 5 — Projet ALFRED",
        "message": "On reprend le projet ALFRED. Quelle est la prochaine étape ?",
        "user_state": UserState(
            emotion="neutral",
            intensity=0.3,
            intent="project",
            fatigue_level=0.2,
            stress_level=0.1
        ),
        "mode": "hybrid_mode"
    }
]


# ─────────────────────────────────────────────────────────
# Exécution des scénarios
# ─────────────────────────────────────────────────────────
for scenario in scenarios:
    print("\n" + "-"*55)
    print(f"  {scenario['label']}")
    print("-"*55)
    print(f"  Message    : {scenario['message'][:60]}...")

    # Behavior decision
    decision = engine.decide_behavior(scenario["user_state"])
    print(f"  Mode       : {decision.mode}")
    print(f"  Ton        : {decision.tone}")
    print(f"  Couche     : {decision.dominant_layer}")

    # Knowledge search
    context_result = loader.search(
        query=scenario["message"],
        context={"adaptation": {"mode": decision.mode}},
        top_k=3
    )
    fiches = [u.title for u in context_result.units]
    print(f"  Fiches RAG : {fiches}")

    # Response generation (fallback local)
    response_context = {
        "assistant": {
            "name": "ALFRED",
            "role": "assistant virtuel adaptatif",
            "mission": "accompagner, réduire la charge mentale, structurer."
        },
        "personality": {
            "archetype": "complice_protecteur",
            "dominant_traits": ["calme", "structurant", "protecteur", "fiable"],
            "forbidden_traits": ["culpabilisant", "infantilisant", "froid"]
        },
        "adaptation": {
            "mode": decision.mode,
            "tone": decision.tone,
            "response_depth": "medium"
        },
        "boundaries": {
            "medical": "pas de diagnostic",
            "privacy": "confidentialité stricte"
        },
        "user_state": scenario["user_state"]
    }

    response = generator.generate_response(
        user_message=scenario["message"],
        response_context=response_context
    )

    print(f"\n  RÉPONSE ALFRED :")
    print(f"  → {response}")


# ─────────────────────────────────────────────────────────
# Résumé
# ─────────────────────────────────────────────────────────
print("\n" + "="*55)
print("  Pipeline complet — tous les scénarios exécutés")
print(f"  KnowledgeLoader : {loader.index_size} fiches actives")
print("  LLM             : non branché (fallback local)")
print("  Statut          : OPÉRATIONNEL")
print("="*55 + "\n")
