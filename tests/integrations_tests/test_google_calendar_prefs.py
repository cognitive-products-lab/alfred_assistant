"""
PROJECT      : ALFRED
BLOCK        : B15
FILE         : tests/integrations_tests/test_google_calendar_prefs.py
ROLE         : Tests unitaires src/ui/google_calendar_prefs.py

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-07-23
VERSION      : V1.0
STATUS       : TESTED

DESCRIPTION :
Consentement Google Agenda (désactivé par défaut). Même pattern que
tests/b15_tests/test_weather_prefs.py.
"""

import shutil
import tempfile
from pathlib import Path

import pytest

from src.ui import google_calendar_prefs as gcp


@pytest.fixture(autouse=True)
def _isolated_file(monkeypatch):
    tmp_dir = Path(tempfile.mkdtemp(prefix="alfred_gcal_prefs_"))
    fake_file = tmp_dir / "google_calendar_prefs.json"
    monkeypatch.setattr(gcp, "_PREFS_FILE", fake_file)
    yield fake_file
    shutil.rmtree(tmp_dir, ignore_errors=True)


def test_consent_is_false_by_default():
    """Porte fermée par défaut — condition de sécurité du gate de consentement externe."""
    state = gcp.load_google_calendar_prefs()
    assert state["consent"] is False


def test_set_consent_true_roundtrip():
    gcp.set_consent(True)
    assert gcp.load_google_calendar_prefs()["consent"] is True


def test_set_consent_false_after_true():
    gcp.set_consent(True)
    gcp.set_consent(False)
    assert gcp.load_google_calendar_prefs()["consent"] is False
