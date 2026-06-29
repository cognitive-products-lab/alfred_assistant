"""
Synchronise knowledge_registry.json et le manifest b18
avec les 114 nouveaux KU migrés, puis régénère les stats.
"""
import json, subprocess
from pathlib import Path
from datetime import date

ROOT    = Path("D:/PROJET_ALFRED/ALFRED_PC")
ROOT_K  = ROOT / "knowledges"
REG     = ROOT_K / "index" / "knowledge_registry.json"
MANIFEST= ROOT / "dashboard/dashboard_data/dashboard_data_manifest.json"
TODAY   = date.today().isoformat()

# 1. Collecter tous les KU
all_ku = {}
for f in sorted(ROOT_K.rglob("*.json")):
    if "index" in f.parts or "backup" in f.name.lower():
        continue
    try:
        d = json.load(open(f, encoding="utf-8"))
        if d.get("type") == "knowledge_unit":
            ku_id = d.get("id", str(f.relative_to(ROOT_K).with_suffix("")))
            all_ku[ku_id] = {
                "id": ku_id,
                "title": d.get("title", ""),
                "domain": d.get("domain", ""),
                "subdomain": d.get("subdomain", ""),
                "status": d.get("status", "validated"),
                "priority": d.get("priority", "medium"),
                "file": str(f.relative_to(ROOT)).replace("\\", "/"),
                "tags": d.get("tags", []),
            }
    except:
        pass

print(f"Total KU sur disque : {len(all_ku)}")

# 2. Mettre à jour le registry
reg = json.load(open(REG, encoding="utf-8"))
existing_ids = {ku["id"] for ku in reg.get("knowledge_units", [])}
new_entries = [v for k, v in all_ku.items() if k not in existing_ids]
reg["knowledge_units"].extend(new_entries)
reg["total_count"] = len(reg["knowledge_units"])
reg["last_updated"] = TODAY
json.dump(reg, open(REG, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print(f"Registry : {len(new_entries)} nouveaux ajoutés -> total {reg['total_count']}")

# 3. Mettre à jour le manifest b18
manifest = json.load(open(MANIFEST, encoding="utf-8"))
b18 = manifest["blocks"]["b18"]
existing_b18 = set(b18.get("expected_files", []))
new_paths = []
for ku_id, info in all_ku.items():
    p = info["file"]
    if p not in existing_b18:
        new_paths.append(p)
        b18["expected_files"].append(p)

total_b18 = len(b18["expected_files"])
b18["expected_count"] = total_b18
ku_count = len(all_ku)
b18["sub_targets"]["knowledge_files"] = ku_count
if b18.get("target_full_files_count", 0) < total_b18:
    b18["target_full_files_count"] = total_b18

json.dump(manifest, open(MANIFEST, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print(f"Manifest b18 : {len(new_paths)} chemins ajoutés -> {total_b18} total")

# 4. Régénérer le dashboard
print("\nRégénération dashboard_data.json...")
result = subprocess.run(
    ["python", "tools/dashboard_tools/dashboard_data/update_dashboard_data.py"],
    cwd=str(ROOT), capture_output=True, text=True
)
for line in result.stdout.strip().split("\n")[-15:]:
    print(line)
if result.returncode != 0:
    print("STDERR:", result.stderr[-500:])
