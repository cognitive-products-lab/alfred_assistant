"""
PROJECT      : ALFRED
BLOCK        : B15 -- Avatar & Interface
FUNCTION     : 15.01.001 -> 15.01.008
FILE         : tests/b15_tests/test_avatar_controller.py
ROLE         : Tests unitaires AvatarController -- machine etats, hooks, TTS sync, renderer

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-05-14
UPDATED      : 2026-05-14
VERSION      : V1.0
STATUS       : STABLE

DESCRIPTION :
Tests complets de src/ui/avatar_controller.py.
Aucune dependance graphique -- mode headless.
Couvre : AvatarState, AvatarController (set_state, set_mode, set_speaking,
         set_listening, set_thinking, set_emotion, set_idle, set_error),
         hooks, renderer, historique, get_animation_descriptor, status,
         get_avatar_controller (singleton).
"""

import sys
from pathlib import Path
from unittest.mock import MagicMock

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from src.ui.avatar_controller import (
    AvatarController,
    AvatarState,
    AVATAR_STATES,
    DEFAULT_STATE,
    get_avatar_controller,
)


# ---------------------------------------------------------
# AvatarState dataclass
# ---------------------------------------------------------

class TestAvatarState:

    def test_default_state_idle(self):
        s = AvatarState()
        assert s.state == DEFAULT_STATE

    def test_default_mode_focus(self):
        s = AvatarState()
        assert s.mode == "focus"

    def test_not_speaking_by_default(self):
        s = AvatarState()
        assert s.is_speaking is False

    def test_not_listening_by_default(self):
        s = AvatarState()
        assert s.is_listening is False

    def test_emotion_neutral_by_default(self):
        s = AvatarState()
        assert s.emotion == "neutral"

    def test_has_timestamp(self):
        s = AvatarState()
        assert s.timestamp != ""


# ---------------------------------------------------------
# AVATAR_STATES constant
# ---------------------------------------------------------

class TestAvatarStatesConstant:

    def test_has_required_states(self):
        for s in ("idle", "listening", "thinking", "speaking",
                  "support", "focus", "challenge", "complicite",
                  "error", "offline"):
            assert s in AVATAR_STATES

    def test_each_state_has_description(self):
        for state, desc in AVATAR_STATES.items():
            assert isinstance(desc, str) and len(desc) > 0


# ---------------------------------------------------------
# AvatarController.__init__
# ---------------------------------------------------------

class TestAvatarControllerInit:

    def test_starts_in_idle(self):
        ctrl = AvatarController(headless=True)
        assert ctrl.state_name == DEFAULT_STATE

    def test_headless_default(self):
        ctrl = AvatarController()
        assert ctrl.headless is False

    def test_headless_true(self):
        ctrl = AvatarController(headless=True)
        assert ctrl.headless is True

    def test_not_speaking_initially(self):
        ctrl = AvatarController(headless=True)
        assert ctrl.is_speaking is False

    def test_not_listening_initially(self):
        ctrl = AvatarController(headless=True)
        assert ctrl.is_listening is False

    def test_history_starts_with_idle(self):
        ctrl = AvatarController(headless=True)
        assert len(ctrl.get_history()) >= 1
        assert ctrl.get_history()[0].state == DEFAULT_STATE


# ---------------------------------------------------------
# set_state()
# ---------------------------------------------------------

class TestSetState:

    def test_changes_state(self):
        ctrl = AvatarController(headless=True)
        ctrl.set_state("speaking")
        assert ctrl.state_name == "speaking"

    def test_returns_true_on_change(self):
        ctrl = AvatarController(headless=True)
        assert ctrl.set_state("listening") is True

    def test_returns_false_same_state(self):
        ctrl = AvatarController(headless=True)
        ctrl.set_state("speaking")
        assert ctrl.set_state("speaking") is False

    def test_returns_false_unknown_state(self):
        ctrl = AvatarController(headless=True)
        assert ctrl.set_state("inexistant") is False

    def test_all_valid_states_accepted(self):
        ctrl = AvatarController(headless=True)
        for state in AVATAR_STATES:
            ctrl._current_state.state = "idle"  # reset
            result = ctrl.set_state(state)
            assert result is True or ctrl.state_name == state


# ---------------------------------------------------------
# set_mode()
# ---------------------------------------------------------

