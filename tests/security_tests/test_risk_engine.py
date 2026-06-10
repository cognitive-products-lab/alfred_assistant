"""
════════════════════════════════════════════════════════════
PROJECT      : ALFRED — tests risk_engine (EBIOS RM)
BLOCK        : B20 · FUNCTION : 20.TEST
VERSION      : V1.0 · STATUS : ACTIVE
════════════════════════════════════════════════════════════
"""
import pytest
from src.security.risk_engine import (
    risk_score, risk_level, RiskScenario,
    ALFRED_RISKS, build_risk_matrix, get_real_posture,
    LIKELIHOOD, IMPACT,
)


# ─── risk_score ───────────────────────────────────────────────────────────────

def test_risk_score_max():
    assert risk_score("MAXIMAL", "CRITIQUE") == 16

def test_risk_score_min():
    assert risk_score("MINIMAL", "NEGLIGEABLE") == 1

def test_risk_score_formula():
    assert risk_score("SIGNIFICATIF", "IMPORTANT") == 3 * 3  # = 9

def test_risk_score_unknown_defaults_to_1():
    assert risk_score("INCONNU", "CRITIQUE") == 1 * 4  # likelihood default 1


# ─── risk_level ───────────────────────────────────────────────────────────────

@pytest.mark.parametrize("score,expected", [
    (16, "CRITIQUE"),
    (12, "CRITIQUE"),
    (11, "ELEVE"),
    (8,  "ELEVE"),
    (7,  "MODERE"),
    (4,  "MODERE"),
    (3,  "FAIBLE"),
    (1,  "FAIBLE"),
])
def test_risk_level_mapping(score, expected):
    assert risk_level(score) == expected


# ─── RiskScenario ─────────────────────────────────────────────────────────────

def test_scenario_properties():
    s = RiskScenario(
        id="TEST",
        threat_source="Attaquant",
        feared_event="Compromission",
        attack_path="Via API",
        asset_targeted="Clés (C4)",
        likelihood="SIGNIFICATIF",
        impact="CRITIQUE",
    )
    assert s.raw_score == 12   # 3 × 4
    assert s.level == "CRITIQUE"


def test_scenario_faible():
    s = RiskScenario(
        id="T2", threat_source="A", feared_event="E",
        attack_path="P", asset_targeted="X",
        likelihood="MINIMAL", impact="NEGLIGEABLE",
    )
    assert s.raw_score == 1
    assert s.level == "FAIBLE"


# ─── ALFRED_RISKS catalogue ───────────────────────────────────────────────────

def test_catalog_not_empty():
    assert len(ALFRED_RISKS) >= 6

def test_all_risks_have_required_fields():
    for r in ALFRED_RISKS:
        assert r.id
        assert r.threat_source
        assert r.feared_event
        assert r.likelihood in LIKELIHOOD
        assert r.impact in IMPACT
        assert r.existing_measures, f"{r.id} sans mesures existantes"

def test_all_ids_unique():
    ids = [r.id for r in ALFRED_RISKS]
    assert len(ids) == len(set(ids))

def test_risks_have_categories():
    assert all(r.category for r in ALFRED_RISKS)

def test_critical_risks_have_measures():
    critical = [r for r in ALFRED_RISKS if r.level == "CRITIQUE"]
    for r in critical:
        assert len(r.existing_measures) >= 2, f"{r.id} critique sans mesures suffisantes"


# ─── build_risk_matrix ────────────────────────────────────────────────────────

def test_matrix_structure():
    matrix = build_risk_matrix(adjust_for_posture=False)
    assert "_meta" in matrix
    assert "scenarios" in matrix
    assert "by_level" in matrix
    assert "priority_actions" in matrix
    assert "generated_at" in matrix

def test_matrix_scenario_count():
    matrix = build_risk_matrix(adjust_for_posture=False)
    assert matrix["scenarios_count"] == len(ALFRED_RISKS)
    assert len(matrix["scenarios"]) == len(ALFRED_RISKS)

def test_matrix_by_level_keys():
    matrix = build_risk_matrix(adjust_for_posture=False)
    for level in ["CRITIQUE", "ELEVE", "MODERE", "FAIBLE"]:
        assert level in matrix["by_level"]

def test_matrix_sorted_by_score():
    matrix = build_risk_matrix(adjust_for_posture=False)
    scores = [s["raw_score"] for s in matrix["scenarios"]]
    assert scores == sorted(scores, reverse=True)

def test_matrix_posture_adjustment():
    matrix_raw = build_risk_matrix(adjust_for_posture=False)
    matrix_adj = build_risk_matrix(adjust_for_posture=True)
    # Avec MFA actif (probable), R01 doit être réduit
    r01_raw = next(s for s in matrix_raw["scenarios"] if s["id"] == "R01")
    r01_adj = next(s for s in matrix_adj["scenarios"] if s["id"] == "R01")
    # Le score ajusté doit être <= score brut
    assert r01_adj["raw_score"] <= r01_raw["raw_score"]

def test_matrix_global_level_valid():
    matrix = build_risk_matrix()
    assert matrix["global_level"] in {"CRITIQUE", "ELEVE", "MODERE", "FAIBLE"}


# ─── get_real_posture ─────────────────────────────────────────────────────────

def test_posture_structure():
    posture = get_real_posture()
    assert "mfa_active" in posture
    assert "backup_ok" in posture
    assert "audit_active" in posture

def test_posture_mfa_active():
    posture = get_real_posture()
    # MFA doit être actif pour OWNER dans la config courante
    assert posture["mfa_active"] is True


# ─── Cohérence globale ────────────────────────────────────────────────────────

def test_no_unmitigated_critical():
    """Tout risque CRITIQUE doit avoir au moins 2 mesures existantes."""
    matrix = build_risk_matrix(adjust_for_posture=True)
    for s in matrix["scenarios"]:
        if s["level"] == "CRITIQUE":
            assert len(s.get("existing_measures", [])) >= 2, (
                f"Risque CRITIQUE sans mesures suffisantes : {s['id']}"
            )
