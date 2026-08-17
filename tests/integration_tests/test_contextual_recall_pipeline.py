"""
PROJECT      : ALFRED
BLOCK        : B02
FUNCTION     : Rappel contextuel spontané (session 3, plan semaine 17-24/08/2026)
FILE         : tests/integration_tests/test_contextual_recall_pipeline.py
ROLE         : Vérifie que build_response() (src/main.py) peuple réellement
               context["contextual_recall"] à partir de la mémoire épisodique,
               pas seulement que get_contextual_recall() fonctionne isolément
               (déjà couvert par tests/test_b02_b03.py::TestContextualRecall).

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-08-17
VERSION      : V1.0
STATUS       : TESTED

DESCRIPTION :
Même pattern que tests/integration_tests/test_v2_pipeline.py::TestBuildResponseV2Integration
(mock des composants, capture du contexte passé à generator.generate_response).
Mémoire épisodique isolée via tmp_path — jamais data/memory/episodes.json réel.
"""

import sys
from pathlib import Path
from unittest.mock import MagicMock

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))


def _make_components():
    adapter = MagicMock()
    adapter.build_response_context.return_value = {
        "adaptation": {"mode": "focus", "tone": "direct"},
        "memory_context": "",
        "knowledge_context": "",
    }

    memory = MagicMock()
    memory.format_context_for_prompt.return_value = ""

    generator = MagicMock()
    generator.generate_response.return_value = "Réponse."

    behavior_engine = MagicMock()
    decision_mock = MagicMock()
    decision_mock.mode = "focus"
    decision_mock.tone = "direct"
    behavior_engine.decide_behavior.return_value = decision_mock
    behavior_engine.apply_v2_decision.return_value = decision_mock

    return {
        "adapter": adapter,
        "behavior_engine": behavior_engine,
        "memory": memory,
        "generator": generator,
        "llm": None,
        "ltm_ok": False,
        "ltm": None,
        "retrieval_engine": None,
    }


def _capture_context(store):
    def side_effect(*args, **kwargs):
        if "response_context" in kwargs:
            store.update(kwargs["response_context"])
        elif len(args) >= 2:
            store.update(args[1])
        return "Réponse capturée."
    return side_effect


def _patch_detect_context(monkeypatch):
    monkeypatch.setattr(
        "src.main.detect_context",
        lambda user_input, time_ctx: {
            "nlp": {},
            "emotion_state": MagicMock(emotion="neutral"),
            "wellbeing": MagicMock(fatigue_score=0.2),
            "mode_b03": "focus",
            "behavior_mode": "focus",
            "behavior_emotion": "neutral",
            "intensity": 0.3,
            "fatigue": 0.2,
        },
    )
    monkeypatch.setattr(
        "src.memory.memory_answer_engine.answer_from_memory",
        lambda user_message, memory_context: None,
    )


class TestContextualRecallInBuildResponse:

    def test_contextual_recall_populated_when_relevant_episode_exists(self, tmp_path, monkeypatch):
        import src.memory.episodic_memory as episodic_memory
        monkeypatch.setattr(episodic_memory, "_EPISODE_FILE", tmp_path / "episodes.json")
        episodic_memory.record_episode(
            "Décision de reprendre le projet ALFRED après la pause santé",
            "Priorise la démonstrabilité pour les soutenances",
            category="decision", emotion="motivated", importance=0.9, tags=["soutenance"],
        )

        from src.main import build_response

        components = _make_components()
        captured = {}
        components["generator"].generate_response.side_effect = _capture_context(captured)
        _patch_detect_context(monkeypatch)

        build_response(
            user_input="je me demande si je serai prête pour les soutenances",
            components=components,
            time_ctx={"energy_level": "medium"},
        )

        assert "contextual_recall" in captured, "context['contextual_recall'] absent — rappel non branché"
        assert "soutenance" in captured["contextual_recall"].lower() or captured["contextual_recall"] != ""

    def test_contextual_recall_empty_when_no_relevant_episode(self, tmp_path, monkeypatch):
        import src.memory.episodic_memory as episodic_memory
        monkeypatch.setattr(episodic_memory, "_EPISODE_FILE", tmp_path / "episodes.json")
        # Fichier vide — aucun épisode enregistré.

        from src.main import build_response

        components = _make_components()
        captured = {}
        components["generator"].generate_response.side_effect = _capture_context(captured)
        _patch_detect_context(monkeypatch)

        build_response(
            user_input="quel temps fait-il aujourd'hui ?",
            components=components,
            time_ctx={"energy_level": "medium"},
        )

        assert captured.get("contextual_recall", "") == ""
