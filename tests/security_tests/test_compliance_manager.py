"""
PROJECT      : ALFRED
BLOCK        : B20
FUNCTION     : XX.XX
FILE         : test_compliance_manager.py
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
Tests B20 — compliance_manager.py
"""

from src.security.compliance_manager import (
    list_sensitive_files,
    compliance_report,
    delete_user_data,
    check_privacy_readiness,
)


def test_list_sensitive_files_returns_list():
    files = list_sensitive_files()

    assert isinstance(files, list)
    assert files
    assert "path" in files[0]
    assert "exists" in files[0]
    assert "size_bytes" in files[0]


def test_compliance_report_contains_expected_fields():
    report = compliance_report()

    assert report["local_first"] is True
    assert "known_sensitive_files" in report
    assert "existing_sensitive_files" in report
    assert "privacy_controls" in report


def test_delete_user_data_requires_confirmation():
    result = delete_user_data(confirm=False)

    assert result["confirmed"] is False
    assert result["deleted"] == []
    assert result["errors"] == []


def test_delete_user_data_with_confirmation_returns_structure():
    result = delete_user_data(confirm=True)

    assert result["confirmed"] is True
    assert "deleted" in result
    assert "missing" in result
    assert "errors" in result


def test_check_privacy_readiness_contains_score():
    result = check_privacy_readiness()

    assert "privacy_score" in result
    assert "privacy_level" in result
    assert "checks" in result
    assert result["privacy_level"] in {"GOOD", "PARTIAL", "WEAK"}