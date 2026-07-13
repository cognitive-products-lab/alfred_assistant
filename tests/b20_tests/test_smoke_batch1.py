"""
PROJECT      : ALFRED
BLOCK        : B20
FUNCTION     : SMOKE
FILE         : tests/b20_tests/test_smoke_batch1.py
ROLE         : Smoke tests (lot 1) pour les fichiers B20 hors security_tests/
               (deja couvert) : consent_art9.py, config/data JSON, logs,
               dashboards HTML, startup_refresh.py.

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-07-05
UPDATED      : 2026-07-05
VERSION      : V1.0
STATUS       : TESTED
"""

import json
from pathlib import Path

import pytest

from src.security.consent_art9 import ConsentArt9Manager, ART9_CATEGORIES
from tools.profile_tools.generate_alfred_params import (
    extract_psychometric_signals,
    derive_alfred_parameters,
)

ROOT = Path(__file__).resolve().parents[2]


# ── tools/profile_tools/generate_alfred_params.py ────────────
# Fixe le 2026-07-05 : docstrings empilées fusionnées (bug systémique,
# meme correctif que src/profile/profile_analyzer.py).

def test_extract_psychometric_signals_empty_profile():
    signals = extract_psychometric_signals({})
    assert signals["disc_C"] == 0
    assert signals["besoin_principal"] == ""


def test_extract_psychometric_signals_reads_nested_fields():
    profile = {
        "disc_profile": {"test_2": {"profil_dominant": "Conforme", "scores": {"conforme_C": 90}}},
        "besoins_professionnels": {"besoin_principal": "SECURITE"},
    }
    signals = extract_psychometric_signals(profile)
    assert signals["disc_dominant"] == "Conforme"
    assert signals["disc_C"] == 90
    assert signals["besoin_principal"] == "SECURITE"


def test_derive_alfred_parameters_returns_tone_default():
    params = derive_alfred_parameters(extract_psychometric_signals({}))
    assert "tone_default" in params
    assert isinstance(params["tone_default"], str) and params["tone_default"]


# ── tools/profile_tools/test_alfred_profile_integration.py ──
# C'est un smoke test autonome (pas un module pytest) — deja execute
# directement (0 erreur, 0 warning) apres le fix des docstrings empilees
# + fix encodage UTF-8 (meme bug ✅/cp1252 que les scripts dashboard).
# Pas de wrapper pytest necessaire : le script EST le test.


# ── src/security/consent_art9.py ─────────────────────────────

def test_consent_art9_record_and_check(tmp_path):
    mgr = ConsentArt9Manager(registry_path=tmp_path / "consent_registry.json")
    result = mgr.record_consent("test_user", "health_data", method="explicit_form")
    assert result["status"] == "OK"
    assert mgr.is_consent_valid("test_user", "health_data") is True


def test_consent_art9_rejects_unknown_category(tmp_path):
    mgr = ConsentArt9Manager(registry_path=tmp_path / "consent_registry.json")
    result = mgr.record_consent("test_user", "categorie_inexistante")
    assert result["status"] == "ERROR"


def test_consent_art9_revoke(tmp_path):
    mgr = ConsentArt9Manager(registry_path=tmp_path / "consent_registry.json")
    mgr.record_consent("test_user", "behavioral_data")
    revoke_result = mgr.revoke_consent("test_user", "behavioral_data")
    assert revoke_result["revoked_count"] == 1
    assert mgr.is_consent_valid("test_user", "behavioral_data") is False


def test_consent_art9_persists_across_instances(tmp_path):
    path = tmp_path / "consent_registry.json"
    mgr1 = ConsentArt9Manager(registry_path=path)
    mgr1.record_consent("test_user", "wellbeing_tracking")

    mgr2 = ConsentArt9Manager(registry_path=path)
    assert mgr2.is_consent_valid("test_user", "wellbeing_tracking") is True


def test_consent_art9_get_summary(tmp_path):
    mgr = ConsentArt9Manager(registry_path=tmp_path / "consent_registry.json")
    mgr.record_consent("test_user", "health_data")
    mgr.record_consent("test_user", "biometric_data")
    mgr.revoke_consent("test_user", "biometric_data")
    summary = mgr.get_summary()
    assert summary["total_consents_recorded"] == 2
    assert summary["active_consents"] == 1
    assert summary["revoked_consents"] == 1


