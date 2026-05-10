from pathlib import Path
import json
from datetime import datetime

ROOT = Path("D:/PROJET_ALFRED/ALFRED_PC")
KNOWLEDGES = ROOT / "knowledges"
OUT = KNOWLEDGES / "knowledge_registry.json"

EXCLUDED = {
    "manifest.json",
    "taxonomy.json",
    "domain_links.json",
    "retrieval_rules.json",
    "governance_rules.json",
    "knowledge_template.json",
    "knowledge_registry.json"
}

items = []

for path in sorted(KNOWLEDGES.rglob("*.json")):
    if path.name in EXCLUDED:
        continue

    rel = path.relative_to(ROOT).as_posix()
    parts = path.relative_to(KNOWLEDGES).parts

    domain = parts[0] if len(parts) > 0 else "unknown"
    subdomain = ".".join(parts[1:-1]) if len(parts) > 2 else domain
    filename = path.stem

    knowledge_id = ".".join(parts).replace(".json", "")

    item = {
        "id": knowledge_id,
        "file": rel,
        "domain": domain,
        "subdomain": subdomain,
        "filename": path.name,
        "status": "active",
        "version": "1.0.0",
        "priority": "to_review",
        "source": "filesystem_scan"
    }

    items.append(item)

registry = {
    "registry_id": "alfred_knowledge_registry_v3_2",
    "version": "3.2.0",
    "last_update": datetime.now().strftime("%Y-%m-%d"),
    "description": "Registry global généré automatiquement depuis l’arborescence réelle du dossier knowledges.",
    "root": "knowledges/",
    "mode": "local_first",
    "governance": {
        "source_of_truth": "filesystem_scan",
        "update_rule": "Relancer generate_knowledge_registry.py après ajout, suppression ou déplacement de fichiers knowledge.",
        "excluded_files": sorted(EXCLUDED)
    },
    "knowledges": items,
    "stats": {
        "total_json_files": len(items),
        "generated_from_tree": True
    }
}

with OUT.open("w", encoding="utf-8") as f:
    json.dump(registry, f, ensure_ascii=False, indent=2)

print(f"Registry généré : {OUT}")
print(f"Fichiers indexés : {len(items)}")