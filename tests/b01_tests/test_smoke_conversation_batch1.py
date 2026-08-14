"""
PROJECT      : ALFRED
BLOCK        : B01
FUNCTION     : SMOKE
FILE         : tests/b01_tests/test_smoke_conversation_batch1.py
ROLE         : Smoke tests (import + comportement de base) pour un premier lot
               de fichiers B01 sans couverture de test existante.

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-07-05
UPDATED      : 2026-07-05
VERSION      : V1.0
STATUS       : TESTED

DESCRIPTION :
Verifie que chaque module s'importe et que ses fonctions/classes publiques
s'executent sans lever d'exception inattendue, avec des assertions minimales
sur la forme du retour. Ne remplace pas une suite de tests comportementale
complete (pas d'assertion fine sur toute la logique metier).
"""

import pytest

from src.conversation.input import audio_capture
from src.conversation.nlp import nlp_engine_v2 as conv_nlp_engine_v2
from src.conversation.input.speech_manager import SpeechManager
from src.conversation.input import text_input
from src.conversation.input.audio_listener import AudioListener
from src.conversation.nlp.intent_classifier import IntentClassifier
from src.conversation.input.input_manager import HybridInputManager
from src.conversation.input import nlp_engine_v2 as input_nlp_engine_v2
from src.conversation.nlp import nlp_engine
from src.conversation.output import tts_output


# ── audio_capture (stub V1) ──────────────────────────────

def test_audio_capture_status_and_availability():
    assert audio_capture.is_audio_available() is False
    assert audio_capture.activate_wake_word_detection() is False
    status = audio_capture.get_audio_status()
    assert status["available"] is False
    assert status["version"] == "stub_v1"


def test_audio_capture_raises_not_available():
    with pytest.raises(audio_capture.AudioCaptureNotAvailable):
        audio_capture.capture_audio()


# ── conversation/nlp/nlp_engine_v2 (analyse simplifiee) ──

def test_conv_nlp_engine_v2_stressed():
    result = conv_nlp_engine_v2.analyze_v2("je suis en stress total, marre de tout")
    assert result["emotion"] == "stressed"
    # IntentNet rebranché le 14/08/2026 (P1) — l'intention n'est plus
    # hardcodée à "conversation", voir tests/b01_tests/test_intent_net_wiring.py
    assert result["intent"] == "emotional_support"


def test_conv_nlp_engine_v2_neutral_default():
    result = conv_nlp_engine_v2.analyze_v2("il fait beau aujourd'hui")
    assert result["emotion"] == "neutral"
    assert result["entities"] == []


# ── speech_manager (orchestrateur, sans STT/TTS reels) ──

def test_speech_manager_init_and_status(capsys):
    manager = SpeechManager(user_name="Test")
    status = manager.get_status()
    assert status["mode"] in ("text", "tts_only", "voice")
    assert "stt_ready" in status and "tts_ready" in status
    assert "SpeechManager(" in repr(manager)
    capsys.readouterr()  # consomme les messages display_system


def test_speech_manager_listen_falls_back_to_text(monkeypatch):
    manager = SpeechManager(user_name="Test")
    monkeypatch.setattr("builtins.input", lambda prompt="": "bonjour")
    assert manager.listen() == "bonjour"


# ── text_input (saisie + historique session) ───────────

def test_text_input_validation_and_exit_commands():
    assert text_input.is_valid_input("bonjour") is True
    assert text_input.is_valid_input("   ") is False
    assert text_input.is_exit_command("exit") is True
    assert text_input.is_exit_command("bonjour") is False


def test_text_input_read_user_input_returns_string(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda prompt="": "bonjour")
    result = text_input.read_user_input()
    assert isinstance(result, str)
    assert result == "bonjour"


def test_text_input_history_roundtrip():
    text_input.clear_history()
    assert text_input.history_count() == 0
    text_input.add_to_history("salut", "bonjour !")
    assert text_input.history_count() == 1
    last = text_input.get_last_exchanges(1)
    assert last[0]["user"] == "salut"
    text_input.clear_history()


