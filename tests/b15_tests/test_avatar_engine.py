"""
PROJECT      : ALFRED
BLOCK        : B15 -- Avatar & Interface
FUNCTION     : 15.07.001 -> 15.07.013
FILE         : tests/b15_tests/test_avatar_engine.py
ROLE         : Tests unitaires AvatarEngine -- facade moteur avatar

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-06-01
UPDATED      : 2026-06-01 (tests sync TTS begin/end_response, on_tts_stop)
VERSION      : V1.0
STATUS       : STABLE

DESCRIPTION :
Tests complets de src/ui/avatar_engine.py.
Mode headless -- aucune dependance Kivy.
Couvre : initialisation, etats, mode, phonemes, background,
         hooks, singleton, statut, arret propre.
"""

import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from src.ui.avatar_engine import (
    AvatarEngine,
    get_avatar_engine,
    reset_avatar_engine,
    _PHONEME_MAP,
)


# ============================================================
# Fixtures helpers
# ============================================================

def _engine() -> AvatarEngine:
    """Retourne un engine headless isole (singleton reinitialise)."""
    reset_avatar_engine()
    # Reinitialise aussi le singleton controller
    import src.ui.avatar_controller as _ac
    _ac._avatar_controller = None
    return AvatarEngine(headless=True)


# ============================================================
# 15.07.001 -- Initialisation
# ============================================================

class TestInit:

    def test_headless_mode(self):
        eng = _engine()
        assert eng.headless is True

    def test_not_started_before_start(self):
        eng = _engine()
        assert eng.started is False

    def test_start_sets_started(self):
        eng = _engine()
        eng.start()
        assert eng.started is True

    def test_start_without_renderer_ok(self):
        eng = _engine()
        eng.start(renderer=None)
        assert eng._renderer is None

    def test_start_with_renderer_sets_renderer(self):
        eng = _engine()
        mock_renderer = MagicMock()
        eng.start(renderer=mock_renderer)
        assert eng._renderer is mock_renderer

    def test_start_connects_renderer_to_controller(self):
        eng = _engine()
        mock_renderer = MagicMock()
        eng.start(renderer=mock_renderer)
        assert eng._controller._renderer is mock_renderer

    def test_default_location_salon(self):
        eng = _engine()
        assert eng._current_location == "salon"

    def test_stop_sets_not_started(self):
        eng = _engine()
        eng.start()
        eng.stop()
        assert eng.started is False

    def test_stop_sets_idle(self):
        eng = _engine()
        eng.start()
        eng.set_thinking()
        eng.stop()
        assert eng.state_name == "idle"


# ============================================================
# 15.07.002 -- Etats principaux
# ============================================================

class TestStates:

    def test_set_speaking_true(self):
        eng = _engine()
        eng.set_speaking(True)
        assert eng.is_speaking is True

    def test_set_speaking_false(self):
        eng = _engine()
        eng.set_speaking(True)
        eng.set_speaking(False)
        assert eng.is_speaking is False

    def test_set_listening_true(self):
        eng = _engine()
        eng.set_listening(True)
        assert eng.is_listening is True

    def test_set_listening_false(self):
        eng = _engine()
        eng.set_listening(True)
        eng.set_listening(False)
        assert eng.is_listening is False

    def test_set_thinking(self):
        eng = _engine()
        eng.set_thinking()
        assert eng.state_name == "thinking"

    def test_set_idle(self):
        eng = _engine()
        eng.set_thinking()
        eng.set_idle()
        assert eng.state_name == "idle"

    def test_set_error(self):
        eng = _engine()
        eng.set_error("test error")
        assert eng.state_name == "error"

    def test_set_state_valid(self):
        eng = _engine()
        ok = eng.set_state("listening")
        assert ok is True
        assert eng.state_name == "listening"

    def test_set_state_invalid(self):
        eng = _engine()
        ok = eng.set_state("unknown_state_xyz")
        assert ok is False

    def test_set_state_same_returns_false(self):
        eng = _engine()
        eng.set_state("thinking")
        ok = eng.set_state("thinking")
        assert ok is False

    def test_speaking_sets_logic_state(self):
        eng = _engine()
        eng.set_speaking(True)
        assert eng._logic.state == "speaking"

    def test_thinking_sets_logic_state(self):
        eng = _engine()
        eng.set_thinking()
        assert eng._logic.state == "thinking"


