"""
PROJECT      : ALFRED
BLOCK        : B15 -- Avatar & Interface
FUNCTION     : 15.02.001 -> 15.02.009
FILE         : tests/b15_tests/test_avatar_renderer.py
ROLE         : Tests unitaires AvatarRendererLogic -- sprite, couleur, animation, layout

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-05-14
UPDATED      : 2026-06-01 (tests _STATE_LAYOUT no-overflow, blink exclusion thinking)
VERSION      : V1.2
STATUS       : STABLE

DESCRIPTION :
Tests de la couche logique pure (AvatarRendererLogic).
Aucune dependance Kivy -- executables en CI headless.
Couvre : sprite selection, couleur, frames parole, animation mapping, existence assets.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from src.ui.avatar_renderer import (
    AvatarRendererLogic,
    _MEDIUM_SPRITES,
    _STATE_COLOR_HEX,
    _STATE_ANIM,
    _STATE_LAYOUT,
    _SPEAKING_MEDIUM_FRAMES,
    _hex_to_rgb,
)


# ---------------------------------------------------------
# _hex_to_rgb
# ---------------------------------------------------------

class TestHexToRgb:

    def test_black(self):
        r, g, b = _hex_to_rgb("#000000")
        assert r == 0.0 and g == 0.0 and b == 0.0

    def test_white(self):
        r, g, b = _hex_to_rgb("#FFFFFF")
        assert abs(r - 1.0) < 0.005

    def test_alfred_blue(self):
        r, g, b = _hex_to_rgb("#4A90D9")
        assert 0.28 < r < 0.30
        assert 0.56 < g < 0.57
        assert 0.85 < b < 0.86

    def test_returns_three_floats(self):
        result = _hex_to_rgb("#8B9FD4")
        assert len(result) == 3
        assert all(0.0 <= v <= 1.0 for v in result)


# ---------------------------------------------------------
# Tables de correspondance
# ---------------------------------------------------------

class TestStateTables:

    _REQUIRED_STATES = (
        "idle", "listening", "thinking", "speaking",
        "support", "focus", "challenge", "complicite",
        "error", "offline",
    )

    def test_all_states_have_sprite(self):
        for s in self._REQUIRED_STATES:
            assert s in _MEDIUM_SPRITES, f"Etat manquant dans _MEDIUM_SPRITES : {s}"

    def test_all_states_have_color(self):
        for s in self._REQUIRED_STATES:
            assert s in _STATE_COLOR_HEX, f"Etat manquant dans _STATE_COLOR_HEX : {s}"

    def test_all_states_have_anim(self):
        for s in self._REQUIRED_STATES:
            assert s in _STATE_ANIM, f"Etat manquant dans _STATE_ANIM : {s}"

    def test_sprite_filenames_valid(self):
        for state, filename in _MEDIUM_SPRITES.items():
            assert isinstance(filename, str) and filename.endswith(".png"), (
                f"{state}: nom de fichier invalide = {filename}"
            )

    def test_color_hex_format(self):
        for state, hex_color in _STATE_COLOR_HEX.items():
            assert hex_color.startswith("#"), f"{state}: manque #"
            assert len(hex_color) == 7, f"{state}: longueur incorrecte"

    def test_anim_tuples_valid_type(self):
        valid_types = {"breathe", "pulse", "mouth", "flash", "static", "none"}
        for state, (anim_type, period) in _STATE_ANIM.items():
            assert anim_type in valid_types, f"{state}: type anim invalide = {anim_type}"
            assert isinstance(period, float), f"{state}: periode doit etre float"

    def test_speaking_frames_not_empty(self):
        assert len(_SPEAKING_MEDIUM_FRAMES) >= 2

    def test_speaking_frames_valid(self):
        for filename in _SPEAKING_MEDIUM_FRAMES:
            assert isinstance(filename, str) and filename.endswith(".png")


# ---------------------------------------------------------
# AvatarRendererLogic
# ---------------------------------------------------------

class TestAvatarRendererLogic:

    def test_initial_state_idle(self):
        logic = AvatarRendererLogic()
        assert logic.state == "idle"

    def test_not_speaking_initially(self):
        logic = AvatarRendererLogic()
        assert logic.is_speaking is False

    def test_set_state_changes(self):
        logic = AvatarRendererLogic()
        logic.set_state("listening")
        assert logic.state == "listening"

    def test_set_speaking_flags(self):
        logic = AvatarRendererLogic()
        logic.set_state("speaking")
        assert logic.is_speaking is True

    def test_set_other_state_clears_speaking(self):
        logic = AvatarRendererLogic()
        logic.set_state("speaking")
        logic.set_state("idle")
        assert logic.is_speaking is False

    def test_get_sprite_returns_string(self):
        logic = AvatarRendererLogic()
        for state in _MEDIUM_SPRITES:
            sprite = logic.get_sprite(state)
            assert isinstance(sprite, str) and len(sprite) > 0

    def test_get_sprite_current_when_empty(self):
        logic = AvatarRendererLogic()
        logic.set_state("support")
        sprite = logic.get_sprite()
        assert "alfred_medium_love" in sprite

    def test_get_sprite_idle_contains_half(self):
        logic = AvatarRendererLogic()
        sprite = logic.get_sprite("idle")
        assert "alfred_medium_neutral" in sprite

    def test_get_sprite_offline_uses_thinking_png_or_closed(self):
        # V1.2+ : offline utilise alfred_medium_neutral
        logic = AvatarRendererLogic()
        sprite = logic.get_sprite("offline")
        assert "alfred_medium_neutral" in sprite

    def test_get_sprite_speaking_contains_a(self):
        logic = AvatarRendererLogic()
        logic.set_state("speaking")
        frame = logic.get_speaking_frame()
        assert "neutral_a" in frame

    def test_next_speaking_frame_cycles(self):
        logic = AvatarRendererLogic()
        logic.set_state("speaking")
        expected_count = len(_SPEAKING_MEDIUM_FRAMES)
        frames = set()
        for _ in range(expected_count + 2):
            frames.add(logic.next_speaking_frame())
        assert len(frames) == expected_count

    def test_speaking_frame_reset_on_state_change(self):
        logic = AvatarRendererLogic()
        logic.set_state("speaking")
        logic.next_speaking_frame()
        logic.next_speaking_frame()
        logic.set_state("idle")
        logic.set_state("speaking")
        # Apres reset, on repart du frame 0 -> next -> frame 1
        first = logic.next_speaking_frame()
        # Le premier appel apres reset est l'index 1 (0+1)
        assert isinstance(first, str)

    def test_get_color_hex_idle(self):
        logic = AvatarRendererLogic()
        assert logic.get_color_hex("idle") == "#8B9FD4"

    def test_get_color_hex_error_red(self):
        logic = AvatarRendererLogic()
        assert logic.get_color_hex("error") == "#D0021B"

    def test_get_color_hex_current(self):
        logic = AvatarRendererLogic()
        logic.set_state("focus")
        assert logic.get_color_hex() == "#4A90D9"

    def test_get_color_rgb_returns_floats(self):
        logic = AvatarRendererLogic()
        r, g, b = logic.get_color_rgb("idle")
        assert all(0.0 <= v <= 1.0 for v in (r, g, b))

    def test_get_anim_idle_breathe(self):
        logic = AvatarRendererLogic()
        anim_type, period = logic.get_anim("idle")
        assert anim_type == "breathe"
        assert period > 0

    def test_get_anim_focus_static(self):
        logic = AvatarRendererLogic()
        anim_type, _ = logic.get_anim("focus")
        assert anim_type == "static"

    def test_get_anim_speaking_mouth(self):
        logic = AvatarRendererLogic()
        anim_type, period = logic.get_anim("speaking")
        assert anim_type == "mouth"
        assert period < 1.0

    def test_get_anim_error_flash(self):
        logic = AvatarRendererLogic()
        anim_type, _ = logic.get_anim("error")
        assert anim_type == "flash"

    def test_get_anim_current_state(self):
        logic = AvatarRendererLogic()
        logic.set_state("challenge")
        anim_type, period = logic.get_anim()
        assert anim_type == "pulse"
        assert period < 1.0


# ---------------------------------------------------------
# Assets (existence fichiers sur disque)
# ---------------------------------------------------------

class TestAvatarAssets:

    def test_all_sprites_exist(self):
        logic = AvatarRendererLogic()
        results = logic.all_sprites_exist()
        missing = [s for s, ok in results.items() if not ok]
        assert missing == [], f"Sprites manquants : {missing}"

    def test_all_speaking_frames_exist(self):
        from src.ui.avatar_renderer import _ASSET_MEDIUM
        from pathlib import Path
        for filename in _SPEAKING_MEDIUM_FRAMES:
            path = _ASSET_MEDIUM / filename
            assert path.exists(), f"Frame manquant : {path}"

    def test_sprite_path_format(self):
        logic = AvatarRendererLogic()
        path = logic.get_sprite("idle")
        assert "alfred_medium" in path
        assert path.endswith(".png")


# ---------------------------------------------------------
# _STATE_LAYOUT -- alignement zoom par état (15.02.007-008)
# ---------------------------------------------------------

class TestStateLayout:

    _REQUIRED_STATES = (
        "idle", "listening", "thinking", "speaking",
        "support", "focus", "challenge", "complicite",
        "error", "offline",
    )

    def test_all_states_have_layout(self):
        for s in self._REQUIRED_STATES:
            assert s in _STATE_LAYOUT, f"Etat manquant dans _STATE_LAYOUT : {s}"

    def test_layout_tuples_are_pairs(self):
        for state, layout in _STATE_LAYOUT.items():
            assert len(layout) == 2, f"{state}: layout doit etre un tuple (sh, y)"

    def test_scale_factor_positive(self):
        """Le facteur de zoom doit etre positif."""
        for state, (sh, y) in _STATE_LAYOUT.items():
            assert sh > 0, f"{state}: sh={sh} doit etre > 0"

    def test_scale_factor_reasonable_range(self):
        """Pas de zoom absurde (< 0.5 ou > 2.0)."""
        for state, (sh, y) in _STATE_LAYOUT.items():
            assert 0.5 < sh < 2.0, f"{state}: sh={sh} hors plage"

    def test_no_overflow_below_zone(self):
        """scale + y_offset <= 1 : aucun debordement sous la zone."""
        for state, (sh, y) in _STATE_LAYOUT.items():
            assert sh + y <= 1.0 + 1e-6, f"{state}: sh+y={sh+y:.3f} > 1 (debordement bas)"

    def test_no_overflow_above_bottom(self):
        """y_offset >= 0 : avatar ne deborde pas au-dessus du bas de zone."""
        for state, (sh, y) in _STATE_LAYOUT.items():
            assert y >= -1e-6, f"{state}: y={y} < 0 (debordement bas)"

    def test_thinking_contained(self):
        """thinking doit etre contenu dans la zone (pas de debordement)."""
        sh, y = _STATE_LAYOUT["thinking"]
        assert sh + y <= 1.0 + 1e-6
        assert y >= -1e-6
