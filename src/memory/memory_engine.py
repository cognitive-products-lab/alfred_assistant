"""
PROJECT      : ALFRED
BLOCK        : B02
FUNCTION     : XX.XX
FILE         : src/memory/memory_engine.py
ROLE         : TO_DEFINE

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-06-03
UPDATED      : 2026-06-03
VERSION      : V1.0
STATUS       : DRAFT

DESCRIPTION :
Memoire & RAG — description a completer.
"""

"""
memory_engine.py
Moteur mémoire local pour ALFRED.

Fonctions :
- Sauvegarder chaque échange (user + alfred) dans un fichier JSON
- Charger les N derniers échanges au démarrage
- Fournir un résumé du contexte pour le prompt

Local-first : tout reste sur le PC, aucun cloud.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional


class MemoryEngine:

    def __init__(
        self,
        history_path: str = "data/memory/episodic/dialogue_history.json",
        max_context_entries: int = 10
    ):
        self.history_path = Path(history_path)
        self.max_context_entries = max_context_entries
        self.history: List[Dict[str, Any]] = []

        self._ensure_file()
        self._load()

    # ─────────────────────────────────────────────────────
    # Initialisation
    # ─────────────────────────────────────────────────────

    def _ensure_file(self) -> None:
        """Crée le fichier et les dossiers parents si absents."""
        self.history_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.history_path.exists():
            self._save_to_disk([])

    def _load(self) -> None:
        """Charge l'historique depuis le disque."""
        try:
            with open(self.history_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.history = data if isinstance(data, list) else []
        except (json.JSONDecodeError, FileNotFoundError):
            self.history = []

    def _save_to_disk(self, data: list) -> None:
        """Sauvegarde l'historique sur le disque."""
        with open(self.history_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    # ─────────────────────────────────────────────────────
    # Écriture
    # ─────────────────────────────────────────────────────

    def save_exchange(
        self,
        user_message: str,
        alfred_response: str,
        mode: Optional[str] = None,
        emotion: Optional[str] = None,
        energy: Optional[str] = None
    ) -> None:
        """Sauvegarde un échange complet."""
        entry = {
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "mode": mode or "unknown",
            "emotion": emotion,
            "energy": energy,
            "user": user_message,
            "alfred": alfred_response
        }
        self.history.append(entry)
        self._save_to_disk(self.history)

    # ─────────────────────────────────────────────────────
    # Lecture
    # ─────────────────────────────────────────────────────

    def get_recent_context(self, n: Optional[int] = None) -> List[Dict[str, Any]]:
        """Retourne les N derniers échanges."""
        limit = n or self.max_context_entries
        return self.history[-limit:] if self.history else []

    def format_context_for_prompt(self, n: Optional[int] = None) -> str:
        """
        Formate les derniers échanges en texte lisible
        pour injection dans le prompt utilisateur.
        """
        recent = self.get_recent_context(n)
        if not recent:
            return ""

        lines = ["HISTORIQUE RÉCENT DE LA CONVERSATION :"]
        for entry in recent:
            ts = entry.get("timestamp", "")[:16].replace("T", " ")
            lines.append(f"[{ts}] Utilisateur : {entry['user']}")
            lines.append(f"[{ts}] ALFRED      : {entry['alfred']}")
            lines.append("")

        return "\n".join(lines)

    def get_relevant_summary(self, user_id: str = "default_user") -> str:
        """
        Résumé condensé des derniers échanges pour injection
        dans le system prompt via response_generator.py.
        Appelé par ResponseGenerator._get_memory_summary().
        """
        recent = self.get_recent_context(5)
        if not recent:
            return ""

        lines = ["Contexte des échanges récents :"]
        for entry in recent:
            ts = entry.get("timestamp", "")[:16].replace("T", " ")
            mode = entry.get("mode", "")
            lines.append(f"- [{ts}][{mode}] User: {entry['user'][:80]}")
            lines.append(f"  ALFRED: {entry['alfred'][:120]}")

        return "\n".join(lines)

    def get_session_summary(self) -> str:
        """Résumé rapide de la session pour affichage au démarrage."""
        total = len(self.history)
        if total == 0:
            return "Aucun échange enregistré."
        last = self.history[-1]
        ts = last.get("timestamp", "")[:16].replace("T", " ")
        return f"{total} échange(s) en mémoire — dernier le {ts}"

    # ─────────────────────────────────────────────────────
    # Utilitaires
    # ─────────────────────────────────────────────────────

    def clear_session(self) -> None:
        """Vide l'historique complet."""
        self.history = []
        self._save_to_disk([])
        print("  Mémoire effacée.")

    def stats(self) -> Dict[str, Any]:
        """Statistiques basiques."""
        return {
            "total_exchanges": len(self.history),
            "file": str(self.history_path),
            "max_context": self.max_context_entries
        }

    def __repr__(self) -> str:
        return (
            f"MemoryEngine("
            f"exchanges={len(self.history)}, "
            f"path='{self.history_path}')"
        )
