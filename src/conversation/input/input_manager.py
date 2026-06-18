# ============================================================
# ALFRED — src/conversation/input/input_manager.py
# Bloc 01.01 — Gestion des conversations
#
# 📚 NOTION EXAM :
#   D12-1 — Capsule 1 : Gestion hybride des entrées clavier/voix
#
# 🎯 UTILITÉ ALFRED :
#   HybridInputManager — arbitre les entrées clavier et vocales
#   via un système de queue thread-safe (clavier prioritaire V1).
#
# 🏗️ DOMAINE :
#   Noyau conversationnel — entrées hybrides texte/voix, thread-safe
#
# UPDATED 2026-06-15 : suppression de get_voice_nowait() (non utilisée
# après le fix du bug "ALFRED ne réagit pas en mode vocal" — main.py
# consomme désormais get_input() en bloquant pour clavier ET voix).
# ============================================================

from __future__ import annotations
import queue
import threading
import time


class HybridInputManager:
    def __init__(self, voice_func):
        self.voice_func = voice_func
        self.inputs = queue.Queue()
        self.running = False
        self.last_keyboard_time = 0

    def start(self):
        self.running = True
        threading.Thread(target=self._keyboard_loop, daemon=True).start()
        threading.Thread(target=self._voice_loop, daemon=True).start()

    def stop(self):
        self.running = False

    def get_input(self):
        return self.inputs.get()

    # =========================
    # CLAVIER = PRIORITAIRE
    # =========================
    def _keyboard_loop(self):
        while self.running:
            try:
                text = input("  Toi ⌨️ : ").strip()
                if text:
                    # coupe temporairement le vocal
                    self.last_keyboard_time = time.time()

                    self.inputs.put(("keyboard", text))

                    # évite collision clavier / micro
                    time.sleep(0.2)
            except EOFError:
                self.inputs.put(("system", "exit"))
                break

    # =========================
    # MICRO = SECONDAIRE
    # =========================
    def _voice_loop(self):
        while self.running:
            try:
                # Si tu viens d’écrire → le micro attend
                if time.time() - self.last_keyboard_time < 10:
                    time.sleep(0.5)
                    continue

                text = self.voice_func().strip()

                if text:
                    self.inputs.put(("voice", text))

            except Exception as exc:
                self.inputs.put(("error", f"Erreur voix : {exc}"))