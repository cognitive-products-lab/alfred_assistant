"""
PROJECT  : ALFRED
BLOCK    : B23
FUNCTION : 23.02 — Orchestration & planification quotidienne
FILE     : tools/daily_update.py
ROLE     : Orchestrateur de la mise à jour quotidienne ALFRED.
           1. Régénère dashboard_gouvernance_data.json
           2. Régénère knowledge_dashboard_data.json
           3. Régénère dashboard_quality_data.json (INTERNE — jamais synchronisé vers le web)
           4. Lance sync_dashboards.py (copie JSON -> ALFRED_WEB + git push)
USAGE    : python tools/daily_update.py
SCHEDULE : Planificateur Windows — tâche ALFRED_DailyUpdate — tous les jours à 07h00
           (identique à daily_update.bat)

⚠️ dashboard_quality_data est un dashboard PRIVÉ : sa régénération reste avant
   l'étape de sync et son JSON n'apparaît jamais dans SRC_* de sync_dashboards.py.
   Ne jamais l'y ajouter sans décision explicite de publication (voir
   dashboard/dashboard_quality_data/dashboard_quality_data_manifest.json).
"""

from __future__ import annotations

import subprocess
import sys
from datetime import datetime
from pathlib import Path

ALFRED_PC = Path(__file__).resolve().parents[1]

STEPS = [
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
        "label": "Sync dashboards → ALFRED_WEB",
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
    print(f"  ALFRED Daily Update — {ts}")
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
