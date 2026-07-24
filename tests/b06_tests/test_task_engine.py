"""
PROJECT      : ALFRED
BLOCK        : B06.03
FILE         : tests/b06_tests/test_task_engine.py
ROLE         : Tests unitaires src/assistant_actions/task_engine.py

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-07-24
VERSION      : V1.0
STATUS       : TESTED

DESCRIPTION :
Fichier JSON isolé par test (tmp_path) — jamais data/actions/tasks.json réel.
"""

from __future__ import annotations

import json
from datetime import datetime, timedelta

from src.assistant_actions.task_engine import Task, TaskEngine


def _engine(tmp_path):
    return TaskEngine(storage_path=tmp_path / "tasks.json")


def test_add_and_list_task(tmp_path):
    engine = _engine(tmp_path)
    task = engine.add("Vermifuger les chiens")

    tasks = engine.list()
    assert len(tasks) == 1
    assert tasks[0].id == task.id
    assert tasks[0].title == "Vermifuger les chiens"
    assert tasks[0].done is False


def test_add_persists_across_new_engine_instance(tmp_path):
    path = tmp_path / "tasks.json"
    TaskEngine(storage_path=path).add("Appeler le dentiste")

    reloaded = TaskEngine(storage_path=path)
    assert len(reloaded.list()) == 1
    assert reloaded.list()[0].title == "Appeler le dentiste"


def test_save_preserves_alfred_header_and_meta(tmp_path):
    path = tmp_path / "tasks.json"
    TaskEngine(storage_path=path).add("Ranger le bureau")

    raw = json.loads(path.read_text(encoding="utf-8"))
    assert "_alfred_header" in raw
    assert "_meta" in raw
    assert raw["_meta"]["status"] == "IMPLEMENTE"
    assert len(raw["tasks"]) == 1


def test_complete_task_marks_done(tmp_path):
    engine = _engine(tmp_path)
    task = engine.add("Preparer le brief Mastere")

    completed = engine.complete(task.id)

    assert completed.done is True
    assert completed.done_at is not None
    assert engine.list() == []  # exclu par défaut de list() une fois terminée
    assert engine.list(include_done=True)[0].done is True


def test_complete_unknown_task_returns_none(tmp_path):
    engine = _engine(tmp_path)
    assert engine.complete("inexistant") is None


def test_delete_task(tmp_path):
    engine = _engine(tmp_path)
    task = engine.add("Tache a supprimer")

    assert engine.delete(task.id) is True
    assert engine.list() == []


def test_delete_unknown_task_returns_false(tmp_path):
    engine = _engine(tmp_path)
    assert engine.delete("inexistant") is False


def test_find_by_title_matches_case_insensitive(tmp_path):
    engine = _engine(tmp_path)
    engine.add("Vermifuger les chiens")
    engine.add("Acheter du pain")

    matches = engine.find_by_title("VERMIFUGER")
    assert len(matches) == 1
    assert matches[0].title == "Vermifuger les chiens"


def test_find_by_title_excludes_done_tasks(tmp_path):
    engine = _engine(tmp_path)
    task = engine.add("Vermifuger les chiens")
    engine.complete(task.id)

    assert engine.find_by_title("vermifuger") == []


def test_list_sorts_by_due_date_then_undated_last(tmp_path):
    engine = _engine(tmp_path)
    now = datetime.now()
    engine.add("Sans echeance")
    engine.add("Echeance proche", due_at=(now + timedelta(days=1)).isoformat())
    engine.add("Echeance lointaine", due_at=(now + timedelta(days=10)).isoformat())

    titles = [t.title for t in engine.list()]
    assert titles == ["Echeance proche", "Echeance lointaine", "Sans echeance"]


def test_is_due_false_without_reminder_flag(tmp_path):
    engine = _engine(tmp_path)
    past = (datetime.now() - timedelta(hours=1)).isoformat()
    task = engine.add("Tache en retard", due_at=past, reminder=False)

    assert task.is_due() is False


def test_is_due_true_with_reminder_and_past_due_date(tmp_path):
    engine = _engine(tmp_path)
    past = (datetime.now() - timedelta(hours=1)).isoformat()
    task = engine.add("Tache a rappeler", due_at=past, reminder=True)

    assert task.is_due() is True


def test_is_due_false_for_future_due_date(tmp_path):
    engine = _engine(tmp_path)
    future = (datetime.now() + timedelta(hours=1)).isoformat()
    task = engine.add("Tache future", due_at=future, reminder=True)

    assert task.is_due() is False


def test_get_due_tasks_returns_only_overdue_reminders(tmp_path):
    engine = _engine(tmp_path)
    past = (datetime.now() - timedelta(hours=1)).isoformat()
    future = (datetime.now() + timedelta(hours=1)).isoformat()
    engine.add("En retard, a rappeler", due_at=past, reminder=True)
    engine.add("En retard, sans rappel", due_at=past, reminder=False)
    engine.add("Future, a rappeler", due_at=future, reminder=True)

    due = engine.get_due_tasks()
    assert len(due) == 1
    assert due[0].title == "En retard, a rappeler"


def test_task_dataclass_defaults():
    task = Task(title="Test")
    assert task.done is False
    assert task.reminder is False
    assert task.due_at is None
    assert task.id  # généré automatiquement
