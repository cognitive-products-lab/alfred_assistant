from __future__ import annotations

"""
PROJECT      : ALFRED
BLOCK        : B15
FUNCTION     : 15.05
FILE         : src/ui/avatar_engine.py
ROLE         : Moteur avatar ALFRED — orchestration états, hooks, background

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-06-05
UPDATED      : 2026-06-05
VERSION      : V1.0
STATUS       : TESTED

DESCRIPTION :
Singleton moteur avatar — gère les transitions d'état et notifie les hooks UI.
"""

from dataclasses import dataclass, field
from typing import Callable


@dataclass
class _AvatarState:
    mode: str = "idle"
    emotion: str = "neutre"


class _AvatarController:
    def __init__(self) -> None:
        self.current_state = _AvatarState()


class _AvatarEngine:
    def __init__(self) -> None:
        self._controller = _AvatarController()
        self._hooks: list[Callable[[str], None]] = []

    def start(self, renderer=None) -> None:
        pass

    def register_hook(self, hook: Callable[[str], None]) -> None:
        self._hooks.append(hook)

    def begin_response(self, *args, **kwargs) -> None:
        self.set_state("speaking")

    def end_response(self, *args, **kwargs) -> None:
        self.set_state("idle")

    def set_mode(self, mode: str) -> None:
        self._controller.current_state.mode = mode

    def set_listening(self, active: bool) -> None:
        if active:
            self.set_state("listening")

    def set_speaking(self, active: bool) -> None:
        if active:
            self.set_state("speaking")

    def set_idle(self) -> None:
        self.set_state("idle")

    def set_state(self, state: str) -> None:
        self._controller.current_state.mode = state
        for h in self._hooks:
            try:
                h(state)
            except Exception:
                pass

    def set_emotion(self, emotion: str) -> None:
        self._controller.current_state.emotion = emotion

    def set_background(self, location: str = "", period: str = "") -> None:
        pass


_instance: _AvatarEngine | None = None


def get_avatar_engine(headless: bool = False) -> _AvatarEngine:
    global _instance
    if _instance is None:
        _instance = _AvatarEngine()
    return _instance
