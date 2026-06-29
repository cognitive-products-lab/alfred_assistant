"""
Ajoute "block": "b18" dans le champ metadata de tous les KU.
Ne touche pas les fichiers qui l'ont déjà.
"""
import json
from pathlib import Path

ROOT = Path("D:/PROJET_ALFRED/ALFRED_PC")
KNOWLEDGES = ROOT / "knowledges"

total = updated = skipped = errors = 0

for f in sorted(KNOWLEDGES.rglob("*.json")):
    if "index" in f.parts or "backup" in f.name.lower():
        continue
    try:
        data = json.loads(f.read_text(encoding="utf-8"))
        if data.get("type") != "knowledge_unit":
            continue
        total += 1
        meta = data.get("metadata", {})
        if meta.get("block") == "b18":
            skipped += 1
            continue
        meta["block"] = "b18"
        data["metadata"] = meta
        f.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        updated += 1
    except Exception as e:
        errors += 1
        print(f"  ERR {f}: {e}")

print(f"Total KU  : {total}")
print(f"Mis à jour: {updated}")
print(f"Déjà OK   : {skipped}")
print(f"Erreurs   : {errors}")
