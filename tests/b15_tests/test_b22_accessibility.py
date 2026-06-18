"""
PROJECT      : ALFRED  |  BLOCK : B22  |  FUNCTION : 22.01 + 22.02 + 22.03 + 22.15
FILE         : tests/b15_tests/test_b22_accessibility.py
ROLE         : Tests Translator V1.1 + TextReader V1.1 + AccessibilityManager
AUTHOR       : Cognitive Products Lab  |  CREATED : 2026-06-01  |  STATUS : ACTIVE
UPDATED      : 2026-06-03 — ajout tests LLMRouter réel, pause, audit_wcag
"""
import time
import pytest
from unittest.mock import MagicMock
from src.accessibility.translation.translator import Translator, SUPPORTED_LANGUAGES
from src.accessibility.audio.text_reader import TextReader
from src.accessibility.accessibility_manager import AccessibilityManager, AccessibilityProfile


# ──────────────────────────────────────────────────────────────────────────────
# Translator
# ──────────────────────────────────────────────────────────────────────────────

class TestTranslator:

    def test_supported_languages_not_empty(self):
        assert len(SUPPORTED_LANGUAGES) >= 4

    def test_supported_languages_contains_fr_en(self):
        assert "fr" in SUPPORTED_LANGUAGES
        assert "en" in SUPPORTED_LANGUAGES

    def test_init_without_llm(self):
        t = Translator()
        assert t._llm is None

    def test_translate_unsupported_lang_raises(self):
        t = Translator()
        with pytest.raises(ValueError):
            t.translate("hello", target_lang="xx")

    def test_translate_without_llm_returns_original(self):
        t = Translator()
        result = t.translate("bonjour", target_lang="en")
        # Sans LLM, retourne le texte original (fallback gracieux)
        assert isinstance(result, str)
        assert len(result) > 0

    def test_translate_cached_on_second_call(self):
        t = Translator()
        t.translate("bonjour", target_lang="en")
        t.translate("bonjour", target_lang="en")
        assert t._stats["hits"] >= 1

    def test_detect_language_french(self):
        t = Translator()
        result = t.detect_language("Bonjour, je suis ALFRED et je vous aide.")
        assert result == "fr"

    def test_detect_language_english(self):
        t = Translator()
        result = t.detect_language("Hello, I am ALFRED and I can help you.")
        assert result == "en"

    def test_detect_language_unknown(self):
        t = Translator()
        result = t.detect_language("XYZ123 @@@ ???")
        assert result in ("unknown", "fr", "en")

    def test_status_returns_dict(self):
        t = Translator()
        s = t.status()
        assert isinstance(s, dict)
        assert "supported_languages" in s
        assert "cache_entries" in s

    def test_clear_cache(self):
        t = Translator()
        t.translate("bonjour", target_lang="en")
        t.clear_cache()
        assert t._stats["hits"] == 0 or len(t._cache) == 0

    def test_cache_eviction_at_max(self):
        t = Translator(cache_size=2)
        # Remplir le cache avec des traductions fictives via _store_cache
        t._store_cache("key1", "val1")
        t._store_cache("key2", "val2")
        t._store_cache("key3", "val3")   # déclenche éviction
        assert len(t._cache) <= 2


# ──────────────────────────────────────────────────────────────────────────────
# TextReader
# ──────────────────────────────────────────────────────────────────────────────

class TestTextReader:

    def test_init_headless(self):
        tr = TextReader()
        assert tr._tts is None
        assert tr.rate == 1.0
        assert tr.volume == 1.0

    def test_is_reading_initially_false(self):
        tr = TextReader()
        assert tr.is_reading() is False

    def test_read_empty_does_not_crash(self):
        tr = TextReader()
        tr.read("")   # ne doit pas lever

    def test_read_headless_completes(self):
        tr = TextReader()
        called = []
        tr.read("Bonjour Alfred.", on_done=lambda: called.append(True))
        assert called == [True]

    def test_read_headless_is_reading_false_after(self):
        tr = TextReader()
        tr.read("test phrase.")
        assert tr.is_reading() is False

    def test_read_sentence_headless_does_not_crash(self):
        tr = TextReader()
        tr.read_sentence("phrase unique")   # ne doit pas lever

    def test_stop_does_not_crash(self):
        tr = TextReader()
        tr.stop()   # ne doit pas lever même sans lecture

    def test_set_rate_clamped(self):
        tr = TextReader()
        tr.set_rate(5.0)
        assert tr.rate == 2.0
        tr.set_rate(0.1)
        assert tr.rate == 0.5

    def test_set_volume_clamped(self):
        tr = TextReader()
        tr.set_volume(2.0)
        assert tr.volume == 1.0
        tr.set_volume(-1.0)
        assert tr.volume == 0.0

    def test_set_pause(self):
        tr = TextReader()
        tr.set_pause(0.5)
        assert tr.pause_ms == 500

    def test_split_sentences(self):
        tr = TextReader()
        sentences = tr._split_sentences("Phrase un. Phrase deux! Phrase trois?")
        assert len(sentences) == 3

    def test_split_sentences_single(self):
        tr = TextReader()
        sentences = tr._split_sentences("Une seule phrase")
        assert len(sentences) == 1

    def test_status_returns_dict(self):
        tr = TextReader()
        s = tr.status()
        assert "tts_connected" in s
        assert "rate" in s
        assert "reading" in s

    def test_read_with_mock_tts(self):
        """Test avec un mock TTS minimal."""
        spoken = []
        class MockTTS:
            def speak(self, text): spoken.append(text)
        tr = TextReader(tts_engine=MockTTS())
        tr.read("Bonjour Alfred. Comment vas-tu?")
        assert len(spoken) >= 1

    def test_on_done_called(self):
        tr = TextReader()
        done = []
        tr.read("Test.", on_done=lambda: done.append(1))
        assert done == [1]


