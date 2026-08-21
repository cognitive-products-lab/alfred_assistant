from __future__ import annotations

"""
PROJECT      : ALFRED
BLOCK        : B18
FUNCTION     : 18.33
FILE         : src/metrics/rag_evaluation.py
ROLE         : Recall@K / Precision@K contre le Golden Dataset

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-08-21
UPDATED      : 2026-08-21
VERSION      : V1.0
STATUS       : TESTED

DESCRIPTION :
Voir docs/architecture/vision_knowledge_training_finetuning_alfred.md, P2
(document source, section 26 — KPI RAG).
"""

"""
ALFRED — rag_evaluation.py
N'invente aucune valeur pour un cas Golden Dataset sans vérité terrain :
seuls les cas portant relevant_knowledge_ids
(src.training.golden_dataset.add_golden_case) participent au calcul.
Sans cas labellisé, retourne (None, None, 0) plutôt qu'un faux 0% —
même principe que evaluation.py pour les dimensions subjectives.
"""

from typing import Any, Callable, Optional

from src.training.golden_dataset import list_golden_cases


def _recall_precision_for_case(
    retrieved_ids: list[str], relevant_ids: list[str], k: int
) -> tuple[float, float]:
    top_k = retrieved_ids[:k]
    relevant_set = set(relevant_ids)
    hits = len(set(top_k) & relevant_set)

    recall = hits / len(relevant_set) if relevant_set else 0.0
    precision = hits / len(top_k) if top_k else 0.0
    return recall, precision


def compute_recall_precision_at_k(
    retriever: Callable[[str], list[str]],
    k: int = 5,
    category: Optional[str] = None,
) -> dict[str, Any]:
    """
    Args:
        retriever : callable(prompt) -> liste de knowledge_id classés par
                    pertinence décroissante — ex.
                    lambda p: KnowledgeRetrievalEngine().retrieve(p).knowledge_ids.
        k          : profondeur de coupe (top-K).
        category   : limite aux cas Golden Dataset d'une catégorie.

    Returns:
        {"recall_at_k": float | None, "precision_at_k": float | None,
         "k": int, "labeled_cases": int, "results": [...]}

        recall_at_k/precision_at_k sont None si aucun cas labellisé
        (relevant_knowledge_ids) n'existe pour la sélection demandée.
    """
    cases = [
        c for c in list_golden_cases(category)
        if c.get("relevant_knowledge_ids")
    ]

    results: list[dict[str, Any]] = []
    for case in cases:
        retrieved_ids = retriever(case["prompt"])
        recall, precision = _recall_precision_for_case(
            retrieved_ids, case["relevant_knowledge_ids"], k
        )
        results.append({
            "case_id": case["case_id"],
            "prompt": case["prompt"],
            "relevant_knowledge_ids": case["relevant_knowledge_ids"],
            "retrieved_ids": retrieved_ids[:k],
            "recall": recall,
            "precision": precision,
        })

    if not results:
        return {
            "recall_at_k": None, "precision_at_k": None,
            "k": k, "labeled_cases": 0, "results": [],
        }

    avg_recall = sum(r["recall"] for r in results) / len(results)
    avg_precision = sum(r["precision"] for r in results) / len(results)

    return {
        "recall_at_k": avg_recall,
        "precision_at_k": avg_precision,
        "k": k,
        "labeled_cases": len(results),
        "results": results,
    }
