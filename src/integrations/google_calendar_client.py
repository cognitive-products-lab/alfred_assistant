"""
PROJECT      : ALFRED
BLOCK        : GLOBAL — Intégrations externes
FILE         : src/integrations/google_calendar_client.py
ROLE         : Client Google Calendar API — lecture et création d'événements

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-07-23
VERSION      : V1.0
STATUS       : DRAFT

DESCRIPTION :
Utilise google-api-python-client (googleapiclient.discovery.build) plutôt
qu'urllib brut (contrairement à weather_client.py) : l'API Google Calendar
nécessite des jetons OAuth avec rafraîchissement automatique, ce que la
bibliothèque officielle gère — la réimplémenter à la main ferait courir un
risque de sécurité (gestion de jetons) pour aucun bénéfice.

Ce module ne sait rien du consentement ni de l'authentification : il prend
des `Credentials` déjà valides en paramètre (voir src/integrations/
google_auth.py) et n'est appelé qu'après vérification du consentement
(src/ui/google_calendar_prefs.py) par l'appelant (src/alfred_desktop.py).

Ne mémorise aucun événement en local — chaque lecture interroge l'API en
direct (pas de cache/miroir local des événements pour l'instant, cf. Chantier
1 : reminder_engine.py reste un moteur séparé, pas fusionné avec ce module).
"""

from __future__ import annotations

_CALENDAR_ID = "primary"


class CalendarError(Exception):
    """Erreur d'appel Google Calendar — message déjà en français, affichable tel quel."""


def _build_service(creds):
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError

    try:
        return build("calendar", "v3", credentials=creds, cache_discovery=False)
    except HttpError as exc:
        raise CalendarError(f"Connexion à Google Agenda impossible : {exc}") from exc


def _normalize_event(event: dict) -> dict:
    start = event.get("start", {})
    end = event.get("end", {})
    all_day = "date" in start
    return {
        "id": event.get("id", ""),
        "summary": event.get("summary", "(Sans titre)"),
        "start": start.get("date") or start.get("dateTime", ""),
        "end": end.get("date") or end.get("dateTime", ""),
        "location": event.get("location"),
        "all_day": all_day,
    }


def list_upcoming_events(creds, max_results: int = 10) -> list[dict]:
    """
    Récupère les prochains événements à venir de l'agenda principal.

    Args:
        creds       : Credentials Google valides (src.integrations.google_auth.get_credentials())
        max_results : Nombre maximum d'événements à retourner

    Returns:
        Liste d'événements normalisés {id, summary, start, end, location, all_day},
        triés par date de début croissante.

    Raises:
        CalendarError en cas d'échec de l'appel API.
    """
    from datetime import datetime, timezone
    from googleapiclient.errors import HttpError

    service = _build_service(creds)
    now = datetime.now(timezone.utc).isoformat()

    try:
        response = (
            service.events()
            .list(
                calendarId=_CALENDAR_ID,
                timeMin=now,
                maxResults=max_results,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
    except HttpError as exc:
        raise CalendarError(f"Lecture de l'agenda impossible : {exc}") from exc

    return [_normalize_event(e) for e in response.get("items", [])]


def create_event(
    creds,
    summary: str,
    start_iso: str,
    end_iso: str,
    location: str | None = None,
    recurrence: list[str] | None = None,
) -> dict:
    """
    Crée un événement dans l'agenda principal.

    Args:
        creds      : Credentials Google valides
        summary    : Titre de l'événement
        start_iso  : Date/heure de début, ISO 8601 (ex. "2026-07-24T15:00:00")
        end_iso    : Date/heure de fin, ISO 8601
        location   : Lieu optionnel
        recurrence : Règles RRULE optionnelles (ex. ["RRULE:FREQ=DAILY"]) pour un
                     événement/rappel répété

    Returns:
        Événement créé, normalisé {id, summary, start, end, location, all_day}.

    Raises:
        CalendarError en cas d'échec de l'appel API.
    """
    from googleapiclient.errors import HttpError

    # timeZone explicite requis par l'API pour les événements récurrents (le
    # décalage UTC dans start_iso/end_iso ne suffit pas : RRULE a besoin d'un
    # nom de fuseau IANA pour gérer les transitions heure d'été/hiver au fil
    # des occurrences) — inclus systématiquement, inoffensif pour un événement
    # non récurrent.
    service = _build_service(creds)
    body = {
        "summary": summary,
        "start": {"dateTime": start_iso, "timeZone": "Europe/Paris"},
        "end": {"dateTime": end_iso, "timeZone": "Europe/Paris"},
    }
    if location:
        body["location"] = location
    if recurrence:
        body["recurrence"] = recurrence

    try:
        created = service.events().insert(calendarId=_CALENDAR_ID, body=body).execute()
    except HttpError as exc:
        raise CalendarError(f"Création de l'événement impossible : {exc}") from exc

    return _normalize_event(created)
