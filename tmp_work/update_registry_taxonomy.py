"""
Met a jour knowledge_registry.json et taxonomy.json avec les nouveaux domaines.
"""
import json
from pathlib import Path

ROOT = Path("D:/PROJET_ALFRED/ALFRED_PC/knowledges")
INDEX = ROOT / "index" / "knowledge_registry.json"
TAXONOMY = ROOT / "taxonomy.json"

# ─── 1. Charger le registry actuel ───────────────────────────────────────────
registry = json.loads(INDEX.read_text(encoding="utf-8"))
existing_ids = {e["id"] for e in registry.get("entries", [])}

# ─── 2. Scanner tous les nouveaux KU et les ajouter ──────────────────────────
new_entries = []
for f in sorted(ROOT.rglob("*.json")):
    if "index" in f.parts or f.name == "taxonomy.json":
        continue
    try:
        d = json.loads(f.read_text(encoding="utf-8"))
    except Exception:
        continue
    if d.get("type") != "knowledge_unit":
        continue
    ku_id = d.get("id", "")
    if ku_id in existing_ids:
        continue
    # Nouveau KU
    new_entries.append({
        "id": ku_id,
        "domain": d.get("domain", ""),
        "subdomain": d.get("subdomain", ""),
        "title": d.get("title", ""),
        "status": d.get("status", "validated"),
        "file": str(f.relative_to(ROOT)).replace("\\", "/")
    })
    existing_ids.add(ku_id)

print(f"Nouveaux KU a ajouter au registry : {len(new_entries)}")
for e in new_entries:
    print(f"  + {e['id']}")

# ─── 3. Mettre a jour le registry ────────────────────────────────────────────
# Detecter la cle des entrees (entries ou knowledge_units)
ku_key = "knowledge_units" if "knowledge_units" in registry else "entries"
registry[ku_key] = registry.get(ku_key, []) + new_entries
registry["total_files"] = len(registry[ku_key])
registry["version"] = "3.1.0"
registry["last_update"] = "2026-06-23"

INDEX.write_text(json.dumps(registry, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"\nRegistry mis a jour : {registry['total_files']} entrees totales")

# ─── 4. Mettre a jour la taxonomy ────────────────────────────────────────────
taxonomy = json.loads(TAXONOMY.read_text(encoding="utf-8"))

new_domains = {
    "communication": {
        "description": "Communication verbale, ecrite, non-verbale, influence, digital",
        "subdomains": ["verbal", "written", "nonverbal", "influence", "digital"]
    },
    "cognition": {
        "description": "Systemes de pensee, heuristiques, biais, apprentissage, attention",
        "subdomains": ["systeme_pensee"]
    },
    "cuisine": {
        "description": "Art culinaire, techniques, cuisines du monde",
        "subdomains": ["fondamentaux", "francaise", "asiatique"]
    }
}

# Ajouter les nouveaux domaines a la taxonomy
for domain, info in new_domains.items():
    if domain not in taxonomy.get("domains", {}):
        taxonomy.setdefault("domains", {})[domain] = info
        print(f"  Domain ajoute: {domain}")
    else:
        # Mise a jour des sous-domaines
        existing_subs = set(taxonomy["domains"][domain].get("subdomains", []))
        for sub in info["subdomains"]:
            if sub not in existing_subs:
                taxonomy["domains"][domain].setdefault("subdomains", []).append(sub)
                print(f"  Subdomain ajoute: {domain}/{sub}")

# Mettre a jour version et date
taxonomy["version"] = "3.1.0"
taxonomy["last_updated"] = "2026-06-23"
taxonomy["total_subdomains"] = sum(
    len(v.get("subdomains", [])) for v in taxonomy.get("domains", {}).values()
)

TAXONOMY.write_text(json.dumps(taxonomy, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"\nTaxonomy mise a jour : {taxonomy['total_subdomains']} sous-domaines")
print("Done.")
