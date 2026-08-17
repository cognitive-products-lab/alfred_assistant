"""
PROJECT      : ALFRED
BLOCK        : B08
FUNCTION     : Capture de préférence utilisateur explicite (main.py)
FILE         : tests/b08_tests/test_preference_capture.py
ROLE         : Tests pour _detect_and_save_preference / _load_preferences
               (data/preferences_profile.json).

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-08-17
VERSION      : V1.0
STATUS       : TESTED

DESCRIPTION :
Régression pour un bug réel trouvé le 17/08/2026 : le print() de
confirmation contenait un emoji (🧠) qui levait UnicodeEncodeError sur
la console Windows (cp1252), capté par le except Exception englobant —
la préférence était bien écrite sur disque mais la fonction retournait
None comme si l'écriture avait échoué. Corrigé en retirant l'emoji.
Testé avec un fichier temporaire, jamais data/preferences_profile.json réel.
"""

import json

import pytest

import src.main as main_module


@pytest.fixture
def prefs_file(tmp_path, monkeypatch):
    path = tmp_path / "preferences_profile.json"
    path.write_text(json.dumps({"_meta": {}, "preferences": []}), encoding="utf-8")
    monkeypatch.setattr(main_module, "_PREFS_FILE", path)
    return path


def test_trigger_phrase_saves_and_returns_content(prefs_file):
    result = main_module._detect_and_save_preference(
        "Retiens que je préfère qu'on m'appelle Cécé le matin"
    )
    assert result is not None
    assert "Cécé" in result

    data = json.loads(prefs_file.read_text(encoding="utf-8"))
    assert len(data["preferences"]) == 1
    assert data["preferences"][0]["source"] == "user_explicit"


def test_non_trigger_message_returns_none(prefs_file):
    result = main_module._detect_and_save_preference("Quel temps fait-il aujourd'hui ?")
    assert result is None

    data = json.loads(prefs_file.read_text(encoding="utf-8"))
    assert data["preferences"] == []


def test_saved_preference_is_reloadable(prefs_file):
    main_module._detect_and_save_preference("N'oublie pas que je travaille le mardi soir")
    prefs = main_module._load_preferences()
    assert len(prefs) == 1
    assert "mardi soir" in prefs[0]["content"]


def test_multiple_preferences_accumulate(prefs_file):
    main_module._detect_and_save_preference("Note que j'aime le café noir")
    main_module._detect_and_save_preference("Souviens-toi que je déteste être interrompue le matin")
    prefs = main_module._load_preferences()
    assert len(prefs) == 2
