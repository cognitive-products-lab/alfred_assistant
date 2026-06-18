"""
PROJECT  : ALFRED / Cognitive Products Lab
BLOCK    : B20
FILE     : tools/dashboard_tools/dashboard_gouvernance/generate_audit_report.py
ROLE     : Génère un rapport d'audit gouvernance daté (.md) depuis dashboard_gouvernance_data.json
           Rapport complet : score global, détail par norme, exigences, preuves, plan d'action, roadmap

USAGE    :
    cd D:/PROJET_ALFRED/ALFRED_PC
    python tools/dashboard_tools/dashboard_gouvernance/generate_audit_report.py

    Le rapport est écrit dans :
      dashboard/dashboard_gouvernance/reports/audit_gouvernance_YYYYMMDD_HHMMSS.md

SCHEDULE : Appelé automatiquement par update_gouvernance_data.py à chaque régénération
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT        = Path(__file__).resolve().parents[3]
DATA_FILE   = ROOT / "dashboard/dashboard_gouvernance/dashboard_gouvernance_data.json"
MANIFEST    = ROOT / "dashboard/dashboard_gouvernance/_manifest.json"
REPORTS_DIR = ROOT / "dashboard/dashboard_gouvernance/reports"

# ── Helpers ────────────────────────────────────────────────────────────────────

STATUS_ICON  = {"done": "✅", "partial": "⚠️", "todo": "❌"}
STATUS_LABEL = {"done": "Atteint", "partial": "Partiel", "todo": "À faire"}
GRADE_DESC   = {
    "A+": "Excellence — conformité totale",
    "A":  "Très bon — quelques points à consolider",
    "B":  "Satisfaisant — plan d'action requis",
    "C":  "En cours — chantier structurant",
    "D":  "Insuffisant — actions correctives urgentes",
}


def _bar(pct: float, width: int = 20) -> str:
    filled = round(pct / 100 * width)
    return "█" * filled + "░" * (width - filled)


def _priority(req: dict) -> str:
    """Déduit une priorité d'action depuis le domaine et le statut."""
    domain = req.get("domain", "")
    status = req.get("status", "todo")
    if status == "done":
        return ""
    high_domains = {"Droits personnes", "Données sensibles", "Accountability", "Incidents"}
    return "🔴 HAUTE" if domain in high_domains else "🟡 MOYENNE"


# ── Sections du rapport ────────────────────────────────────────────────────────

def section_header(data: dict, manifest: dict, ts: str) -> str:
    g      = data["global"]
    score  = g["score_pct"]
    grade  = g["grade"]
    grade_txt = GRADE_DESC.get(grade, "")
    gen_at = data["_meta"].get("generated_at", ts)[:19].replace("T", " ")

    return f"""# Rapport d'Audit Gouvernance — ALFRED / Cognitive Products Lab

> **Date d'audit :** {ts}
> **Données générées le :** {gen_at} UTC
> **Manifest version :** {data["_meta"].get("manifest_version", "?")}
> **Généré par :** generate_audit_report.py

---

## 1. Synthèse Exécutive

| Indicateur | Valeur |
|---|---|
| **Score CPL global** | **{score}%** |
| **Grade** | **{grade}** — {grade_txt} |
| Normes actives évaluées | {g["active_norms"]} |
| Normes planifiées | {g["planned_norms"]} |
| Exigences totales (normes actives) | {g["total_requirements"]} |

```
Score global  [{_bar(score)}]  {score}%
```

"""


def section_scores_par_norme(norms: list) -> str:
    lines = ["## 2. Scores par norme\n"]
    lines.append("| Norme | Score | Grade | OK | Partial | À faire | Total |")
    lines.append("|---|---|---|---|---|---|---|")

    for n in norms:
        if n["status"] == "active":
            sc   = n["score_pct"]
            ok   = n["requirements_done"]
            par  = n["requirements_partial"]
            todo = n["requirements_todo"]
            tot  = n["requirements_total"]
            grade = "A+" if sc >= 85 else "A" if sc >= 70 else "B" if sc >= 50 else "C" if sc >= 30 else "D"
            lines.append(f"| **{n['id']}** | `[{_bar(sc, 12)}]` {sc}% | {grade} | {ok} | {par} | {todo} | {tot} |")
        else:
            lines.append(f"| {n['id']} | _(planifié — {n.get('planned_date', '?')})_ | — | — | — | — | {n.get('requirements_total', '?')} |")

    lines.append("")
    return "\n".join(lines) + "\n"


