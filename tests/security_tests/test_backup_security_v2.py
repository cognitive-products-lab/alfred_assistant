"""
════════════════════════════════════════════════════════════
PROJECT      : ALFRED — tests backup_security V2
BLOCK        : B20 · FUNCTION : 20.TEST
VERSION      : V2.0 · STATUS : ACTIVE
════════════════════════════════════════════════════════════
"""
import json
import pytest
from pathlib import Path
from src.security.backup_security import (
    secure_backup, backup_many, list_backups, summarize_backups,
    cleanup_old_backups, cleanup_old_backups_by_ttl,
    verify_backup_integrity, restore_backup,
    _sha256, BACKUP_DIR, MANIFEST_FILE,
)


@pytest.fixture(autouse=True)
def clean_backup_dir(tmp_path, monkeypatch):
    """Redirige BACKUP_DIR et MANIFEST_FILE vers tmp_path."""
    import src.security.backup_security as bk
    monkeypatch.setattr(bk, "BACKUP_DIR", tmp_path / "backup")
    monkeypatch.setattr(bk, "MANIFEST_FILE", tmp_path / "backup" / ".manifest.json")
    (tmp_path / "backup").mkdir()
    yield


@pytest.fixture
def sample_file(tmp_path):
    f = tmp_path / "secret.json"
    f.write_text('{"key": "value", "sensitive": true}', encoding="utf-8")
    return f


# ─── _sha256 ──────────────────────────────────────────────────────────────────

def test_sha256_consistent(sample_file):
    h1 = _sha256(sample_file)
    h2 = _sha256(sample_file)
    assert h1 == h2 and len(h1) == 64


def test_sha256_differs_on_change(tmp_path):
    f = tmp_path / "file.txt"
    f.write_text("hello")
    h1 = _sha256(f)
    f.write_text("world")
    h2 = _sha256(f)
    assert h1 != h2


# ─── secure_backup V2 ────────────────────────────────────────────────────────

def test_secure_backup_creates_file(sample_file):
    dest = secure_backup(str(sample_file))
    assert Path(dest).exists()


def test_secure_backup_manifest_entry(sample_file):
    import src.security.backup_security as bk
    secure_backup(str(sample_file))
    manifest = json.loads(bk.MANIFEST_FILE.read_text(encoding="utf-8"))
    assert "secret.json" in manifest
    assert len(manifest["secret.json"]) == 1
    assert "src_hash" in manifest["secret.json"][0]
    assert "dst_hash" in manifest["secret.json"][0]


def test_secure_backup_missing_source():
    with pytest.raises(FileNotFoundError):
        secure_backup("/nonexistent/path.json")


def test_secure_backup_empty_path():
    with pytest.raises(ValueError):
        secure_backup("")


def test_secure_backup_with_label(sample_file):
    dest = secure_backup(str(sample_file), label="pre-update")
    assert "pre-update" in dest


def test_secure_backup_rotation(sample_file):
    """Avec max_keep=2 et 3 backups → seulement 2 conservés."""
    import src.security.backup_security as bk
    for _ in range(3):
        secure_backup(str(sample_file), max_keep=2)
    manifest = json.loads(bk.MANIFEST_FILE.read_text(encoding="utf-8"))
    assert len(manifest["secret.json"]) <= 2


# ─── verify_backup_integrity ─────────────────────────────────────────────────

def test_verify_integrity_ok(sample_file):
    dest = secure_backup(str(sample_file))
    result = verify_backup_integrity(dest)
    assert result["ok"] is True


def test_verify_integrity_tampered(sample_file):
    dest = secure_backup(str(sample_file))
    Path(dest).write_text("TAMPERED", encoding="utf-8")
    result = verify_backup_integrity(dest)
    assert result["ok"] is False


def test_verify_integrity_missing():
    result = verify_backup_integrity("/nonexistent/backup.bak")
    assert result["ok"] is False


def test_verify_integrity_not_in_manifest(tmp_path):
    f = tmp_path / "orphan.bak"
    f.write_text("orphan backup")
    result = verify_backup_integrity(str(f))
    assert result["ok"] is None   # non référencé


# ─── restore_backup ──────────────────────────────────────────────────────────

def test_restore_backup_ok(sample_file, tmp_path):
    dest_backup = secure_backup(str(sample_file))
    restore_dest = tmp_path / "restored.json"
    result = restore_backup(dest_backup, str(restore_dest))
    assert result["ok"] is True
    assert restore_dest.exists()
    assert restore_dest.read_text(encoding="utf-8") == sample_file.read_text(encoding="utf-8")


def test_restore_backup_missing():
    result = restore_backup("/nonexistent.bak", "/tmp/dest.json")
    assert result["ok"] is False


def test_restore_backup_tampered_blocked(sample_file, tmp_path):
    dest_backup = secure_backup(str(sample_file))
    Path(dest_backup).write_text("TAMPERED", encoding="utf-8")
    result = restore_backup(dest_backup, str(tmp_path / "out.json"), verify=True)
    assert result["ok"] is False


# ─── cleanup TTL ──────────────────────────────────────────────────────────────

def test_cleanup_ttl_keeps_recent(sample_file):
    secure_backup(str(sample_file))
    result = cleanup_old_backups_by_ttl(ttl_days=30)
    assert result["deleted"] == 0


def test_cleanup_ttl_deletes_old(sample_file, monkeypatch):
    """Simuler un backup "vieux" en patchant son timestamp dans le manifeste."""
    import src.security.backup_security as bk
    from datetime import timedelta
    secure_backup(str(sample_file))
    manifest = json.loads(bk.MANIFEST_FILE.read_text(encoding="utf-8"))
    from datetime import datetime, timezone
    old_ts = (datetime.now(timezone.utc) - timedelta(days=60)).isoformat()
    manifest["secret.json"][0]["timestamp"] = old_ts
    bk.MANIFEST_FILE.write_text(json.dumps(manifest), encoding="utf-8")
    result = cleanup_old_backups_by_ttl(ttl_days=30)
    assert result["deleted"] >= 1


# ─── backup_many V2 ───────────────────────────────────────────────────────────

def test_backup_many_ok(sample_file, tmp_path):
    f2 = tmp_path / "config.json"
    f2.write_text('{"setting": true}', encoding="utf-8")
    result = backup_many([str(sample_file), str(f2)])
    assert len(result["success"]) == 2
    assert len(result["errors"]) == 0


def test_backup_many_partial_error(sample_file):
    result = backup_many([str(sample_file), "/nonexistent/file.json"])
    assert len(result["success"]) == 1
    assert len(result["errors"]) == 1


# ─── summarize V2 ────────────────────────────────────────────────────────────

def test_summarize_backups_empty():
    s = summarize_backups()
    assert s["total_backups"] == 0


def test_summarize_backups_with_files(sample_file):
    secure_backup(str(sample_file))
    s = summarize_backups()
    assert s["total_backups"] >= 1
    assert s["total_size_bytes"] >= 0
    assert "manifest_entries" in s
