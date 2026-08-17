# ============================================================
# ALFRED — tests/test_b02_b03.py
# Tests Blocs 02 & 03 — Mémoire + Émotions
#
# Lancer :
#   cd D:\PROJET_ALFRED\ALFRED_PC
#   .venv\Scripts\Activate.ps1
#   pytest tests/test_b02_b03.py -v
#
# STATUS  : VALIDATED
# ============================================================

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


# ══════════════════════════════════════════════════════════
# BLOC 02 — MÉMOIRE
# ══════════════════════════════════════════════════════════

class TestMemoryManager:
    """Tests B02.01 — Mémoire court terme."""

    def setup_method(self):
        from src.memory.memory_manager import reset_session
        reset_session("Céline")

    def test_add_and_get_exchange(self):
        from src.memory.memory_manager import add_exchange, get_history, history_count
        add_exchange("Bonjour Alfred", "Bonjour Céline !", "greeting", "neutral")
        assert history_count() == 1
        history = get_history()
        assert history[0]["user"] == "Bonjour Alfred"
        assert history[0]["intent"] == "greeting"

    def test_get_last_n_exchanges(self):
        from src.memory.memory_manager import add_exchange, get_history
        for i in range(5):
            add_exchange(f"message {i}", f"réponse {i}")
        last3 = get_history(3)
        assert len(last3) == 3
        assert last3[-1]["user"] == "message 4"

    def test_context_set_get(self):
        from src.memory.memory_manager import set_context, get_context
        set_context("current_topic", "ALFRED project")
        assert get_context("current_topic") == "ALFRED project"
        assert get_context("missing_key", "default") == "default"

    def test_update_context_from_analysis(self):
        from src.memory.memory_manager import update_context_from_analysis, get_context
        analysis = {"intent": "engineering", "emotion": "focused", "language": "fr"}
        update_context_from_analysis(analysis)
        assert get_context("last_intent") == "engineering"
        assert get_context("last_emotion") == "focused"

    def test_dominant_emotion(self):
        from src.memory.memory_manager import add_exchange, get_dominant_emotion
        add_exchange("je suis stressée", "...", "emotional_support", "stressed")
        add_exchange("encore stressée", "...", "emotional_support", "stressed")
        add_exchange("un peu mieux", "...", "general", "neutral")
        assert get_dominant_emotion() == "stressed"

    def test_session_summary(self):
        from src.memory.memory_manager import add_exchange, get_session_summary
        add_exchange("test", "réponse", "engineering", "focused")
        summary = get_session_summary()
        assert "session_id" in summary
        assert summary["exchange_count"] == 1
        assert "engineering" in summary["intents_seen"]

    def test_format_history_for_prompt(self):
        from src.memory.memory_manager import add_exchange, format_history_for_prompt
        add_exchange("Qu'est-ce que Python ?", "Python est un langage...")
        text = format_history_for_prompt(1)
        assert "Céline" in text
        assert "Python" in text


class TestLongTermMemory:
    """Tests B02.02 — Mémoire long terme SQLite."""

    def test_init_db(self):
        from src.memory.long_term_memory import init_db
        init_db()  # Ne doit pas crasher

    def test_save_and_retrieve_fact(self):
        from src.memory.long_term_memory import init_db, save_fact, get_fact
        init_db()
        save_fact("test_key_pytest", "test_value_pytest", "general")
        result = get_fact("test_key_pytest")
        assert result == "test_value_pytest"

    def test_save_fact_complex(self):
        from src.memory.long_term_memory import init_db, save_fact, get_fact
        init_db()
        save_fact("langages_pytest", ["Python", "SQL"], "profil")
        result = get_fact("langages_pytest")
        assert "Python" in result

    def test_save_and_search_exchange(self):
        from src.memory.long_term_memory import init_db, save_exchange, search_memories
        init_db()
        save_exchange("session_test", "test pytest mémoire", "réponse test", "engineering")
        results = search_memories("pytest mémoire")
        assert any("pytest mémoire" in r["user_input"] for r in results)

    def test_record_and_get_pattern(self):
        from src.memory.long_term_memory import init_db, record_pattern, get_top_patterns
        init_db()
        record_pattern("fatigue_soir_pytest", "behavior")
        record_pattern("fatigue_soir_pytest", "behavior")
        patterns = get_top_patterns(5)
        keys = [p["pattern_key"] for p in patterns]
        assert "fatigue_soir_pytest" in keys

    def test_memory_stats(self):
        from src.memory.long_term_memory import init_db, get_memory_stats
        init_db()
        stats = get_memory_stats()
        assert "memories_active" in stats
        assert "facts" in stats
        assert "db_path" in stats


