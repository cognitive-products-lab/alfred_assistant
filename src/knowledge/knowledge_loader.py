from __future__ import annotations

"""
PROJECT      : ALFRED
BLOCK        : GLOBAL
FUNCTION     : XX.XX
FILE         : src/knowledge/knowledge_loader.py
ROLE         : TO_DEFINE

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-06-03
UPDATED      : 2026-06-05
VERSION      : V1.1
STATUS       : TESTED

DESCRIPTION :
Module ALFRED — description a completer.
"""

"""
ALFRED — knowledge_loader.py
Charge les fichiers knowledge depuis le registry officiel du Bloc 18.
"""

import json
from pathlib import Path
from typing import Any

from src.knowledge.knowledge_schema import normalize_knowledge_metadata


class KnowledgeLoader:
    def __init__(
        self,
        project_root: str | Path = "D:/PROJET_ALFRED/ALFRED_PC",
        knowledge_root: str | Path | None = None,
        config_dir: str | Path | None = None,
        debug: bool = False,
    ):
        self.project_root = Path(project_root)
        self.knowledge_root = Path(knowledge_root) if knowledge_root else self.project_root / "knowledges"
        self.config_dir = Path(config_dir) if config_dir else self.project_root / "config"
        self.debug = debug

        self.registry_path = self.knowledge_root / "knowledge_registry.json"
        self.taxonomy_path = self.knowledge_root / "taxonomy.json"
        self.domain_links_path = self.knowledge_root / "domain_links.json"
        self.retrieval_rules_path = self.knowledge_root / "retrieval_rules.json"

        self.registry: dict[str, Any] = {}
        self.taxonomy: dict[str, Any] = {}
        self.domain_links: dict[str, Any] = {}
        self.retrieval_rules: dict[str, Any] = {}

        self.knowledge_index: dict[str, dict[str, Any]] = {}

        self.load_system_files()
        self.build_index()

    # -----------------------------------------------------
    # JSON loading
    # -----------------------------------------------------
    def read_json(self, path: Path) -> dict[str, Any]:
        if not path.exists():
            return {}

        try:
            with path.open("r", encoding="utf-8-sig") as file:
                return json.load(file)
        except json.JSONDecodeError as error:
            print(f"[KnowledgeLoader] JSON invalide : {path} — {error}")
            return {}
        except OSError as error:
            print(f"[KnowledgeLoader] Erreur lecture : {path} — {error}")
            return {}

    def load_system_files(self) -> None:
        self.registry = self.read_json(self.registry_path)
        self.taxonomy = self.read_json(self.taxonomy_path)
        self.domain_links = self.read_json(self.domain_links_path)
        self.retrieval_rules = self.read_json(self.retrieval_rules_path)

    # -----------------------------------------------------
    # Registry / index
    # -----------------------------------------------------
    def build_index(self) -> None:
        self.knowledge_index.clear()

        knowledges = self.registry.get("knowledges", [])

        for item in knowledges:
            knowledge_id = item.get("id")
            relative_file = item.get("file")
            status = item.get("status", "unknown")

            if not knowledge_id or not relative_file:
                continue

            if status not in ("active", "existing"):
                continue

            file_path = self.project_root / relative_file
            data = self.read_json(file_path)

            if not data:
                continue

            self.knowledge_index[knowledge_id] = {
                "id": knowledge_id,
                "file": relative_file,
                "path": str(file_path),
                "domain": item.get("domain", "unknown"),
                "subdomain": item.get("subdomain", "unknown"),
                "status": status,
                "registry": item,
                "data": data,
                # Provenance/fraîcheur/confidentialité — voir
                # docs/architecture/vision_knowledge_training_finetuning_alfred.md,
                # P0. Sous-dict dédié pour ne jamais entrer en collision
                # avec "status" ci-dessus (status registry actif/existant,
                # concept différent du cycle de vie VALIDATED/STALE/...).
                "metadata": normalize_knowledge_metadata(data),
            }

    # -----------------------------------------------------
    @property
    def index_size(self) -> int:
        return len(self.knowledge_index)

    def search(self, query: str, context: dict | None = None, top_k: int = 5):
        """Recherche simple par mots-clés dans l'index knowledge."""
        from dataclasses import dataclass, field as dc_field

        @dataclass
        class _Unit:
            title: str
            knowledge_id: str
            score: float

        @dataclass
        class _SearchResult:
            units: list = dc_field(default_factory=list)

        query_lower = query.lower()
        scored = []
        for kid, item in self.knowledge_index.items():
            title = item.get("title", kid)
            text = f"{title} {' '.join(item.get('tags', []))}".lower()
            score = sum(1 for word in query_lower.split() if word in text)
            if score > 0:
                scored.append(_Unit(title=title, knowledge_id=kid, score=score))
        scored.sort(key=lambda u: u.score, reverse=True)
        return _SearchResult(units=scored[:top_k])

    # Access helpers
    # -----------------------------------------------------
    def get_knowledge(self, knowledge_id: str) -> dict[str, Any] | None:
        return self.knowledge_index.get(knowledge_id)

    def get_many(self, knowledge_ids: list[str]) -> list[dict[str, Any]]:
        return [
            self.knowledge_index[kid]
            for kid in knowledge_ids
            if kid in self.knowledge_index
        ]

    def get_by_domain(self, domain: str) -> list[dict[str, Any]]:
        return [
            item for item in self.knowledge_index.values()
            if item.get("domain") == domain
        ]

    def get_by_subdomain(self, subdomain: str) -> list[dict[str, Any]]:
        return [
            item for item in self.knowledge_index.values()
            if item.get("subdomain") == subdomain
        ]

    def list_ids(self) -> list[str]:
        return sorted(self.knowledge_index.keys())

    def stats(self) -> dict[str, Any]:
        return {
            "registry_version": self.registry.get("version"),
            "taxonomy_version": self.taxonomy.get("version"),
            "domain_links_version": self.domain_links.get("version"),
            "retrieval_rules_version": self.retrieval_rules.get("version"),
            "indexed_knowledge_count": len(self.knowledge_index),
            "registry_knowledge_count": len(self.registry.get("knowledges", []))
        }

    def reload(self) -> None:
        self.load_system_files()
        self.build_index()


if __name__ == "__main__":
    loader = KnowledgeLoader()

    print("=== ALFRED KnowledgeLoader ===")
    print(loader.stats())

    print("\nPremiers IDs indexés :")
    for kid in loader.list_ids()[:10]:
        print("-", kid)