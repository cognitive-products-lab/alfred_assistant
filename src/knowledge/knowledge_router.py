# ============================================================
# ALFRED — src/knowledge/knowledge_router.py
# Bloc 18.10 — Base métier & expertise
#
# 📚 NOTION EXAM :
#   D22-2 — Capsule 5 : Routage des knowledges — architecture legacy
#
# 🎯 UTILITÉ ALFRED :
#   DÉPRÉCIÉ — routeur legacy conservé pour historique.
#   Remplacé par domain_matcher, taxonomy_router, retrieval_engine.
#
# 🏗️ DOMAINE :
#   Base de connaissances — routage Bloc 18, pipeline B18 V3+
# ============================================================

"""
DEPRECATED — Legacy knowledge router.

Ce fichier est conservé temporairement pour historique.
Il ne doit plus être utilisé dans le pipeline B18.

Remplacé par :
- domain_matcher.py
- taxonomy_router.py
- knowledge_ranker.py
- retrieval_engine.py
"""
# ARBORESCENCE SUPPORTÉE :
#   knowledges/
#   ├── core/           Identité, modes, règles, éthique
#   ├── user/           Profil, adaptation, contexte, feedback
#   ├── softskills/     17 soft skills
#   ├── reasoning/      8 modules de raisonnement
#   ├── memory/         7 modules mémoire
#   ├── psychology/     7 modules psychologie
#   └── cpl/
#       ├── strategy/           Stratégie, valeur, business model
#       ├── ethics_governance/  Éthique IA, gouvernance, accessibilité
#       ├── human_communication/ Communication, client, EI
#       ├── human_organization/ Énergie, charge mentale
#       ├── execution/          Décision, projet, risque, tâches
#       ├── business_piloting/  Pricing, rentabilité, revenus
#       └── product_ia/         Produit, besoins, tech
#
# VERSION : 2.0.0 — refonte complète sur nouvelle arborescence
# ============================================================

import json
from pathlib import Path
from typing import Union

from paths import PATHS


# ─────────────────────────────────────────────────────────
# Loader de base
# ─────────────────────────────────────────────────────────

def _load(path: Path) -> dict:
    """Charge un fichier JSON knowledge. Retourne {} si absent."""
    if not path.exists():
        return {"error": f"Knowledge non trouvé : {path}", "summary": "", "concepts": []}
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def _load_multi(*paths: Path) -> list[dict]:
    """Charge plusieurs knowledges et retourne la liste."""
    return [_load(p) for p in paths]


# ─────────────────────────────────────────────────────────
# Routes principales — intent → fichier(s)
# ─────────────────────────────────────────────────────────

