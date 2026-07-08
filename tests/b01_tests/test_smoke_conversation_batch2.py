"""
PROJECT      : ALFRED
BLOCK        : B01
FUNCTION     : SMOKE
FILE         : tests/b01_tests/test_smoke_conversation_batch2.py
ROLE         : Smoke tests (lot 2) pour les fichiers B01 restants sans
               couverture de test (clients LLM, routeur, entree point V3,
               config/donnees JSON).

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-07-05
UPDATED      : 2026-07-05
VERSION      : V1.0
STATUS       : TESTED

DESCRIPTION :
Verifie import + comportement de base des modules, sans dependance reseau
reelle (clients LLM mockes). Ne remplace pas une suite comportementale
complete.
"""

import json
from pathlib import Path

import pytest

from src.input import audio_capture as input_audio_capture
from src.llm.llm_client_anthropic import AnthropicLLMClient
from src.llm.llm_router import LLMRouter
from src.llm.vision_client_ollama import OllamaVisionClient
from src import main_v3
import src.alfred_with_ui as alfred_with_ui

ROOT = Path(__file__).resolve().parents[2]


# ── src/input/audio_capture.py (sounddevice, avec fallback) ─

def test_input_audio_capture_returns_bool():
    assert isinstance(input_audio_capture.is_audio_available(), bool)


# ── src/llm/llm_client_anthropic.py (mocke, pas d'appel reseau) ─

def test_anthropic_client_missing_key_raises(monkeypatch):
    monkeypatch.setattr(
        "src.llm.llm_client_anthropic.load_dotenv", lambda *a, **k: None
    )
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    with pytest.raises(ValueError):
        AnthropicLLMClient()


def test_anthropic_client_generate_mocked(monkeypatch):
    class FakeContentBlock:
        def __init__(self, text):
            self.text = text

    class FakeMessage:
        def __init__(self, text):
            self.content = [FakeContentBlock(text)]

    class FakeMessages:
        def create(self, **kwargs):
            return FakeMessage("  réponse simulée  ")

    class FakeAnthropic:
        def __init__(self, api_key):
            self.messages = FakeMessages()

    monkeypatch.setattr(
        "src.llm.llm_client_anthropic.load_dotenv", lambda *a, **k: None
    )
    monkeypatch.setenv("ANTHROPIC_API_KEY", "fake-key-for-tests")
    monkeypatch.setattr("anthropic.Anthropic", FakeAnthropic)

    client = AnthropicLLMClient()
    assert client.is_available() is True
    assert client.generate("system", "user") == "réponse simulée"


# ── src/llm/llm_router.py (fakes, sans reseau) ──────────────

class _FakeLLMClient:
    def __init__(self, name, available=True):
        self.name = name
        self._available = available
        self.calls = []

    def is_available(self):
        return self._available

    def generate(self, system_prompt, user_prompt, previous_response_id=None, **kwargs):
        self.calls.append((system_prompt, user_prompt))
        return f"réponse de {self.name}"


def test_llm_router_uses_primary_when_available():
    router = LLMRouter(primary=_FakeLLMClient("ollama"))
    assert router.is_available() is True
    assert router.generate("sys", "hello") == "réponse de ollama"
    assert router.last_provider == "ollama"


def test_llm_router_falls_back_to_secondary_on_primary_failure():
    class FailingClient(_FakeLLMClient):
        def generate(self, *a, **k):
            raise RuntimeError("ollama down")

    router = LLMRouter(
        primary=FailingClient("ollama"),
        secondary=_FakeLLMClient("openai"),
        allow_cloud_fallback=True,
    )
    assert router.generate("sys", "hello") == "réponse de openai"
    assert router.last_provider == "openai"


def test_llm_router_raises_when_nothing_available():
    router = LLMRouter(primary=None, secondary=None, tertiary=None)
    with pytest.raises(RuntimeError):
        router.generate("sys", "hello")


def test_llm_router_provider_status_shape():
    router = LLMRouter(primary=_FakeLLMClient("ollama"))
    status = router.provider_status()
    assert status["primary_available"] is True
    assert status["last_provider"] == "none"  # generate() pas encore appelé


# ── src/llm/vision_client_ollama.py (hote injoignable, pas de reseau reel) ─

def test_vision_client_unavailable_on_unreachable_host():
    client = OllamaVisionClient(base_url="http://127.0.0.1:1", timeout=1)
    assert client.is_available() is False


def test_vision_client_analyze_image_raises_on_unreachable_host():
    client = OllamaVisionClient(base_url="http://127.0.0.1:1", timeout=1)
    with pytest.raises(ConnectionError):
        client.analyze_image("ZmFrZQ==", "Décris cette image.")


# ── src/main_v3.py (fonctions pures uniquement) ─────────────

def test_main_v3_sanitize_input():
    assert main_v3.sanitize_input("   ") == ""
    assert main_v3.sanitize_input("bonjour") == "bonjour"
    long_input = "a" * (main_v3.MAX_INPUT_LENGTH + 50)
    assert len(main_v3.sanitize_input(long_input)) == main_v3.MAX_INPUT_LENGTH


def test_main_v3_clean_for_tts():
    assert main_v3.clean_for_tts("Attention ⚠️ !") == "Attention Attention. !"
    assert main_v3.clean_for_tts("l’heure") == "l'heure"


def test_main_v3_safe_getattr():
    class Obj:
        value = 42

    assert main_v3.safe_getattr(Obj(), "value") == 42
    assert main_v3.safe_getattr(Obj(), "missing", "default") == "default"


# ── src/alfred_with_ui.py (retry logic, sans lancer Kivy/tkinter) ─

def test_alfred_with_ui_pipeline_retries_on_failure(monkeypatch, capsys):
    attempts = {"count": 0}

    def failing_main():
        attempts["count"] += 1
        raise RuntimeError("crash simulé")

    monkeypatch.setattr("src.main.main", failing_main)
    monkeypatch.setattr(alfred_with_ui, "_RESTART_DELAY", 0.0)

    alfred_with_ui._run_pipeline()

    assert attempts["count"] == alfred_with_ui._MAX_RESTARTS


def test_alfred_with_ui_pipeline_stops_on_success(monkeypatch):
    attempts = {"count": 0}

    def ok_main():
        attempts["count"] += 1

    monkeypatch.setattr("src.main.main", ok_main)
    alfred_with_ui._run_pipeline()

    assert attempts["count"] == 1


# ── config/conversation_rules.json + data/memory (fichiers de config/donnees) ─

def test_conversation_rules_json_structure():
    data = json.loads((ROOT / "config" / "conversation_rules.json").read_text(encoding="utf-8"))
    assert "general_rules" in data
    assert "discussion_modes" in data


def test_dialogue_history_json_is_valid_list():
    data = json.loads(
        (ROOT / "data" / "memory" / "episodic" / "dialogue_history.json").read_text(encoding="utf-8")
    )
    assert isinstance(data, list)
