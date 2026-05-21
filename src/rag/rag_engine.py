# -*- coding: utf-8 -*-
"""
rag_engine.py — ALFRED V3
Moteur RAG : indexation et recherche sémantique des mémoires.

Backend : ChromaDB local (fallback keyword si non installé).
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from src.rag.chroma_store import ChromaStore


class RAGEngine:
    """
    Indexe les échanges et les documents, puis les retrouve par similarité sémantique.

    Deux collections :
    - memory  : échanges utilisateur/ALFRED
    - knowledge : documents de connaissance
    """

    def __init__(
        self,
        persist_directory: str = "data/memory/chroma",
    ):
        self._memory_store = ChromaStore(
            persist_directory=persist_directory,
            collection_name="alfred_memory",
        )
        self._knowledge_store = ChromaStore(
            persist_directory=persist_directory,
            collection_name="alfred_knowledge",
        )

    # ── Indexation ────────────────────────────────────────

    def index_exchange(
        self,
        user_input: str,
        response: str,
        session_id: str,
        turn: int,
    ) -> None:
        """Indexe un échange utilisateur/ALFRED dans la mémoire sémantique."""
        doc_id = f"{session_id}_t{turn}"
        text = f"Utilisateur : {user_input}\nALFRED : {response}"
        metadata = {
            "session_id": session_id,
            "turn": turn,
            "role": "exchange",
        }
        self._memory_store.add(text=text, doc_id=doc_id, metadata=metadata)

    def index_document(
        self,
        text: str,
        doc_id: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> bool:
        """Indexe un document de connaissance."""
        return self._knowledge_store.add(
            text=text,
            doc_id=doc_id,
            metadata=metadata or {},
        )

    # ── Recherche ─────────────────────────────────────────

    def search_memories(
        self,
        query: str,
        n_results: int = 5,
    ) -> List[Dict[str, Any]]:
        """Recherche sémantique dans la mémoire conversationnelle."""
        return self._memory_store.search(query=query, n_results=n_results)

    def search_knowledge(
        self,
        query: str,
        n_results: int = 3,
    ) -> List[Dict[str, Any]]:
        """Recherche sémantique dans la base de connaissance."""
        return self._knowledge_store.search(query=query, n_results=n_results)

    def search_all(
        self,
        query: str,
        n_results: int = 5,
    ) -> List[Dict[str, Any]]:
        """Fusionne mémoire + knowledge, trie par pertinence."""
        mem = self._memory_store.search(query=query, n_results=n_results)
        know = self._knowledge_store.search(query=query, n_results=n_results)
        merged = mem + know
        merged.sort(key=lambda r: r.get("score", 0.0), reverse=True)
        return merged[:n_results]

    # ── Statut ────────────────────────────────────────────

    @property
    def is_available(self) -> bool:
        return self._memory_store.is_available or self._knowledge_store.is_available

    def get_status(self) -> Dict[str, Any]:
        return {
            "memory": self._memory_store.get_status(),
            "knowledge": self._knowledge_store.get_status(),
        }