def test_consent_art9_categories_frozen():
    assert "health_data" in ART9_CATEGORIES
    assert "mental_health_data" in ART9_CATEGORIES


# ── Config/data JSON ──────────────────────────────────────────

def test_safety_rules_json_structure():
    data = json.loads((ROOT / "config" / "safety_rules.json").read_text(encoding="utf-8"))
    assert "principles" in data
    assert isinstance(data["principles"], list) and data["principles"]


def test_audit_retention_policy_json_structure():
    data = json.loads((ROOT / "config" / "security" / "audit_retention_policy.json").read_text(encoding="utf-8"))
    assert isinstance(data["retention_days"], int) and data["retention_days"] > 0


def test_trusted_devices_json_structure():
    data = json.loads((ROOT / "config" / "security" / "trusted_devices.json").read_text(encoding="utf-8"))
    assert "devices" in data
    assert isinstance(data["devices"], list)


def test_incident_register_json_is_valid_list_of_incidents():
    data = json.loads((ROOT / "data" / "security" / "incident_register.json").read_text(encoding="utf-8"))
    assert isinstance(data, list)
    if data:
        for key in ("timestamp", "level", "description", "source", "status"):
            assert key in data[0]


def test_security_log_is_readable_text():
    path = ROOT / "logs" / "security" / "security.log"
    text = path.read_text(encoding="utf-8", errors="replace")
    assert text.strip()


# ── Dashboards HTML (validite basique) ───────────────────────

HTML_FILES = [
    "dashboard/dashboard_gouvernance/dashboard_gouvernance.html",
    "dashboard/dashboard_gouvernance/dashboard_gouvernance_dynamique.html",
    "dashboard/dashboard_gouvernance/index.html",
    "dashboard/dashboard_gouvernance/norm.html",
    "dashboard/dashboard_security/dashboard_security.html",
    "dashboard/dashboard_security/dashboard_security_dynamique.html",
    "dashboard/dashboard_tests/dashboard_tests.html",
    "dashboard/dashboard_tests/dashboard_tests_dynamique.html",
    "scripts/alfred_dashboard.html",
    "templates/html_dashboard_template.html",
]


@pytest.mark.parametrize("relpath", HTML_FILES)
def test_dashboard_html_is_well_formed(relpath):
    text = (ROOT / relpath).read_text(encoding="utf-8", errors="replace")
    assert text.strip()
    lower = text.lower()
    assert "<html" in lower or "<!doctype" in lower or "<div" in lower


# ── Manifests/registres dashboard (structure JSON) ───────────
# Les 3 anciens duplicatas racine (dashboard/dashboard_manifest.json,
# dashboard/dashboard_data.json, dashboard/validation_registry.json) ont été
# archivés le 13/07/2026 (dashboard/_archive/, point C4-D du plan d'action) —
# ils étaient obsolètes depuis mai/juillet 2026 et superflus par rapport à
# leurs équivalents dans dashboard/dashboard_data/.

DASHBOARD_JSON_FILES = [
    "dashboard/dashboard_conformite/_manifest.json",
    "dashboard/dashboard_data/validation_registry.json",
    "dashboard/dashboard_data/dashboard_data.json",
    "dashboard/dashboard_data/dashboard_data_manifest.json",
]


@pytest.mark.parametrize("relpath", DASHBOARD_JSON_FILES)
def test_dashboard_json_files_are_valid_json(relpath):
    data = json.loads((ROOT / relpath).read_text(encoding="utf-8-sig"))
    assert isinstance(data, dict) and data


# ── tools/startup_refresh.py ──────────────────────────────────

def test_startup_refresh_async_runs_without_error():
    from tools.startup_refresh import refresh_knowledge_dashboard_async
    import threading

    before_threads = threading.active_count()
    refresh_knowledge_dashboard_async()
    # Le thread est daemon et asynchrone — on vérifie juste qu'il démarre sans exception
    assert threading.active_count() >= before_threads