class TestEpisodicMemory:
    """Tests B02.03 — Mémoire épisodique."""

    @pytest.fixture(autouse=True)
    def _isolate_episode_file(self, tmp_path, monkeypatch):
        """
        Sans ça, record_episode() écrit dans le vrai data/memory/episodes.json
        à chaque run de la suite — trouvé le 17/08/2026 : 99 épisodes de test
        ("Important"/"Très important" etc.) accumulés dans les données réelles
        au fil des exécutions répétées de ces tests, faussant la Vue Mémoire.
        """
        import src.memory.episodic_memory as episodic_memory
        monkeypatch.setattr(episodic_memory, "_EPISODE_FILE", tmp_path / "episodes.json")

    def test_record_and_retrieve_episode(self):
        from src.memory.episodic_memory import record_episode, get_timeline
        ep_id = record_episode(
            title="Test pytest épisode",
            description="Episode créé pendant les tests",
            category="learning",
            emotion="focused",
            importance=0.8,
            tags=["pytest", "test"],
        )
        assert ep_id.startswith("ep_")
        timeline = get_timeline(limit=5)
        titles = [e["title"] for e in timeline]
        assert "Test pytest épisode" in titles

    def test_get_important_episodes(self):
        from src.memory.episodic_memory import record_episode, get_important_episodes
        record_episode("Important", "Très important", importance=0.95)
        record_episode("Anecdote", "Peu important", importance=0.1)
        important = get_important_episodes(threshold=0.7)
        assert all(e["importance"] >= 0.7 for e in important)

    def test_get_episodes_by_emotion(self):
        from src.memory.episodic_memory import record_episode, get_episodes_by_emotion
        record_episode("Moment stress", "test", emotion="stressed", importance=0.6)
        episodes = get_episodes_by_emotion("stressed")
        assert all(e["emotion"] == "stressed" for e in episodes)

    def test_search_episodes(self):
        from src.memory.episodic_memory import record_episode, search_episodes
        record_episode("Percée ALFRED", "Grande avancée sur le projet ALFRED")
        results = search_episodes("ALFRED")
        assert len(results) > 0

    def test_episode_stats(self):
        from src.memory.episodic_memory import get_episode_stats
        stats = get_episode_stats()
        assert "total_episodes" in stats
        assert "categories" in stats


class TestMemoryIndexer:
    """Tests B02.05 — Indexation mémoire."""

    def test_search_all_memory(self):
        from src.memory.memory_indexer import search_all_memory
        results = search_all_memory("test")
        assert "keyword" in results
        assert "total_found" in results

    def test_build_memory_context(self):
        from src.memory.memory_indexer import build_memory_context
        ctx = build_memory_context()
        assert "session" in ctx
        assert "dominant_emotion" in ctx

    def test_format_memory_for_prompt(self):
        from src.memory.memory_indexer import format_memory_for_prompt
        text = format_memory_for_prompt(3)
        assert "[Mémoire ALFRED]" in text

    def test_get_memory_stats(self):
        from src.memory.memory_indexer import get_memory_stats
        stats = get_memory_stats()
        assert "session" in stats
        assert "long_term" in stats
        assert "episodic" in stats


