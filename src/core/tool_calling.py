# ============================================================
# ALFRED — src/core/tool_calling.py
# Bloc 01.05b — Function-calling : actions réelles depuis la conversation
#
# 🎯 UTILITÉ ALFRED :
#   Avant ce module, une demande comme « ajoute un rappel à mon agenda »
#   n'avait aucun moyen d'aboutir à une action réelle : le LLM se contentait
#   d'inventer une réponse plausible (voir incident du 23/07/2026 où il a
#   halluciné une UI appartenant à ALFRED CPL, un autre produit). Ce module
#   définit les outils réels que le LLM peut appeler, et exécute ces appels
#   en s'appuyant sur les fonctions déjà vérifiées en conditions réelles
#   (src/ui/google_calendar_data.py — mêmes portes consentement + connexion
#   OAuth que le formulaire manuel "Ajouter un événement").
#
#   Les petits modèles locaux (ex. llama3.2 via Ollama) construisent de façon
#   peu fiable des datetimes ISO 8601 complets avec fuseau. Le schéma des
#   outils leur demande donc une date, une heure et une durée séparées — la
#   conversion en ISO 8601 (Europe/Paris) est faite ici, pas par le modèle.
#
# STATUS  : DRAFT
# ============================================================

from __future__ import annotations

import logging
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

logger = logging.getLogger(__name__)

_FRANCE_TZ = ZoneInfo("Europe/Paris")

_RECURRENCE_RULES: dict[str, list[str] | None] = {
    "none": None,
    "daily": ["RRULE:FREQ=DAILY"],
    "weekly": ["RRULE:FREQ=WEEKLY"],
}

_OUTLOOK_RECURRENCE_TYPES: dict[str, str] = {
    "daily": "daily",
    "weekly": "weekly",
}


def _build_outlook_recurrence(keyword: str, start_dt: datetime) -> dict | None:
    """Motif de récurrence au format natif Microsoft Graph — structurellement
    différent des RRULE Google (voir _RECURRENCE_RULES), donc construit
    séparément plutôt que traduit."""
    graph_type = _OUTLOOK_RECURRENCE_TYPES.get(keyword)
    if not graph_type:
        return None
    return {
        "pattern": {"type": graph_type, "interval": 1},
        "range": {"type": "noEnd", "startDate": start_dt.strftime("%Y-%m-%d")},
    }

