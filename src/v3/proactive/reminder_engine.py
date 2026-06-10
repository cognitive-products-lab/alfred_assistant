"""
PROJECT      : ALFRED
BLOCK        : B11 -- Intelligence Cognitive
FUNCTION     : 11.05.001 -> 11.05.005
FILE         : src/v3/proactive/reminder_engine.py
ROLE         : Moteur de rappels -- gestion rappels utilisateur locaux

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-05-14
UPDATED      : 2026-05-14
VERSION      : V1.0
STATUS       : TESTED

DESCRIPTION :
Moteur de rappels local ALFRED V3.
Gere les rappels simples (one-shot) et recurrents.
Local-first : aucun cloud, stockage JSON sur disque.

Fonctions couvertes :
  11.05.001 Creation rappel                         OK V1
  11.05.002 Liste rappels actifs                    OK V1
  11.05.003 Rappels dus (trigger check)             OK V1
  11.05.004 Suppression rappel                      OK V1
  11.05.005 Persistence JSON locale                 OK V1
"""

from __future__ import annotations

import json
import uuid
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
from typing import List, Optional

try:
    from paths import DATA_MEMORY
    _DEFAULT_STORAGE = str(DATA_MEMORY / "reminders.json")
except ImportError:
    _DEFAULT_STORAGE = "data/memory/reminders.json"


# ============================================================
# Modele rappel
# ============================================================

@dataclass
class Reminder:
    """Un rappel utilisateur."""
    id:          str   = field(default_factory=lambda: str(uuid.uuid4())[:8])
    title:       str   = ""
    due_at:      str   = ""       # ISO datetime string
    recurrent:   bool  = False
    interval_h:  float = 24.0     # Intervalle si recurrent (heures)
    active:      bool  = True
    created_at:  str   = field(default_factory=lambda: datetime.now().isoformat())

    def is_due(self) -> bool:
        """True si le rappel est arrive a echeance."""
        if not self.active or not self.due_at:
            return False
        try:
            due = datetime.fromisoformat(self.due_at)
            return datetime.now() >= due
        except (ValueError, TypeError):
            return False


# ============================================================
# ReminderEngine
# ============================================================

class ReminderEngine:
    """
    Moteur de rappels local ALFRED V3.
    Stockage JSON, sans cloud, sans serveur.

    Usage :
        engine = ReminderEngine(storage_path="data/reminders.json")
        r = engine.add("Reunion design", due_at="2026-05-14T15:00:00")
        due = engine.get_due_reminders()
    """

    def __init__(self, storage_path: str = _DEFAULT_STORAGE):
        self.storage_path = Path(storage_path)
        self._reminders: List[Reminder] = []
        self._load()

    # --------------------------------------------------------
    # Persistence
    # --------------------------------------------------------

    def _load(self) -> None:
        if not self.storage_path.exists():
            return
        try:
            data = json.loads(self.storage_path.read_text(encoding="utf-8"))
            self._reminders = [Reminder(**r) for r in data]
        except Exception:
            self._reminders = []

    def _save(self) -> None:
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        data = [asdict(r) for r in self._reminders]
        self.storage_path.write_text(
            json.dumps(data, indent=2, ensure_ascii=False),
            encoding="utf-8"
        )

    # --------------------------------------------------------
    # CRUD rappels
    # --------------------------------------------------------

    def add(
        self,
        title:      str,
        due_at:     str,
        recurrent:  bool  = False,
        interval_h: float = 24.0,
    ) -> Reminder:
        """
        Ajoute un rappel.

        Args:
            title      : Titre du rappel
            due_at     : Datetime ISO (ex: "2026-05-14T15:00:00")
            recurrent  : True si rappel recurrent
            interval_h : Intervalle en heures (si recurrent)

        Returns:
            Reminder cree
        """
        r = Reminder(
            title      = title,
            due_at     = due_at,
            recurrent  = recurrent,
            interval_h = interval_h,
        )
        self._reminders.append(r)
        self._save()
        return r

    def remove(self, reminder_id: str) -> bool:
        """
        Supprime un rappel par ID.

        Returns:
            True si supprime, False si non trouve
        """
        before = len(self._reminders)
        self._reminders = [r for r in self._reminders if r.id != reminder_id]
        if len(self._reminders) < before:
            self._save()
            return True
        return False

    def get_active(self) -> List[Reminder]:
        """Retourne tous les rappels actifs."""
        return [r for r in self._reminders if r.active]

    def get_due_reminders(self) -> List[Reminder]:
        """
        Retourne les rappels arrives a echeance.
        Les marque comme inactifs (one-shot) ou met a jour leur date (recurrents).
        """
        due = [r for r in self._reminders if r.is_due()]

        for r in due:
            if r.recurrent:
                from datetime import timedelta
                try:
                    current = datetime.fromisoformat(r.due_at)
                    r.due_at = (current + timedelta(hours=r.interval_h)).isoformat()
                except Exception:
                    r.active = False
            else:
                r.active = False

        if due:
            self._save()

        return due

    def clear_all(self) -> None:
        """Supprime tous les rappels."""
        self._reminders = []
        self._save()

    # --------------------------------------------------------
    # Statut
    # --------------------------------------------------------

    def status(self) -> dict:
        active = self.get_active()
        return {
            "total":          len(self._reminders),
            "active":         len(active),
            "due":            len(self.get_due_reminders()),
            "storage":        str(self.storage_path),
            "version":        "reminder_v1",
        }
