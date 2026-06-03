"""
ALFRED — knowledge_loader.py
Charge les fichiers knowledge depuis le registry officiel du Bloc 18.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class KnowledgeLoader:
    def __init__(self, project_root: str | Path = "D:/PROJET_ALFRED/ALFRED_PC"):
        self.project_root = Path(project_root)
        self.knowledge_root = self.project_root / "knowledges"

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
                "data": data
            }

    # -----------------------------------------------------
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