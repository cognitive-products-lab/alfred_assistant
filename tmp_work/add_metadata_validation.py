"""
Ajoute un bloc metadata de validation à tous les KU existants.
Structure ajoutée après le champ "status" :

  "status": "validated",
  "metadata": {
    "created_at": "2026-06-23",
    "validated_at": "2026-06-23",
    "validated_by": "ALFRED enrichment pipeline",
    "enrichment_version": "day2",
    "schema_version": "1.2",
    "review_notes": ""
  }

Les KU qui ont déjà un bloc metadata ne sont pas modifiés.
"""
import json
from pathlib import Path
from datetime import date

ROOT = Path("D:/PROJET_ALFRED/ALFRED_PC/knowledges")
TODAY = date.today().isoformat()

# Déterminer l'enrichment_version par dossier
def get_enrichment_version(path: Path) -> str:
    parts = path.parts
    # Heuristique : les domaines du day1 = communication, cognition, cuisine, culture/manga
    # day2 = culture/webtoon, culture/romance, human/humour, human/seduction_relations,
    #         human/vie_privee, cpl/usage_professionnel
    day1_domains = {"communication", "cognition", "cuisine"}
    day1_subdomains = {"manga"}  # culture/manga
    day2_subdomains = {"webtoon", "romance", "humour", "seduction_relations", "vie_privee", "usage_professionnel"}

    # Trouver le domaine dans le path
    try:
        idx = list(parts).index("knowledges")
        domain = parts[idx + 1] if idx + 1 < len(parts) else ""
        subdomain = parts[idx + 2] if idx + 2 < len(parts) else ""
    except (ValueError, IndexError):
        return "day1"

    if domain in day1_domains:
        return "day1"
    if subdomain in day1_subdomains:
        return "day1"
    if subdomain in day2_subdomains:
        return "day2"
    return "day1"  # défaut pour les anciens KU

total = 0
updated = 0
skipped = 0
errors = 0

for json_file in sorted(ROOT.rglob("*.json")):
    # Ignorer les fichiers d'index
    if "index" in json_file.parts:
        continue

    try:
        content = json_file.read_text(encoding="utf-8")
        data = json.loads(content)

        # Vérifier que c'est un KU
        if data.get("type") != "knowledge_unit":
            continue

        total += 1

        # Déjà un bloc metadata complet ? Skip
        if "metadata" in data and "validated_at" in data.get("metadata", {}):
            skipped += 1
            continue

        # Construire le bloc metadata
        ev = get_enrichment_version(json_file)
        metadata_block = {
            "created_at": TODAY,
            "validated_at": TODAY,
            "validated_by": "ALFRED enrichment pipeline",
            "enrichment_version": ev,
            "schema_version": data.get("schema_version", "1.2"),
            "review_notes": ""
        }

        # Insérer le bloc metadata juste après "status"
        # Reconstruire le dict dans le bon ordre
        new_data = {}
        for k, v in data.items():
            new_data[k] = v
            if k == "status":
                new_data["metadata"] = metadata_block

        # Si "status" n'existait pas, ajouter metadata à la fin
        if "metadata" not in new_data:
            new_data["metadata"] = metadata_block

        json_file.write_text(
            json.dumps(new_data, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )
        updated += 1
        print(f"  OK  {json_file.relative_to(ROOT)}")

    except Exception as e:
        errors += 1
        print(f"  ERR {json_file}: {e}")

print(f"\n=== Résultat ===")
print(f"  Total KU   : {total}")
print(f"  Mis à jour : {updated}")
print(f"  Déjà OK    : {skipped}")
print(f"  Erreurs    : {errors}")
