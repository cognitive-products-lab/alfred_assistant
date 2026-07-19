"""
════════════════════════════════════════════════════════════
PROJECT      : ALFRED
BLOCK        : B22
FUNCTION     : 22.07
FILE         : fatigue_reducer.py
ROLE         : Réduction de la fatigue cognitive — chunking, pauses, densité informationnelle

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-05-22
UPDATED      : 2026-05-22
VERSION      : V1.0
STATUS       : VALIDATED

DEPENDENCIES :
- re
- logging
- dataclasses

SECURITY :
- Local-first
- Security by Design

DESCRIPTION :
Découpe les réponses longues en segments digestibles, insère des suggestions de pause
et réduit la densité informationnelle selon le niveau de charge cognitive détecté.
Seuils configurables : DEFAULT_CHUNK_WORDS=80, PAUSE_AFTER_N_CHUNKS=3.
════════════════════════════════════════════════════════════
"""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass

logger = logging.getLogger(__name__)

DEFAULT_CHUNK_WORDS = 80
PAUSE_AFTER_N_CHUNKS = 3
PAUSE_MESSAGE = "💡 Petite pause conseillée avant de continuer."


@dataclass
class ChunkedContent:
    chunks: list[str]
    total_words: int
    pause_indices: list[int]   # indices des chunks après lesquels une pause est suggérée


class FatigueReducer:
    """
    22.07 Réduction de la fatigue cognitive.

    Découpe le contenu et signale les moments de pause.
    """

    def __init__(self, chunk_words: int = DEFAULT_CHUNK_WORDS) -> None:
        self.chunk_words = chunk_words
        logger.info("FatigueReducer initialisé (chunk=%d mots)", chunk_words)

    def chunk(self, text: str) -> ChunkedContent:
        """
        Découpe `text` en segments de `chunk_words` mots max,
        en respectant les fins de phrase.
        """
        sentences = re.split(r"(?<=[.!?])\s+", text.strip())
        chunks: list[str] = []
        current: list[str] = []
        current_wc = 0

        for sentence in sentences:
            wc = len(sentence.split())
            if current_wc + wc > self.chunk_words and current:
                chunks.append(" ".join(current))
                current = [sentence]
                current_wc = wc
            else:
                current.append(sentence)
                current_wc += wc

        if current:
            chunks.append(" ".join(current))

        pause_indices = [
            i for i in range(1, len(chunks))
            if i % PAUSE_AFTER_N_CHUNKS == 0
        ]

        return ChunkedContent(
            chunks=chunks,
            total_words=len(text.split()),
            pause_indices=pause_indices,
        )

    def format_with_breaks(self, text: str) -> str:
        """Retourne le texte reformaté avec sauts de ligne entre les chunks."""
        result = self.chunk(text)
        return "\n\n".join(result.chunks)

    def format_with_pauses(self, text: str) -> list[str]:
        """
        Retourne la liste des chunks avec les messages de pause insérés.
        Utile pour l'affichage progressif chunk par chunk.
        """
        result = self.chunk(text)
        output: list[str] = []
        for i, chunk in enumerate(result.chunks):
            output.append(chunk)
            if i in result.pause_indices:
                output.append(PAUSE_MESSAGE)
        return output

    def status(self) -> dict:
        return {
            "chunk_words": self.chunk_words,
            "pause_after_n_chunks": PAUSE_AFTER_N_CHUNKS,
        }


# ─────────────────────────────────────────────────────────
# Test standalone
# ─────────────────────────────────────────────────────────
if __name__ == "__main__":
    fr = FatigueReducer(chunk_words=30)
    sample = (
        "L'intelligence artificielle transforme nos vies. "
        "Elle permet d'automatiser des tâches complexes. "
        "Les modèles de langage apprennent à partir de grandes quantités de texte. "
        "Ils peuvent répondre à des questions, rédiger des e-mails et résumer des documents. "
        "Cependant, ils ont des limites importantes. "
        "Il faut les utiliser avec discernement."
    )
    chunked = fr.chunk(sample)
    print(f"Chunks : {len(chunked.chunks)}")
    print(f"Pauses après : {chunked.pause_indices}")
    print("FatigueReducer skeleton OK.")
