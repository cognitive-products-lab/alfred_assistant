"""
ALFRED — domain_matcher.py
Associe une requête utilisateur aux routes définies dans domain_links.json.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any

from src.knowledge.knowledge_loader import KnowledgeLoader


@dataclass
class DomainMatch:
    route_id: str
    score: float
    matched_keywords: list[str] = field(default_factory=list)
    intents: list[str] = field(default_factory=list)
    priority_domains: list[str] = field(default_factory=list)
    priority_knowledge: list[str] = field(default_factory=list)
    safety_rule: str | None = None


class DomainMatcher:

    SYNONYMS = {
        "fatigue": ["fatigue", "fatigué", "fatiguée", "épuisé", "épuisée"],
        "organisation": ["organisation", "organiser", "m'organiser"],
        "stress": ["stress", "stressé", "stressée", "angoisse"],
        "mémoire": ["mémoire", "souvenir", "retenir", "oublier"],
        "sécurité": ["sécurité", "cybersécurité", "rgpd"]
    }

    def __init__(self, loader: KnowledgeLoader):
        self.loader = loader
        self.domain_links = loader.domain_links
        self.routing_links = self.domain_links.get("routing_links", {})

    def normalize(self, text: str) -> str:
        text = text.lower().strip()
        text = re.sub(r"\s+", " ", text)
        return text

    def match(self, query: str, top_k: int = 5) -> list[DomainMatch]:
        normalized_query = self.normalize(query)
        matches: list[DomainMatch] = []

        for route_id, route in self.routing_links.items():
            keywords = route.get("keywords", [])
            matched_keywords = []

            for keyword in keywords:
                normalized_keyword = self.normalize(keyword)

                # Match exact
                if normalized_keyword in normalized_query:
                    matched_keywords.append(keyword)
                    continue

                # Match synonymes
                variants = self.SYNONYMS.get(normalized_keyword, [])

                for variant in variants:
                    if self.normalize(variant) in normalized_query:
                        matched_keywords.append(keyword)
                        break

            if not matched_keywords:
                continue

            score = self.compute_score(
                matched_keywords=matched_keywords,
                route=route,
                normalized_query=normalized_query
            )

            matches.append(
                DomainMatch(
                    route_id=route_id,
                    score=score,
                    matched_keywords=matched_keywords,
                    intents=route.get("intents", []),
                    priority_domains=route.get("priority_domains", []),
                    priority_knowledge=route.get("priority_knowledge", []),
                    safety_rule=route.get("safety_rule")
                )
            )

        matches.sort(key=lambda item: item.score, reverse=True)

        return matches[:top_k]

    def compute_score(
        self,
        matched_keywords: list[str],
        route: dict[str, Any],
        normalized_query: str
    ) -> float:

        score = 0.0

        # Score mots-clés
        score += len(matched_keywords) * 3.0

        # Bonus mots-clés longs
        for keyword in matched_keywords:
            if len(keyword) >= 8:
                score += 1.5

            if " " in keyword:
                score += 2.0

        route_context = " ".join([
            " ".join(route.get("priority_domains", [])),
            " ".join(route.get("intents", []))
        ]).lower()

        # Bonus sécurité
        if any(term in normalized_query for term in [
            "danger", "risque", "urgent", "sécurité", "rgpd"
        ]):
            if "security" in route_context or "ethics" in route_context:
                score += 5.0

        # Bonus émotion / fatigue
        if any(term in normalized_query for term in [
            "fatigue", "fatiguée", "stress", "burnout"
        ]):
            if "human" in route_context or "health" in route_context:
                score += 4.0

        # Bonus mémoire
        if any(term in normalized_query for term in [
            "mémoire", "souvenir", "retenir"
        ]):
            if "memory" in route_context:
                score += 4.0

        return score

    def get_priority_knowledge_ids(
        self,
        query: str,
        top_k_routes: int = 3
    ) -> list[str]:

        matches = self.match(query, top_k=top_k_routes)

        knowledge_ids: list[str] = []

        for match in matches:
            for knowledge_id in match.priority_knowledge:
                if knowledge_id not in knowledge_ids:
                    knowledge_ids.append(knowledge_id)

        return knowledge_ids

    def get_priority_domains(
        self,
        query: str,
        top_k_routes: int = 3
    ) -> list[str]:

        matches = self.match(query, top_k=top_k_routes)

        domains: list[str] = []

        for match in matches:
            for domain in match.priority_domains:
                if domain not in domains:
                    domains.append(domain)

        return domains

    def debug_match(self, query: str) -> None:

        print(f"Question : {query}\n")

        matches = self.match(query)

        if not matches:
            print("Aucune route détectée.\n")
            return

        for match in matches:
            print(f"[{match.score:.1f}] {match.route_id}")
            print(f"  Keywords : {match.matched_keywords}")
            print(f"  Domains  : {match.priority_domains}")
            print(f"  Knowledge: {match.priority_knowledge[:5]}")

            if match.safety_rule:
                print(f"  Safety   : {match.safety_rule}")

            print()


if __name__ == "__main__":

    loader = KnowledgeLoader()
    matcher = DomainMatcher(loader)

    tests = [
        "Je suis fatiguée et j'ai du mal à m'organiser.",
        "Explique-moi comment fonctionne un RAG avec une base vectorielle.",
        "Comment structurer la stratégie business d'ALFRED CPL ?",
        "Quelles règles RGPD pour la mémoire d'Alfred ?",
        "Pourquoi Alfred s'inspire de Jarvis et Alfred Pennyworth ?"
    ]

    for test in tests:
        print("=" * 80)
        matcher.debug_match(test)