class TestContextualRecall:
    """Tests session 3 (17-24/08/2026) — rappel contextuel spontané, get_contextual_recall()."""

    @pytest.fixture(autouse=True)
    def _isolate_episode_file(self, tmp_path, monkeypatch):
        import src.memory.episodic_memory as episodic_memory
        monkeypatch.setattr(episodic_memory, "_EPISODE_FILE", tmp_path / "episodes.json")

    def test_recalls_relevant_episode_above_threshold(self):
        from src.memory.episodic_memory import record_episode
        from src.memory.memory_indexer import get_contextual_recall

        record_episode(
            "Décision de reprendre le projet ALFRED après la pause santé",
            "Priorise la démonstrabilité pour les soutenances",
            category="decision", emotion="motivated", importance=0.9, tags=["soutenance"],
        )
        recall = get_contextual_recall("je me demande si je serai prête pour les soutenances")
        assert recall is not None
        assert recall["kind"] == "episode"

    def test_no_recall_for_unrelated_message(self):
        from src.memory.episodic_memory import record_episode
        from src.memory.memory_indexer import get_contextual_recall

        record_episode("Décision de reprendre le projet ALFRED", "test", importance=0.9)
        assert get_contextual_recall("quel temps fait-il aujourd'hui ?") is None

    def test_no_recall_below_importance_threshold(self):
        from src.memory.episodic_memory import record_episode
        from src.memory.memory_indexer import get_contextual_recall

        record_episode("Bug TTS corrigé", "le tts lisait les balises", importance=0.4, tags=["tts"])
        assert get_contextual_recall("le bug tts est revenu") is None

    def test_excluded_id_not_recalled_again(self):
        from src.memory.episodic_memory import record_episode
        from src.memory.memory_indexer import get_contextual_recall

        ep_id = record_episode("Décision soutenance", "test", importance=0.9, tags=["soutenance"])
        assert get_contextual_recall("les soutenances me stressent", exclude_ids={ep_id}) is None


class TestRAGStub:
    """Tests B02.04 — RAG stub."""

    def test_rag_status(self):
        from src.memory.rag_stub import get_rag_status, is_rag_available
        status = get_rag_status()
        assert "available" in status
        assert "planned" in status

    def test_semantic_search_stub(self):
        from src.memory.rag_stub import semantic_search
        results = semantic_search("test query")
        assert isinstance(results, list)


# ══════════════════════════════════════════════════════════
# BLOC 03 — ÉMOTIONS & RÉGULATION
# ══════════════════════════════════════════════════════════

class TestEmotionDetector:
    """Tests B03.01 — Détection émotion."""

    def test_detect_stressed(self):
        from src.regulation.emotion_detector import detect_emotion
        state = detect_emotion("je suis stressée et débordée")
        assert state.emotion == "stressed"
        assert state.intensity > 0
        assert state.valence == "negative"

    def test_detect_tired(self):
        from src.regulation.emotion_detector import detect_emotion
        state = detect_emotion("je suis épuisée, lessivée")
        assert state.emotion == "tired"
        assert state.arousal == "low"

    def test_detect_motivated(self):
        from src.regulation.emotion_detector import detect_emotion
        state = detect_emotion("je suis super motivée, on y va !")
        assert state.emotion == "motivated"
        assert state.valence == "positive"

    def test_detect_neutral(self):
        from src.regulation.emotion_detector import detect_emotion
        state = detect_emotion("montre-moi les tâches du jour")
        assert state.emotion == "neutral"
        assert state.intensity == 0.0

    def test_detect_distress_priority(self):
        from src.regulation.emotion_detector import detect_emotion
        # La détresse doit prendre la priorité sur la fatigue
        state = detect_emotion("je n'en peux plus, je veux tout lâcher")
        assert state.emotion == "distress"
        assert state.intensity >= 0.7

    def test_intensity_scales_with_signals(self):
        from src.regulation.emotion_detector import detect_emotion
        state_low   = detect_emotion("je suis un peu fatiguée")
        state_high  = detect_emotion("je suis épuisée, lessivée, vidée, crevée")
        assert state_high.intensity >= state_low.intensity

    def test_is_negative(self):
        from src.regulation.emotion_detector import detect_emotion, is_negative_emotion
        state = detect_emotion("je suis triste")
        assert is_negative_emotion(state) is True

    def test_requires_support(self):
        from src.regulation.emotion_detector import detect_emotion, requires_support_mode
        state = detect_emotion("je suis stressée et angoissée")
        assert requires_support_mode(state) is True

    def test_emotion_label_fr(self):
        from src.regulation.emotion_detector import get_emotion_label_fr
        assert get_emotion_label_fr("stressed") == "stress"
        assert get_emotion_label_fr("neutral") == "neutre"


