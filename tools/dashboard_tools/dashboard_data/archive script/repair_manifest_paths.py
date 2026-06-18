"""
PROJECT      : ALFRED
BLOCK        : DASHBOARD
FILE         : tools/dashboard_tools/dashboard_data/repair_manifest_paths.py
ROLE         : Repare et normalise les chemins de fichiers dans dashboard_data_manifest.json

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-05-10
UPDATED      : 2026-05-23
VERSION      : V1.1
STATUS       : STABLE

DESCRIPTION :
Lit dashboard_data_manifest.json, indexe tous les fichiers reels du projet,
tente de corriger automatiquement les chemins invalides par correspondance
sur le nom de fichier (un seul match = reparation auto), produit un backup
et un rapport JSON dans reports/manifest_repair_report.json.
"""

from pathlib import Path
import json
from collections import defaultdict

ROOT = Path(__file__).resolve().parents[3]

MANIFEST_PATH = ROOT / "dashboard" / "dashboard_data" / "dashboard_data_manifest.json"
BACKUP_PATH = ROOT / "dashboard" / "_archive" / "dashboard_data_manifest_before_auto_repair.json"

# =========================
# LOAD MANIFEST
# =========================

with MANIFEST_PATH.open("r", encoding="utf-8") as f:
    manifest = json.load(f)

# backup
with BACKUP_PATH.open("w", encoding="utf-8") as f:
    json.dump(manifest, f, indent=2, ensure_ascii=False)

# =========================
# INDEX REAL FILES
# =========================

real_files = list(ROOT.rglob("*"))

filename_index = defaultdict(list)

for file in real_files:
    if file.is_file():
        filename_index[file.name].append(
            str(file.relative_to(ROOT)).replace("\\", "/")
        )

# =========================
# REPAIR
# =========================

repaired = 0
unresolved = []

for block_id, block in manifest.get("blocks", {}).items():

    expected_files = block.get("expected_files", [])
    new_expected = []

    for old_path in expected_files:

        normalized = old_path.replace("\\", "/")

        full_old = ROOT / normalized

        # fichier existe déjà
        if full_old.exists():
            new_expected.append(normalized)
            continue

        filename = Path(normalized).name

        matches = filename_index.get(filename, [])

        # un seul match = réparation auto
        if len(matches) == 1:
            new_expected.append(matches[0])
            repaired += 1
            print(f"[REPAIRED] {normalized}")
            print(f"           -> {matches[0]}")

        else:
            new_expected.append(normalized)
            unresolved.append({
                "missing": normalized,
                "matches": matches
            })

    block["expected_files"] = new_expected

# =========================
# SAVE
# =========================

with MANIFEST_PATH.open("w", encoding="utf-8") as f:
    json.dump(manifest, f, indent=2, ensure_ascii=False)

REPORT_PATH = ROOT / "reports" / "manifest_repair_report.json"

with REPORT_PATH.open("w", encoding="utf-8") as f:
    json.dump({
        "repaired_count": repaired,
        "unresolved": unresolved
    }, f, indent=2, ensure_ascii=False)

print("\n=========================")
print(f"REPAIRED : {repaired}")
print(f"UNRESOLVED : {len(unresolved)}")
print("=========================")
print(f"Report : {REPORT_PATH}")