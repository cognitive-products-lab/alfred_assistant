# -*- coding: utf-8 -*-
"""
state_manager.py — ALFRED V3
État de session persistant sur la durée d'une conversation.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict


@dataclass
class SessionState:
    session_id: str
    turn_count: int = 0
    current_mode: str = "focus"
    current_emotion: str = "neutral"
    emotion_intensity: float = 0.0
    wellbeing_energy: str = "normal"
    last_intent: str = "general_discussion"
    context: Dict[str, Any] = field(default_factory=dict)
    active_since: str = field(default_factory=lambda: datetime.now().isoformat())

    def increment_turn(self) -> None:
        self.turn_count += 1

    def update_emotion(self, emotion: str, intensity: float) -> None:
        self.current_emotion = emotion
        self.emotion_intensity = intensity

    def update_mode(self, mode: str) -> None:
        self.current_mode = mode

    def set(self, key: str, value: Any) -> None:
        self.context[key] = value

    def get(self, key: str, default: Any = None) -> Any:
        return self.context.get(key, default)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "session_id": self.session_id,
            "turn_count": self.turn_count,
            "current_mode": self.current_mode,
            "current_emotion": self.current_emotion,
            "emotion_intensity": self.emotion_intensity,
            "wellbeing_energy": self.wellbeing_energy,
            "last_intent": self.last_intent,
            "active_since": self.active_since,
        }