# ---------------------------------------------------------------------------
# Schéma des outils — format proche d'OpenAI/Ollama (function calling),
# converti pour Anthropic dans _anthropic_tools().
# ---------------------------------------------------------------------------
TOOL_SPECS: list[dict] = [
    {
        "name": "create_calendar_event",
        "description": (
            "Crée un événement ou un rappel réel dans l'agenda (Google par "
            "défaut, ou Outlook si l'utilisateur le nomme explicitement). À "
            "utiliser dès que l'utilisateur demande d'ajouter un rendez-vous, "
            "un événement ou un rappel à son agenda — ne jamais inventer "
            "d'instructions d'interface à la place, toujours appeler cet outil."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "summary": {
                    "type": "string",
                    "description": "Titre court de l'événement ou du rappel.",
                },
                "date": {
                    "type": "string",
                    "description": (
                        "Date au format YYYY-MM-DD. Si l'utilisateur ne précise "
                        "pas de date (ex. juste une heure), utilise la date du "
                        "jour indiquée dans le contexte."
                    ),
                },
                "time": {
                    "type": "string",
                    "description": "Heure de début au format HH:MM (24h).",
                },
                "duration_minutes": {
                    "type": "integer",
                    "description": "Durée en minutes. 15 par défaut si absent.",
                },
                "recurrence": {
                    "type": "string",
                    "enum": ["none", "daily", "weekly"],
                    "description": (
                        "Répétition : none (par défaut), daily (tous les jours), "
                        "weekly (toutes les semaines)."
                    ),
                },
                "location": {
                    "type": "string",
                    "description": "Lieu optionnel.",
                },
                "provider": {
                    "type": "string",
                    "enum": ["google", "outlook"],
                    "description": (
                        "Laisser vide sauf si l'utilisateur nomme explicitement "
                        "\"Google\" ou \"Outlook\" — sinon l'agenda par défaut "
                        "configuré dans Paramètres est utilisé."
                    ),
                },
            },
            "required": ["summary", "time"],
        },
    },
    {
        "name": "list_calendar_events",
        "description": "Liste les prochains événements réels de l'agenda (Google par défaut, ou Outlook si nommé).",
        "parameters": {
            "type": "object",
            "properties": {
                "max_results": {
                    "type": "integer",
                    "description": "Nombre maximum d'événements à retourner (10 par défaut).",
                },
                "provider": {
                    "type": "string",
                    "enum": ["google", "outlook"],
                    "description": "Laisser vide sauf si l'utilisateur nomme explicitement l'agenda à consulter.",
                },
            },
            "required": [],
        },
    },
    {
        "name": "update_calendar_event",
        "description": (
            "Modifie un événement existant dans l'agenda (déplace l'heure/la "
            "date, change le titre, la durée ou le lieu). Identifie l'événement à "
            "partir d'un extrait de son titre actuel — pas besoin d'un identifiant "
            "technique."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "summary_hint": {
                    "type": "string",
                    "description": "Extrait du titre actuel de l'événement à modifier (ex. 'dentiste').",
                },
                "new_summary": {"type": "string", "description": "Nouveau titre, si à changer."},
                "new_date": {"type": "string", "description": "Nouvelle date YYYY-MM-DD, si à changer."},
                "new_time": {"type": "string", "description": "Nouvelle heure HH:MM, si à changer."},
                "new_duration_minutes": {"type": "integer", "description": "Nouvelle durée en minutes, si à changer."},
                "new_location": {"type": "string", "description": "Nouveau lieu, si à changer."},
                "provider": {
                    "type": "string",
                    "enum": ["google", "outlook"],
                    "description": "Laisser vide sauf si l'utilisateur nomme explicitement l'agenda concerné.",
                },
            },
            "required": ["summary_hint"],
        },
    },
    {
        "name": "delete_calendar_event",
        "description": (
            "Supprime un événement (ou toute une série récurrente) de l'agenda. "
            "Identifie l'événement à partir d'un extrait de son titre."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "summary_hint": {
                    "type": "string",
                    "description": "Extrait du titre de l'événement à supprimer (ex. 'manger').",
                },
                "provider": {
                    "type": "string",
                    "enum": ["google", "outlook"],
                    "description": "Laisser vide sauf si l'utilisateur nomme explicitement l'agenda concerné.",
                },
            },
            "required": ["summary_hint"],
        },
    },
    {
        "name": "create_task",
        "description": (
            "Crée une tâche réelle dans la liste de tâches d'ALFRED. Une tâche "
            "peut ne pas avoir d'échéance (ex. 'ranger le bureau') ou en avoir "
            "une (ex. 'appeler le dentiste demain'). Utilise cet outil dès que "
            "l'utilisateur demande d'ajouter/noter/créer une tâche."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "title": {"type": "string", "description": "Titre court de la tâche."},
                "due_date": {
                    "type": "string",
                    "description": "Date d'échéance YYYY-MM-DD, si l'utilisateur en donne une. Laisser vide si aucune échéance.",
                },
                "due_time": {
                    "type": "string",
                    "description": "Heure d'échéance HH:MM, si l'utilisateur en donne une.",
                },
                "reminder": {
                    "type": "boolean",
                    "description": "True si l'utilisateur veut être rappelé à l'échéance, sinon False (simple pense-bête).",
                },
                "notes": {"type": "string", "description": "Détails optionnels sur la tâche."},
            },
            "required": ["title"],
        },
    },
    {
        "name": "list_tasks",
        "description": "Liste les tâches réelles de l'utilisateur (en cours par défaut).",
        "parameters": {
            "type": "object",
            "properties": {
                "include_done": {
                    "type": "boolean",
                    "description": "True pour inclure aussi les tâches déjà terminées (False par défaut).",
                },
            },
            "required": [],
        },
    },
    {
        "name": "complete_task",
        "description": (
            "Marque une tâche comme terminée. Identifie la tâche à partir d'un "
            "extrait de son titre."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "title_hint": {
                    "type": "string",
                    "description": "Extrait du titre de la tâche terminée (ex. 'vermifuger').",
                },
            },
            "required": ["title_hint"],
        },
    },
    {
        "name": "delete_task",
        "description": "Supprime une tâche. Identifie la tâche à partir d'un extrait de son titre.",
        "parameters": {
            "type": "object",
            "properties": {
                "title_hint": {
                    "type": "string",
                    "description": "Extrait du titre de la tâche à supprimer.",
                },
            },
            "required": ["title_hint"],
        },
    },
]


def openai_style_tools() -> list[dict]:
    """Format attendu par l'API OpenAI et par Ollama /api/chat."""
    return [{"type": "function", "function": spec} for spec in TOOL_SPECS]


def anthropic_style_tools() -> list[dict]:
    """Format attendu par l'API Anthropic (input_schema plutôt que parameters)."""
    return [
        {
            "name": spec["name"],
            "description": spec["description"],
            "input_schema": spec["parameters"],
        }
        for spec in TOOL_SPECS
    ]


