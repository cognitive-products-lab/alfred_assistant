"""
════════════════════════════════════════════════════════════
PROJECT      : ALFRED
BLOCK        : B05
FILE         : src/ui/pin_dialog.py
ROLE         : Popup tkinter saisie PIN — avant démarrage Kivy

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-06-20
UPDATED      : 2026-06-20
VERSION      : V1.0
STATUS       : VALIDATED

DESCRIPTION :
Fenêtre de saisie PIN indépendante de Kivy (tkinter).
Lancée dans le thread principal AVANT AlfredApp.run(),
elle n'entre donc pas en conflit avec la boucle Kivy.

Polices : OpenDyslexic3-Regular.ttf (assets/fonts/)
          chargée temporairement via AddFontResourceExW.
Theme   : dark violet (#1a1a2e / #7c4dff)
════════════════════════════════════════════════════════════
"""
from __future__ import annotations

import ctypes
import sys
import tkinter as tk
from pathlib import Path

ROOT       = Path(__file__).resolve().parent.parent.parent
_FONT_PATH = ROOT / "assets" / "fonts" / "OpenDyslexic3-Regular.ttf"

_BG      = "#1a1a2e"
_FG      = "#e8e8ff"
_ACCENT  = "#7c4dff"
_ENTRY   = "#16213e"
_ERR     = "#ff6b6b"
_SUCCESS = "#4caf50"
_BTN_ACT = "#5c35cc"


def _load_font() -> str:
    """
    Charge OpenDyslexic3 temporairement dans GDI (Windows).
    Retourne le nom famille si succès, sinon 'Segoe UI'.
    """
    if sys.platform == "win32" and _FONT_PATH.exists():
        try:
            # FR_PRIVATE = 0x10 — disponible pour ce processus uniquement
            ctypes.windll.gdi32.AddFontResourceExW(str(_FONT_PATH), 0x10, 0)
            return "OpenDyslexic3"
        except Exception:
            pass
    return "Segoe UI"


def _center(win: tk.Tk | tk.Toplevel, w: int, h: int) -> None:
    win.update_idletasks()
    sw = win.winfo_screenwidth()
    sh = win.winfo_screenheight()
    win.geometry(f"{w}x{h}+{(sw - w) // 2}+{(sh - h) // 2}")


# ─────────────────────────────────────────────────────────────────────────────
# Dialogue authentification PIN
# ─────────────────────────────────────────────────────────────────────────────

def show_auth_dialog(
    user_id: str,
    authenticate_fn,
    max_attempts: int = 3,
) -> bool:
    """
    Affiche la popup de saisie PIN.

    Args:
        user_id        : identifiant utilisateur
        authenticate_fn: callable(user_id, pin) → {"success": bool, "reason": str}
        max_attempts   : nombre de tentatives avant blocage

    Returns:
        True si authentification réussie, False sinon.
    """
    font = _load_font()
    f_title  = (font, 20, "bold")
    f_sub    = (font, 12)
    f_entry  = (font, 22)
    f_btn    = (font, 13, "bold")
    f_err    = (font, 11)

    result   = {"ok": False, "attempts": 0}

    root = tk.Tk()
    root.title("ALFRED — Authentification")
    root.configure(bg=_BG)
    root.resizable(False, False)
    root.attributes("-topmost", True)
    _center(root, 400, 360)

    # ── Titre ─────────────────────────────────────────────────────────────────
    tk.Label(root, text="ALFRED", font=f_title, bg=_BG, fg=_ACCENT).pack(pady=(32, 2))
    tk.Label(root, text="Entrez votre code PIN", font=f_sub, bg=_BG, fg=_FG).pack(pady=(0, 22))

    # ── Champ PIN ─────────────────────────────────────────────────────────────
    pin_var = tk.StringVar()
    entry = tk.Entry(
        root, textvariable=pin_var, show="●",
        font=f_entry, bg=_ENTRY, fg=_FG,
        insertbackground=_FG, relief="flat",
        width=12, justify="center", bd=0,
    )
    # Bordure fine simulée via un frame coloré
    frame_entry = tk.Frame(root, bg=_ACCENT, padx=2, pady=2)
    frame_entry.pack(padx=60)
    entry_inner = tk.Frame(frame_entry, bg=_ENTRY)
    entry_inner.pack()
    entry.pack(in_=entry_inner, ipady=10, padx=4)
    entry.focus_set()

    # ── Message erreur / statut ────────────────────────────────────────────────
    msg_var = tk.StringVar()
    msg_lbl = tk.Label(root, textvariable=msg_var, font=f_err, bg=_BG, fg=_ERR,
                       wraplength=340)
    msg_lbl.pack(pady=(10, 0))

    # ── Bouton Valider ─────────────────────────────────────────────────────────
    def _validate(*_):
        pin = pin_var.get().strip()
        if not pin:
            msg_var.set("Veuillez saisir votre PIN.")
            return

        btn.configure(state="disabled")
        auth = authenticate_fn(user_id, pin)

        if auth["success"]:
            msg_var.set("Accès autorisé.")
            msg_lbl.configure(fg=_SUCCESS)
            result["ok"] = True
            root.after(600, lambda: (root.quit(), root.destroy()))
            return

        result["attempts"] += 1
        pin_var.set("")
        entry.focus_set()
        remaining = max_attempts - result["attempts"]

        if remaining <= 0:
            msg_var.set("Accès refusé — trop de tentatives.")
            root.after(1400, lambda: (root.quit(), root.destroy()))
        else:
            reason = auth.get("reason", "PIN incorrect")
            msg_var.set(f"{reason}  —  {remaining} essai(s) restant(s)")
            btn.configure(state="normal")

    btn = tk.Button(
        root, text="Valider", font=f_btn,
        bg=_ACCENT, fg="white", activebackground=_BTN_ACT,
        relief="flat", padx=24, pady=10,
        cursor="hand2", command=_validate,
    )
    btn.pack(pady=20)

    entry.bind("<Return>", _validate)
    root.protocol("WM_DELETE_WINDOW", lambda: sys.exit(0))

    root.mainloop()
    return result["ok"]


