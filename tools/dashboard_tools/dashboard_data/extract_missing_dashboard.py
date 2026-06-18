"""
PROJECT      : ALFRED
BLOCK        : DASHBOARD
FILE         : tools/dashboard_tools/dashboard_data/extract_missing_dashboard.py
ROLE         : Extrait les fichiers manquants depuis dashboard_data.json et genere un rapport

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-05-10
UPDATED      : 2026-05-23
VERSION      : V1.1
STATUS       : STABLE

DESCRIPTION :
Lit dashboard_data.json, identifie tous les blocs ayant des fichiers manquants
(files_missing), et genere reports/missing_dashboard_paths.txt avec le detail
par bloc.
"""

from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[3]
DATA = ROOT / "dashboard" / "dashboard_data" / "dashboard_data.json"
REPORT = ROOT / "reports" / "missing_dashboard_paths.txt"

with DATA.open("r", encoding="utf-8") as f:
    data = json.load(f)

lines = []

for block in data.get("blocks", []):
    block_id = block.get("id")
    label = block.get("label")
    missing = block.get("files_missing", [])

    if missing:
        lines.append(f"\n=== {block_id} | {label} | {len(missing)} missing ===")
        for path in missing:
            lines.append(path)

REPORT.parent.mkdir(parents=True, exist_ok=True)
REPORT.write_text("\n".join(lines), encoding="utf-8")

print(f"Rapport généré : {REPORT}")