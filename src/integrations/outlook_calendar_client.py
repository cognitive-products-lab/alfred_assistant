# ============================================================
# ALFRED — src/integrations/outlook_calendar_client.py
# BLOC GLOBAL — Intégrations externes
# ROLE : Client Microsoft Graph — lecture/création/modification/suppression
#        d'événements, même rôle que google_calendar_client.py pour Google.
#
# Utilise des appels REST directs (requests) plutôt qu'un SDK officiel lourd
# (msgraph-sdk, API async par défaut) — même choix que weather_client.py pour
# une API REST simple, l'API Calendar de Microsoft Graph n'a pas besoin de
# plus. L'authentification (jeton MSAL) reste dans outlook_auth.py ; ce
# module ne prend qu'un access_token déjà valide en paramètre et ne sait
# rien du consentement (voir src/ui/outlook_calendar_prefs.py, appelé par
# src/ui/outlook_calendar_data.py).
#
# Signatures volontairement alignées sur google_calendar_client.py
# (list_upcoming_events/create_event/update_event/delete_event/find_event)
# pour que src/core/tool_calling.py puisse router entre les deux
# fournisseurs de façon quasi polymorphe.
# ============================================================

from __future__ import annotations

_GRAPH_BASE = "https://graph.microsoft.com/v1.0"
_TIMEOUT = 15


class OutlookCalendarError(Exception):
    """Erreur d'appel Microsoft Graph — message déjà en français, affichable tel quel."""


def _headers(access_token: str) -> dict:
    return {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}


def _normalize_event(event: dict) -> dict:
    start = event.get("start") or {}
    end = event.get("end") or {}
    return {
        "id": event.get("id", ""),
        "summary": event.get("subject") or "(Sans titre)",
        "start": start.get("dateTime", ""),
        "end": end.get("dateTime", ""),
        "location": (event.get("location") or {}).get("displayName") or None,
        "all_day": bool(event.get("isAllDay", False)),
        "recurring_event_id": event.get("seriesMasterId"),
    }


def list_upcoming_events(access_token: str, max_results: int = 10) -> list[dict]:
    """
    Récupère les prochains événements à venir (30 jours) de l'agenda
    principal. Utilise /me/calendarview plutôt que /me/events : Graph
    expanse alors automatiquement les événements récurrents en occurrences
    individuelles (équivalent du singleEvents=True de l'API Google).
    """
    import requests
    from datetime import datetime, timedelta, timezone

    now = datetime.now(timezone.utc)
    params = {
        "startDateTime": now.isoformat(),
        "endDateTime": (now + timedelta(days=30)).isoformat(),
        "$orderby": "start/dateTime",
        "$top": max_results,
    }
    try:
        resp = requests.get(
            f"{_GRAPH_BASE}/me/calendarview",
            headers=_headers(access_token), params=params, timeout=_TIMEOUT,
        )
        resp.raise_for_status()
    except requests.RequestException as exc:
        raise OutlookCalendarError(f"Lecture de l'agenda Outlook impossible : {exc}") from exc

    items = resp.json().get("value", [])
    return [_normalize_event(e) for e in items[:max_results]]


def create_event(
    access_token: str,
    summary: str,
    start_iso: str,
    end_iso: str,
    location: str | None = None,
    recurrence: dict | None = None,
) -> dict:
    """
    Crée un événement dans l'agenda principal.

    Args:
        access_token : Access token Microsoft Graph valide
        summary      : Titre de l'événement
        start_iso    : Date/heure de début, ISO 8601 sans décalage (ex. "2026-07-24T15:00:00")
        end_iso      : Date/heure de fin, ISO 8601 sans décalage
        location     : Lieu optionnel
        recurrence   : Motif de récurrence Graph natif optionnel, ex.
                       {"pattern": {"type": "daily", "interval": 1},
                        "range": {"type": "noEnd", "startDate": "2026-07-24"}}

    Raises:
        OutlookCalendarError en cas d'échec de l'appel API.
    """
    import requests

    body: dict = {
        "subject": summary,
        "start": {"dateTime": start_iso, "timeZone": "Europe/Paris"},
        "end": {"dateTime": end_iso, "timeZone": "Europe/Paris"},
    }
    if location:
        body["location"] = {"displayName": location}
    if recurrence:
        body["recurrence"] = recurrence

    try:
        resp = requests.post(
            f"{_GRAPH_BASE}/me/events", headers=_headers(access_token), json=body, timeout=_TIMEOUT,
        )
        resp.raise_for_status()
    except requests.RequestException as exc:
        raise OutlookCalendarError(f"Création de l'événement Outlook impossible : {exc}") from exc

    return _normalize_event(resp.json())


