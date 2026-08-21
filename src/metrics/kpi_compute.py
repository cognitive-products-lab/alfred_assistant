from __future__ import annotations

"""
PROJECT      : ALFRED
BLOCK        : B18
FUNCTION     : 18.32
FILE         : src/metrics/kpi_compute.py
ROLE         : Calcul réel des KPI ALFRED — phase Measure (Lean Six Sigma)

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-08-21
UPDATED      : 2026-08-21
VERSION      : V1.0
STATUS       : TESTED

DESCRIPTION :
Voir docs/architecture/vision_knowledge_training_finetuning_alfred.md, P2
(document source, section 26).
"""

"""
ALFRED — kpi_compute.py
Une fonction de calcul par KPI de base_status "KO" dans kpi_catalog.py —
aucune fonction pour un KPI "OFF" : un stub qui renverrait 0.0 ou None sans
distinction donnerait un faux sentiment de mesure. get_kpi_status_report()
est le point d'entrée unique (phase Control) : il recalcule chaque KPI KO,
le fait passer à "OK" si min_sample_size est atteint, laisse les KPI OFF
inchangés (jamais de valeur calculée pour eux).
"""

from typing import Any, Optional

from src.metrics.kpi_catalog import KPI_CATALOG, KPIDefinition
from src.metrics.request_log import read_requests


def compute_knowledge_reuse_rate() -> tuple[Optional[float], int]:
    requests = read_requests()
    if not requests:
        return None, 0
    used = sum(1 for r in requests if r.get("used_knowledge"))
    return used / len(requests), len(requests)


def compute_external_call_rate() -> tuple[Optional[float], int]:
    requests = read_requests()
    if not requests:
        return None, 0
    external = sum(1 for r in requests if not r.get("local_success"))
    return external / len(requests), len(requests)


def compute_routing_local_success_rate() -> tuple[Optional[float], int]:
    requests = read_requests()
    if not requests:
        return None, 0
    success = sum(1 for r in requests if r.get("local_success"))
    return success / len(requests), len(requests)


def compute_routing_external_escalation_rate() -> tuple[Optional[float], int]:
    requests = read_requests()
    if not requests:
        return None, 0
    escalated = sum(1 for r in requests if r.get("external_source"))
    return escalated / len(requests), len(requests)


def compute_rag_stale_knowledge_rate() -> tuple[Optional[float], int]:
    from src.knowledge.knowledge_loader import KnowledgeLoader
    from src.knowledge.freshness_checker import scan_knowledge_index

    loader = KnowledgeLoader()
    grouped = scan_knowledge_index(loader.knowledge_index)
    total = sum(len(ids) for ids in grouped.values())
    if total == 0:
        return None, 0
    stale = len(grouped["STALE"]) + len(grouped["REVALIDATION_REQUIRED"])
    return stale / total, total


def compute_training_candidate_count() -> tuple[Optional[float], int]:
    from src.training.dataset_store import current_count, list_versions

    total = 0
    for category in ("instructions", "preferences"):
        total += current_count(category)
        total += sum(v["count"] for v in list_versions(category))
    return float(total), total


def compute_training_acceptance_rate() -> tuple[Optional[float], int]:
    from src.training.dataset_store import read_current

    entries = read_current("instructions")
    if not entries:
        return None, 0
    eligible = sum(1 for e in entries if e.get("training_eligible"))
    return eligible / len(entries), len(entries)


def compute_training_dataset_size_by_version() -> tuple[Optional[dict[str, Any]], int]:
    from src.training.dataset_store import list_versions

    sizes: dict[str, Any] = {}
    total_versions = 0
    for category in ("instructions", "preferences"):
        versions = list_versions(category)
        sizes[category] = {v["version"]: v["count"] for v in versions}
        total_versions += len(versions)
    return sizes, total_versions


def compute_training_duplicate_rate() -> tuple[Optional[float], int]:
    from src.training.dataset_store import read_current

    entries = read_current("instructions")
    if not entries:
        return None, 0
    scores = [e.get("duplicate_score", 0.0) for e in entries]
    return sum(scores) / len(scores), len(entries)


_COMPUTE_FUNCTIONS = {
    "knowledge_reuse_rate": compute_knowledge_reuse_rate,
    "external_call_rate": compute_external_call_rate,
    "rag_stale_knowledge_rate": compute_rag_stale_knowledge_rate,
    "training_candidate_count": compute_training_candidate_count,
    "training_acceptance_rate": compute_training_acceptance_rate,
    "training_dataset_size_by_version": compute_training_dataset_size_by_version,
    "training_duplicate_rate": compute_training_duplicate_rate,
    "routing_local_success_rate": compute_routing_local_success_rate,
    "routing_external_escalation_rate": compute_routing_external_escalation_rate,
}


def get_kpi_status_report() -> list[dict[str, Any]]:
    """
    Recalcule chaque KPI "KO" du catalogue et résout son statut réel :
    "OK" si une valeur a pu être calculée ET que min_sample_size (si défini)
    est atteint, sinon "KO" (avec le volume actuel dans status_reason). Les
    KPI "OFF" du catalogue passent inchangés, sans valeur calculée.

    Returns:
        Une entrée par KPI du catalogue : tous les champs de
        KPIDefinition, plus "status" (résolu) et "value" (None si non
        calculable).
    """
    report: list[dict[str, Any]] = []

    for kpi in KPI_CATALOG:
        entry = {
            "kpi_id": kpi.kpi_id,
            "name": kpi.name,
            "category": kpi.category,
            "definition": kpi.definition,
            "formula": kpi.formula,
            "data_source": kpi.data_source,
            "unit": kpi.unit,
            "target": kpi.target,
            "value": None,
            "sample_size": None,
        }

        if kpi.base_status == "OFF":
            entry["status"] = "OFF"
            entry["status_reason"] = kpi.status_reason
            report.append(entry)
            continue

        compute_fn = _COMPUTE_FUNCTIONS.get(kpi.kpi_id)
        if compute_fn is None:
            # Filet de sécurité : un KPI "KO" sans fonction de calcul
            # enregistrée reste KO plutôt que de planter le rapport.
            entry["status"] = "KO"
            entry["status_reason"] = kpi.status_reason
            report.append(entry)
            continue

        value, sample_size = compute_fn()
        entry["value"] = value
        entry["sample_size"] = sample_size

        min_sample = kpi.min_sample_size or 0
        if value is not None and sample_size >= min_sample:
            entry["status"] = "OK"
            entry["status_reason"] = f"Calculé sur {sample_size} échantillon(s)."
        else:
            entry["status"] = "KO"
            entry["status_reason"] = (
                f"Volume insuffisant : {sample_size}/{min_sample} échantillon(s) requis."
                if min_sample
                else "Aucune donnée disponible pour le moment."
            )

        report.append(entry)

    return report