class TestSetMode:

    def test_support_mode(self):
        ctrl = AvatarController(headless=True)
        ctrl.set_mode("support")
        assert ctrl.current_state.mode == "support"

    def test_state_follows_mode_when_idle(self):
        ctrl = AvatarController(headless=True)
        ctrl.set_mode("challenge")
        assert ctrl.state_name == "challenge"

    def test_invalid_mode_returns_false(self):
        ctrl = AvatarController(headless=True)
        assert ctrl.set_mode("unknown_mode") is False

    def test_mode_does_not_override_speaking(self):
        ctrl = AvatarController(headless=True)
        ctrl.set_speaking(True)
        ctrl.set_mode("support")
        # En train de parler -> etat reste "speaking"
        assert ctrl.state_name == "speaking"
        assert ctrl.current_state.mode == "support"

    def test_all_valid_modes(self):
        ctrl = AvatarController(headless=True)
        for mode in ("support", "focus", "challenge", "complicite"):
            result = ctrl.set_mode(mode)
            assert result is True


# ---------------------------------------------------------
# set_speaking()
# ---------------------------------------------------------

class TestSetSpeaking:

    def test_speaking_true_sets_state(self):
        ctrl = AvatarController(headless=True)
        ctrl.set_speaking(True)
        assert ctrl.state_name == "speaking"
        assert ctrl.is_speaking is True

    def test_speaking_false_returns_to_mode(self):
        ctrl = AvatarController(headless=True)
        ctrl.set_mode("support")
        ctrl.set_speaking(True)
        ctrl.set_speaking(False)
        assert ctrl.state_name == "support"
        assert ctrl.is_speaking is False

    def test_speaking_false_default_focus(self):
        ctrl = AvatarController(headless=True)
        ctrl.set_speaking(True)
        ctrl.set_speaking(False)
        # Mode par defaut = focus
        assert ctrl.state_name == "focus"


# ---------------------------------------------------------
# set_listening()
# ---------------------------------------------------------

class TestSetListening:

    def test_listening_true_sets_state(self):
        ctrl = AvatarController(headless=True)
        ctrl.set_listening(True)
        assert ctrl.state_name == "listening"
        assert ctrl.is_listening is True

    def test_listening_false_returns_to_mode(self):
        ctrl = AvatarController(headless=True)
        ctrl.set_mode("complicite")
        ctrl.set_listening(True)
        ctrl.set_listening(False)
        assert ctrl.state_name == "complicite"
        assert ctrl.is_listening is False


# ---------------------------------------------------------
# set_thinking()
# ---------------------------------------------------------

class TestSetThinking:

    def test_thinking_sets_state(self):
        ctrl = AvatarController(headless=True)
        ctrl.set_thinking()
        assert ctrl.state_name == "thinking"

    def test_thinking_clears_listening(self):
        ctrl = AvatarController(headless=True)
        ctrl.set_listening(True)
        ctrl.set_thinking()
        assert ctrl.is_listening is False


# ---------------------------------------------------------
# set_emotion()
# ---------------------------------------------------------

class TestSetEmotion:

    def test_updates_emotion(self):
        ctrl = AvatarController(headless=True)
        ctrl.set_emotion("happy")
        assert ctrl.current_state.emotion == "happy"

    def test_emotion_persists(self):
        ctrl = AvatarController(headless=True)
        ctrl.set_emotion("stressed")
        ctrl.set_mode("support")
        assert ctrl.current_state.emotion == "stressed"


# ---------------------------------------------------------
# set_idle() / set_error()
# ---------------------------------------------------------

class TestIdleAndError:

    def test_set_idle(self):
        ctrl = AvatarController(headless=True)
        ctrl.set_speaking(True)
        ctrl.set_idle()
        assert ctrl.state_name == "idle"
        assert ctrl.is_speaking is False
        assert ctrl.is_listening is False

    def test_set_error(self):
        ctrl = AvatarController(headless=True)
        ctrl.set_error("test error")
        assert ctrl.state_name == "error"


# ---------------------------------------------------------
# Hooks
# ---------------------------------------------------------

class TestHooks:

    def test_hook_called_on_state_change(self):
        ctrl = AvatarController(headless=True)
        calls = []
        ctrl.register_hook(lambda s: calls.append(s))
        ctrl.set_state("speaking")
        assert "speaking" in calls

    def test_hook_not_called_same_state(self):
        ctrl = AvatarController(headless=True)
        calls = []
        ctrl.register_hook(lambda s: calls.append(s))
        ctrl.set_state("idle")  # deja idle
        assert len(calls) == 0

    def test_multiple_hooks_all_called(self):
        ctrl = AvatarController(headless=True)
        r1, r2 = [], []
        ctrl.register_hook(lambda s: r1.append(s))
        ctrl.register_hook(lambda s: r2.append(s))
        ctrl.set_state("listening")
        assert len(r1) == 1
        assert len(r2) == 1

    def test_hook_exception_does_not_crash(self):
        ctrl = AvatarController(headless=True)
        def bad_hook(s):
            raise RuntimeError("hook error")
        ctrl.register_hook(bad_hook)
        ctrl.set_state("speaking")  # ne doit pas lever
        assert ctrl.state_name == "speaking"


