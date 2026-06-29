"""
Liste les fichiers B18 avec status partial ou coded,
en réutilisant la même logique que update_dashboard_data.py.
"""
import json, sys
from pathlib import Path

sys.path.insert(0, str(Path("D:/PROJET_ALFRED/ALFRED_PC/tools/dashboard_tools/dashboard_data")))
from update_dashboard_data import evaluate_file

ROOT = Path("D:/PROJET_ALFRED/ALFRED_PC")
MANIFEST = ROOT / "dashboard/dashboard_data/dashboard_data_manifest.json"

manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
b18_files = manifest["blocks"]["b18"]["expected_files"]

partial = []
coded = []

for rel in b18_files:
    abs_path = ROOT / rel
    info = evaluate_file(rel)
    s = info.get("status", "absent")
    if s == "partial":
        partial.append(rel)
    elif s == "coded":
        coded.append(rel)

print(f"=== PARTIAL ({len(partial)}) ===")
for f in sorted(partial):
    print(" ", f)

print(f"\n=== CODED ({len(coded)}) ===")
for f in sorted(coded):
    print(" ", f)
