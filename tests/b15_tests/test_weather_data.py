"""
PROJECT      : ALFRED
BLOCK        : B15
FUNCTION     : 15.09
FILE         : tests/b15_tests/test_weather_data.py
ROLE         : Tests unitaires src/ui/weather_data.py

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-07-19
VERSION      : V1.0
STATUS       : TESTED

DESCRIPTION :
Orchestration météo : porte de consentement fermée par défaut, localisation
par défaut extraite du profil, override utilisateur prioritaire, cache
mémoire 20 min, propagation des erreurs réseau sans jamais lever d'exception
côté appelant (toujours un dict avec ok=True/False).
"""

import json
import shutil
import tempfile
from pathlib import Path

import pytest

from paths import PATHS
from src.ui import weather_data as wd
from src.ui import weather_prefs as wp


@pytest.fixture(autouse=True)
def _isolated_prefs_file(monkeypatch):
    tmp_dir = Path(tempfile.mkdtemp(prefix="alfred_weather_data_"))
    monkeypatch.setattr(wp, "_PREFS_FILE", tmp_dir / "weather_prefs.json")
    yield
    shutil.rmtree(tmp_dir, ignore_errors=True)


@pytest.fixture(autouse=True)
def _clear_weather_cache():
    wd._cache.clear()
    yield
    wd._cache.clear()


@pytest.fixture
def _profile_with_postal_code(monkeypatch):
    """Redirige data_profile vers un identity_celine.json de test."""
    tmp_dir = Path(tempfile.mkdtemp(prefix="alfred_profile_"))
    monkeypatch.setattr(PATHS, "data_profile", tmp_dir)

    def _write(localite: str):
        (tmp_dir / "identity_celine.json").write_text(
            json.dumps({"identity": {"localite": localite}}, ensure_ascii=False),
            encoding="utf-8",
        )

    yield _write
    shutil.rmtree(tmp_dir, ignore_errors=True)


def _fake_weather_result(**overrides):
    base = {"commune": "Manchecourt", "postal_code": "45300", "lat": 48.1, "lon": 2.3,
            "temperature_c": 20.0, "label": "Ciel dégagé", "icon": "sun", "weather_code": 0}
    base.update(overrides)
    return base


# =============================================================================
# Porte de consentement — condition de sécurité
# =============================================================================

def test_get_weather_state_returns_consent_false_by_default():
    """Rien n'est appelé côté réseau tant que le consentement n'est pas activé."""
    state = wd.get_weather_state()
    assert state == {"consent": False}


def test_get_weather_state_never_touches_network_without_consent(monkeypatch):
    def _boom(*a, **k):
        raise AssertionError("weather_client ne doit pas être appelé sans consentement")

    monkeypatch.setattr("src.integrations.weather_client.get_weather_for_postal_code", _boom)
    wd.get_weather_state()  # ne doit pas lever AssertionError


def test_search_weather_returns_consent_false_without_consent():
    assert wd.search_weather("75001") == {"consent": False}


# =============================================================================
# Localisation par défaut (profil) vs override
# =============================================================================

def test_no_location_when_profile_has_no_postal_code(monkeypatch, _profile_with_postal_code):
    _profile_with_postal_code("Pas de code postal ici")
    wp.set_consent(True)
    state = wd.get_weather_state()
    assert state == {"consent": True, "no_location": True}


def test_uses_profile_postal_code_by_default(monkeypatch, _profile_with_postal_code):
    _profile_with_postal_code("45300 Manchecourt, Loiret")
    wp.set_consent(True)
    monkeypatch.setattr(
        "src.integrations.weather_client.get_weather_for_postal_code",
        lambda cp, commune_hint=None: _fake_weather_result(postal_code=cp, commune=commune_hint),
    )
    state = wd.get_weather_state()
    assert state["consent"] is True
    assert state["is_override"] is False
    assert state["ok"] is True
    assert state["postal_code"] == "45300"
    assert state["commune"] == "Manchecourt"  # indice de commune transmis


