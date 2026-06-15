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

    def get_voice_nowait(self):
        """Récupère un item voix/erreur sans bloquer, sinon None.

        Les items clavier/système (déjà gérés via input() direct) sont
        remis dans la file pour ne pas être perdus.
        """
        try:
            item = self.inputs.get_nowait()
        except queue.Empty:
            return None

        if item[0] in ("voice", "error"):
            return item

        self.inputs.put(item)
        return None

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