# ============================================================
# ALFRED — src/memory/rag_stub.py
# Bloc 02.04 — Contextualisation intelligente
#
# 📚 NOTION EXAM :
#   D22-3 — Capsule 3 : Architecture RAG — ChromaDB local, embeddings
#   multilingues (sentence-transformers), zéro cloud.
#
# 🎯 UTILITÉ ALFRED :
#   Recherche sémantique locale sur la mémoire épisodique — retrouve un
#   souvenir même sans chevauchement de mots-clés exact (contrairement à
#   episodic_memory.search_episodes(), recherche substring pure). Nom de
#   fichier conservé (rag_stub.py) pour compatibilité — le contenu n'est
#   plus un stub depuis le 18/08/2026 (session 6, plan semaine 17-24/08).
#
# 🏗️ DOMAINE :
#   Mémoire & contexte — RAG local-first, ChromaDB + sentence-transformers,
#   zéro cloud (les embeddings sont calculés localement, aucune donnée
#   n'est envoyée à un service externe).
#
# STATUS  : VALIDATED
# ============================================================

from __future__ import annotations

from pathlib import Path
from typing import Any

_BASE = Path(__file__).resolve().parents[2]
_CHROMA_PATH = _BASE / "data" / "memory" / "chroma"
_COLLECTION_NAME = "alfred_episodic_memory"
_EMBEDDING_MODEL = "paraphrase-multilingual-MiniLM-L12-v2"

_client: Any = None
_collection: Any = None
_embedding_fn: Any = None


class RAGNotAvailable(Exception):
    """Levée quand le système RAG sémantique n'est pas disponible."""
    pass


def is_rag_available() -> bool:
    """Vérifie si ChromaDB est installé et disponible."""
    try:
        import chromadb  # noqa: F401
        return True
    except ImportError:
        return False


def _reset_client() -> None:
    """Force la recréation du client/collection au prochain appel — utilisé
    par les tests après avoir monkeypatché _CHROMA_PATH, jamais en production.
    Ferme explicitement le client existant avant de le remplacer : sans ça,
    le handle SQLite sous-jacent reste ouvert jusqu'au passage du garbage
    collector, ce qui fait échouer le nettoyage de tmp_path sous Windows
    (PermissionError, fichier encore utilisé — trouvé le 21/08/2026)."""
    global _client, _collection
    if _client is not None:
        try:
            _client.close()
        except Exception:
            pass
    _client = None
    _collection = None


def _get_collection():
    """Client ChromaDB persistant + collection, créés paresseusement une
    seule fois (le chargement du modèle d'embeddings est coûteux — ne pas
    le refaire à chaque appel)."""
    global _client, _collection, _embedding_fn

    if _collection is not None:
        return _collection

    import chromadb
    from chromadb.utils import embedding_functions

    _CHROMA_PATH.mkdir(parents=True, exist_ok=True)
    _client = chromadb.PersistentClient(path=str(_CHROMA_PATH))

    if _embedding_fn is None:
        _embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name=_EMBEDDING_MODEL
        )

    _collection = _client.get_or_create_collection(
        name=_COLLECTION_NAME,
        embedding_function=_embedding_fn,
    )
    return _collection


def index_document(text: str, doc_id: str, metadata: dict | None = None) -> bool:
    """
    Indexe un document dans ChromaDB (upsert — réindexer un doc_id déjà
    présent met à jour son contenu plutôt que de le dupliquer).

    Args:
        text     : Texte à indexer
        doc_id   : Identifiant unique du document
        metadata : Métadonnées associées (ChromaDB refuse les valeurs None
                   dans les métadonnées — filtrées ici)

    Returns:
        True si indexé, False si RAG indisponible ou texte vide
    """
    if not is_rag_available() or not text or not text.strip():
        return False

    try:
        collection = _get_collection()
        clean_meta = {k: v for k, v in (metadata or {}).items() if v is not None}
        collection.upsert(documents=[text], ids=[doc_id], metadatas=[clean_meta or {"_empty": True}])
        return True
    except Exception:
        return False


def semantic_search(query: str, n_results: int = 5) -> list[dict]:
    """
    Recherche sémantique dans la mémoire vectorielle — retrouve un
    document par similarité de sens, pas par présence littérale du mot.

    Args:
        query     : Question en langage naturel
        n_results : Nombre de résultats

    Returns:
        [] si RAG indisponible, requête vide, ou index vide. Sinon une
        liste de {"id", "text", "metadata", "distance"} triée par
        pertinence (distance croissante = plus pertinent).
    """
    if not is_rag_available() or not query or not query.strip():
        return []

    try:
        collection = _get_collection()
        count = collection.count()
        if count == 0:
            return []

        results = collection.query(query_texts=[query], n_results=min(n_results, count))

        ids = results.get("ids", [[]])[0]
        docs = results.get("documents", [[]])[0]
        metas = results.get("metadatas", [[]])[0]
        dists = results.get("distances", [[]])[0]

        return [
            {
                "id": ids[i],
                "text": docs[i] if i < len(docs) else "",
                "metadata": metas[i] if i < len(metas) else {},
                "distance": dists[i] if i < len(dists) else None,
            }
            for i in range(len(ids))
        ]
    except Exception:
        return []


def get_rag_status() -> dict:
    """Retourne l'état du système RAG."""
    available = is_rag_available()
    indexed_count = 0
    if available:
        try:
            indexed_count = _get_collection().count()
        except Exception:
            pass

    return {
        "available":         available,
        "engine":            "chromadb" if available else None,
        "version":           "chromadb_v3" if available else "stub_v2",
        "embedding_model":   _EMBEDDING_MODEL if available else None,
        "indexed_documents": indexed_count,
        "storage_path":      str(_CHROMA_PATH),
        "planned":           "ChromaDB local + sentence-transformers — actif depuis le 18/08/2026 (clé conservée pour compat, plus vraiment 'planned')",
    }
