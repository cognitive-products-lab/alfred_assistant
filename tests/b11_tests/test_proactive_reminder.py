"""
PROJECT      : ALFRED
BLOCK        : B11 -- Intelligence Cognitive
FUNCTION     : 11.04.001 -> 11.05.005
FILE         : tests/b11_tests/test_proactive_reminder.py
ROLE         : Tests unitaires ProactiveEngine + ReminderEngine

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-05-14
UPDATED      : 2026-05-14
VERSION      : V1.0
STATUS       : STABLE

DESCRIPTION :
Tests complets de :
  - src/v3/proactive/proactive_engine.py
  - src/v3/proactive/reminder_engine.py
Utilise tempfile.mkdtemp() pour isoler le stockage JSON (pas de tmp_path).
"""

import sys
import shutil
import tempfile
from pathlib import Path
from datetime import datetime, timedelta

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from src.v3.proactive.proactive_engine import (
    ProactiveEngine,
    ProactiveSuggestion,
)
from src.v3.proactive.reminder_engine import (
    ReminderEngine,
    Reminder,
)


# ---------------------------------------------------------
# ProactiveSuggestion dataclass
# ---------------------------------------------------------

class TestProactiveSuggestion:

    def test_default_category_general(self):
        s = ProactiveSuggestion()
        assert s.category == "general"

    def test_default_can_dismiss(self):
        s = ProactiveSuggestion()
        assert s.can_dismiss is True

    def test_has_timestamp(self):
        s = ProactiveSuggestion()
        assert s.timestamp != ""

    def test_custom_fields(self):
        s = ProactiveSuggestion(trigger="test", content="msg", category="wellbeing", priority=3)
        assert s.trigger == "test"
        assert s.priority == 3


# ---------------------------------------------------------
# ProactiveEngine
# ---------------------------------------------------------

class TestProactiveEngine:

    def test_disabled_returns_none(self):
        engine = ProactiveEngine(enabled=False)
        result = engine.check_and_suggest()
        assert result is None

    def test_no_signals_returns_none(self):
        engine = ProactiveEngine(cooldown_minutes=0)
        result = engine.check_and_suggest()
        assert result is None

    def test_high_fatigue_triggers_suggestion(self):
        from src.regulation.wellbeing_tracker import WellbeingState
        engine = ProactiveEngine(cooldown_minutes=0)
        state  = WellbeingState(fatigue_score=0.85, energy_level="low")
        result = engine.check_and_suggest(wellbeing_state=state)
        assert result is not None
        assert isinstance(result, ProactiveSuggestion)
        assert result.trigger == "high_fatigue"

    def test_flow_state_triggers_suggestion(self):
        from src.regulation.wellbeing_tracker import WellbeingState
        engine = ProactiveEngine(cooldown_minutes=0)
        state  = WellbeingState(flow_detected=True, fatigue_score=0.0)
        result = engine.check_and_suggest(wellbeing_state=state)
        assert result is not None
        assert result.trigger == "flow_state"

    def test_stressed_emotion_triggers_suggestion(self):
        engine  = ProactiveEngine(cooldown_minutes=0)
        emotion = {"emotion": "stressed", "intensity": 0.7}
        result  = engine.check_and_suggest(emotion_signal=emotion)
        assert result is not None
        assert "stressed" in result.trigger or "emotion" in result.trigger

    def test_low_emotion_intensity_no_suggestion(self):
        engine  = ProactiveEngine(cooldown_minutes=0)
        emotion = {"emotion": "stressed", "intensity": 0.2}
        result  = engine.check_and_suggest(emotion_signal=emotion)
        assert result is None

    def test_late_night_low_energy_context(self):
        engine  = ProactiveEngine(cooldown_minutes=0)
        context = {"period": "nuit", "energy_level": "low"}
        result  = engine.check_and_suggest(context_signal=context)
        assert result is not None
        assert result.category == "context"

    def test_cooldown_prevents_second_suggestion(self):
        from src.regulation.wellbeing_tracker import WellbeingState
        engine = ProactiveEngine(cooldown_minutes=60)  # 1h cooldown
        state  = WellbeingState(fatigue_score=0.85, energy_level="low")
        result1 = engine.check_and_suggest(wellbeing_state=state)
        assert result1 is not None
        result2 = engine.check_and_suggest(wellbeing_state=state)
        assert result2 is None

    def test_max_suggestions_limit(self):
        engine = ProactiveEngine(cooldown_minutes=0, max_suggestions=3)
        for _ in range(3):
            engine.force_suggestion("test")
        result = engine.check_and_suggest(context_signal={"period": "nuit", "energy_level": "low"})
        assert result is None

    def test_force_suggestion_bypasses_cooldown(self):
        engine = ProactiveEngine(cooldown_minutes=999)
        result = engine.force_suggestion("Message force", category="general")
        assert isinstance(result, ProactiveSuggestion)
        assert result.content == "Message force"

    def test_history_records_suggestions(self):
        engine = ProactiveEngine(cooldown_minutes=0)
        engine.force_suggestion("s1")
        engine.force_suggestion("s2")
        history = engine.get_history()
        assert len(history) == 2

    def test_clear_history(self):
        engine = ProactiveEngine(cooldown_minutes=0)
        engine.force_suggestion("s1")
        engine.clear_history()
        assert len(engine.get_history()) == 0

    def test_enable_disable(self):
        engine = ProactiveEngine(enabled=True)
        engine.disable()
        assert engine.enabled is False
        engine.enable()
        assert engine.enabled is True

    def test_status_returns_dict(self):
        engine = ProactiveEngine()
        s = engine.status()
        assert isinstance(s, dict)
        for k in ("enabled", "cooldown_minutes", "max_suggestions",
                  "suggestions_sent", "version"):
            assert k in s


