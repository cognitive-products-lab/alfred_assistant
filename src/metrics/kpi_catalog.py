from __future__ import annotations

"""
PROJECT      : ALFRED
BLOCK        : B18
FUNCTION     : 18.31
FILE         : src/metrics/kpi_catalog.py
ROLE         : Catalogue des KPI ALFRED — phase Define (Lean Six Sigma)

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
ALFRED — kpi_catalog.py
Un KPI par ligne du document source (section 26), avec définition, formule,
source de donnée, et un statut de base :

- "OFF" : structurellement non mesurable aujourd'hui, aucune fonction de
  calcul n'existe (voir kpi_compute.py) — nécessite soit des vérités
  terrain qui n'existent pas (Recall@K, Precision@K, grounding), soit un
  entraînement réel jamais lancé (Fine-Tuning), soit un mécanisme de
  détection qui n'existe pas encore (correction utilisateur).
- "KO" : formule et source de donnée prêtes, mais volume de données
  actuellement insuffisant pour un chiffre significatif (min_sample_size).
  Passe à "OK" dynamiquement dès que le volume est atteint — voir
  kpi_compute.get_kpi_status_report().

Ce fichier ne calcule jamais rien lui-même (phase Define, pas Measure).
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class KPIDefinition:
    kpi_id: str
    name: str
    category: str  # Knowledge | External Dependency | RAG | Training | Fine-Tuning | Routing
    definition: str
    formula: str
    data_source: str
    unit: str
    target: Optional[str]
    base_status: str  # "OFF" | "KO"
    status_reason: str
    min_sample_size: Optional[int] = None


KPI_CATALOG: list[KPIDefinition] = [
    # ── Knowledge ────────────────────────────────────────────
    KPIDefinition(
        kpi_id="knowledge_reuse_rate",
        name="Taux de réutilisation de connaissance",
        category="Knowledge",
        definition="Pourcentage de nouvelles demandes résolues grâce à une connaissance déjà acquise.",
        formula="requêtes avec knowledge_ids non vide / total des requêtes",
        data_source="src.metrics.request_log",
        unit="%",
        target=None,
        base_status="KO",
        status_reason="Dénominateur désormais tracé (request_log.py, 21/08/2026) — volume insuffisant tant que min_sample_size n'est pas atteint.",
        min_sample_size=30,
    ),

    # ── External Dependency ─────────────────────────────────
    KPIDefinition(
        kpi_id="external_call_rate",
        name="Taux d'appel externe",
        category="External Dependency",
        definition="Pourcentage de demandes nécessitant OpenAI/Anthropic. Objectif long terme : voir ce taux diminuer pour les tâches récurrentes.",
        formula="requêtes avec local_success=False / total des requêtes",
        data_source="src.metrics.request_log",
        unit="%",
        target=None,
        base_status="KO",
        status_reason="Même dénominateur que knowledge_reuse_rate — même contrainte de volume.",
        min_sample_size=30,
    ),

    # ── RAG ──────────────────────────────────────────────────
    KPIDefinition(
        kpi_id="rag_recall_at_k",
        name="Recall@K",
        category="RAG",
        definition="Proportion des connaissances réellement pertinentes qui sont effectivement retrouvées dans les K premiers résultats.",
        formula="connaissances pertinentes retrouvées / connaissances pertinentes totales",
        data_source="src.metrics.rag_evaluation + src.training.golden_dataset (champ relevant_knowledge_ids)",
        unit="%",
        target=None,
        base_status="KO",
        status_reason="Infrastructure prête (21/08/2026, golden_dataset.add_golden_case(relevant_knowledge_ids=...)) — volume insuffisant tant qu'aucun cas Golden Dataset n'est labellisé avec sa vérité terrain.",
        min_sample_size=3,
    ),
    KPIDefinition(
        kpi_id="rag_precision_at_k",
        name="Precision@K",
        category="RAG",
        definition="Proportion des K résultats retournés qui sont réellement pertinents.",
        formula="connaissances pertinentes parmi les K retournées / K",
        data_source="src.metrics.rag_evaluation + src.training.golden_dataset (champ relevant_knowledge_ids)",
        unit="%",
        target=None,
        base_status="KO",
        status_reason="Même infrastructure et même contrainte de volume que rag_recall_at_k.",
        min_sample_size=3,
    ),
    KPIDefinition(
        kpi_id="rag_grounded_rate",
        name="Taux de réponses correctement grounded",
        category="RAG",
        definition="Pourcentage de réponses dont le contenu est effectivement appuyé par la connaissance citée.",
        formula="—",
        data_source="—",
        unit="%",
        target=None,
        base_status="OFF",
        status_reason="Nécessite un jugement humain ou un modèle évaluateur (LLM-judge) — aucun des deux n'existe dans ce projet ; un score inventé serait trompeur.",
    ),
    KPIDefinition(
        kpi_id="rag_stale_knowledge_rate",
        name="Taux de connaissances périmées",
        category="RAG",
        definition="Pourcentage de fiches knowledge classées STALE ou REVALIDATION_REQUIRED.",
        formula="(STALE + REVALIDATION_REQUIRED) / total des fiches indexées",
        data_source="src.knowledge.freshness_checker.scan_knowledge_index",
        unit="%",
        target="0%",
        base_status="KO",  # OK dès le premier calcul — pas de contrainte de volume, corpus déjà réel
        status_reason="Calculable immédiatement sur le corpus réel — pas de dépendance à un volume d'usage.",
    ),

    # ── Training ─────────────────────────────────────────────
    KPIDefinition(
        kpi_id="training_candidate_count",
        name="Nombre de Training Candidates",
        category="Training",
        definition="Volume total d'exemples capturés (instructions + preferences), toutes versions confondues.",
        formula="somme des entrées courantes + versionnées, par catégorie",
        data_source="src.training.dataset_store",
        unit="count",
        target=None,
        base_status="KO",
        status_reason="Calculable immédiatement, y compris à 0 — statut résolu dynamiquement (voir kpi_compute.py).",
    ),
    KPIDefinition(
        kpi_id="training_acceptance_rate",
        name="Taux accepté après Quality Gate",
        category="Training",
        definition="Pourcentage d'entrées Instruction Dataset marquées training_eligible=True.",
        formula="entrées training_eligible=True / total des entrées courantes",
        data_source="src.training.dataset_store (catégorie instructions)",
        unit="%",
        target=None,
        base_status="KO",
        status_reason="Volume insuffisant tant qu'aucune entrée n'existe dans instructions/current.jsonl.",
        min_sample_size=1,
    ),
    KPIDefinition(
        kpi_id="training_dataset_size_by_version",
        name="Taille par version de dataset",
        category="Training",
        definition="Nombre d'entrées figées dans chaque version d'un dataset.",
        formula="dataset_store.list_versions(catégorie) → count par version",
        data_source="src.training.dataset_store",
        unit="count",
        target=None,
        base_status="KO",
        status_reason="Calculable immédiatement, y compris à 0 version — statut résolu dynamiquement.",
    ),
    KPIDefinition(
        kpi_id="training_duplicate_rate",
        name="Taux de duplication",
        category="Training",
        definition="Score de duplication moyen des entrées Instruction Dataset courantes.",
        formula="moyenne(duplicate_score) sur les entrées courantes",
        data_source="src.training.dataset_store (catégorie instructions)",
        unit="ratio 0-1",
        target=None,
        base_status="KO",
        status_reason="Volume insuffisant tant qu'aucune entrée n'existe.",
        min_sample_size=1,
    ),

    # ── Fine-Tuning ──────────────────────────────────────────
    KPIDefinition(
        kpi_id="finetuning_performance_delta",
        name="Performance avant/après",
        category="Fine-Tuning",
        definition="Écart de performance entre l'adapter courant et un candidat, sur le Golden Dataset.",
        formula="score(candidat) - score(courant)",
        data_source="—",
        unit="ratio",
        target=None,
        base_status="OFF",
        status_reason="Nécessite un adapter réellement entraîné — src.training.lora_pipeline n'est pas implémenté (en attente de matériel compatible).",
    ),
    KPIDefinition(
        kpi_id="finetuning_regressions",
        name="Régressions",
        category="Fine-Tuning",
        definition="Nombre de cas Golden Dataset réussis par l'adapter courant mais échoués par le candidat.",
        formula="—",
        data_source="—",
        unit="count",
        target="0",
        base_status="OFF",
        status_reason="Même blocage que finetuning_performance_delta.",
    ),
    KPIDefinition(
        kpi_id="finetuning_training_cost",
        name="Coût d'entraînement",
        category="Fine-Tuning",
        definition="Coût (temps machine, éventuellement cloud loué) d'un run d'entraînement.",
        formula="—",
        data_source="—",
        unit="€ ou heures",
        target=None,
        base_status="OFF",
        status_reason="Même blocage.",
    ),
    KPIDefinition(
        kpi_id="finetuning_training_duration",
        name="Durée",
        category="Fine-Tuning",
        definition="Durée totale d'un run d'entraînement.",
        formula="—",
        data_source="—",
        unit="heures",
        target=None,
        base_status="OFF",
        status_reason="Même blocage.",
    ),
    KPIDefinition(
        kpi_id="finetuning_adapter_size",
        name="Taille de l'adapter",
        category="Fine-Tuning",
        definition="Taille sur disque de l'adapter produit.",
        formula="—",
        data_source="—",
        unit="Mo",
        target=None,
        base_status="OFF",
        status_reason="Même blocage.",
    ),

    # ── Routing ──────────────────────────────────────────────
    KPIDefinition(
        kpi_id="routing_local_success_rate",
        name="Route success rate (local)",
        category="Routing",
        definition="Pourcentage de requêtes résolues directement en local (Ollama), sans repli cloud.",
        formula="requêtes avec local_success=True / total des requêtes",
        data_source="src.metrics.request_log",
        unit="%",
        target=None,
        base_status="KO",
        status_reason="Même dénominateur que knowledge_reuse_rate/external_call_rate — complémentaire d'external_call_rate.",
        min_sample_size=30,
    ),
    KPIDefinition(
        kpi_id="routing_correction_rate",
        name="Correction rate",
        category="Routing",
        definition="Pourcentage de réponses ALFRED corrigées explicitement par l'utilisateur juste après.",
        formula="—",
        data_source="—",
        unit="%",
        target=None,
        base_status="OFF",
        status_reason="Aucun mécanisme de détection d'une correction utilisateur n'existe dans le pipeline (voie 'corrections utilisateur' des Training Candidates, document source section 11, documentée mais non branchée).",
    ),
    KPIDefinition(
        kpi_id="routing_external_escalation_rate",
        name="External escalation rate",
        category="Routing",
        definition="Pourcentage de requêtes escaladées vers un fournisseur externe — vue \"routage\" du même phénomène qu'external_call_rate (catégorie \"External Dependency\").",
        formula="requêtes avec external_source non nul / total des requêtes",
        data_source="src.metrics.request_log",
        unit="%",
        target=None,
        base_status="KO",
        status_reason="Même dénominateur qu'external_call_rate — entrée distincte car le document source la liste sous une catégorie différente (Routing), même donnée sous-jacente.",
        min_sample_size=30,
    ),
]


def get_kpi(kpi_id: str) -> Optional[KPIDefinition]:
    for kpi in KPI_CATALOG:
        if kpi.kpi_id == kpi_id:
            return kpi
    return None


def list_by_category(category: str) -> list[KPIDefinition]:
    return [kpi for kpi in KPI_CATALOG if kpi.category == category]


def list_by_status(base_status: str) -> list[KPIDefinition]:
    return [kpi for kpi in KPI_CATALOG if kpi.base_status == base_status]
