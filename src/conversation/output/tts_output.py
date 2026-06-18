# ============================================================
# ALFRED — src/conversation/output/tts_output.py
# Bloc 04.02 — Synthèse vocale (TTS)
#
# 📚 NOTION EXAM :
#   D13-2 — Capsule 4 : Interface de sortie vocale et affichage terminal
#
# 🎯 UTILITÉ ALFRED :
#   Façade de sortie V1 — affichage terminal et stub TTS
#   en attente du moteur Piper V3 (tts_piper.py).
#
# 🏗️ DOMAINE :
#   Interaction vocale — sortie audio et texte terminal V1
# ============================================================

import sys


# ─────────────────────────────────────────────────────────
# Affichage terminal (actif V1)
# ─────────────────────────────────────────────────────────

# Préfixe visuel ALFRED
_ALFRED_PREFIX = "🤖 ALFRED : "
_SYSTEM_PREFIX = "  [système] "
_SEPARATOR     = "─" * 50


def display_response(text: str, show_separator: bool = False) -> None:
    """
    Affiche la réponse d'ALFRED dans le terminal.

    Args:
        text            : Texte de la réponse
        show_separator  : Affiche un séparateur visuel
    """
    if show_separator:
        print(f"\n{_SEPARATOR}")
    print(f"\n{_ALFRED_PREFIX}{text}\n")


def display_system(message: str) -> None:
    """
    Affiche un message système (non-réponse ALFRED).

    Args:
        message : Message informatif système
    """
    print(f"{_SYSTEM_PREFIX}{message}")


def display_welcome(user_name: str, greeting: str, period: str) -> None:
    """
    Affiche le message d'accueil ALFRED au démarrage de session.

    Args:
        user_name : Prénom de l'utilisateur
        greeting  : Salutation adaptée à l'heure
        period    : Période de la journée
    """
    print(f"\n{'═' * 50}")
    print(f"  🤖 ALFRED — Assistant personnel")
    print(f"{'═' * 50}")
    print(f"\n  {greeting} {user_name}.")
    print(f"  Je suis là. Qu'est-ce qui t'amène ce {period} ?\n")


def display_goodbye(user_name: str) -> None:
    """
    Affiche le message de fin de session.

    Args:
        user_name : Prénom de l'utilisateur
    """
    print(f"\n{_ALFRED_PREFIX}À bientôt {user_name}. Prends soin de toi.\n")
    print(f"{'─' * 50}\n")


def display_error(message: str) -> None:
    """
    Affiche un message d'erreur.

    Args:
        message : Description de l'erreur
    """
    print(f"\n  ⚠️  {message}\n", file=sys.stderr)


def display_session_summary(exchange_count: int) -> None:
    """
    Affiche un résumé de fin de session.

    Args:
        exchange_count : Nombre d'échanges de la session
    """
    print(f"\n{'─' * 50}")
    print(f"  Session terminée — {exchange_count} échange(s)")
    print(f"{'─' * 50}\n")


# ─────────────────────────────────────────────────────────
# TTS (stub V1 → actif V3)
# ─────────────────────────────────────────────────────────

def is_tts_available() -> bool:
    """
    Vérifie si la synthèse vocale est disponible.
    V1 : toujours False.
    V3 : True si Piper/Coqui chargé.
    """
    return False


def speak(text: str, emotion: str = "neutral") -> None:
    """
    Synthétise vocalement un texte.

    V1 STUB : affiche uniquement dans le terminal.
    V3 : Piper/Coqui local avec adaptation émotionnelle.

    Args:
        text    : Texte à synthétiser
        emotion : État émotionnel pour adapter l'intonation
    """
    # En V1 : fallback sur affichage terminal
    display_response(text)


def get_tts_status() -> dict:
    """
    Retourne l'état du système TTS.

    Returns:
        dict avec statut et version
    """
    return {
        "available": False,
        "engine":    None,
        "version":   "stub_v1",
        "planned":   "piper_coqui_v3",
        "message":   "TTS vocal prévu en V3 (Piper/Coqui + RTX 5080)",
    }
