from __future__ import annotations

"""
PROJECT      : ALFRED
BLOCK        : GLOBAL
FUNCTION     : XX.XX
FILE         : src/knowledge/retrieval_engine.py
ROLE         : TO_DEFINE

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-06-03
UPDATED      : 2026-06-05
VERSION      : V1.1
STATUS       : TESTED

DESCRIPTION :
Module ALFRED — description a completer.
"""

"""
ALFRED — retrieval_engine.py
Orchestrateur principal du Knowledge Retrieval Engine B18.
"""

from dataclasses import dataclass, field
from typing import Any, Callable

from src.knowledge.knowledge_loader import KnowledgeLoader
from src.knowledge.domain_matcher import DomainMatcher
from src.knowledge.taxonomy_router import TaxonomyRouter
from src.knowledge.knowledge_ranker import KnowledgeRanker, RankedKnowledge
from src.knowledge.context_merger import ContextMerger, MergedKnowledgeContext
from src.security.audit_trail import write_audit_event

# Type d'un filtre d'accès additionnel : (items_classés, identifiant) -> (autorisés, bloqués).
# Le moteur core reste générique — il ne connaît aucune notion de rôle métier ou de
# client. Les produits construits sur ALFRED (ex. ALFRED CPL, dépôt séparé) injectent
# leurs propres filtres au constructeur plutôt que d'être importés en dur ici.
AccessFilter = Callable[[list[RankedKnowledge], str], "tuple[list[RankedKnowledge], list[RankedKnowledge]]"]

@dataclass
class RetrievalResult:
    query: str
    ranked_knowledge: list[RankedKnowledge] = field(default_factory=list)
    merged_context: MergedKnowledgeContext | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def prompt_block(self) -> str:
        if not self.merged_context:
            return ""
        return self.merged_context.prompt_block

    @property
    def knowledge_ids(self) -> list[str]:
        if not self.merged_context:
            return []
        return self.merged_context.knowledge_ids

    @property
    def domains(self) -> list[str]:
        if not self.merged_context:
            return []
        return self.merged_context.domains

    @property
    def citations(self) -> list[dict[str, Any]]:
        if not self.merged_context:
            return []
        return self.merged_context.citations

    @property
    def contradictions(self) -> list[dict[str, Any]]:
        if not self.merged_context:
            return []
        return self.merged_context.contradictions

    @property
    def blocked_knowledge_ids(self) -> list[str]:
        return self.metadata.get("blocked_by_role", [])

    @property
    def blocked_by_client_ids(self) -> list[str]:
        return self.metadata.get("blocked_by_client", [])


