"""
PROJECT      : ALFRED
BLOCK        : B15
FUNCTION     : 15.04
FILE         : tests/b15_tests/test_avatar_controller.py
ROLE         : Tests unitaires src/ui/avatar_controller.py

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-06-05
UPDATED      : 2026-06-05
VERSION      : V1.0
STATUS       : TESTED
"""

import pytest
from src.ui.avatar_controller import AVATAR_STATES


def test_avatar_states_is_dict():
    assert isinstance(AVATAR_STATES, dict)


def test_required_states_present():
    for state in ("idle", "listening", "thinking", "speaking", "error"):
        assert state in AVATAR_STATES, f"État manquant : {state}"


def test_values_are_strings():
    for key, val in AVATAR_STATES.items():
        assert isinstance(val, str), f"Valeur non-string pour l'état {key}"


def test_no_empty_values():
    for key, val in AVATAR_STATES.items():
        assert val.strip(), f"Valeur vide pour l'état {key}"
