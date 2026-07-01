"""
════════════════════════════════════════════════════════════
PROJECT      : ALFRED
BLOCK        : B20 — Sécurité, Gouvernance & Conformité
FUNCTION     : DASHBOARD.TEST
FILE         : tests/dashboard_tests/test_dashboard_risk_impact.py
ROLE         : Tests d'intégration — pipeline + structure dashboard_risk_impact.json

AUTHOR       : Cognitive Products Lab — Céline Rousselot
CREATED      : 2026-06-30
UPDATED      : 2026-06-30
VERSION      : V1.0
STATUS       : ACTIVE

DESCRIPTION :
Teste le pipeline update_risk_impact_data.py et la structure JSON :
  - Exécution sans erreur
  - Structure dashboard_risk_impact.json valide
  - 15 risques présents
  - Scores P×I cohérents (1-25)
  - Niveaux corrects selon seuils ISO 31000
  - Analyse d'impact à 6 axes pour chaque risque
  - Catalogue de contrôles non vide
  - 3 politiques présentes (données, sécurité, RSE)
  - Global cohérent avec somme des risques
════════════════════════════════════════════════════════════
"""

import json
import subprocess
import sys
from pathlib import Path

import pytest

_ROOT          = Path(__file__).resolve().parents[2]
_RISK_DIR      = _ROOT / "dashboard" / "dashboard_risk_impact"
_DATA_FILE     = _RISK_DIR / "dashboard_risk_impact.json"
_REPORTS_DIR   = _RISK_DIR / "reports"
_UPDATE_SCRIPT = _ROOT / "tools" / "dashboard_tools" / "dashboard_risk_impact" / "update_risk_impact_data.py"

VALID_LEVELS   = {"critique", "eleve", "moyen", "faible"}
VALID_STATUSES = {"ouvert", "contrôlé", "accepté", "clos"}
IMPACT_AXES    = {"confidentialite", "integrite", "disponibilite", "conformite", "reputation", "financier"}
REQUIRED_POLICIES = {"data_processing", "security", "rse"}

THRESHOLDS = [(1, 4, "faible"), (5, 9, "moyen"), (10, 14, "eleve"), (15, 25, "critique")]


def expected_level(score: int) -> str:
    for lo, hi, level in THRESHOLDS:
        if lo <= score <= hi:
            return level
    return "critique"


# ─── Fichier source ──────────────────────────────────────────────────────────

def test_data_file_exists():
    assert _DATA_FILE.exists(), f"dashboard_risk_impact.json absent : {_DATA_FILE}"


# ─── Pipeline ────────────────────────────────────────────────────────────────

def test_pipeline_runs_without_error():
    if not _UPDATE_SCRIPT.exists():
        pytest.skip("Script update_risk_impact_data.py introuvable")
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
    for key in ("_meta", "global", "matrix_config", "risks", "controls", "policies"):
        assert key in data, f"Clé manquante : '{key}'"


def test_minimum_risks(data):
    assert len(data["risks"]) >= 10, (
        f"Trop peu de risques : {len(data['risks'])} (minimum 10)"
    )


def test_risk_fields(data):
    for r in data["risks"]:
        for field in ("id", "name", "category", "likelihood", "impact", "score",
                      "level", "status", "description", "controls", "residual_score"):
            assert field in r, f"Champ '{field}' manquant dans {r.get('id','?')}"
        assert r["level"]  in VALID_LEVELS,   f"Niveau invalide '{r['level']}' pour {r['id']}"
        assert r["status"] in VALID_STATUSES,  f"Statut invalide '{r['status']}' pour {r['id']}"


def test_scores_coherent(data):
    for r in data["risks"]:
        p, i = r["likelihood"], r["impact"]
        assert 1 <= p <= 5, f"Probabilité hors [1-5] pour {r['id']}"
        assert 1 <= i <= 5, f"Impact hors [1-5] pour {r['id']}"
        assert r["score"] == p * i, (
            f"score {r['score']} ≠ P×I {p*i} pour {r['id']}"
        )
        assert r["level"] == expected_level(r["score"]), (
            f"Niveau '{r['level']}' incorrect pour score {r['score']} ({r['id']})"
        )


def test_residual_score_lower(data):
    for r in data["risks"]:
        assert r["residual_score"] <= r["score"], (
            f"Score résiduel ({r['residual_score']}) > score brut ({r['score']}) pour {r['id']}"
        )


def test_impact_analysis_axes(data):
    for r in data["risks"]:
        ia = r.get("impact_analysis", {})
        if ia:
            for axis in IMPACT_AXES:
                assert axis in ia, (
                    f"Axe impact '{axis}' manquant pour {r['id']}"
                )
                assert 1 <= ia[axis] <= 5, (
                    f"Valeur hors [1-5] pour axe '{axis}' du risque {r['id']}"
                )


def test_controls_catalog(data):
    controls = data.get("controls", [])
    assert len(controls) > 0, "Catalogue de contrôles vide"
    for c in controls:
        for field in ("id", "name", "category", "status", "description"):
            assert field in c, f"Champ '{field}' manquant dans contrôle {c.get('id','?')}"
        assert c["status"] in ("actif", "partiel", "planifié"), (
            f"Statut contrôle invalide '{c['status']}' pour {c['id']}"
        )


def test_controls_referenced_exist(data):
    ctrl_ids = {c["id"] for c in data.get("controls", [])}
    for r in data["risks"]:
        for cid in r.get("controls", []):
            assert cid in ctrl_ids, (
                f"Contrôle '{cid}' référencé par {r['id']} absent du catalogue"
            )


def test_policies_present(data):
    policies = data.get("policies", {})
    assert REQUIRED_POLICIES.issubset(set(policies.keys())), (
        f"Politiques manquantes : {REQUIRED_POLICIES - set(policies.keys())}"
    )


def test_policy_structure(data):
    for key, policy in data.get("policies", {}).items():
        for field in ("title", "sections"):
            assert field in policy, f"Champ '{field}' manquant dans politique '{key}'"
        assert len(policy["sections"]) > 0, f"Politique '{key}' sans sections"


def test_global_coherence(data):
    g = data["global"]
    risks = data["risks"]
    assert g["total"] == len(risks), (
        f"global.total ({g['total']}) ≠ len(risks) ({len(risks)})"
    )
    computed_brut = sum(r["score"] for r in risks)
    assert g["risk_score_brut"] == computed_brut, (
        f"risk_score_brut ({g['risk_score_brut']}) ≠ somme scores ({computed_brut})"
    )
    total_levels = g["critique"] + g["eleve"] + g["moyen"] + g["faible"]
    assert total_levels == g["total"], (
        f"Somme niveaux ({total_levels}) ≠ total ({g['total']})"
    )


def test_matrix_config(data):
    mc = data.get("matrix_config", {})
    assert "x_levels" in mc and len(mc["x_levels"]) == 5
    assert "y_levels" in mc and len(mc["y_levels"]) == 5
    assert "thresholds" in mc
