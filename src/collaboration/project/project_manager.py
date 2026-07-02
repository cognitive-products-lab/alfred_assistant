"""
PROJECT      : ALFRED
BLOCK        : Bloc 12.01/12.02/12.03/12.04/12.05 — Collaboration professionnelle
DASHBOARD    : B10 — Collaboration & Coordination
FILE         : src/collaboration/project/project_manager.py
ROLE         : API haut niveau + raisonnement — gestion de projet / stratégie

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-07-02
VERSION      : V1.2
STATUS       : TO_TEST

DESCRIPTION :
Couche métier au-dessus de project_store.py (SQLite). Expose la création
et la lecture/écriture d'objectifs/tâches/jalons/décisions/documents, un
pointeur "projet actif", un raisonnement simple de priorisation (prochaines
actions actionnables selon les dépendances) et le formatage du contexte
pour injection dans le prompt système ALFRED (cf. response_generator.py,
clé de contexte "pm_context").

Couvre les sous-codes officiels du Bloc 12 (docs/ALFRED_BLOCS_REFERENCE.md) :
  12.01 Gestion de projet      -> projets/objectifs/tâches/jalons/dépendances
  12.02 Coordination d'équipe  -> champ "assignee" sur les tâches
  12.03 Support décisionnel    -> add_decision/get_decisions (mémoire des décisions)
  12.04 Communication professionnelle -> generate_status_report() (co-rédaction) +
                                          context["collaboration_mode"] (registre pro, voir response_generator.py)
  12.05 Gestion documentaire   -> add_document/get_documents
"""
# ============================================================
# ALFRED — src/collaboration/project/project_manager.py
# Bloc 12.01/12.02/12.03/12.04/12.05 — Collaboration professionnelle (dashboard : B10)
# ============================================================

from datetime import date
from typing import Any

from src.collaboration.project import project_store as store

_PRIORITY_RANK = {"high": 0, "medium": 1, "low": 2}


# ─────────────────────────────────────────────────────────
# Init
# ─────────────────────────────────────────────────────────

def init_db() -> None:
    store.init_db()


# ─────────────────────────────────────────────────────────
# Projets & projet actif
# ─────────────────────────────────────────────────────────

def create_project(name: str, description: str = "", deadline: str | None = None, activate: bool = True) -> int:
    """
    Crée un projet et l'active par défaut.

    Args:
        name        : Nom unique du projet
        description : Description libre
        deadline    : Échéance ISO (YYYY-MM-DD), optionnelle
        activate    : Si True, devient le projet actif

    Returns:
        ID du projet créé
    """
    project_id = store.create_project(name=name, description=description, deadline=deadline)
    if activate:
        store.set_active_project_id(project_id)
    return project_id


def list_projects(status: str | None = None) -> list[dict]:
    return store.list_projects(status=status)


def resolve_project(name_or_none: str | None = None) -> dict | None:
    """
    Résout un projet par nom (insensible à la casse), ou retourne le
    projet actif si aucun nom n'est fourni.
    """
    if name_or_none:
        for p in store.list_projects():
            if p["name"].lower() == name_or_none.strip().lower():
                return p
        return None

    active_id = store.get_active_project_id()
    if active_id:
        p = store.get_project_by_id(active_id)
        if p:
            return p

    # Fallback : un seul projet actif existant -> on le considère implicite
    active_projects = store.list_projects(status="active")
    if len(active_projects) == 1:
        return active_projects[0]
    return None


def set_active_project(name: str) -> dict | None:
    project = resolve_project(name)
    if project:
        store.set_active_project_id(project["id"])
    return project


def get_active_project() -> dict | None:
    return resolve_project(None)


# ─────────────────────────────────────────────────────────
# Objectifs
# ─────────────────────────────────────────────────────────

def add_goal(project_name: str | None, title: str, priority: str = "medium", target_date: str | None = None) -> int | None:
    project = resolve_project(project_name)
    if not project:
        return None
    return store.add_goal(project["id"], title=title, priority=priority, target_date=target_date)


# ─────────────────────────────────────────────────────────
# Tâches (12.01 gestion de projet, 12.02 coordination d'équipe)
# ─────────────────────────────────────────────────────────

