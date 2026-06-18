"""
PROJECT      : ALFRED
BLOCK        : B20
FUNCTION     : XX.XX
FILE         : test_role_manager.py
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
Tests B20 — role_manager.py
"""

from src.security.role_manager import (
    normalize_role,
    role_exists,
    list_roles,
    get_role_description,
    get_role_level,
    is_role_at_least,
    list_role_details,
)


def test_normalize_role():
    assert normalize_role(" owner ") == "OWNER"
    assert normalize_role("") == "GUEST"


def test_role_exists_true():
    assert role_exists("OWNER") is True


def test_role_exists_false():
    assert role_exists("UNKNOWN_ROLE") is False


def test_list_roles_returns_dict():
    roles = list_roles()

    assert isinstance(roles, dict)
    assert "OWNER" in roles


def test_get_role_description_known():
    description = get_role_description("OWNER")

    assert "contrôle complet" in description


def test_get_role_description_unknown():
    assert get_role_description("UNKNOWN") == "Rôle inconnu."


def test_get_role_level():
    assert get_role_level("OWNER") > get_role_level("GUEST")


def test_is_role_at_least_true():
    assert is_role_at_least("OWNER", "ADMIN") is True


def test_is_role_at_least_false():
    assert is_role_at_least("GUEST", "ADMIN") is False


def test_list_role_details():
    details = list_role_details()

    assert isinstance(details, list)
    assert details
    assert "role" in details[0]
    assert "description" in details[0]
    assert "level" in details[0]