"""
PROJECT  : ALFRED / Cognitive Products Lab
BLOCK    : B20
FILE     : tools/dashboard_tools/dashboard_gouvernance/update_gouvernance_data.py
ROLE     : Lit _manifest.json, vérifie les fichiers de preuve sur disque,
           recalcule les scores de conformité, écrit dashboard_gouvernance_data.json

USAGE    :
    cd D:/PROJET_ALFRED/ALFRED_PC
    python tools/dashboard_tools/dashboard_gouvernance/update_gouvernance_data.py

SCHEDULE : Peut être intégré à sync_dashboards.py ou lancé via le .bat
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
MANIFEST = ROOT / "dashboard" / "dashboard_gouvernance" / "_manifest.json"
OUTPUT   = ROOT / "dashboard" / "dashboard_gouvernance" / "dashboard_gouvernance_data.json"

SCORE_WEIGHT = {"done": 1.0, "partial": 0.5, "todo": 0.0, "na": 0.0}


def check_proof(proof_files: list[str]) -> bool:
    """Retourne True si au moins un fichier de preuve existe sur disque."""
    if not proof_files:
        return False
    return any((ROOT / p).exists() for p in proof_files)


def evaluate_requirement(req: dict) -> dict:
    """
    Détermine le statut effectif d'une exigence en croisant le statut déclaré
    et la présence réelle des fichiers de preuve.
    """
    declared = req.get("status", "todo")
    proof_ok = check_proof(req.get("proof_files", []))

    # Si déclaré done/partial mais aucune preuve trouvée → dégrade à partial/todo
    if declared == "done" and not proof_ok and req.get("proof_files"):
        effective = "partial"
        flag = "proof_missing"
    elif declared == "partial" and not proof_ok and req.get("proof_files"):
        effective = "todo"
        flag = "proof_missing"
    else:
        effective = declared
        flag = "ok" if proof_ok else ("no_proof_required" if not req.get("proof_files") else "ok")

    return {
        "id": req["id"],
        "label": req["label"],
        "domain": req.get("domain", ""),
        "status": effective,
        "declared_status": declared,
        "proof_present": proof_ok,
        "flag": flag,
        "note": req.get("note", ""),
    }


def compute_norm_score(norm: dict, evaluated: list[dict]) -> dict:
    """Calcule le score d'une norme à partir des exigences évaluées."""
    if norm.get("status") != "active":
        return {
            "id": norm["id"],
            "label": norm["label"],
            "subtitle": norm.get("subtitle", ""),
            "category": norm.get("category", ""),
            "color": norm.get("color", "#647086"),
            "status": norm.get("status", "planned"),
            "planned_date": norm.get("planned_date", ""),
            "score_pct": None,
            "requirements_total": len(norm.get("requirements", [])),
            "requirements_done": 0,
            "requirements_partial": 0,
            "requirements_todo": len(norm.get("requirements", [])),
            "requirements": evaluated,
        }

    total = len(evaluated)
    if total == 0:
        return {"id": norm["id"], "score_pct": 0.0, "requirements_total": 0}

    raw_score = sum(SCORE_WEIGHT.get(r["status"], 0.0) for r in evaluated)
    score_pct = round(raw_score / total * 100, 1)

    done = sum(1 for r in evaluated if r["status"] == "done")
    partial = sum(1 for r in evaluated if r["status"] == "partial")
    todo = sum(1 for r in evaluated if r["status"] == "todo")

    return {
        "id": norm["id"],
        "label": norm["label"],
        "subtitle": norm.get("subtitle", ""),
        "category": norm.get("category", ""),
        "color": norm.get("color", "#00d4ff"),
        "status": "active",
        "score_pct": score_pct,
        "raw_score": round(raw_score, 2),
        "requirements_total": total,
        "requirements_done": done,
        "requirements_partial": partial,
        "requirements_todo": todo,
        "requirements": evaluated,
    }


