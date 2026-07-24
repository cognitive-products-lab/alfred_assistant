"""
PROJECT      : ALFRED
BLOCK        : B15 — Avatar & Interface
FILE         : src/ui/tasks_data.py
ROLE         : Orchestration tâches pour la vue Tâches + le raccourci
                "Nouvelle tâche" (CRUD, planification, rappels dus)

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-07-24
VERSION      : V1.0
STATUS       : DRAFT

DESCRIPTION :
Point d'entrée unique appelé par AlfredDesktopAPI, même rôle que
src/ui/google_calendar_data.py pour l'agenda. Pas de porte consentement ici
(contrairement à l'agenda/météo) : les tâches sont une donnée 100% locale,
sans appel réseau ni tiers — rien à consentir au sens RGPD, juste du stockage
JSON local (data/actions/tasks.json).
"""

from __future__ import annotations

from dataclasses import asdict

from src.assistant_actions.task_engine import TaskEngine

_engine: TaskEngine | None = None


def _get_engine() -> TaskEngine:
    global _engine
    if _engine is None:
        _engine = TaskEngine()
    return _engine


def get_tasks_state(include_done: bool = False) -> dict:
    """État complet pour la vue Tâches — une seule méthode à appeler côté JS."""
    tasks = _get_engine().list(include_done=include_done)
    return {"ok": True, "tasks": [asdict(t) for t in tasks]}


def create_task(
    title: str,
    due_at: str | None = None,
    reminder: bool = False,
    notes: str | None = None,
) -> dict:
    """Crée une tâche — appelé depuis le raccourci "Nouvelle tâche" et depuis
    les outils du LLM (src/core/tool_calling.py)."""
    title = (title or "").strip()
    if not title:
        return {"ok": False, "error": "Le titre de la tâche est requis."}

    task = _get_engine().add(title=title, due_at=due_at or None, reminder=reminder, notes=notes)
    return {"ok": True, "task": asdict(task)}


def find_tasks(title_hint: str) -> dict:
    """Cherche des tâches par titre approximatif — utilisé par les outils du
    LLM pour résoudre "ma tâche vermifuger le chien" en task_id réel."""
    tasks = _get_engine().find_by_title(title_hint)
    return {"ok": True, "tasks": [asdict(t) for t in tasks]}


def complete_task(task_id: str) -> dict:
    task = _get_engine().complete(task_id)
    if not task:
        return {"ok": False, "error": "Tâche introuvable."}
    return {"ok": True, "task": asdict(task)}


def delete_task(task_id: str) -> dict:
    deleted = _get_engine().delete(task_id)
    if not deleted:
        return {"ok": False, "error": "Tâche introuvable."}
    return {"ok": True}


def get_due_tasks() -> dict:
    """Tâches à rappeler maintenant — consommé par le timer proactif
    (src/alfred_desktop.py) et par l'outil list_due_tasks côté LLM."""
    tasks = _get_engine().get_due_tasks()
    return {"ok": True, "tasks": [asdict(t) for t in tasks]}
