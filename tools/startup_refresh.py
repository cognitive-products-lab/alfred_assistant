"""
PROJECT  : ALFRED
FILE     : tools/startup_refresh.py
ROLE     : Lance generate_knowledge_dashboard.py dans un thread daemon au démarrage
           d'ALFRED (main.py ou alfred_with_ui.py) — non bloquant, silencieux.

Usage :
    from tools.startup_refresh import refresh_knowledge_dashboard_async
    refresh_knowledge_dashboard_async()

STATUS : TESTED
"""

from __future__ import annotations

import subprocess
import sys
import threading
from pathlib import Path

ALFRED_PC = Path(__file__).resolve().parents[1]
GEN_SCRIPT = ALFRED_PC / "dashboard/dashboard_knowledges_tool/generate_knowledge_dashboard.py"


def _run() -> None:
    if not GEN_SCRIPT.exists():
        return
    try:
        subprocess.run(
            [sys.executable, str(GEN_SCRIPT)],
            cwd=str(ALFRED_PC),
            capture_output=True,
            timeout=60,
        )
    except Exception:
        pass  # silencieux — ne jamais bloquer le démarrage d'ALFRED


def refresh_knowledge_dashboard_async() -> None:
    """Régénère knowledge_dashboard_data.json en arrière-plan sans bloquer ALFRED."""
    t = threading.Thread(target=_run, name="knowledge-refresh", daemon=True)
    t.start()