# ── audio_listener (facade simulation) ──────────────────

def test_audio_listener_simulation_mode(monkeypatch):
    listener = AudioListener(mode="simulation")
    monkeypatch.setattr("builtins.input", lambda prompt="": "ping")
    assert listener.listen() == "ping"


def test_audio_listener_unsupported_mode_returns_none():
    listener = AudioListener(mode="bogus")
    assert listener.listen() is None


def test_audio_listener_audio_capture_not_implemented():
    listener = AudioListener(mode="audio_capture")
    with pytest.raises(NotImplementedError):
        listener._listen_audio_capture()


# ── intent_classifier (regles simples) ──────────────────

def test_intent_classifier_rules():
    clf = IntentClassifier()
    assert clf.classify("Bonjour Alfred") == "greeting"
    assert clf.classify("rappelle-moi d'appeler") == "task"
    assert clf.classify("xyz sans rapport") == "fallback"


# ── input_manager (queue hybride, sans lancer les threads) ──

def test_hybrid_input_manager_queue_without_threads():
    manager = HybridInputManager(voice_func=lambda: "")
    assert manager.running is False
    manager.inputs.put(("keyboard", "test"))
    assert manager.get_input() == ("keyboard", "test")


# ── conversation/input/nlp_engine_v2 (pipeline complet V2) ──

def test_input_nlp_engine_v2_language_and_emotion():
    assert input_nlp_engine_v2.detect_language("bonjour comment vas-tu") == "fr"
    assert input_nlp_engine_v2.detect_language("hello how are you") == "en"
    emotion = input_nlp_engine_v2.detect_emotion("je suis fatiguée et épuisée")
    assert emotion["emotion"] == "tired"


def test_input_nlp_engine_v2_analyze_full_pipeline():
    result = input_nlp_engine_v2.analyze_v2("bonjour, comment planifier ma journée ?")
    assert result["method"] == "keyword_v2"
    assert "intent" in result and "emotion" in result and "language" in result


def test_input_nlp_engine_v2_vocal_mode():
    # emotion absente du mapping -> fallback sur l'intent
    analysis = {"emotion": "curious", "intent": "greeting"}
    assert input_nlp_engine_v2.get_vocal_mode_from_analysis(analysis) == "complicite"
    # emotion presente dans le mapping -> priorite a l'emotion sur l'intent
    analysis = {"emotion": "stressed", "intent": "greeting"}
    assert input_nlp_engine_v2.get_vocal_mode_from_analysis(analysis) == "support"


# ── conversation/nlp/nlp_engine (V1 regles + entites) ───

def test_nlp_engine_detect_intent_and_entities():
    result = nlp_engine.detect_intent("organiser mon planning de demain")
    assert result["intent"] == "organization"
    entities = nlp_engine.extract_entities("rendez-vous demain à 14h30")
    assert "demain" in entities.get("dates", [])
    assert "14h30" in entities.get("times", [])


def test_nlp_engine_analyze_and_label():
    result = nlp_engine.analyze("bonjour Alfred")
    assert result["intent"] == "greeting"
    assert nlp_engine.get_intent_label("greeting") == "Salutation"


# ── conversation/output/tts_output (affichage terminal V1) ──

def test_tts_output_display_and_status(capsys):
    tts_output.display_response("Bonjour")
    tts_output.display_system("info")
    tts_output.display_welcome("Céline", "Bonjour", "matin")
    tts_output.display_goodbye("Céline")
    tts_output.display_error("oups")
    tts_output.display_session_summary(3)
    out = capsys.readouterr()
    assert "ALFRED" in out.out

    assert tts_output.is_tts_available() is False
    status = tts_output.get_tts_status()
    assert status["available"] is False

    tts_output.speak("test vocal")
