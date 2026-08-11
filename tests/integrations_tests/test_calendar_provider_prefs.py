"""
PROJECT      : ALFRED
BLOCK        : B15
FILE         : tests/integrations_tests/test_calendar_provider_prefs.py
ROLE         : Tests unitaires src/ui/calendar_provider_prefs.py

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-07-24
VERSION      : V1.0
STATUS       : TESTED
"""

import shutil
import tempfile
from pathlib import Path

import pytest

from src.ui import calendar_provider_prefs as cpp


@pytest.fixture(autouse=True)
def _isolated_file(monkeypatch):
    tmp_dir = Path(tempfile.mkdtemp(prefix="alfred_calendar_provider_"))
    fake_file = tmp_dir / "calendar_provider_prefs.json"
    monkeypatch.setattr(cpp, "_PREFS_FILE", fake_file)
    yield fake_file
    shutil.rmtree(tmp_dir, ignore_errors=True)


def test_default_provider_is_google_when_no_file():
    assert cpp.load_default_calendar_provider() == "google"


def test_set_and_load_outlook_roundtrip():
    cpp.set_default_calendar_provider("outlook")
    assert cpp.load_default_calendar_provider() == "outlook"


def test_set_and_load_google_roundtrip():
    cpp.set_default_calendar_provider("outlook")
    cpp.set_default_calendar_provider("google")
    assert cpp.load_default_calendar_provider() == "google"


def test_set_invalid_provider_raises():
    with pytest.raises(ValueError):
        cpp.set_default_calendar_provider("yahoo")


def test_load_falls_back_to_google_on_corrupted_file(_isolated_file):
    fake_file = _isolated_file
    fake_file.parent.mkdir(parents=True, exist_ok=True)
    fake_file.write_text("not-valid-json", encoding="utf-8")
    assert cpp.load_default_calendar_provider() == "google"


def test_load_falls_back_to_google_on_invalid_provider_value(_isolated_file):
    import json
    fake_file = _isolated_file
    fake_file.parent.mkdir(parents=True, exist_ok=True)
    fake_file.write_text(json.dumps({"default_provider": "yahoo"}), encoding="utf-8")
    assert cpp.load_default_calendar_provider() == "google"