def add_task(
    project_name: str | None,
    title: str,
    goal_id: int | None = None,
    priority: str = "medium",
    due_date: str | None = None,
    assignee: str = "",
) -> int | None:
    project = resolve_project(project_name)
    if not project:
        return None
    return store.add_task(
        project["id"], title=title, goal_id=goal_id, priority=priority,
        due_date=due_date, assignee=assignee,
    )


def update_task_status(project_name: str | None, title_fragment: str, status: str, blocked_reason: str = "") -> dict | None:
    project = resolve_project(project_name)
    if not project:
        return None
    task = store.find_task_by_title(project["id"], title_fragment)
    if not task:
        return None
    store.update_task_status(task["id"], status=status, blocked_reason=blocked_reason)
    return task


def add_dependency_by_title(project_name: str | None, task_title: str, depends_on_title: str) -> bool:
    project = resolve_project(project_name)
    if not project:
        return False
    task = store.find_task_by_title(project["id"], task_title)
    depends_on = store.find_task_by_title(project["id"], depends_on_title)
    if not task or not depends_on:
        return False
    store.add_dependency(task["id"], depends_on["id"])
    return True


def get_tasks_by_assignee(project_name: str | None, assignee: str) -> list[dict]:
    """12.02 Coordination d'équipe — charge de travail par personne."""
    project = resolve_project(project_name)
    if not project:
        return []
    return store.get_tasks_by_assignee(project["id"], assignee)


# ─────────────────────────────────────────────────────────
# Jalons
# ─────────────────────────────────────────────────────────

def add_milestone(project_name: str | None, title: str, target_date: str | None = None) -> int | None:
    project = resolve_project(project_name)
    if not project:
        return None
    return store.add_milestone(project["id"], title=title, target_date=target_date)


# ─────────────────────────────────────────────────────────
# Journal / décisions (12.03 support décisionnel)
# ─────────────────────────────────────────────────────────

def add_journal_entry(project_name: str | None, content: str, entry_type: str = "note") -> int | None:
    project = resolve_project(project_name)
    if not project:
        return None
    return store.add_journal_entry(project["id"], content=content, entry_type=entry_type)


def add_decision(
    project_name: str | None,
    content: str,
    options_considered: str = "",
    rationale: str = "",
) -> int | None:
    """
    Enregistre une décision structurée (mémoire des décisions — 12.03).

    Args:
        content             : La décision elle-même, en une phrase
        options_considered  : Les alternatives envisagées
        rationale           : Pourquoi ce choix plutôt qu'un autre
    """
    project = resolve_project(project_name)
    if not project:
        return None
    return store.add_decision(
        project["id"], content=content,
        options_considered=options_considered, rationale=rationale,
    )


def get_decisions(project_name: str | None = None, n: int = 5) -> list[dict]:
    project = resolve_project(project_name)
    if not project:
        return []
    return store.get_decisions(project["id"], n=n)


# ─────────────────────────────────────────────────────────
# Documents (12.05 gestion documentaire)
# ─────────────────────────────────────────────────────────

def add_document(
    project_name: str | None,
    title: str,
    location: str = "",
    doc_type: str = "note",
    status: str = "draft",
) -> int | None:
    project = resolve_project(project_name)
    if not project:
        return None
    return store.add_document(project["id"], title=title, location=location, doc_type=doc_type, status=status)


def get_documents(project_name: str | None = None, status: str | None = None) -> list[dict]:
    project = resolve_project(project_name)
    if not project:
        return []
    return store.get_documents(project["id"], status=status)


def update_document_status_by_title(project_name: str | None, title_fragment: str, status: str) -> dict | None:
    project = resolve_project(project_name)
    if not project:
        return None
    for doc in store.get_documents(project["id"]):
        if title_fragment.lower() in doc["title"].lower():
            store.update_document_status(doc["id"], status)
            doc["status"] = status
            return doc
    return None


# ─────────────────────────────────────────────────────────
# Raisonnement — prochaines actions actionnables
# ─────────────────────────────────────────────────────────

