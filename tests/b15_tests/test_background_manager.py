"""
PROJECT      : ALFRED
BLOCK        : B15
FUNCTION     : 15.02
FILE         : tests/b15_tests/test_background_manager.py
ROLE         : Tests unitaires src/ui/background_manager.py

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-06-05
UPDATED      : 2026-06-05
VERSION      : V1.0
STATUS       : TESTED
"""

import pytest
from src.ui.background_manager import BackgroundManager


def test_instantiation():
    bm = BackgroundManager()
    assert bm is not None


def test_set_background_no_args():
    bm = BackgroundManager()
    bm.set_background()


def test_set_background_with_location():
    bm = BackgroundManager()
    bm.set_background(location="salon")


def test_set_background_with_period():
    bm = BackgroundManager()
    bm.set_background(period="matin")


def test_set_background_full():
    bm = BackgroundManager()
    bm.set_background(location="cuisine", period="soir")
