from __future__ import annotations

"""
PROJECT      : ALFRED
BLOCK        : B18
FUNCTION     : 18.27
FILE         : src/training/evaluation.py
ROLE         : Pipeline d'évaluation contre le Golden Dataset

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-08-21
UPDATED      : 2026-08-21
VERSION      : V1.0
STATUS       : TESTED

DESCRIPTION :
Voir docs/architecture/vision_knowledge_training_finetuning_alfred.md, P2
(document source, sections 21-22).
"""

"""
ALFRED — evaluation.py
N'invente aucun score pour les dimensions subjectives que le document
source liste en section 21 (qualité des réponses, personnalité,
hallucinations...) : seuls les cas du Golden Dataset dotés d'un `check`
explicite (golden_dataset.add_golden_case(check=...)) sont notés
automatiquement. Les autres remontent en "pending_review" — une lecture
humaine reste le seul juge légitime pour ce qui n'est pas mécaniquement
vérifiable, cohérent avec le principe déjà appliqué dans tout ce chantier
(aucune validation automatique ne remplace un humain).

Utilisable dès aujourd'hui, indépendamment de tout adapter fine-tuné :
`responder` est n'importe quel callable prompt -> réponse, y compris le
pipeline ALFRED actuel — sert de baseline de non-régression avant même
qu'un premier adapter existe.
"""

import json
import os
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Optional

from src.training.golden_dataset import list_golden_cases

_ROOT = Path(__file__).resolve().parents[2]
REPORTS_PATH = _ROOT / "data" / "training" / "golden" / "evaluation_reports.json"
REPORTS_PATH.parent.mkdir(parents=True, exist_ok=True)


def _apply_check(response: str, check: Optional[dict[str, Any]]) -> Optional[bool]:
    """None = pas de check déterministe défini, le cas reste pending_review."""
    if not check:
        return None
    check_type = check.get("type")
    value = (check.get("value") or "").lower()
    response_lower = (response or "").lower()

    if check_type == "contains":
        return value in response_lower
    if check_type == "not_contains":
        return value not in response_lower
    return None


def _read_reports() -> list[dict[str, Any]]:
    if not REPORTS_PATH.exists():
        return []
    return json.loads(REPORTS_PATH.read_text(encoding="utf-8")).get("reports", [])


def _save_report(report: dict[str, Any]) -> None:
    reports = _read_reports()
    reports.append(report)
    tmp_path = REPORTS_PATH.with_suffix(".json.tmp")
    tmp_path.write_text(
        json.dumps({"reports": reports}, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    os.replace(tmp_path, REPORTS_PATH)


def run_evaluation(
    responder: Callable[[str], str],
    category: Optional[str] = None,
    run_label: str = "",
) -> dict[str, Any]:
    """
    Exécute le Golden Dataset (ou une catégorie) contre `responder` et
    produit un rapport — voir document source section 21 (comparer
    Current vs Candidate) et section 23 (les rapports d'évaluation font
    partie de ce qu'il faut conserver pour l'audit/rollback).

    Args:
        responder  : callable(prompt) -> réponse. Peut être le pipeline
                     ALFRED actuel, un adapter candidat une fois
                     src.training.lora_pipeline implémenté, ou tout autre
                     système comparable.
        category    : limite l'évaluation à une catégorie de
                     golden_dataset.GOLDEN_CASE_CATEGORIES.
        run_label   : identifiant libre pour retrouver ce rapport ensuite
                     (ex. un adapter_version).

    Returns:
        {"run_id", "run_label", "timestamp", "total", "passed", "failed",
         "pending_review", "results": [...]}
    """
    cases = list_golden_cases(category)
    results: list[dict[str, Any]] = []

    for case in cases:
        response = responder(case["prompt"])
        passed = _apply_check(response, case.get("check"))
        results.append({
            "case_id": case["case_id"],
            "category": case["category"],
            "prompt": case["prompt"],
            "response": response,
            "expected_behavior": case["expected_behavior"],
            "passed": passed,
        })

    report = {
        "run_id": f"eval_{uuid.uuid4().hex[:12]}",
        "run_label": run_label,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "total": len(results),
        "passed": sum(1 for r in results if r["passed"] is True),
        "failed": sum(1 for r in results if r["passed"] is False),
        "pending_review": sum(1 for r in results if r["passed"] is None),
        "results": results,
    }
    _save_report(report)
    return report


def list_reports(run_label: Optional[str] = None) -> list[dict[str, Any]]:
    reports = _read_reports()
    if run_label is not None:
        reports = [r for r in reports if r["run_label"] == run_label]
    return reports
