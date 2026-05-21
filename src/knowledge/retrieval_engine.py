"""
ALFRED — retrieval_engine.py
Orchestrateur principal du Knowledge Retrieval Engine B18.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from src.knowledge.knowledge_loader import KnowledgeLoader
from src.knowledge.domain_matcher import DomainMatcher
from src.knowledge.taxonomy_router import TaxonomyRouter
from src.knowledge.knowledge_ranker import KnowledgeRanker, RankedKnowledge
from src.knowledge.context_merger import ContextMerger, MergedKnowledgeContext

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


class KnowledgeRetrievalEngine:
    """
    Point d'entrée unique pour interroger le système knowledge B18.
    """

    def __init__(
        self,
        project_root: str = "D:/PROJET_ALFRED/ALFRED_PC",
        max_chars_per_knowledge: int = 900
    ):
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

    def retrieve(
        self,
        query: str,
        conversation_context: dict[str, Any] | None = None
    ) -> RetrievalResult:
        conversation_context = conversation_context or {}

        ranked = self.ranker.rank(query)

        merged = self.merger.merge(
            query=query,
            ranked_knowledge=ranked,
            conversation_context=conversation_context
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
                "has_safety_notes": bool(merged.safety_notes)
            }
        )

    def retrieve_prompt(
        self,
        query: str,
        conversation_context: dict[str, Any] | None = None
    ) -> str:
        result = self.retrieve(
            query=query,
            conversation_context=conversation_context
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
                print(f"  Sources: {item.sources}")
                print(f"  Domains: {item.domains}")

        print("\n--- PROMPT BLOCK ---")
        print(result.prompt_block)


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
