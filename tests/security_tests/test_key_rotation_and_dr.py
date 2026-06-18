"""
════════════════════════════════════════════════════════════
PROJECT      : ALFRED — tests key_rotation_scheduler + disaster_recovery
BLOCK        : B20 · FUNCTION : 20.TEST
VERSION      : V1.0 · STATUS : ACTIVE
════════════════════════════════════════════════════════════
"""
import json
import pytest
from pathlib import Path
from src.security.key_rotation_scheduler import (
    check_key_age, check_all_keys, record_rotation,
    get_rotation_history, get_last_rotation, get_smsi_summary,
    ROTATION_THRESHOLDS,
)
from src.security.disaster_recovery import (
    create_snapshot, list_snapshots, verify_restore,
    build_pca_report, get_latest_snapshot,
    _SNAPSHOT_DIR, _DR_LOG,
)


@pytest.fixture(autouse=True)
def clean_dr_state(tmp_path, monkeypatch):
    """Isole les snapshots et logs dans tmp_path."""
    import src.security.disaster_recovery as dr
    import src.security.key_rotation_scheduler as kr
    snap = tmp_path / "snapshots"
    snap.mkdir()
    log  = tmp_path / "dr_log.json"
    rot  = tmp_path / "rotation_log.json"
    monkeypatch.setattr(dr, "_SNAPSHOT_DIR", snap)
    monkeypatch.setattr(dr, "_DR_LOG", log)
    monkeypatch.setattr(kr, "_ROTATION_LOG", rot)
    yield


@pytest.fixture
def inject_secrets(monkeypatch):
    monkeypatch.setenv("FERNET_KEY",     "test_fernet_key_value")
    monkeypatch.setenv("SECRET_KEY",     "test_secret_key_value")
    monkeypatch.setenv("API_SECRET_KEY", "test_api_key_value")
    monkeypatch.setenv("PIN_SALT",       "test_pin_salt_value")
    yield


# ─── check_key_age ────────────────────────────────────────────────────────────

def test_check_key_age_structure(inject_secrets):
    result = check_key_age("FERNET_KEY")
    assert "key" in result
    assert "needs_rotation" in result
    assert "threshold_days" in result
    assert "status" in result

def test_check_key_age_existing(inject_secrets):
    result = check_key_age("FERNET_KEY")
    assert result["exists"] is True

def test_check_key_age_missing(monkeypatch):
    monkeypatch.delenv("FERNET_KEY", raising=False)
    result = check_key_age("FERNET_KEY")
    assert result["exists"] is False
    assert result["needs_rotation"] is False

def test_check_key_age_very_high_threshold(inject_secrets):
    result = check_key_age("FERNET_KEY", threshold_days=9999)
    assert result["needs_rotation"] is False
    assert result["status"] == "OK"

def test_check_key_age_custom_threshold(inject_secrets):
    """Un seuil personnalisé (1 jour) ne déclenche pas rotation si clé est du jour."""
    result_high = check_key_age("FERNET_KEY", threshold_days=9999)
    result_low  = check_key_age("FERNET_KEY", threshold_days=1)
    # Avec threshold=9999, pas de rotation ; avec threshold=1, dépend de l'âge
    assert result_high["needs_rotation"] is False
    assert result_low["threshold_days"] == 1


# ─── check_all_keys ───────────────────────────────────────────────────────────

def test_check_all_keys_structure(inject_secrets):
    result = check_all_keys()
    assert "checked_at" in result
    assert "keys" in result
    assert "rotation_needed" in result
    assert "all_ok" in result

def test_check_all_keys_contains_known(inject_secrets):
    result = check_all_keys()
    for key in ROTATION_THRESHOLDS:
        assert key in result["keys"]


# ─── record_rotation / history ────────────────────────────────────────────────

def test_record_rotation(inject_secrets):
    record_rotation("FERNET_KEY", notes="test")
    history = get_rotation_history("FERNET_KEY")
    assert len(history) == 1
    assert history[0]["key"] == "FERNET_KEY"

def test_record_rotation_multiple(inject_secrets):
    record_rotation("FERNET_KEY")
    record_rotation("SECRET_KEY")
    assert len(get_rotation_history("FERNET_KEY")) == 1
    assert len(get_rotation_history("SECRET_KEY")) == 1

def test_get_last_rotation_none():
    assert get_last_rotation("NONEXISTENT_KEY") is None

def test_get_last_rotation_present(inject_secrets):
    record_rotation("FERNET_KEY", notes="after rotation")
    last = get_last_rotation("FERNET_KEY")
    assert last is not None
    assert last["notes"] == "after rotation"

def test_rotation_reduces_age(inject_secrets):
    """Après enregistrement d'une rotation, needs_rotation doit baisser."""
    record_rotation("FERNET_KEY")
    result = check_key_age("FERNET_KEY")
    # Après rotation immédiate, age_since ≈ 0 → pas de rotation requise
    assert result["needs_rotation"] is False