_RELATIVE_DATE_OFFSETS: dict[str, int] = {
    "today": 0, "aujourd'hui": 0, "aujourdhui": 0,
    "tomorrow": 1, "demain": 1,
    "after tomorrow": 2, "apres-demain": 2, "après-demain": 2, "apres demain": 2, "après demain": 2,
}


def _parse_date(raw: str | None) -> datetime:
    """Résout la date fournie par le modèle — retombe sur aujourd'hui si absente/invalide.
    Le petit modèle local (llama3.2) répond parfois par un mot relatif (FR ou
    EN, ex. "demain"/"tomorrow") plutôt que par la date YYYY-MM-DD demandée
    dans le schéma de l'outil — reconnu explicitement plutôt que de tomber
    silencieusement sur aujourd'hui (bug réel observé : événement créé le
    mauvais jour sans erreur visible)."""
    now = datetime.now(_FRANCE_TZ)
    if not raw or not raw.strip():
        return now

    key = raw.strip().lower()
    if key in _RELATIVE_DATE_OFFSETS:
        return now + timedelta(days=_RELATIVE_DATE_OFFSETS[key])

    for fmt in ("%Y-%m-%d", "%d/%m/%Y"):
        try:
            parsed = datetime.strptime(raw.strip(), fmt)
            return parsed.replace(tzinfo=_FRANCE_TZ)
        except ValueError:
            continue
    logger.warning("tool_calling: date illisible (%r), repli sur aujourd'hui", raw)
    return now


def _parse_time(raw: str | None) -> tuple[int, int]:
    """Résout l'heure HH:MM fournie par le modèle — retombe sur l'heure courante si invalide."""
    if raw:
        for sep in (":", "h"):
            if sep in raw:
                hh, _, mm = raw.strip().partition(sep)
                try:
                    hour = int(hh)
                    minute = int(mm) if mm.strip() else 0
                    if 0 <= hour <= 23 and 0 <= minute <= 59:
                        return hour, minute
                except ValueError:
                    pass
    now = datetime.now(_FRANCE_TZ)
    logger.warning("tool_calling: heure illisible (%r), repli sur l'heure courante", raw)
    return now.hour, now.minute


def _build_iso_range(arguments: dict) -> tuple[str, str]:
    base_date = _parse_date(arguments.get("date"))
    hour, minute = _parse_time(arguments.get("time"))
    start = base_date.replace(hour=hour, minute=minute, second=0, microsecond=0)

    try:
        duration = int(arguments.get("duration_minutes") or 15)
    except (TypeError, ValueError):
        duration = 15
    if duration <= 0:
        duration = 15

    end = start + timedelta(minutes=duration)
    return start.isoformat(), end.isoformat()


def _existing_event_datetimes(event: dict) -> tuple[datetime, datetime]:
    """Parse les dates ISO d'un événement déjà existant (pour en déduire sa
    durée actuelle lors d'une modification partielle — ex. déplacer juste
    l'heure sans changer la longueur du rendez-vous)."""
    return datetime.fromisoformat(event["start"]), datetime.fromisoformat(event["end"])


def _calendar_module(provider: str):
    """Module data-layer du fournisseur d'agenda résolu — google_calendar_data.py
    et outlook_calendar_data.py exposent des fonctions au nom et à la
    signature identiques exprès, pour permettre ce dispatch polymorphe."""
    if provider == "outlook":
        import src.ui.outlook_calendar_data as mod
    else:
        import src.ui.google_calendar_data as mod
    return mod


def _resolve_calendar_provider(arguments: dict) -> str:
    """Fournisseur explicitement nommé par l'utilisateur ("provider" dans les
    arguments de l'outil), sinon le fournisseur par défaut configuré dans
    Paramètres (Google par défaut — décision de Céline le 24/07/2026, voir
    src/ui/calendar_provider_prefs.py)."""
    requested = (arguments.get("provider") or "").strip().lower()
    if requested in ("google", "outlook"):
        return requested
    from src.ui.calendar_provider_prefs import load_default_calendar_provider
    return load_default_calendar_provider()


