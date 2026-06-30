"""
════════════════════════════════════════════════════════════
PROJECT      : ALFRED
BLOCK        : B20 — Sécurité, Gouvernance & Conformité
FUNCTION     : DASHBOARD.TEST
FILE         : tests/dashboard_tests/test_dashboard_vulnerabilites.py
ROLE         : Tests d'intégration — pipeline + structure dashboard_vulnerabilites.json

AUTHOR       : Cognitive Products Lab — Céline Rousselot
CREATED      : 2026-06-30
UPDATED      : 2026-06-30
VERSION      : V1.0
STATUS       : ACTIVE

DESCRIPTION :
Teste le pipeline update_vulnerabilites_data.py et la structure JSON :
  - Exécution sans erreur
  - Structure dashboard_vulnerabilites.json valide
  - Catalogue des vulnérabilités non vide
  - Champs obligatoires par vulnérabilité
  - Scores P×I dans les bornes (1-25)
  - Config scan/notification présente
  - Tâches d'automatisation valides
════════════════════════════════════════════════════════════
"""

import json
import subprocess
import sys
from pathlib import Path

import pytest

_ROOT         = Path(__file__).resolve().parents[2]
_VULN_DIR     = _ROOT / "dashboard" / "dashboard_vulnerabilites"
_DATA_FILE    = _VULN_DIR / "dashboard_vulnerabilites.json"
_REPORTS_DIR  = _VULN_DIR / "reports"
_UPDATE_SCRIPT = _ROOT / "tools" / "dashboard_tools" / "dashboard_vulnerabilites" / "update_vulnerabilites_data.py"

VALID_SEVERITIES = {"critique", "eleve", "moyen", "faible", "informatif"}
VALID_STATUSES   = {"ouvert", "en cours", "contrôlé", "résolu", "accepté"}


# ─── Fichier source ──────────────────────────────────────────────────────────

def test_data_file_exists():
    assert _DATA_FILE.exists(), f"dashboard_vulnerabilites.json absent : {_DATA_FILE}"


# ─── Pipeline ────────────────────────────────────────────────────────────────

def test_pipeline_runs_without_error():
    if not _UPDATE_SCRIPT.exists():
        pytest.skip("Script update_vulnerabilites_data.py introuvable")
    result = subprocess.run(
        [sys.executable, str(_UPDATE_SCRIPT)],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
        cwd=str(_ROOT), timeout=120,
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
    for key in ("_meta", "config", "summary", "vulnerabilities", "automation_tasks", "scan_history"):
        assert key in data, f"Clé manquante : '{key}'"


def test_config_scan_fields(data):
    cfg = data["config"]
    assert "scan" in cfg
    assert "cron"  in cfg["scan"]
    assert "human" in cfg["scan"]
    assert "notification_thresholds" in cfg
    assert "channels" in cfg


def test_vulnerabilities_not_empty(data):
    assert len(data["vulnerabilities"]) > 0, "Catalogue vide"


def test_vulnerability_fields(data):
    for v in data["vulnerabilities"]:
        for field in ("id", "category", "name", "severity", "likelihood", "impact", "status"):
            assert field in v, f"Champ '{field}' manquant dans {v.get('id','?')}"
        assert v["severity"] in VALID_SEVERITIES, (
            f"Sévérité invalide '{v['severity']}' pour {v['id']}"
        )
        assert v["status"] in VALID_STATUSES, (
            f"Statut invalide '{v['status']}' pour {v['id']}"
        )


def test_scores_in_range(data):
    for v in data["vulnerabilities"]:
        score = v["likelihood"] * v["impact"]
        assert 1 <= score <= 25, (
            f"Score {score} hors bornes pour {v['id']} (P={v['likelihood']}, I={v['impact']})"
        )
        assert 1 <= v["likelihood"] <= 5, f"Probabilité hors [1-5] pour {v['id']}"
        assert 1 <= v["impact"]     <= 5, f"Impact hors [1-5] pour {v['id']}"


def test_summary_consistency(data):
    s = data["summary"]
    vulns = data["vulnerabilities"]
    assert s["total"] == len(vulns), "summary.total ≠ len(vulnerabilities)"
    by_sev = s.get("by_severity", {})
    computed = sum(by_sev.values())
    assert computed == s["total"], f"Somme sévérités ({computed}) ≠ total ({s['total']})"


def test_automation_tasks(data):
    tasks = data.get("automation_tasks", [])
    assert len(tasks) > 0, "Aucune tâche d'automatisation définie"
    for t in tasks:
        assert "id"   in t, f"Tâche sans 'id' : {t}"
        assert "name" in t, f"Tâche sans 'name' : {t}"
        assert "cron" in t, f"Tâche {t.get('id','?')} sans 'cron'"
        assert "active" in t, f"Tâche {t.get('id','?')} sans 'active'"


def test_scan_history_structure(data):
    for entry in data.get("scan_history", []):
        assert "date"   in entry
        assert "type"   in entry
        assert "result" in entry
