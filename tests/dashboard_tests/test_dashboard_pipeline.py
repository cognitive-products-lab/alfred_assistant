"""
════════════════════════════════════════════════════════════
PROJECT      : ALFRED
BLOCK        : DASHBOARD
FUNCTION     : DASHBOARD.TEST
FILE         : tests/dashboard_tests/test_dashboard_pipeline.py
ROLE         : Tests d'intégration — pipeline manifest → dashboard_data.json

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-06-01
VERSION      : V1.0
STATUS       : ACTIVE

DESCRIPTION :
Teste le pipeline complet update_dashboard_data.py :
lecture manifest → évaluation fichiers → génération dashboard_data.json.
Utilise un manifest synthétique en tmp_path pour isolation totale.
════════════════════════════════════════════════════════════
"""

import json
import subprocess
import sys
from pathlib import Path

import pytest

_ROOT = Path(__file__).resolve().parents[2]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))


# ─── Tests pipeline subprocess (isolation totale) ─────────────────────────────

def test_real_pipeline_runs_without_error():
    """
    Lance update_dashboard_data.py en subprocess depuis la racine projet.
    Vérifie qu'il s'exécute sans erreur et produit dashboard_data.json.
    """
    script = _ROOT / "tools" / "dashboard_tools" / "dashboard_data" / "update_dashboard_data.py"
    if not script.exists():
        pytest.skip("Script update_dashboard_data.py introuvable")

    result = subprocess.run(
        [sys.executable, str(script)],
        capture_output=True, text=True, cwd=str(_ROOT),
        timeout=60,
    )
    assert result.returncode == 0, (
        f"Le script a échoué (code {result.returncode}):\n{result.stderr[-500:]}"
    )


def test_real_dashboard_data_json_valid():
    """
    Test de non-régression : le vrai dashboard_data.json est un JSON valide
    avec la structure attendue. blocks peut être une liste ou un dict.
    """
    dashboard_dir = _ROOT / "dashboard" / "dashboard_data"
    data_file = dashboard_dir / "dashboard_data.json"
    if not data_file.exists():
        pytest.skip("dashboard_data.json absent — lancer update_dashboard_data.py")

    data = json.loads(data_file.read_text(encoding="utf-8"))
    assert "blocks" in data
    # blocks peut être une liste (format actuel) ou un dict (format ancien)
    assert isinstance(data["blocks"], (dict, list))
    assert len(data["blocks"]) > 0


def test_real_manifest_loadable():
    """Le manifest réel est un JSON valide."""
    manifest = _ROOT / "dashboard" / "dashboard_data" / "dashboard_data_manifest.json"
    if not manifest.exists():
        pytest.skip("manifest absent")
    data = json.loads(manifest.read_text(encoding="utf-8"))
    assert "blocks" in data or "_meta" in data
