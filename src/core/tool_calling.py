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

# ---------------------------------------------------------------------------
# Schéma des outils — format proche d'OpenAI/Ollama (function calling),
# converti pour Anthropic dans _anthropic_tools().
# ---------------------------------------------------------------------------
TOOL_SPECS: list[dict] = [
    {
        "name": "create_calendar_event",
        "description": (
            "Crée un événement ou un rappel réel dans Google Agenda. À utiliser "
            "dès que l'utilisateur demande d'ajouter un rendez-vous, un événement "
            "ou un rappel à son agenda — ne jamais inventer d'instructions "
            "d'interface à la place, toujours appeler cet outil."
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
            },
            "required": ["summary", "time"],
        },
    },
    {
        "name": "list_calendar_events",
        "description": "Liste les prochains événements réels de Google Agenda.",
        "parameters": {
            "type": "object",
            "properties": {
                "max_results": {
                    "type": "integer",
                    "description": "Nombre maximum d'événements à retourner (10 par défaut).",
                },
            },
            "required": [],
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


def _parse_date(raw: str | None) -> datetime:
    """Résout la date fournie par le modèle — retombe sur aujourd'hui si absente/invalide."""
    now = datetime.now(_FRANCE_TZ)
    if not raw or not raw.strip() or raw.strip().lower() in ("today", "aujourd'hui", "aujourdhui"):
        return now
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


def _consent_gated_error(result: dict) -> dict | None:
    """Traduit les portes consentement/connexion de google_calendar_data.py
    en erreur française exploitable par le LLM. Retourne None si les deux
    portes sont ouvertes (rien à bloquer)."""
    if not result.get("consent", False):
        return {
            "ok": False,
            "error": (
                "Le consentement Google Agenda n'est pas activé. Dis à "
                "l'utilisateur d'aller dans Paramètres > Agenda pour l'activer."
            ),
        }
    if not result.get("connected", False):
        return {
            "ok": False,
            "error": (
                "Google Agenda n'est pas connecté. Dis à l'utilisateur d'aller "
                "dans Paramètres > Agenda > Se connecter à Google."
            ),
        }
    return None


def execute_tool(name: str, arguments: dict) -> dict:
    """Exécute un outil réel et retourne un résultat JSON-sérialisable,
    toujours en français, jamais d'exception non gérée (le LLM doit toujours
    recevoir une réponse — succès ou erreur explicite)."""
    try:
        if name == "create_calendar_event":
            from src.ui.google_calendar_data import create_calendar_event

            start_iso, end_iso = _build_iso_range(arguments)
            recurrence = _RECURRENCE_RULES.get(
                (arguments.get("recurrence") or "none").strip().lower()
            )
            summary = (arguments.get("summary") or "Rappel").strip()

            result = create_calendar_event(
                summary=summary,
                start_iso=start_iso,
                end_iso=end_iso,
                location=arguments.get("location") or None,
                recurrence=recurrence,
            )
            gate_error = _consent_gated_error(result)
            if gate_error:
                return gate_error
            if not result.get("ok", False):
                return {"ok": False, "error": result.get("error", "Erreur inconnue.")}
            return {"ok": True, "event": result.get("event")}

        if name == "list_calendar_events":
            from src.ui.google_calendar_data import get_calendar_state

            try:
                max_results = int(arguments.get("max_results") or 10)
            except (TypeError, ValueError):
                max_results = 10

            result = get_calendar_state(max_results=max_results)
            gate_error = _consent_gated_error(result)
            if gate_error:
                return gate_error
            if not result.get("ok", False):
                return {"ok": False, "error": result.get("error", "Erreur inconnue.")}
            return {"ok": True, "events": result.get("events")}

        return {"ok": False, "error": f"Outil inconnu : {name}"}
    except Exception as exc:
        logger.error("tool_calling: échec exécution outil %s : %s", name, exc)
        return {"ok": False, "error": f"Erreur lors de l'exécution de l'outil : {exc}"}
