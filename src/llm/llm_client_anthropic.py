"""
llm_client_anthropic.py
Client Anthropic (Claude) pour ALFRED.

Pré-requis :
    pip install anthropic python-dotenv

Variable d'environnement (.env) :
    ANTHROPIC_API_KEY=ta_cle_api
"""

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
    ) -> str:
        message = self.client.messages.create(
            model=self.model,
            max_tokens=self.max_output_tokens,
            temperature=self.temperature,
            system=system_prompt,
            messages=[
                {"role": "user", "content": user_prompt}
            ],
        )
        return message.content[0].text.strip()

    def is_available(self) -> bool:
        return self.client is not None
