from __future__ import annotations

"""
PROJECT      : ALFRED
BLOCK        : B18
FUNCTION     : 18.03
FILE         : src/knowledge/taxonomy_router.py
ROLE         : Exploite taxonomy.json pour router les requêtes vers les knowledge_ids

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-06-03
UPDATED      : 2026-06-05
VERSION      : V1.1
STATUS       : TESTED

DESCRIPTION :
Router taxonomique — résout domaines, sous-domaines et intents depuis taxonomy.json.
"""

"""
ALFRED — taxonomy_router.py
Exploite taxonomy.json pour retrouver les domaines, sous-domaines,
intents et knowledge_ids liés à une requête.
"""

import re
from dataclasses import dataclass, field
from typing import Any

from src.knowledge.knowledge_loader import KnowledgeLoader
from src.knowledge.french_stopwords import FRENCH_STOPWORDS


@dataclass
class TaxonomyRoute:
    domain: str
    subdomain: str
    score: float
    intents: list[str] = field(default_factory=list)
    linked_knowledge: list[str] = field(default_factory=list)
    priority: str = "medium"
    status: str = "active"


class TaxonomyRouter:
    def __init__(self, loader: KnowledgeLoader):
        self.loader = loader
        self.taxonomy = loader.taxonomy
        self.domains = self.taxonomy.get("domains", {})

    def normalize(self, text: str) -> str:
        return text.lower().strip()

    def route(self, query: str, top_k: int = 5) -> list[TaxonomyRoute]:
        query_norm = self.normalize(query)
        routes: list[TaxonomyRoute] = []

        for domain_id, domain_data in self.domains.items():
            domain_priority = domain_data.get("priority", "medium")
            subdomains = domain_data.get("subdomains", {})

            for subdomain_id, subdomain_data in subdomains.items():
                status = subdomain_data.get("status", "active")

                if status == "planned":
                    continue

                intents = subdomain_data.get("intents", [])
                linked_knowledge = subdomain_data.get("linked_knowledge", [])
                label = subdomain_data.get("label", "")

                score = self.compute_score(
                    query_norm=query_norm,
                    domain_id=domain_id,
                    subdomain_id=subdomain_id,
                    label=label,
                    intents=intents,
                    linked_knowledge=linked_knowledge,
                    domain_priority=domain_priority
                )

                if score <= 0:
                    continue

                routes.append(
                    TaxonomyRoute(
                        domain=domain_id,
                        subdomain=subdomain_id,
                        score=score,
                        intents=intents,
                        linked_knowledge=linked_knowledge,
                        priority=domain_priority,
                        status=status
                    )
                )

        routes.sort(key=lambda item: item.score, reverse=True)
        return routes[:top_k]

    def compute_score(
        self,
        query_norm: str,
        domain_id: str,
        subdomain_id: str,
        label: str,
        intents: list[str],
        linked_knowledge: list[str],
        domain_priority: str
    ) -> float:
        score = 0.0

        searchable_parts = [
            domain_id,
            subdomain_id,
            label,
            " ".join(intents),
            " ".join(linked_knowledge)
        ]

        searchable_text = self.normalize(" ".join(searchable_parts))
        # Mots entiers uniquement (pas de substring) — un "in searchable_text"
        # brut ferait matcher n'importe quel mot de 4+ lettres à l'intérieur
        # d'un mot plus long sans rapport (même bug déjà corrigé côté
        # knowledge_ranker.py::_add_keyword_content_scores le 15/08/2026,
        # mais pas ici).
        searchable_words = set(re.findall(r"\w+", searchable_text))

        # \w+ retire la ponctuation collée aux mots (ex. "iso27001," -> "iso27001")
        words = [
            word for word in re.findall(r"\w+", query_norm.replace("'", " ").replace("-", " "))
            if len(word) >= 4 and word not in FRENCH_STOPWORDS
        ]

        for word in words:
            if word in searchable_words:
                score += 2.0

        if domain_id in query_norm:
            score += 3.0

        if subdomain_id.replace("_", " ") in query_norm:
            score += 4.0

        if label and self.normalize(label) in query_norm:
            score += 4.0

        priority_bonus = {
            "critical": 3.0,
            "high": 2.0,
            "medium": 1.0,
            "optional": 0.5
        }

        if score > 0:
            score += priority_bonus.get(domain_priority, 1.0)

        return score

    def get_linked_knowledge_ids(
        self,
        query: str,
        top_k_routes: int = 5
    ) -> list[str]:
        routes = self.route(query, top_k=top_k_routes)

        knowledge_ids: list[str] = []

        for route in routes:
            for knowledge_id in route.linked_knowledge:
                if knowledge_id not in knowledge_ids:
                    knowledge_ids.append(knowledge_id)

        return knowledge_ids

    def get_domains(
        self,
        query: str,
        top_k_routes: int = 5
    ) -> list[str]:
        routes = self.route(query, top_k=top_k_routes)

        domains: list[str] = []

        for route in routes:
            if route.domain not in domains:
                domains.append(route.domain)

        return domains

    def debug_route(self, query: str) -> None:
        print(f"Question : {query}\n")

        routes = self.route(query)

        if not routes:
            print("Aucune route taxonomy détectée.\n")
            return

        for route in routes:
            print(f"[{route.score:.1f}] {route.domain}.{route.subdomain}")
            print(f"  Priority : {route.priority}")
            print(f"  Intents  : {route.intents[:5]}")
            print(f"  Knowledge: {route.linked_knowledge[:5]}")
            print()


if __name__ == "__main__":
    loader = KnowledgeLoader()
    router = TaxonomyRouter(loader)

    tests = [
        "Je suis fatiguée et j'ai du mal à m'organiser.",
        "Explique-moi comment fonctionne un RAG avec une base vectorielle.",
        "Comment structurer la stratégie business d'ALFRED CPL ?",
        "Quelles règles RGPD pour la mémoire d'Alfred ?",
        "Pourquoi Alfred s'inspire de Jarvis et Alfred Pennyworth ?"
    ]

    for test in tests:
        print("=" * 80)
        router.debug_route(test)