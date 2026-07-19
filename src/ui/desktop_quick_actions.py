"""
PROJECT      : ALFRED
BLOCK        : B15 — Avatar & Interface
FILE         : src/ui/desktop_quick_actions.py
ROLE         : Actions rapides du dashboard desktop, adossées à de vrais backends

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-07-19
VERSION      : V1.0
STATUS       : DRAFT

DESCRIPTION :
Le widget "Actions rapides" n'avait aucun handler câblé (à part "Ouvrir le
mode vocal", déjà réel). Sur les 5 boutons de la maquette, seuls 3 ont un
backend réel exploitable directement — les 2 autres restent volontairement
inertes avec un message honnête plutôt qu'un faux comportement :
  - "Lancer une sauvegarde"      -> run_backup() (réel, ce module)
  - "Résumer ma journée"         -> summarize_today() (réel, ce module)
  - "Rechercher un document"     -> search_knowledge() (réel — cherche dans
    la base de connaissances ALFRED, PAS des documents utilisateur arbitraires,
    aucun moteur de ce type n'existe)
  - "Nouvelle tâche"              -> aucun TaskEngine n'existe encore (backlog)
  - "Ajouter un événement"        -> aucune intégration agenda externe encore
    (backlog Google Agenda)

run_backup() sauvegarde les fichiers personnels les plus critiques et
difficiles à régénérer (identité/profil, mémoire épisodique/long terme,
rappels) via src/security/backup_security.py — complémentaire, pas un
remplacement, du mirroring robocopy planifié (backup_alfred.ps1, tâche
"ALFRED - Sauvegarde quotidienne").
"""

from __future__ import annotations

_BACKUP_TARGETS = [
    "data/profile/identity_celine.json",
    "data/profile/personality_celine.json",
    "data/profile/emotional_celine.json",
    "data/memory/episodes.json",
    "data/memory/reminders.json",
    "data/memory/wellbeing_log.json",
]


def run_backup() -> dict:
    """Sauvegarde à la demande des fichiers personnels critiques."""
    from pathlib import Path
    from paths import PATHS
    from src.security.backup_security import backup_many

    root = PATHS.data.parent
    existing = [str(root / p) for p in _BACKUP_TARGETS if (root / p).exists()]
    if not existing:
        return {"ok": False, "error": "Aucun fichier à sauvegarder trouvé."}

    result = backup_many(existing, label="dashboard_manuel")
    ok = len(result.get("errors", [])) == 0
    return {
        "ok": ok,
        "backed_up": len(result.get("success", [])),
        "errors": [e["error"] for e in result.get("errors", [])],
    }


def summarize_today() -> dict:
    """Résumé lisible de la journée : épisodes, rappels, tendance énergie."""
    from datetime import datetime
    from src.memory.episodic_memory import get_timeline

    today = datetime.now().date().isoformat()
    episodes_today = [e for e in get_timeline(limit=50) if e.get("created_at", "").startswith(today)]

    reminders_today = []
    try:
        from src.main import get_live_components
        components = get_live_components()
        engine = components.get("reminder_engine") if components else None
        if engine:
            reminders_today = [r.title for r in engine.get_active() if r.due_at.startswith(today)]
    except Exception:
        pass

    energy_dominant = None
    try:
        from src.regulation.wellbeing_tracker import get_daily_energy_summary
        energy_dominant = get_daily_energy_summary().get("dominant")
    except Exception:
        pass

    lines = []
    if episodes_today:
        lines.append(f"{len(episodes_today)} échange(s) notable(s) aujourd'hui.")
        for e in episodes_today[:5]:
            lines.append(f"  • {e.get('title', '')}")
    else:
        lines.append("Aucun échange notable enregistré aujourd'hui pour l'instant.")

    if reminders_today:
        lines.append(f"{len(reminders_today)} rappel(s) du jour : " + ", ".join(reminders_today))

    if energy_dominant and energy_dominant != "unknown":
        lines.append(f"Énergie dominante aujourd'hui : {energy_dominant}.")

    return {"ok": True, "summary": "\n".join(lines), "episode_count": len(episodes_today)}


def search_knowledge(query: str) -> dict:
    """Recherche dans la base de connaissances ALFRED (pas de documents utilisateur)."""
    query = (query or "").strip()
    if not query:
        return {"ok": False, "error": "Recherche vide."}

    try:
        from src.knowledge.retrieval_engine import KnowledgeRetrievalEngine
        engine = KnowledgeRetrievalEngine()
        result = engine.retrieve(query=query, user_id="celine")
    except Exception as exc:
        return {"ok": False, "error": str(exc)}

    items = []
    for ranked in result.ranked_knowledge[:8]:
        data = ranked.data or {}
        items.append({
            "id": ranked.knowledge_id,
            "title": data.get("title") or ranked.knowledge_id,
            "summary": (data.get("summary") or "")[:200],
            "score": round(ranked.score, 2),
        })

    return {"ok": True, "query": query, "results": items}