# Table de routage : intent_name → liste de Path
_ROUTES: dict[str, list[Path]] = {

    # ── Soutien émotionnel ──────────────────────────────
    "emotional_support": [
        PATHS.knowledge_softskills    / "emotional_management.json",
        PATHS.knowledge_psychology    / "emotional_patterns.json",
        PATHS.knowledge_psychology    / "burnout_prevention.json",
    ],

    # ── Fatigue / surcharge ─────────────────────────────
    "fatigue_support": [
        PATHS.knowledge_cpl_human_org / "energy_management.json",
        PATHS.knowledge_psychology    / "cognitive_load.json",
        PATHS.knowledge_psychology    / "decision_fatigue.json",
    ],

    # ── Stress ──────────────────────────────────────────
    "stress_support": [
        PATHS.knowledge_cpl_human_org / "energy_management.json",
        PATHS.knowledge_cpl_human_com / "emotional_intelligence.json",
        PATHS.knowledge_softskills    / "resilience.json",
    ],

    # ── Organisation / productivité ─────────────────────
    "organization": [
        PATHS.knowledge_softskills    / "organization.json",
        PATHS.knowledge_cpl_execution / "task_prioritization.json",
        PATHS.knowledge_softskills    / "focus_management.json",
    ],

    # ── Décision ────────────────────────────────────────
    "decision": [
        PATHS.knowledge_cpl_execution / "decision_making_framework.json",
        PATHS.knowledge_reasoning     / "decision_models.json",
        PATHS.knowledge_reasoning     / "tradeoff_analysis.json",
    ],

    # ── Résolution de problèmes ─────────────────────────
    "problem_solving": [
        PATHS.knowledge_softskills    / "problem_solving.json",
        PATHS.knowledge_reasoning     / "root_cause_analysis.json",
        PATHS.knowledge_reasoning     / "reasoning_engine.json",
    ],

    # ── Raisonnement complexe ───────────────────────────
    "reasoning": [
        PATHS.knowledge_reasoning     / "reasoning_engine.json",
        PATHS.knowledge_reasoning     / "multi_step_reasoning.json",
        PATHS.knowledge_reasoning     / "reasoning_advanced.json",
    ],

    # ── Mémoire ─────────────────────────────────────────
    "memory": [
        PATHS.knowledge_memory        / "memory_system.json",
        PATHS.knowledge_memory        / "episodic_memory.json",
        PATHS.knowledge_memory        / "semantic_memory.json",
    ],

    # ── Communication ───────────────────────────────────
    "communication": [
        PATHS.knowledge_cpl_human_com / "communication_principles.json",
        PATHS.knowledge_softskills    / "communication_clarity.json",
        PATHS.knowledge_softskills    / "active_listening.json",
    ],

    # ── Relation client ─────────────────────────────────
    "client_interaction": [
        PATHS.knowledge_cpl_human_com / "client_interaction.json",
        PATHS.knowledge_cpl_human_com / "communication_principles.json",
        PATHS.knowledge_softskills    / "assertiveness.json",
    ],

    # ── Stratégie & vision ──────────────────────────────
    "strategy_vision": [
        PATHS.knowledge_cpl_strategy  / "strategy_fundamentals.json",
        PATHS.knowledge_cpl_strategy  / "value_proposition_framework.json",
        PATHS.knowledge_cpl_strategy  / "business_model_design.json",
    ],

    # ── Business model ──────────────────────────────────
    "business_model": [
        PATHS.knowledge_cpl_strategy  / "business_model_design.json",
        PATHS.knowledge_cpl_business  / "pricing_strategy.json",
        PATHS.knowledge_cpl_business  / "revenue_mix_strategy.json",
    ],

    # ── Rentabilité / finance ───────────────────────────
    "profitability": [
        PATHS.knowledge_cpl_business  / "profitability_analysis.json",
        PATHS.knowledge_cpl_business  / "pricing_strategy.json",
        PATHS.knowledge_cpl_strategy  / "business_model_design.json",
    ],

    # ── Éthique & gouvernance ───────────────────────────
    "ethics_governance": [
        PATHS.knowledge_cpl_ethics    / "ethical_ai_framework.json",
        PATHS.knowledge_cpl_ethics    / "governance_model.json",
        PATHS.knowledge_cpl_ethics    / "accessibility_principles.json",
    ],

    # ── Conception produit ──────────────────────────────
    "product_design": [
        PATHS.knowledge_cpl_product   / "product_design_methodology.json",
        PATHS.knowledge_cpl_product   / "user_needs_analysis.json",
        PATHS.knowledge_cpl_product   / "tech_tradeoff_framework.json",
    ],

    # ── Risque & projet ─────────────────────────────────
    "risk": [
        PATHS.knowledge_cpl_execution / "risk_management.json",
        PATHS.knowledge_cpl_execution / "project_management_core.json",
        PATHS.knowledge_cpl_product   / "tech_tradeoff_framework.json",
    ],

    # ── Besoins utilisateur ─────────────────────────────
    "user_needs": [
        PATHS.knowledge_cpl_product   / "user_needs_analysis.json",
        PATHS.knowledge_cpl_strategy  / "value_proposition_framework.json",
        PATHS.knowledge_cpl_ethics    / "accessibility_principles.json",
    ],

    # ── Motivation & résilience ─────────────────────────
    "motivation": [
        PATHS.knowledge_psychology    / "motivation.json",
        PATHS.knowledge_softskills    / "resilience.json",
        PATHS.knowledge_softskills    / "discipline.json",
    ],

    # ── Conflit & assertivité ───────────────────────────
    "conflict": [
        PATHS.knowledge_softskills    / "conflict_management.json",
        PATHS.knowledge_softskills    / "negotiation.json",
        PATHS.knowledge_softskills    / "assertiveness.json",
    ],

    # ── Connaissance IA/produit (legacy) ────────────────
    "product_knowledge": [
        PATHS.knowledge_cpl_product   / "product_design_methodology.json",
        PATHS.knowledge_cpl_product   / "user_needs_analysis.json",
    ],
}