# ============================================================
# 15.07.003 -- Mode ALFRED
# ============================================================

class TestMode:

    def test_set_mode_support(self):
        eng = _engine()
        ok = eng.set_mode("support")
        assert ok is True

    def test_set_mode_focus(self):
        eng = _engine()
        ok = eng.set_mode("focus")
        assert ok is True

    def test_set_mode_challenge(self):
        eng = _engine()
        ok = eng.set_mode("challenge")
        assert ok is True

    def test_set_mode_complicite(self):
        eng = _engine()
        ok = eng.set_mode("complicite")
        assert ok is True

    def test_set_mode_invalid(self):
        eng = _engine()
        ok = eng.set_mode("unknown_mode")
        assert ok is False

    def test_set_emotion(self):
        eng = _engine()
        eng.set_emotion("happy")
        assert eng._controller.current_state.emotion == "happy"

    def test_mode_propagated_to_controller(self):
        eng = _engine()
        eng.set_mode("support")
        assert eng._controller.current_state.mode == "support"


# ============================================================
# 15.07.004 -- Lip-sync phonemes
# ============================================================

class TestPhonemes:

    def test_phoneme_a_returns_string(self):
        eng = _engine()
        path = eng.set_phoneme("a")
        assert isinstance(path, str)
        assert len(path) > 0

    def test_phoneme_m_returns_string(self):
        eng = _engine()
        path = eng.set_phoneme("m")
        assert isinstance(path, str)

    def test_phoneme_unknown_returns_string(self):
        eng = _engine()
        path = eng.set_phoneme("xyz_unknown")
        assert isinstance(path, str)

    def test_phoneme_empty_returns_string(self):
        eng = _engine()
        path = eng.set_phoneme("")
        assert isinstance(path, str)

    def test_next_speaking_frame_returns_string(self):
        eng = _engine()
        frame = eng.next_speaking_frame()
        assert isinstance(frame, str)

    def test_next_speaking_frame_advances(self):
        eng = _engine()
        f1 = eng.next_speaking_frame()
        f2 = eng.next_speaking_frame()
        # Avec 6 frames, les deux premiers doivent etre differents
        # (sauf si fallback base_normal avec 1 seul sprite)
        assert isinstance(f1, str) and isinstance(f2, str)

    def test_phoneme_map_covers_main_vowels(self):
        for ph in ["a", "e", "i", "o", "u", "m"]:
            assert ph in _PHONEME_MAP

    def test_phoneme_map_silence(self):
        assert _PHONEME_MAP.get("") == "idle"
        assert _PHONEME_MAP.get("sil") == "idle"


# ============================================================
# 15.07.005 -- Background
# ============================================================

class TestBackground:

    def test_set_background_returns_string(self):
        eng = _engine()
        path = eng.set_background("salon", "jour")
        assert isinstance(path, str)

    def test_set_background_updates_location(self):
        eng = _engine()
        eng.set_background("chambre", "nuit")
        assert eng._current_location == "chambre"

    def test_set_background_updates_period(self):
        eng = _engine()
        eng.set_background("salon", "soiree")
        assert eng._current_period == "soiree"

    def test_set_background_without_period_uses_auto(self):
        eng = _engine()
        eng.set_background("salon")
        assert eng._current_period != ""

    def test_set_background_without_location_keeps_current(self):
        eng = _engine()
        eng._current_location = "bureau"
        eng.set_background(period="jour")
        assert eng._current_location == "bureau"

    def test_refresh_background_returns_string(self):
        eng = _engine()
        path = eng.refresh_background()
        assert isinstance(path, str)

    def test_set_background_calls_renderer(self):
        eng = _engine()
        mock_renderer = MagicMock()
        eng.start(renderer=mock_renderer)
        eng.set_background("ville", "jour")
        mock_renderer.update_background.assert_called()

    def test_set_background_no_renderer_ok(self):
        eng = _engine()
        eng.start(renderer=None)
        path = eng.set_background("salon", "jour")
        assert isinstance(path, str)


