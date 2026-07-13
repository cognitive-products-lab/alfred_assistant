"""
════════════════════════════════════════════════════════════
PROJECT      : ALFRED
BLOCK        : Bloc 11.05 — Gouvernance data
FUNCTION     : DASHBOARD.TEST
FILE         : tests/dashboard_tests/test_dashboard_quality_data.py
ROLE         : Tests d'intégration — pipeline registre → dashboard_quality_data.json
               + tests unitaires du moteur d'alertes sur fixtures synthétiques.

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-07-12
VERSION      : V1.0
STATUS       : ACTIVE

DESCRIPTION :
Teste le pipeline complet update_quality_data_dashboard.py :
  - Exécution sans erreur
  - Structure dashboard_quality_data.json valide
  - Cohérence des agrégats (documented_count, defined_count, ...)
  - Chaque type d'alerte est détecté sur des fiches synthétiques dédiées
  - Le dashboard n'est jamais référencé dans tools/sync_dashboards.py (garde-fou "PRIVÉ")
════════════════════════════════════════════════════════════
"""

import importlib.util
import json
import subprocess
import sys
from datetime import date, timedelta
from pathlib import Path

import pytest

_ROOT = Path(__file__).resolve().parents[2]
_DASHBOARD_DIR = _ROOT / "dashboard" / "dashboard_quality_data"
_REGISTRY = _DASHBOARD_DIR / "data_quality_registry.json"
_DATA_FILE = _DASHBOARD_DIR / "dashboard_quality_data.json"
_MANIFEST = _DASHBOARD_DIR / "dashboard_quality_data_manifest.json"
_UPDATE_SCRIPT = _ROOT / "tools" / "dashboard_tools" / "dashboard_quality_data" / "update_quality_data_dashboard.py"
_SYNC_SCRIPT = _ROOT / "tools" / "sync_dashboards.py"


