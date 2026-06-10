"""
════════════════════════════════════════════════════════════
PROJECT      : ALFRED — tests asset_classifier + data_flow_mapper
BLOCK        : B20 · FUNCTION : 20.TEST
VERSION      : V1.0 · STATUS : ACTIVE
════════════════════════════════════════════════════════════
"""
import pytest
from pathlib import Path
from src.security.asset_classifier import (
    classify_path, classify_file, build_classification_report,
    C1_PUBLIC, C2_INTERNE, C3_CONFIDENTIEL, C4_SECRET,
    CLASSIFICATION_LABELS, _ROOT,
)
from src.security.data_flow_mapper import (
    get_registry, get_treatment_by_id,
    build_rgpd_report, check_rgpd_compliance,
    ALFRED_TREATMENTS,
)


# ─── classify_path ────────────────────────────────────────────────────────────

@pytest.mark.parametrize("rel_path,expected_level", [
    (".env",                           C4_SECRET),
    ("data/security/mfa_secrets.json", C4_SECRET),
    ("data/security/fernet.key",       C4_SECRET),
    ("data/users/instances/user.json", C3_CONFIDENTIEL),
    ("data/memory/episodic/dialogue_history.json", C3_CONFIDENTIEL),
    ("logs/security/audit_trail.jsonl", C3_CONFIDENTIEL),
    ("config/settings.json",           C2_INTERNE),
    ("src/security/mfa_manager.py",    C2_INTERNE),
    ("tests/test_mfa.py",              C2_INTERNE),
    ("README.md",                      C1_PUBLIC),
    ("knowledges/core/identity.json",  C1_PUBLIC),
])
def test_classify_path_levels(rel_path, expected_level, tmp_path):
    # Créer le fichier dans tmp_path pour avoir un Path relatif à la racine
    fake_root = tmp_path
    p = fake_root / rel_path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text("content")

    # Patcher _ROOT temporairement
    import src.security.asset_classifier as ac
    original_root = ac._ROOT
    try:
        ac._ROOT = fake_root
        level, _ = classify_path(p)
        assert level == expected_level, f"{rel_path}: attendu {expected_level}, obtenu {level}"
    finally:
        ac._ROOT = original_root


def test_classify_path_returns_tuple():
    p = _ROOT / "README.md"
    result = classify_path(p)
    assert isinstance(result, tuple)
    assert len(result) == 2
    assert result[0] in {C1_PUBLIC, C2_INTERNE, C3_CONFIDENTIEL, C4_SECRET}


# ─── classify_file ────────────────────────────────────────────────────────────

def test_classify_file_structure():
    p = _ROOT / "README.md"
    if not p.exists():
        pytest.skip("README.md absent")
    result = classify_file(p)
    assert "path" in result
    assert "classification" in result
    assert "label" in result
    assert "justification" in result
    assert "size_bytes" in result
    assert "exists" in result


def test_classify_file_nonexistent():
    p = _ROOT / "ghost_file_xyz.json"
    result = classify_file(p)
    assert result["exists"] is False
    assert result["size_bytes"] == 0


# ─── CLASSIFICATION_LABELS ────────────────────────────────────────────────────

def test_all_levels_have_labels():
    for level in [C1_PUBLIC, C2_INTERNE, C3_CONFIDENTIEL, C4_SECRET]:
        assert level in CLASSIFICATION_LABELS
        assert len(CLASSIFICATION_LABELS[level]) > 5


# ─── build_classification_report ─────────────────────────────────────────────

def test_report_structure():
    assets = [
        {"classification": C4_SECRET,       "path": "a.env",   "size_bytes": 100, "exists": True},
        {"classification": C3_CONFIDENTIEL, "path": "b.json",  "size_bytes": 200, "exists": True},
        {"classification": C2_INTERNE,      "path": "c.py",    "size_bytes": 300, "exists": True},
        {"classification": C1_PUBLIC,       "path": "d.md",    "size_bytes": 50,  "exists": True},
    ]
    report = build_classification_report(assets)
    assert "stats" in report
    assert "critical_assets" in report
    assert "total_assets" in report
    assert report["total_assets"] == 4
    assert report["critical_count"] == 2  # C3 + C4


def test_report_stats_per_level():
    assets = [
        {"classification": C4_SECRET, "path": "k.env", "size_bytes": 10, "exists": True},
        {"classification": C4_SECRET, "path": "l.key", "size_bytes": 20, "exists": True},
    ]
    report = build_classification_report(assets)
    assert report["stats"][C4_SECRET]["count"] == 2


def test_report_meta():
    report = build_classification_report([])
    assert "_meta" in report
    assert report["_meta"]["project"] == "ALFRED"


# ─── data_flow_mapper ─────────────────────────────────────────────────────────

def test_registry_not_empty():
    registry = get_registry()
    assert len(registry) >= 5

def test_all_treatments_have_required_fields():
    for t in ALFRED_TREATMENTS:
        assert t.id
        assert t.name
        assert t.purpose
        assert t.legal_basis
        assert t.retention_days > 0

def test_get_treatment_by_id():
    t = get_treatment_by_id("T01")
    assert t is not None
    assert t.name != ""

def test_get_treatment_by_id_missing():
    assert get_treatment_by_id("T99") is None

def test_no_cross_border_transfers():
    """Tous les traitements ALFRED doivent être locaux (pas de transfert hors UE)."""
    for t in ALFRED_TREATMENTS:
        assert t.cross_border is False, f"Transfert hors UE non attendu : {t.id} {t.name}"

def test_health_data_treatment_exists():
    """Les données de santé doivent être identifiées (Art. 9 RGPD)."""
    health = [t for t in ALFRED_TREATMENTS if "santé" in " ".join(t.data_categories).lower()]
    assert len(health) >= 1

# ─── build_rgpd_report ────────────────────────────────────────────────────────

def test_rgpd_report_structure():
    report = build_rgpd_report()
    assert "_meta" in report
    assert "treatments" in report
    assert "summary" in report
    assert report["treatments_count"] == len(ALFRED_TREATMENTS)

def test_rgpd_report_retention_human():
    report = build_rgpd_report()
    for t in report["treatments"]:
        assert "retention_human" in t
        assert "an" in t["retention_human"] or "jour" in t["retention_human"]

def test_rgpd_report_cross_border_text():
    report = build_rgpd_report()
    for t in report["treatments"]:
        assert "cross_border_text" in t

# ─── check_rgpd_compliance ───────────────────────────────────────────────────

def test_compliance_structure():
    result = check_rgpd_compliance()
    assert "score" in result
    assert "max_score" in result
    assert "compliance_rate" in result
    assert "checks" in result
    assert "grade" in result

def test_compliance_high_score():
    """ALFRED doit avoir un score de conformité RGPD élevé."""
    result = check_rgpd_compliance()
    assert result["compliance_rate"] >= 80, (
        f"Score RGPD trop bas : {result['compliance_rate']}% "
        f"— vérifier {[c for c in result['checks'] if not c['ok']]}"
    )

def test_compliance_no_cross_border_check_passes():
    result = check_rgpd_compliance()
    cross_check = next((c for c in result["checks"] if "hors UE" in c["title"]), None)
    assert cross_check is not None
    assert cross_check["ok"] is True
