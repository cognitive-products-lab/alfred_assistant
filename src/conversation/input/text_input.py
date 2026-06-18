# ============================================================
# ALFRED — src/conversation/input/text_input.py
# Bloc 01.01 — Gestion des conversations
#
# 📚 NOTION EXAM :
#   D12-1 — Capsule 1 : Dialogue texte et historisation des échanges
#
# 🎯 UTILITÉ ALFRED :
#   Gère la saisie clavier terminal, nettoie et valide l'input
#   et historise les échanges de la session en cours.
#
# 🏗️ DOMAINE :
#   Noyau conversationnel — interface texte V1, hotpath clavier
# ============================================================

import html
import re
from datetime import datetime

from src.security.input_validator import sanitize_input
from src.security.security_logger import log_event

# ── Constantes ────────────────────────────────────────────
MAX_INPUT_LENGTH = 1000
_EXIT_COMMANDS = {"exit", "quit", "quitter", "bye", "au revoir", ":q"}

# ── Historique session (en mémoire) ───────────────────────
_session_history: list[dict] = []


# ─────────────────────────────────────────────────────────
# Lecture input terminal
# ─────────────────────────────────────────────────────────

def read_user_input(prompt: str = "Vous : ") -> str:
    """
    Lit une saisie clavier depuis le terminal.
    Retourne la chaîne nettoyée ou "" si vide.

    Args:
        prompt : Texte affiché avant la saisie

    Returns:
        Texte saisi, nettoyé et sécurisé
    """
    try:
        raw = input(prompt)
    except (EOFError, KeyboardInterrupt):
        log_event("Session interrompue par l'utilisateur", "INFO")
        return ":exit_signal:"

    cleaned = sanitize_input(raw, max_length=MAX_INPUT_LENGTH)

    if cleaned != raw.strip():
        log_event("Input nettoyé par le validateur de sécurité", "WARNING")

    return cleaned


def is_exit_command(user_input: str) -> bool:
    """
    Détecte si l'utilisateur veut quitter la session.

    Args:
        user_input : Texte saisi

    Returns:
        True si c'est une commande de sortie
    """
    return user_input.strip().lower() in _EXIT_COMMANDS or user_input == ":exit_signal:"


# ─────────────────────────────────────────────────────────
# Validation
# ─────────────────────────────────────────────────────────

def is_valid_input(user_input: str) -> bool:
    """
    Vérifie que l'input est non vide et dans les limites acceptables.

    Args:
        user_input : Texte à valider

    Returns:
        True si valide
    """
    if not user_input or not user_input.strip():
        return False
    if len(user_input) > MAX_INPUT_LENGTH:
        log_event(f"Input trop long : {len(user_input)} caractères", "WARNING")
        return False
    return True


# ─────────────────────────────────────────────────────────
# Historique session
# ─────────────────────────────────────────────────────────

def add_to_history(user_input: str, assistant_response: str) -> None:
    """
    Enregistre un échange dans l'historique de session en mémoire.

    Args:
        user_input          : Message de l'utilisateur
        assistant_response  : Réponse d'ALFRED
    """
    _session_history.append({
        "timestamp": datetime.now().isoformat(),
        "user": user_input,
        "alfred": assistant_response,
    })


def get_history() -> list[dict]:
    """Retourne l'historique complet de la session courante."""
    return _session_history.copy()


def get_last_exchanges(n: int = 3) -> list[dict]:
    """
    Retourne les n derniers échanges de la session.

    Args:
        n : Nombre d'échanges à retourner

    Returns:
        Liste des n derniers échanges
    """
    return _session_history[-n:] if _session_history else []


def clear_history() -> None:
    """Vide l'historique de session (reset)."""
    global _session_history
    _session_history = []
    log_event("Historique session vidé", "INFO")


def history_count() -> int:
    """Retourne le nombre d'échanges enregistrés dans la session."""
    return len(_session_history)
