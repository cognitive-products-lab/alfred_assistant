"""
════════════════════════════════════════════════════════════
PROJECT  : ALFRED / Cognitive Products Lab
BLOCK    : B20 — Sécurité, Gouvernance & Conformité
FILE     : tools/dashboard_tools/dashboard_vulnerabilites/update_vulnerabilites_data.py
ROLE     : Scanne les logs pip-audit, met à jour les statuts de vulnérabilités,
           recalcule les compteurs par sévérité/statut,
           écrit dashboard_vulnerabilites.json mis à jour.

AUTHOR   : Cognitive Products Lab — Céline Rousselot
CREATED  : 2026-06-30
UPDATED  : 2026-06-30
VERSION  : V1.0
STATUS   : STABLE

USAGE    :
    cd D:/PROJET_ALFRED/ALFRED_PC
    python tools/dashboard_tools/dashboard_vulnerabilites/update_vulnerabilites_data.py

SCHEDULE : Chaque dimanche après pip-audit (via sync_dashboards.py)
════════════════════════════════════════════════════════════
"""

from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
DATA_FILE  = ROOT / "dashboard" / "dashboard_vulnerabilites" / "dashboard_vulnerabilites.json"
LOGS_DIR   = ROOT / "logs" / "security"
REPORTS_DIR = ROOT / "dashboard" / "dashboard_vulnerabilites" / "reports"


def run_pip_audit() -> dict:
    """Lance pip-audit et retourne le résultat JSON (ou vide si indisponible)."""
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip_audit", "--format", "json"],
            capture_output=True, text=True, timeout=120,
        )
        if result.returncode == 0:
            return {"vulns": [], "status": "ok", "raw": result.stdout}
        return {"vulns": [], "status": "error", "stderr": result.stderr[:500]}
    except FileNotFoundError:
        return {"vulns": [], "status": "unavailable", "note": "pip-audit non installé"}
    except Exception as exc:
        return {"vulns": [], "status": "error", "note": str(exc)}


def recompute_summary(vulnerabilities: list[dict]) -> dict:
    """Recalcule les compteurs résumé à partir du catalogue."""
    by_sev: dict[str, int] = {"critique": 0, "eleve": 0, "moyen": 0, "faible": 0}
    by_st: dict[str, int]  = {"ouvert": 0, "en_cours": 0, "contrôlé": 0, "résolu": 0, "accepté": 0}
    for v in vulnerabilities:
        sev = v.get("severity", "faible")
        st  = v.get("status", "ouvert")
        by_sev[sev] = by_sev.get(sev, 0) + 1
        by_st[st]   = by_st.get(st, 0) + 1
    return {
        "total":       len(vulnerabilities),
        "by_severity": by_sev,
        "by_status":   by_st,
    }


def update_vulnerabilites_data() -> None:
    """Pipeline principal."""
    if not DATA_FILE.exists():
        raise FileNotFoundError(f"Fichier source introuvable : {DATA_FILE}")

    with open(DATA_FILE, encoding="utf-8") as f:
        data = json.load(f)

    # Recalcule la synthèse
    data["summary"] = recompute_summary(data.get("vulnerabilities", []))

    # Met à jour la date du dernier scan dans config
    now_str = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S")
    data.setdefault("config", {}).setdefault("scan", {})["last"] = now_str[:10]

    # Ajoute une entrée historique
    audit_result = run_pip_audit()
    history_entry = {
        "date":        datetime.now().strftime("%Y-%m-%d"),
        "type":        "pip-audit",
        "result":      audit_result.get("status", "error"),
        "vulns_found": len(audit_result.get("vulns", [])),
        "duration_s":  None,
        "report":      None,
    }
    data.setdefault("scan_history", []).insert(0, history_entry)
    data["scan_history"] = data["scan_history"][:20]  # garde 20 entrées max

    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    # Rapport
    REPORTS_DIR.mkdir(exist_ok=True)
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    report_path = REPORTS_DIR / f"vuln_report_{datetime.now().strftime('%Y%m%d')}.md"
    with open(report_path, "w", encoding="utf-8") as r:
        s = data["summary"]
        r.write(f"# Rapport Vulnérabilités ALFRED — {datetime.now().strftime('%Y-%m-%d')}\n\n")
        r.write(f"**Total** : {s['total']} | Élevées : {s['by_severity'].get('eleve',0)} | "
                f"Modérées : {s['by_severity'].get('moyen',0)} | Ouvertes : {s['by_status'].get('ouvert',0)}\n\n")
        for v in data.get("vulnerabilities", []):
            icon = "🔴" if v["severity"]=="critique" else "🟠" if v["severity"]=="eleve" else "🟡" if v["severity"]=="moyen" else "🟢"
            r.write(f"- {icon} `{v['id']}` **{v['name']}** — {v['status']}\n")
            r.write(f"  _{v.get('description','')}_\n")
            r.write(f"  → Remédiation : {v.get('remediation','—')}\n\n")

    s = data["summary"]
    print(f"[vulnerabilites] ✓ {s['total']} vulnérabilités | "
          f"Élevées: {s['by_severity'].get('eleve',0)} | "
          f"Ouvertes: {s['by_status'].get('ouvert',0)}")
    print(f"[vulnerabilites] ✓ Rapport : {report_path}")


if __name__ == "__main__":
    update_vulnerabilites_data()