# ──────────────────────────────────────────────────────────────────────────────
# TextReader — pause entre phrases (bug fix 2026-06-03)
# ──────────────────────────────────────────────────────────────────────────────

class TestTextReaderPause:

    def test_pause_applied_between_sentences(self):
        """La pause doit être appliquée entre les phrases (pas après la dernière)."""
        timestamps = []

        class MockTTS:
            def speak(self, text):
                timestamps.append(time.monotonic())

        pause = 0.05   # 50 ms — suffisant pour être mesurable sans ralentir les tests
        tr = TextReader(tts_engine=MockTTS(), pause_between_sentences=pause)
        tr.read("Phrase un. Phrase deux. Phrase trois.")

        assert len(timestamps) == 3, f"Attendu 3 appels speak, obtenu {len(timestamps)}"
        # La pause doit exister entre phrase 1→2 et 2→3 (pas après la 3e)
        gap_1_2 = timestamps[1] - timestamps[0]
        gap_2_3 = timestamps[2] - timestamps[1]
        assert gap_1_2 >= pause * 0.8, f"Pause 1→2 trop courte : {gap_1_2:.3f}s"
        assert gap_2_3 >= pause * 0.8, f"Pause 2→3 trop courte : {gap_2_3:.3f}s"

    def test_no_pause_after_last_sentence(self):
        """Pas de pause inutile après la dernière phrase."""
        call_times = []

        class MockTTS:
            def speak(self, text):
                call_times.append(time.monotonic())

        tr = TextReader(tts_engine=MockTTS(), pause_between_sentences=0.2)
        t0 = time.monotonic()
        tr.read("Phrase unique.")
        elapsed = time.monotonic() - t0
        # Une seule phrase → aucune pause → doit terminer rapidement
        assert elapsed < 0.15, f"Pause inutile après phrase unique : {elapsed:.3f}s"

    def test_pause_zero_no_sleep(self):
        """Avec pause=0, aucun sleep ne doit être appelé."""
        spoken = []

        class MockTTS:
            def speak(self, text): spoken.append(text)

        tr = TextReader(tts_engine=MockTTS(), pause_between_sentences=0.0)
        t0 = time.monotonic()
        tr.read("Un. Deux. Trois.")
        elapsed = time.monotonic() - t0
        assert len(spoken) == 3
        assert elapsed < 0.1   # quasi-instantané


# ──────────────────────────────────────────────────────────────────────────────
# Translator — interface LLMRouter correcte (bug fix 2026-06-03)
# ──────────────────────────────────────────────────────────────────────────────

