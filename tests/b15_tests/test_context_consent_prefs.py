"""
PROJECT      : ALFRED
BLOCK        : B15
FUNCTION     : 15.13
FILE         : tests/b15_tests/test_context_consent_prefs.py
ROLE         : Tests unitaires src/ui/context_consent_prefs.py

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-07-19
VERSION      : V1.0
STATUS       : TESTED

DESCRIPTION :
Consentement par catégorie ("Agenda du jour" / "5 dernières tâches" /
"Préférences vocales") pour le widget "données utilisées" du dashboard.
"""

import shutil
import tempfile
from pathlib import Path

import pytest

from src.ui import context_consent_prefs as ccp


@pytest.fixture(autouse=True)
def _isolated_file(monkeypatch):
    tmp_dir = Path(tempfile.mkdtemp(prefix="alfred_context_consent_"))
    monkeypatch.setattr(ccp, "_PREFS_FILE", tmp_dir / "context_consent.json")
    yield
    shutil.rmtree(tmp_dir, ignore_errors=True)


def test_defaults_are_all_enabled():
    state = ccp.load_context_consent()
    assert state == {"agenda": True, "taches": True, "voice_prefs": True}


def test_set_context_consent_disables_one_category_only():
    ccp.set_context_consent("agenda", False)
    state = ccp.load_context_consent()
    assert state["agenda"] is False
    assert state["taches"] is True
    assert state["voice_prefs"] is True


def test_set_context_consent_roundtrip_for_each_category():
    for category in ("agenda", "taches", "voice_prefs"):
        ccp.set_context_consent(category, False)
        assert ccp.load_context_consent()[category] is False
        ccp.set_context_consent(category, True)
        assert ccp.load_context_consent()[category] is True


def test_set_context_consent_rejects_unknown_category():
    with pytest.raises(ValueError):
        ccp.set_context_consent("inconnu", False)
