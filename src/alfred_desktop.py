"""
PROJECT      : ALFRED
BLOCK        : GLOBAL
FILE         : src/alfred_desktop.py
ROLE         : Point d'entree ALFRED avec l'interface desktop HTML (pywebview)

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-07-18
UPDATED      : 2026-07-23
VERSION      : V1.3
STATUS       : DRAFT — texte + dashboard + mode vocal (micro/TTS) + visèmes phonème-exactes branchés

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

Branché en V1.2 :
  - Tableau de bord branché sur les vraies sources (src/ui/desktop_dashboard_data.py) :
    recommandations (ProactiveEngine), état émotionnel (MultiSignalFusionEngine +
    correction/désactivation persistée dans emotion_override_prefs.py), planning
    (ReminderEngine), appareils connectés (device_settings.py — inventaire local
    réel uniquement, pas d'appareils réseau fictifs), activité récente
    (episodic_memory.py, alimentée par un nouvel appel record_episode() par
    échange dans main.py).
  - Mode vocal : micro push-to-talk réel (src/ui/desktop_mic.py, reprend le
    pattern sd.InputStream + _transcribe_audio déjà utilisé par alfred_app.py),
    le texte transcrit passe par le même send_message()/ui_bridge que le mode
    texte. États écoute/parole synchronisés sur les vrais évènements TTS
    (set_ui_speaking/set_ui_listening, désormais monkeypatchés eux aussi) au
    lieu d'un minuteur factice.

Branché en V1.3 :
  - Synchronisation labiale phonème-exacte (V00-V14) : PiperTTS.speak() est
    passé du CLI piper.exe (sous-processus) à l'API Python de Piper
    (voice.synthesize_wav(..., include_alignments=True)), qui donne les
    timings réels par phonème sans synthèse double. src/conversation/output/
    phoneme_viseme_map.py convertit la séquence de phonèmes IPA en timeline
    de visèmes ({"v": "V03", "t": ..., "d": ...}), poussée juste avant
    onSpeaking(true) via le nouvel évènement onVisemes (voir
    set_ui_visemes dans src/ui/alfred_app.py). Nécessite que le modèle .onnx
    ait été patché avec `python -m piper.patch_voice_with_alignment` (sinon
    Piper renvoie une liste d'alignments vide — fallback silencieux sur
    l'ancien cycle de visèmes à intervalle fixe côté JS).

Pas encore branché (prochaines étapes) :
  - Coupure effective du son en cours de lecture sur "Interrompre" (le TTS
    continue de jouer la phrase en cours).

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


def _on_speaking(active: bool) -> None:
    _push("onSpeaking", active)


def _on_listening(active: bool) -> None:
    _push("onListening", active)


def _on_voice_error(message: str) -> None:
    _push("onVoiceError", message)


def _on_visemes(timeline: list) -> None:
    _push("onVisemes", timeline)


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
    # set_ui_speaking / set_ui_listening sont déjà appelés par main.py (callbacks
    # TTS on_play_start/on_play_stop, et boucle principale) mais n'étaient pas
    # branchés côté desktop HTML — c'est ce qui manquait pour un mode vocal réel.
    _alfred_app_module.set_ui_speaking = _on_speaking
    _alfred_app_module.set_ui_listening = _on_listening
    _alfred_app_module.set_ui_voice_error = _on_voice_error
    # Timeline de visèmes phonème-exacte, émise juste avant onSpeaking(true) —
    # voir main.py::_cb_visemes et PiperTTS.on_visemes.
    _alfred_app_module.set_ui_visemes = _on_visemes


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

    # ── Tableau de bord (données réelles, voir src/ui/desktop_dashboard_data.py) ──

    def get_recommandations(self) -> list:
        from src.ui.desktop_dashboard_data import get_recommandations
        return get_recommandations()

    def get_emotion_state(self) -> dict:
        from src.ui.desktop_dashboard_data import get_emotion_state
        return get_emotion_state()

    def set_emotion_override(self, enabled: bool) -> dict:
        from src.ui.desktop_dashboard_data import set_emotion_override
        return set_emotion_override(enabled)

    def correct_emotion(self, mood_label: str) -> dict:
        from src.ui.desktop_dashboard_data import correct_emotion
        return correct_emotion(mood_label)

    def get_planning(self) -> list:
        from src.ui.desktop_dashboard_data import get_planning
        return get_planning()

    def get_devices(self) -> dict:
        from src.ui.desktop_dashboard_data import get_devices
        return get_devices()

    def get_activite(self) -> list:
        from src.ui.desktop_dashboard_data import get_activite
        return get_activite()

    def get_kpis(self) -> dict:
        from src.ui.desktop_dashboard_data import get_kpis
        return get_kpis()

    def get_notifications(self) -> list:
        from src.ui.desktop_dashboard_data import get_notifications
        return get_notifications()

    def get_context_consent(self) -> dict:
        from src.ui.context_consent_prefs import load_context_consent
        return load_context_consent()

    def set_context_consent(self, category: str, enabled: bool) -> dict:
        from src.ui.context_consent_prefs import set_context_consent
        return set_context_consent(category, enabled)

    # ── Actions rapides (voir src/ui/desktop_quick_actions.py) ───────────────────

    def run_backup(self) -> dict:
        from src.ui.desktop_quick_actions import run_backup
        return run_backup()

    def summarize_today(self) -> dict:
        from src.ui.desktop_quick_actions import summarize_today
        return summarize_today()

    def search_knowledge(self, query: str) -> dict:
        from src.ui.desktop_quick_actions import search_knowledge
        return search_knowledge(query)

    # ── Météo (premier appel réseau externe du pipeline — voir weather_data.py) ──

    def get_weather(self) -> dict:
        from src.ui.weather_data import get_weather_state
        return get_weather_state()

    def set_weather_consent(self, enabled: bool) -> dict:
        from src.ui.weather_data import set_weather_consent
        return set_weather_consent(enabled)

    def search_weather(self, postal_code: str) -> dict:
        from src.ui.weather_data import search_weather
        return search_weather(postal_code)

    def reset_weather_location(self) -> dict:
        from src.ui.weather_data import reset_weather_location
        return reset_weather_location()

    # ── Mode vocal — micro push-to-talk (voir src/ui/desktop_mic.py) ─────────────

    def start_recording(self) -> dict:
        from src.ui.desktop_mic import start_recording
        return start_recording()

    def stop_recording(self) -> dict:
        from src.ui.desktop_mic import stop_recording
        return stop_recording()

    def interrupt_speech(self) -> dict:
        from src.ui.desktop_tts_control import interrupt_speech
        return interrupt_speech()


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

    # Pré-scan caméra/micro/sortie audio en arrière-plan (widget "Appareils
    # connectés") — évite que le premier chargement du dashboard bloque sur
    # le scan OpenCV des index caméra (~1-2s/index).
    try:
        from src.ui.device_settings import prefetch_devices_async
        prefetch_devices_async()
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
