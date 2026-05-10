# -*- coding: utf-8 -*-
"""
llm_router.py — Routeur LLM ALFRED

Ordre de priorité :
1. Ollama local
2. OpenAI cloud si autorisé et disponible
3. Erreur explicite si aucun moteur disponible

Objectif :
- Garder ALFRED local-first
- Éviter le fallback silencieux
- Tracer clairement quel moteur répond
"""

from __future__ import annotations

from typing import Any, Optional


class LLMRouter:
    def __init__(
        self,
        primary: Optional[Any] = None,
        secondary: Optional[Any] = None,
        allow_cloud_fallback: bool = False,
        debug: bool = False,
    ):
        self.primary = primary
        self.secondary = secondary
        self.allow_cloud_fallback = allow_cloud_fallback
        self.debug = debug
        self.last_provider = "none"

    def is_available(self) -> bool:
        return self._is_client_available(self.primary) or (
            self.allow_cloud_fallback and self._is_client_available(self.secondary)
        )

    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        previous_response_id: Optional[str] = None,
    ) -> str:
        if self._is_client_available(self.primary):
            try:
                self.last_provider = "ollama"
                if self.debug:
                    print("🧠 LLMRouter : utilisation Ollama local")
                return self.primary.generate(
                    system_prompt=system_prompt,
                    user_prompt=user_prompt,
                    previous_response_id=previous_response_id,
                )
            except Exception as exc:
                if self.debug:
                    print(f"⚠️ LLMRouter : Ollama KO pendant generate() — {exc}")

        if self.allow_cloud_fallback and self._is_client_available(self.secondary):
            try:
                self.last_provider = "openai"
                if self.debug:
                    print("☁️ LLMRouter : utilisation OpenAI fallback")
                return self.secondary.generate(
                    system_prompt=system_prompt,
                    user_prompt=user_prompt,
                    previous_response_id=previous_response_id,
                )
            except Exception as exc:
                if self.debug:
                    print(f"⚠️ LLMRouter : OpenAI KO pendant generate() — {exc}")

        self.last_provider = "none"
        raise RuntimeError(
            "Aucun moteur LLM disponible : Ollama KO et OpenAI indisponible ou désactivé."
        )

    def _is_client_available(self, client: Optional[Any]) -> bool:
        if client is None:
            return False

        if not hasattr(client, "is_available"):
            return True

        try:
            return bool(client.is_available())
        except Exception:
            return False

    def provider_status(self) -> dict[str, Any]:
        return {
            "primary_available": self._is_client_available(self.primary),
            "secondary_available": self._is_client_available(self.secondary),
            "allow_cloud_fallback": self.allow_cloud_fallback,
            "last_provider": self.last_provider,
        }
