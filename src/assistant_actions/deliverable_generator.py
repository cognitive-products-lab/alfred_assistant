"""
════════════════════════════════════════════════════════════
PROJECT      : ALFRED
BLOCK        : B10 (ALFRED CPL)
FUNCTION     : 10.09
FILE         : src/assistant_actions/deliverable_generator.py
ROLE         : Génération de livrables métier soumis à validation humaine

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-07-11
VERSION      : V1.0
STATUS       : ACTIVE

DESCRIPTION :
Point d'entrée unique pour produire un livrable métier (fiche de cadrage,
registre de risques...) dans ALFRED CPL. Enchaîne :
  1. Recherche documentaire (B18) filtrée par rôle métier (B10/cpl_role_access)
     et par client (B10/cpl_client_isolation) — mêmes règles d'accès qu'une
     question normale.
  2. Remplissage d'un gabarit à partir des connaissances retrouvées
     (assistant_actions/deliverable_templates.py) — jamais de contenu inventé.
  3. Passage obligatoire par le pipeline Zero Trust (zero_trust_orchestrator) :
     l'action GENERATE_DELIVERABLE est toujours mise en REVIEW (policy_engine),
     donc le livrable est mis en file d'attente de validation humaine
     (human_validation) plutôt que renvoyé comme définitif.

Le livrable retourné à l'utilisateur est donc TOUJOURS un brouillon associé
à un approval_id — jamais un document final.
════════════════════════════════════════════════════════════
"""
from __future__ import annotations

from typing import Any

from src.knowledge.retrieval_engine import KnowledgeRetrievalEngine
from src.assistant_actions.deliverable_templates import render_deliverable, TEMPLATE_TYPES
from src.security.zero_trust_orchestrator import authorize_request


def generate_deliverable(
    deliverable_type: str,
    topic: str,
    user_id: str,
    role: str,
    device_id: str,
    session_id: str,
    client_id: str = "",
    request_id: str = "",
    retrieval_engine: KnowledgeRetrievalEngine | None = None,
) -> dict[str, Any]:
    """
    Génère un brouillon de livrable métier et le soumet à validation humaine.

    Args:
        deliverable_type : "fiche_cadrage" | "registre_risques"
        topic : sujet du livrable (ex. "projet d'automatisation IA interne")
        session_id : session déjà authentifiée (aucune création implicite de session —
            Zero Trust : pas d'accès à une action sensible sans authentification préalable)
        retrieval_engine : instance existante à réutiliser, sinon une nouvelle est créée
            (coûteux — préférer réutiliser l'instance de l'application appelante)

    Returns:
        {
          "authorized": False, "decision": "REVIEW", "pending": True, "approval_id": ...,
          "deliverable": {...brouillon structuré...}
        }
        ou un refus classique du pipeline Zero Trust (device/MFA/permission) si un
        contrôle antérieur à la génération échoue — auquel cas aucun livrable n'est produit.
    """
    if deliverable_type not in TEMPLATE_TYPES:
        raise ValueError(
            f"Type de livrable inconnu : {deliverable_type!r} "
            f"(types disponibles : {', '.join(TEMPLATE_TYPES)})"
        )

    engine = retrieval_engine or KnowledgeRetrievalEngine()

    retrieval_result = engine.retrieve(
        query=topic,
        conversation_context={"mode": "deliverable_generation", "deliverable_type": deliverable_type},
        user_id=user_id,
        role=role,
        request_id=request_id,
        client_id=client_id,
    )

    deliverable = render_deliverable(
        deliverable_type=deliverable_type,
        topic=topic,
        ranked_knowledge=retrieval_result.ranked_knowledge,
        citations=retrieval_result.citations,
    )
    deliverable["client_id"] = client_id or None
    deliverable["contradictions"] = retrieval_result.contradictions

    auth_result = authorize_request(
        user_id=user_id,
        role=role,
        permission="RUN_AI_MODULE",
        action="GENERATE_DELIVERABLE",
        resource=f"deliverable:{deliverable_type}:{topic}",
        resource_sensitivity="MEDIUM",
        device_id=device_id,
        user_input=topic,
        session_id=session_id,
        payload=deliverable,
        request_id=request_id,
    )

    auth_result["deliverable"] = deliverable
    return auth_result