def _load_module():
    spec = importlib.util.spec_from_file_location("update_quality_data_dashboard", _UPDATE_SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# ─── Pipeline ────────────────────────────────────────────────────────────────

def test_pipeline_runs_without_error():
    if not _UPDATE_SCRIPT.exists():
        pytest.skip("Script update_quality_data_dashboard.py introuvable")
    result = subprocess.run(
        [sys.executable, str(_UPDATE_SCRIPT)],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
        cwd=str(_ROOT), timeout=60,
    )
    assert result.returncode == 0, (
        f"Le script a échoué (code {result.returncode}):\n{result.stderr[-500:]}"
    )


def test_data_file_generated():
    assert _DATA_FILE.exists(), (
        "dashboard_quality_data.json absent — lancer update_quality_data_dashboard.py"
    )


# ─── Structure JSON ───────────────────────────────────────────────────────────

@pytest.fixture(scope="module")
def data():
    if not _DATA_FILE.exists():
        pytest.skip("dashboard_quality_data.json absent")
    return json.loads(_DATA_FILE.read_text(encoding="utf-8"))


def test_data_has_required_top_level_keys(data):
    for key in ("_meta", "global", "alerts", "entries", "scales"):
        assert key in data, f"Clé manquante : {key}"


def test_meta_marks_private(data):
    """Le dashboard doit toujours se déclarer PRIVÉ dans ses métadonnées."""
    assert data["_meta"].get("visibility") == "PRIVE"


def test_entries_is_list_non_empty(data):
    assert isinstance(data["entries"], list)
    assert len(data["entries"]) > 0


REQUIRED_ENTRY_FIELDS = (
    "id", "name", "documented", "defined", "status", "data_type",
    "sensitivity_classification", "security_level_planned", "intended_use",
    "retention_period", "update_frequency", "authorized_roles",
    "created_at", "last_modified_at", "planned_deletion_at",
)


def test_each_entry_has_required_fields(data):
    for entry in data["entries"]:
        for field in REQUIRED_ENTRY_FIELDS:
            assert field in entry, f"Champ manquant dans {entry.get('id')}: {field}"


VALID_STATUSES = {"a_creer", "a_connecter", "utilisable", "utilisee", "obsolete"}


def test_entry_status_values_valid(data):
    for entry in data["entries"]:
        assert entry["status"] in VALID_STATUSES, (
            f"Statut invalide pour {entry['id']}: {entry['status']}"
        )


def test_security_level_planned_in_range(data):
    for entry in data["entries"]:
        level = entry["security_level_planned"]
        assert isinstance(level, int) and 1 <= level <= 5, (
            f"Niveau de sécurité prévu hors plage 1-5 pour {entry['id']}: {level}"
        )


def test_global_counts_consistent(data):
    g = data["global"]
    entries = data["entries"]
    assert g["total_entries"] == len(entries)
    assert g["documented_count"] == sum(1 for e in entries if e["documented"])
    assert g["defined_count"] == sum(1 for e in entries if e["defined"])
    assert g["undocumented_count"] == len(entries) - g["documented_count"]
    assert g["undefined_count"] == len(entries) - g["defined_count"]


def test_alerts_total_matches_items(data):
    assert data["alerts"]["total"] == len(data["alerts"]["items"])


VALID_SEVERITIES = {"critical", "warning", "info"}


def test_alert_items_have_required_fields(data):
    for alert in data["alerts"]["items"]:
        for field in ("entry_id", "entry_name", "type", "severity", "message"):
            assert field in alert, f"Champ manquant dans une alerte : {field}"
        assert alert["severity"] in VALID_SEVERITIES


# ─── Manifest ─────────────────────────────────────────────────────────────────

def test_manifest_loadable_and_marked_private():
    assert _MANIFEST.exists(), "dashboard_quality_data_manifest.json introuvable"
    manifest = json.loads(_MANIFEST.read_text(encoding="utf-8"))
    assert manifest.get("visibility", "").startswith("PRIVE")


def test_registry_loadable():
    assert _REGISTRY.exists(), "data_quality_registry.json introuvable"
    registry = json.loads(_REGISTRY.read_text(encoding="utf-8"))
    assert "entries" in registry


# ─── Garde-fou : jamais publié ────────────────────────────────────────────────

def test_never_referenced_in_sync_dashboards():
    """dashboard_quality_data ne doit JAMAIS être copié vers ALFRED_WEB."""
    if not _SYNC_SCRIPT.exists():
        pytest.skip("tools/sync_dashboards.py introuvable")
    content = _SYNC_SCRIPT.read_text(encoding="utf-8")
    assert "quality_data" not in content, (
        "dashboard_quality_data est référencé dans sync_dashboards.py — "
        "ce dashboard interne ne doit jamais être publié sur ALFRED_WEB."
    )


# ─── Moteur d'alertes — fixtures synthétiques ─────────────────────────────────

@pytest.fixture(scope="module")
def engine():
    return _load_module()


def _base_entry(**overrides) -> dict:
    entry = {
        "id": "TEST-001",
        "name": "Fiche de test",
        "documented": True,
        "defined": True,
        "status": "utilisee",
        "data_type": "privee",
        "sensitivity_classification": "C2_INTERNE",
        "security_level_planned": 2,
        "intended_use": ["technique"],
        "retention_period": "1 an",
        "update_frequency": "quotidienne",
        "authorized_roles": {"read": ["OWNER"], "write": ["OWNER"]},
        "created_at": "2026-01-01",
        "last_modified_at": "2026-01-01",
        "planned_deletion_at": None,
    }
    entry.update(overrides)
    return entry


def test_alert_undefined_data(engine):
    entry = _base_entry(documented=False, defined=False)
    alerts = engine.check_undefined(entry)
    types = {a["type"] for a in alerts}
    assert "donnee_non_documentee" in types
    assert "donnee_non_definie" in types


def test_alert_obsolete_status(engine):
    entry = _base_entry(status="obsolete")
    alerts = engine.check_obsolete(entry)
    assert any(a["type"] == "statut_obsolete" for a in alerts)


def test_alert_created_but_unused(engine):
    old_date = (date.today() - timedelta(days=200)).isoformat()
    entry = _base_entry(status="utilisable", created_at=old_date)
    alerts = engine.check_created_but_unused(entry, date.today())
    assert any(a["type"] == "donnee_creee_non_utilisee" for a in alerts)


def test_no_unused_alert_when_status_a_creer(engine):
    """Une donnée pas encore créée ne doit jamais déclencher l'alerte 'créée mais non utilisée'."""
    old_date = (date.today() - timedelta(days=400)).isoformat()
    entry = _base_entry(status="a_creer", created_at=old_date)
    alerts = engine.check_created_but_unused(entry, date.today())
    assert alerts == []


def test_alert_missing_access_control(engine):
    entry = _base_entry(status="utilisee", authorized_roles={"read": [], "write": []})
    alerts = engine.check_access_control(entry, engine.load_roles())
    assert any(a["type"] == "controle_acces_absent" for a in alerts)


def test_alert_unauthorized_access_role_too_weak(engine):
    """Un rôle GUEST (habilitation LOW) ne doit pas pouvoir lire une donnée de niveau 5."""
    entry = _base_entry(
        security_level_planned=5,
        authorized_roles={"read": ["GUEST"], "write": ["OWNER"]},
    )
    alerts = engine.check_access_control(entry, engine.load_roles())
    assert any(a["type"] == "acces_non_autorise" for a in alerts)


def test_access_exception_downgrades_alert_to_info(engine):
    """Une dérogation documentée (access_exceptions) transforme l'alerte critique en info."""
    entry = _base_entry(
        security_level_planned=5,
        authorized_roles={"read": [], "write": ["AI_MODULE"]},
        access_exceptions=[{
            "role": "AI_MODULE", "scope": "write",
            "justification": "Écriture seule, append-only, nécessaire à la traçabilité.",
            "reviewed_by": "OWNER", "reviewed_at": "2026-07-13",
        }],
    )
    alerts = engine.check_access_control(entry, engine.load_roles())
    types = {a["type"] for a in alerts}
    assert "acces_derogatoire_documente" in types
    assert "acces_non_autorise" not in types
    derogation = next(a for a in alerts if a["type"] == "acces_derogatoire_documente")
    assert derogation["severity"] == "info"


def test_access_exception_scope_mismatch_still_alerts(engine):
    """Une dérogation qui ne couvre pas le bon scope (read vs write) ne doit pas masquer l'alerte."""
    entry = _base_entry(
        security_level_planned=5,
        authorized_roles={"read": ["AI_MODULE"], "write": []},
        access_exceptions=[{
            "role": "AI_MODULE", "scope": "write",
            "justification": "Ne couvre que l'écriture.",
            "reviewed_by": "OWNER", "reviewed_at": "2026-07-13",
        }],
    )
    alerts = engine.check_access_control(entry, engine.load_roles())
    assert any(a["type"] == "acces_non_autorise" for a in alerts)


def test_alert_unknown_role(engine):
    entry = _base_entry(authorized_roles={"read": ["ROLE_QUI_N_EXISTE_PAS"], "write": []})
    alerts = engine.check_access_control(entry, engine.load_roles())
    assert any(a["type"] == "acces_role_inconnu" for a in alerts)


def test_alert_deletion_overdue(engine):
    past_date = (date.today() - timedelta(days=5)).isoformat()
    entry = _base_entry(status="utilisee", planned_deletion_at=past_date)
    alerts = engine.check_deletion_overdue(entry, date.today())
    assert any(a["type"] == "purge_en_retard" for a in alerts)


def test_no_deletion_alert_once_obsolete(engine):
    past_date = (date.today() - timedelta(days=5)).isoformat()
    entry = _base_entry(status="obsolete", planned_deletion_at=past_date)
    alerts = engine.check_deletion_overdue(entry, date.today())
    assert alerts == []
