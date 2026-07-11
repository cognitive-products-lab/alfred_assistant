"""
════════════════════════════════════════════════════════════
PROJECT      : ALFRED
BLOCK        : B10
FUNCTION     : 10.TEST
FILE         : tests/b10_tests/test_deliverable_generator.py
ROLE         : Tests unitaires — deliverable_generator.py

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-07-11
VERSION      : V1.0
STATUS       : ACTIVE

DESCRIPTION :
Couvre le pipeline complet : retrieval (filtré rôle + client) -> gabarit ->
mise en file de validation humaine (GENERATE_DELIVERABLE est toujours REVIEW).
Isolation piste d'audit / file d'approbation garantie par
tests/conftest.py (isolate_security_state_files).
════════════════════════════════════════════════════════════
"""
import pytest

from src.assistant_actions.deliverable_generator import generate_deliverable
from src.security.session_manager import create_session
from src.security.mfa_manager import mark_verified
from src.security import human_validation as hv


def _authenticated_session(user_id: str, role: str) -> str:
    session_id = create_session(user_id=user_id, device_id="local_pc", role=role)
    mark_verified(user_id, session_id)
    return session_id


def test_generate_deliverable_returns_review_pending():
    session_id = _authenticated_session("t_cdp", "CHEF_DE_PROJET")
    result = generate_deliverable(
        deliverable_type="fiche_cadrage",
        topic="lancement d'un projet d'assistant IA pour le service client",
        user_id="t_cdp", role="CHEF_DE_PROJET",
        device_id="local_pc", session_id=session_id,
        client_id="nova_ingenierie", request_id="test-req-1",
    )
    assert result["decision"] == "REVIEW"
    assert result["pending"] is True
    assert result["approval_id"]
    assert result["deliverable"]["status"] == "draft"


def test_generated_deliverable_can_be_approved():
    session_id = _authenticated_session("t_cdp2", "CHEF_DE_PROJET")
    result = generate_deliverable(
        deliverable_type="fiche_cadrage",
        topic="lancement d'un projet interne",
        user_id="t_cdp2", role="CHEF_DE_PROJET",
        device_id="local_pc", session_id=session_id,
        client_id="nova_ingenierie",
    )
    approved = hv.approve_request(result["approval_id"], approved_by="owner_test", note="ok")
    assert approved["status"] == "approved"
    # Le brouillon complet doit être préservé dans le payload de la demande approuvée.
    assert approved["payload"]["deliverable_type"] == "fiche_cadrage"


def test_generate_deliverable_respects_client_isolation():
    """Un livrable généré pour Atlas Conseil ne doit jamais citer PMO-07 (Nova)."""
    session_id = _authenticated_session("t_cdp3", "CHEF_DE_PROJET")
    result = generate_deliverable(
        deliverable_type="fiche_cadrage",
        topic="lancement d'un nouveau projet",
        user_id="t_cdp3", role="CHEF_DE_PROJET",
        device_id="local_pc", session_id=session_id,
        client_id="atlas_conseil",
    )
    knowledge_ids = result["deliverable"]["knowledge_ids_used"]
    assert "cpl.demo_scenario.pmo07_project_launch_procedure_v3_2" not in knowledge_ids


def test_generate_deliverable_unknown_type_raises():
    session_id = _authenticated_session("t_cdp4", "CHEF_DE_PROJET")
    with pytest.raises(ValueError):
        generate_deliverable(
            deliverable_type="type_inexistant",
            topic="sujet",
            user_id="t_cdp4", role="CHEF_DE_PROJET",
            device_id="local_pc", session_id=session_id,
        )


def test_generate_deliverable_registre_risques():
    session_id = _authenticated_session("t_rh1", "RH")
    result = generate_deliverable(
        deliverable_type="registre_risques",
        topic="risques liés au recrutement",
        user_id="t_rh1", role="RH",
        device_id="local_pc", session_id=session_id,
    )
    assert result["decision"] == "REVIEW"
    assert result["deliverable"]["deliverable_type"] == "registre_risques"
