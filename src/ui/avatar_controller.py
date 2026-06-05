"""
PROJECT      : ALFRED
BLOCK        : B15
FUNCTION     : 15.04
FILE         : src/ui/avatar_controller.py
ROLE         : Définition des états avatar ALFRED

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-06-05
UPDATED      : 2026-06-05
VERSION      : V1.0
STATUS       : TESTED

DESCRIPTION :
Référentiel des états avatar (idle, listening, thinking, speaking, error).
"""

"""Stub avatar_controller — états avatar ALFRED."""

AVATAR_STATES: dict[str, str] = {
    "idle":      "assets/avatar/idle.png",
    "listening": "assets/avatar/listening.png",
    "thinking":  "assets/avatar/thinking.png",
    "speaking":  "assets/avatar/speaking.png",
    "error":     "assets/avatar/error.png",
}
