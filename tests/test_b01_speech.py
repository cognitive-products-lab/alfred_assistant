# ============================================================
# ALFRED — tests/test_b01_speech.py
# Tests Bloc 01 — Interaction conversationnelle V1 → V3
#
# Lancer :
#   cd D:\PROJET_ALFRED\ALFRED_PC
#   .venv\Scripts\Activate.ps1
#   pytest tests/test_b01_speech.py -v
# ============================================================

import sys
from pathlib import Path

# Assure que src/ est dans le path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


# ─────────────────────────────────────────────────────────
# Tests B01.02 — text_input.py
# ─────────────────────────────────────────────────────────

class TestTextInput:

    def test_is_valid_input_ok(self):
        from src.input.text_input import is_valid_input
        assert is_valid_input("Bonjour Alfred") is True

    def test_is_valid_input_empty(self):
        from src.input.text_input import is_valid_input
        assert is_valid_input("") is False
        assert is_valid_input("   ") is False

    def test_is_valid_input_too_long(self):
        from src.input.text_input import is_valid_input
        assert is_valid_input("x" * 1001) is False

    def test_is_exit_command(self):
        from src.input.text_input import is_exit_command
        assert is_exit_command("exit") is True
        assert is_exit_command("quitter") is True
        assert is_exit_command("bye") is True
        assert is_exit_command("bonjour") is False

    def test_history_add_and_get(self):
        from src.input.text_input import (
            add_to_history, get_history,
            get_last_exchanges, clear_history, history_count
        )
        clear_history()
        assert history_count() == 0

        add_to_history("Bonjour", "Bonjour Céline !")
        add_to_history("Comment tu vas ?", "Très bien merci.")
        assert history_count() == 2

        history = get_history()
        assert history[0]["user"] == "Bonjour"
        assert history[1]["alfred"] == "Très bien merci."

        last = get_last_exchanges(1)
        assert len(last) == 1
        assert last[0]["user"] == "Comment tu vas ?"

        clear_history()
        assert history_count() == 0


# ─────────────────────────────────────────────────────────
# Tests B01.04 — nlp_engine.py
# ─────────────────────────────────────────────────────────

class TestNLPEngine:

    def test_intent_organisation(self):
        from src.input.nlp_engine import detect_intent
        result = detect_intent("je veux organiser mon planning de la semaine")
        assert result["intent"] == "organization"
        assert result["score"] > 0

    def test_intent_emotional_support(self):
        from src.input.nlp_engine import detect_intent
        result = detect_intent("je suis stressée et fatiguée")
        assert result["intent"] == "emotional_support"

    def test_intent_engineering(self):
        from src.input.nlp_engine import detect_intent
        result = detect_intent("j'ai un bug dans mon code python")
        assert result["intent"] == "engineering"

    def test_intent_greeting(self):
        from src.input.nlp_engine import detect_intent
        result = detect_intent("bonjour alfred")
        assert result["intent"] == "greeting"

    def test_intent_general_fallback(self):
        from src.input.nlp_engine import detect_intent
        result = detect_intent("xkjf zqwer")
        assert result["intent"] == "general"

    def test_entities_dates(self):
        from src.input.nlp_engine import extract_entities
        result = extract_entities("on se voit demain matin")
        assert "dates" in result
        assert "demain" in result["dates"]
        assert "ce matin" in result["dates"] or "matin" in str(result)

    def test_entities_time(self):
        from src.input.nlp_engine import extract_entities
        result = extract_entities("rendez-vous à 14h30")
        assert "times" in result
        assert "14h30" in result["times"]

    def test_entities_numbers(self):
        from src.input.nlp_engine import extract_entities
        result = extract_entities("j'ai 3 réunions demain")
        assert "numbers" in result
        assert 3 in result["numbers"]

    def test_analyze_full(self):
        from src.input.nlp_engine import analyze
        result = analyze("je suis fatiguée, j'ai 5 réunions demain")
        assert "intent" in result
        assert "entities" in result
        assert "timestamp" in result
        assert result["method"] == "keyword_v1"


# ─────────────────────────────────────────────────────────
# Tests B01.04 V2 — nlp_engine_v2.py
# ─────────────────────────────────────────────────────────

class TestNLPEngineV2:

    def test_detect_emotion_stressed(self):
        from src.input.nlp_engine_v2 import detect_emotion
        result = detect_emotion("je suis stressée et débordée")
        assert result["emotion"] == "stressed"
        assert result["score"] > 0

    def test_detect_emotion_neutral(self):
        from src.input.nlp_engine_v2 import detect_emotion
        result = detect_emotion("montre-moi mon planning")
        assert result["emotion"] == "neutral"

    def test_detect_language_fr(self):
        from src.input.nlp_engine_v2 import detect_language
        assert detect_language("je veux organiser ma journée") == "fr"

    def test_detect_language_en(self):
        from src.input.nlp_engine_v2 import detect_language
        assert detect_language("I want to organize my day") == "en"

    def test_analyze_v2_full(self):
        from src.input.nlp_engine_v2 import analyze_v2
        result = analyze_v2("je suis fatiguée et stressée ce soir")
        assert result["intent"] == "emotional_support"
        assert result["emotion"] in ["stressed", "tired"]
        assert result["language"] == "fr"
        assert "confidence" in result
        assert result["method"] == "keyword_v2"

    def test_vocal_mode_from_analysis_support(self):
        from src.input.nlp_engine_v2 import analyze_v2, get_vocal_mode_from_analysis
        analysis = analyze_v2("je suis stressée et débordée")
        mode = get_vocal_mode_from_analysis(analysis)
        assert mode == "support"

    def test_vocal_mode_from_analysis_focus(self):
        from src.input.nlp_engine_v2 import analyze_v2, get_vocal_mode_from_analysis
        analysis = analyze_v2("j'ai un bug dans mon code python")
        mode = get_vocal_mode_from_analysis(analysis)
        assert mode == "focus"


