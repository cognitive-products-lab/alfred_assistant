"""
PROJECT      : ALFRED
BLOCK        : B15
FILE         : tests/integrations_tests/test_outlook_calendar_prefs.py
ROLE         : Tests unitaires src/ui/outlook_calendar_prefs.py

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-07-24
VERSION      : V1.0
STATUS       : TESTED

DESCRIPTION :
Consentement Agenda Outlook (désactivé par défaut). Même pattern que
tests/integrations_tests/test_google_calendar_prefs.py.
"""

import shutil
import tempfile
from pathlib import Path

import pytest

from src.ui import outlook_calendar_prefs as ocp


@pytest.fixture(autouse=True)
def _isolated_file(monkeypatch):
    tmp_dir = Path(tempfile.mkdtemp(prefix="alfred_outlook_prefs_"))
    fake_file = tmp_dir / "outlook_calendar_prefs.json"
    monkeypatch.setattr(ocp, "_PREFS_FILE", fake_file)
    yield fake_file
    shutil.rmtree(tmp_dir, ignore_errors=True)


def test_consent_is_false_by_default():
    state = ocp.load_outlook_calendar_prefs()
    assert state["consent"] is False


def test_set_consent_true_roundtrip():
    ocp.set_consent(True)
    assert ocp.load_outlook_calendar_prefs()["consent"] is True


def test_set_consent_false_after_true():
    ocp.set_consent(True)
    ocp.set_consent(False)
    assert ocp.load_outlook_calendar_prefs()["consent"] is False
