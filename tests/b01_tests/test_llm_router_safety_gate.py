"""
════════════════════════════════════════════════════════════
PROJECT      : ALFRED
BLOCK        : B01
FUNCTION     : 01.04
FILE         : test_llm_router_safety_gate.py
ROLE         : Tests du branchement SafetyNet dans LLMRouter (src/llm/llm_router.py)

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-08-14
UPDATED      : 2026-08-14
VERSION      : V1.0
STATUS       : ACTIVE

DESCRIPTION :
Vérifie que LLMRouter.generate() refuse le repli cloud (OpenAI/Anthropic)
quand cloud_allowed=False, même si Ollama est indisponible et
allow_cloud_fallback=True — la politique de contenu prime sur la
disponibilité technique. Vérifie aussi la rétrocompatibilité (défaut
cloud_allowed=True) et le cas nominal où le repli reste autorisé.
════════════════════════════════════════════════════════════
"""

import pytest

from src.llm.llm_router import LLMRouter


class _FailingClient:
    """Simule Ollama indisponible : is_available() True mais generate() lève."""

    def is_available(self):
        return True

    def generate(self, **kwargs):
        raise RuntimeError("ollama down")


class _StubCloudClient:
    def __init__(self, label):
        self.label = label
        self.called = False

    def is_available(self):
        return True

    def generate(self, **kwargs):
        self.called = True
        return f"réponse de {self.label}"


def test_cloud_blocked_when_sensitive_even_if_ollama_down():
    openai = _StubCloudClient("openai")
    anthropic = _StubCloudClient("anthropic")
    router = LLMRouter(
        primary=_FailingClient(), secondary=openai, tertiary=anthropic,
        allow_cloud_fallback=True,
    )

    with pytest.raises(RuntimeError, match="SafetyNet"):
        router.generate("system", "prompt sensible", cloud_allowed=False)

    assert openai.called is False
    assert anthropic.called is False
    assert router.last_provider == "blocked_by_safety"


def test_cloud_fallback_still_works_when_allowed():
    openai = _StubCloudClient("openai")
    anthropic = _StubCloudClient("anthropic")
    router = LLMRouter(
        primary=_FailingClient(), secondary=openai, tertiary=anthropic,
        allow_cloud_fallback=True,
    )

    response = router.generate("system", "prompt neutre", cloud_allowed=True)

    assert response == "réponse de openai"
    assert openai.called is True
    assert router.last_provider == "openai"


def test_default_cloud_allowed_is_true_backward_compatible():
    openai = _StubCloudClient("openai")
    router = LLMRouter(
        primary=_FailingClient(), secondary=openai, tertiary=None,
        allow_cloud_fallback=True,
    )

    response = router.generate("system", "prompt sans cloud_allowed explicite")

    assert response == "réponse de openai"