def test_search_weather_sets_override_and_persists(monkeypatch, _profile_with_postal_code):
    _profile_with_postal_code("45300 Manchecourt, Loiret")
    wp.set_consent(True)
    monkeypatch.setattr(
        "src.integrations.weather_client.get_weather_for_postal_code",
        lambda cp, commune_hint=None: _fake_weather_result(postal_code=cp, commune="Paris"),
    )
    state = wd.search_weather("75001")
    assert state["is_override"] is True
    assert state["postal_code"] == "75001"
    assert wp.load_weather_prefs()["last_postal_code"] == "75001"


def test_search_weather_rejects_invalid_postal_code():
    wp.set_consent(True)
    state = wd.search_weather("abc")
    assert state["ok"] is False
    assert "code postal" in state["error"]


def test_reset_weather_location_clears_override(monkeypatch, _profile_with_postal_code):
    _profile_with_postal_code("45300 Manchecourt, Loiret")
    wp.set_consent(True)
    monkeypatch.setattr(
        "src.integrations.weather_client.get_weather_for_postal_code",
        lambda cp, commune_hint=None: _fake_weather_result(postal_code=cp),
    )
    wd.search_weather("75001")
    state = wd.reset_weather_location()
    assert state["is_override"] is False
    assert state["postal_code"] == "45300"
    assert wp.load_weather_prefs()["last_postal_code"] is None


# =============================================================================
# set_weather_consent
# =============================================================================

def test_set_weather_consent_true_returns_full_state(monkeypatch, _profile_with_postal_code):
    _profile_with_postal_code("45300 Manchecourt, Loiret")
    monkeypatch.setattr(
        "src.integrations.weather_client.get_weather_for_postal_code",
        lambda cp, commune_hint=None: _fake_weather_result(postal_code=cp),
    )
    state = wd.set_weather_consent(True)
    assert state["consent"] is True
    assert state["ok"] is True


def test_set_weather_consent_false_returns_minimal_state():
    wp.set_consent(True)
    state = wd.set_weather_consent(False)
    assert state == {"consent": False}


# =============================================================================
# Cache mémoire
# =============================================================================

def test_fetch_cached_reuses_result_within_ttl(monkeypatch, _profile_with_postal_code):
    _profile_with_postal_code("45300 Manchecourt, Loiret")
    wp.set_consent(True)
    call_count = {"n": 0}

    def fake_fetch(cp, commune_hint=None):
        call_count["n"] += 1
        return _fake_weather_result(postal_code=cp)

    monkeypatch.setattr("src.integrations.weather_client.get_weather_for_postal_code", fake_fetch)
    wd.get_weather_state()
    wd.get_weather_state()
    wd.get_weather_state()
    assert call_count["n"] == 1  # servi par le cache les 2 fois suivantes


def test_fetch_cached_refetches_after_ttl_expires(monkeypatch, _profile_with_postal_code):
    _profile_with_postal_code("45300 Manchecourt, Loiret")
    wp.set_consent(True)
    call_count = {"n": 0}
    monkeypatch.setattr(
        "src.integrations.weather_client.get_weather_for_postal_code",
        lambda cp, commune_hint=None: (call_count.__setitem__("n", call_count["n"] + 1),
                                        _fake_weather_result(postal_code=cp))[1],
    )
    fake_now = [1000.0]
    monkeypatch.setattr(wd.time, "time", lambda: fake_now[0])

    wd.get_weather_state()
    fake_now[0] += wd._CACHE_TTL_SECONDS + 1
    wd.get_weather_state()

    assert call_count["n"] == 2


# =============================================================================
# Erreur réseau propagée sans exception
# =============================================================================

def test_weather_error_from_client_becomes_ok_false(monkeypatch, _profile_with_postal_code):
    from src.integrations.weather_client import WeatherError

    _profile_with_postal_code("45300 Manchecourt, Loiret")
    wp.set_consent(True)

    def raise_error(cp, commune_hint=None):
        raise WeatherError("Connexion météo impossible : timeout")

    monkeypatch.setattr("src.integrations.weather_client.get_weather_for_postal_code", raise_error)
    state = wd.get_weather_state()
    assert state["ok"] is False
    assert "Connexion météo impossible" in state["error"]
