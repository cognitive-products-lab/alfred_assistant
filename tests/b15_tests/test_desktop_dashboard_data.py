"""
PROJECT      : ALFRED
BLOCK        : B15
FUNCTION     : 15.11
FILE         : tests/b15_tests/test_desktop_dashboard_data.py
ROLE         : Tests unitaires src/ui/desktop_dashboard_data.py

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-07-19
VERSION      : V1.0
STATUS       : TESTED

DESCRIPTION :
Agrégation des widgets dashboard. Le pipeline réel (src.main.get_live_components)
est monkeypatché partout — ces tests ne dépendent d'aucun composant vivant
(LLM, TTS, etc.), seulement de la forme des données retournées.
"""

import shutil
import tempfile
import types
from pathlib import Path

import pytest

import src.main as main_module
from src.ui import desktop_dashboard_data as ddd
from src.ui import emotion_override_prefs as eop


@pytest.fixture(autouse=True)
def _isolated_emotion_override_file(monkeypatch):
    tmp_dir = Path(tempfile.mkdtemp(prefix="alfred_ddd_emotion_"))
    monkeypatch.setattr(eop, "_OVERRIDE_FILE", tmp_dir / "emotion_override.json")
    yield
    shutil.rmtree(tmp_dir, ignore_errors=True)


@pytest.fixture
def no_live_components(monkeypatch):
    monkeypatch.setattr(main_module, "get_live_components", lambda: None)


def _fake_components(**overrides):
    base = {}
    base.update(overrides)
    return base


# =============================================================================
# get_recommandations
# =============================================================================

def test_get_recommandations_empty_when_no_live_components(no_live_components):
    assert ddd.get_recommandations() == []


def test_get_recommandations_empty_when_engine_missing(monkeypatch):
    monkeypatch.setattr(main_module, "get_live_components", lambda: _fake_components())
    assert ddd.get_recommandations() == []


def test_get_recommandations_maps_suggestion_fields(monkeypatch):
    suggestion = types.SimpleNamespace(
        content="Vous semblez fatiguée, une pause ?",
        category="wellbeing",
        priority=3,
        can_dismiss=True,
        trigger="high_fatigue",
        timestamp="2026-07-19T10:00:00",
    )
    engine = types.SimpleNamespace(get_history=lambda n: [suggestion])
    monkeypatch.setattr(main_module, "get_live_components",
                         lambda: _fake_components(proactive_engine=engine))

    result = ddd.get_recommandations()
    assert len(result) == 1
    assert result[0]["content"] == suggestion.content
    assert result[0]["trigger"] == "high_fatigue"
    assert "fatigue" in result[0]["why"].lower()


def test_get_recommandations_unknown_trigger_gets_generic_justification(monkeypatch):
    suggestion = types.SimpleNamespace(
        content="...", category="general", priority=1, can_dismiss=True,
        trigger="unknown_trigger_code", timestamp="2026-07-19T10:00:00",
    )
    engine = types.SimpleNamespace(get_history=lambda n: [suggestion])
    monkeypatch.setattr(main_module, "get_live_components",
                         lambda: _fake_components(proactive_engine=engine))
    result = ddd.get_recommandations()
    assert result[0]["why"] == "Basé sur votre contexte actuel"


def test_get_recommandations_most_recent_first(monkeypatch):
    old = types.SimpleNamespace(content="old", category="c", priority=1, can_dismiss=True,
                                 trigger="t1", timestamp="t")
    new = types.SimpleNamespace(content="new", category="c", priority=1, can_dismiss=True,
                                 trigger="t2", timestamp="t")
    engine = types.SimpleNamespace(get_history=lambda n: [old, new])
    monkeypatch.setattr(main_module, "get_live_components",
                         lambda: _fake_components(proactive_engine=engine))
    result = ddd.get_recommandations()
    assert result[0]["content"] == "new"
    assert result[1]["content"] == "old"


# =============================================================================
# get_emotion_state
# =============================================================================

def test_get_emotion_state_disabled(no_live_components):
    eop.save_emotion_override(enabled=False)
    assert ddd.get_emotion_state() == {"enabled": False}


def test_get_emotion_state_manual_override_takes_priority(no_live_components):
    eop.save_emotion_override(manual_mood="Calme")
    state = ddd.get_emotion_state()
    assert state["enabled"] is True
    assert state["manual"] is True
    assert "Calme" in state["mood_label"]
    assert "corrigé par vous" in state["mood_label"]


def test_get_emotion_state_no_data_before_first_exchange(monkeypatch):
    monkeypatch.setattr(main_module, "get_live_components", lambda: _fake_components())
    state = ddd.get_emotion_state()
    assert state == {"enabled": True, "manual": False, "no_data": True}