def _resolve_single_event(summary_hint: str, provider: str) -> tuple[dict | None, dict | None]:
    """Résout un extrait de titre vers un événement unique via find_calendar_events.
    Retourne (event, None) en cas de succès, ou (None, erreur_française) sinon
    (aucun résultat, plusieurs résultats ambigus, ou porte consentement/connexion
    fermée)."""
    hint = (summary_hint or "").strip()
    if not hint:
        return None, {"ok": False, "error": "Un extrait du titre de l'événement est requis."}

    found = _calendar_module(provider).find_calendar_events(hint)
    gate_error = _consent_gated_error(found, provider)
    if gate_error:
        return None, gate_error
    if not found.get("ok", False):
        return None, {"ok": False, "error": found.get("error", "Erreur inconnue.")}

    candidates = found.get("events") or []
    if not candidates:
        return None, {"ok": False, "error": f"Aucun événement trouvé avec « {hint} » dans le titre."}
    if len(candidates) > 1:
        listing = "; ".join(f"{c['summary']} ({c['start']})" for c in candidates[:5])
        return None, {
            "ok": False,
            "error": f"Plusieurs événements correspondent à « {hint} » : {listing}. Demande à l'utilisateur de préciser lequel.",
        }
    return candidates[0], None


def _resolve_single_task(title_hint: str) -> tuple[dict | None, dict | None]:
    """Résout un extrait de titre vers une tâche unique via find_tasks — même
    principe que _resolve_single_event côté agenda."""
    from src.ui.tasks_data import find_tasks

    hint = (title_hint or "").strip()
    if not hint:
        return None, {"ok": False, "error": "Un extrait du titre de la tâche est requis."}

    found = find_tasks(hint)
    if not found.get("ok", False):
        return None, {"ok": False, "error": found.get("error", "Erreur inconnue.")}

    candidates = found.get("tasks") or []
    if not candidates:
        return None, {"ok": False, "error": f"Aucune tâche trouvée avec « {hint} » dans le titre."}
    if len(candidates) > 1:
        listing = "; ".join(c["title"] for c in candidates[:5])
        return None, {
            "ok": False,
            "error": f"Plusieurs tâches correspondent à « {hint} » : {listing}. Demande à l'utilisateur de préciser laquelle.",
        }
    return candidates[0], None


def _consent_gated_error(result: dict, provider: str = "google") -> dict | None:
    """Traduit les portes consentement/connexion de google_calendar_data.py /
    outlook_calendar_data.py en erreur française exploitable par le LLM.
    Retourne None si les deux portes sont ouvertes (rien à bloquer)."""
    label = "Agenda Outlook" if provider == "outlook" else "Google Agenda"
    if not result.get("consent", False):
        return {
            "ok": False,
            "error": (
                f"Le consentement {label} n'est pas activé. Dis à "
                f"l'utilisateur d'aller dans Paramètres > Agenda pour l'activer."
            ),
        }
    if not result.get("connected", False):
        return {
            "ok": False,
            "error": (
                f"{label} n'est pas connecté. Dis à l'utilisateur d'aller "
                f"dans Paramètres > Agenda > Se connecter."
            ),
        }
    return None


