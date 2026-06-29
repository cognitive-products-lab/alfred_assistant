"""
Mise a jour du knowledge_registry.json avec les 60 nouveaux KU du jour 2.
"""
import json
from pathlib import Path
from datetime import date

ROOT = Path("D:/PROJET_ALFRED/ALFRED_PC/knowledges")
REGISTRY_PATH = ROOT / "index" / "knowledge_registry.json"

registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
ku_key = "knowledge_units" if "knowledge_units" in registry else "entries"

# Collecter tous les KU existants par ID
existing_ids = {ku["id"] for ku in registry[ku_key]}

# Domaines day 2
new_paths = [
    "culture/webtoon", "human/humour", "human/seduction_relations",
    "human/vie_privee", "cpl/usage_professionnel", "culture/romance"
]

added = 0
for folder in new_paths:
    folder_path = ROOT / folder
    if not folder_path.exists():
        print(f"  SKIP (not found): {folder}")
        continue
    for f in sorted(folder_path.glob("*.json")):
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
            if data.get("type") == "knowledge_unit":
                ku_id = data.get("id", "")
                if ku_id not in existing_ids:
                    entry = {
                        "id": ku_id,
                        "title": data.get("title", ""),
                        "domain": data.get("domain", ""),
                        "subdomain": data.get("subdomain", ""),
                        "file": str(f.relative_to(ROOT)).replace("\\", "/"),
                        "status": data.get("status", "validated"),
                        "priority": data.get("priority", "medium"),
                        "tags": data.get("tags", [])
                    }
                    registry[ku_key].append(entry)
                    existing_ids.add(ku_id)
                    added += 1
                    print(f"  + {ku_id}")
        except Exception as e:
            print(f"  ERROR {f}: {e}")

total = len(registry[ku_key])
registry["total_files"] = total

# Version bump
current = registry.get("version", "3.1.0").split(".")
new_minor = int(current[1]) + 1
registry["version"] = f"{current[0]}.{new_minor}.0"
registry["last_update"] = date.today().isoformat()

REGISTRY_PATH.write_text(json.dumps(registry, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"\nRegistry v{registry['version']} — {total} KU total (+{added} ajoutés)")
