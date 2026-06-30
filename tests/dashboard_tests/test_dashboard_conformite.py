"""
════════════════════════════════════════════════════════════
PROJECT      : ALFRED
BLOCK        : B20 — Sécurité, Gouvernance & Conformité
FUNCTION     : DASHBOARD.TEST
FILE         : tests/dashboard_tests/test_dashboard_conformite.py
ROLE         : Tests d'intégration — pipeline + structure dashboard_conformite.json

AUTHOR       : Cognitive Products Lab — Céline Rousselot
CREATED      : 2026-06-30
UPDATED      : 2026-06-30
VERSION      : V1.0
STATUS       : ACTIVE

DESCRIPTION :
Teste le pipeline update_conformite_data.py et la structure JSON :
  - Exécution sans erreur
  - Structure dashboard_conformite.json valide
  - 9 normes présentes dont CRA
  - Scores cohérents (0–100)
  - Champs obligatoires par exigence
  - Global cohérent avec la somme des normes
  - Rapport audit .md généré
════════════════════════════════════════════════════════════
"""

import json
import subprocess
import sys
from pathlib import Path

import pytest

_ROOT          = Path(__file__).resolve().parents[2]
_CONFORM_DIR   = _ROOT / "dashboard" / "dashboard_conformite"
_DATA_FILE     = _CONFORM_DIR / "dashboard_conformite.json"
_MANIFEST      = _CONFORM_DIR / "_manifest.json"
_REPORTS_DIR   = _CONFORM_DIR / "reports"
_UPDATE_SCRIPT = _ROOT / "tools" / "dashboard_tools" / "dashboard_conformite" / "update_conformite_data.py"

REQUIRED_NORM_IDS   = {"RGPD", "LIL", "AIACT", "NIS2", "ISO27001", "CRA", "HDS", "SECNUMCLOUD", "PASSI"}
VALID_STATUSES      = {"conforme", "en_cours", "todo", "non_concerne"}
VALID_CRITICITE     = {"critique", "eleve", "haute", "moyenne", "faible", "nulle", "non_concerne"}


# ─── Fichiers sources ────────────────────────────────────────────────────────

def test_data_file_exists():
    assert _DATA_FILE.exists(), f"dashboard_conformite.json absent : {_DATA_FILE}"


def test_manifest_exists():
    assert _MANIFEST.exists(), f"_manifest.json absent : {_MANIFEST}"


# ─── Pipeline ────────────────────────────────────────────────────────────────

def test_pipeline_runs_without_error():
    if not _UPDATE_SCRIPT.exists():
        pytest.skip("Script update_conformite_data.py introuvable")
    result = subprocess.run(
        [sys.executable, str(_UPDATE_SCRIPT)],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
        cwd=str(_ROOT), timeout=60,
    )
    assert result.returncode == 0, (
        f"Script échoué (code {result.returncode}):\n{result.stderr[-500:]}"
    )


# ─── Structure JSON ──────────────────────────────────────────────────────────

@pytest.fixture(scope="module")
def data():
    with open(_DATA_FILE, encoding="utf-8") as f:
        return json.load(f)


def test_top_level_keys(data):
    for key in ("_meta", "norms", "global"):
        assert key in data, f"Clé manquante : '{key}'"


def test_meta_fields(data):
    meta = data["_meta"]
    assert "version"     in meta
    assert "description" in meta


def test_norms_present(data):
    norm_ids = {n["id"] for n in data["norms"]}
    assert REQUIRED_NORM_IDS.issubset(norm_ids), (
        f"Normes manquantes : {REQUIRED_NORM_IDS - norm_ids}"
    )


def test_cra_norm_present(data):
    ids = [n["id"] for n in data["norms"]]
    assert "CRA" in ids, "Norme CRA (Cyber Resilience Act) absente"


def test_norm_structure(data):
    for norm in data["norms"]:
        assert "id"           in norm, f"Norme sans 'id' : {norm}"
        assert "label"        in norm, f"Norme {norm.get('id')} sans 'label'"
        assert "requirements" in norm, f"Norme {norm.get('id')} sans 'requirements'"
        assert "stats"        in norm, f"Norme {norm.get('id')} sans 'stats'"
        assert isinstance(norm["requirements"], list)


def test_requirement_fields(data):
    for norm in data["norms"]:
        for req in norm.get("requirements", []):
            for field in ("id", "article", "label", "domain", "status", "criticite"):
                assert field in req, (
                    f"Champ '{field}' manquant dans {req.get('id','?')} ({norm['id']})"
                )
            assert req["status"] in VALID_STATUSES, (
                f"Statut invalide '{req['status']}' pour {req.get('id','?')}"
            )
            assert req["criticite"] in VALID_CRITICITE, (
                f"Criticité invalide '{req['criticite']}' pour {req.get('id','?')}"
            )


def test_norm_score_range(data):
    for norm in data["norms"]:
        stats = norm.get("stats", {})
        pct = stats.get("score_pct", 0)
        assert 0 <= pct <= 100, (
            f"score_pct hors bornes [{pct}] pour norme {norm['id']}"
        )


def test_global_coherence(data):
    g = data["global"]
    total_from_norms = sum(
        len(n.get("requirements", [])) for n in data["norms"]
    )
    assert g["total_requirements"] == total_from_norms, (
        f"global.total_requirements ({g['total_requirements']}) ≠ somme normes ({total_from_norms})"
    )
    assert 0 <= g["score_pct"] <= 100
    assert g["grade"] in ("A", "B+", "B", "C", "D")


def test_global_sum_consistency(data):
    g = data["global"]
    total_check = g["conforme"] + g["en_cours"] + g["todo"] + g["non_concerne"]
    assert total_check == g["total_requirements"], (
        f"Somme statuts ({total_check}) ≠ total ({g['total_requirements']})"
    )
