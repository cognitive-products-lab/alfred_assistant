"""
PROJECT      : ALFRED
BLOCK        : B15
FUNCTION     : SMOKE
FILE         : tests/b15_tests/test_smoke_pin_dialog.py
ROLE         : Smoke tests pour les fonctions pures de src/ui/pin_dialog.py
               (le reste du module est une UI tkinter modale bloquante,
               non testable par automatisation).

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-07-05
UPDATED      : 2026-07-05
VERSION      : V1.0
STATUS       : TESTED
"""

import tkinter as tk

import pytest

from src.ui.pin_dialog import _load_font, _center


def test_load_font_returns_string():
    font_name = _load_font()
    assert font_name in ("OpenDyslexic3", "Segoe UI")


def test_center_positions_window_without_mainloop():
    try:
        root = tk.Tk()
    except tk.TclError:
        pytest.skip("Pas d'affichage disponible pour tkinter dans cet environnement")
    try:
        _center(root, 400, 300)
        root.update()
        geometry = root.geometry()
        assert "400x300" in geometry
    finally:
        root.destroy()
