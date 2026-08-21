from __future__ import annotations

"""
PROJECT      : ALFRED
BLOCK        : B18
FUNCTION     : 18.25
FILE         : src/training/lora_pipeline.py
ROLE         : Contrat du pipeline de fine-tuning LoRA/QLoRA — NON IMPLÉMENTÉ

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-08-21
UPDATED      : 2026-08-21
VERSION      : V0.0
STATUS       : NOT_IMPLEMENTED

DESCRIPTION :
Voir docs/architecture/vision_knowledge_training_finetuning_alfred.md, P3
(document source, sections 18-21).
"""

"""
ALFRED — lora_pipeline.py

STATUT : NON IMPLÉMENTÉ — en attente de matériel compatible (mesure faite
le 21/08/2026, voir doc de vision). Les fonctions ci-dessous définissent le
contrat exact qui sera implémenté une fois le matériel disponible :
signatures et docstrings stables dès maintenant, pour que l'intégration
future avec adapter_registry.py et dataset_store.py n'ait pas à changer de
forme.

Aucune fonction n'appelle un modèle réel — lever NotImplementedError plutôt
que de simuler un entraînement serait trompeur (le document source, section
21, exige une évaluation réelle avant tout déploiement ; un pipeline factice
produirait un faux sentiment de progrès).

Dépendances prévues (pas encore ajoutées à requirements — inutiles tant que
non implémenté) : peft, transformers, bitsandbytes, accelerate.
"""

from dataclasses import dataclass
from typing import Any


@dataclass
class TrainingRunConfig:
    """Paramètres d'un entraînement LoRA/QLoRA — document source section 18."""
    base_model: str
    dataset_category: str
    dataset_version: str
    method: str = "qlora"  # "lora" | "qlora"
    rank: int = 8
    learning_rate: float = 2e-4
    epochs: int = 1


def prepare_training_run(config: TrainingRunConfig) -> dict[str, Any]:
    """
    Doit à terme : valider que le dataset versionné existe
    (dataset_store.read_version), détecter le matériel disponible et
    refuser si incompatible, charger le modèle de base — sans lancer
    d'entraînement.

    Raises:
        NotImplementedError : en attente de matériel compatible — voir
        docs/architecture/vision_knowledge_training_finetuning_alfred.md, P3.
    """
    raise NotImplementedError(
        "prepare_training_run() : en attente de matériel compatible — voir "
        "docs/architecture/vision_knowledge_training_finetuning_alfred.md, P3."
    )


def run_lora_finetuning(config: TrainingRunConfig) -> dict[str, Any]:
    """
    Doit à terme : lancer un entraînement LoRA/QLoRA réel (peft +
    transformers + bitsandbytes) et retourner un artefact directement
    passable à adapter_registry.register_adapter() (adapter_version,
    base_model, dataset_versions, training_config).

    Raises:
        NotImplementedError : voir prepare_training_run().
    """
    raise NotImplementedError(
        "run_lora_finetuning() : en attente de matériel compatible — voir "
        "docs/architecture/vision_knowledge_training_finetuning_alfred.md, P3."
    )
