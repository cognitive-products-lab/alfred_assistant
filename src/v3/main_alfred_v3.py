# -*- coding: utf-8 -*-
"""
main_alfred_v3.py — ALFRED V3 — Point d'entrée orchestrateur

Remplace le pipeline manuel de main.py par AlfredOrchestrator.
Avatar/TTS non branché — pipeline texte uniquement.

Usage :
    python -m src.v3.main_alfred_v3
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.v3.orchestrator import AlfredOrchestrator

# ── Chemins ───────────────────────────────────────────────
PERSONALITY_PATH = str(
    ROOT / "data" / "personality" / "instances" / "personality_core_instance.json"
)
USER_PROFILE_PATH = str(
    ROOT / "data" / "users" / "instances" / "user_celine_instance.json"
)
MEMORY_PATH = str(
    ROOT / "data" / "memory" / "episodic" / "dialogue_history.json"
)

# ── Commandes intégrées ───────────────────────────────────
COMMANDS = {
    "exit": lambda orch: ("exit", None),
    "quit": lambda orch: ("exit", None),
    "statut": lambda orch: ("print", _format_status(orch.get_status())),
    "reset": lambda orch: ("reset", None),
    "mode support": lambda orch: ("mode", "support"),
    "mode focus": lambda orch: ("mode", "focus"),
    "mode challenge": lambda orch: ("mode", "challenge"),
    "mode complicite": lambda orch: ("mode", "complicite"),
}


def _format_status(status: dict) -> str:
    session = status.get("session", {})
    modules = status.get("modules", {})
    rag = status.get("rag", {})
    lines = [
        f"── Session {session.get('session_id')} — Tour {session.get('turn_count')} ──",
        f"Mode : {session.get('current_mode')} | Émotion : {session.get('current_emotion')}",
        f"Wellbeing : {session.get('wellbeing_energy')}",
        "",
        "Modules chargés :",
    ]
    for k, v in modules.items():
        lines.append(f"  {'✓' if v else '✗'} {k}")
    mem_status = rag.get("memory", {})
    lines.append(
        f"\nRAG : {mem_status.get('backend', '?')} — "
        f"{mem_status.get('count', 0)} documents indexés"
    )
    return "\n".join(lines)


def run() -> None:
    print("\n" + "=" * 50)
    print("  ALFRED V3 — Orchestrateur cognitif adaptatif")
    print("  'exit' pour quitter | 'statut' pour l'état")
    print("=" * 50 + "\n")

    orch = AlfredOrchestrator(
        personality_path=PERSONALITY_PATH,
        user_profile_path=USER_PROFILE_PATH,
        memory_path=MEMORY_PATH,
        debug=False,
    )

    status = orch.get_status()
    loaded = sum(1 for v in status["modules"].values() if v)
    total = len(status["modules"])
    print(f"[Init] {loaded}/{total} modules chargés — session {status['session']['session_id']}\n")

    while True:
        try:
            user_input = input("Vous : ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nAu revoir.")
            break

        if not user_input:
            continue

        cmd = COMMANDS.get(user_input.lower())
        if cmd:
            action, payload = cmd(orch)
            if action == "exit":
                print("ALFRED : À bientôt.")
                break
            elif action == "print":
                print(payload)
            elif action == "reset":
                orch.reset_session()
                print("[Session réinitialisée]")
            elif action == "mode":
                orch.set_mode(payload)
                print(f"[Mode → {payload}]")
            continue

        resp = orch.process(user_input)

        prefix = ""
        if resp.blocked:
            prefix = "[PROTÉGÉ] "
        elif resp.fallback:
            prefix = "[hors ligne] "

        print(f"\nALFRED : {prefix}{resp.text}\n")


if __name__ == "__main__":
    run()