def compute_global_score(norms_data: list[dict]) -> dict:
    """Score global CPL pondéré par le nombre d'exigences des normes actives."""
    active = [n for n in norms_data if n["status"] == "active"]
    if not active:
        return {"score_pct": 0.0, "grade": "?", "total_requirements": 0}

    total_reqs = sum(n["requirements_total"] for n in active)
    total_raw = sum(n.get("raw_score", 0.0) for n in active)

    if total_reqs == 0:
        return {"score_pct": 0.0, "grade": "?", "total_requirements": 0}

    score_pct = round(total_raw / total_reqs * 100, 1)
    grade = "A+" if score_pct >= 85 else "A" if score_pct >= 70 else "B" if score_pct >= 50 else "C" if score_pct >= 30 else "D"

    return {
        "score_pct": score_pct,
        "grade": grade,
        "total_requirements": total_reqs,
        "active_norms": len(active),
        "planned_norms": len(norms_data) - len(active),
    }


def build_roadmap() -> list[dict]:
    return [
        {"title": "Socle Zero Trust — 43 modules · 651 tests A+", "status": "done", "date": "Juin 2026"},
        {"title": "RGPD Art. 30 — registre 6 traitements · 0 transfert hors UE", "status": "done", "date": "Juin 2026"},
        {"title": "SMSI ISO 27001 — classification C1→C4, journalisation, MFA", "status": "done", "date": "Juin 2026"},
        {"title": "Dashboard Conformité Réglementaire dynamique (7 normes)", "status": "done", "date": "Juin 2026"},
        {"title": "RGPD — portabilité Art. 20 + consentement Art. 9 formel", "status": "active", "date": "V2 2026"},
        {"title": "ISO 27001 — PCA, revue de direction, gestion vulnérabilités", "status": "planned", "date": "Q3 2026"},
        {"title": "AI Act — HITL, registre risques IA, gouvernance données", "status": "planned", "date": "Q4 2026"},
        {"title": "NIS2 — procédure signalement incidents (ANSSI/CERT-FR)", "status": "planned", "date": "Q4 2026"},
        {"title": "VLAN isolation PC Alfred · micro-segmentation réseau (ISO A.8.20)", "status": "planned", "date": "Q3 2026"},
        {"title": "HDS — hébergement données santé ARTHUR (Décret 2018-137)", "status": "future", "date": "V2 2027"},
        {"title": "SecNumCloud — infrastructure souveraine + audit ANSSI", "status": "future", "date": "V3 2027"},
        {"title": "PASSI — pentest qualifié ANSSI annuel", "status": "future", "date": "V3 2027"},
    ]


def build() -> dict:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    scoring_weights = manifest["_meta"]["scoring"]

    norms_data = []
    for norm in manifest["norms"]:
        evaluated = [evaluate_requirement(req) for req in norm.get("requirements", [])]
        norms_data.append(compute_norm_score(norm, evaluated))

    global_score = compute_global_score(norms_data)

    return {
        "_meta": {
            "project": "ALFRED / Cognitive Products Lab",
            "file": "dashboard_gouvernance_data.json",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "generated_by": "update_gouvernance_data.py",
            "manifest_version": manifest["_meta"]["version"],
            "scoring": scoring_weights,
        },
        "global": global_score,
        "norms": norms_data,
        "roadmap": build_roadmap(),
    }


def main() -> None:
    print("\n=== ALFRED — Mise à jour conformité réglementaire ===\n")

    if not MANIFEST.exists():
        print(f"  [ERREUR] Manifest introuvable : {MANIFEST}")
        return

    data = build()

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    g = data["global"]
    print(f"  Score CPL global : {g['score_pct']}% — Grade {g['grade']}")
    print(f"  Normes actives : {g['active_norms']} · Exigences totales : {g['total_requirements']}\n")

    for norm in data["norms"]:
        if norm["status"] == "active":
            bar = f"{norm['score_pct']:5.1f}%"
            print(f"  [{norm['id']:12s}] {bar}  ({norm['requirements_done']} OK · "
                  f"{norm['requirements_partial']} partial · {norm['requirements_todo']} todo)")
        else:
            print(f"  [{norm['id']:12s}] PLANIFIÉ  ({norm.get('planned_date', '')})")

    print(f"\n  Fichier : {OUTPUT}")
    print("=" * 52)


if __name__ == "__main__":
    main()
