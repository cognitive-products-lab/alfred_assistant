"""
PROJECT : ALFRED
BLOCK   : B01 / RGPD
FILE    : src/conversation/commands/erasure_command.py
ROLE    : Droit à l'effacement Art. 17 RGPD — suppression complète des données utilisateur
STATUS  : VALIDATED

Point d'entrée unique pour le droit à l'effacement : combine la suppression
des fichiers sensibles (src.security.compliance_manager.delete_user_data)
et la purge de la mémoire long terme (src.memory.long_term_memory.delete_all_memories),
qui existaient déjà toutes les deux, testées, mais sans aucun point d'entrée
utilisateur réel avant ce module (constat du 11/07/2026).

Usage :
    from src.conversation.commands.erasure_command import erase_user_data
    result = erase_user_data(confirm=True)

En ligne de commande, une confirmation textuelle explicite est requise
en plus du flag --confirm, pour éviter toute suppression accidentelle.
"""

from __future__ import annotations

import sys
from datetime import datetime, timezone
from pathlib import Path

from src.security.compliance_manager import delete_user_data
from src.memory.long_term_memory import delete_all_memories

ROOT = Path(__file__).resolve().parents[3]

_CLI_CONFIRM_PHRASE = "SUPPRIMER MES DONNEES"


def erase_user_data(confirm: bool = False) -> dict:
    """
    Exécute le droit à l'effacement Art. 17 RGPD : supprime les fichiers
    sensibles connus et purge la mémoire long terme (SQLite).

    Args:
        confirm : Doit être True pour exécuter réellement la suppression.

    Returns:
        dict avec 'confirmed', 'files', 'memory_purged', 'errors', 'erased_at'.
    """
    erased_at = datetime.now(timezone.utc).isoformat()

    if not confirm:
        return {
            "confirmed": False,
            "right": "Art. 17",
            "files": {"deleted": [], "missing": [], "errors": []},
            "memory_purged": False,
            "erased_at": erased_at,
        }

    files_result = delete_user_data(confirm=True)
    memory_purged = delete_all_memories(confirm=True)

    return {
        "confirmed": True,
        "right": "Art. 17",
        "files": files_result,
        "memory_purged": memory_purged,
        "erased_at": erased_at,
    }


def _run_cli() -> int:
    if "--confirm" not in sys.argv:
        print("[Art.17] Aucune suppression effectuée — relancer avec --confirm.")
        return 1

    print(f"[Art.17] Cette action est irréversible. Tapez exactement \"{_CLI_CONFIRM_PHRASE}\" pour continuer :")
    typed = input("> ").strip()
    if typed != _CLI_CONFIRM_PHRASE:
        print("[Art.17] Confirmation incorrecte — suppression annulée.")
        return 1

    result = erase_user_data(confirm=True)
    print(f"[Art.17] Suppression effectuée à {result['erased_at']}")
    print(f"  Fichiers supprimés : {result['files']['deleted']}")
    print(f"  Fichiers absents   : {result['files']['missing']}")
    print(f"  Mémoire purgée     : {result['memory_purged']}")
    if result["files"]["errors"]:
        print(f"  Erreurs            : {result['files']['errors']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(_run_cli())
