"""
PROJECT      : ALFRED
BLOCK        : B01
FILE         : llm_client_anthropic.py
ROLE         : Client Anthropic Claude pour ALFRED — fallback cloud

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-06-03
VERSION      : V1.0
STATUS       : ACTIVE

DESCRIPTION :
Client Anthropic Claude pour ALFRED.
Même interface que OpenAILLMClient (generate / is_available).
Utilisé comme fallback cloud dans LLMRouter.

Pré-requis :
    pip install anthropic python-dotenv

Variable d'environnement (.env) :
    ANTHROPIC_API_KEY=sk-ant-...

Modèles recommandés :
    claude-haiku-4-5          → rapide, économique (fallback léger)
    claude-3-5-haiku-20241022 → haiku stable
    claude-sonnet-4-5         → qualité supérieure (plus cher)
    claude-3-5-sonnet-20241022→ sonnet stable
"""

from __future__ import annotations

import os
from typing import Optional

from pathlib import Path as _Path
from dotenv import load_dotenv, find_dotenv


class AnthropicLLMClient:
    """
    Client Anthropic Claude pour ALFRED.

    Interface identique à OpenAILLMClient pour être interchangeable
    dans LLMRouter (primary / secondary / tertiary).
    """

    def __init__(
        self,
        model: str = "claude-haiku-4-5",
        temperature: float = 0.4,
        max_output_tokens: int = 1200,
    ) -> None:
        # Cherche .env depuis la racine du projet (2 niveaux au-dessus de src/llm/)
        _root_env = _Path(__file__).resolve().parents[2] / ".env"
        if _root_env.exists():
            load_dotenv(_root_env, override=True)
        else:
            load_dotenv(find_dotenv(usecwd=False), override=True)
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY manquante dans .env")

        try:
            import anthropic as _anthropic
            self._anthropic = _anthropic
            self.client = _anthropic.Anthropic(api_key=api_key)
        except ImportError as exc:
            raise ImportError(
                "Package 'anthropic' manquant. Installe-le : pip install anthropic"
            ) from exc

        self.model = model
        self.temperature = temperature
        self.max_output_tokens = max_output_tokens

    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        previous_response_id: Optional[str] = None,   # ignoré (pas de continuité Anthropic V1)
        on_sentence=None,                               # ignoré (pas de streaming V1)
    ) -> str:
        """
        Génère une réponse via Anthropic Claude.

        Args:
            system_prompt : Instructions système ALFRED
            user_prompt   : Message utilisateur enrichi
            previous_response_id : Non utilisé (compatibilité interface)
            on_sentence          : Non utilisé (compatibilité interface)

        Returns:
            Texte de la réponse
        """
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
        """Vérifie que le client est initialisé."""
        return self.client is not None

    def model_info(self) -> dict:
        """Retourne les infos du modèle actif."""
        return {
            "provider":   "anthropic",
            "model":      self.model,
            "temperature": self.temperature,
            "max_tokens": self.max_output_tokens,
        }
