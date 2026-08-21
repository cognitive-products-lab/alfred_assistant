from __future__ import annotations

"""
PROJECT      : ALFRED
BLOCK        : B18
FUNCTION     : 18.26
FILE         : src/training/golden_dataset.py
ROLE         : Golden Dataset — corpus de référence pour l'évaluation

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-08-21
UPDATED      : 2026-08-21
VERSION      : V1.0
STATUS       : TESTED

DESCRIPTION :
Voir docs/architecture/vision_knowledge_training_finetuning_alfred.md, P2
(document source, section 22).
"""

"""
ALFRED — golden_dataset.py
Corpus de cas que chaque nouvelle version doit impérativement réussir. Ne
sert JAMAIS à entraîner (section 22 : "il doit principalement servir de
référence d'évaluation afin d'éviter de biaiser les tests") — stocké
séparément d'instructions/preferences (src/training/dataset_store.py) pour
qu'aucun pipeline de training ne puisse l'absorber par erreur.

Store JSON simple (pas JSONL versionné comme dataset_store.py) : un Golden
Dataset est curé (ajout, correction ponctuelle) plutôt qu'accumulé en flux
continu — un fichier unique reflète mieux cet usage.
"""

import json
import os
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

_ROOT = Path(__file__).resolve().parents[2]
GOLDEN_PATH = _ROOT / "data" / "training" / "golden" / "golden_dataset.json"
GOLDEN_PATH.parent.mkdir(parents=True, exist_ok=True)

# Catégories proposées par le document source (section 22) — indicatives,
# pas imposées : category reste une chaîne libre.
GOLDEN_CASE_CATEGORIES = (
    "intentions_critiques", "privacy", "routage", "memoire",
    "personnalite", "refus", "outils", "rag", "conversationnel",
)


def _read_store() -> dict[str, Any]:
    if not GOLDEN_PATH.exists():
        return {"cases": []}
    return json.loads(GOLDEN_PATH.read_text(encoding="utf-8"))


def _write_store(store: dict[str, Any]) -> None:
    tmp_path = GOLDEN_PATH.with_suffix(".json.tmp")
    tmp_path.write_text(json.dumps(store, indent=2, ensure_ascii=False), encoding="utf-8")
    os.replace(tmp_path, GOLDEN_PATH)


def add_golden_case(
    prompt: str,
    category: str,
    expected_behavior: str,
    check: Optional[dict[str, Any]] = None,
    created_by: str = "manual",
) -> dict[str, Any]:
    """
    Args:
        prompt            : la question/instruction du cas de test.
        category           : voir GOLDEN_CASE_CATEGORIES (indicatif).
        expected_behavior : description en langage naturel de ce qu'une
                             bonne réponse doit faire — toujours renseigné,
                             même quand `check` est absent, pour qu'une
                             relecture humaine sache quoi juger.
        check              : optionnel, un contrôle automatisable —
                             {"type": "contains" | "not_contains",
                              "value": "..."}. Sans `check`, le cas reste
                             "pending_review" lors d'une évaluation
                             (src.training.evaluation) : ce module n'invente
                             jamais de score pour des dimensions subjectives
                             (hallucination, personnalité, pertinence...).
        created_by         : qui a ajouté ce cas.

    Returns:
        Le cas créé, avec son case_id.
    """
    case = {
        "case_id": f"golden_{uuid.uuid4().hex[:12]}",
        "prompt": prompt,
        "category": category,
        "expected_behavior": expected_behavior,
        "check": check,
        "created_by": created_by,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    store = _read_store()
    store.setdefault("cases", []).append(case)
    _write_store(store)
    return case


def list_golden_cases(category: Optional[str] = None) -> list[dict[str, Any]]:
    cases = _read_store().get("cases", [])
    if category is not None:
        cases = [c for c in cases if c["category"] == category]
    return cases


def get_golden_case(case_id: str) -> Optional[dict[str, Any]]:
    for case in _read_store().get("cases", []):
        if case["case_id"] == case_id:
            return case
    return None


def remove_golden_case(case_id: str) -> None:
    store = _read_store()
    cases = store.get("cases", [])
    remaining = [c for c in cases if c["case_id"] != case_id]
    if len(remaining) == len(cases):
        raise ValueError(f"case_id introuvable : {case_id}")
    store["cases"] = remaining
    _write_store(store)
