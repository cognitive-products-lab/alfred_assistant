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
STATUS       : VALIDATED

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
    citations: list[dict[str, Any]] = field(default_factory=list)
    contradictions: list[dict[str, Any]] = field(default_factory=list)


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
        citations: list[dict[str, Any]] = []

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

            citation = self._extract_citation(item)
            if citation:
                citations.append(citation)

        contradictions = self._detect_contradictions(citations)

        prompt_block = self._build_prompt_block(
            query=query,
            blocks=blocks,
            safety_notes=safety_notes,
            conversation_context=conversation_context,
            citations=citations,
            contradictions=contradictions
        )

        return MergedKnowledgeContext(
            query=query,
            knowledge_ids=knowledge_ids,
            domains=domains,
            sources=sources,
            safety_notes=safety_notes,
            prompt_block=prompt_block,
            citations=citations,
            contradictions=contradictions,
            metadata={
                "knowledge_count": len(knowledge_ids),
                "domain_count": len(domains),
                "source_count": len(sources),
                "has_safety_notes": bool(safety_notes),
                "citation_count": len(citations),
                "contradiction_count": len(contradictions),
                "conversation_context_keys": list(conversation_context.keys())
            }
        )

    def _extract_citation(self, item: RankedKnowledge) -> dict[str, Any] | None:
        """Extrait les métadonnées de source (document/version/date) d'une connaissance, si présentes."""
        if not item.data:
            return None

        data = item.data.get("data", {})
        source_document = data.get("source_document")

        if not isinstance(source_document, dict) or not source_document:
            return None

        return {
            "knowledge_id": item.knowledge_id,
            "reference": source_document.get("reference", ""),
            "name": source_document.get("name", ""),
            "version": source_document.get("version", ""),
            "validated_date": source_document.get("validated_date", ""),
            "owner": source_document.get("owner", ""),
            "document_status": source_document.get("document_status", ""),
            "still_referenced_in": source_document.get("still_referenced_in") or [],
        }

    def _detect_contradictions(self, citations: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Détecte les cas où deux sources citées partagent la même référence documentaire
        mais des versions ou statuts différents — signal de contradiction à signaler à l'utilisateur."""
        by_reference: dict[str, list[dict[str, Any]]] = {}

        for citation in citations:
            reference = citation.get("reference")
            if not reference:
                continue
            by_reference.setdefault(reference, []).append(citation)

        contradictions: list[dict[str, Any]] = []

        for reference, group in by_reference.items():
            versions = {c.get("version") for c in group if c.get("version")}
            if len(group) < 2 or len(versions) < 2:
                continue

            current = next((c for c in group if c.get("document_status") == "current"), None)
            superseded = [c for c in group if c.get("document_status") != "current"]

            contradictions.append({
                "reference": reference,
                "versions_found": sorted(versions),
                "current_version": current.get("version") if current else None,
                "current_validated_date": current.get("validated_date") if current else None,
                "superseded_versions": [
                    {
                        "version": c.get("version"),
                        "validated_date": c.get("validated_date"),
                        "still_referenced_in": c.get("still_referenced_in"),
                    }
                    for c in superseded
                ],
            })

        return contradictions

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
        source_document = data.get("source_document")

        parts = [
            f"KNOWLEDGE_ID: {item.knowledge_id}",
            f"SCORE: {item.score:.1f}",
            f"TITLE: {title}"
        ]

        if isinstance(source_document, dict) and source_document:
            reference = source_document.get("reference", "")
            version = source_document.get("version", "")
            validated_date = source_document.get("validated_date", "")
            owner = source_document.get("owner", "")
            document_status = source_document.get("document_status", "")
            still_referenced_in = source_document.get("still_referenced_in") or []

            parts.append(
                f"SOURCE: {reference} — version {version}, validée le {validated_date}"
                f" (propriétaire : {owner or 'non renseigné'}, statut : {document_status or 'non renseigné'})"
            )
            if still_referenced_in:
                parts.append(
                    "ENCORE RÉFÉRENCÉ DANS : " + "; ".join(str(v) for v in still_referenced_in)
                )

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
        conversation_context: dict[str, Any],
        citations: list[dict[str, Any]] | None = None,
        contradictions: list[dict[str, Any]] | None = None
    ) -> str:

        citations = citations or []
        contradictions = contradictions or []

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

        if citations:
            sections.append("\n--- SOURCES ---")
            for citation in citations:
                sections.append(
                    f"- {citation.get('reference')} — version {citation.get('version')}, "
                    f"validée le {citation.get('validated_date')} "
                    f"(propriétaire : {citation.get('owner') or 'non renseigné'})"
                )

        if contradictions:
            sections.append("\n--- CONTRADICTIONS DETECTED ---")
            for contradiction in contradictions:
                superseded_desc = ", ".join(
                    f"v{s.get('version')} (validée le {s.get('validated_date')}, "
                    f"encore référencée dans : {', '.join(s.get('still_referenced_in') or []) or 'non précisé'})"
                    for s in contradiction.get("superseded_versions", [])
                )
                sections.append(
                    f"- {contradiction.get('reference')} : version actuelle "
                    f"{contradiction.get('current_version')} (validée le {contradiction.get('current_validated_date')}), "
                    f"mais version(s) antérieure(s) encore référencée(s) : {superseded_desc}"
                )

        if safety_notes:
            sections.append("\n--- SAFETY NOTES ---")
            for note in safety_notes[:8]:
                sections.append(f"- {note}")

        sections.append("\n--- INSTRUCTION DE RÉPONSE ---")
        # Traduit en français le 15/08/2026 : ce bloc était injecté tel quel
        # dans un system prompt sinon entièrement français (voir
        # response_generator.py::_build_knowledge_block) — un paragraphe
        # anglais isolé dans un prompt français déstabilisait le modèle local
        # (llama3.2), observé en conditions réelles comme une dérive en
        # charabia anglais incohérent.
        instruction = (
            "Utilise la connaissance sélectionnée pour répondre de façon claire, sûre et "
            "contextuelle. N'invente pas de connaissance absente de ce contexte. "
            "Si le sujet est médical, légal, financier ou à risque élevé, reste prudent."
        )
        if citations:
            instruction += (
                " Si une section SOURCES est présente, cite explicitement la référence du "
                "document, sa version et sa date de validation dans ta réponse."
            )
        if contradictions:
            instruction += (
                " Si une section CONTRADICTIONS DÉTECTÉES est présente, signale explicitement "
                "le conflit à l'utilisateur et recommande une validation par le propriétaire du "
                "document plutôt que de choisir une version toi-même."
            )
        sections.append(instruction)

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