def section_detail_norme(norm: dict) -> str:
    if norm["status"] != "active":
        return ""

    nid   = norm["id"]
    label = norm["label"]
    sub   = norm.get("subtitle", "")
    sc    = norm["score_pct"]
    reqs  = norm.get("requirements", [])

    lines = [
        f"### {nid} — {label}",
        f"_{sub}_  ",
        f"**Score : {sc}%** `[{_bar(sc)}]`  ",
        f"{norm['requirements_done']} atteints · {norm['requirements_partial']} partiels · {norm['requirements_todo']} à faire",
        "",
        "| ID | Exigence | Domaine | Statut | Preuve | Priorité |",
        "|---|---|---|---|---|---|",
    ]

    for r in reqs:
        icon    = STATUS_ICON.get(r["status"], "❓")
        lbl     = STATUS_LABEL.get(r["status"], r["status"])
        proof   = "✓" if r.get("proof_present") else ("—" if not r.get("declared_status") else "⚠ manquante")
        flag    = " _(preuve manquante)_" if r.get("flag") == "proof_missing" else ""
        note    = f" _{r['note']}_" if r.get("note") else ""
        prio    = _priority(r)
        lines.append(
            f"| {r['id']} | {r['label']}{note}{flag} | {r['domain']} | {icon} {lbl} | {proof} | {prio} |"
        )

    lines.append("")
    return "\n".join(lines) + "\n"


def section_plan_action(norms: list) -> str:
    lines = ["## 4. Plan d'action — Exigences à traiter\n"]

    haute  = []
    moyenne = []

    for norm in norms:
        if norm["status"] != "active":
            continue
        for r in norm.get("requirements", []):
            if r["status"] == "done":
                continue
            prio = _priority(r)
            entry = {
                "norm_id":  norm["id"],
                "req_id":   r["id"],
                "label":    r["label"],
                "domain":   r.get("domain", ""),
                "status":   r["status"],
                "note":     r.get("note", ""),
                "flag":     r.get("flag", ""),
                "prio":     prio,
            }
            if "HAUTE" in prio:
                haute.append(entry)
            else:
                moyenne.append(entry)

    def fmt_entry(e: dict) -> str:
        icon = STATUS_ICON.get(e["status"], "❓")
        note = f"\n  > _{e['note']}_" if e["note"] else ""
        flag = "\n  > ⚠ fichier de preuve introuvable" if e["flag"] == "proof_missing" else ""
        return f"- **[{e['norm_id']}]** `{e['req_id']}` — {e['label']} {icon}{note}{flag}"

    if haute:
        lines.append("### 4.1 Priorité HAUTE\n")
        lines.extend(fmt_entry(e) for e in haute)
        lines.append("")

    if moyenne:
        lines.append("### 4.2 Priorité MOYENNE\n")
        lines.extend(fmt_entry(e) for e in moyenne)
        lines.append("")

    if not haute and not moyenne:
        lines.append("_Aucune action requise — toutes les exigences actives sont atteintes._\n")

    return "\n".join(lines) + "\n"


def section_preuves_manquantes(norms: list) -> str:
    missing = []
    for norm in norms:
        if norm["status"] != "active":
            continue
        for r in norm.get("requirements", []):
            if r.get("flag") == "proof_missing":
                missing.append({"norm": norm["id"], "req": r["id"], "label": r["label"]})

    if not missing:
        return "## 5. Fichiers de preuve\n\n✅ Tous les fichiers de preuve déclarés sont présents sur disque.\n\n"

    lines = [
        "## 5. Fichiers de preuve manquants\n",
        "Les exigences suivantes sont déclarées mais sans fichier de preuve détecté sur disque.",
        "Le statut a été rétrogradé automatiquement.\n",
        "| Norme | Exigence | Label |",
        "|---|---|---|",
    ]
    for m in missing:
        lines.append(f"| {m['norm']} | `{m['req']}` | {m['label']} |")
    lines.append("")
    return "\n".join(lines) + "\n"


def section_normes_planifiees(norms: list) -> str:
    planned = [n for n in norms if n["status"] != "active"]
    if not planned:
        return ""

    lines = ["## 6. Normes planifiées\n"]
    for n in planned:
        lines.append(f"### {n['id']} — {n['label']}")
        lines.append(f"_{n.get('subtitle', '')}_  ")
        lines.append(f"**Horizon :** {n.get('planned_date', '?')}  ")
        lines.append(f"**Périmètre :** {n.get('requirements_total', 0)} exigences à cadrer\n")

        reqs = n.get("requirements", [])
        if reqs:
            lines.append("| ID | Exigence | Domaine |")
            lines.append("|---|---|---|")
            for r in reqs:
                lines.append(f"| {r['id']} | {r['label']} | {r.get('domain', '')} |")
            lines.append("")

    return "\n".join(lines) + "\n"