class TestModeManager:
    """Tests B03.02/03 — Machine à états 4 modes."""

    def setup_method(self):
        # Reset singleton entre tests
        import src.regulation.mode_manager as mm
        mm._mode_manager = None

    def test_init_default_mode(self):
        from src.regulation.mode_manager import get_mode_manager
        manager = get_mode_manager()
        assert manager.current_mode == "focus"

    def test_set_mode(self):
        from src.regulation.mode_manager import get_mode_manager
        manager = get_mode_manager()
        result = manager.set_mode("support", "test")
        assert result is True
        assert manager.current_mode == "support"

    def test_set_invalid_mode(self):
        from src.regulation.mode_manager import get_mode_manager
        manager = get_mode_manager()
        result = manager.set_mode("invalid_mode")
        assert result is False
        assert manager.current_mode == "focus"

    def test_update_from_emotion_stressed(self):
        from src.regulation.mode_manager import get_mode_manager
        from src.regulation.emotion_detector import detect_emotion
        manager = get_mode_manager()
        state = detect_emotion("je suis stressée")
        mode = manager.update_from_emotion(state)
        assert mode == "support"

    def test_update_from_emotion_motivated(self):
        from src.regulation.mode_manager import get_mode_manager
        from src.regulation.emotion_detector import detect_emotion
        manager = get_mode_manager()
        state = detect_emotion("je suis super motivée !")
        mode = manager.update_from_emotion(state)
        assert mode == "challenge"

    def test_update_from_context_low_energy(self):
        from src.regulation.mode_manager import get_mode_manager
        manager = get_mode_manager()
        mode = manager.update_from_context("low", "general")
        assert mode == "support"

    def test_get_mode_prefix_returns_string(self):
        from src.regulation.mode_manager import get_mode_manager
        manager = get_mode_manager()
        prefix = manager.get_mode_prefix()
        assert isinstance(prefix, str)

    def test_response_guidelines(self):
        from src.regulation.mode_manager import get_mode_manager
        manager = get_mode_manager()
        guidelines = manager.get_response_guidelines()
        assert "[Mode ALFRED" in guidelines

    def test_transition_log(self):
        from src.regulation.mode_manager import get_mode_manager
        manager = get_mode_manager()
        manager.set_mode("support", "test1")
        manager.set_mode("focus", "test2")
        log = manager.get_transition_log()
        assert len(log) == 2
        assert log[0]["to"] == "support"

    def test_status(self):
        from src.regulation.mode_manager import get_mode_manager
        manager = get_mode_manager()
        status = manager.get_status()
        assert "current_mode" in status
        assert "voice_profile" in status

    def test_transition_hook(self):
        from src.regulation.mode_manager import get_mode_manager
        manager = get_mode_manager()
        transitions = []
        manager.register_transition_hook(lambda f, t: transitions.append((f, t)))
        manager.set_mode("support", "hook_test")
        assert len(transitions) == 1
        assert transitions[0] == ("focus", "support")


