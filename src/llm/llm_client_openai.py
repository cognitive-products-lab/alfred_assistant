"""
PROJECT      : ALFRED
BLOCK        : B04
FUNCTION     : XX.XX
FILE         : src/llm/llm_client_openai.py
ROLE         : TO_DEFINE

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-06-03
UPDATED      : 2026-06-05
VERSION      : V1.1
STATUS       : VALIDATED

DESCRIPTION :
LLM Router Ollama/OpenAI — description a completer.
"""

"""
llm_client_openai.py
Client OpenAI pour ALFRED.

Pré-requis :
    pip install openai python-dotenv

Variable d'environnement (.env) :
    OPENAI_API_KEY=ta_cle_api
"""

import json
import os
from typing import Optional

from dotenv import load_dotenv
from openai import OpenAI


class OpenAILLMClient:

    def __init__(
        self,
        model: str = "gpt-4o",
        temperature: float = 0.4,
        max_output_tokens: int = 1200
    ):
        load_dotenv()
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY manquante dans .env")

        self.client = OpenAI(api_key=api_key)
        self.model = model
        self.temperature = temperature
        self.max_output_tokens = max_output_tokens

    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        previous_response_id: Optional[str] = None,
        on_sentence=None,
        tools: bool = False,
    ) -> str:
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]

        if tools:
            from src.core.tool_calling import openai_style_tools

            return self._run_tool_loop(messages, openai_style_tools())

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=self.temperature,
            max_tokens=self.max_output_tokens
        )
        return response.choices[0].message.content.strip()

    def _run_tool_loop(
        self,
        messages: list[dict],
        tools: list[dict],
        max_rounds: int = 3,
    ) -> str:
        """Boucle function-calling OpenAI — voir OllamaLLMClient._run_tool_loop
        pour le même principe côté modèle local."""
        from src.core.tool_calling import execute_tool

        for _ in range(max_rounds):
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=self.temperature,
                max_tokens=self.max_output_tokens,
                tools=tools,
            )
            message = response.choices[0].message

            if not message.tool_calls:
                return (message.content or "").strip()

            messages.append(message.model_dump())
            for call in message.tool_calls:
                try:
                    arguments = json.loads(call.function.arguments)
                except json.JSONDecodeError:
                    arguments = {}
                result = execute_tool(call.function.name, arguments)
                messages.append({
                    "role": "tool",
                    "tool_call_id": call.id,
                    "content": json.dumps(result, ensure_ascii=False),
                })

        return "Désolé, je n'ai pas réussi à finaliser cette action après plusieurs tentatives."

    def is_available(self) -> bool:
        """Vérifie que la clé API est présente et le client initialisé."""
        return self.client is not None