def section_roadmap(items: list) -> str:
    if not items:
        return ""

    ICONS = {"done": "✅", "active": "🔵", "planned": "🟡", "future": "🔮"}
    LABELS = {"done": "Terminé", "active": "En cours", "planned": "Planifié", "future": "Futur"}

    lines = [
        "## 7. Roadmap Conformité\n",
        "| Statut | Jalon | Horizon |",
        "|---|---|---|",
    ]
    for item in items:
        icon  = ICONS.get(item["status"], "○")
        label = LABELS.get(item["status"], item["status"])
        lines.append(f"| {icon} {label} | {item['title']} | {item.get('date', '?')} |")

    lines.append("")
    return "\n".join(lines) + "\n"


def section_droits_rgpd(norms: list) -> str:
    """Section dédiée aux 5 droits RGPD — focus conformité personnelle."""
    rgpd = next((n for n in norms if n["id"] == "RGPD" and n["status"] == "active"), None)
    if not rgpd:
        return ""

    droits = {
        "RGPD-03": "Art. 15 — Accès",
        "RGPD-04": "Art. 16 — Rectification",  # ou RGPD-05
        "RGPD-05": "Art. 17 — Effacement",
        "RGPD-07": "Art. 20 — Portabilité",
        "RGPD-11": "Art. 21 — Opposition",
    }
    # Reconstruire depuis les exigences réelles
    req_map = {r["id"]: r for r in rgpd.get("requirements", [])}

    lines = [
        "## 8. Focus — Droits individuels RGPD\n",
        "| Droit | Exigence | Statut | Preuve |\n|---|---|---|---|",
    ]
    for req_id, droit_label in droits.items():
        r = req_map.get(req_id)
        if r:
            icon  = STATUS_ICON.get(r["status"], "❓")
            proof = "✓ présente" if r.get("proof_present") else "⚠ manquante"
            lines.append(f"| **{droit_label}** | {r['label']} | {icon} {STATUS_LABEL[r['status']]} | {proof} |")
        else:
            lines.append(f"| **{droit_label}** | _(non trouvé dans le manifest)_ | ❓ | — |")

    lines.append("")
    return "\n".join(lines) + "\n"


def section_footer(ts: str) -> str:
    return f"""---

## 9. Informations d'audit

| Champ | Valeur |
|---|---|
| Date du rapport | {ts} |
| Méthode d'évaluation | Vérification automatique des fichiers de preuve sur disque |
| Scoring | done = 1.0 · partial = 0.5 · todo = 0.0 |
| Pondération | Proportionnelle au nombre d'exigences par norme |
| Outil | `tools/dashboard_tools/dashboard_gouvernance/generate_audit_report.py` |
| Données source | `dashboard/dashboard_gouvernance/dashboard_gouvernance_data.json` |
| Manifest | `dashboard/dashboard_gouvernance/_manifest.json` |

> Ce rapport est généré automatiquement à chaque exécution de `update_gouvernance_data.py`.
> Il constitue la trace d'audit horodatée de l'état de conformité réglementaire d'ALFRED.
> **Cognitive Products Lab — Confidentiel interne**

"""


# ── Assemblage ─────────────────────────────────────────────────────────────────

def generate_report(data_path: Path = DATA_FILE, output_dir: Path = REPORTS_DIR) -> Path:
    data     = json.loads(data_path.read_text(encoding="utf-8"))
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8")) if MANIFEST.exists() else {}

    now = datetime.now(timezone.utc)
    ts  = now.strftime("%Y-%m-%d %H:%M UTC")
    ts_file = now.strftime("%Y%m%d_%H%M%S")

    output_dir.mkdir(parents=True, exist_ok=True)
    report_path = output_dir / f"audit_gouvernance_{ts_file}.md"

    norms    = data.get("norms", [])
    roadmap  = data.get("roadmap", [])

    # Section 3 : détail par norme active
    sec3_lines = ["## 3. Détail des exigences par norme\n"]
    for norm in norms:
        sec3_lines.append(section_detail_norme(norm))

    report = (
        section_header(data, manifest, ts)
        + section_scores_par_norme(norms)
        + "\n".join(sec3_lines) + "\n"
        + section_plan_action(norms)
        + section_preuves_manquantes(norms)
        + section_normes_planifiees(norms)
        + section_roadmap(roadmap)
        + section_droits_rgpd(norms)
        + section_footer(ts)
    )

    report_path.write_text(report, encoding="utf-8")
    return report_path


# ── Main ───────────────────────────────────────────────────────────────────────

def main() -> None:
    print("\n=== ALFRED — Génération rapport d'audit gouvernance ===\n")

    if not DATA_FILE.exists():
        print(f"  [ERREUR] Données introuvables : {DATA_FILE}")
        print("  Exécuter d'abord : python tools/dashboard_tools/dashboard_gouvernance/update_gouvernance_data.py")
        return

    path = generate_report()
    size = path.stat().st_size
    print(f"  [OK]  Rapport généré : {path}")
    print(f"        Taille : {size:,} octets")
    print(f"        Répertoire : {REPORTS_DIR}")
    print("=" * 52)


if __name__ == "__main__":
    main()
