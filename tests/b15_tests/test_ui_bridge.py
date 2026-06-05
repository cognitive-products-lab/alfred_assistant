"""
PROJECT      : ALFRED
BLOCK        : B15
FUNCTION     : 15.06
FILE         : tests/b15_tests/test_ui_bridge.py
ROLE         : Tests unitaires src/ui/ui_bridge.py

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-06-05
UPDATED      : 2026-06-05
VERSION      : V1.0
STATUS       : TESTED
"""

import threading
import pytest
from src.ui.ui_bridge import activate, is_active, send_user_input, wait_for_ui_input
import src.ui.ui_bridge as _bridge


@pytest.fixture(autouse=True)
def reset_bridge():
    """Réinitialise l'état du bridge avant chaque test."""
    import importlib
    importlib.reload(_bridge)
    yield


def test_inactive_by_default():
    assert _bridge.is_active() is False


def test_activate():
    _bridge.activate()
    assert _bridge.is_active() is True


def test_send_and_receive():
    _bridge.activate()
    _bridge.send_user_input("bonjour alfred")
    result = _bridge.wait_for_ui_input(timeout=1.0)
    assert result == "bonjour alfred"


def test_multiple_messages_fifo():
    _bridge.activate()
    for msg in ["un", "deux", "trois"]:
        _bridge.send_user_input(msg)
    assert _bridge.wait_for_ui_input(timeout=1.0) == "un"
    assert _bridge.wait_for_ui_input(timeout=1.0) == "deux"
    assert _bridge.wait_for_ui_input(timeout=1.0) == "trois"


def test_wait_timeout_raises():
    _bridge.activate()
    import queue
    with pytest.raises(queue.Empty):
        _bridge.wait_for_ui_input(timeout=0.1)


def test_thread_safe_send():
    """Plusieurs threads envoient en parallèle — aucun message perdu."""
    _bridge.activate()
    n = 20
    threads = [threading.Thread(target=_bridge.send_user_input, args=(f"msg{i}",)) for i in range(n)]
    for t in threads: t.start()
    for t in threads: t.join()
    received = []
    for _ in range(n):
        received.append(_bridge.wait_for_ui_input(timeout=1.0))
    assert len(received) == n
