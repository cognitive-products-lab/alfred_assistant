"""
Compte et liste les KU sans "type": "knowledge_unit" dans le dossier knowledges/.
Ce sont des anciens KU qui n'ont pas encore été migrés vers schema v1.2.
"""
import json
from pathlib import Path
from collections import defaultdict

ROOT = Path("D:/PROJET_ALFRED/ALFRED_PC/knowledges")
SKIP = {"index"}

old_ku = []
by_domain = defaultdict(list)

for f in sorted(ROOT.rglob("*.json")):
    if any(s in f.parts for s in SKIP):
        continue
    if "backup" in f.name.lower():
        continue
    try:
        d = json.load(open(f, encoding="utf-8"))
        if d.get("type") == "knowledge_unit":
            continue  # déjà migré
        # Heuristique : un KU ancien a "status", "summary" ou "knowledge"
        if "summary" in d or "knowledge" in d or "core_definition" in d:
            rel = str(f.relative_to(ROOT))
            old_ku.append(rel)
            # domaine = premier dossier après knowledges/
            parts = f.relative_to(ROOT).parts
            domain = parts[0] if len(parts) > 1 else "root"
            by_domain[domain].append(rel)
    except Exception as e:
        pass

print(f"Total anciens KU (sans type=knowledge_unit) : {len(old_ku)}")
print()
for domain, files in sorted(by_domain.items()):
    print(f"  {domain:40s} : {len(files)} fichiers")
