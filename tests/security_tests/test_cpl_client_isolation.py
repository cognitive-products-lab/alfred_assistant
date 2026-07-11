"""
════════════════════════════════════════════════════════════
PROJECT      : ALFRED
BLOCK        : B10
FUNCTION     : 10.TEST
FILE         : tests/security_tests/test_cpl_client_isolation.py
ROLE         : Tests unitaires — cpl_client_isolation.py

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-07-11
VERSION      : V1.0
STATUS       : ACTIVE

DESCRIPTION :
Couvre : is_known_client, is_client_scope_allowed, filter_by_client_access
(isolation stricte des bases de connaissances entre entreprises clientes).
════════════════════════════════════════════════════════════
"""
from dataclasses import dataclass, field
from typing import Any

from src.security.cpl_client_isolation import (
    is_known_client,
    is_client_scope_allowed,
    filter_by_client_access,
)


@dataclass
class _FakeRankedKnowledge:
    knowledge_id: str
    data: dict[str, Any] = field(default_factory=dict)


def _item(knowledge_id: str, client_scope: str | None) -> _FakeRankedKnowledge:
    raw: dict[str, Any] = {}
    if client_scope is not None:
        raw["client_scope"] = client_scope
    return _FakeRankedKnowledge(knowledge_id=knowledge_id, data={"data": raw})


def test_known_demo_clients_recognized():
    assert is_known_client("nova_ingenierie") is True
    assert is_known_client("atlas_conseil") is True


def test_unknown_client_not_recognized():
    assert is_known_client("client_inexistant") is False
    assert is_known_client("") is False


def test_transversal_knowledge_always_allowed():
    assert is_client_scope_allowed("nova_ingenierie", None) is True
    assert is_client_scope_allowed("", None) is True
    assert is_client_scope_allowed("atlas_conseil", "") is True


def test_client_scoped_knowledge_allowed_for_matching_client():
    assert is_client_scope_allowed("nova_ingenierie", "nova_ingenierie") is True


def test_client_scoped_knowledge_denied_for_other_client():
    assert is_client_scope_allowed("atlas_conseil", "nova_ingenierie") is False


def test_client_scoped_knowledge_denied_without_client_context():
    assert is_client_scope_allowed("", "nova_ingenierie") is False


def test_filter_by_client_access_isolates_between_two_clients():
    items = [
        _item("nova_doc", "nova_ingenierie"),
        _item("atlas_doc", "atlas_conseil"),
        _item("transversal_doc", None),
    ]

    allowed_nova, blocked_nova = filter_by_client_access(items, "nova_ingenierie")
    assert {i.knowledge_id for i in allowed_nova} == {"nova_doc", "transversal_doc"}
    assert {i.knowledge_id for i in blocked_nova} == {"atlas_doc"}

    allowed_atlas, blocked_atlas = filter_by_client_access(items, "atlas_conseil")
    assert {i.knowledge_id for i in allowed_atlas} == {"atlas_doc", "transversal_doc"}
    assert {i.knowledge_id for i in blocked_atlas} == {"nova_doc"}


def test_filter_by_client_access_without_client_id_only_transversal():
    items = [_item("nova_doc", "nova_ingenierie"), _item("transversal_doc", None)]
    allowed, blocked = filter_by_client_access(items, "")
    assert [i.knowledge_id for i in allowed] == ["transversal_doc"]
    assert [i.knowledge_id for i in blocked] == ["nova_doc"]