# ─────────────────────────────────────────────────────────────────────────────
# Dialogue création PIN (première utilisation)
# ─────────────────────────────────────────────────────────────────────────────

def show_register_dialog(user_id: str, register_pin_fn) -> bool:
    """
    Affiche la popup de création de PIN (aucun PIN enregistré).

    Returns:
        True si PIN créé ou skip, False si l'utilisateur ferme la fenêtre.
    """
    font = _load_font()
    f_title = (font, 18, "bold")
    f_sub   = (font, 11)
    f_entry = (font, 20)
    f_btn   = (font, 12, "bold")
    f_err   = (font, 10)

    result = {"ok": False}

    root = tk.Tk()
    root.title("ALFRED — Créer un code PIN")
    root.configure(bg=_BG)
    root.resizable(False, False)
    root.attributes("-topmost", True)
    _center(root, 420, 420)

    tk.Label(root, text="ALFRED", font=f_title, bg=_BG, fg=_ACCENT).pack(pady=(28, 2))
    tk.Label(root, text="Première utilisation — créez un code PIN\npour sécuriser votre assistant.",
             font=f_sub, bg=_BG, fg=_FG, justify="center").pack(pady=(0, 18))

    def _entry_frame(parent, show_char=""):
        frm = tk.Frame(parent, bg=_ACCENT, padx=2, pady=2)
        frm.pack(padx=50, pady=3)
        inner = tk.Frame(frm, bg=_ENTRY)
        inner.pack()
        var = tk.StringVar()
        e = tk.Entry(inner, textvariable=var, font=f_entry, bg=_ENTRY, fg=_FG,
                     insertbackground=_FG, relief="flat", width=11,
                     justify="center", bd=0, show=show_char or "")
        e.pack(ipady=8, padx=4)
        return e, var

    tk.Label(root, text="Nouveau PIN (4 caractères min.)", font=f_sub, bg=_BG, fg=_FG).pack()
    e1, v1 = _entry_frame(root, "●")
    tk.Label(root, text="Confirmer le PIN", font=f_sub, bg=_BG, fg=_FG).pack(pady=(8, 0))
    e2, v2 = _entry_frame(root, "●")
    e1.focus_set()

    msg_var = tk.StringVar()
    msg_lbl = tk.Label(root, textvariable=msg_var, font=f_err, bg=_BG, fg=_ERR, wraplength=360)
    msg_lbl.pack(pady=(8, 0))

    def _create(*_):
        p1, p2 = v1.get().strip(), v2.get().strip()
        if not p1:
            msg_var.set("Veuillez saisir un PIN.")
            return
        if p1 != p2:
            msg_var.set("Les PINs ne correspondent pas.")
            v2.set("")
            e2.focus_set()
            return
        if not register_pin_fn(user_id, p1):
            msg_var.set("PIN invalide (4 à 32 caractères).")
            v1.set(""); v2.set("")
            e1.focus_set()
            return
        msg_var.set("PIN créé avec succès !")
        msg_lbl.configure(fg=_SUCCESS)
        result["ok"] = True
        root.after(800, lambda: (root.quit(), root.destroy()))

    def _skip():
        result["ok"] = True
        root.quit()
        root.destroy()

    btn_frame = tk.Frame(root, bg=_BG)
    btn_frame.pack(pady=16)

    tk.Button(btn_frame, text="Créer le PIN", font=f_btn,
              bg=_ACCENT, fg="white", activebackground=_BTN_ACT,
              relief="flat", padx=18, pady=8, cursor="hand2",
              command=_create).pack(side="left", padx=8)

    tk.Button(btn_frame, text="Passer", font=(font, 11),
              bg="#333355", fg=_FG, activebackground="#444466",
              relief="flat", padx=12, pady=8, cursor="hand2",
              command=_skip).pack(side="left", padx=8)

    e1.bind("<Return>", lambda _: e2.focus_set())
    e2.bind("<Return>", _create)
    root.protocol("WM_DELETE_WINDOW", lambda: sys.exit(0))

    root.mainloop()
    return result["ok"]
