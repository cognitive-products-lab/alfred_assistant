"""
PROJECT      : ALFRED
BLOCK        : TOOLS
FUNCTION     : TOOLS
FILE         : tools/generate_backlog.py
ROLE         : Genere BACKLOG.md depuis dashboard_data.json

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-06-03
UPDATED      : 2026-06-03
VERSION      : V1.0
STATUS       : ACTIVE

DESCRIPTION :
Lit dashboard_data.json, classe les fichiers par statut et genere
BACKLOG.md avec les priorites par bloc.
"""

from __future__ import annotations

import json
from pathlib import Path
from datetime import datetime

ROOT     = Path(__file__).resolve().parents[1]
WEB_JSON = ROOT.parent / "ALFRED_WEB/static/dashboard/dashboard_data.json"
LOCAL_JSON = ROOT / "dashboard/dashboard_data/dashboard_data.json"

# Choisir le JSON le plus recent
def load_json() -> dict:
    for p in [LOCAL_JSON, WEB_JSON]:
        if p.exists():
            with open(p, encoding="utf-8") as f:
                return json.load(f)
    raise FileNotFoundError("dashboard_data.json introuvable")


STATUS_PRIORITY = {
    "absent":      1,
    "to_start":    2,
    "empty":       3,
    "partial":     4,
    "created":     5,
    "coded":       6,
    "structural":  7,
    "tested":      8,
    "validated":   9,
    "alias_existing":     10,
    "merged_in_other_file": 11,
    "archive":     12,
}

STATUS_EMOJI = {
    "absent":      "❌",
    "to_start":    "🔲",
    "empty":       "🔲",
    "partial":     "🟡",
    "created":     "🟡",
    "coded":       "🟦",
    "structural":  "⚙️",
    "tested":      "🧪",
    "validated":   "✅",
    "alias_existing":     "🔗",
    "merged_in_other_file": "🔀",
    "archive":     "📦",
}

STATUS_LABEL = {
    "absent":      "A créer",
    "to_start":    "A démarrer",
    "empty":       "Vide",
    "partial":     "Partiel",
    "created":     "Créé (squelette)",
    "coded":       "Codé — à tester",
    "structural":  "Structurel",
    "tested":      "Testé — à valider",
    "validated":   "Validé ✅",
    "alias_existing": "Alias",
    "merged_in_other_file": "Fusionné",
    "archive":     "Archivé",
}


