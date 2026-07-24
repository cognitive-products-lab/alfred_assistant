"""
PROJECT      : ALFRED
BLOCK        : B06.03
FILE         : tests/b06_tests/test_tool_calling_tasks.py
ROLE         : Tests unitaires des outils "tâches" de src/core/tool_calling.py

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-07-24
VERSION      : V1.0
STATUS       : TESTED

DESCRIPTION :
src.ui.tasks_data est monkeypatché — ces tests vérifient le dispatch et la
résolution title_hint -> tâche unique, pas le moteur réel (voir
test_task_engine.py pour ça).
"""

from __future__ import annotations

import src.ui.tasks_data as tasks_data
from src.core import tool_calling


def test_create_task_minimal(monkeypatch):
    monkeypatch.setattr(
        tasks_data, "create_task",
        lambda **kw: {"ok": True, "task": {"id": "t1", "title": kw["title"], "due_at": kw.get("due_at")}},
    )

    result = tool_calling.execute_tool("create_task", {"title": "Ranger le bureau"})

    assert result == {"ok": True, "task": {"id": "t1", "title": "Ranger le bureau", "due_at": None}}


def test_create_task_with_date_and_time_builds_due_at(monkeypatch):
    captured = {}

    def fake_create_task(**kw):
        captured.update(kw)
        return {"ok": True, "task": {"id": "t2", **kw}}

    monkeypatch.setattr(tasks_data, "create_task", fake_create_task)

    tool_calling.execute_tool(
        "create_task",
        {"title": "Appeler le dentiste", "due_date": "2026-07-25", "due_time": "14:30", "reminder": True},
    )

    assert captured["due_at"].startswith("2026-07-25T14:30:00")
    assert captured["reminder"] is True


def test_create_task_error_propagates(monkeypatch):
    monkeypatch.setattr(
        tasks_data, "create_task",
        lambda **kw: {"ok": False, "error": "Le titre de la tâche est requis."},
    )

    result = tool_calling.execute_tool("create_task", {"title": ""})
    assert result == {"ok": False, "error": "Le titre de la tâche est requis."}


def test_list_tasks(monkeypatch):
    monkeypatch.setattr(
        tasks_data, "get_tasks_state",
        lambda include_done=False: {"ok": True, "tasks": [{"id": "t1", "title": "X"}]},
    )

    result = tool_calling.execute_tool("list_tasks", {})
    assert result == {"ok": True, "tasks": [{"id": "t1", "title": "X"}]}


def test_complete_task_resolves_single_match(monkeypatch):
    monkeypatch.setattr(
        tasks_data, "find_tasks",
        lambda hint: {"ok": True, "tasks": [{"id": "t1", "title": "Vermifuger les chiens"}]},
    )
    monkeypatch.setattr(
        tasks_data, "complete_task",
        lambda task_id: {"ok": True, "task": {"id": task_id, "title": "Vermifuger les chiens", "done": True}},
    )

    result = tool_calling.execute_tool("complete_task", {"title_hint": "vermifuger"})

    assert result["ok"] is True
    assert result["task"]["done"] is True


def test_complete_task_no_match_returns_clear_error(monkeypatch):
    monkeypatch.setattr(tasks_data, "find_tasks", lambda hint: {"ok": True, "tasks": []})

    result = tool_calling.execute_tool("complete_task", {"title_hint": "inexistant"})

    assert result["ok"] is False
    assert "inexistant" in result["error"]


def test_complete_task_ambiguous_match_lists_candidates(monkeypatch):
    monkeypatch.setattr(
        tasks_data, "find_tasks",
        lambda hint: {"ok": True, "tasks": [
            {"id": "t1", "title": "Appeler le dentiste"},
            {"id": "t2", "title": "Appeler le garagiste"},
        ]},
    )

    result = tool_calling.execute_tool("complete_task", {"title_hint": "appeler"})

    assert result["ok"] is False
    assert "dentiste" in result["error"] and "garagiste" in result["error"]


def test_delete_task_resolves_and_deletes(monkeypatch):
    monkeypatch.setattr(
        tasks_data, "find_tasks",
        lambda hint: {"ok": True, "tasks": [{"id": "t1", "title": "Tache a supprimer"}]},
    )
    monkeypatch.setattr(tasks_data, "delete_task", lambda task_id: {"ok": True})

    result = tool_calling.execute_tool("delete_task", {"title_hint": "supprimer"})

    assert result == {"ok": True, "deleted_title": "Tache a supprimer"}


def test_unknown_tool_name_returns_error():
    result = tool_calling.execute_tool("does_not_exist", {})
    assert result["ok"] is False
    assert "does_not_exist" in result["error"]
