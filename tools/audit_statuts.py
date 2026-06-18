"""
PROJECT      : ALFRED
BLOCK        : TOOLS
FUNCTION     : XX.XX
FILE         : tools/audit_statuts.py
ROLE         : TO_DEFINE

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-06-03
UPDATED      : 2026-06-03
VERSION      : V1.0
STATUS       : DRAFT

DESCRIPTION :
Outils projet — description a completer.
"""

import json

with open("D:/PROJET_ALFRED/ALFRED_WEB/static/dashboard/dashboard_data.json", encoding="utf-8") as f:
    d = json.load(f)

gc     = d.get("global_status_counts", {})
blocks = d.get("blocks", [])
total  = max(d.get("total_files_detected", 1), 1)

print(f"AUDIT STATUTS — {d.get('last_update','?')}")
print(f"Fichiers : {d.get('total_files_detected',0)} detectes / {d.get('total_expected_files',0)} attendus / {d.get('total_target_full_files',0)} cible full")
print(f"Progression technique : {d.get('global_progress',0)}%   Full projet : {d.get('global_full_project_progress',0)}%")
print()

print("=" * 60)
print("REPARTITION GLOBALE")
print("=" * 60)
STATUTS = [
    ("validated",         "Valides (prod-ready)"),
    ("tested",            "Testes"),
    ("coded",             "Codes (pas encore testes)"),
    ("partial",           "Partiels"),
    ("created",           "Crees (squelette)"),
    ("empty",             "Vides"),
    ("structural",        "Structurels (config/data)"),
    ("alias_existing",    "Alias (refs)"),
    ("merged_in_other_file", "Fusionnes"),
    ("absent",            "Absents"),
    ("to_start",          "A demarrer"),
]
for key, label in STATUTS:
    v = gc.get(key, 0)
    if v:
        bar = "#" * min(40, round(v / total * 40))
        print(f"  {label:30}: {v:4}  {round(v/total*100,1):5.1f}%  {bar}")

print()
print("=" * 60)
print("PAR BLOC")
print("=" * 60)
HDR = f"  {'ID':4}  {'Label':33}  {'Tech':6}  {'Val':>4}  {'Tst':>3}  {'Cod':>4}  {'Par':>3}  {'Stru':>4}  {'Miss':>4}"
print(HDR)
print("  " + "-" * (len(HDR) - 2))

for b in blocks:
    sc   = b.get("status_counts", {})
    par  = sc.get("partial", 0) + sc.get("empty", 0) + sc.get("created", 0)
    miss = b.get("missing_count", 0)
    pct  = b.get("progress", 0)
    bid  = b.get("id", "?").upper()
    lab  = b.get("label", "")[:33]
    val  = sc.get("validated", 0)
    tst  = sc.get("tested", 0)
    cod  = sc.get("coded", 0)
    stru = sc.get("structural", 0)
    print(f"  {bid:4}  {lab:33}  {pct:5.1f}%  {val:4}  {tst:3}  {cod:4}  {par:3}  {stru:4}  {miss:4}")

print()
print("SYNTHESE")
val_t  = gc.get("validated", 0)
tst_t  = gc.get("tested", 0)
cod_t  = gc.get("coded", 0)
par_t  = gc.get("partial", 0) + gc.get("empty", 0) + gc.get("created", 0)
stru_t = gc.get("structural", 0)
abs_t  = gc.get("absent", 0) + gc.get("to_start", 0)
print(f"  Prod-ready (val+tst)  : {val_t+tst_t:4}  ({round((val_t+tst_t)/total*100,1)}%)")
print(f"  Codes (pas testes)    : {cod_t:4}  ({round(cod_t/total*100,1)}%)")
print(f"  En cours (partiels)   : {par_t:4}  ({round(par_t/total*100,1)}%)")
print(f"  Structurels           : {stru_t:4}  ({round(stru_t/total*100,1)}%)")
print(f"  A creer / absents     : {abs_t:4}  ({round(abs_t/total*100,1)}%)")