# ─────────────────────────────────────────────────────────
# Détection automatique intent → route par émotion
# ─────────────────────────────────────────────────────────

_EMOTION_ROUTES: dict[str, str] = {
    "fatigue":    "fatigue_support",
    "exhausted":  "fatigue_support",
    "stress":     "stress_support",
    "anxious":    "stress_support",
    "sad":        "emotional_support",
    "distress":   "emotional_support",
    "overwhelmed":"fatigue_support",
    "confused":   "problem_solving",
    "motivated":  "motivation",
    "ambitious":  "strategy_vision",
}


# ─────────────────────────────────────────────────────────
# API publique
# ─────────────────────────────────────────────────────────

def route_knowledge(
    intent: str,
    emotion: str = "neutral",
    multi: bool = False
) -> Union[dict, list[dict]]:
    """
    Charge le(s) knowledge(s) correspondant à un intent.

    Args:
        intent  : Intention détectée (voir _ROUTES)
        emotion : État émotionnel détecté (voir _EMOTION_ROUTES)
        multi   : Si True, retourne la liste complète des knowledges

    Returns:
        dict unique (premier knowledge) ou list[dict] si multi=True
    """
    # 1. Résolution par émotion si intent non trouvé
    resolved_intent = intent
    if intent not in _ROUTES and emotion in _EMOTION_ROUTES:
        resolved_intent = _EMOTION_ROUTES[emotion]

    # 2. Fallback sur emotional_support si toujours inconnu
    if resolved_intent not in _ROUTES:
        resolved_intent = "emotional_support"

    paths = _ROUTES[resolved_intent]

    if multi:
        return _load_multi(*paths)

    # Mode simple : retourner le premier knowledge valide
    for p in paths:
        k = _load(p)
        if "error" not in k:
            return k

    return _load(paths[0])  # retourner quand même (avec l'erreur)


def get_knowledge(folder: str, filename: str) -> dict:
    """
    Accès direct à un fichier knowledge par dossier + nom.

    Exemples :
        get_knowledge("softskills", "resilience")
        get_knowledge("cpl/strategy", "strategy_fundamentals")

    Args:
        folder   : Sous-dossier relatif dans knowledges/
        filename : Nom du fichier sans extension

    Returns:
        dict du knowledge
    """
    path = PATHS.knowledges / folder / f"{filename}.json"
    return _load(path)


def list_available_intents() -> list[str]:
    """Retourne la liste de tous les intents routables."""
    return sorted(_ROUTES.keys())


def check_routes() -> dict:
    """
    Vérifie que tous les fichiers référencés existent.
    Utile pour le démarrage et les tests.

    Returns:
        dict avec "ok" (list) et "missing" (list)
    """
    ok, missing = [], []
    for intent, paths in _ROUTES.items():
        for p in paths:
            entry = f"{intent} → {p.name}"
            if p.exists():
                ok.append(entry)
            else:
                missing.append(entry)
    return {"ok": ok, "missing": missing}


# ─────────────────────────────────────────────────────────
# Test standalone
# ─────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=== ALFRED — Knowledge Router ===\n")

    # Vérification de toutes les routes
    report = check_routes()
    print(f"✅ Routes OK      : {len(report['ok'])}")
    print(f"❌ Routes manquantes : {len(report['missing'])}")
    if report["missing"]:
        print("\nFichiers manquants :")
        for m in report["missing"]:
            print(f"  - {m}")

    print("\nIntents disponibles :")
    for intent in list_available_intents():
        print(f"  · {intent}")

    print("\nTest route 'decision' :")
    k = route_knowledge("decision")
    print(f"  → {k.get('name', k.get('id', 'inconnu'))} — {k.get('purpose', k.get('summary', ''))[:60]}")

    print("\nTest route émotion 'fatigue' :")
    k = route_knowledge("unknown_intent", emotion="fatigue")
    print(f"  → {k.get('name', k.get('id', 'inconnu'))} — {k.get('purpose', k.get('summary', ''))[:60]}")
