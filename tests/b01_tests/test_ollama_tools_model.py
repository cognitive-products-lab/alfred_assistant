"""
════════════════════════════════════════════════════════════
PROJECT      : ALFRED
BLOCK        : B01
FUNCTION     : 01.04
FILE         : test_ollama_tools_model.py
ROLE         : Tests de la sobriété modèle (tools_model) dans OllamaLLMClient

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-08-14
UPDATED      : 2026-08-14
VERSION      : V1.0
STATUS       : ACTIVE

DESCRIPTION :
Point P2 du chantier "sobriété/indépendance LLM externe"
(docs/architecture/vision_architecture_cognitive_alfred.md). Vérifie que
OllamaLLMClient peut utiliser un modèle dédié pour les tours function-calling
(tools=True) sans changer le comportement par défaut (tools_model absent =
même modèle pour tout, rétrocompatible). Aucun appel réseau réel — mock de
_run_tool_loop et inspection directe de _build_request().
════════════════════════════════════════════════════════════
"""

import json
from unittest.mock import patch

from src.llm.llm_client_ollama import OllamaLLMClient


def test_tools_model_defaults_to_model_when_not_set():
    client = OllamaLLMClient(model="llama3.2")

    assert client.tools_model == "llama3.2"


def test_tools_model_can_be_set_explicitly():
    client = OllamaLLMClient(model="llama3.2", tools_model="mistral:7b")

    assert client.tools_model == "mistral:7b"
    assert client.model == "llama3.2"


def test_build_request_uses_model_override_when_given():
    client = OllamaLLMClient(model="llama3.2")
    req = client._build_request(
        [{"role": "user", "content": "salut"}], stream=False, model="mistral:7b",
    )
    payload = json.loads(req.data.decode("utf-8"))

    assert payload["model"] == "mistral:7b"


def test_build_request_falls_back_to_self_model_without_override():
    client = OllamaLLMClient(model="llama3.2")
    req = client._build_request([{"role": "user", "content": "salut"}], stream=False)
    payload = json.loads(req.data.decode("utf-8"))

    assert payload["model"] == "llama3.2"


def test_profile_info_exposes_tools_model():
    client = OllamaLLMClient(model="llama3.2", tools_model="phi3:mini")

    assert client.profile_info()["tools_model"] == "phi3:mini"


def test_generate_with_tools_passes_tools_model_to_tool_loop():
    client = OllamaLLMClient(model="llama3.2", tools_model="mistral:7b")

    with patch.object(
        client, "_run_tool_loop",
        return_value=([], "réponse finale", True),
    ) as mocked_loop, patch(
        "src.core.tool_calling.openai_style_tools", return_value=[],
    ):
        client.generate(system_prompt="sys", user_prompt="planifie ma journée", tools=True)

    assert mocked_loop.call_args.kwargs["model"] == "mistral:7b"


def test_generate_with_tools_defaults_to_model_without_tools_model():
    client = OllamaLLMClient(model="llama3.2")

    with patch.object(
        client, "_run_tool_loop",
        return_value=([], "réponse finale", True),
    ) as mocked_loop, patch(
        "src.core.tool_calling.openai_style_tools", return_value=[],
    ):
        client.generate(system_prompt="sys", user_prompt="planifie ma journée", tools=True)

    assert mocked_loop.call_args.kwargs["model"] == "llama3.2"
