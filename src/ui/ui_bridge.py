"""
PROJECT      : ALFRED
BLOCK        : B15
FUNCTION     : 15.06
FILE         : src/ui/ui_bridge.py
ROLE         : Bridge thread-safe UI Kivy <-> pipeline ALFRED

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-06-05
UPDATED      : 2026-06-05
VERSION      : V1.0
STATUS       : TESTED

DESCRIPTION :
Queue thread-safe pour la communication bidirectionnelle UI/pipeline.
"""

"""Bridge thread-safe entre l'UI Kivy et le pipeline ALFRED.

API publique :
  activate()           — initialise la file (appelé avant le démarrage Kivy)
  is_active() -> bool  — True si le bridge est actif
  send_user_input(text) — UI -> pipeline : envoie un message utilisateur
  wait_for_ui_input() -> str — pipeline : bloque jusqu'au prochain message
"""

import queue
import threading

_queue: queue.Queue[str] = queue.Queue()
_active = False
_lock = threading.Lock()


def activate() -> None:
    global _active
    with _lock:
        _active = True


def is_active() -> bool:
    with _lock:
        return _active


def send_user_input(text: str) -> None:
    """Appelé depuis le thread UI pour transmettre l'input au pipeline."""
    _queue.put(text)


def wait_for_ui_input(timeout: float | None = None) -> str:
    """Bloque le thread pipeline jusqu'à réception d'un message UI."""
    return _queue.get(timeout=timeout)