class TestModeManagerSignals:
    """
    Tests B03.02/03 — update_from_signals().

    Corrige le 14/08/2026 un bug réel de regulation_engine.py::_run_mode() :
    update_from_emotion() était appelé PUIS update_from_context(), et
    l'intent pouvait écraser silencieusement une décision d'émotion plus
    prioritaire (ex. émotion "stressed"→support annulée par intent
    "engineering"→focus sur la même requête). update_from_signals() applique
    un ordre de priorité explicite : protection > énergie basse > émotion >
    intent (utilisé seulement si l'émotion n'a rien résolu).
    """

    def setup_method(self):
        import src.regulation.mode_manager as mm
        mm._mode_manager = None

    def test_emotion_wins_over_conflicting_intent(self):
        from src.regulation.mode_manager import get_mode_manager
        from src.regulation.emotion_detector import EmotionalState
        manager = get_mode_manager()
        state = EmotionalState(emotion="stressed", intensity=0.5, valence="negative")

        mode = manager.update_from_signals(emotion=state, energy_level="medium", intent="engineering")

        assert mode == "support"

    def test_low_energy_beats_emotion_and_intent(self):
        from src.regulation.mode_manager import get_mode_manager
        from src.regulation.emotion_detector import EmotionalState
        manager = get_mode_manager()
        state = EmotionalState(emotion="motivated", intensity=0.6, valence="positive")

        mode = manager.update_from_signals(emotion=state, energy_level="low", intent="engineering")

        assert mode == "support"

    def test_intent_used_as_fallback_when_emotion_unresolved(self):
        from src.regulation.mode_manager import get_mode_manager
        from src.regulation.emotion_detector import EmotionalState
        manager = get_mode_manager()
        # "unknown_emotion" ne correspond à aucun trigger de mode -> l'intent
        # devient le signal décisif.
        state = EmotionalState(emotion="unknown_emotion", intensity=0.3, valence="neutral")

        mode = manager.update_from_signals(emotion=state, energy_level="medium", intent="organization")

        assert mode == "focus"

    def test_neutral_emotion_does_not_block_intent(self):
        from src.regulation.mode_manager import get_mode_manager
        from src.regulation.emotion_detector import EmotionalState
        manager = get_mode_manager()
        # "neutral" = absence de signal, pas une émotion dominante réelle —
        # c'est le cas majoritaire en usage réel (bug constaté le 14/08/2026
        # via une vérification manuelle bout-en-bout sur RegulationEngine).
        state = EmotionalState(emotion="neutral", intensity=0.0, valence="neutral")

        mode = manager.update_from_signals(emotion=state, energy_level="medium", intent="emotional_support")

        assert mode == "support"

    def test_protection_needed_overrides_everything(self):
        from src.regulation.mode_manager import get_mode_manager
        from src.regulation.emotion_detector import EmotionalState
        manager = get_mode_manager()
        state = EmotionalState(emotion="distress", intensity=0.9, valence="negative")

        mode = manager.update_from_signals(emotion=state, energy_level="high", intent="engineering")

        assert mode == "support"

    def test_no_signals_keeps_current_mode(self):
        from src.regulation.mode_manager import get_mode_manager
        manager = get_mode_manager()
        manager.set_mode("challenge", "setup")

        mode = manager.update_from_signals()

        assert mode == "challenge"


class TestIntentToMode:
    """
    Tests B03.02 — INTENT_TO_MODE couvre le catalogue d'intentions réel
    (src/input/nlp_engine.py::_INTENT_CATALOG, consommé en production via
    regulation_engine.py). Avant l'extension du 14/08/2026, 7 des 11
    intentions réelles (farewell, organization, reminder, weather, music,
    information, project) n'avaient aucun effet sur le mode.
    """

    def test_real_catalog_intents_all_mapped(self):
        from src.regulation.mode_manager import INTENT_TO_MODE
        from src.input.nlp_engine import _INTENT_CATALOG

        unmapped = [
            intent for intent in _INTENT_CATALOG
            if intent != "general" and intent not in INTENT_TO_MODE
        ]
        assert unmapped == [], f"Intentions réelles sans mode associé : {unmapped}"

    def test_organization_and_reminder_map_to_focus(self):
        from src.regulation.mode_manager import INTENT_TO_MODE
        assert INTENT_TO_MODE["organization"] == "focus"
        assert INTENT_TO_MODE["reminder"] == "focus"

    def test_farewell_maps_to_complicite(self):
        from src.regulation.mode_manager import INTENT_TO_MODE
        assert INTENT_TO_MODE["farewell"] == "complicite"


