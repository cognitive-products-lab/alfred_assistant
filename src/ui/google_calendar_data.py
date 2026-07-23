"""
PROJECT      : ALFRED
BLOCK        : B15 — Avatar & Interface
FILE         : src/ui/google_calendar_data.py
ROLE         : Orchestration Google Agenda pour la vue Agenda + le raccourci
                "Ajouter un événement" (consentement, connexion OAuth, appels API)

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-07-23
VERSION      : V1.0
STATUS       : DRAFT

DESCRIPTION :
Point d'entrée unique appelé par AlfredDesktopAPI, même rôle que
src/ui/weather_data.py pour la météo. Deux portes successives avant tout
appel réseau : le consentement (src/ui/google_calendar_prefs.py) puis la
connexion OAuth (src/integrations/google_auth.py) — sans les deux, aucun
appel à l'API Google Calendar n'est fait.
"""

from __future__ import annotations


def get_calendar_state(max_results: int = 10) -> dict:
    """État complet pour la vue Agenda — une seule méthode à appeler côté JS."""
    from src.ui.google_calendar_prefs import load_google_calendar_prefs

    if not load_google_calendar_prefs()["consent"]:
        return {"consent": False}

    from src.integrations import google_auth

    creds = google_auth.get_credentials()
    if not creds:
        return {"consent": True, "connected": False}

    from src.integrations.google_calendar_client import list_upcoming_events, CalendarError

    try:
        events = list_upcoming_events(creds, max_results=max_results)
        return {"consent": True, "connected": True, "ok": True, "events": events}
    except CalendarError as exc:
        return {"consent": True, "connected": True, "ok": False, "error": str(exc)}


def set_calendar_consent(enabled: bool) -> dict:
    from src.ui.google_calendar_prefs import set_consent

    set_consent(enabled)
    return get_calendar_state()


def get_google_auth_status() -> dict:
    from src.integrations import google_auth

    return {"connected": google_auth.is_connected()}


def start_google_auth() -> dict:
    """Lance le flux OAuth (bloquant, ouvre le navigateur système)."""
    from src.integrations import google_auth

    result = google_auth.start_auth_flow()
    return {**result, **get_calendar_state()}


def disconnect_google_calendar() -> dict:
    from src.integrations import google_auth

    google_auth.disconnect()
    return get_calendar_state()


def create_calendar_event(
    summary: str,
    start_iso: str,
    end_iso: str,
    location: str | None = None,
    recurrence: list[str] | None = None,
) -> dict:
    """Crée un événement — appelé depuis le raccourci "Ajouter un événement"
    et depuis les outils du LLM (src/core/tool_calling.py)."""
    from src.ui.google_calendar_prefs import load_google_calendar_prefs

    if not load_google_calendar_prefs()["consent"]:
        return {"consent": False}

    from src.integrations import google_auth

    creds = google_auth.get_credentials()
    if not creds:
        return {"consent": True, "connected": False}

    from src.integrations.google_calendar_client import create_event, CalendarError

    summary = (summary or "").strip()
    if not summary:
        return {"consent": True, "connected": True, "ok": False,
                "error": "Le titre de l'événement est requis."}

    try:
        event = create_event(
            creds, summary, start_iso, end_iso,
            location=location or None, recurrence=recurrence or None,
        )
        return {"consent": True, "connected": True, "ok": True, "event": event}
    except CalendarError as exc:
        return {"consent": True, "connected": True, "ok": False, "error": str(exc)}
