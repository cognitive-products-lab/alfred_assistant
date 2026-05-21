# -*- coding: utf-8 -*-
"""
chroma_store.py — ALFRED V3
Wrapper ChromaDB avec fallback keyword si chromadb non installé.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any, Dict, List


class ChromaStore:
    """
    Abstraction sur ChromaDB.
    Si chromadb n'est pas installé, bascule en recherche keyword.
    """

    def __init__(
        self,
        persist_directory: str = "data/memory/chroma",
        collection_name: str = "alfred_memory",
    ):
        self._available = False
        self._client = None
        self._collection = None
        self._collection_name = collection_name
        self._fallback_store: List[Dict[str, Any]] = []

        try:
            import chromadb

            Path(persist_directory).mkdir(parents=True, exist_ok=True)
            self._client = chromadb.PersistentClient(path=persist_directory)
            self._collection = self._client.get_or_create_collection(
                name=collection_name,
                metadata={"hnsw:space": "cosine"},
            )
            self._available = True
        except Exception:
            pass

    @property
    def is_available(self) -> bool:
        return self._available

    def add(self, text: str, doc_id: str, metadata: Dict[str, Any] | None = None) -> bool:
        if not text or not doc_id:
            return False

        if self._available:
            try:
                self._collection.upsert(
                    documents=[text],
                    ids=[doc_id],
                    metadatas=[metadata or {}],
                )
                return True
            except Exception:
                return False

        # Fallback keyword store
        self._fallback_store.append(
            {"id": doc_id, "document": text, "metadata": metadata or {}}
        )
        return True

    def search(self, query: str, n_results: int = 5) -> List[Dict[str, Any]]:
        if not query:
            return []

        if self._available:
            try:
                count = self._collection.count()
                if count == 0:
                    return []
                results = self._collection.query(
                    query_texts=[query],
                    n_results=min(n_results, count),
                )
                docs = results.get("documents", [[]])[0]
                metas = results.get("metadatas", [[]])[0]
                distances = results.get("distances", [[]])[0]
                return [
                    {
                        "document": doc,
                        "metadata": meta,
                        "score": max(0.0, 1.0 - dist),
                    }
                    for doc, meta, dist in zip(docs, metas, distances)
                ]
            except Exception:
                return []

        # Fallback keyword search
        terms = re.findall(r"\w+", query.lower())
        scored: List[tuple[float, Dict[str, Any]]] = []
        for entry in self._fallback_store:
            doc_lower = entry["document"].lower()
            hits = sum(1 for t in terms if t in doc_lower)
            if hits > 0:
                scored.append((hits / max(len(terms), 1), entry))
        scored.sort(key=lambda x: x[0], reverse=True)
        return [
            {"document": e["document"], "metadata": e["metadata"], "score": s}
            for s, e in scored[:n_results]
        ]

    def count(self) -> int:
        if self._available:
            try:
                return self._collection.count()
            except Exception:
                return 0
        return len(self._fallback_store)

    def get_status(self) -> Dict[str, Any]:
        return {
            "available": self._available,
            "backend": "chromadb" if self._available else "keyword_fallback",
            "count": self.count(),
            "collection": self._collection_name,
        }