class TestProtectionGuard:
    """Tests B03.04 — Mode protection."""

    def test_is_crisis_detected(self):
        from src.regulation.protection_guard import is_crisis
        assert is_crisis("je veux me faire du mal") is True
        assert is_crisis("je veux organiser ma journée") is False

    def test_is_protection_needed_distress(self):
        from src.regulation.protection_guard import is_protection_needed
        from src.regulation.emotion_detector import EmotionalState
        state = EmotionalState(emotion="distress", intensity=0.9, valence="negative")
        assert is_protection_needed(state) is True

    def test_is_protection_needed_stressed_high(self):
        from src.regulation.protection_guard import is_protection_needed
        from src.regulation.emotion_detector import EmotionalState
        state = EmotionalState(emotion="stressed", intensity=0.8, valence="negative")
        assert is_protection_needed(state) is True

    def test_is_protection_not_needed_low(self):
        from src.regulation.protection_guard import is_protection_needed
        from src.regulation.emotion_detector import EmotionalState
        state = EmotionalState(emotion="stressed", intensity=0.2, valence="negative")
        assert is_protection_needed(state) is False

    def test_crisis_response_contains_resources(self):
        from src.regulation.protection_guard import get_crisis_response
        response = get_crisis_response()
        assert "3114" in response
        assert "professionnel" in response.lower() or "aide" in response.lower()

    def test_protection_response_non_crisis(self):
        from src.regulation.protection_guard import get_protection_response
        response = get_protection_response("stressed", 0.7)
        assert len(response) > 20
        assert isinstance(response, str)

    def test_check_ethical_boundaries_clean(self):
        from src.regulation.protection_guard import check_ethical_boundaries
        result = check_ethical_boundaries("Voici les trois étapes pour avancer.")
        assert result["passed"] is True
        assert len(result["alerts"]) == 0

    def test_ethical_disclaimer(self):
        from src.regulation.protection_guard import get_ethical_disclaimer
        text = get_ethical_disclaimer()
        assert "professionnels" in text or "professionnel" in text


class TestWellbeingTracker:
    """Tests B03.05 — Suivi bien-être."""

    def test_analyze_fatigue_high(self):
        from src.regulation.wellbeing_tracker import analyze_wellbeing, is_low_energy
        state = analyze_wellbeing("je suis épuisée, lessivée, vidée")
        assert is_low_energy(state) is True
        assert state.fatigue_score >= 0.7

    def test_analyze_flow(self):
        from src.regulation.wellbeing_tracker import analyze_wellbeing, is_in_flow
        state = analyze_wellbeing("je suis dans le flow, super concentrée, ça avance bien")
        assert is_in_flow(state) is True
        assert state.energy_level == "high"

    def test_analyze_neutral(self):
        from src.regulation.wellbeing_tracker import analyze_wellbeing
        state = analyze_wellbeing("montre-moi mes tâches")
        assert state.fatigue_score < 0.3
        assert state.flow_detected is False

    def test_mode_suggestion_fatigue(self):
        from src.regulation.wellbeing_tracker import analyze_wellbeing
        state = analyze_wellbeing("je suis vraiment fatiguée, j'en peux plus")
        assert state.mode_suggestion == "support"

    def test_mode_suggestion_flow(self):
        from src.regulation.wellbeing_tracker import analyze_wellbeing
        state = analyze_wellbeing("je suis dans le flow, concentrée")
        assert state.mode_suggestion == "focus"

    def test_wellbeing_suggestion_high_fatigue(self):
        from src.regulation.wellbeing_tracker import analyze_wellbeing, get_wellbeing_suggestion
        state = analyze_wellbeing("je suis épuisée, crevée, lessivée")
        suggestion = get_wellbeing_suggestion(state)
        assert suggestion is not None
        assert isinstance(suggestion, str)

    def test_wellbeing_suggestion_flow(self):
        from src.regulation.wellbeing_tracker import analyze_wellbeing, get_wellbeing_suggestion
        state = analyze_wellbeing("je suis dans le flow")
        suggestion = get_wellbeing_suggestion(state)
        assert suggestion is not None

    def test_log_and_get_curve(self):
        from src.regulation.wellbeing_tracker import analyze_wellbeing, log_wellbeing_point, get_energy_curve
        state = analyze_wellbeing("je suis fatiguée")
        log_wellbeing_point(state)
        curve = get_energy_curve(hours=1)
        assert isinstance(curve, list)

    def test_daily_summary(self):
        from src.regulation.wellbeing_tracker import get_daily_energy_summary
        summary = get_daily_energy_summary()
        assert "dominant" in summary
