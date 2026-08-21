from __future__ import annotations

"""
PROJECT      : ALFRED
BLOCK        : B18
FUNCTION     : 18.24
FILE         : src/training/adapter_registry.py
ROLE         : Registre des adapters ALFRED — audit et rollback

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-08-21
UPDATED      : 2026-08-21
VERSION      : V1.0
STATUS       : TESTED

DESCRIPTION :
Voir docs/architecture/vision_knowledge_training_finetuning_alfred.md, P3
(document source, sections 17, 19, 23).
"""

"""
ALFRED — adapter_registry.py
Bookkeeping pur (JSON), indépendant du matériel : utilisable dès
aujourd'hui même sans qu'aucun entraînement réel n'ait eu lieu — voir
src/training/lora_pipeline.py pour le pipeline d'entraînement lui-même,
non implémenté en attente de matériel compatible.

Chaque entrée relie : base_model, dataset_version(s), training_config,
adapter_version, status (staging/production/disabled/rejected),
evaluation_report — nécessaire pour l'audit et le rollback (document
source section 17 : "une version de modèle doit toujours pouvoir être
reliée à MODEL VERSION + BASE MODEL + DATASET VERSION + TRAINING CONFIG +
ADAPTER VERSION").
"""

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

_ROOT = Path(__file__).resolve().parents[2]
REGISTRY_PATH = _ROOT / "data" / "training" / "adapters" / "adapter_registry.json"
REGISTRY_PATH.parent.mkdir(parents=True, exist_ok=True)

VALID_STATUSES = ("staging", "production", "disabled", "rejected")


def _read_registry() -> dict[str, Any]:
    if not REGISTRY_PATH.exists():
        return {"adapters": []}
    return json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))


def _write_registry(registry: dict[str, Any]) -> None:
    tmp_path = REGISTRY_PATH.with_suffix(".json.tmp")
    tmp_path.write_text(json.dumps(registry, indent=2, ensure_ascii=False), encoding="utf-8")
    os.replace(tmp_path, REGISTRY_PATH)


def register_adapter(
    adapter_version: str,
    base_model: str,
    dataset_versions: dict[str, str],
    training_config: dict[str, Any],
    status: str = "staging",
) -> dict[str, Any]:
    """
    Enregistre un adapter — jamais en "production" à l'enregistrement (voir
    document source, contrainte non négociable #9 : aucun nouvel adapter ne
    passe automatiquement en production sans évaluation).

    Args:
        adapter_version  : identifiant choisi à la main (ex. "v0.1").
        base_model        : identifiant du modèle de base (ex. "mistral:7b").
        dataset_versions : {catégorie: version} — ex.
                            {"instructions": "v0.1"} — relie l'adapter aux
                            versions exactes de dataset utilisées.
        training_config  : hyperparamètres (méthode LoRA/QLoRA, rank,
                            learning_rate...).
        status            : "staging" (défaut) — ne jamais passer
                            "production" directement à l'enregistrement.

    Raises:
        ValueError si status == "production" à l'enregistrement, si
        adapter_version existe déjà, ou si status est invalide.
    """
    if status not in VALID_STATUSES:
        raise ValueError(f"status invalide : {status} (attendu : {VALID_STATUSES})")
    if status == "production":
        raise ValueError(
            "Un adapter ne peut jamais être enregistré directement en "
            "'production' — passer par staging puis promote_to_production()."
        )

    registry = _read_registry()
    existing_versions = {a["adapter_version"] for a in registry.get("adapters", [])}
    if adapter_version in existing_versions:
        raise ValueError(f"adapter_version '{adapter_version}' existe déjà.")

    entry = {
        "adapter_version": adapter_version,
        "base_model": base_model,
        "dataset_versions": dataset_versions,
        "training_config": training_config,
        "status": status,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "evaluation_report": None,
    }
    registry.setdefault("adapters", []).append(entry)
    _write_registry(registry)
    return entry


def get_adapter(adapter_version: str) -> Optional[dict[str, Any]]:
    for entry in _read_registry().get("adapters", []):
        if entry["adapter_version"] == adapter_version:
            return entry
    return None


def list_adapters(status: Optional[str] = None) -> list[dict[str, Any]]:
    adapters = _read_registry().get("adapters", [])
    if status is not None:
        adapters = [a for a in adapters if a["status"] == status]
    return adapters


def record_evaluation(adapter_version: str, evaluation_report: dict[str, Any]) -> None:
    """Attache un rapport d'évaluation (Golden Dataset — document source
    section 22) à un adapter existant."""
    registry = _read_registry()
    for entry in registry.get("adapters", []):
        if entry["adapter_version"] == adapter_version:
            entry["evaluation_report"] = evaluation_report
            _write_registry(registry)
            return
    raise ValueError(f"adapter_version introuvable : {adapter_version}")


def promote_to_production(adapter_version: str) -> None:
    """
    Fait passer un adapter en production — désactive automatiquement tout
    adapter déjà en production (rollback trivial ensuite via
    disable_adapter()).

    Raises:
        ValueError si l'adapter n'a pas de rapport d'évaluation (contrainte
        non négociable #9) ou n'est pas trouvé.
    """
    registry = _read_registry()
    target = None
    for entry in registry.get("adapters", []):
        if entry["adapter_version"] == adapter_version:
            target = entry
        elif entry["status"] == "production":
            entry["status"] = "disabled"

    if target is None:
        raise ValueError(f"adapter_version introuvable : {adapter_version}")
    if target.get("evaluation_report") is None:
        raise ValueError(
            f"Adapter '{adapter_version}' n'a pas de rapport d'évaluation — "
            "record_evaluation() requis avant promote_to_production()."
        )

    target["status"] = "production"
    _write_registry(registry)


def disable_adapter(adapter_version: str) -> None:
    """Rollback (document source, section 23) : désactive un adapter sans
    reconstruire tout le système."""
    registry = _read_registry()
    for entry in registry.get("adapters", []):
        if entry["adapter_version"] == adapter_version:
            entry["status"] = "disabled"
            _write_registry(registry)
            return
    raise ValueError(f"adapter_version introuvable : {adapter_version}")


def get_active_production_adapter() -> Optional[dict[str, Any]]:
    for entry in list_adapters(status="production"):
        return entry
    return None
