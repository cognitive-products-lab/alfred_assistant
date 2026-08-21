from __future__ import annotations

"""
PROJECT      : ALFRED
BLOCK        : B18
FUNCTION     : 18.20
FILE         : src/training/dataset_store.py
ROLE         : Store JSONL versionné générique pour les datasets d'entraînement

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-08-21
UPDATED      : 2026-08-21
VERSION      : V1.0
STATUS       : TESTED

DESCRIPTION :
Voir docs/architecture/vision_knowledge_training_finetuning_alfred.md, P1
(document source, sections 12 et 17 — arborescence ALFRED_DATA et
versioning des datasets).
"""

"""
ALFRED — dataset_store.py
Réutilisé par toutes les catégories de dataset d'entraînement
(instructions/, preferences/, ...). Une "catégorie" = un sous-dossier
data/training/{categorie}/. Chaque catégorie a un fichier "courant"
(current.jsonl) où les nouvelles entrées s'accumulent, et zéro ou plusieurs
fichiers versionnés archivés (alfred_{categorie}_v0.1.jsonl, v0.2...) créés
par un bump_version() explicite.

Volontairement différent de gap_dataset.py/knowledge_candidates.py (rotation
automatique par taille, pensés comme des journaux diagnostiques) : un
dataset d'entraînement a besoin de versions stables et nommées par un
humain, pas d'une rotation opportuniste — voir document source section 17,
"une version de modèle doit toujours pouvoir être reliée à un dataset
version".
"""

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

_ROOT = Path(__file__).resolve().parents[2]
TRAINING_ROOT = _ROOT / "data" / "training"


def _category_dir(category: str) -> Path:
    d = TRAINING_ROOT / category
    d.mkdir(parents=True, exist_ok=True)
    return d


def _current_file(category: str) -> Path:
    return _category_dir(category) / "current.jsonl"


def _manifest_file(category: str) -> Path:
    return _category_dir(category) / "manifest.json"


def _read_manifest(category: str) -> dict[str, Any]:
    path = _manifest_file(category)
    if not path.exists():
        return {"category": category, "versions": []}
    return json.loads(path.read_text(encoding="utf-8"))


def _write_manifest(category: str, manifest: dict[str, Any]) -> None:
    _manifest_file(category).write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8"
    )


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    entries: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            entries.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return entries


def append_entry(category: str, entry: dict[str, Any]) -> Path:
    """Ajoute une entrée au fichier courant de la catégorie (non versionné
    tant que bump_version() n'a pas été appelé pour cette catégorie)."""
    path = _current_file(category)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    return path


def read_current(category: str, limit: Optional[int] = None) -> list[dict[str, Any]]:
    """Entrées du fichier courant (pas encore figées dans une version)."""
    entries = _read_jsonl(_current_file(category))
    if limit is not None:
        entries = entries[-limit:]
    return entries


def current_count(category: str) -> int:
    return len(read_current(category))


def list_versions(category: str) -> list[dict[str, Any]]:
    return _read_manifest(category).get("versions", [])


def read_version(category: str, version: str) -> list[dict[str, Any]]:
    versions = {v["version"]: v for v in list_versions(category)}
    entry = versions.get(version)
    if entry is None:
        return []
    return _read_jsonl(_category_dir(category) / entry["file"])


def bump_version(category: str, version: str) -> Path:
    """
    Fige le fichier courant sous un nom de version explicite
    (alfred_{category}_{version}.jsonl) et démarre un nouveau fichier
    courant vide.

    Args:
        version: identifiant choisi par un humain (ex. "v0.1", "v1.0") —
                 volontairement pas auto-incrémenté : "v0.1 -> v0.2" n'a de
                 sens que si un humain juge le contenu suffisamment
                 différent pour le justifier (document source section 17).

    Raises:
        ValueError si le fichier courant est vide (rien à figer) ou si la
        version existe déjà pour cette catégorie.
    """
    current_path = _current_file(category)
    if not current_path.exists() or current_path.stat().st_size == 0:
        raise ValueError(f"Rien à figer pour la catégorie '{category}' (fichier courant vide).")

    manifest = _read_manifest(category)
    existing_versions = {v["version"] for v in manifest.get("versions", [])}
    if version in existing_versions:
        raise ValueError(f"La version '{version}' existe déjà pour '{category}'.")

    archived_name = f"alfred_{category}_{version}.jsonl"
    archived_path = _category_dir(category) / archived_name
    current_path.rename(archived_path)

    manifest.setdefault("versions", []).append({
        "version": version,
        "file": archived_name,
        "count": len(_read_jsonl(archived_path)),
        "created_at": datetime.now(timezone.utc).isoformat(),
    })
    _write_manifest(category, manifest)

    return archived_path
