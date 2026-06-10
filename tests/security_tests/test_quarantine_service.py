"""
PROJECT      : ALFRED
BLOCK        : B20
FUNCTION     : XX.XX
FILE         : test_quarantine_service.py
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
Tests B20 — quarantine_service.py
"""

from src.security.quarantine_service import (
    quarantine_item,
    quarantine_module,
    is_quarantined,
    release_item,
    release_module,
    list_quarantined,
    summarize_quarantine,
)


def test_quarantine_item_marks_item_as_quarantined():
    entry = quarantine_item(
        item_name="module_test_quarantine",
        reason="pytest reason",
        item_type="module",
        severity="HIGH",
        source="pytest",
    )

    assert entry["item_name"] == "module_test_quarantine"
    assert entry["status"] == "QUARANTINED"
    assert is_quarantined("module_test_quarantine") is True


def test_release_item_releases_quarantine():
    quarantine_item(
        item_name="module_test_release",
        reason="pytest reason",
        item_type="module",
        severity="HIGH",
    )

    result = release_item(
        item_name="module_test_release",
        reason="pytest release",
    )

    assert result is True
    assert is_quarantined("module_test_release") is False


def test_release_unknown_item_returns_false():
    result = release_item("unknown_quarantine_item_pytest")

    assert result is False


def test_quarantine_module_legacy_function():
    quarantine_module(
        module_name="legacy_module_test",
        reason="legacy pytest",
    )

    assert is_quarantined("legacy_module_test") is True

    release_module("legacy_module_test")

    assert is_quarantined("legacy_module_test") is False


def test_list_quarantined_returns_list():
    quarantine_item(
        item_name="module_test_list",
        reason="pytest list",
        item_type="module",
    )

    items = list_quarantined(active_only=True)

    assert isinstance(items, list)
    assert any(item["item_name"] == "module_test_list" for item in items)


def test_summarize_quarantine_contains_expected_fields():
    summary = summarize_quarantine()

    assert "active_total" in summary
    assert "history_total" in summary
    assert "by_type" in summary
    assert "by_severity" in summary
    assert "active_items" in summary