"""
════════════════════════════════════════════════════════════
PROJECT  : ALFRED / Cognitive Products Lab
BLOCK    : B20 — Sécurité, Gouvernance & Conformité
FILE     : tools/dashboard_tools/dashboard_risk_impact/update_risk_impact_data.py
ROLE     : Recalcule les scores de risque (brut, résiduel, global),
           met à jour les compteurs par niveau et statut,
           écrit dashboard_risk_impact.json mis à jour.

AUTHOR   : Cognitive Products Lab — Céline Rousselot
CREATED  : 2026-06-30
UPDATED  : 2026-06-30
VERSION  : V1.0
STATUS   : STABLE

USAGE    :
    cd D:/PROJET_ALFRED/ALFRED_PC
    python tools/dashboard_tools/dashboard_risk_impact/update_risk_impact_data.py

SCHEDULE : Mensuel ou à chaque révision de la matrice des risques
════════════════════════════════════════════════════════════
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parents[3]
DATA_FILE   = ROOT / "dashboard" / "dashboard_risk_impact" / "dashboard_risk_impact.json"
REPORTS_DIR = ROOT / "dashboard" / "dashboard_risk_impact" / "reports"

THRESHOLDS = {
    "faible":   (1, 4),
    "moyen":    (5, 9),
    "eleve":    (10, 14),
    "critique": (15, 25),
}


def score_to_level(score: int) -> str:
    for level, (lo, hi) in THRESHOLDS.items():
        if lo <= score <= hi:
            return level
    return "critique"


def recompute_global(risks: list[dict]) -> dict:
    """Recalcule le score global à partir des risques."""
    score_brut     = sum(r.get("score", r.get("likelihood", 1) * r.get("impact", 1)) for r in risks)
    score_residuel = sum(r.get("residual_score", 0) for r in risks)
    max_possible   = len(risks) * 25 if risks else 1
    reduction_pct  = round((1 - score_residuel / max(score_brut, 1)) * 100) if score_brut else 0

    by_level  = {"critique": 0, "eleve": 0, "moyen": 0, "faible": 0}
    by_status = {"ouvert": 0, "contrôlé": 0, "accepté": 0, "clos": 0}
    for r in risks:
        level  = r.get("level", score_to_level(r.get("score", 0)))
        status = r.get("status", "ouvert")
        by_level[level]   = by_level.get(level, 0) + 1
        by_status[status] = by_status.get(status, 0) + 1

    return {
        "total":              len(risks),
        "critique":           by_level["critique"],
        "eleve":              by_level["eleve"],
        "moyen":              by_level["moyen"],
        "faible":             by_level["faible"],
        "ouvert":             by_status.get("ouvert", 0),
        "controle":           by_status.get("contrôlé", 0),
        "accepte":            by_status.get("accepté", 0),
        "clos":               by_status.get("clos", 0),
        "risk_score_brut":    score_brut,
        "risk_score_residuel": score_residuel,
        "reduction_pct":      reduction_pct,
        "last_review":        datetime.now().strftime("%Y-%m-%d"),
        "next_review":        "2026-09-30",
    }


def update_risk_impact_data() -> None:
    """Pipeline principal."""
    if not DATA_FILE.exists():
        raise FileNotFoundError(f"Fichier source introuvable : {DATA_FILE}")

    with open(DATA_FILE, encoding="utf-8") as f:
        data = json.load(f)

    risks = data.get("risks", [])

    # Recalcule score et niveau pour chaque risque
    for r in risks:
        score = r.get("likelihood", 1) * r.get("impact", 1)
        r["score"] = score
        r["level"] = score_to_level(score)

    data["global"] = recompute_global(risks)
    data["_meta"]["updated_at"] = datetime.now(timezone.utc).isoformat(timespec="seconds")

    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    # Rapport
    REPORTS_DIR.mkdir(exist_ok=True)
    report_path = REPORTS_DIR / f"risk_report_{datetime.now().strftime('%Y%m%d')}.md"
    with open(report_path, "w", encoding="utf-8") as r:
        g = data["global"]
        r.write(f"# Rapport Risques & Impact ALFRED — {datetime.now().strftime('%Y-%m-%d')}\n\n")
        r.write(f"**Score brut total** : {g['risk_score_brut']} | "
                f"**Score résiduel** : {g['risk_score_residuel']} | "
                f"**Réduction** : {g['reduction_pct']}%\n\n")
        r.write(f"| Niveau | Nombre |\n|---|---|\n")
        r.write(f"| Critique | {g['critique']} |\n")
        r.write(f"| Élevé    | {g['eleve']} |\n")
        r.write(f"| Modéré   | {g['moyen']} |\n")
        r.write(f"| Faible   | {g['faible']} |\n\n")
        level_icon = {"critique":"🔴","eleve":"🟠","moyen":"🟡","faible":"🟢"}
        for risk in sorted(risks, key=lambda x: x.get("score", 0), reverse=True):
            icon = level_icon.get(risk.get("level","moyen"), "—")
            r.write(f"- {icon} `{risk['id']}` **{risk['name']}** — score {risk['score']}/25 "
                    f"→ résiduel {risk.get('residual_score',0)}/25 ({risk.get('status','—')})\n")

    print(f"[risk_impact] ✓ Score brut: {g['risk_score_brut']} | "
          f"Résiduel: {g['risk_score_residuel']} | Réduction: {g['reduction_pct']}%")
    print(f"[risk_impact] ✓ Rapport : {report_path}")


if __name__ == "__main__":
    update_risk_impact_data()