class TestTranslatorLLMRouter:

    def test_generate_called_with_system_and_user_prompt(self):
        """generate() doit être appelé avec system_prompt + user_prompt (pas un seul arg)."""
        mock_llm = MagicMock()
        mock_llm.generate.return_value = "Hello"

        t = Translator(llm_router=mock_llm)
        result = t.translate("Bonjour", target_lang="en")

        assert mock_llm.generate.called, "generate() non appelé"
        call_kwargs = mock_llm.generate.call_args

        # Vérifie que les deux arguments nommés sont présents
        assert "system_prompt" in call_kwargs.kwargs, (
            "generate() appelé sans system_prompt — ancien bug détecté"
        )
        assert "user_prompt" in call_kwargs.kwargs, (
            "generate() appelé sans user_prompt — ancien bug détecté"
        )
        assert result == "Hello"

    def test_system_prompt_mentions_target_language(self):
        """Le system_prompt doit mentionner la langue cible."""
        mock_llm = MagicMock()
        mock_llm.generate.return_value = "Hola"

        t = Translator(llm_router=mock_llm)
        t.translate("Bonjour", target_lang="es")

        call_kwargs = mock_llm.generate.call_args
        system_prompt = call_kwargs.kwargs.get("system_prompt", "")
        assert "espagnol" in system_prompt.lower(), (
            f"system_prompt ne mentionne pas la langue : {system_prompt!r}"
        )

    def test_user_prompt_contains_source_text(self):
        """Le user_prompt doit contenir le texte source à traduire."""
        mock_llm = MagicMock()
        mock_llm.generate.return_value = "Good morning"

        t = Translator(llm_router=mock_llm)
        t.translate("Bonjour le monde", target_lang="en")

        call_kwargs = mock_llm.generate.call_args
        user_prompt = call_kwargs.kwargs.get("user_prompt", "")
        assert "Bonjour le monde" in user_prompt, (
            f"user_prompt ne contient pas le texte source : {user_prompt!r}"
        )

    def test_llm_exception_returns_original(self):
        """Si le LLM lève une exception, retourner le texte original sans crasher."""
        mock_llm = MagicMock()
        mock_llm.generate.side_effect = RuntimeError("LLM hors ligne")

        t = Translator(llm_router=mock_llm)
        result = t.translate("Texte original", target_lang="en")

        assert result == "Texte original"
        assert t._stats["errors"] == 1

    def test_result_cached_after_llm_call(self):
        """La réponse LLM doit être mise en cache."""
        mock_llm = MagicMock()
        mock_llm.generate.return_value = "Good morning"

        t = Translator(llm_router=mock_llm)
        t.translate("Bonjour", target_lang="en")
        t.translate("Bonjour", target_lang="en")   # doit utiliser le cache

        assert mock_llm.generate.call_count == 1, "Cache non utilisé — LLM appelé 2 fois"
        assert t._stats["hits"] == 1


# ──────────────────────────────────────────────────────────────────────────────
# AccessibilityManager — audit_wcag (bug fix 2026-06-03)
# ──────────────────────────────────────────────────────────────────────────────

class TestAccessibilityManager:

    def test_init(self):
        mgr = AccessibilityManager()
        assert mgr.status()["wcag_level"] == "AA"

    def test_set_and_get_profile(self):
        mgr = AccessibilityManager()
        mgr.set_user("celine", AccessibilityProfile(language="fr", tts_enabled=True))
        p = mgr.get_profile("celine")
        assert p.language == "fr"
        assert p.tts_enabled is True

    def test_update_profile(self):
        mgr = AccessibilityManager()
        mgr.set_user("celine")
        mgr.update_profile("celine", simplify_text=True, tts_rate=0.8)
        p = mgr.get_profile("celine")
        assert p.simplify_text is True
        assert p.tts_rate == 0.8

    def test_should_simplify_default_false(self):
        mgr = AccessibilityManager()
        assert mgr.should_simplify("unknown_user") is False

    def test_get_policy_summary(self):
        mgr = AccessibilityManager()
        policy = mgr.get_policy_summary()
        assert "wcag_level" in policy
        assert "supported_languages" in policy
        assert "fr" in policy["supported_languages"]

    def test_audit_wcag_returns_dict(self):
        """audit_wcag() ne doit plus lever NotImplementedError."""
        mgr = AccessibilityManager()
        result = mgr.audit_wcag("conversation_box")
        assert isinstance(result, dict)

    def test_audit_wcag_has_required_keys(self):
        mgr = AccessibilityManager()
        result = mgr.audit_wcag("input_row")
        for key in ("component", "level", "compliant", "score", "passed", "failed", "summary"):
            assert key in result, f"Clé manquante : {key}"

    def test_audit_wcag_component_in_result(self):
        mgr = AccessibilityManager()
        result = mgr.audit_wcag("avatar_renderer")
        assert result["component"] == "avatar_renderer"

    def test_audit_wcag_score_between_0_and_1(self):
        mgr = AccessibilityManager()
        result = mgr.audit_wcag("test")
        assert 0.0 <= result["score"] <= 1.0

    def test_audit_wcag_level_is_aa(self):
        mgr = AccessibilityManager()
        result = mgr.audit_wcag("test")
        assert result["level"] == "AA"

    def test_get_wcag_checklist_not_empty(self):
        mgr = AccessibilityManager()
        checklist = mgr.get_wcag_checklist()
        assert len(checklist) >= 5
        assert all("criterion" in c and "name" in c for c in checklist)