def get_next_actions(project_id: int, limit: int = 3) -> list[dict]:
    """
    Détermine les tâches actionnables immédiatement : statut todo/in_progress
    ET toutes leurs dépendances sont à l'état 'done'.
    Triées par priorité puis échéance (les tâches sans échéance en dernier).

    C'est le cœur du raisonnement de priorisation d'ALFRED : il ne suggère
    jamais une tâche encore bloquée par une dépendance non terminée.
    """
    candidates = []
    for task in store.get_tasks(project_id):
        if task["status"] not in ("todo", "in_progress"):
            continue
        deps = store.get_dependencies(task["id"])
        if any(d["status"] != "done" for d in deps):
            continue
        candidates.append(task)

    candidates.sort(
        key=lambda t: (
            _PRIORITY_RANK.get(t["priority"], 1),
            t["due_date"] or "9999-99-99",
        )
    )
    return candidates[:limit]


def get_blocked_tasks(project_id: int) -> list[dict]:
    return store.get_tasks(project_id, status="blocked")


def get_overdue_tasks(project_id: int) -> list[dict]:
    today = date.today().isoformat()
    overdue = []
    for task in store.get_tasks(project_id):
        if task["status"] in ("done", "cancelled"):
            continue
        if task["due_date"] and task["due_date"] < today:
            overdue.append(task)
    return overdue


def get_upcoming_milestones(project_id: int, limit: int = 3) -> list[dict]:
    pending = store.get_milestones(project_id, status="pending")
    pending.sort(key=lambda m: m["target_date"] or "9999-99-99")
    return pending[:limit]


def get_project_summary(project_id: int) -> dict[str, Any]:
    """Résumé structuré d'un projet — base des dashboards et du contexte prompt."""
    tasks = store.get_tasks(project_id)
    status_counts: dict[str, int] = {}
    for t in tasks:
        status_counts[t["status"]] = status_counts.get(t["status"], 0) + 1

    return {
        "task_status_counts": status_counts,
        "tasks_total": len(tasks),
        "goals_active": store.get_goals(project_id, status="active"),
        "blocked_tasks": get_blocked_tasks(project_id),
        "overdue_tasks": get_overdue_tasks(project_id),
        "next_actions": get_next_actions(project_id),
        "upcoming_milestones": get_upcoming_milestones(project_id),
        "recent_decisions": store.get_decisions(project_id, n=3),
        "open_documents": store.get_documents(project_id, status="draft") + store.get_documents(project_id, status="review"),
    }


# ─────────────────────────────────────────────────────────
# Formatage pour injection dans le prompt LLM
# ─────────────────────────────────────────────────────────

def format_context_for_prompt(project_name: str | None = None) -> str:
    """
    Formate l'état du projet actif (ou nommé) pour injection dans le
    prompt système ALFRED (context["pm_context"], voir main.py/build_response).
    Retourne une chaîne vide si aucun projet actif n'est résolu.
    """
    project = resolve_project(project_name)
    if not project:
        return ""

    summary = get_project_summary(project["id"])
    lines = [f"Projet actif : {project['name']} (statut : {project['status']})"]
    if project.get("deadline"):
        lines.append(f"Échéance projet : {project['deadline']}")
    if project.get("description"):
        lines.append(f"Description : {project['description']}")

    if summary["goals_active"]:
        lines.append("Objectifs actifs :")
        for g in summary["goals_active"]:
            due = f" (échéance {g['target_date']})" if g["target_date"] else ""
            lines.append(f"  - [{g['priority']}] {g['title']}{due}")

    counts = summary["task_status_counts"]
    if counts:
        counts_str = ", ".join(f"{v} {k}" for k, v in counts.items())
        lines.append(f"Tâches ({summary['tasks_total']} au total) : {counts_str}")

    if summary["blocked_tasks"]:
        lines.append("Tâches bloquées :")
        for t in summary["blocked_tasks"]:
            reason = f" — {t['blocked_reason']}" if t["blocked_reason"] else ""
            who = f" (assignée à {t['assignee']})" if t.get("assignee") else ""
            lines.append(f"  - {t['title']}{who}{reason}")

    if summary["overdue_tasks"]:
        lines.append("Tâches en retard :")
        for t in summary["overdue_tasks"]:
            lines.append(f"  - {t['title']} (échéance dépassée : {t['due_date']})")

    if summary["next_actions"]:
        lines.append("Prochaines actions actionnables (dépendances levées) :")
        for t in summary["next_actions"]:
            due = f" (échéance {t['due_date']})" if t["due_date"] else ""
            who = f" — {t['assignee']}" if t.get("assignee") else ""
            lines.append(f"  - [{t['priority']}] {t['title']}{due}{who}")

    if summary["upcoming_milestones"]:
        lines.append("Jalons à venir :")
        for m in summary["upcoming_milestones"]:
            date_str = f" — {m['target_date']}" if m["target_date"] else ""
            lines.append(f"  - {m['title']}{date_str}")

    if summary["recent_decisions"]:
        lines.append("Décisions récentes :")
        for d in summary["recent_decisions"]:
            rationale = f" (raison : {d['rationale']})" if d.get("rationale") else ""
            lines.append(f"  - {d['content']}{rationale}")

    if summary["open_documents"]:
        lines.append("Documents en cours :")
        for doc in summary["open_documents"]:
            loc = f" — {doc['location']}" if doc.get("location") else ""
            lines.append(f"  - [{doc['status']}] {doc['title']}{loc}")

    return "\n".join(lines)


