"""
PROJECT      : ALFRED
BLOCK        : GLOBAL
FILE         : src/alfred_desktop.py
ROLE         : Point d'entree ALFRED avec l'interface desktop HTML (pywebview)

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-07-18
UPDATED      : 2026-07-18
VERSION      : V1.1
STATUS       : DRAFT — mode texte + réglages branchés, reste à câbler (voix, données)

DESCRIPTION :
Remplace src/alfred_with_ui.py (interface Kivy) par la nouvelle interface
HTML/CSS/JS (tableau de bord + mode vocal avec avatar) affichee dans une
fenetre native via pywebview.

Branché en V1.1 :
  - Mode texte (page Mode vocal -> "Passer en mode texte") envoie réellement
    les messages au pipeline ALFRED via ui_bridge.send_user_input(), et
    affiche les vraies réponses (avec streaming phrase par phrase), via un
    pont JS<->Python pywebview (js_api côté JS, window.evaluate_js côté
    Python). Le bridge remplace dynamiquement (monkeypatch) les hooks
    set_ui_response / set_ui_thinking / set_ui_input_enabled / stream_ui_phrase
    de src/ui/alfred_app.py — ils sont conçus pour être no-op sans app Kivy
    active, donc ce remplacement est sans risque pour l'ancien point d'entrée
    Kivy (alfred_with_ui.py) qui continue de fonctionner normalement.
  - Réglages d'apparence/accessibilité (thème, taille de texte, contraste,
    animations, sous-titres, police dyslexie) sont persistés dans
    data/settings/desktop_ui_prefs.json (src/ui/desktop_prefs.py) et
    restaurés au démarrage.

Pas encore branché (prochaines étapes) :
  - Tableau de bord (tâches, agenda, mémoire, appareils) reste sur données
    de démonstration statiques.
  - Mode vocal (micro réel, TTS réel, avatar synchronisé) reste simulé —
    seul le mode texte parle au vrai pipeline pour l'instant.

L'ancien point d'entree Kivy (src/alfred_with_ui.py) reste present et
fonctionnel pour revenir en arriere si besoin — il n'est plus appele par
start_alfred.bat mais peut toujours etre lance directement.

Usage :
  python src/alfred_desktop.py
"""

from __future__ import annotations

import json
import sys
import threading
import time
from pathlib import Path

# ── Fix encodage console Windows ──────────────────────────────────────────────
# reconfigure() modifie l'encoding de l'objet TextIOWrapper existant sans
# fermer le buffer sous-jacent (contrairement a io.TextIOWrapper).
# Necessaire sur Windows ou cp1252 est le codec par defaut → crash sur emojis.
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

UI_HTML_PATH = ROOT / "interface" / "desktop_ui" / "index.html"

_window = None  # référence pywebview, remplie après create_window()


# ============================================================
# Pont Python -> JS  (pousse les évènements pipeline dans la page)
# ============================================================

def _push(js_call: str, *args) -> None:
    """Appelle window.__alfredBridge.<js_call>(...args) dans la page, si prête."""
    if _window is None:
        return
    payload = ", ".join(json.dumps(a) for a in args)
    try:
        _window.evaluate_js(
            f"window.__alfredBridge && window.__alfredBridge.{js_call}({payload})"
        )
    except Exception:
        pass  # page pas encore chargée, ou fenêtre fermée


def _on_response(text: str) -> None:
    _push("onResponse", text)


def _on_thinking(thinking: bool = True) -> None:
    _push("onThinking", thinking)


def _on_input_enabled(enabled: bool) -> None:
    _push("onInputEnabled", enabled)


def _on_stream_phrase(phrase: str) -> None:
    _push("onStreamPhrase", phrase)


def _install_bridge_hooks() -> None:
    """
    Remplace les hooks pipeline->UI de src.ui.alfred_app par nos versions
    pywebview. main.py fait `from src.ui.alfred_app import set_ui_response`
    à chaque appel (pas au niveau module), donc ce monkeypatch est pris en
    compte tant qu'il est fait avant le démarrage du thread pipeline.
    """
    import src.ui.alfred_app as _alfred_app_module
    _alfred_app_module.set_ui_response = _on_response
    _alfred_app_module.set_ui_thinking = _on_thinking
    _alfred_app_module.set_ui_input_enabled = _on_input_enabled
    _alfred_app_module.stream_ui_phrase = _on_stream_phrase


# ============================================================
# Pont JS -> Python  (API exposée à window.pywebview.api)
# ============================================================

class AlfredDesktopAPI:
    def send_message(self, text: str) -> dict:
        """Appelé depuis le mode texte : transmet le message au pipeline ALFRED."""
        from src.ui.ui_bridge import send_user_input
        send_user_input(text or "")
        return {"ok": True}

    def get_settings(self) -> dict:
        """Réglages persistés, lus au chargement de la page."""
        from src.ui.desktop_prefs import load_desktop_prefs
        return load_desktop_prefs()

    def save_setting(self, key: str, value) -> dict:
        """Persiste un réglage d'apparence/accessibilité modifié côté UI."""
        from src.ui.desktop_prefs import save_desktop_pref
        return save_desktop_pref(key, value)


# ============================================================
# Pipeline avec auto-restart (identique a alfred_with_ui.py)
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
                _on_response(f"⚠️ ALFRED redémarre ({attempt}/{_MAX_RESTARTS})... un instant.")
                time.sleep(_RESTART_DELAY)
            else:
                print(
                    f"\n  [ALFRED] Erreur fatale après {_MAX_RESTARTS} tentatives : {exc}"
                )
                _on_response("❌ ALFRED a rencontré un problème critique. Relance l'application.")


# ============================================================
# Point d'entrée
# ============================================================

if __name__ == "__main__":
    # ── Authentification via popup tkinter (avant la fenêtre desktop) ────────
    from src.auth.authenticator import has_pin, register_pin, authenticate
    import src.main as _main_mod
    from src.ui.pin_dialog import show_auth_dialog, show_register_dialog

    if has_pin("celine"):
        _ok = show_auth_dialog("celine", authenticate)
    else:
        _ok = show_register_dialog("celine", register_pin)

    if not _ok:
        sys.exit(1)

    _main_mod._AUTH_DONE = True   # évite double auth dans le thread pipeline

    # Branche nos hooks avant de démarrer quoi que ce soit qui pourrait y appeler
    _install_bridge_hooks()

    # Signale au pipeline qu'une UI est active : main.py lira désormais les
    # messages via ui_bridge.wait_for_ui_input() (mode texte) au lieu de
    # input() console.
    from src.ui.ui_bridge import activate as _bridge_activate
    _bridge_activate()

    # Régénère la knowledge map en arrière-plan (non bloquant)
    try:
        from tools.startup_refresh import refresh_knowledge_dashboard_async
        refresh_knowledge_dashboard_async()
    except Exception:
        pass

    # Pipeline en thread daemon (auto-restart intégré)
    pipeline_thread = threading.Thread(
        target=_run_pipeline,
        name="alfred-pipeline",
        daemon=True,
    )
    pipeline_thread.start()

    # Fenêtre desktop HTML dans le thread principal (obligatoire sur Windows/macOS)
    if not UI_HTML_PATH.exists():
        print(f"  [ALFRED] Interface introuvable : {UI_HTML_PATH}")
        sys.exit(1)

    import webview

    _window = webview.create_window(
        "ALFRED",
        url=UI_HTML_PATH.as_uri(),
        js_api=AlfredDesktopAPI(),
        width=1440,
        height=900,
        min_size=(1100, 700),
        background_color="#0A0B16",
    )
    webview.start()
