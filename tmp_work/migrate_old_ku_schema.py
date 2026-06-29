"""
Migre les anciens KU (sans type=knowledge_unit) vers schema v1.2 :
  - Ajoute schema_version: "1.2"
  - Ajoute type: "knowledge_unit"
  - Passe status: "validated"
  - Ajoute bloc metadata complet avec block: "b18"
  - Génère un id si absent (basé sur le chemin)
"""
import json
from pathlib import Path
from datetime import date

ROOT_K = Path("D:/PROJET_ALFRED/ALFRED_PC/knowledges")
ROOT   = Path("D:/PROJET_ALFRED/ALFRED_PC")
TODAY  = date.today().isoformat()
SKIP   = {"index"}

total = updated = skipped = errors = 0

for f in sorted(ROOT_K.rglob("*.json")):
    if any(s in f.parts for s in SKIP):
        continue
    if "backup" in f.name.lower():
        continue
    try:
        d = json.load(open(f, encoding="utf-8"))

        # Déjà migré
        if d.get("type") == "knowledge_unit":
            skipped += 1
            continue

        # Heuristique : contient du contenu KU
        if not ("summary" in d or "knowledge" in d or "core_definition" in d):
            continue

        total += 1

        # Calculer l'id depuis le chemin si absent
        if not d.get("id"):
            rel_parts = f.relative_to(ROOT_K).with_suffix("").parts
            d["id"] = "knowledges." + ".".join(rel_parts)

        # Calculer domaine/sous-domaine depuis le chemin
        parts = f.relative_to(ROOT_K).parts
        if not d.get("domain") and len(parts) >= 2:
            d["domain"] = parts[0]
        if not d.get("subdomain") and len(parts) >= 3:
            d["subdomain"] = parts[1]

        # enrichment_version
        subdomain = d.get("subdomain", "")
        day2_sub = {"webtoon","romance","humour","seduction_relations","vie_privee","usage_professionnel"}
        ev = "day2" if subdomain in day2_sub else "day1"

        # Reconstruire en ordre propre : injecter les champs manquants en tête
        new_d = {}
        new_d["schema_version"] = "1.2"
        new_d["type"] = "knowledge_unit"

        # Copier tous les champs existants, sauf ceux qu'on écrase
        skip_fields = {"schema_version", "type", "status", "metadata"}
        for k, v in d.items():
            if k not in skip_fields:
                new_d[k] = v

        new_d["status"] = "validated"
        new_d["metadata"] = {
            "created_at": TODAY,
            "validated_at": TODAY,
            "validated_by": "ALFRED enrichment pipeline",
            "enrichment_version": ev,
            "schema_version": "1.2",
            "review_notes": "migré depuis ancien format",
            "block": "b18"
        }

        f.write_text(json.dumps(new_d, ensure_ascii=False, indent=2), encoding="utf-8")
        updated += 1
        print(f"  OK  {f.relative_to(ROOT_K)}")

    except Exception as e:
        errors += 1
        print(f"  ERR {f}: {e}")

print(f"\n=== Résultat ===")
print(f"  Anciens KU migrés : {updated}")
print(f"  Déjà v1.2         : {skipped}")
print(f"  Erreurs           : {errors}")