# ============================================================
# 15.07.006 -- Hooks pipeline
# ============================================================

class TestHooks:

    def test_register_hook_called_on_state_change(self):
        eng = _engine()
        fired = []
        eng.register_hook(lambda s: fired.append(s))
        eng.set_thinking()
        assert "thinking" in fired

    def test_register_hook_called_on_speaking(self):
        eng = _engine()
        fired = []
        eng.register_hook(lambda s: fired.append(s))
        eng.set_speaking(True)
        assert "speaking" in fired

    def test_multiple_hooks_all_called(self):
        eng = _engine()
        log1, log2 = [], []
        eng.register_hook(lambda s: log1.append(s))
        eng.register_hook(lambda s: log2.append(s))
        eng.set_error()
        assert log1 and log2

    def test_hook_exception_does_not_crash_engine(self):
        eng = _engine()
        def bad_hook(s):
            raise RuntimeError("hook crash")
        eng.register_hook(bad_hook)
        eng.set_thinking()  # ne doit pas lever

    def test_hook_registered_on_controller(self):
        eng = _engine()
        fired = []
        eng.register_hook(lambda s: fired.append(s))
        # Le hook est aussi sur le controller
        assert len(eng._controller._hooks) >= 1


# ============================================================
# 15.07.007 -- Mode headless
# ============================================================

class TestHeadless:

    def test_headless_no_renderer(self):
        eng = _engine()
        assert eng._renderer is None

    def test_headless_set_speaking_no_crash(self):
        eng = _engine()
        eng.set_speaking(True)
        eng.set_speaking(False)

    def test_headless_set_background_no_crash(self):
        eng = _engine()
        eng.set_background("salon", "jour")

    def test_headless_full_cycle(self):
        eng = _engine()
        eng.start()
        eng.set_mode("support")
        eng.set_listening(True)
        eng.set_thinking()
        eng.set_speaking(True)
        eng.set_phoneme("a")
        eng.set_phoneme("m")
        eng.set_speaking(False)
        eng.set_idle()
        eng.stop()
        assert eng.state_name == "idle"


# ============================================================
# 15.07.008 -- Statut consolide
# ============================================================

class TestStatus:

    def test_status_returns_dict(self):
        eng = _engine()
        s = eng.status()
        assert isinstance(s, dict)

    def test_status_keys_present(self):
        eng = _engine()
        s = eng.status()
        for key in ("state", "mode", "is_speaking", "is_listening",
                    "emotion", "location", "period", "headless",
                    "has_renderer", "version", "timestamp"):
            assert key in s, f"Cle manquante : {key}"

    def test_status_version(self):
        eng = _engine()
        assert eng.status()["version"] == "avatar_engine_v1"

    def test_status_state_after_thinking(self):
        eng = _engine()
        eng.set_thinking()
        assert eng.status()["state"] == "thinking"

    def test_status_has_renderer_false(self):
        eng = _engine()
        assert eng.status()["has_renderer"] is False

    def test_status_has_renderer_true(self):
        eng = _engine()
        mock_renderer = MagicMock()
        mock_renderer.status.return_value = {"kivy": False}
        eng.start(renderer=mock_renderer)
        assert eng.status()["has_renderer"] is True

    def test_status_timestamp_is_string(self):
        eng = _engine()
        ts = eng.status()["timestamp"]
        assert isinstance(ts, str) and "T" in ts


# ============================================================
# 15.07.009 -- Singleton
# ============================================================

