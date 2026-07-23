# ============================================================
# ALFRED — src/llm/llm_client_anthropic.py
# Bloc 01.04c — Client LLM Anthropic (priorité 3)
# Version : 1.0 — 2026-06-18
#
# 📚 NOTION EXAM :
#   D52-1 — Capsule 5 : Routage LLM — local-first, fallback cloud
#
# 🎯 UTILITÉ ALFRED :
#   Client Anthropic Claude — fallback tertiary (Ollama → OpenAI → Claude).
#   Requiert ANTHROPIC_API_KEY dans .env.
#   pip install anthropic python-dotenv
#
# 🏗️ DOMAINE :
#   Noyau conversationnel — LLM cloud tertiary
#
# STATUS  : VALIDATED
# ============================================================

import json
import os
from typing import Optional

from dotenv import load_dotenv


class AnthropicLLMClient:

    def __init__(
        self,
        model: str = "claude-sonnet-4-6",
        temperature: float = 0.4,
        max_output_tokens: int = 1200,
    ):
        load_dotenv()
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY manquante dans .env")

        try:
            import anthropic
            self.client = anthropic.Anthropic(api_key=api_key)
        except ImportError:
            raise ImportError("Package 'anthropic' manquant — pip install anthropic")

        self.model = model
        self.temperature = temperature
        self.max_output_tokens = max_output_tokens

    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        previous_response_id: Optional[str] = None,
        tools: bool = False,
    ) -> str:
        messages = [{"role": "user", "content": user_prompt}]

        if tools:
            from src.core.tool_calling import anthropic_style_tools

            return self._run_tool_loop(system_prompt, messages, anthropic_style_tools())

        message = self.client.messages.create(
            model=self.model,
            max_tokens=self.max_output_tokens,
            temperature=self.temperature,
            system=system_prompt,
            messages=messages,
        )
        return message.content[0].text.strip()

    def _run_tool_loop(
        self,
        system_prompt: str,
        messages: list[dict],
        tools: list[dict],
        max_rounds: int = 3,
    ) -> str:
        """Boucle function-calling Anthropic — voir OllamaLLMClient._run_tool_loop
        pour le même principe côté modèle local."""
        from src.core.tool_calling import execute_tool

        for _ in range(max_rounds):
            message = self.client.messages.create(
                model=self.model,
                max_tokens=self.max_output_tokens,
                temperature=self.temperature,
                system=system_prompt,
                messages=messages,
                tools=tools,
            )

            if message.stop_reason != "tool_use":
                text_blocks = [b.text for b in message.content if b.type == "text"]
                return "".join(text_blocks).strip()

            messages.append({"role": "assistant", "content": message.content})
            tool_results = []
            for block in message.content:
                if block.type != "tool_use":
                    continue
                result = execute_tool(block.name, block.input or {})
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": json.dumps(result, ensure_ascii=False),
                })
            messages.append({"role": "user", "content": tool_results})

        return "Désolé, je n'ai pas réussi à finaliser cette action après plusieurs tentatives."

    def is_available(self) -> bool:
        return self.client is not None
