"""
PROJECT      : ALFRED
BLOCK        : B20
FUNCTION     : XX.XX
FILE         : test_permission_manager.py
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
Tests B20 — permission_manager.py
"""

from src.security.permission_manager import (
    get_permissions,
    list_permissions,
    all_permissions,
    permission_exists,
    role_has_permission,
    add_permission_to_role,
    summarize_permissions,
    normalize_permission,
    normalize_role,
)


def test_normalize_permission():
    assert normalize_permission(" read_memory ") == "READ_MEMORY"


def test_normalize_role():
    assert normalize_role(" owner ") == "OWNER"
    assert normalize_role("") == "GUEST"


def test_get_permissions_owner_contains_delete_data():
    permissions = get_permissions("OWNER")

    assert "DELETE_DATA" in permissions


def test_get_permissions_unknown_role_empty():
    assert get_permissions("UNKNOWN") == []


def test_list_permissions_returns_dict():
    permissions = list_permissions()

    assert isinstance(permissions, dict)
    assert "OWNER" in permissions


def test_all_permissions_contains_run_ai_module():
    permissions = all_permissions()

    assert "RUN_AI_MODULE" in permissions


def test_permission_exists_true():
    assert permission_exists("RUN_AI_MODULE") is True


def test_permission_exists_false():
    assert permission_exists("UNKNOWN_PERMISSION") is False


def test_role_has_permission_true():
    assert role_has_permission("OWNER", "DELETE_DATA") is True


def test_role_has_permission_false():
    assert role_has_permission("GUEST", "DELETE_DATA") is False


def test_add_permission_to_role():
    result = add_permission_to_role("USER", "TEST_PERMISSION")

    assert result is True
    assert role_has_permission("USER", "TEST_PERMISSION") is True


def test_add_permission_to_unknown_role_false():
    assert add_permission_to_role("UNKNOWN", "TEST_PERMISSION") is False


def test_summarize_permissions():
    summary = summarize_permissions()

    assert "roles_count" in summary
    assert "unique_permissions_count" in summary
    assert summary["roles_count"] >= 1