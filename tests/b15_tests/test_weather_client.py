"""
PROJECT      : ALFRED
BLOCK        : B15
FUNCTION     : 15.08
FILE         : tests/b15_tests/test_weather_client.py
ROLE         : Tests unitaires src/integrations/weather_client.py

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-07-19
VERSION      : V1.0
STATUS       : TESTED

DESCRIPTION :
Aucun test ne touche le réseau réel — _get_json (seul point d'entrée HTTP du
module) est monkeypatché partout. Couvre l'extraction code postal/commune,
la désambiguïsation par indice de commune (cas réel rencontré en session :
45300 résout par défaut sur "Ascoux", pas la commune attendue), le mapping
des codes météo WMO, et la propagation des erreurs réseau en WeatherError.
"""

import urllib.error

import pytest

from src.integrations import weather_client as wc


# =============================================================================
# extract_postal_code / extract_commune_hint
# =============================================================================

def test_extract_postal_code_finds_five_digits():
    assert wc.extract_postal_code("45300 Manchecourt, Loiret") == "45300"


def test_extract_postal_code_returns_none_when_absent():
    assert wc.extract_postal_code("pas de code postal ici") is None


def test_extract_postal_code_handles_empty_string():
    assert wc.extract_postal_code("") is None
    assert wc.extract_postal_code(None) is None


def test_extract_commune_hint_captures_name_before_comma():
    assert wc.extract_commune_hint("45300 Manchecourt, Loiret") == "Manchecourt"


def test_extract_commune_hint_handles_no_trailing_comma():
    assert wc.extract_commune_hint("75001 Paris") == "Paris"


def test_extract_commune_hint_returns_none_without_postal_code():
    assert wc.extract_commune_hint("Manchecourt, Loiret") is None


# =============================================================================
# geocode_postal_code
# =============================================================================

def test_geocode_rejects_invalid_postal_code_format():
    with pytest.raises(wc.WeatherError):
        wc.geocode_postal_code("abc")
    with pytest.raises(wc.WeatherError):
        wc.geocode_postal_code("123")


def test_geocode_raises_when_no_commune_found(monkeypatch):
    monkeypatch.setattr(wc, "_get_json", lambda url: [])
    with pytest.raises(wc.WeatherError):
        wc.geocode_postal_code("99999")


def test_geocode_defaults_to_first_result_without_hint(monkeypatch):
    monkeypatch.setattr(wc, "_get_json", lambda url: [
        {"nom": "Ascoux", "centre": {"coordinates": [2.2514, 48.1294]}},
        {"nom": "Manchecourt", "centre": {"coordinates": [2.30, 48.15]}},
    ])
    result = wc.geocode_postal_code("45300")
    assert result["commune"] == "Ascoux"
    assert result["postal_code"] == "45300"
    assert result["lon"] == 2.2514
    assert result["lat"] == 48.1294


def test_geocode_matches_commune_hint_when_present(monkeypatch):
    """Cas réel vérifié en session : sans indice, 45300 -> 'Ascoux' au lieu de
    la commune attendue. Avec l'indice, la bonne commune est sélectionnée."""
    monkeypatch.setattr(wc, "_get_json", lambda url: [
        {"nom": "Ascoux", "centre": {"coordinates": [2.2514, 48.1294]}},
        {"nom": "Manchecourt", "centre": {"coordinates": [2.30, 48.15]}},
    ])
    result = wc.geocode_postal_code("45300", commune_hint="Manchecourt")
    assert result["commune"] == "Manchecourt"
    assert result["lon"] == 2.30


def test_geocode_hint_match_is_case_insensitive(monkeypatch):
    monkeypatch.setattr(wc, "_get_json", lambda url: [
        {"nom": "Manchecourt", "centre": {"coordinates": [2.30, 48.15]}},
    ])
    result = wc.geocode_postal_code("45300", commune_hint="manchecourt")
    assert result["commune"] == "Manchecourt"


def test_geocode_falls_back_to_first_when_hint_not_found(monkeypatch):
    """Cas réel : 'Manchecourt' n'est même pas une commune INSEE indépendante
    dans certains cas — le code ne doit pas planter, juste retomber sur le premier."""
    monkeypatch.setattr(wc, "_get_json", lambda url: [
        {"nom": "Ascoux", "centre": {"coordinates": [2.2514, 48.1294]}},
    ])
    result = wc.geocode_postal_code("45300", commune_hint="Manchecourt")
    assert result["commune"] == "Ascoux"


# =============================================================================
# get_current_weather
# =============================================================================

def test_get_current_weather_maps_known_wmo_code(monkeypatch):
    monkeypatch.setattr(wc, "_get_json", lambda url: {
        "current": {"temperature_2m": 21.4, "weather_code": 0}
    })
    result = wc.get_current_weather(48.0, 2.0)
    assert result == {"temperature_c": 21.4, "label": "Ciel dégagé", "icon": "sun", "weather_code": 0}


def test_get_current_weather_maps_rain_code(monkeypatch):
    monkeypatch.setattr(wc, "_get_json", lambda url: {
        "current": {"temperature_2m": 12.0, "weather_code": 61}
    })
    result = wc.get_current_weather(48.0, 2.0)
    assert result["label"] == "Pluie légère"
    assert result["icon"] == "rain"


def test_get_current_weather_unknown_code_has_fallback_label(monkeypatch):
    monkeypatch.setattr(wc, "_get_json", lambda url: {
        "current": {"temperature_2m": 10.0, "weather_code": 999}
    })
    result = wc.get_current_weather(48.0, 2.0)
    assert result["label"] == "Conditions inconnues"
    assert result["icon"] == "cloud"


def test_get_current_weather_raises_on_missing_current_key(monkeypatch):
    monkeypatch.setattr(wc, "_get_json", lambda url: {})
    with pytest.raises(wc.WeatherError):
        wc.get_current_weather(48.0, 2.0)


# =============================================================================
# get_weather_for_postal_code (intégration des deux appels)
# =============================================================================

def test_get_weather_for_postal_code_combines_geocode_and_forecast(monkeypatch):
    calls = {"geo": 0, "forecast": 0}

    def fake_get_json(url):
        if "geo.api.gouv.fr" in url:
            calls["geo"] += 1
            return [{"nom": "Manchecourt", "centre": {"coordinates": [2.30, 48.15]}}]
        calls["forecast"] += 1
        return {"current": {"temperature_2m": 18.0, "weather_code": 2}}

    monkeypatch.setattr(wc, "_get_json", fake_get_json)
    result = wc.get_weather_for_postal_code("45300", commune_hint="Manchecourt")

    assert calls == {"geo": 1, "forecast": 1}
    assert result["commune"] == "Manchecourt"
    assert result["temperature_c"] == 18.0
    assert result["label"] == "Partiellement nuageux"


# =============================================================================
# Erreurs réseau
# =============================================================================

def test_get_json_wraps_url_error_as_weather_error(monkeypatch):
    def raise_url_error(req, timeout):
        raise urllib.error.URLError("no connection")

    monkeypatch.setattr(wc.urllib.request, "urlopen", raise_url_error)
    with pytest.raises(wc.WeatherError):
        wc._get_json("https://example.invalid")
