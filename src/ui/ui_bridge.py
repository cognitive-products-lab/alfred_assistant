"""
PROJECT      : ALFRED
BLOCK        : B15 -- Avatar & Interface
FILE         : src/ui/ui_bridge.py
ROLE         : Bridge thread-safe entre l'interface Kivy et le pipeline conversationnel

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-05-15
VERSION      : V1.0
STATUS       : STABLE

DESCRIPTION :
Module de communication bidirectionnel entre le thread Kivy (UI) et
le thread daemon pipeline (main.py).

  UI -> Pipeline : queue _input_queue  (TextInput -> wait_for_ui_input())
  Pipeline -> UI : deja gere par set_ui_response() dans alfred_app.py

Usage :
  # Dans alfred_with_ui.py, avant de lancer le pipeline :
  from src.ui.ui_bridge import activate
  activate()

  # Dans le pipeline (main.py) :
  from src.ui.ui_bridge import is_active, wait_for_ui_input
  if is_active():
      text = wait_for_ui_input()   # bloquant jusqu'a saisie UI
  else:
      text = input("Toi : ").strip()

  # Dans alfred_app.py (thread Kivy) :
  from src.ui.ui_bridge import send_user_input, set_response_callback
  send_user_input("Bonjour ALFRED")
"""

from __future__ import annotations

import queue
import threading
from typing import Callable, Optional

# ============================================================
# Etat global du bridge
# ============================================================

_input_queue:      "queue.Queue[tuple[str, str]]"  = queue.Queue()
_ui_active:        bool                           = False
_response_cb:      Optional[Callable[[str], None]] = None
_user_msg_cb:      Optional[Callable[[str], None]] = None
_lock:             threading.Lock                 = threading.Lock()


# ============================================================
# Activation / desactivation
# ============================================================

def activate() -> None:
    """Signale que l'interface Kivy est active. Appeler avant le pipeline."""
    global _ui_active
    with _lock:
        _ui_active = True


def deactivate() -> None:
    """Desactive le bridge (utile pour les tests)."""
    global _ui_active
    with _lock:
        _ui_active = False
    # Debloquer le pipeline si en attente
    _input_queue.put(("", "local"))


def is_active() -> bool:
    """Retourne True si l'interface Kivy est active."""
    with _lock:
        return _ui_active


# ============================================================
# UI -> Pipeline  (saisie utilisateur)
# ============================================================

def send_user_input(text: str, origin: str = "local") -> None:
    """
    Envoie le texte saisi dans l'interface Kivy (ou distante, voir origin)
    vers le pipeline. Appele depuis le thread Kivy, ou depuis
    AlfredDesktopAPI.send_message (local et /api/rpc distant confondus).

    origin : "local" (fenetre pywebview/Kivy du PC) ou "remote" (client
    distant, ex. WebView Android via /api/rpc) -- determine plus loin
    (main.py) quelle interface joue physiquement l'audio TTS de la
    reponse a ce message (voir tts_piper.py::speak(play_locally=...)).
    """
    stripped = text.strip()
    if stripped:
        # Notifie l'UI que le message est en route (affichage immediat)
        if _user_msg_cb:
            _user_msg_cb(stripped)
        _input_queue.put((stripped, origin))


def wait_for_ui_input() -> tuple[str, str]:
    """
    Attend et retourne le prochain (message, origin) saisi dans l'UI.
    Bloquant. Appele depuis le thread pipeline (daemon).
    Retourne ("", "local") si le bridge est desactive.
    """
    return _input_queue.get()


def drain_input_queue() -> None:
    """Vide la file d'entree (utile au reset ou en fin de session)."""
    while not _input_queue.empty():
        try:
            _input_queue.get_nowait()
        except queue.Empty:
            break


# ============================================================
# Pipeline -> UI  (callbacks optionnels)
# ============================================================

def set_response_callback(cb: Callable[[str], None]) -> None:
    """
    Enregistre un callback appele quand une reponse ALFRED est disponible.
    (Alternative / complement a set_ui_response() dans alfred_app.py)
    """
    global _response_cb
    _response_cb = cb


def set_user_message_callback(cb: Callable[[str], None]) -> None:
    """
    Enregistre un callback appele quand l'utilisateur envoie un message.
    Permet d'afficher le message cote UI avant la reponse.
    """
    global _user_msg_cb
    _user_msg_cb = cb


def notify_response(text: str) -> None:
    """Notifie l'UI qu'une reponse est disponible (via callback si enregistre)."""
    if _response_cb:
        _response_cb(text)


# ============================================================
# Statut debug
# ============================================================

def status() -> dict:
    return {
        "ui_active":    is_active(),
        "queue_size":   _input_queue.qsize(),
        "has_resp_cb":  _response_cb is not None,
        "has_msg_cb":   _user_msg_cb is not None,
    }
