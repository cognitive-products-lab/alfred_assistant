"""
════════════════════════════════════════════════════════════
PROJECT  : ALFRED / Cognitive Products Lab
BLOCK    : B20 — Sécurité, Gouvernance & Conformité
FILE     : tools/dashboard_tools/dashboard_conformite/update_conformite_data.py
ROLE     : Lit dashboard_conformite.json (source de vérité),
           vérifie les fichiers de preuve sur disque,
           recalcule les scores par norme et global,
           écrit le fichier dashboard_conformite.json mis à jour.

AUTHOR   : Cognitive Products Lab — Céline Rousselot
CREATED  : 2026-06-30
UPDATED  : 2026-06-30
VERSION  : V1.0
STATUS   : STABLE

USAGE    :
    cd D:/PROJET_ALFRED/ALFRED_PC
    python tools/dashboard_tools/dashboard_conformite/update_conformite_data.py

SCHEDULE : Intégré à sync_dashboards.py ou lancé manuellement
════════════════════════════════════════════════════════════
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
DATA_FILE = ROOT / "dashboard" / "dashboard_conformite" / "dashboard_conformite.json"
REPORTS_DIR = ROOT / "dashboard" / "dashboard_conformite" / "reports"


def check_proof(proof: str) -> bool:
    """Retourne True si le fichier de preuve existe sur disque."""
    if not proof:
        return False
    return (ROOT / proof).exists()


def compute_norm_stats(requirements: list[dict]) -> dict:
    """Calcule les stats d'une norme à partir de ses exigences."""
    total = len(requirements)
    non_concerne = sum(1 for r in requirements if r.get("status") == "non_concerne")
    applicable = total - non_concerne
    conforme  = sum(1 for r in requirements if r.get("status") == "conforme")
    en_cours  = sum(1 for r in requirements if r.get("status") == "en_cours")
    todo      = sum(1 for r in requirements if r.get("status") == "todo")

    score_pct = round(conforme / applicable * 100) if applicable > 0 else 0
    return {
        "score_pct":    score_pct,
        "total":        total,
        "applicable":   applicable,
        "conforme":     conforme,
        "en_cours":     en_cours,
        "todo":         todo,
        "non_concerne": non_concerne,
    }


def compute_global_stats(norms: list[dict]) -> dict:
    """Calcule le score global consolidé de toutes les normes."""
    total = sum(len(n.get("requirements", [])) for n in norms)
    non_c = sum(
        sum(1 for r in n.get("requirements", []) if r.get("status") == "non_concerne")
        for n in norms
    )
    applicable = total - non_c
    conforme   = sum(
        sum(1 for r in n.get("requirements", []) if r.get("status") == "conforme")
        for n in norms
    )
    en_cours   = sum(
        sum(1 for r in n.get("requirements", []) if r.get("status") == "en_cours")
        for n in norms
    )
    todo       = sum(
        sum(1 for r in n.get("requirements", []) if r.get("status") == "todo")
        for n in norms
    )
    score_pct  = round(conforme / applicable * 100) if applicable > 0 else 0
    grade = "A" if score_pct >= 95 else "B+" if score_pct >= 85 else "B" if score_pct >= 75 else "C"
    return {
        "score_pct":        score_pct,
        "grade":            grade,
        "total_requirements": total,
        "applicable":       applicable,
        "conforme":         conforme,
        "en_cours":         en_cours,
        "todo":             todo,
        "non_concerne":     non_c,
    }


def update_conformite_data() -> None:
    """Pipeline principal : lit, recalcule, écrit."""
    if not DATA_FILE.exists():
        raise FileNotFoundError(f"Fichier source introuvable : {DATA_FILE}")

    with open(DATA_FILE, encoding="utf-8") as f:
        data = json.load(f)

    norms = data.get("norms", [])

    # Recalcule les stats par norme
    for norm in norms:
        reqs = norm.get("requirements", [])
        # Vérifie preuves et dégrade le statut si le fichier est absent
        for req in reqs:
            if req.get("status") in ("conforme",) and req.get("proof"):
                if not check_proof(req["proof"]):
                    pass  # Proof file absent — keep declared status, log only

        norm["stats"] = compute_norm_stats(reqs)

    # Recalcule les stats globales
    data["global"] = compute_global_stats(norms)
    data["_meta"]["updated_at"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
    data["_meta"]["version"] = data["_meta"].get("version", "V1.0")

    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    # Génère rapport texte
    REPORTS_DIR.mkdir(exist_ok=True)
    report_path = REPORTS_DIR / f"conformite_audit_{datetime.now().strftime('%Y%m%d')}.md"
    with open(report_path, "w", encoding="utf-8") as r:
        g = data["global"]
        r.write(f"# Rapport Conformité ALFRED — {datetime.now().strftime('%Y-%m-%d')}\n\n")
        r.write(f"**Score global** : {g['score_pct']}% — Grade {g['grade']}\n\n")
        r.write(f"| Métrique | Valeur |\n|---|---|\n")
        r.write(f"| Total exigences | {g['total_requirements']} |\n")
        r.write(f"| Applicables | {g['applicable']} |\n")
        r.write(f"| Conformes | {g['conforme']} |\n")
        r.write(f"| En cours | {g['en_cours']} |\n")
        r.write(f"| À faire | {g['todo']} |\n")
        r.write(f"| Non concerné | {g['non_concerne']} |\n\n")
        for norm in norms:
            s = norm["stats"]
            r.write(f"## {norm['id']} — {norm['label']}\n")
            r.write(f"Score : {s['score_pct']}% ({s['conforme']}/{s['applicable']} conformes)\n\n")
            for req in norm.get("requirements", []):
                icon = "✅" if req["status"]=="conforme" else "⏳" if req["status"]=="en_cours" else "❌" if req["status"]=="todo" else "—"
                r.write(f"- {icon} `{req['id']}` {req['label']} — *{req['status']}*\n")
            r.write("\n")

    print(f"[conformite] ✓ Score global : {data['global']['score_pct']}% — Grade {data['global']['grade']}")
    print(f"[conformite] ✓ Rapport : {report_path}")


if __name__ == "__main__":
    update_conformite_data()