# ─────────────────────────────────────────────────────────
# Tests B01.05 — context_builder.py
# ─────────────────────────────────────────────────────────

class TestContextBuilder:

    def test_time_context_keys(self):
        from src.input.context_builder import get_time_context
        ctx = get_time_context()
        assert "time" in ctx
        assert "period" in ctx
        assert "energy_level" in ctx
        assert "greeting" in ctx
        assert ctx["energy_level"] in ["high", "medium", "low"]
        assert ctx["period"] in ["matin", "midi", "après-midi", "soirée", "nuit"]

    def test_device_context(self):
        from src.input.context_builder import get_device_context
        ctx = get_device_context("test_pc")
        assert ctx["device_id"] == "test_pc"
        assert ctx["device_type"] == "desktop"
        assert "os" in ctx

    def test_conversation_context_empty(self):
        from src.input.context_builder import get_conversation_context
        ctx = get_conversation_context([])
        assert ctx["is_first_message"] is True
        assert ctx["conversation_stage"] == "opening"

    def test_conversation_context_active(self):
        from src.input.context_builder import get_conversation_context
        history = [{"user": f"msg {i}", "alfred": "ok"} for i in range(5)]
        ctx = get_conversation_context(history)
        assert ctx["conversation_stage"] == "active"
        assert ctx["exchange_count"] == 5

    def test_build_context_complete(self):
        from src.input.context_builder import build_context
        ctx = build_context(history=[], user_name="Céline")
        assert ctx["user_name"] == "Céline"
        assert "time" in ctx
        assert "device" in ctx
        assert "conversation" in ctx
        assert "greeting" in ctx

    def test_format_context_for_prompt(self):
        from src.input.context_builder import build_context, format_context_for_prompt
        ctx = build_context([], "Céline")
        text = format_context_for_prompt(ctx)
        assert "Céline" in text
        assert "[Contexte session]" in text


# ─────────────────────────────────────────────────────────
# Tests B01 V3 — voice_profile.py
# ─────────────────────────────────────────────────────────

class TestVoiceProfile:

    def test_get_voice_params_modes(self):
        from src.input.voice_profile import get_voice_params
        for mode in ["support", "focus", "challenge", "complicite", "default"]:
            params = get_voice_params(mode)
            assert 0.5 <= params.length_scale <= 1.5
            assert 0.0 <= params.noise_scale <= 1.0
            assert params.speaker_id == 1  # Pierre

    def test_get_voice_params_emotion(self):
        from src.input.voice_profile import get_voice_params
        params_stressed = get_voice_params("stressed")
        params_focus    = get_voice_params("focused")
        # Stressed → support (plus lent)
        assert params_stressed.length_scale > params_focus.length_scale

    def test_get_mode_from_energy(self):
        from src.input.voice_profile import get_mode_from_energy
        assert get_mode_from_energy("high")   == "focus"
        assert get_mode_from_energy("low")    == "support"
        assert get_mode_from_energy("medium") == "complicite"


# ─────────────────────────────────────────────────────────
# Tests B01 V3 — stt_whisper.py (sans micro)
# ─────────────────────────────────────────────────────────

class TestSTTWhisper:

    def test_status_structure(self):
        from src.input.stt_whisper import get_stt_status
        status = get_stt_status()
        assert "available" in status
        assert "model_size" in status
        assert "wake_word" in status
        assert status["wake_word"] == "alfred"

    def test_wake_word_detection(self):
        from src.input.stt_whisper import detect_wake_word
        assert detect_wake_word("hey Alfred, comment ça va ?") is True
        assert detect_wake_word("ALFRED aide-moi") is True
        assert detect_wake_word("bonjour comment vas-tu") is False


# ─────────────────────────────────────────────────────────
# Tests B01 V3 — tts_piper.py (sans lecture audio)
# ─────────────────────────────────────────────────────────

class TestTTSPiper:

    def test_status_structure(self):
        from src.output.tts_piper import get_tts_status
        status = get_tts_status()
        assert "available" in status
        assert "model" in status
        assert status["model"] == "fr_FR-upmc-medium"
        assert status["speaker"] == "pierre"
        assert status["speaker_id"] == 1

    def test_is_tts_available_returns_bool(self):
        from src.output.tts_piper import is_tts_available
        result = is_tts_available()
        assert isinstance(result, bool)


# ─────────────────────────────────────────────────────────
# Tests B01 V3 — speech_manager.py
# ─────────────────────────────────────────────────────────

class TestSpeechManager:

    def test_init_no_crash(self):
        from src.input.speech_manager import SpeechManager
        manager = SpeechManager(user_name="Céline")
        assert manager is not None
        assert manager._mode in ["text", "tts_only", "voice"]

    def test_status_structure(self):
        from src.input.speech_manager import SpeechManager
        manager = SpeechManager()
        status = manager.get_status()
        assert "mode" in status
        assert "stt_ready" in status
        assert "tts_ready" in status

    def test_repr(self):
        from src.input.speech_manager import SpeechManager
        manager = SpeechManager()
        assert "SpeechManager" in repr(manager)
