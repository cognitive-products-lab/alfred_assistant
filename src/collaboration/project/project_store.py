"""
PROJECT      : ALFRED
BLOCK        : Bloc 12.01/12.02/12.03/12.05 — Collaboration professionnelle
DASHBOARD    : B10 — Collaboration & Coordination
FILE         : src/collaboration/project/project_store.py
ROLE         : Persistance SQLite — projets, objectifs, tâches, jalons, dépendances,
               décisions, documents

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-07-02
VERSION      : V1.1
STATUS       : TO_TEST

DESCRIPTION :
Couche de stockage SQLite pour le module collaboration professionnelle
(Bloc 12 — docs/ALFRED_BLOCS_REFERENCE.md). Fonctions module-level (pas de
classe), même convention que src/memory/long_term_memory.py. Chemins
ancrés sur paths.PATHS.
"""
# ============================================================
# ALFRED — src/collaboration/project/project_store.py
# Bloc 12.01 Gestion de projet / 12.02 Coordination d'équipe /
# 12.03 Support décisionnel / 12.05 Gestion documentaire (dashboard : B10)
# ============================================================

import sqlite3
from datetime import datetime
from typing import Any

from src.security.security_logger import log_event
from paths import PATHS

# ── Chemins ───────────────────────────────────────────────
_DB_DIR  = PATHS.data_collaboration
_DB_PATH = _DB_DIR / "alfred_collaboration.db"
_DB_DIR.mkdir(parents=True, exist_ok=True)

# ── Statuts valides ───────────────────────────────────────
PROJECT_STATUSES   = {"active", "paused", "done", "archived"}
GOAL_STATUSES       = {"active", "achieved", "dropped"}
TASK_STATUSES       = {"todo", "in_progress", "blocked", "done", "cancelled"}
MILESTONE_STATUSES  = {"pending", "reached", "missed"}
PRIORITIES          = {"low", "medium", "high"}
DOCUMENT_STATUSES    = {"draft", "review", "final", "archived"}
DECISION_ENTRY_TYPE  = "decision"


