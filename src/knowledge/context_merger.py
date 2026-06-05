from __future__ import annotations

"""
PROJECT      : ALFRED
BLOCK        : B18
FUNCTION     : 18.05
FILE         : src/knowledge/context_merger.py
ROLE         : Construit un contexte exploitable à partir des connaissances classées

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-06-03
UPDATED      : 2026-06-05
VERSION      : V1.1
STATUS       : TESTED

DESCRIPTION :
Fusion contexte — assemble le bloc knowledge final injecté dans le prompt LLM.
"""

"""
ALFRED — context_merger.py
Construit un contexte exploitable à partir des connaissances classées.
"""

from dataclasses import dataclass, field
from typing import Any

from src.knowledge.knowledge_ranker import RankedKnowledge


@dataclass
class MergedKnowledgeContext:
    query: str
    knowledge_ids: list[str] = field(default_factory=list)
    domains: list[str] = field(default_factory=list)
    sources: list[str] = field(default_factory=list)
    safety_notes: list[str] = field(default_factory=list)
    prompt_block: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)


class ContextMerger:
    def __init__(self, max_chars_per_knowledge: int = 900):
        self.max_chars_per_knowledge = max_chars_per_knowledge

    def merge(
        self,
        query: str,
        ranked_knowledge: list[RankedKnowledge],
        conversation_context: dict[str, Any] | None = None
    ) -> MergedKnowledgeContext:

        conversation_context = conversation_context or {}

        knowledge_ids: list[str] = []
        domains: list[str] = []
        sources: list[str] = []
        safety_notes: list[str] = []
        blocks: list[str] = []

        for item in ranked_knowledge:
            knowledge_ids.append(item.knowledge_id)

            for domain in item.domains:
                if domain not in domains:
                    domains.append(domain)

            for source in item.sources:
                if source not in sources:
                    sources.append(source)

            block = self._build_knowledge_block(item)

            if block:
                blocks.append(block)

            safety = self._extract_safety_notes(item)
            for note in safety:
                if note not in safety_notes:
                    safety_notes.append(note)

        prompt_block = self._build_prompt_block(
            query=query,
            blocks=blocks,
            safety_notes=safety_notes,
            conversation_context=conversation_context
        )

        return MergedKnowledgeContext(
            query=query,
            knowledge_ids=knowledge_ids,
            domains=domains,
            sources=sources,
            safety_notes=safety_notes,
            prompt_block=prompt_block,
            metadata={
                "knowledge_count": len(knowledge_ids),
                "domain_count": len(domains),
                "source_count": len(sources),
                "has_safety_notes": bool(safety_notes),
                "conversation_context_keys": list(conversation_context.keys())
            }
        )

    def _build_knowledge_block(self, item: RankedKnowledge) -> str:
        if not item.data:
            return ""

        data = item.data.get("data", {})
        registry = item.data.get("registry", {})

        title = data.get("title") or registry.get("filename") or item.knowledge_id
        summary = data.get("summary", "")
        purpose = data.get("purpose", "")

        content = data.get("content", {})
        definition = ""

        if isinstance(content, dict):
            definition = (
                content.get("definition")
                or content.get("core_definition")
                or ""
            )

        elif isinstance(content, str):
            definition = content

        tags = data.get("tags", [])
        intents = data.get("intents", [])

        parts = [
            f"KNOWLEDGE_ID: {item.knowledge_id}",
            f"SCORE: {item.score:.1f}",
            f"TITLE: {title}"
        ]

        if summary:
            parts.append(f"SUMMARY: {summary}")

        if purpose:
            parts.append(f"PURPOSE: {purpose}")

        if definition:
            parts.append(f"DEFINITION: {definition}")

        if tags:
            parts.append("TAGS: " + ", ".join(str(tag) for tag in tags[:8]))

        if intents:
            parts.append("INTENTS: " + ", ".join(str(intent) for intent in intents[:8]))

        block = "\n".join(parts)

        if len(block) > self.max_chars_per_knowledge:
            block = block[:self.max_chars_per_knowledge] + "…"

        return block

    def _extract_safety_notes(self, item: RankedKnowledge) -> list[str]:
        if not item.data:
            return []

        data = item.data.get("data", {})
        notes: list[str] = []

        safety_notes = data.get("safety_notes")

        if isinstance(safety_notes, str):
            notes.append(safety_notes)

        if isinstance(safety_notes, dict):
            fallback = safety_notes.get("fallback_behavior")
            if fallback:
                notes.append(str(fallback))

            forbidden = safety_notes.get("forbidden_usage", [])
            if isinstance(forbidden, list):
                notes.extend(str(value) for value in forbidden)

        safety_level = data.get("safety_level")
        if safety_level in ("sensitive", "high_risk"):
            notes.append(f"Safety level: {safety_level}")

        return notes

    def _build_prompt_block(
        self,
        query: str,
        blocks: list[str],
        safety_notes: list[str],
        conversation_context: dict[str, Any]
    ) -> str:

        sections: list[str] = []

        sections.append("=== ALFRED KNOWLEDGE CONTEXT ===")
        sections.append(f"USER_QUERY: {query}")

        if conversation_context:
            sections.append("\n--- CONVERSATION CONTEXT ---")
            for key, value in conversation_context.items():
                sections.append(f"{key}: {value}")

        if blocks:
            sections.append("\n--- SELECTED KNOWLEDGE ---")
            sections.append("\n\n".join(blocks))
        else:
            sections.append("\n--- SELECTED KNOWLEDGE ---")
            sections.append("No relevant knowledge found.")

        if safety_notes:
            sections.append("\n--- SAFETY NOTES ---")
            for note in safety_notes[:8]:
                sections.append(f"- {note}")

        sections.append("\n--- RESPONSE INSTRUCTION ---")
        sections.append(
            "Use the selected knowledge to answer clearly, safely and contextually. "
            "Do not invent knowledge that is not present. "
            "If the topic is medical, legal, financial or high-risk, stay cautious."
        )

        return "\n".join(sections)

    def to_prompt(self, merged_context: MergedKnowledgeContext) -> str:
        return merged_context.prompt_block


if __name__ == "__main__":
    from knowledge_loader import KnowledgeLoader
    from domain_matcher import DomainMatcher
    from taxonomy_router import TaxonomyRouter
    from knowledge_ranker import KnowledgeRanker

    loader = KnowledgeLoader()
    matcher = DomainMatcher(loader)
    router = TaxonomyRouter(loader)
    ranker = KnowledgeRanker(loader, matcher, router)
    merger = ContextMerger()

    query = "Je suis fatiguée et j'ai du mal à m'organiser."
    ranked = ranker.rank(query)

    merged = merger.merge(
        query=query,
        ranked_knowledge=ranked,
        conversation_context={
            "mode": "support_mode",
            "language": "fr"
        }
    )

    print(merged.prompt_block)