"""
════════════════════════════════════════════════════════════
PROJECT      : ALFRED
BLOCK        : B10
FUNCTION     : 10.TEST
FILE         : tests/security_tests/test_human_validation.py
ROLE         : Tests unitaires — human_validation.py

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-07-11
VERSION      : V1.0
STATUS       : ACTIVE

DESCRIPTION :
Couvre : submit_for_review, approve_request, reject_request, list_pending,
list_all, summarize_approvals. Isolation garantie par le fixture autouse
isolate_security_state_files (tests/conftest.py) — n'écrit jamais dans
data/security/pending_approvals.json réel.
════════════════════════════════════════════════════════════
"""
from src.security import human_validation as hv


def test_submit_for_review_creates_pending_entry():
    entry = hv.submit_for_review(
        user_id="u1", role="CHEF_DE_PROJET", action="GENERATE_DELIVERABLE",
        resource="deliverable:fiche_cadrage:test",
    )
    assert entry["status"] == "pending"
    assert entry["approval_id"]
    assert entry in hv.list_pending()


def test_submit_for_review_preserves_payload():
    entry = hv.submit_for_review(
        user_id="u1", role="RH", action="GENERATE_DELIVERABLE",
        resource="deliverable:x", payload={"draft": "contenu brouillon"},
    )
    assert entry["payload"] == {"draft": "contenu brouillon"}


def test_list_pending_filters_by_role():
    hv.submit_for_review(user_id="u1", role="CHEF_DE_PROJET", action="A", resource="r1")
    hv.submit_for_review(user_id="u2", role="RH", action="A", resource="r2")
    assert len(hv.list_pending(role="CHEF_DE_PROJET")) == 1
    assert len(hv.list_pending(role="RH")) == 1
    assert len(hv.list_pending()) == 2


def test_approve_request_updates_status():
    entry = hv.submit_for_review(user_id="u1", role="CHEF_DE_PROJET", action="A", resource="r1")
    approved = hv.approve_request(entry["approval_id"], approved_by="owner", note="ok")
    assert approved["status"] == "approved"
    assert approved["decided_by"] == "owner"
    assert approved["decision_note"] == "ok"
    assert approved["decided_at"] is not None
    assert hv.list_pending() == []


def test_reject_request_updates_status():
    entry = hv.submit_for_review(user_id="u1", role="RH", action="A", resource="r1")
    rejected = hv.reject_request(entry["approval_id"], rejected_by="owner", note="non conforme")
    assert rejected["status"] == "rejected"
    assert rejected["decision_note"] == "non conforme"


def test_decide_on_unknown_id_returns_none():
    assert hv.approve_request("id-inexistant", approved_by="owner") is None
    assert hv.reject_request("id-inexistant", rejected_by="owner") is None


def test_decide_is_idempotent_does_not_overwrite():
    entry = hv.submit_for_review(user_id="u1", role="CHEF_DE_PROJET", action="A", resource="r1")
    first = hv.approve_request(entry["approval_id"], approved_by="owner", note="premiere decision")
    second = hv.reject_request(entry["approval_id"], rejected_by="autre", note="tentative rejet")
    # La deuxième décision ne doit pas écraser la première.
    assert second["status"] == "approved"
    assert second["decision_note"] == "premiere decision"


def test_get_request_returns_entry():
    entry = hv.submit_for_review(user_id="u1", role="RH", action="A", resource="r1")
    fetched = hv.get_request(entry["approval_id"])
    assert fetched["approval_id"] == entry["approval_id"]


def test_get_request_unknown_returns_none():
    assert hv.get_request("id-inexistant") is None


def test_summarize_approvals_counts_by_status():
    e1 = hv.submit_for_review(user_id="u1", role="CHEF_DE_PROJET", action="A", resource="r1")
    e2 = hv.submit_for_review(user_id="u2", role="RH", action="A", resource="r2")
    hv.submit_for_review(user_id="u3", role="RH", action="A", resource="r3")
    hv.approve_request(e1["approval_id"], approved_by="owner")
    hv.reject_request(e2["approval_id"], rejected_by="owner")

    summary = hv.summarize_approvals()
    assert summary["total"] == 3
    assert summary["by_status"]["approved"] == 1
    assert summary["by_status"]["rejected"] == 1
    assert summary["by_status"]["pending"] == 1
