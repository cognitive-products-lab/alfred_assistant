"""
PROJECT      : ALFRED
BLOCK        : B20
FUNCTION     : XX.XX
FILE         : test_access_control.py
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
Tests B20 — access_control.py
"""

import pytest

from src.security.access_control import (
    has_access,
    check_access,
    require_access,
)


def test_has_access_owner_permission():
    assert has_access("OWNER", "DELETE_DATA") is True


def test_has_access_guest_denied():
    assert has_access("GUEST", "DELETE_DATA") is False


def test_check_access_allow():
    result = check_access(
        role="OWNER",
        permission="RUN_AI_MODULE",
        user_id="celine",
        request_id="req-access-001",
    )

    assert result["allowed"] is True
    assert result["role"] == "OWNER"
    assert result["permission"] == "RUN_AI_MODULE"
    assert result["reason"] == "ALLOW"


def test_check_access_unknown_role():
    result = check_access(
        role="UNKNOWN_ROLE",
        permission="RUN_AI_MODULE",
    )

    assert result["allowed"] is False
    assert result["reason"] == "ROLE_UNKNOWN"


def test_check_access_empty_permission():
    result = check_access(
        role="OWNER",
        permission="",
    )

    assert result["allowed"] is False
    assert result["reason"] == "PERMISSION_EMPTY"


def test_check_access_unknown_permission():
    result = check_access(
        role="OWNER",
        permission="UNKNOWN_PERMISSION",
    )

    assert result["allowed"] is False
    assert result["reason"] == "PERMISSION_UNKNOWN"


def test_check_access_permission_denied():
    result = check_access(
        role="GUEST",
        permission="ACCESS_SECURITY_LOGS",
    )

    assert result["allowed"] is False
    assert result["reason"] == "PERMISSION_DENIED"


def test_require_access_allow():
    require_access("OWNER", "DELETE_DATA")


def test_require_access_denied_raises():
    with pytest.raises(PermissionError):
        require_access("GUEST", "DELETE_DATA")