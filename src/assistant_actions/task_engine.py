# ============================================================
# ALFRED — src/assistant_actions/task_engine.py
# Bloc 06.03 — Gestion des tâches
#
# 🎯 UTILITÉ ALFRED :
#   Moteur de tâches local — créer, lister, planifier, terminer, supprimer.
#   Analogue à ReminderEngine (src/v3/proactive/reminder_engine.py, V3 non
#   actif) mais pour l'architecture active (main.py/alfred_desktop.py), avec
#   une échéance optionnelle plutôt qu'obligatoire : une tâche peut exister
#   sans date ("ranger le bureau") ou en avoir une ("appeler le dentiste
#   demain 14h").
#
#   Stockage : data/actions/tasks.json — schéma défini le 16/07/2026
#   (_alfred_header/_meta/tasks), jamais chargé par du code jusqu'ici
#   (status: "SCHEMA_DEFINI"). Ce module est la première implémentation
#   réelle — le header/meta existants sont préservés à chaque sauvegarde.
#
# STATUS  : DRAFT
# ============================================================

from __future__ import annotations

import json
import logging
import uuid
from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)

try:
    from paths import PATHS
    _TASKS_FILE = PATHS.data / "actions" / "tasks.json"
except Exception:
    _TASKS_FILE = Path(__file__).resolve().parents[2] / "data" / "actions" / "tasks.json"

_DEFAULT_HEADER = {
    "_alfred_header": {
        "file": "data/actions/tasks.json",
        "bloc": "Bloc 06.03 — Gestion des tâches",
        "notion_exam": "D06-3 — Capsule Gestion des tâches",
        "utilite_alfred": "Liste des tâches utilisateur — analogue à ReminderEngine (src/v3/proactive/reminder_engine.py) mais pour des tâches sans échéance stricte.",
        "domaine": "Assistance quotidienne — gestion des tâches",
    },
    "_meta": {
        "project": "ALFRED",
        "version": "V1.0",
        "status": "IMPLEMENTE",
        "created": "2026-07-16",
    },
}


@dataclass
class Task:
    """Une tâche utilisateur — échéance optionnelle (contrairement à Reminder,
    où due_at est la raison d'être de l'objet)."""
    id:         str            = field(default_factory=lambda: str(uuid.uuid4())[:8])
    title:      str            = ""
    created_at: str            = field(default_factory=lambda: datetime.now().isoformat())
    due_at:     Optional[str]  = None   # ISO datetime, optionnel
    reminder:   bool           = False  # ALFRED doit-il le rappeler proactivement à échéance ?
    done:       bool           = False
    done_at:    Optional[str]  = None
    notes:      Optional[str]  = None

    def is_due(self) -> bool:
        """True si la tâche a une échéance dépassée, n'est pas déjà terminée,
        et doit être rappelée (reminder=True)."""
        if self.done or not self.due_at or not self.reminder:
            return False
        try:
            due = datetime.fromisoformat(self.due_at)
            now = datetime.now(due.tzinfo) if due.tzinfo else datetime.now()
            return now >= due
        except (ValueError, TypeError):
            return False


class TaskEngine:
    """Moteur de tâches local — stockage JSON, aucun réseau."""

    def __init__(self, storage_path: str | Path = _TASKS_FILE):
        self.storage_path = Path(storage_path)
        self._tasks: list[Task] = []
        self._raw_header: dict = dict(_DEFAULT_HEADER)
        self._load()

    # ------------------------------------------------------------------
    # Persistance
    # ------------------------------------------------------------------

    def _load(self) -> None:
        if not self.storage_path.exists():
            self._tasks = []
            return
        try:
            data = json.loads(self.storage_path.read_text(encoding="utf-8"))
            self._raw_header = {
                k: v for k, v in data.items() if k in ("_alfred_header", "_meta")
            } or dict(_DEFAULT_HEADER)
            self._tasks = [Task(**t) for t in data.get("tasks", [])]
        except Exception as exc:
            logger.warning("task_engine: lecture tasks.json échouée : %s", exc)
            self._tasks = []

    def _save(self) -> None:
        try:
            self.storage_path.parent.mkdir(parents=True, exist_ok=True)
            payload = {
                **self._raw_header,
                "tasks": [asdict(t) for t in self._tasks],
            }
            self.storage_path.write_text(
                json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8"
            )
        except Exception as exc:
            logger.error("task_engine: écriture tasks.json échouée : %s", exc)

    # ------------------------------------------------------------------
    # CRUD
    # ------------------------------------------------------------------

    def add(
        self,
        title: str,
        due_at: Optional[str] = None,
        reminder: bool = False,
        notes: Optional[str] = None,
    ) -> Task:
        task = Task(title=title.strip(), due_at=due_at, reminder=reminder, notes=notes or None)
        self._tasks.append(task)
        self._save()
        return task

    def list(self, include_done: bool = False) -> list[Task]:
        tasks = self._tasks if include_done else [t for t in self._tasks if not t.done]
        return sorted(tasks, key=lambda t: (t.due_at is None, t.due_at or "", t.created_at))

    def get(self, task_id: str) -> Optional[Task]:
        return next((t for t in self._tasks if t.id == task_id), None)

    def find_by_title(self, title_hint: str) -> list[Task]:
        """Résout un extrait de titre vers les tâches correspondantes (pour le
        function-calling — voir src/core/tool_calling.py), même principe que
        find_event() côté Google Agenda."""
        hint = title_hint.strip().lower()
        if not hint:
            return []
        return [t for t in self._tasks if not t.done and hint in t.title.lower()]

    def complete(self, task_id: str) -> Optional[Task]:
        task = self.get(task_id)
        if not task:
            return None
        task.done = True
        task.done_at = datetime.now().isoformat()
        self._save()
        return task

    def delete(self, task_id: str) -> bool:
        before = len(self._tasks)
        self._tasks = [t for t in self._tasks if t.id != task_id]
        if len(self._tasks) != before:
            self._save()
            return True
        return False

    def get_due_tasks(self) -> list[Task]:
        """Tâches avec reminder=True et échéance dépassée, pas encore
        terminées — consommé par le rappel proactif (voir src/ui/tasks_data.py
        et le câblage timer côté alfred_desktop.py)."""
        return [t for t in self._tasks if t.is_due()]
