"""
════════════════════════════════════════════════════════════
PROJECT      : ALFRED
BLOCK        : B10
FUNCTION     : 10.TEST
FILE         : tests/security_tests/test_cpl_role_access.py
ROLE         : Tests unitaires — cpl_role_access.py

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-07-11
VERSION      : V1.0
STATUS       : ACTIVE

DESCRIPTION :
Couvre : is_business_role, get_allowed_domains, is_domain_allowed,
filter_by_role_access (rôles métier ALFRED CPL — Chef de projet, RH).
════════════════════════════════════════════════════════════
"""
from dataclasses import dataclass, field
from typing import Any

from src.security.cpl_role_access import (
    is_business_role,
    get_allowed_domains,
    is_domain_allowed,
    filter_by_role_access,
)


@dataclass
class _FakeRankedKnowledge:
    knowledge_id: str
    data: dict[str, Any] = field(default_factory=dict)


def _item(knowledge_id: str, domain: str) -> _FakeRankedKnowledge:
    return _FakeRankedKnowledge(knowledge_id=knowledge_id, data={"domain": domain})


def test_business_role_recognized():
    assert is_business_role("CHEF_DE_PROJET") is True
    assert is_business_role("RH") is True


def test_system_role_not_business_role():
    assert is_business_role("OWNER") is False
    assert is_business_role("") is False


def test_chef_de_projet_allows_cpl_domain():
    assert is_domain_allowed("CHEF_DE_PROJET", "cpl") is True


def test_chef_de_projet_denies_hr_domain():
    assert is_domain_allowed("CHEF_DE_PROJET", "ressources_humaines") is False


def test_rh_allows_hr_domain():
    assert is_domain_allowed("RH", "ressources_humaines") is True


def test_rh_denies_cpl_domain():
    assert is_domain_allowed("RH", "cpl") is False


def test_system_role_not_restricted_by_domain_filter():
    # Un rôle système (non métier CPL) n'est pas concerné par ce filtre.
    assert is_domain_allowed("OWNER", "ressources_humaines") is True


def test_get_allowed_domains_unknown_role_returns_empty():
    assert get_allowed_domains("UNKNOWN_ROLE") == []


def test_filter_by_role_access_splits_allowed_and_blocked():
    items = [_item("a", "cpl"), _item("b", "ressources_humaines")]
    allowed, blocked = filter_by_role_access(items, "CHEF_DE_PROJET")
    assert [i.knowledge_id for i in allowed] == ["a"]
    assert [i.knowledge_id for i in blocked] == ["b"]


def test_filter_by_role_access_unrestricted_for_system_role():
    items = [_item("a", "cpl"), _item("b", "ressources_humaines")]
    allowed, blocked = filter_by_role_access(items, "OWNER")
    assert len(allowed) == 2
    assert blocked == []


def test_filter_by_role_access_empty_role_unrestricted():
    items = [_item("a", "cpl")]
    allowed, blocked = filter_by_role_access(items, "")
    assert len(allowed) == 1