def generate(d: dict) -> str:
    gc     = d.get("global_status_counts", {})
    blocks = d.get("blocks", [])
    total  = max(d.get("total_files_detected", 1), 1)
    now    = datetime.now().strftime("%d/%m/%Y %H:%M")
    update = d.get("last_update", "?")

    lines = []
    lines.append(f"# ALFRED — BACKLOG & RÉFÉRENTIEL FICHIERS")
    lines.append(f"")
    lines.append(f"> Généré le {now} depuis `dashboard_data.json` (mis à jour le {update})")
    lines.append(f"> Progression technique : **{d.get('global_progress',0)}%** · Full projet : **{d.get('global_full_project_progress',0)}%**")
    lines.append(f"> {d.get('total_files_detected',0)} fichiers détectés / {d.get('total_target_full_files',0)} cible full")
    lines.append(f"")

    # ── Synthèse globale ────────────────────────────────────────────────────
    lines.append(f"## Synthèse globale")
    lines.append(f"")
    lines.append(f"| Statut | Nb | % | Priorité |")
    lines.append(f"|--------|---:|--:|----------|")

    todo_statuses = ["absent","to_start","empty","partial","created","coded","tested"]
    done_statuses = ["validated","structural","alias_existing","merged_in_other_file","archive"]

    for s in todo_statuses + done_statuses:
        v = gc.get(s, 0)
        if not v:
            continue
        prio = "🔴 Urgent" if s in ("absent","to_start","empty") else \
               "🟡 Sprint" if s in ("partial","created","coded") else \
               "🧪 Tests" if s == "tested" else "✅ Done"
        lines.append(f"| {STATUS_EMOJI.get(s,'')} {STATUS_LABEL.get(s,s)} | {v} | {round(v/total*100,1)}% | {prio} |")
    lines.append(f"")

    # ── Par bloc ────────────────────────────────────────────────────────────
    lines.append(f"## Backlog par bloc")
    lines.append(f"")

    for b in blocks:
        bid   = b.get("id","?").upper()
        label = b.get("label","")
        pct   = b.get("progress", 0)
        sc    = b.get("status_counts", {})
        files = b.get("files", [])
        miss  = b.get("missing_count", 0)

        val  = sc.get("validated", 0)
        tst  = sc.get("tested", 0)
        cod  = sc.get("coded", 0)
        par  = sc.get("partial",0) + sc.get("empty",0) + sc.get("created",0)
        stru = sc.get("structural", 0)

        # Icone de statut bloc
        if pct == 100:
            icon = "✅"
        elif pct >= 80:
            icon = "🟢"
        elif pct >= 60:
            icon = "🟡"
        elif pct > 0:
            icon = "🟠"
        else:
            icon = "❌"

        lines.append(f"### {icon} {bid} — {label} `{pct}%`")
        lines.append(f"")
        lines.append(f"| KPI | Valeur |")
        lines.append(f"|-----|--------|")
        lines.append(f"| Validés | {val} |")
        lines.append(f"| Testés | {tst} |")
        lines.append(f"| Codés (à tester) | {cod} |")
        lines.append(f"| Partiels | {par} |")
        lines.append(f"| Structurels | {stru} |")
        lines.append(f"| Manquants | {miss} |")
        lines.append(f"")
        if b.get("roadmap_note"):
            lines.append(f"> {b['roadmap_note']}")
            lines.append(f"")

        # Fichiers nécessitant une action (statut < tested)
        action_files = [
            f for f in files
            if STATUS_PRIORITY.get(f.get("status",""), 99) < STATUS_PRIORITY["tested"]
            and f.get("status") not in ("structural","alias_existing","merged_in_other_file","archive")
        ]
        if action_files:
            action_files.sort(key=lambda f: STATUS_PRIORITY.get(f.get("status",""), 99))
            lines.append(f"**Fichiers à traiter :**")
            lines.append(f"")
            lines.append(f"| Fichier | Statut | Action |")
            lines.append(f"|---------|--------|--------|")
            for af in action_files[:30]:  # max 30 par bloc
                st  = af.get("status","?")
                fp  = af.get("path", af.get("file","?"))
                em  = STATUS_EMOJI.get(st,"")
                lbl = STATUS_LABEL.get(st, st)
                action = "Créer" if st in ("absent","to_start","empty") else \
                         "Compléter" if st in ("partial","created") else \
                         "Tester" if st == "coded" else lbl
                lines.append(f"| `{fp}` | {em} {lbl} | {action} |")
            if len(action_files) > 30:
                lines.append(f"| *... {len(action_files)-30} autres* | | |")
            lines.append(f"")

    # ── Fichiers codés non testés (priorité sprint) ─────────────────────────
    all_coded = []
    for b in blocks:
        for f in b.get("files", []):
            if f.get("status") == "coded":
                all_coded.append((b.get("id","?").upper(), f.get("path", f.get("file","?"))))

    if all_coded:
        lines.append(f"## 🟦 Sprint — Fichiers codés à tester ({len(all_coded)})")
        lines.append(f"")
        lines.append(f"Ces fichiers sont implémentés mais n'ont pas encore de tests.")
        lines.append(f"")
        cur_block = None
        for bid, fp in sorted(all_coded):
            if bid != cur_block:
                lines.append(f"**{bid}**")
                cur_block = bid
            lines.append(f"- `{fp}`")
        lines.append(f"")

    return "\n".join(lines)


if __name__ == "__main__":
    d = load_json()
    content = generate(d)

    out = ROOT / "BACKLOG.md"
    out.write_text(content, encoding="utf-8")
    print(f"BACKLOG.md genere : {out}")
    print(f"  {len(content.splitlines())} lignes")
