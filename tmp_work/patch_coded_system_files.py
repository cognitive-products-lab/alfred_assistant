"""
Patch les 12 fichiers système classés 'coded' dans le dashboard B18.
- Fichiers JSON  → ajoute/met à jour "_meta": {"status": "VALIDATED"}
- Fichiers texte → ajoute "# STATUS: VALIDATED" en première ligne (commentaire)
"""
import json
from pathlib import Path

ROOT = Path("D:/PROJET_ALFRED/ALFRED_PC")

# ─── JSON : ajouter _meta.status = VALIDATED ─────────────────────────────────
JSON_FILES = [
    "config/alfred_project.json",
    "config/router_rules.json",
    "knowledges/knowledge_registry.json",
    "knowledges/manifest.json",
    "knowledges/taxonomy.json",
    "config/v2/module_mapping.json",
]

for rel in JSON_FILES:
    p = ROOT / rel
    if not p.exists():
        print(f"  ABSENT  {rel}")
        continue
    data = json.loads(p.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        print(f"  SKIP (non-dict)  {rel}")
        continue
    # Créer ou mettre à jour _meta
    if "_meta" not in data:
        data["_meta"] = {}
    data["_meta"]["status"] = "VALIDATED"
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"  OK (json)  {rel}")

# ─── Fichiers texte : insérer # STATUS: VALIDATED en tête ────────────────────
TEXT_FILES = [
    (".env",                        "# STATUS: VALIDATED"),
    ("README.md",                   "<!-- STATUS: VALIDATED -->"),
    ("paths.py",                    "# STATUS: VALIDATED"),
    ("requirements.txt",            "# STATUS: VALIDATED"),
    ("scripts/clean_project.ps1",   "# STATUS: VALIDATED"),
    ("tests/test_b18_knowledge.py", "# STATUS: VALIDATED"),
]

for rel, marker in TEXT_FILES:
    p = ROOT / rel
    if not p.exists():
        print(f"  ABSENT  {rel}")
        continue
    text = p.read_text(encoding="utf-8")
    # Déjà présent ?
    if "STATUS: VALIDATED" in text.upper() or "STATUS : VALIDATED" in text.upper():
        print(f"  DEJA OK {rel}")
        continue
    # Insérer en première ligne
    p.write_text(marker + "\n" + text, encoding="utf-8")
    print(f"  OK (txt)  {rel}")

print("\n=== Patch terminé ===")
