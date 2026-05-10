# ============================================================
# ALFRED — src/memory/rag_stub.py
# Bloc 02.04 — Mémoire sémantique & RAG
#
# STATUT V2 : STUB — Interface stable, implémentation V3+
#
# V3+ : ChromaDB local + sentence-transformers
#       embeddings sur disque externe HDD 4To
#       RTX 5080 pour vitesse d'indexation
#
# Dépendances V3+ (décommenter requirements.txt) :
#   chromadb>=0.4.0
#   sentence-transformers>=2.7.0
# ============================================================


class RAGNotAvailable(Exception):
    """Levée quand le système RAG sémantique n'est pas disponible."""
    pass


def is_rag_available() -> bool:
    """
    Vérifie si ChromaDB est installé et disponible.
    V2 : toujours False. V3+ : True si chromadb installé.
    """
    try:
        import chromadb  # noqa
        return True
    except ImportError:
        return False


def index_document(text: str, doc_id: str, metadata: dict | None = None) -> bool:
    """
    Indexe un document dans ChromaDB.
    V2 STUB → retourne False.

    Args:
        text     : Texte à indexer
        doc_id   : Identifiant unique du document
        metadata : Métadonnées associées

    Returns:
        False en V2, True si indexé en V3+
    """
    if not is_rag_available():
        return False

    # TODO V3+ :
    # from chromadb import Client
    # client = Client()
    # collection = client.get_or_create_collection("alfred_memory")
    # collection.add(documents=[text], ids=[doc_id], metadatas=[metadata or {}])
    return False


def semantic_search(query: str, n_results: int = 5) -> list[dict]:
    """
    Recherche sémantique dans la mémoire vectorielle.
    V2 STUB → retourne liste vide.

    Args:
        query     : Question en langage naturel
        n_results : Nombre de résultats

    Returns:
        [] en V2, résultats sémantiques en V3+
    """
    if not is_rag_available():
        return []

    # TODO V3+ :
    # results = collection.query(query_texts=[query], n_results=n_results)
    # return results["documents"]
    return []


def get_rag_status() -> dict:
    """Retourne l'état du système RAG."""
    return {
        "available": is_rag_available(),
        "engine":    "chromadb" if is_rag_available() else None,
        "version":   "stub_v2" if not is_rag_available() else "chromadb_v3",
        "planned":   "ChromaDB local + sentence-transformers V3+",
        "hardware":  "RTX 5080 recommandé pour indexation rapide",
    }