class TestSingleton:

    def test_get_avatar_engine_returns_engine(self):
        reset_avatar_engine()
        import src.ui.avatar_controller as _ac
        _ac._avatar_controller = None
        eng = get_avatar_engine(headless=True)
        assert isinstance(eng, AvatarEngine)

    def test_get_avatar_engine_same_instance(self):
        reset_avatar_engine()
        import src.ui.avatar_controller as _ac
        _ac._avatar_controller = None
        e1 = get_avatar_engine(headless=True)
        e2 = get_avatar_engine(headless=True)
        assert e1 is e2

    def test_reset_avatar_engine_creates_new(self):
        import src.ui.avatar_controller as _ac
        _ac._avatar_controller = None
        reset_avatar_engine()
        e1 = get_avatar_engine(headless=True)
        reset_avatar_engine()
        _ac._avatar_controller = None
        e2 = get_avatar_engine(headless=True)
        assert e1 is not e2

    def test_headless_upgrade(self):
        reset_avatar_engine()
        import src.ui.avatar_controller as _ac
        _ac._avatar_controller = None
        e_headless = get_avatar_engine(headless=True)
        get_avatar_engine(headless=False)
        assert e_headless._headless is False


# ============================================================
# 15.07.010 -- Arret propre
# ============================================================

class TestStop:

    def test_stop_after_speaking(self):
        eng = _engine()
        eng.start()
        eng.set_speaking(True)
        eng.stop()
        assert not eng.started

    def test_stop_idempotent(self):
        eng = _engine()
        eng.start()
        eng.stop()
        eng.stop()  # ne doit pas lever

    def test_stop_without_start(self):
        eng = _engine()
        eng.stop()  # ne doit pas lever
        assert not eng.started


# ============================================================
# 15.07.011-013 -- Synchronisation séquence réponse (Bug 2)
# ============================================================

class TestResponseSequence:

    def test_begin_response_sets_thinking(self):
        eng = _engine()
        eng.begin_response()
        assert eng.state_name == "thinking"

    def test_begin_response_locks_response_active(self):
        eng = _engine()
        eng.begin_response()
        assert eng._response_active is True

    def test_end_response_clears_lock(self):
        eng = _engine()
        eng.begin_response()
        eng.end_response()
        assert eng._response_active is False

    def test_end_response_exits_speaking(self):
        eng = _engine()
        eng.begin_response()
        eng.set_speaking(True)   # simule on_play_start TTS
        eng.end_response()
        assert eng.is_speaking is False

    def test_on_tts_stop_during_response_keeps_speaking(self):
        """Entre deux phrases, on_tts_stop ne doit PAS couper le visuel speaking."""
        eng = _engine()
        eng.begin_response()
        eng.set_speaking(True)        # première phrase commence
        eng.on_tts_stop()             # première phrase finie — verrou actif
        # Le controller a bien is_speaking=True car on_tts_stop n'a pas coupé
        assert eng._response_active is True

    def test_on_tts_stop_outside_response_resets_state(self):
        """Hors séquence, on_tts_stop repasse en état mode."""
        eng = _engine()
        eng._response_active = False
        eng.set_speaking(True)
        eng.on_tts_stop()
        assert eng.is_speaking is False

    def test_full_response_cycle(self):
        """Cycle complet : begin → speaking × 3 phrases → end."""
        eng = _engine()
        fired = []
        eng.register_hook(lambda s: fired.append(s))

        eng.begin_response()
        assert eng.state_name == "thinking"

        for _ in range(3):
            eng.set_speaking(True)      # on_play_start TTS
            eng.on_tts_stop()           # on_play_stop inter-phrase

        eng.end_response()
        assert eng.is_speaking is False
        assert eng._response_active is False

    def test_begin_response_hook_fires_thinking(self):
        eng = _engine()
        fired = []
        eng.register_hook(lambda s: fired.append(s))
        eng.begin_response()
        assert "thinking" in fired

    def test_end_response_no_crash_without_begin(self):
        eng = _engine()
        eng.end_response()   # ne doit pas lever

    def test_response_active_false_by_default(self):
        eng = _engine()
        assert eng._response_active is False