# ─── get_smsi_summary ─────────────────────────────────────────────────────────

def test_smsi_summary_structure(inject_secrets):
    summary = get_smsi_summary()
    assert "smsi_score" in summary
    assert "smsi_grade" in summary
    assert "key_rotation" in summary
    assert "rgpd_compliance" in summary
    assert "risk_summary" in summary

def test_smsi_score_range(inject_secrets):
    summary = get_smsi_summary()
    assert 0 <= summary["smsi_score"] <= 100

def test_smsi_grade_valid(inject_secrets):
    summary = get_smsi_summary()
    assert summary["smsi_grade"] in {"A", "B", "C"}


# ─── create_snapshot ──────────────────────────────────────────────────────────

def test_create_snapshot_ok(tmp_path, monkeypatch):
    import src.security.disaster_recovery as dr
    # Créer des fichiers sources dans tmp_path
    src_dir = tmp_path / "src_project"
    (src_dir / "data" / "users").mkdir(parents=True)
    (src_dir / "data" / "users" / "user.json").write_text('{"name":"test"}')
    monkeypatch.setattr(dr, "_ROOT", src_dir)

    result = create_snapshot(label="test", paths=["data/users/"])
    assert result["ok"] is True
    assert len(result["files_saved"]) >= 1
    assert result["size_bytes"] > 0

def test_create_snapshot_manifest(tmp_path, monkeypatch):
    import src.security.disaster_recovery as dr
    src_dir = tmp_path / "src_project"
    (src_dir / "data").mkdir(parents=True)
    (src_dir / "data" / "file.json").write_text('{}')
    monkeypatch.setattr(dr, "_ROOT", src_dir)

    result = create_snapshot(label="manifest_test", paths=["data/"])
    snap_dir = Path(result["snapshot_dir"])
    assert (snap_dir / "_manifest.json").exists()
    m = json.loads((snap_dir / "_manifest.json").read_text(encoding="utf-8"))
    assert "snapshot_id" in m

def test_create_snapshot_empty_paths(tmp_path, monkeypatch):
    """Snapshot avec chemins inexistants → 0 fichiers mais pas d'erreur."""
    import src.security.disaster_recovery as dr
    monkeypatch.setattr(dr, "_ROOT", tmp_path)
    result = create_snapshot(paths=["nonexistent/path/"])
    assert result["ok"] is True
    assert len(result["files_saved"]) == 0


# ─── list_snapshots ───────────────────────────────────────────────────────────

def test_list_snapshots_empty():
    snaps = list_snapshots()
    assert snaps == []

def test_list_snapshots_after_create(tmp_path, monkeypatch):
    import src.security.disaster_recovery as dr
    src_dir = tmp_path / "src"
    (src_dir / "data").mkdir(parents=True)
    (src_dir / "data" / "f.json").write_text("{}")
    monkeypatch.setattr(dr, "_ROOT", src_dir)
    create_snapshot(label="listed", paths=["data/"])
    snaps = list_snapshots()
    assert len(snaps) == 1


# ─── test_restore ────────────────────────────────────────────────────────────

def test_restore_ok(tmp_path, monkeypatch):
    import src.security.disaster_recovery as dr
    src_dir = tmp_path / "src"
    (src_dir / "data").mkdir(parents=True)
    (src_dir / "data" / "critical.json").write_text('{"data": true}')
    monkeypatch.setattr(dr, "_ROOT", src_dir)

    snap = create_snapshot(label="restore_test", paths=["data/"])
    restore_dir = tmp_path / "restore_out"
    restore_dir.mkdir(parents=True)
    result = verify_restore(snap["snapshot_id"], test_dir=restore_dir)
    assert result["ok"] is True
    assert result["integrity_check"] is True

def test_restore_missing_snapshot():
    result = verify_restore("nonexistent_snapshot_xyz")
    assert result["ok"] is False


# ─── build_pca_report ────────────────────────────────────────────────────────

def test_pca_report_structure():
    report = build_pca_report()
    assert "_meta" in report
    assert "snapshots_count" in report
    assert "rpo_target_hours" in report
    assert "checks" in report
    assert "compliance_rate" in report

def test_pca_report_without_snapshots():
    report = build_pca_report()
    assert report["snapshots_count"] == 0
    assert report["rpo_met"] is False

def test_pca_report_grade():
    report = build_pca_report()
    assert report["grade"] in {"A", "B", "C"}

def test_pca_report_after_snapshot(tmp_path, monkeypatch):
    import src.security.disaster_recovery as dr
    src_dir = tmp_path / "src"
    (src_dir / "data").mkdir(parents=True)
    (src_dir / "data" / "f.json").write_text("{}")
    monkeypatch.setattr(dr, "_ROOT", src_dir)

    create_snapshot(paths=["data/"])
    report = build_pca_report()
    assert report["snapshots_count"] == 1
    assert report["latest_snapshot"] is not None