class KnowledgeRetrievalEngine:
    """
    Point d'entrée unique pour interroger le système knowledge B18.
    """

    def __init__(
        self,
        project_root: str | KnowledgeLoader = "D:/PROJET_ALFRED/ALFRED_PC",
        max_chars_per_knowledge: int = 900,
        role_filter: AccessFilter | None = None,
        client_filter: AccessFilter | None = None,
    ):
        if isinstance(project_root, KnowledgeLoader):
            self.loader = project_root
        else:
            self.loader = KnowledgeLoader(project_root=project_root)
        self.matcher = DomainMatcher(self.loader)
        self.router = TaxonomyRouter(self.loader)
        self.ranker = KnowledgeRanker(
            loader=self.loader,
            matcher=self.matcher,
            router=self.router
        )
        self.merger = ContextMerger(
            max_chars_per_knowledge=max_chars_per_knowledge
        )
        # Filtres d'accès optionnels (rôle métier, client...) — voir AccessFilter
        # ci-dessus. Sans filtre injecté, retrieve() ne restreint rien : le moteur
        # core reste utilisable seul (assistant personnel) sans dépendance externe.
        self.role_filter = role_filter
        self.client_filter = client_filter

    def retrieve(
        self,
        query: str,
        conversation_context: dict[str, Any] | None = None,
        user_id: str = "",
        role: str = "",
        request_id: str = "",
        client_id: str = ""
    ) -> RetrievalResult:
        conversation_context = conversation_context or {}

        ranked = self.ranker.rank(query)

        blocked_by_role: list[RankedKnowledge] = []
        blocked_by_client: list[RankedKnowledge] = []

        if self.role_filter:
            ranked, blocked_by_role = self.role_filter(ranked, role)
        if self.client_filter:
            ranked, blocked_by_client = self.client_filter(ranked, client_id)

        merged = self.merger.merge(
            query=query,
            ranked_knowledge=ranked,
            conversation_context=conversation_context
        )

        if user_id and merged.knowledge_ids:
            self._log_knowledge_consultation(
                knowledge_ids=merged.knowledge_ids,
                user_id=user_id,
                role=role,
                request_id=request_id
            )

        if user_id and blocked_by_role:
            self._log_blocked_by_role(
                blocked_items=blocked_by_role,
                user_id=user_id,
                role=role,
                request_id=request_id
            )

        if user_id and blocked_by_client:
            self._log_blocked_by_client(
                blocked_items=blocked_by_client,
                user_id=user_id,
                role=role,
                client_id=client_id,
                request_id=request_id
            )

        return RetrievalResult(
            query=query,
            ranked_knowledge=ranked,
            merged_context=merged,
            metadata={
                "indexed_knowledge_count": self.loader.stats().get("indexed_knowledge_count"),
                "ranked_knowledge_count": len(ranked),
                "selected_knowledge_ids": merged.knowledge_ids,
                "selected_domains": merged.domains,
                "sources": merged.sources,
                "blocked_by_role": [item.knowledge_id for item in blocked_by_role],
                "blocked_by_client": [item.knowledge_id for item in blocked_by_client],
                "client_id": client_id,
                "has_safety_notes": bool(merged.safety_notes),
                "citations": merged.citations,
                "contradictions": merged.contradictions
            }
        )

    def _log_knowledge_consultation(
        self,
        knowledge_ids: list[str],
        user_id: str,
        role: str,
        request_id: str
    ) -> None:
        """Trace chaque connaissance consultée dans la piste d'audit sécurité (B20)."""
        try:
            for knowledge_id in knowledge_ids:
                write_audit_event(
                    user_id=user_id,
                    action="consult_knowledge",
                    resource=knowledge_id,
                    decision="ALLOW",
                    request_id=request_id,
                    role=role
                )
        except Exception:
            # La journalisation ne doit jamais bloquer une réponse à l'utilisateur.
            pass

    def _log_blocked_by_role(
        self,
        blocked_items: list[RankedKnowledge],
        user_id: str,
        role: str,
        request_id: str
    ) -> None:
        """Trace les connaissances écartées faute d'habilitation (rôle métier CPL) — B10/B20."""
        try:
            for item in blocked_items:
                write_audit_event(
                    user_id=user_id,
                    action="consult_knowledge",
                    resource=item.knowledge_id,
                    decision="DENY_PERMISSION",
                    request_id=request_id,
                    role=role
                )
        except Exception:
            pass

    def _log_blocked_by_client(
        self,
        blocked_items: list[RankedKnowledge],
        user_id: str,
        role: str,
        client_id: str,
        request_id: str
    ) -> None:
        """Trace les connaissances écartées faute d'appartenance au bon client (isolation multi-tenant) — B10/B20."""
        try:
            for item in blocked_items:
                write_audit_event(
                    user_id=user_id,
                    action="consult_knowledge",
                    resource=item.knowledge_id,
                    decision="DENY_CLIENT_ISOLATION",
                    request_id=request_id,
                    role=role,
                    device_id=f"requested_client:{client_id or 'none'}"
                )
        except Exception:
            pass

    def retrieve_prompt(
        self,
        query: str,
        conversation_context: dict[str, Any] | None = None,
        user_id: str = "",
        role: str = "",
        request_id: str = "",
        client_id: str = ""
    ) -> str:
        result = self.retrieve(
            query=query,
            conversation_context=conversation_context,
            user_id=user_id,
            role=role,
            request_id=request_id,
            client_id=client_id
        )
        return result.prompt_block

    def debug(
        self,
        query: str,
        conversation_context: dict[str, Any] | None = None
    ) -> None:
        result = self.retrieve(
            query=query,
            conversation_context=conversation_context
        )

        print("=" * 80)
        print("ALFRED — KNOWLEDGE RETRIEVAL ENGINE")
        print("=" * 80)
        print(f"QUERY: {query}")
        print()

        print("--- METADATA ---")
        for key, value in result.metadata.items():
            print(f"{key}: {value}")

        print("\n--- RANKED KNOWLEDGE ---")
        if not result.ranked_knowledge:
            print("Aucun knowledge sélectionné.")
        else:
            for item in result.ranked_knowledge:
                print(f"[{item.score:.1f}] {item.knowledge_id}")


# Alias pour compatibilité avec les tests et imports existants
RetrievalEngine = KnowledgeRetrievalEngine


if __name__ == "__main__":
    engine = KnowledgeRetrievalEngine()

    tests = [
        "Je suis fatiguée et j'ai du mal à m'organiser.",
        "Explique-moi comment fonctionne un RAG avec une base vectorielle.",
        "Comment structurer la stratégie business d'ALFRED CPL ?",
        "Quelles règles RGPD pour la mémoire d'Alfred ?",
        "Pourquoi Alfred s'inspire de Jarvis et Alfred Pennyworth ?"
    ]

    for test in tests:
        engine.debug(
            query=test,
            conversation_context={
                "mode": "knowledge_retrieval_test",
                "language": "fr"
            }
        )
        print("\n\n")