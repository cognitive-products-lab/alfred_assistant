"""
PROJECT      : ALFRED
BLOCK        : GLOBAL — Intégrations externes
FILE         : src/integrations/weather_client.py
ROLE         : Client HTTP météo — résolution code postal FR + prévisions courantes

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-07-19
VERSION      : V1.0
STATUS       : DRAFT

DESCRIPTION :
Premier appel réseau réellement externe du pipeline ALFRED (Ollama, seul
autre appel HTTP du code, reste local — cf. src/llm/llm_client_ollama.py).
Nécessite donc un consentement explicite avant tout appel — géré par
src/ui/weather_prefs.py, pas ici : ce module est un simple client HTTP sans
état, il ne sait rien du consentement.

Deux services publics, gratuits, sans clé API :
  - geo.api.gouv.fr (API officielle de l'État français) pour résoudre un
    code postal en coordonnées — plus fiable qu'un géocodage générique par
    nom pour ce cas d'usage précis (codes postaux français uniquement).
  - open-meteo.com pour les prévisions courantes à partir de ces coordonnées.

Utilise urllib.request (stdlib, même approche que llm_client_ollama.py) —
pas de dépendance requests, absente de requirements.txt.
"""

from __future__ import annotations

import json
import re
import urllib.error
import urllib.parse
import urllib.request

_GEO_GOUV_URL = "https://geo.api.gouv.fr/communes"
_OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"
_TIMEOUT = 5

# Codes WMO (weather_code d'Open-Meteo) -> (libellé FR, catégorie icône)
_WMO_LABELS: dict[int, tuple[str, str]] = {
    0: ("Ciel dégagé", "sun"),
    1: ("Plutôt dégagé", "sun"),
    2: ("Partiellement nuageux", "cloud-sun"),
    3: ("Couvert", "cloud"),
    45: ("Brouillard", "fog"),
    48: ("Brouillard givrant", "fog"),
    51: ("Bruine légère", "rain"),
    53: ("Bruine modérée", "rain"),
    55: ("Bruine dense", "rain"),
    56: ("Bruine verglaçante", "rain"),
    57: ("Bruine verglaçante dense", "rain"),
    61: ("Pluie légère", "rain"),
    63: ("Pluie modérée", "rain"),
    65: ("Pluie forte", "rain"),
    66: ("Pluie verglaçante", "rain"),
    67: ("Pluie verglaçante forte", "rain"),
    71: ("Neige légère", "snow"),
    73: ("Neige modérée", "snow"),
    75: ("Neige forte", "snow"),
    77: ("Neige en grains", "snow"),
    80: ("Averses légères", "rain"),
    81: ("Averses modérées", "rain"),
    82: ("Averses violentes", "rain"),
    85: ("Averses de neige légères", "snow"),
    86: ("Averses de neige fortes", "snow"),
    95: ("Orage", "storm"),
    96: ("Orage avec grêle légère", "storm"),
    99: ("Orage avec grêle forte", "storm"),
}


class WeatherError(Exception):
    """Erreur réseau ou de résolution — message déjà en français, affichable tel quel."""


def _get_json(url: str) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": "ALFRED-assistant/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=_TIMEOUT) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.URLError as exc:
        raise WeatherError(f"Connexion météo impossible : {exc.reason}") from exc
    except (json.JSONDecodeError, TimeoutError) as exc:
        raise WeatherError(f"Réponse météo invalide : {exc}") from exc


def extract_postal_code(text: str) -> str | None:
    """Extrait un code postal français (5 chiffres) d'un texte libre (ex. profil 'localite')."""
    match = re.search(r"\b\d{5}\b", text or "")
    return match.group(0) if match else None


def extract_commune_hint(text: str) -> str | None:
    """
    Extrait le nom de commune qui suit le code postal dans un texte libre
    (ex. "45300 Manchecourt, Loiret" -> "Manchecourt"). Un même code postal
    français couvre souvent plusieurs communes (testé en direct : 45300
    résout par défaut sur "Ascoux", pas "Manchecourt") — ce indice sert à
    désambiguïser plutôt que de prendre le premier résultat au hasard.
    """
    match = re.search(r"\b\d{5}\s+([A-Za-zÀ-ÿ' -]+?)(?:,|$)", text or "")
    return match.group(1).strip() if match else None


def geocode_postal_code(postal_code: str, commune_hint: str | None = None) -> dict:
    """
    Résout un code postal français en coordonnées via geo.api.gouv.fr.
    Un code postal peut couvrir plusieurs communes : si `commune_hint` est
    fourni, on cherche la commune dont le nom correspond parmi les résultats
    plutôt que de prendre le premier (arbitraire) renvoyé par l'API.

    Returns:
        {"commune": str, "postal_code": str, "lat": float, "lon": float}

    Raises:
        WeatherError si le code postal est invalide ou introuvable.
    """
    if not re.fullmatch(r"\d{5}", postal_code or ""):
        raise WeatherError(f"« {postal_code} » n'est pas un code postal français valide.")

    params = urllib.parse.urlencode({
        "codePostal": postal_code,
        "fields": "nom,centre",
        "format": "json",
        "limit": "20",
    })
    data = _get_json(f"{_GEO_GOUV_URL}?{params}")
    if not data:
        raise WeatherError(f"Aucune commune trouvée pour le code postal {postal_code}.")

    commune = data[0]
    if commune_hint:
        hint_norm = commune_hint.strip().casefold()
        match = next((c for c in data if c["nom"].casefold() == hint_norm), None)
        commune = match or commune

    lon, lat = commune["centre"]["coordinates"]
    return {
        "commune": commune["nom"],
        "postal_code": postal_code,
        "lat": lat,
        "lon": lon,
    }


def get_current_weather(lat: float, lon: float) -> dict:
    """
    Prévisions courantes via Open-Meteo pour des coordonnées données.

    Returns:
        {"temperature_c": float, "label": str, "icon": str, "weather_code": int}
    """
    params = urllib.parse.urlencode({
        "latitude": f"{lat:.4f}",
        "longitude": f"{lon:.4f}",
        "current": "temperature_2m,weather_code",
        "timezone": "auto",
    })
    data = _get_json(f"{_OPEN_METEO_URL}?{params}")
    current = data.get("current")
    if not current:
        raise WeatherError("Réponse météo incomplète.")

    code = int(current.get("weather_code", -1))
    label, icon = _WMO_LABELS.get(code, ("Conditions inconnues", "cloud"))
    return {
        "temperature_c": current.get("temperature_2m"),
        "label": label,
        "icon": icon,
        "weather_code": code,
    }


def get_weather_for_postal_code(postal_code: str, commune_hint: str | None = None) -> dict:
    """Combine géocodage + prévisions en un seul appel pratique."""
    location = geocode_postal_code(postal_code, commune_hint=commune_hint)
    weather = get_current_weather(location["lat"], location["lon"])
    return {**location, **weather}
