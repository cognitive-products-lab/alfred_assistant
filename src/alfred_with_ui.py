"""
PROJECT      : ALFRED
BLOCK        : GLOBAL
FILE         : src/alfred_with_ui.py
ROLE         : Point d'entree ALFRED avec interface graphique Kivy

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-05-14
UPDATED      : 2026-06-01
VERSION      : V1.2
STATUS       : STABLE

DESCRIPTION :
Lance ALFRED avec l'interface graphique Kivy en parallele du pipeline
conversationnel texte.

Architecture :
  Thread principal  -> AlfredApp Kivy (obligatoire sur Windows/macOS)
  Thread daemon     -> pipeline conversationnel main.main()
  Bridge            -> ui_bridge (queue thread-safe UI <-> pipeline)

Auto-restart :
  Le pipeline relance automatiquement en cas de crash (max 5 tentatives).
  Utile quand le contexte LLM est plein ou quand Ollama est recharge.

Communication pipeline -> UI :
  AvatarController singleton (partagé) :
    avatar.set_thinking()   -> renderer.update_state("thinking")  via Clock
    avatar.set_speaking()   -> renderer.update_state("speaking")  via Clock
    avatar.set_listening()  -> renderer.update_state("listening") via Clock
  set_ui_response(text)     -> ConversationBox.add_alfred_message() via Clock
  stream_ui_phrase(phrase)  -> ConversationBox.append_stream_phrase() via Clock
  set_ui_thinking(bool)     -> message réflexion personnalisé via Clock
  set_ui_input_enabled(bool)-> InputRow.set_enabled() via Clock
  set_ui_speaking(bool)     -> SoundWaveWidget.set_speaking() via Clock
  set_ui_listening(bool)    -> SoundWaveWidget.set_listening() via Clock

Usage :
  python src/alfred_with_ui.py

Le champ TextInput dans la fenêtre Kivy remplace la saisie terminal.
La fenêtre Kivy affiche l'avatar, la conversation et les contrôles.
"""

from __future__ import annotations

import sys
import threading
import time
from pathlib import Path

# ── Fix encodage console Windows ──────────────────────────────────────────────
# reconfigure() modifie l'encoding de l'objet TextIOWrapper existant sans
# fermer le buffer sous-jacent (contrairement à io.TextIOWrapper).
# Nécessaire sur Windows où cp1252 est le codec par défaut → crash sur emojis.
if sys.platform == "win32":
    for _stream in (sys.stdout, sys.stderr):
        if hasattr(_stream, "reconfigure"):
            try:
                _stream.reconfigure(encoding="utf-8", errors="replace")
            except Exception:
                pass

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# ============================================================
# Pipeline avec auto-restart
# ============================================================

_MAX_RESTARTS  = 5
_RESTART_DELAY = 3.0    # secondes entre les tentatives


def _run_pipeline() -> None:
    """
    Lance le pipeline ALFRED en boucle avec auto-restart.
    Relance en cas de crash (contexte LLM plein, Ollama reload, etc.).
    S'arrete proprement si l'utilisateur quitte (SystemExit) ou
    si le nombre de redemarrages maximum est atteint.
    """
    attempt = 0
    while attempt < _MAX_RESTARTS:
        attempt += 1
        try:
            from src.main import main
            main()
            # main() termine normalement (exit/quit de l'utilisateur)
            print("\n  [ALFRED] Pipeline terminé normalement.")
            break

        except SystemExit:
            print("\n  [ALFRED] Arrêt demandé.")
            break

        except Exception as exc:
            if attempt < _MAX_RESTARTS:
                print(
                    f"\n  [ALFRED] Incident pipeline (tentative {attempt}/{_MAX_RESTARTS}) : {exc}"
                    f"\n  [ALFRED] Redémarrage dans {_RESTART_DELAY:.0f}s..."
                )
                try:
                    from src.ui.alfred_app import set_ui_response
                    set_ui_response(
                        f"⚠️ ALFRED redémarre ({attempt}/{_MAX_RESTARTS})... "
                        "un instant."
                    )
                except Exception:
                    pass
                time.sleep(_RESTART_DELAY)
            else:
                print(
                    f"\n  [ALFRED] Erreur fatale après {_MAX_RESTARTS} tentatives : {exc}"
                )
                try:
                    from src.ui.alfred_app import set_ui_response
                    set_ui_response(
                        "❌ ALFRED a rencontré un problème critique. "
                        "Relance l'application."
                    )
                except Exception:
                    pass


# ============================================================
# Point d'entrée
# ============================================================

if __name__ == "__main__":
    # ── Workaround Kivy ZeroDivisionError sur Windows multi-écrans ───────────
    # win._density peut tomber à 0 quand la fenêtre passe sur un 2e écran
    # (bug sdl2 + Windows DPI scaling). Forcer density=1 évite le crash.
    import os as _os
    _os.environ.setdefault("KIVY_METRICS_DENSITY", "1")

    # Activer le bridge UI <-> pipeline avant tout
    from src.ui.ui_bridge import activate as _bridge_activate
    _bridge_activate()

    # Pipeline en thread daemon (auto-restart integre)
    pipeline_thread = threading.Thread(
        target=_run_pipeline,
        name="alfred-pipeline",
        daemon=True,
    )
    pipeline_thread.start()

    # Interface Kivy dans le thread principal (obligatoire sur Windows/macOS)
    from src.ui.alfred_app import AlfredApp
    AlfredApp(demo_mode=False, location="salon").run()
