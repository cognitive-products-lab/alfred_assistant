"""
PROJECT      : ALFRED
BLOCK        : B15
FUNCTION     : 15.07
FILE         : tests/b15_tests/test_weather_prefs.py
ROLE         : Tests unitaires src/ui/weather_prefs.py

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-07-19
VERSION      : V1.0
STATUS       : TESTED

DESCRIPTION :
Consentement météo (désactivé par défaut) + dernier code postal recherché.
"""

import shutil
import tempfile
from pathlib import Path

import pytest

from src.ui import weather_prefs as wp


@pytest.fixture(autouse=True)
def _isolated_file(monkeypatch):
    tmp_dir = Path(tempfile.mkdtemp(prefix="alfred_weather_prefs_"))
    fake_file = tmp_dir / "weather_prefs.json"
    monkeypatch.setattr(wp, "_PREFS_FILE", fake_file)
    yield fake_file
    shutil.rmtree(tmp_dir, ignore_errors=True)


def test_consent_is_false_by_default():
    """Porte fermée par défaut — condition de sécurité du gate de consentement externe."""
    state = wp.load_weather_prefs()
    assert state["consent"] is False
    assert state["last_postal_code"] is None


def test_set_consent_true_roundtrip():
    wp.set_consent(True)
    assert wp.load_weather_prefs()["consent"] is True


def test_set_consent_false_after_true():
    wp.set_consent(True)
    wp.set_consent(False)
    assert wp.load_weather_prefs()["consent"] is False


def test_set_last_postal_code_roundtrip():
    wp.set_last_postal_code("75001")
    assert wp.load_weather_prefs()["last_postal_code"] == "75001"


def test_set_last_postal_code_none_clears_override():
    wp.set_last_postal_code("75001")
    wp.set_last_postal_code(None)
    assert wp.load_weather_prefs()["last_postal_code"] is None


def test_consent_and_postal_code_persist_independently():
    wp.set_consent(True)
    wp.set_last_postal_code("13001")
    state = wp.load_weather_prefs()
    assert state["consent"] is True
    assert state["last_postal_code"] == "13001"
