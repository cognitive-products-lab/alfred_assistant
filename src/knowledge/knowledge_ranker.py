from __future__ import annotations

"""
PROJECT      : ALFRED
BLOCK        : B18
FUNCTION     : 18.04
FILE         : src/knowledge/knowledge_ranker.py
ROLE         : Fusionne et classe les knowledge_ids issus du domain_matcher et du taxonomy_router

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-06-03
UPDATED      : 2026-06-05
VERSION      : V1.1
STATUS       : TESTED

DESCRIPTION :
Classement knowledge — scoring et déduplication des IDs pour le contexte LLM.
"""

"""
ALFRED — knowledge_ranker.py
Fusionne et classe les knowledge_ids issus du domain_matcher et du taxonomy_router.
"""

import re
from dataclasses import dataclass, field
from typing import Any

from src.knowledge.knowledge_loader import KnowledgeLoader
from src.knowledge.domain_matcher import DomainMatcher
from src.knowledge.taxonomy_router import TaxonomyRouter


@dataclass
class RankedKnowledge:
    knowledge_id: str
    score: float
    sources: list[str] = field(default_factory=list)
    domains: list[str] = field(default_factory=list)
    data: dict[str, Any] | None = None


class KnowledgeRanker:
    def __init__(
        self,
        loader: KnowledgeLoader,
        matcher: DomainMatcher | None = None,
        router: TaxonomyRouter | None = None,
    ):
        self.loader = loader
        self.matcher = matcher
        self.router = router
        self.rules = loader.retrieval_rules

        scoring = self.rules.get("knowledge_scoring_rules", {})
        self.max_loaded = scoring.get("max_knowledge_loaded_per_query", 6)
        self.minimum_score = scoring.get("minimum_score_to_use", 3.0)

    def rank(self, query: str, knowledge_ids: list[str] | None = None) -> list[RankedKnowledge]:
        scores: dict[str, RankedKnowledge] = {}

        self._add_domain_matcher_scores(query, scores)
        self._add_taxonomy_router_scores(query, scores)
        self._add_keyword_content_scores(query, scores)

        ranked = list(scores.values())

        ranked = [
            item for item in ranked
            if item.score >= self.minimum_score
        ]

        ranked.sort(key=lambda item: item.score, reverse=True)

        return ranked[:self.max_loaded]

    def _ensure_item(
        self,
        scores: dict[str, RankedKnowledge],
        knowledge_id: str
    ) -> RankedKnowledge:
        if knowledge_id not in scores:
            knowledge = self.loader.get_knowledge(knowledge_id)
            domains = []

            if knowledge:
                domain = knowledge.get("domain")
                subdomain = knowledge.get("subdomain")

                if domain:
                    domains.append(domain)

                if subdomain and subdomain not in domains:
                    domains.append(subdomain)

            scores[knowledge_id] = RankedKnowledge(
                knowledge_id=knowledge_id,
                score=0.0,
                sources=[],
                domains=domains,
                data=knowledge
            )

        return scores[knowledge_id]

    def _add_domain_matcher_scores(
        self,
        query: str,
        scores: dict[str, RankedKnowledge]
    ) -> None:
        if not self.matcher:
            return
        matches = self.matcher.match(query, top_k=5)

        for match in matches:
            for knowledge_id in match.priority_knowledge:
                if not self.loader.get_knowledge(knowledge_id):
                    continue

                item = self._ensure_item(scores, knowledge_id)
                item.score += match.score

                if "domain_matcher" not in item.sources:
                    item.sources.append("domain_matcher")

                for domain in match.priority_domains:
                    if domain not in item.domains:
                        item.domains.append(domain)

    def _add_taxonomy_router_scores(
        self,
        query: str,
        scores: dict[str, RankedKnowledge]
    ) -> None:
        if not self.router:
            return
        routes = self.router.route(query, top_k=5)

        for route in routes:
            for knowledge_id in route.linked_knowledge:
                if not self.loader.get_knowledge(knowledge_id):
                    continue

                item = self._ensure_item(scores, knowledge_id)
                item.score += route.score

                if "taxonomy_router" not in item.sources:
                    item.sources.append("taxonomy_router")

                if route.domain not in item.domains:
                    item.domains.append(route.domain)

                if route.subdomain not in item.domains:
                    item.domains.append(route.subdomain)

    def _add_keyword_content_scores(
        self,
        query: str,
        scores: dict[str, RankedKnowledge]
    ) -> None:
        query_lower = query.lower()

        # \w+ retire la ponctuation collée aux mots (ex. "iso27001," -> "iso27001")
        query_words = [
            word.lower()
            for word in re.findall(r"\w+", query.replace("'", " ").replace("-", " "))
            if len(word) >= 4
        ]

        technical_keywords = [
            "rag",
            "retrieval",
            "embedding",
            "base vectorielle",
            "llm",
            "chunking",
            "mémoire sémantique"
        ]

        general_culture_prefixes = [
            "culture.general.",
            "culture.culture_generale."
        ]

        is_technical_query = any(
            keyword in query_lower
            for keyword in technical_keywords
        )

        for knowledge_id, knowledge in self.loader.knowledge_index.items():
            searchable = self._build_searchable_text(knowledge).lower()

            hits = 0
            for word in query_words:
                if word in searchable:
                    hits += 1

            if hits <= 0:
                continue

            item = self._ensure_item(scores, knowledge_id)
            item.score += hits * 1.5

            if "content_keywords" not in item.sources:
                item.sources.append("content_keywords")

            # Pénalité culture générale sur requête technique
            if is_technical_query and any(
                knowledge_id.startswith(prefix)
                for prefix in general_culture_prefixes
            ):
                item.score -= 6.0

    def _build_searchable_text(self, knowledge: dict[str, Any]) -> str:
        data = knowledge.get("data", {})
        registry = knowledge.get("registry", {})

        parts = [
            knowledge.get("id", ""),
            knowledge.get("domain", ""),
            knowledge.get("subdomain", ""),
            registry.get("filename", ""),
            registry.get("category", "")
        ]

        for key in [
            "title",
            "summary",
            "purpose",
            "domain",
            "subdomain",
            "category",
            "core_definition"
        ]:
            value = data.get(key)
            if isinstance(value, str):
                parts.append(value)

        for key in ["tags", "intents", "usage_context"]:
            value = data.get(key)
            if isinstance(value, list):
                parts.extend(str(v) for v in value)

        content = data.get("content")
        if isinstance(content, dict):
            parts.append(str(content))

        return " ".join(parts)

    def debug_rank(self, query: str) -> None:
        print(f"Question : {query}\n")

        ranked = self.rank(query)

        if not ranked:
            print("Aucun knowledge classé.\n")
            return

        for item in ranked:
            print(f"[{item.score:.1f}] {item.knowledge_id}")
            print(f"  Sources : {item.sources}")
            print(f"  Domains : {item.domains}")

            if item.data:
                data = item.data.get("data", {})
                print(f"  Title   : {data.get('title', item.knowledge_id)}")
                print(f"  File    : {item.data.get('file')}")

            print()


if __name__ == "__main__":
    loader = KnowledgeLoader()
    matcher = DomainMatcher(loader)
    router = TaxonomyRouter(loader)
    ranker = KnowledgeRanker(loader, matcher, router)

    tests = [
        "Je suis fatiguée et j'ai du mal à m'organiser.",
        "Explique-moi comment fonctionne un RAG avec une base vectorielle.",
        "Comment structurer la stratégie business d'ALFRED CPL ?",
        "Quelles règles RGPD pour la mémoire d'Alfred ?",
        "Pourquoi Alfred s'inspire de Jarvis et Alfred Pennyworth ?"
    ]

    for test in tests:
        print("=" * 80)
        ranker.debug_rank(test)