# ─────────────────────────────────────────────────────────
# Co-rédaction — 12.04 Communication professionnelle
# ─────────────────────────────────────────────────────────

def generate_status_report(project_name: str | None = None, save_as_document: bool = False) -> str:
    """
    Génère un compte-rendu d'avancement prêt à être envoyé (co-rédaction —
    12.04), à partir des mêmes données structurées que format_context_for_prompt
    mais mis en forme comme un livrable plutôt qu'un bloc de contexte prompt.

    Args:
        project_name     : Projet ciblé (défaut : projet actif)
        save_as_document : Si True, enregistre le rapport dans le registre
                            documentaire du projet (12.05, doc_type="rapport")

    Returns:
        Le rapport formaté, ou une chaîne vide si aucun projet n'est résolu.
    """
    project = resolve_project(project_name)
    if not project:
        return ""

    summary = get_project_summary(project["id"])
    today = date.today().isoformat()

    lines = [
        f"COMPTE-RENDU D'AVANCEMENT — {project['name']}",
        f"Date : {today}",
        "",
        "OBJECTIF",
    ]
    if summary["goals_active"]:
        for g in summary["goals_active"]:
            due = f", échéance {g['target_date']}" if g["target_date"] else ""
            lines.append(f"- {g['title']}{due}")
    else:
        lines.append("- (aucun objectif actif défini)")

    counts = summary["task_status_counts"]
    total = summary["tasks_total"]
    done = counts.get("done", 0)
    pct = round(100 * done / total) if total else 0
    lines += ["", "AVANCEMENT", f"- {done}/{total} tâches terminées ({pct}%)"]
    for status, n in counts.items():
        if status != "done":
            lines.append(f"- {n} en statut « {status} »")

    lines += ["", "POINTS DE BLOCAGE"]
    if summary["blocked_tasks"] or summary["overdue_tasks"]:
        for t in summary["blocked_tasks"]:
            reason = f" — {t['blocked_reason']}" if t["blocked_reason"] else ""
            lines.append(f"- {t['title']}{reason}")
        for t in summary["overdue_tasks"]:
            lines.append(f"- {t['title']} (retard, échéance {t['due_date']})")
    else:
        lines.append("- Aucun")

    lines += ["", "PROCHAINES ACTIONS"]
    if summary["next_actions"]:
        for t in summary["next_actions"]:
            who = f" ({t['assignee']})" if t.get("assignee") else ""
            lines.append(f"- {t['title']}{who}")
    else:
        lines.append("- Aucune action immédiatement actionnable")

    if summary["recent_decisions"]:
        lines += ["", "DÉCISIONS RÉCENTES"]
        for d in summary["recent_decisions"]:
            lines.append(f"- {d['content']}")

    if summary["upcoming_milestones"]:
        lines += ["", "PROCHAINS JALONS"]
        for m in summary["upcoming_milestones"]:
            date_str = f" — {m['target_date']}" if m["target_date"] else ""
            lines.append(f"- {m['title']}{date_str}")

    report = "\n".join(lines)

    if save_as_document:
        store.add_document(
            project["id"],
            title=f"Compte-rendu {today}",
            doc_type="rapport",
            status="final",
        )

    return report
