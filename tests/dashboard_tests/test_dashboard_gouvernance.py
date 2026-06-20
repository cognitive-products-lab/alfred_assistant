"""
════════════════════════════════════════════════════════════
PROJECT      : ALFRED
BLOCK        : B20 — Sécurité, Gouvernance & Conformité
FUNCTION     : DASHBOARD.TEST
FILE         : tests/dashboard_tests/test_dashboard_gouvernance.py
ROLE         : Tests d'intégration — pipeline manifest → dashboard_gouvernance_data.json

AUTHOR       : Cognitive Products Lab — Céline Darras
CREATED      : 2026-06-20
UPDATED      : 2026-06-20
VERSION      : V1.0
STATUS       : ACTIVE

DESCRIPTION :
Teste le pipeline complet update_gouvernance_data.py :
  - Exécution sans erreur
  - Structure dashboard_gouvernance_data.json valide
  - Scores cohérents (0–100)
  - Roadmap présente et bien formée
  - Rapport audit .md généré
  - Intégrité du manifest _manifest.json
════════════════════════════════════════════════════════════
"""

import json
import subprocess
import sys
from pathlib import Path

import pytest

_ROOT = Path(__file__).resolve().parents[2]
_GOUVERNANCE_DIR = _ROOT / "dashboard" / "dashboard_gouvernance"
_MANIFEST = _GOUVERNANCE_DIR / "_manifest.json"
_DATA_FILE = _GOUVERNANCE_DIR / "dashboard_gouvernance_data.json"
_REPORTS_DIR = _GOUVERNANCE_DIR / "reports"
_UPDATE_SCRIPT = _ROOT / "tools" / "dashboard_tools" / "dashboard_gouvernance" / "update_gouvernance_data.py"


# ─── Pipeline ────────────────────────────────────────────────────────────────

def test_pipeline_runs_without_error():
    """update_gouvernance_data.py s'exécute sans erreur depuis la racine projet."""
    if not _UPDATE_SCRIPT.exists():
        pytest.skip("Script update_gouvernance_data.py introuvable")

    result = subprocess.run(
        [sys.executable, str(_UPDATE_SCRIPT)],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
        cwd=str(_ROOT), timeout=60,
    )
    assert result.returncode == 0, (
        f"Le script a échoué (code {result.returncode}):\n{result.stderr[-500:]}"
    )


def test_data_file_generated():
    """dashboard_gouvernance_data.json existe après exécution du pipeline."""
    assert _DATA_FILE.exists(), (
        "dashboard_gouvernance_data.json absent — lancer update_gouvernance_data.py"
    )


# ─── Structure JSON ───────────────────────────────────────────────────────────

@pytest.fixture(scope="module")
def data():
    if not _DATA_FILE.exists():
        pytest.skip("dashboard_gouvernance_data.json absent")
    return json.loads(_DATA_FILE.read_text(encoding="utf-8"))


def test_data_has_required_top_level_keys(data):
    """Le JSON contient les clés racine attendues."""
    for key in ("_meta", "global", "norms", "roadmap"):
        assert key in data, f"Clé manquante : {key}"


def test_meta_has_generated_at(data):
    """_meta contient un champ generated_at non vide."""
    assert "generated_at" in data["_meta"]
    assert data["_meta"]["generated_at"]


def test_global_score_in_range(data):
    """Le score global est entre 0 et 100."""
    score = data["global"].get("score_pct")
    assert score is not None, "global.score_pct manquant"
    assert 0 <= score <= 100, f"Score hors plage : {score}"


def test_global_grade_present(data):
    """Le grade global est présent (A+, A, B, C, D)."""
    grade = data["global"].get("grade")
    assert grade in ("A+", "A", "B", "C", "D"), f"Grade invalide : {grade}"


def test_norms_is_list_non_empty(data):
    """norms est une liste non vide."""
    assert isinstance(data["norms"], list)
    assert len(data["norms"]) > 0


