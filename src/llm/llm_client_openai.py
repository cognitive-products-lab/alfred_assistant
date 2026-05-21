"""
llm_client_openai.py
Client OpenAI pour ALFRED.

Pré-requis :
    pip install openai python-dotenv

Variable d'environnement (.env) :
    OPENAI_API_KEY=ta_cle_api
"""

import os
from typing import Optional

from dotenv import load_dotenv
from openai import OpenAI


class OpenAILLMClient:

    def __init__(
        self,
        model: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        temperature: float = float(os.getenv("OPENAI_TEMPERATURE", "0.4")),
        max_output_tokens: int = int(os.getenv("OPENAI_MAX_TOKENS", "1200"))
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
        previous_response_id: Optional[str] = None
    ) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=self.temperature,
            max_tokens=self.max_output_tokens
        )
        return response.choices[0].message.content.strip()

    def is_available(self) -> bool:
        """Vérifie que la clé API est présente et le client initialisé."""
        return self.client is not None