def update_event(
    access_token: str,
    event_id: str,
    summary: str | None = None,
    start_iso: str | None = None,
    end_iso: str | None = None,
    location: str | None = None,
) -> dict:
    """Modifie un événement existant (patch partiel). Raises OutlookCalendarError."""
    import requests

    body: dict = {}
    if summary is not None:
        body["subject"] = summary
    if start_iso is not None:
        body["start"] = {"dateTime": start_iso, "timeZone": "Europe/Paris"}
    if end_iso is not None:
        body["end"] = {"dateTime": end_iso, "timeZone": "Europe/Paris"}
    if location is not None:
        body["location"] = {"displayName": location}

    try:
        resp = requests.patch(
            f"{_GRAPH_BASE}/me/events/{event_id}",
            headers=_headers(access_token), json=body, timeout=_TIMEOUT,
        )
        resp.raise_for_status()
    except requests.RequestException as exc:
        raise OutlookCalendarError(f"Modification de l'événement Outlook impossible : {exc}") from exc

    return _normalize_event(resp.json())


def delete_event(access_token: str, event_id: str) -> None:
    """Supprime un événement (ou toute une série récurrente si event_id est
    l'identifiant de l'événement maître — voir find_event). Raises OutlookCalendarError."""
    import requests

    try:
        resp = requests.delete(
            f"{_GRAPH_BASE}/me/events/{event_id}", headers=_headers(access_token), timeout=_TIMEOUT,
        )
        resp.raise_for_status()
    except requests.RequestException as exc:
        raise OutlookCalendarError(f"Suppression de l'événement Outlook impossible : {exc}") from exc


def find_event(access_token: str, summary_hint: str, max_candidates: int = 25) -> list[dict]:
    """
    Cherche, parmi les événements des dernières 24h + prochains 30 jours,
    ceux dont le titre contient summary_hint (insensible à la casse) — même
    principe que google_calendar_client.find_event(). Retourne l'identifiant
    de la SÉRIE (seriesMasterId) pour un événement récurrent, dédoublonné.
    """
    import requests
    from datetime import datetime, timedelta, timezone

    hint = summary_hint.strip().lower()
    if not hint:
        return []

    now = datetime.now(timezone.utc)
    params = {
        "startDateTime": (now - timedelta(hours=24)).isoformat(),
        "endDateTime": (now + timedelta(days=30)).isoformat(),
        "$orderby": "start/dateTime",
        "$top": max_candidates,
    }
    try:
        resp = requests.get(
            f"{_GRAPH_BASE}/me/calendarview",
            headers=_headers(access_token), params=params, timeout=_TIMEOUT,
        )
        resp.raise_for_status()
    except requests.RequestException as exc:
        raise OutlookCalendarError(f"Recherche de l'événement Outlook impossible : {exc}") from exc

    events = [_normalize_event(e) for e in resp.json().get("value", [])]

    seen_series: set[str] = set()
    matches: list[dict] = []
    for event in events:
        if hint not in event["summary"].lower():
            continue
        series_id = event.get("recurring_event_id") or event["id"]
        if series_id in seen_series:
            continue
        seen_series.add(series_id)
        matches.append({**event, "id": series_id})

    return matches
