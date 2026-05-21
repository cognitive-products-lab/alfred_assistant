# -*- coding: utf-8 -*-
"""
context_builder.py — ALFRED V3
Assemble le contexte supplémentaire à injecter dans le prompt LLM.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional


class ContextBuilder:
    """
    Construit un bloc textuel enrichi pour le prompt système :
    RAG sémantique + knowledge routing + wellbeing hint.
    Ces éléments viennent s'ajouter au contexte standard de ResponseGenerator.
    """

    def build_extra_system_block(
        self,
        rag_results: Optional[List[Dict[str, Any]]] = None,
        knowledge_context: Optional[Dict[str, Any]] = None,
        wellbeing_suggestion: Optional[str] = None,
        state_dict: Optional[Dict[str, Any]] = None,
    ) -> str:
        blocks: List[str] = []

        rag_block = self._format_rag(rag_results or [])
        if rag_block:
            blocks.append(rag_block)

        know_block = self._format_knowledge(knowledge_context or {})
        if know_block:
            blocks.append(know_block)

        if wellbeing_suggestion:
            blocks.append(f"[Suggestion bien-être] {wellbeing_suggestion}")

        if state_dict:
            mode = state_dict.get("current_mode", "")
            emotion = state_dict.get("current_emotion", "")
            if mode or emotion:
                blocks.append(f"[État session] Mode : {mode} | Émotion : {emotion}")

        return "\n\n".join(blocks)

    # ── Formateurs privés ─────────────────────────────────

    def _format_rag(self, results: List[Dict[str, Any]]) -> str:
        if not results:
            return ""
        lines = ["[Mémoire sémantique pertinente]"]
        for r in results[:3]:
            doc = r.get("document", "").strip()
            score = r.get("score", 0.0)
            if doc:
                lines.append(f"• (pertinence {score:.2f}) {doc[:250]}")
        return "\n".join(lines) if len(lines) > 1 else ""

    def _format_knowledge(self, ctx: Dict[str, Any]) -> str:
        if not ctx:
            return ""
        # Format RetrievalEngine result
        prompt_block = ctx.get("prompt_block", "")
        if prompt_block:
            return str(prompt_block)[:600]
        # Format legacy dict
        domain = ctx.get("domain", "")
        content = ctx.get("content", "")
        if not content:
            return ""
        header = f"[Knowledge — {domain}]" if domain else "[Knowledge]"
        return f"{header}\n{str(content)[:400]}"