def execute_tool(name: str, arguments: dict) -> dict:
    """Exécute un outil réel et retourne un résultat JSON-sérialisable,
    toujours en français, jamais d'exception non gérée (le LLM doit toujours
    recevoir une réponse — succès ou erreur explicite)."""
    try:
        if name == "create_calendar_event":
            provider = _resolve_calendar_provider(arguments)
            mod = _calendar_module(provider)

            start_iso, end_iso = _build_iso_range(arguments)
            recurrence_keyword = (arguments.get("recurrence") or "none").strip().lower()
            if provider == "outlook":
                recurrence = _build_outlook_recurrence(recurrence_keyword, datetime.fromisoformat(start_iso))
            else:
                recurrence = _RECURRENCE_RULES.get(recurrence_keyword)
            summary = (arguments.get("summary") or "Rappel").strip()

            result = mod.create_calendar_event(
                summary=summary,
                start_iso=start_iso,
                end_iso=end_iso,
                location=arguments.get("location") or None,
                recurrence=recurrence,
            )
            gate_error = _consent_gated_error(result, provider)
            if gate_error:
                return gate_error
            if not result.get("ok", False):
                return {"ok": False, "error": result.get("error", "Erreur inconnue.")}
            return {"ok": True, "event": result.get("event")}

        if name == "list_calendar_events":
            provider = _resolve_calendar_provider(arguments)
            mod = _calendar_module(provider)

            try:
                max_results = int(arguments.get("max_results") or 10)
            except (TypeError, ValueError):
                max_results = 10

            result = mod.get_calendar_state(max_results=max_results)
            gate_error = _consent_gated_error(result, provider)
            if gate_error:
                return gate_error
            if not result.get("ok", False):
                return {"ok": False, "error": result.get("error", "Erreur inconnue.")}
            return {"ok": True, "events": result.get("events")}

        if name == "update_calendar_event":
            provider = _resolve_calendar_provider(arguments)
            mod = _calendar_module(provider)

            event, error = _resolve_single_event(arguments.get("summary_hint", ""), provider)
            if error:
                return error

            try:
                current_start, current_end = _existing_event_datetimes(event)
                current_duration = current_end - current_start
            except (KeyError, ValueError):
                current_start = datetime.now(_FRANCE_TZ)
                current_duration = timedelta(minutes=15)

            new_date_raw = arguments.get("new_date")
            new_time_raw = arguments.get("new_time")
            start_iso = end_iso = None
            if new_date_raw or new_time_raw:
                base_date = _parse_date(new_date_raw) if new_date_raw else current_start
                if new_time_raw:
                    hour, minute = _parse_time(new_time_raw)
                else:
                    hour, minute = current_start.hour, current_start.minute
                new_start = base_date.replace(hour=hour, minute=minute, second=0, microsecond=0)

                try:
                    explicit_duration = int(arguments.get("new_duration_minutes") or 0) or None
                except (TypeError, ValueError):
                    explicit_duration = None
                duration = timedelta(minutes=explicit_duration) if explicit_duration else current_duration
                new_end = new_start + duration
                start_iso, end_iso = new_start.isoformat(), new_end.isoformat()

            result = mod.update_calendar_event(
                event_id=event["id"],
                summary=arguments.get("new_summary") or None,
                start_iso=start_iso,
                end_iso=end_iso,
                location=arguments.get("new_location") or None,
            )
            gate_error = _consent_gated_error(result, provider)
            if gate_error:
                return gate_error
            if not result.get("ok", False):
                return {"ok": False, "error": result.get("error", "Erreur inconnue.")}
            return {"ok": True, "event": result.get("event")}

        if name == "delete_calendar_event":
            provider = _resolve_calendar_provider(arguments)
            mod = _calendar_module(provider)

            event, error = _resolve_single_event(arguments.get("summary_hint", ""), provider)
            if error:
                return error

            result = mod.delete_calendar_event(event_id=event["id"])
            gate_error = _consent_gated_error(result, provider)
            if gate_error:
                return gate_error
            if not result.get("ok", False):
                return {"ok": False, "error": result.get("error", "Erreur inconnue.")}
            return {"ok": True, "deleted_summary": event["summary"]}

        if name == "create_task":
            from src.ui.tasks_data import create_task

            title = (arguments.get("title") or "").strip()
            due_date_raw = arguments.get("due_date")
            due_time_raw = arguments.get("due_time")

            due_at = None
            if due_date_raw or due_time_raw:
                base_date = _parse_date(due_date_raw) if due_date_raw else datetime.now(_FRANCE_TZ)
                if due_time_raw:
                    hour, minute = _parse_time(due_time_raw)
                    base_date = base_date.replace(hour=hour, minute=minute, second=0, microsecond=0)
                due_at = base_date.isoformat()

            result = create_task(
                title=title,
                due_at=due_at,
                reminder=bool(arguments.get("reminder", False)),
                notes=arguments.get("notes") or None,
            )
            if not result.get("ok", False):
                return {"ok": False, "error": result.get("error", "Erreur inconnue.")}
            return {"ok": True, "task": result.get("task")}

        if name == "list_tasks":
            from src.ui.tasks_data import get_tasks_state

            result = get_tasks_state(include_done=bool(arguments.get("include_done", False)))
            if not result.get("ok", False):
                return {"ok": False, "error": result.get("error", "Erreur inconnue.")}
            return {"ok": True, "tasks": result.get("tasks")}

        if name == "complete_task":
            from src.ui.tasks_data import complete_task

            task, error = _resolve_single_task(arguments.get("title_hint", ""))
            if error:
                return error

            result = complete_task(task_id=task["id"])
            if not result.get("ok", False):
                return {"ok": False, "error": result.get("error", "Erreur inconnue.")}
            return {"ok": True, "task": result.get("task")}

        if name == "delete_task":
            from src.ui.tasks_data import delete_task

            task, error = _resolve_single_task(arguments.get("title_hint", ""))
            if error:
                return error

            result = delete_task(task_id=task["id"])
            if not result.get("ok", False):
                return {"ok": False, "error": result.get("error", "Erreur inconnue.")}
            return {"ok": True, "deleted_title": task["title"]}

        return {"ok": False, "error": f"Outil inconnu : {name}"}
    except Exception as exc:
        logger.error("tool_calling: échec exécution outil %s : %s", name, exc)
        return {"ok": False, "error": f"Erreur lors de l'exécution de l'outil : {exc}"}