def _get_conn() -> sqlite3.Connection:
    """Retourne une connexion SQLite avec row_factory et clés étrangères actives."""
    conn = sqlite3.connect(str(_DB_PATH))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db() -> None:
    """Crée les tables SQLite si elles n'existent pas. Appelé au démarrage d'ALFRED."""
    with _get_conn() as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS projects (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                name        TEXT NOT NULL UNIQUE,
                description TEXT DEFAULT '',
                status      TEXT DEFAULT 'active',
                deadline    TEXT,
                created_at  TEXT NOT NULL,
                updated_at  TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS goals (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                project_id  INTEGER NOT NULL REFERENCES projects(id),
                title       TEXT NOT NULL,
                description TEXT DEFAULT '',
                status      TEXT DEFAULT 'active',
                priority    TEXT DEFAULT 'medium',
                target_date TEXT,
                created_at  TEXT NOT NULL,
                updated_at  TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS tasks (
                id             INTEGER PRIMARY KEY AUTOINCREMENT,
                project_id     INTEGER NOT NULL REFERENCES projects(id),
                goal_id        INTEGER REFERENCES goals(id),
                title          TEXT NOT NULL,
                description    TEXT DEFAULT '',
                status         TEXT DEFAULT 'todo',
                priority       TEXT DEFAULT 'medium',
                due_date       TEXT,
                assignee       TEXT DEFAULT '',
                blocked_reason TEXT DEFAULT '',
                created_at     TEXT NOT NULL,
                updated_at     TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS task_dependencies (
                id                  INTEGER PRIMARY KEY AUTOINCREMENT,
                task_id             INTEGER NOT NULL REFERENCES tasks(id),
                depends_on_task_id  INTEGER NOT NULL REFERENCES tasks(id),
                UNIQUE(task_id, depends_on_task_id)
            );

            CREATE TABLE IF NOT EXISTS milestones (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                project_id  INTEGER NOT NULL REFERENCES projects(id),
                title       TEXT NOT NULL,
                target_date TEXT,
                status      TEXT DEFAULT 'pending',
                created_at  TEXT NOT NULL,
                updated_at  TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS journal (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                project_id  INTEGER NOT NULL REFERENCES projects(id),
                timestamp   TEXT NOT NULL,
                content     TEXT NOT NULL,
                entry_type  TEXT DEFAULT 'note',
                options_considered TEXT DEFAULT '',
                rationale   TEXT DEFAULT ''
            );

            CREATE TABLE IF NOT EXISTS documents (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                project_id  INTEGER NOT NULL REFERENCES projects(id),
                title       TEXT NOT NULL,
                location    TEXT DEFAULT '',
                doc_type    TEXT DEFAULT 'note',
                status      TEXT DEFAULT 'draft',
                created_at  TEXT NOT NULL,
                updated_at  TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS state (
                key   TEXT PRIMARY KEY,
                value TEXT
            );

            CREATE INDEX IF NOT EXISTS idx_goals_project      ON goals(project_id);
            CREATE INDEX IF NOT EXISTS idx_tasks_project       ON tasks(project_id);
            CREATE INDEX IF NOT EXISTS idx_tasks_goal          ON tasks(goal_id);
            CREATE INDEX IF NOT EXISTS idx_tasks_status        ON tasks(status);
            CREATE INDEX IF NOT EXISTS idx_deps_task           ON task_dependencies(task_id);
            CREATE INDEX IF NOT EXISTS idx_milestones_project  ON milestones(project_id);
            CREATE INDEX IF NOT EXISTS idx_journal_project     ON journal(project_id);
            CREATE INDEX IF NOT EXISTS idx_documents_project   ON documents(project_id);
        """)
    log_event("Base collaboration professionnelle (Bloc 12 / dashboard B10) initialisée")


# ─────────────────────────────────────────────────────────
# Projets
# ─────────────────────────────────────────────────────────

def create_project(name: str, description: str = "", deadline: str | None = None) -> int:
    """Crée un projet. Lève sqlite3.IntegrityError si le nom existe déjà."""
    now = datetime.now().isoformat()
    with _get_conn() as conn:
        cursor = conn.execute("""
            INSERT INTO projects (name, description, status, deadline, created_at, updated_at)
            VALUES (?, ?, 'active', ?, ?, ?)
        """, (name, description, deadline, now, now))
        return cursor.lastrowid


def get_project_by_name(name: str) -> dict | None:
    with _get_conn() as conn:
        row = conn.execute("SELECT * FROM projects WHERE name = ?", (name,)).fetchone()
    return dict(row) if row else None


def get_project_by_id(project_id: int) -> dict | None:
    with _get_conn() as conn:
        row = conn.execute("SELECT * FROM projects WHERE id = ?", (project_id,)).fetchone()
    return dict(row) if row else None


def list_projects(status: str | None = None) -> list[dict]:
    with _get_conn() as conn:
        if status:
            rows = conn.execute(
                "SELECT * FROM projects WHERE status = ? ORDER BY updated_at DESC", (status,)
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT * FROM projects ORDER BY updated_at DESC"
            ).fetchall()
    return [dict(r) for r in rows]


def update_project_status(project_id: int, status: str) -> None:
    if status not in PROJECT_STATUSES:
        raise ValueError(f"Statut projet invalide : {status}")
    with _get_conn() as conn:
        conn.execute(
            "UPDATE projects SET status = ?, updated_at = ? WHERE id = ?",
            (status, datetime.now().isoformat(), project_id),
        )


# ─────────────────────────────────────────────────────────
# Pointeur "projet actif"
# ─────────────────────────────────────────────────────────

def set_active_project_id(project_id: int) -> None:
    with _get_conn() as conn:
        conn.execute("""
            INSERT INTO state (key, value) VALUES ('active_project_id', ?)
            ON CONFLICT(key) DO UPDATE SET value = excluded.value
        """, (str(project_id),))


def get_active_project_id() -> int | None:
    with _get_conn() as conn:
        row = conn.execute("SELECT value FROM state WHERE key = 'active_project_id'").fetchone()
    if row is None or row["value"] is None:
        return None
    try:
        return int(row["value"])
    except (TypeError, ValueError):
        return None


# ─────────────────────────────────────────────────────────
# Objectifs (goals)
# ─────────────────────────────────────────────────────────

def add_goal(
    project_id: int,
    title: str,
    description: str = "",
    priority: str = "medium",
    target_date: str | None = None,
) -> int:
    now = datetime.now().isoformat()
    with _get_conn() as conn:
        cursor = conn.execute("""
            INSERT INTO goals (project_id, title, description, status, priority, target_date, created_at, updated_at)
            VALUES (?, ?, ?, 'active', ?, ?, ?, ?)
        """, (project_id, title, description, priority, target_date, now, now))
        return cursor.lastrowid


def get_goals(project_id: int, status: str | None = None) -> list[dict]:
    with _get_conn() as conn:
        if status:
            rows = conn.execute(
                "SELECT * FROM goals WHERE project_id = ? AND status = ? ORDER BY priority DESC, target_date",
                (project_id, status),
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT * FROM goals WHERE project_id = ? ORDER BY status, priority DESC", (project_id,)
            ).fetchall()
    return [dict(r) for r in rows]


def update_goal_status(goal_id: int, status: str) -> None:
    if status not in GOAL_STATUSES:
        raise ValueError(f"Statut objectif invalide : {status}")
    with _get_conn() as conn:
        conn.execute(
            "UPDATE goals SET status = ?, updated_at = ? WHERE id = ?",
            (status, datetime.now().isoformat(), goal_id),
        )


# ─────────────────────────────────────────────────────────
# Tâches
# ─────────────────────────────────────────────────────────

def add_task(
    project_id: int,
    title: str,
    goal_id: int | None = None,
    description: str = "",
    priority: str = "medium",
    due_date: str | None = None,
    assignee: str = "",
) -> int:
    now = datetime.now().isoformat()
    with _get_conn() as conn:
        cursor = conn.execute("""
            INSERT INTO tasks (project_id, goal_id, title, description, status, priority, due_date, assignee, created_at, updated_at)
            VALUES (?, ?, ?, ?, 'todo', ?, ?, ?, ?, ?)
        """, (project_id, goal_id, title, description, priority, due_date, assignee, now, now))
        return cursor.lastrowid


def get_tasks_by_assignee(project_id: int, assignee: str) -> list[dict]:
    with _get_conn() as conn:
        rows = conn.execute("""
            SELECT * FROM tasks WHERE project_id = ? AND assignee = ?
            ORDER BY status, priority DESC, due_date
        """, (project_id, assignee)).fetchall()
    return [dict(r) for r in rows]


def get_task(task_id: int) -> dict | None:
    with _get_conn() as conn:
        row = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    return dict(row) if row else None


def get_tasks(project_id: int, status: str | None = None) -> list[dict]:
    with _get_conn() as conn:
        if status:
            rows = conn.execute(
                "SELECT * FROM tasks WHERE project_id = ? AND status = ? ORDER BY priority DESC, due_date",
                (project_id, status),
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT * FROM tasks WHERE project_id = ? ORDER BY status, priority DESC, due_date",
                (project_id,),
            ).fetchall()
    return [dict(r) for r in rows]


def find_task_by_title(project_id: int, title_fragment: str) -> dict | None:
    """Recherche approximative — utilisée par les commandes en langage naturel."""
    with _get_conn() as conn:
        row = conn.execute("""
            SELECT * FROM tasks
            WHERE project_id = ? AND status NOT IN ('done', 'cancelled') AND title LIKE ?
            ORDER BY updated_at DESC LIMIT 1
        """, (project_id, f"%{title_fragment}%")).fetchone()
    return dict(row) if row else None


def update_task_status(task_id: int, status: str, blocked_reason: str = "") -> None:
    if status not in TASK_STATUSES:
        raise ValueError(f"Statut tâche invalide : {status}")
    with _get_conn() as conn:
        conn.execute(
            "UPDATE tasks SET status = ?, blocked_reason = ?, updated_at = ? WHERE id = ?",
            (status, blocked_reason if status == "blocked" else "", datetime.now().isoformat(), task_id),
        )


# ─────────────────────────────────────────────────────────
# Dépendances entre tâches
# ─────────────────────────────────────────────────────────

def add_dependency(task_id: int, depends_on_task_id: int) -> None:
    if task_id == depends_on_task_id:
        raise ValueError("Une tâche ne peut pas dépendre d'elle-même.")
    with _get_conn() as conn:
        conn.execute("""
            INSERT OR IGNORE INTO task_dependencies (task_id, depends_on_task_id)
            VALUES (?, ?)
        """, (task_id, depends_on_task_id))


def get_dependencies(task_id: int) -> list[dict]:
    """Retourne les tâches dont dépend task_id (doivent être terminées avant)."""
    with _get_conn() as conn:
        rows = conn.execute("""
            SELECT t.* FROM tasks t
            JOIN task_dependencies d ON d.depends_on_task_id = t.id
            WHERE d.task_id = ?
        """, (task_id,)).fetchall()
    return [dict(r) for r in rows]


# ─────────────────────────────────────────────────────────
# Jalons
# ─────────────────────────────────────────────────────────

def add_milestone(project_id: int, title: str, target_date: str | None = None) -> int:
    now = datetime.now().isoformat()
    with _get_conn() as conn:
        cursor = conn.execute("""
            INSERT INTO milestones (project_id, title, target_date, status, created_at, updated_at)
            VALUES (?, ?, ?, 'pending', ?, ?)
        """, (project_id, title, target_date, now, now))
        return cursor.lastrowid


def get_milestones(project_id: int, status: str | None = None) -> list[dict]:
    with _get_conn() as conn:
        if status:
            rows = conn.execute(
                "SELECT * FROM milestones WHERE project_id = ? AND status = ? ORDER BY target_date",
                (project_id, status),
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT * FROM milestones WHERE project_id = ? ORDER BY target_date", (project_id,)
            ).fetchall()
    return [dict(r) for r in rows]


def update_milestone_status(milestone_id: int, status: str) -> None:
    if status not in MILESTONE_STATUSES:
        raise ValueError(f"Statut jalon invalide : {status}")
    with _get_conn() as conn:
        conn.execute(
            "UPDATE milestones SET status = ?, updated_at = ? WHERE id = ?",
            (status, datetime.now().isoformat(), milestone_id),
        )


# ─────────────────────────────────────────────────────────
# Journal (notes / risques) — 12.03 mémoire des décisions
# ─────────────────────────────────────────────────────────

def add_journal_entry(project_id: int, content: str, entry_type: str = "note") -> int:
    with _get_conn() as conn:
        cursor = conn.execute("""
            INSERT INTO journal (project_id, timestamp, content, entry_type)
            VALUES (?, ?, ?, ?)
        """, (project_id, datetime.now().isoformat(), content, entry_type))
        return cursor.lastrowid


def get_journal(project_id: int, n: int = 10, entry_type: str | None = None) -> list[dict]:
    with _get_conn() as conn:
        if entry_type:
            rows = conn.execute("""
                SELECT * FROM journal WHERE project_id = ? AND entry_type = ?
                ORDER BY timestamp DESC LIMIT ?
            """, (project_id, entry_type, n)).fetchall()
        else:
            rows = conn.execute("""
                SELECT * FROM journal WHERE project_id = ?
                ORDER BY timestamp DESC LIMIT ?
            """, (project_id, n)).fetchall()
    return [dict(r) for r in rows]


def add_decision(
    project_id: int,
    content: str,
    options_considered: str = "",
    rationale: str = "",
) -> int:
    """Enregistre une décision — le 'options_considered' et 'rationale' forment la mémoire de décision (12.03)."""
    with _get_conn() as conn:
        cursor = conn.execute("""
            INSERT INTO journal (project_id, timestamp, content, entry_type, options_considered, rationale)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (project_id, datetime.now().isoformat(), content, DECISION_ENTRY_TYPE, options_considered, rationale))
        return cursor.lastrowid


def get_decisions(project_id: int, n: int = 10) -> list[dict]:
    return get_journal(project_id, n=n, entry_type=DECISION_ENTRY_TYPE)


# ─────────────────────────────────────────────────────────
# Documents — 12.05 gestion documentaire
# ─────────────────────────────────────────────────────────

def add_document(
    project_id: int,
    title: str,
    location: str = "",
    doc_type: str = "note",
    status: str = "draft",
) -> int:
    now = datetime.now().isoformat()
    with _get_conn() as conn:
        cursor = conn.execute("""
            INSERT INTO documents (project_id, title, location, doc_type, status, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (project_id, title, location, doc_type, status, now, now))
        return cursor.lastrowid


def get_documents(project_id: int, status: str | None = None) -> list[dict]:
    with _get_conn() as conn:
        if status:
            rows = conn.execute(
                "SELECT * FROM documents WHERE project_id = ? AND status = ? ORDER BY updated_at DESC",
                (project_id, status),
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT * FROM documents WHERE project_id = ? ORDER BY updated_at DESC", (project_id,)
            ).fetchall()
    return [dict(r) for r in rows]


def update_document_status(document_id: int, status: str) -> None:
    if status not in DOCUMENT_STATUSES:
        raise ValueError(f"Statut document invalide : {status}")
    with _get_conn() as conn:
        conn.execute(
            "UPDATE documents SET status = ?, updated_at = ? WHERE id = ?",
            (status, datetime.now().isoformat(), document_id),
        )