def test_each_norm_has_required_fields(data):
    """Chaque norme a id, label, score_pct, status, requirements."""
    for norm in data["norms"]:
        for field in ("id", "label", "score_pct", "status", "requirements"):
            assert field in norm, f"Champ manquant dans la norme {norm.get('id')}: {field}"


def test_norm_scores_in_range(data):
    """Les scores de chaque norme active sont entre 0 et 100."""
    for norm in data["norms"]:
        if norm["status"] == "active":
            score = norm.get("score_pct")
            assert score is not None, f"Score manquant pour {norm['id']}"
            assert 0 <= score <= 100, f"Score hors plage pour {norm['id']}: {score}"


def test_requirements_have_status(data):
    """Chaque exigence a un statut valide (done/partial/todo)."""
    valid = {"done", "partial", "todo"}
    for norm in data["norms"]:
        for req in norm.get("requirements", []):
            assert req.get("status") in valid, (
                f"Statut invalide pour {req.get('id')}: {req.get('status')}"
            )


def test_rgpd_norm_present(data):
    """La norme RGPD est présente dans les données."""
    ids = [n["id"] for n in data["norms"]]
    assert "RGPD" in ids, f"Norme RGPD absente — normes trouvées : {ids}"


def test_iso27001_norm_present(data):
    """La norme ISO27001 est présente dans les données."""
    ids = [n["id"] for n in data["norms"]]
    assert "ISO27001" in ids, f"Norme ISO27001 absente — normes trouvées : {ids}"


# ─── Roadmap ──────────────────────────────────────────────────────────────────

def test_roadmap_is_list_non_empty(data):
    """La roadmap est une liste non vide."""
    assert isinstance(data["roadmap"], list)
    assert len(data["roadmap"]) > 0


def test_roadmap_items_have_required_fields(data):
    """Chaque item roadmap a title, status, date."""
    valid_statuses = {"done", "active", "planned", "future"}
    for item in data["roadmap"]:
        for field in ("title", "status", "date"):
            assert field in item, f"Champ manquant dans roadmap item : {field}"
        assert item["status"] in valid_statuses, (
            f"Statut roadmap invalide : {item['status']} (item: {item.get('title')})"
        )


def test_roadmap_has_done_items(data):
    """La roadmap contient au moins un item done."""
    done = [i for i in data["roadmap"] if i["status"] == "done"]
    assert len(done) > 0, "Aucun item done dans la roadmap"


# ─── Rapport audit ────────────────────────────────────────────────────────────

def test_reports_directory_exists():
    """Le dossier reports/ existe."""
    assert _REPORTS_DIR.exists(), "Dossier reports/ manquant"


def test_at_least_one_audit_report_exists():
    """Au moins un rapport audit_gouvernance_*.md existe."""
    reports = list(_REPORTS_DIR.glob("audit_gouvernance_*.md"))
    assert len(reports) > 0, "Aucun rapport d'audit trouvé dans reports/"


# ─── Manifest ─────────────────────────────────────────────────────────────────

def test_manifest_loadable():
    """_manifest.json est un JSON valide."""
    assert _MANIFEST.exists(), "_manifest.json introuvable"
    data = json.loads(_MANIFEST.read_text(encoding="utf-8"))
    assert "_meta" in data
    assert "norms" in data


def test_manifest_norms_have_requirements():
    """Chaque norme du manifest a une liste requirements non vide."""
    data = json.loads(_MANIFEST.read_text(encoding="utf-8"))
    for norm in data["norms"]:
        reqs = norm.get("requirements", [])
        assert len(reqs) > 0, f"Norme {norm['id']} sans exigences dans le manifest"


def test_manifest_requirement_ids_unique():
    """Les IDs des exigences sont uniques dans tout le manifest."""
    data = json.loads(_MANIFEST.read_text(encoding="utf-8"))
    all_ids = []
    for norm in data["norms"]:
        for req in norm.get("requirements", []):
            all_ids.append(req["id"])
    assert len(all_ids) == len(set(all_ids)), (
        f"IDs en doublon dans le manifest : {[x for x in all_ids if all_ids.count(x) > 1]}"
    )
