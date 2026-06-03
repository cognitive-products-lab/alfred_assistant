"""
PROJECT      : ALFRED
BLOCK        : DASHBOARD
FUNCTION     : XX.XX
FILE         : tools/dashboard_tools/dashboard_data/compare_manifest_target_complet.py
ROLE         : Comparaison complete du manifest courant contre les cibles V1 et complete

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-05-10
UPDATED      : 2026-05-23
VERSION      : V1.1
STATUS       : STABLE

DESCRIPTION :
Lit dashboard_data_manifest.json, dashboard_manifest_target_v1.json et
dashboard_manifest_target_complet.json, effectue une comparaison multi-version
et produit des rapports JSON detailles d avancement par bloc.
"""

import sys
from pathlib import Path
import json
from datetime import datetime
import argparse

ROOT = Path(__file__).resolve().parents[3]
DASHBOARD_DIR = ROOT / "dashboard" / "dashboard_data"
DASHBOARD_DIR.mkdir(parents=True, exist_ok=True)

MANIFEST_CURRENT  = DASHBOARD_DIR / "dashboard_data_manifest.json"
MANIFEST_V1       = DASHBOARD_DIR / "dashboard_manifest_target_v1.json"
MANIFEST_COMPLET  = DASHBOARD_DIR / "dashboard_manifest_target_complet.json"

OUTPUT_V1_JSON = DASHBOARD_DIR / "dashboard_target_report_v1.json"
OUTPUT_V1_MD   = DASHBOARD_DIR / "dashboard_target_report_v1.md"

OUTPUT_FULL_JSON = DASHBOARD_DIR / "dashboard_target_report_complet.json"
OUTPUT_FULL_MD   = DASHBOARD_DIR / "dashboard_target_report_complet.md"

def load_json(path):
    if not path.exists():
        raise FileNotFoundError(f"Introuvable : {path}")
    with open(path, "r", encoding="utf-8-sig") as f:
        return json.load(f)

def get_status(rel):
    path = ROOT / rel
    if not path.exists(): return "absent"
    if path.is_file() and path.stat().st_size == 0: return "empty"
    if path.suffix.lower() == ".json":
        try:
            with open(path, encoding="utf-8-sig") as f: json.load(f)
            return "coded"
        except Exception: return "partial"
    if path.suffix.lower() == ".py":
        c = path.read_text(encoding="utf-8-sig", errors="ignore").strip()
        if not c: return "empty"
        if "def " in c or "class " in c: return "coded"
        return "partial"
    return "coded"

def biz(status):
    if status in ("absent","empty"): return "A coder"
    if status in ("partial","created","coded"): return "Code partiel"
    if status == "valid": return "Version finale"
    return "A verifier"

def normalize(m):
    return m.get("blocks", m)

def run(target_path, output_json, output_md):
    if not target_path.exists():
        print(f"[ALFRED] Fichier cible introuvable : {target_path.name} — comparaison ignoree.")
        print(f"[ALFRED] Creez ce fichier dans dashboard/dashboard_data/ pour activer la comparaison.")
        return
    if not MANIFEST_CURRENT.exists():
        print(f"[ALFRED] Manifest courant introuvable : {MANIFEST_CURRENT.name}")
        return
    target  = load_json(target_path)
    current = load_json(MANIFEST_CURRENT)
    t_blocks = normalize(target)
    c_blocks = normalize(current)
    current_files = {f.replace("\\", "/")
                     for b in c_blocks.values()
                     for f in b.get("expected_files", [])}
    report = dict(last_update=datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                  manifest_target=target_path.name,
                  missing_files=[], existing_not_tracked=[], files=[])
    md = [f"# Rapport ALFRED vs {target_path.name}\n"]
    for bid, block in t_blocks.items():
        label = block.get("label","")
        md.append(f"## {bid.upper()} -- {label}\n")
        for f in block.get("expected_files", []):
            fc = f.replace("\\", "/")
            exists  = (ROOT / fc).exists()
            tracked = fc in current_files
            st = get_status(fc)
            bz = biz(st)
            report["files"].append(dict(block=bid,path=fc,exists=exists,tracked=tracked,status=st,business_status=bz))
            if not exists:
                report["missing_files"].append(fc)
                md.append(f"- MANQUANT {bz} -- {fc}")
            elif not tracked:
                report["existing_not_tracked"].append(fc)
                md.append(f"- NON_TRACKE {bz} -- {fc}")
            else:
                md.append(f"- OK {bz} -- {fc}")
        md.append("")
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps(report, indent=4, ensure_ascii=False), encoding="utf-8")
    output_md.write_text("\n".join(md), encoding="utf-8")
    print(f"Rapport vs {target_path.name}")
    print(f"Manquants   : {len(report['missing_files'])}")
    print(f"Non trackes : {len(report['existing_not_tracked'])}")
    return report

def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--target", choices=["v1", "complet", "both"], default="both")
    args = parser.parse_args()

    if args.target in ("v1", "both"):
        run(
            MANIFEST_V1,
            DASHBOARD_DIR / "dashboard_target_report_v1.json",
            DASHBOARD_DIR / "dashboard_target_report_v1.md"
        )

    if args.target in ("complet", "both"):
        run(
            MANIFEST_COMPLET,
            DASHBOARD_DIR / "dashboard_target_report_complet.json",
            DASHBOARD_DIR / "dashboard_target_report_complet.md"
        )

if __name__ == '__main__':
    main()
