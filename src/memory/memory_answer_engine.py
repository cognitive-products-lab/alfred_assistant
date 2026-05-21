# -*- coding: utf-8 -*-
"""
memory_answer_engine.py — ALFRED
Réponses déterministes basées sur la mémoire.
"""

from __future__ import annotations

import re
from typing import Optional


CURRENT_WORK_PATTERNS = [
    r"sur quoi je travaille",
    r"sur quoi suis-je en train de travailler",
    r"sur quoi est-ce que je travaille",
    r"que fais-je actuellement",
    r"qu['’]est-ce que je fais actuellement",
    r"tu sais sur quoi je travaille",
    r"mon travail actuel",
    r"ce que je fais en ce moment",
    r"sur quoi je travail",
    r"sur quoi je travaille",
    r"sur quoi est ce que je travail",
    r"sur quoi est-ce que je travaille",
    r"sur quoi je bosse",
    r"ce que je travaille actuellement",
]


def answer_from_memory(user_message: str, memory_context: str) -> Optional[str]:
    msg = normalize(user_message)

    if is_current_work_question(msg):
        return answer_current_work(memory_context)

    return None


def normalize(text: str) -> str:
    return text.lower().strip()


def is_current_work_question(msg: str) -> bool:
    return any(re.search(pattern, msg) for pattern in CURRENT_WORK_PATTERNS)


def answer_current_work(memory_context: str) -> str:
    if not memory_context or not memory_context.strip():
        return "Je n’ai pas encore d’information fiable en mémoire sur ton travail actuel."

    lines = memory_context.splitlines()

    priority_markers = [
        "je travaille actuellement sur",
        "je travaille sur",
        "on travaille sur",
        "nous travaillons sur",
        "création",
        "creation",
        "corriger",
        "améliorer",
        "ameliorer",
        "brancher",
        "intégrer",
        "integrer",
        "llm",
        "ollama",
        "openai",
        "mémoire",
        "memoire",
        "alfred",
        "mode vocal",
        "memory_answer_engine",
    ]

    candidates: list[str] = []

    for line in lines:
        clean = line.strip()
        lower = clean.lower()

        if not clean:
            continue

        if "céline :" in lower or "toi :" in lower:
            if any(marker in lower for marker in priority_markers):
                candidates.append(clean)

    if not candidates:
        return (
            "Je vois de la mémoire récente, mais aucun élément assez fiable pour dire "
            "précisément sur quoi tu travailles actuellement."
        )

    last = candidates[-1]
    last = re.sub(r"^- \[[^\]]+\]\s*", "", last)
    last = last.replace("Céline :", "").replace("Toi :", "").strip()

    return (
        "Tu travailles actuellement sur :\n\n"
        f"👉 {last}\n\n"
        "Je m’appuie ici sur la mémoire récente, pas sur une supposition."
    )
