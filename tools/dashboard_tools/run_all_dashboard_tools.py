"""
PROJECT  : ALFRED
BLOCK    : B20
FUNCTION : 20.TOOLS
FILE     : tools/dashboard_tools/run_all_dashboard_tools.py
ROLE     : Orchestrateur MANUEL complet — régénère TOUS les dashboards
           (y compris dashboard_data, dashboard_security, dashboard_test qui
           ne font PAS partie de la tâche planifiée quotidienne daily_update.py),
           puis synchronise ALFRED_PC -> ALFRED_WEB (git push).
USAGE    : python tools/dashboard_tools/run_all_dashboard_tools.py
           (ou double-clic sur run_all_dashboard_tools.bat)

⚠️ Différence avec daily_update.py :
   daily_update.py est le sous-ensemble AUTOMATISÉ (tâche planifiée Windows,
   2x/jour). Ce script est le lanceur MANUEL complet — il inclut en plus
   update_dashboard_data.py, dashboard_security.py et dashboard_test.py
   (ce dernier relance la suite pytest security_tests/, peut prendre
   plusieurs minutes).

⚠️ dashboard_quality_data est un dashboard PRIVÉ : sa régénération reste avant
   l'étape de sync et son JSON n'apparaît jamais dans SRC_* de sync_dashboards.py.
"""

from __future__ import annotations

import subprocess
import sys
from datetime import datetime
from pathlib import Path

ALFRED_PC = Path(__file__).resolve().parents[2]

STEPS = [
    {
        "label": "Dashboard DATA (suivi global des blocs)",
        "script": ALFRED_PC / "tools/dashboard_tools/dashboard_data/update_dashboard_data.py",
    },
    {
        "label": "Gouvernance data",
        "script": ALFRED_PC / "tools/dashboard_tools/dashboard_gouvernance/update_gouvernance_data.py",
    },
    {
        "label": "Conformité réglementaire data",
        "script": ALFRED_PC / "tools/dashboard_tools/dashboard_conformite/update_conformite_data.py",
    },
    {
        "label": "Vulnérabilités data",
        "script": ALFRED_PC / "tools/dashboard_tools/dashboard_vulnerabilites/update_vulnerabilites_data.py",
    },
    {
        "label": "Risques & Impact data",
        "script": ALFRED_PC / "tools/dashboard_tools/dashboard_risk_impact/update_risk_impact_data.py",
    },
    {
        "label": "Sécurité (SOC/incidents/accès)",
        "script": ALFRED_PC / "tools/dashboard_tools/dashboard_security/dashboard_security.py",
    },
    {
        "label": "Tests sécurité (pytest security_tests/ — le plus long)",
        "script": ALFRED_PC / "tools/dashboard_tools/dashboard_tests/dashboard_test.py",
    },
    {
        "label": "Knowledge registry",
        "script": ALFRED_PC / "tools/knowledge_tools/generate_knowledge_registry.py",
    },
    {
        "label": "Knowledge dashboard",
        "script": ALFRED_PC / "dashboard/dashboard_knowledges_tool/generate_knowledge_dashboard.py",
    },
    {
        "label": "Qualité data [INTERNE — non synchronisé vers le web]",
        "script": ALFRED_PC / "tools/dashboard_tools/dashboard_quality_data/update_quality_data_dashboard.py",
    },
    {
        "label": "Sync dashboards → ALFRED_WEB (+ git push)",
        "script": ALFRED_PC / "tools/sync_dashboards.py",
    },
]


def run_step(label: str, script: Path) -> bool:
    if not script.exists():
        print(f"  [SKIP]  {label}  — script introuvable : {script}")
        return True  # non bloquant

    print(f"  [RUN]   {label} ...")
    result = subprocess.run(
        [sys.executable, str(script)],
        cwd=str(ALFRED_PC),
        capture_output=True,
        text=True,
    )
    if result.stdout.strip():
        for line in result.stdout.strip().splitlines():
            print(f"          {line}")
    if result.returncode != 0:
        print(f"  [ERREUR] {label}")
        if result.stderr.strip():
            print(f"           {result.stderr.strip()[:300]}")
        return False
    print(f"  [OK]    {label}")
    return True


def main() -> None:
    ts = datetime.now().isoformat(timespec="seconds")
    print(f"\n{'='*54}")
    print(f"  ALFRED — Régénération complète de tous les dashboards")
    print(f"  {ts}")
    print(f"{'='*54}\n")

    success = True
    for step in STEPS:
        ok = run_step(step["label"], step["script"])
        if not ok:
            success = False
            print(f"  → Étape échouée, les suivantes continuent quand même.\n")
        print()

    status = "OK" if success else "PARTIEL (voir détails ci-dessus)"
    print(f"{'='*54}")
    print(f"  Terminé [{status}] — {datetime.now().strftime('%H:%M:%S')}")
    print(f"{'='*54}\n")


if __name__ == "__main__":
    main()