# ---------------------------------------------------------
# Reminder dataclass
# ---------------------------------------------------------

class TestReminder:

    def test_default_active(self):
        r = Reminder(title="test", due_at="2026-05-14T12:00:00")
        assert r.active is True

    def test_has_id(self):
        r = Reminder()
        assert r.id != ""

    def test_is_due_past(self):
        past = (datetime.now() - timedelta(minutes=5)).isoformat()
        r = Reminder(title="test", due_at=past)
        assert r.is_due() is True

    def test_is_due_future(self):
        future = (datetime.now() + timedelta(hours=1)).isoformat()
        r = Reminder(title="test", due_at=future)
        assert r.is_due() is False

    def test_is_due_false_when_inactive(self):
        past = (datetime.now() - timedelta(minutes=5)).isoformat()
        r = Reminder(title="test", due_at=past, active=False)
        assert r.is_due() is False

    def test_is_due_false_empty_due_at(self):
        r = Reminder(title="test", due_at="")
        assert r.is_due() is False


# ---------------------------------------------------------
# ReminderEngine
# ---------------------------------------------------------

def _make_engine() -> tuple[ReminderEngine, Path]:
    """Cree un ReminderEngine dans un repertoire temporaire."""
    tmp = Path(tempfile.mkdtemp())
    path = tmp / "reminders.json"
    engine = ReminderEngine(storage_path=str(path))
    return engine, tmp


class TestReminderEngine:

    def test_starts_empty(self):
        engine, tmp = _make_engine()
        try:
            assert engine.get_active() == []
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_add_reminder(self):
        engine, tmp = _make_engine()
        try:
            future = (datetime.now() + timedelta(hours=1)).isoformat()
            r = engine.add("Reunion", due_at=future)
            assert isinstance(r, Reminder)
            assert r.title == "Reunion"
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_add_persists_to_disk(self):
        engine, tmp = _make_engine()
        path = engine.storage_path
        try:
            future = (datetime.now() + timedelta(hours=1)).isoformat()
            engine.add("Test", due_at=future)
            assert path.exists()
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_get_active_returns_added(self):
        engine, tmp = _make_engine()
        try:
            future = (datetime.now() + timedelta(hours=1)).isoformat()
            engine.add("Rappel A", due_at=future)
            engine.add("Rappel B", due_at=future)
            active = engine.get_active()
            assert len(active) == 2
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_get_due_reminders_past(self):
        engine, tmp = _make_engine()
        try:
            past = (datetime.now() - timedelta(minutes=5)).isoformat()
            engine.add("Passe", due_at=past)
            due = engine.get_due_reminders()
            assert len(due) == 1
            assert due[0].title == "Passe"
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_get_due_deactivates_one_shot(self):
        engine, tmp = _make_engine()
        try:
            past = (datetime.now() - timedelta(minutes=5)).isoformat()
            engine.add("One-shot", due_at=past, recurrent=False)
            engine.get_due_reminders()
            active = engine.get_active()
            assert len(active) == 0
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_get_due_updates_recurrent(self):
        engine, tmp = _make_engine()
        try:
            past = (datetime.now() - timedelta(minutes=5)).isoformat()
            engine.add("Recurrent", due_at=past, recurrent=True, interval_h=1.0)
            engine.get_due_reminders()
            active = engine.get_active()
            assert len(active) == 1  # Toujours actif mais date mise a jour
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_future_reminder_not_due(self):
        engine, tmp = _make_engine()
        try:
            future = (datetime.now() + timedelta(hours=2)).isoformat()
            engine.add("Futur", due_at=future)
            due = engine.get_due_reminders()
            assert len(due) == 0
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_remove_reminder(self):
        engine, tmp = _make_engine()
        try:
            future = (datetime.now() + timedelta(hours=1)).isoformat()
            r = engine.add("A supprimer", due_at=future)
            result = engine.remove(r.id)
            assert result is True
            assert len(engine.get_active()) == 0
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_remove_nonexistent_returns_false(self):
        engine, tmp = _make_engine()
        try:
            assert engine.remove("inexistant_id") is False
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_clear_all(self):
        engine, tmp = _make_engine()
        try:
            future = (datetime.now() + timedelta(hours=1)).isoformat()
            engine.add("R1", due_at=future)
            engine.add("R2", due_at=future)
            engine.clear_all()
            assert engine.get_active() == []
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_status_returns_dict(self):
        engine, tmp = _make_engine()
        try:
            s = engine.status()
            assert isinstance(s, dict)
            for k in ("total", "active", "storage", "version"):
                assert k in s
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_loads_from_existing_file(self):
        engine, tmp = _make_engine()
        path = engine.storage_path
        try:
            future = (datetime.now() + timedelta(hours=1)).isoformat()
            engine.add("Persistant", due_at=future)
            # Recharger depuis le fichier
            engine2 = ReminderEngine(storage_path=str(path))
            assert len(engine2.get_active()) == 1
            assert engine2.get_active()[0].title == "Persistant"
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
