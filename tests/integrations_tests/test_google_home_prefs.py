"""
PROJECT      : ALFRED
BLOCK        : B15
FILE         : tests/integrations_tests/test_google_home_prefs.py
ROLE         : Tests unitaires src/ui/google_home_prefs.py

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-07-23
VERSION      : V1.0
STATUS       : TESTED

DESCRIPTION :
Consentement Google Home + Project ID Device Access. Même pattern que
tests/integrations_tests/test_google_calendar_prefs.py.
"""

import shutil
import tempfile
from pathlib import Path

import pytest

from src.ui import google_home_prefs as ghp


@pytest.fixture(autouse=True)
def _isolated_file(monkeypatch):
    tmp_dir = Path(tempfile.mkdtemp(prefix="alfred_ghome_prefs_"))
    fake_file = tmp_dir / "google_home_prefs.json"
    monkeypatch.setattr(ghp, "_PREFS_FILE", fake_file)
    yield fake_file
    shutil.rmtree(tmp_dir, ignore_errors=True)


def test_consent_is_false_by_default():
    """Porte fermée par défaut — condition de sécurité du gate de consentement externe."""
    state = ghp.load_google_home_prefs()
    assert state["consent"] is False
    assert state["project_id"] is None


def test_set_consent_true_roundtrip():
    ghp.set_consent(True)
    assert ghp.load_google_home_prefs()["consent"] is True


def test_set_project_id_roundtrip():
    ghp.set_project_id("4e4b0f16-dee4-49be-a354-be038ab2643e")
    assert ghp.load_google_home_prefs()["project_id"] == "4e4b0f16-dee4-49be-a354-be038ab2643e"


def test_set_project_id_strips_whitespace():
    ghp.set_project_id("  abc-123  ")
    assert ghp.load_google_home_prefs()["project_id"] == "abc-123"


def test_set_project_id_empty_string_clears_to_none():
    ghp.set_project_id("abc-123")
    ghp.set_project_id("")
    assert ghp.load_google_home_prefs()["project_id"] is None


def test_consent_and_project_id_persist_independently():
    ghp.set_consent(True)
    ghp.set_project_id("proj-1")
    state = ghp.load_google_home_prefs()
    assert state["consent"] is True
    assert state["project_id"] == "proj-1"
