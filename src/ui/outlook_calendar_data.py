"""
PROJECT      : ALFRED
BLOCK        : B15 — Avatar & Interface
FILE         : src/ui/outlook_calendar_data.py
ROLE         : Orchestration Agenda Outlook (consentement, connexion OAuth,
                appels API) — second fournisseur d'agenda

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-07-24
VERSION      : V1.0
STATUS       : DRAFT

DESCRIPTION :
Point d'entrée unique appelé par AlfredDesktopAPI, même rôle et même forme
que src/ui/google_calendar_data.py. Deux portes successives avant tout appel
réseau : le consentement (src/ui/outlook_calendar_prefs.py) puis la
connexion OAuth (src/integrations/outlook_auth.py) — sans les deux, aucun
appel à Microsoft Graph n'est fait.
"""

from __future__ import annotations


def get_calendar_state(max_results: int = 10) -> dict:
    """État complet pour la vue Agenda — une seule méthode à appeler côté JS."""
    from src.ui.outlook_calendar_prefs import load_outlook_calendar_prefs

    if not load_outlook_calendar_prefs()["consent"]:
        return {"consent": False}

    from src.integrations import outlook_auth

    token = outlook_auth.get_credentials()
    if not token:
        return {"consent": True, "connected": False}

    from src.integrations.outlook_calendar_client import list_upcoming_events, OutlookCalendarError

    try:
        events = list_upcoming_events(token, max_results=max_results)
        return {"consent": True, "connected": True, "ok": True, "events": events}
    except OutlookCalendarError as exc:
        return {"consent": True, "connected": True, "ok": False, "error": str(exc)}


def set_calendar_consent(enabled: bool) -> dict:
    from src.ui.outlook_calendar_prefs import set_consent

    set_consent(enabled)
    return get_calendar_state()


def get_outlook_auth_status() -> dict:
    from src.integrations import outlook_auth

    return {"connected": outlook_auth.is_connected()}


def start_outlook_auth() -> dict:
    """Lance le flux OAuth (bloquant, ouvre le navigateur système)."""
    from src.integrations import outlook_auth

    result = outlook_auth.start_auth_flow()
    return {**result, **get_calendar_state()}


def disconnect_outlook_calendar() -> dict:
    from src.integrations import outlook_auth

    outlook_auth.disconnect()
    return get_calendar_state()


def create_calendar_event(
    summary: str,
    start_iso: str,
    end_iso: str,
    location: str | None = None,
    recurrence: dict | None = None,
) -> dict:
    """Crée un événement — appelé depuis les outils du LLM
    (src/core/tool_calling.py). recurrence : motif Graph natif (voir
    src/integrations/outlook_calendar_client.py), pas des RRULE Google."""
    from src.ui.outlook_calendar_prefs import load_outlook_calendar_prefs

    if not load_outlook_calendar_prefs()["consent"]:
        return {"consent": False}

    from src.integrations import outlook_auth

    token = outlook_auth.get_credentials()
    if not token:
        return {"consent": True, "connected": False}

    from src.integrations.outlook_calendar_client import create_event, OutlookCalendarError

    summary = (summary or "").strip()
    if not summary:
        return {"consent": True, "connected": True, "ok": False,
                "error": "Le titre de l'événement est requis."}

    try:
        event = create_event(
            token, summary, start_iso, end_iso,
            location=location or None, recurrence=recurrence or None,
        )
        return {"consent": True, "connected": True, "ok": True, "event": event}
    except OutlookCalendarError as exc:
        return {"consent": True, "connected": True, "ok": False, "error": str(exc)}


def find_calendar_events(summary_hint: str) -> dict:
    """Cherche des événements par titre approximatif — utilisé par les outils
    du LLM pour résoudre un extrait de titre en event_id réel avant
    modification/suppression."""
    from src.ui.outlook_calendar_prefs import load_outlook_calendar_prefs

    if not load_outlook_calendar_prefs()["consent"]:
        return {"consent": False}

    from src.integrations import outlook_auth

    token = outlook_auth.get_credentials()
    if not token:
        return {"consent": True, "connected": False}

    from src.integrations.outlook_calendar_client import find_event, OutlookCalendarError

    try:
        events = find_event(token, summary_hint)
        return {"consent": True, "connected": True, "ok": True, "events": events}
    except OutlookCalendarError as exc:
        return {"consent": True, "connected": True, "ok": False, "error": str(exc)}


def update_calendar_event(
    event_id: str,
    summary: str | None = None,
    start_iso: str | None = None,
    end_iso: str | None = None,
    location: str | None = None,
) -> dict:
    """Modifie un événement existant — appelé depuis les outils du LLM."""
    from src.ui.outlook_calendar_prefs import load_outlook_calendar_prefs

    if not load_outlook_calendar_prefs()["consent"]:
        return {"consent": False}

    from src.integrations import outlook_auth

    token = outlook_auth.get_credentials()
    if not token:
        return {"consent": True, "connected": False}

    from src.integrations.outlook_calendar_client import update_event, OutlookCalendarError

    try:
        event = update_event(
            token, event_id, summary=summary, start_iso=start_iso,
            end_iso=end_iso, location=location,
        )
        return {"consent": True, "connected": True, "ok": True, "event": event}
    except OutlookCalendarError as exc:
        return {"consent": True, "connected": True, "ok": False, "error": str(exc)}


def delete_calendar_event(event_id: str) -> dict:
    """Supprime un événement (ou une série récurrente) — appelé depuis les
    outils du LLM."""
    from src.ui.outlook_calendar_prefs import load_outlook_calendar_prefs

    if not load_outlook_calendar_prefs()["consent"]:
        return {"consent": False}

    from src.integrations import outlook_auth

    token = outlook_auth.get_credentials()
    if not token:
        return {"consent": True, "connected": False}

    from src.integrations.outlook_calendar_client import delete_event, OutlookCalendarError

    try:
        delete_event(token, event_id)
        return {"consent": True, "connected": True, "ok": True}
    except OutlookCalendarError as exc:
        return {"consent": True, "connected": True, "ok": False, "error": str(exc)}
