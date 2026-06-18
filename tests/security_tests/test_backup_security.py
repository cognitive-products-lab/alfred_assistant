"""
PROJECT      : ALFRED
BLOCK        : B20
FUNCTION     : XX.XX
FILE         : test_backup_security.py
ROLE         : TO_DEFINE

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-05-10
UPDATED      : 2026-05-10
VERSION      : V1.0
STATUS       : DRAFT

DESCRIPTION :
TO_COMPLETE
"""

"""
Tests B20 — backup_security.py
Utilise tempfile au lieu de tmp_path (évite PermissionError Windows sur .pytest_cache)
"""

import tempfile
import shutil
from pathlib import Path

import pytest

import src.security.backup_security as backup_security
from src.security.backup_security import (
    secure_backup,
    backup_many,
    list_backups,
    summarize_backups,
    cleanup_old_backups,
)


@pytest.fixture(autouse=True)
def isolate_backup_dir(tmp_path, monkeypatch):
    """Empeche les tests d'ecrire/supprimer dans backup/security/ (dossier reel)."""
    backup_dir = tmp_path / "backup_security"
    backup_dir.mkdir(parents=True, exist_ok=True)
    monkeypatch.setattr(backup_security, "BACKUP_DIR", backup_dir)
    monkeypatch.setattr(backup_security, "MANIFEST_FILE", backup_dir / ".manifest.json")
    yield


def test_secure_backup_creates_backup():
    tmp_dir = Path(tempfile.mkdtemp())
    try:
        source = tmp_dir / "sensitive.txt"
        source.write_text("secret-data", encoding="utf-8")

        backup_path = secure_backup(str(source), label="pytest")
        backup = Path(backup_path)

        assert backup.exists()
        assert backup.read_text(encoding="utf-8") == "secret-data"
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)


def test_secure_backup_missing_file_raises():
    with pytest.raises(FileNotFoundError):
        secure_backup("missing_file_for_test.txt")


def test_secure_backup_directory_raises():
    tmp_dir = Path(tempfile.mkdtemp())
    try:
        with pytest.raises(ValueError):
            secure_backup(str(tmp_dir))
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)


def test_backup_many_success_and_error():
    tmp_dir = Path(tempfile.mkdtemp())
    try:
        source = tmp_dir / "file1.txt"
        source.write_text("content", encoding="utf-8")

        result = backup_many(
            [
                str(source),
                "missing_file_for_batch_test.txt",
            ],
            label="pytest_batch",
        )

        assert len(result["success"]) == 1
        assert len(result["errors"]) == 1
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)


def test_list_backups_returns_list():
    backups = list_backups()

    assert isinstance(backups, list)


def test_summarize_backups_contains_expected_fields():
    summary = summarize_backups()

    assert "total_backups" in summary
    assert "total_size_bytes" in summary
    assert "last_backup" in summary
    assert "backup_dir" in summary


def test_cleanup_old_backups_returns_summary():
    result = cleanup_old_backups(keep_last=20)

    assert "deleted" in result
    assert "kept" in result