def test_get_emotion_state_live_signal(monkeypatch):
    fused = types.SimpleNamespace(
        dominant_emotion="tired", confidence=0.64, sources_used=["nlp", "emotion", "context"],
    )
    monkeypatch.setattr(main_module, "get_live_components",
                         lambda: _fake_components(_last_fused=fused))
    monkeypatch.setattr(
        "src.regulation.wellbeing_tracker.get_daily_energy_summary",
        lambda: {"dominant": "low"},
    )
    state = ddd.get_emotion_state()
    assert state["enabled"] is True
    assert state["manual"] is False
    assert state["mood_label"] == "Fatigué(e)"
    assert state["confidence_pct"] == 64
    assert state["bar_pct"] == 64
    assert "Ton détecté dans vos derniers échanges" in state["sources"]
    assert state["energy_dominant"] == "low"


def test_get_emotion_state_unknown_emotion_capitalizes_raw_label(monkeypatch):
    fused = types.SimpleNamespace(dominant_emotion="curious", confidence=0.5, sources_used=[])
    monkeypatch.setattr(main_module, "get_live_components",
                         lambda: _fake_components(_last_fused=fused))
    monkeypatch.setattr("src.regulation.wellbeing_tracker.get_daily_energy_summary",
                         lambda: {"dominant": "unknown"})
    state = ddd.get_emotion_state()
    assert state["mood_label"] == "Curious"


# =============================================================================
# set_emotion_override / correct_emotion
# =============================================================================

def test_set_emotion_override_false_then_true_clears_manual_mood(no_live_components):
    eop.save_emotion_override(manual_mood="Stressé(e)")
    ddd.set_emotion_override(False)
    state = ddd.set_emotion_override(True)
    # réactiver repart sur le signal live, pas sur l'ancienne correction manuelle
    assert state.get("manual") is not True or state.get("no_data") is True


def test_correct_emotion_persists_and_returns_state(no_live_components):
    state = ddd.correct_emotion("Content(e)")
    assert state["manual"] is True
    assert "Content(e)" in state["mood_label"]


# =============================================================================
# get_planning
# =============================================================================

def test_get_planning_empty_when_no_reminders(no_live_components, monkeypatch, tmp_path):
    monkeypatch.setattr(
        "src.v3.proactive.reminder_engine.ReminderEngine",
        lambda storage_path=None: types.SimpleNamespace(get_active=lambda: []),
    )
    assert ddd.get_planning() == []


def test_get_planning_uses_live_engine_and_sorts_by_due_date(monkeypatch):
    r1 = types.SimpleNamespace(id="a", title="Plus tard", due_at="2026-07-20T18:00:00",
                                recurrent=False, is_due=lambda: False)
    r2 = types.SimpleNamespace(id="b", title="Plus tôt", due_at="2026-07-20T09:00:00",
                                recurrent=False, is_due=lambda: True)
    engine = types.SimpleNamespace(get_active=lambda: [r1, r2])
    import src.main as m
    monkeypatch.setattr(m, "get_live_components", lambda: _fake_components(reminder_engine=engine))

    result = ddd.get_planning()
    assert [r["id"] for r in result] == ["b", "a"]
    assert result[0]["overdue"] is True
    assert result[1]["overdue"] is False


# =============================================================================
# get_devices
# =============================================================================

def test_get_devices_shapes_response(monkeypatch):
    monkeypatch.setattr("src.ui.device_settings.get_cached_cameras",
                         lambda: [{"index": 0, "name": "Cam"}])
    monkeypatch.setattr("src.ui.device_settings.get_cached_audio_inputs",
                         lambda: [{"index": -1, "name": "Micro"}])
    monkeypatch.setattr("src.ui.device_settings.get_cached_audio_outputs",
                         lambda: [{"index": -1, "name": "Sortie"}])
    monkeypatch.setattr("src.ui.device_settings.load_device_settings",
                         lambda: {"camera_index": 0, "audio_input_index": -1, "audio_output_index": -1})

    result = ddd.get_devices()
    assert result["cameras"] == [{"index": 0, "name": "Cam"}]
    assert result["active"]["camera_index"] == 0


# =============================================================================
# get_activite
# =============================================================================

def test_get_activite_delegates_to_episodic_memory(monkeypatch):
    monkeypatch.setattr(
        "src.memory.episodic_memory.get_timeline",
        lambda limit=10: [{"id": "ep_1", "title": "Test"}],
    )
    result = ddd.get_activite()
    assert result == [{"id": "ep_1", "title": "Test"}]