# ---------------------------------------------------------
# Renderer
# ---------------------------------------------------------

class TestRenderer:

    def test_renderer_connected(self):
        ctrl = AvatarController(headless=False)
        renderer = MagicMock()
        ctrl.set_renderer(renderer)
        assert ctrl.status()["has_renderer"] is True

    def test_renderer_update_state_called(self):
        ctrl = AvatarController(headless=False)
        renderer = MagicMock()
        ctrl.set_renderer(renderer)
        ctrl.set_state("speaking")
        renderer.update_state.assert_called_once_with("speaking")

    def test_renderer_not_called_in_headless(self):
        ctrl = AvatarController(headless=True)
        renderer = MagicMock()
        ctrl.set_renderer(renderer)
        ctrl.set_state("speaking")
        renderer.update_state.assert_not_called()


# ---------------------------------------------------------
# Historique
# ---------------------------------------------------------

class TestHistory:

    def test_history_grows_on_transitions(self):
        ctrl = AvatarController(headless=True)
        initial_count = len(ctrl.get_history())
        ctrl.set_state("listening")
        ctrl.set_state("thinking")
        ctrl.set_state("speaking")
        assert len(ctrl.get_history()) == initial_count + 3

    def test_get_history_n(self):
        ctrl = AvatarController(headless=True)
        ctrl.set_state("listening")
        ctrl.set_state("thinking")
        ctrl.set_state("speaking")
        assert len(ctrl.get_history(2)) == 2

    def test_clear_history(self):
        ctrl = AvatarController(headless=True)
        ctrl.set_state("listening")
        ctrl.clear_history()
        assert ctrl.get_history() == []


# ---------------------------------------------------------
# get_animation_descriptor()
# ---------------------------------------------------------

class TestAnimationDescriptor:

    def test_returns_dict(self):
        ctrl = AvatarController(headless=True)
        desc = ctrl.get_animation_descriptor("idle")
        assert isinstance(desc, dict)

    def test_required_keys(self):
        ctrl = AvatarController(headless=True)
        desc = ctrl.get_animation_descriptor("speaking")
        for k in ("color", "animation", "intensity", "state", "description"):
            assert k in desc

    def test_state_field_matches(self):
        ctrl = AvatarController(headless=True)
        desc = ctrl.get_animation_descriptor("support")
        assert desc["state"] == "support"

    def test_current_state_used_when_no_arg(self):
        ctrl = AvatarController(headless=True)
        ctrl.set_state("listening")
        desc = ctrl.get_animation_descriptor()
        assert desc["state"] == "listening"

    def test_all_states_have_descriptor(self):
        ctrl = AvatarController(headless=True)
        for state in AVATAR_STATES:
            desc = ctrl.get_animation_descriptor(state)
            assert desc["color"] != ""


# ---------------------------------------------------------
# status()
# ---------------------------------------------------------

class TestStatus:

    def test_returns_dict(self):
        ctrl = AvatarController(headless=True)
        assert isinstance(ctrl.status(), dict)

    def test_required_keys(self):
        ctrl = AvatarController(headless=True)
        s = ctrl.status()
        for k in ("current_state", "mode", "is_speaking", "is_listening",
                  "emotion", "headless", "hooks_count", "has_renderer",
                  "history_count", "version"):
            assert k in s

    def test_headless_reflected(self):
        ctrl = AvatarController(headless=True)
        assert ctrl.status()["headless"] is True

    def test_hooks_count_updates(self):
        ctrl = AvatarController(headless=True)
        ctrl.register_hook(lambda s: None)
        ctrl.register_hook(lambda s: None)
        assert ctrl.status()["hooks_count"] == 2


# ---------------------------------------------------------
# get_avatar_controller() singleton
# ---------------------------------------------------------

class TestSingleton:

    def test_returns_avatar_controller(self):
        import src.ui.avatar_controller as ac
        ac._avatar_controller = None
        ctrl = get_avatar_controller(headless=True)
        assert isinstance(ctrl, AvatarController)

    def test_same_instance_returned(self):
        import src.ui.avatar_controller as ac
        ac._avatar_controller = None
        ctrl1 = get_avatar_controller(headless=True)
        ctrl2 = get_avatar_controller(headless=True)
        assert ctrl1 is ctrl2
