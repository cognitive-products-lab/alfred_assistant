"""
PROJECT      : ALFRED
BLOCK        : B01
FUNCTION     : XX.XX
FILE         : llm_router.py
ROLE         : TO_DEFINE

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-05-10
P26-05-12
VERSION      : V1.0
STATUS       : ACTIVE

DESCRIPTION :
TO_COMPLETE
"""
from __future__ import annotations

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


from typing import Any, Callable, Optional


class LLMRouter:
    def __init__(
        self,
        primary: Optional[Any] = None,
        secondary: Optional[Any] = None,
        tertiary: Optional[Any] = None,
        allow_cloud_fallback: bool = False,
        debug: bool = False,
    ):
        self.primary   = primary
        self.secondary = secondary
        self.tertiary  = tertiary     # 3e provider (ex: Anthropic)
        self.allow_cloud_fallback = allow_cloud_fallback
        self.debug = debug
        self.last_provider = "none"

    def _provider_label(self, client: Optional[Any]) -> str:
        """Retourne le label lisible d'un client LLM."""
        if client is None:
            return "none"
        if hasattr(client, "model_info"):
            info = client.model_info()
            return f"{info.get('provider', '?')}:{info.get('model', '?')}"
        model = getattr(client, "model", None)
        name  = type(client).__name__.lower()
        if "ollama" in name:
            return f"ollama:{model or 'local'}"
        if "openai" in name:
            return f"openai:{model or '?'}"
        if "anthropic" in name:
            return f"anthropic:{model or '?'}"
        return name

    def is_available(self) -> bool:
        return self._is_client_available(self.primary) or (
            self.allow_cloud_fallback and (
                self._is_client_available(self.secondary)
                or self._is_client_available(self.tertiary)
            )
        )

    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        previous_response_id: Optional[str] = None,
        on_sentence: Optional[Callable[[str], None]] = None,
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
                    on_sentence=on_sentence,
                )
            except Exception as exc:
                if self.debug:
                    print(f"⚠️ LLMRouter : Ollama KO pendant generate() — {exc}")

        if self.allow_cloud_fallback and self._is_client_available(self.secondary):
            try:
                self.last_provider = self._provider_label(self.secondary)
                if self.debug:
                    print(f"☁️ LLMRouter : utilisation {self.last_provider} (fallback)")
                return self.secondary.generate(
                    system_prompt=system_prompt,
                    user_prompt=user_prompt,
                    previous_response_id=previous_response_id,
                )
            except Exception as exc:
                if self.debug:
                    print(f"⚠️ LLMRouter : {self._provider_label(self.secondary)} KO — {exc}")

        if self.allow_cloud_fallback and self._is_client_available(self.tertiary):
            try:
                self.last_provider = self._provider_label(self.tertiary)
                if self.debug:
                    print(f"☁️ LLMRouter : utilisation {self.last_provider} (fallback 2)")
                return self.tertiary.generate(
                    system_prompt=system_prompt,
                    user_prompt=user_prompt,
                    previous_response_id=previous_response_id,
                )
            except Exception as exc:
                if self.debug:
                    print(f"⚠️ LLMRouter : {self._provider_label(self.tertiary)} KO — {exc}")

        self.last_provider = "none"
        raise RuntimeError(
            "Aucun moteur LLM disponible : Ollama, secondary et tertiary tous KO."
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
            "primary_available":   self._is_client_available(self.primary),
            "secondary_available": self._is_client_available(self.secondary),
            "tertiary_available":  self._is_client_available(self.tertiary),
            "allow_cloud_fallback": self.allow_cloud_fallback,
            "last_provider": self.last_provider,
            "secondary_label": self._provider_label(self.secondary),
            "tertiary_label":  self._provider_label(self.tertiary),
        }
