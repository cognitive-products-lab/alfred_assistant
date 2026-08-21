"""
PROJECT      : ALFRED
BLOCK        : B15 -- Avatar & Interface
FILE         : tests/b15_tests/test_ui_bridge.py
ROLE         : Tests unitaires ui_bridge -- queue thread-safe UI<->pipeline

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-05-15
VERSION      : V1.0
STATUS       : STABLE

DESCRIPTION :
Tests de ui_bridge sans dependance Kivy.
Couvre : activate/deactivate, send/receive, callbacks, drain, statut.
"""

import sys
import threading
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import src.ui.ui_bridge as bridge


def _reset_bridge() -> None:
    """Remet le bridge dans son etat initial entre les tests."""
    bridge.deactivate()
    bridge.drain_input_queue()
    bridge._response_cb = None
    bridge._user_msg_cb = None


# ============================================================
# Activate / deactivate
# ============================================================

class TestActivation:
    def test_initially_inactive(self):
        _reset_bridge()
        assert bridge.is_active() is False

    def test_activate(self):
        _reset_bridge()
        bridge.activate()
        assert bridge.is_active() is True

    def test_deactivate(self):
        _reset_bridge()
        bridge.activate()
        bridge.deactivate()
        assert bridge.is_active() is False

    def test_deactivate_unblocks_queue(self):
        """deactivate() pousse "" dans la queue pour debloquer un eventuel wait."""
        _reset_bridge()
        bridge.activate()
        bridge.deactivate()
        val = bridge._input_queue.get_nowait()
        assert val == ("", "local")


# ============================================================
# send_user_input / wait_for_ui_input
# ============================================================

class TestInputQueue:
    def test_send_and_receive(self):
        _reset_bridge()
        bridge.send_user_input("Bonjour ALFRED")
        received = bridge._input_queue.get_nowait()
        assert received == ("Bonjour ALFRED", "local")

    def test_send_strips_whitespace(self):
        _reset_bridge()
        bridge.send_user_input("  hello  ")
        received = bridge._input_queue.get_nowait()
        assert received == ("hello", "local")

    def test_send_empty_ignored(self):
        _reset_bridge()
        bridge.drain_input_queue()
        bridge.send_user_input("   ")
        assert bridge._input_queue.empty()

    def test_multiple_messages_fifo(self):
        _reset_bridge()
        for msg in ["un", "deux", "trois"]:
            bridge.send_user_input(msg)
        results = []
        while not bridge._input_queue.empty():
            results.append(bridge._input_queue.get_nowait())
        assert results == [("un", "local"), ("deux", "local"), ("trois", "local")]

    def test_wait_for_ui_input_blocking(self):
        """wait_for_ui_input() bloque jusqu'a reception."""
        _reset_bridge()

        def _producer():
            import time; time.sleep(0.05)
            bridge.send_user_input("message async")

        t = threading.Thread(target=_producer, daemon=True)
        t.start()
        result = bridge.wait_for_ui_input()
        t.join(timeout=1.0)
        assert result == ("message async", "local")


# ============================================================
# drain_input_queue
# ============================================================

class TestDrain:
    def test_drain_empty(self):
        _reset_bridge()
        bridge.drain_input_queue()   # ne doit pas lever d'exception
        assert bridge._input_queue.empty()

    def test_drain_clears_queue(self):
        _reset_bridge()
        for _ in range(5):
            bridge._input_queue.put("test")
        bridge.drain_input_queue()
        assert bridge._input_queue.empty()


# ============================================================
# Callbacks
# ============================================================

class TestCallbacks:
    def test_user_message_callback_fired(self):
        _reset_bridge()
        received: list[str] = []
        bridge.set_user_message_callback(received.append)
        bridge.send_user_input("coucou")
        assert "coucou" in received

    def test_response_callback_via_notify(self):
        _reset_bridge()
        received: list[str] = []
        bridge.set_response_callback(received.append)
        bridge.notify_response("Bonjour !")
        assert "Bonjour !" in received

    def test_no_callback_no_error(self):
        _reset_bridge()
        bridge.notify_response("sans callback")   # ne doit pas lever


# ============================================================
# Status
# ============================================================

class TestStatus:
    def test_status_keys(self):
        _reset_bridge()
        s = bridge.status()
        assert "ui_active" in s
        assert "queue_size" in s
        assert "has_resp_cb" in s
        assert "has_msg_cb" in s

    def test_status_reflects_state(self):
        _reset_bridge()
        bridge.activate()
        bridge.send_user_input("x")
        s = bridge.status()
        assert s["ui_active"] is True
        assert s["queue_size"] == 1
        _reset_bridge()


# ============================================================
# Thread safety
# ============================================================

class TestThreadSafety:
    def test_concurrent_sends(self):
        _reset_bridge()
        N = 50
        errors: list[Exception] = []

        def _send(i: int):
            try:
                bridge.send_user_input(f"msg{i}")
            except Exception as e:
                errors.append(e)

        threads = [threading.Thread(target=_send, args=(i,)) for i in range(N)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert not errors
        assert bridge._input_queue.qsize() == N
        _reset_bridge()
