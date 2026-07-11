"""
════════════════════════════════════════════════════════════
PROJECT      : ALFRED
BLOCK        : B10
FUNCTION     : 10.TEST
FILE         : tests/b10_tests/test_deliverable_templates.py
ROLE         : Tests unitaires — deliverable_templates.py

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-07-11
VERSION      : V1.0
STATUS       : ACTIVE

DESCRIPTION :
Couvre : render_fiche_cadrage, render_registre_risques, render_deliverable
(gabarits de livrables métier assemblés à partir de connaissances retrouvées).
════════════════════════════════════════════════════════════
"""
from dataclasses import dataclass, field
from typing import Any

import pytest

from src.assistant_actions.deliverable_templates import (
    render_fiche_cadrage,
    render_registre_risques,
    render_deliverable,
    TEMPLATE_TYPES,
)


@dataclass
class _FakeRankedKnowledge:
    knowledge_id: str
    data: dict[str, Any] = field(default_factory=dict)


def _pmo07_like_item() -> _FakeRankedKnowledge:
    return _FakeRankedKnowledge(
        knowledge_id="cpl.demo_scenario.pmo07_project_launch_procedure_v3_2",
        data={"data": {"knowledge": {
            "process_steps": ["Cadrage", "Validation", "Exécution"],
            "cadrage_requirements": ["Objectifs", "Parties prenantes", "Registre des risques"],
        }}},
    )


def _risk_management_item() -> _FakeRankedKnowledge:
    return _FakeRankedKnowledge(
        knowledge_id="cpl.execution.risk_management",
        data={"data": {"knowledge": {
            "risk_categories": ["Risques techniques", "Risques calendaires"],
            "response_strategies": [
                {"strategy": "Réduction", "logic": "Réduire probabilité ou impact"},
            ],
        }}},
    )


def _citation() -> dict[str, Any]:
    return {
        "reference": "PMO-07", "version": "3.2", "validated_date": "2026-06-12",
        "owner": "PMO / Direction de programme",
    }


# ─── render_fiche_cadrage ──────────────────────────────────────────────────────

def test_fiche_cadrage_is_marked_draft():
    result = render_fiche_cadrage("lancement projet test", [_pmo07_like_item()], [_citation()])
    assert result["status"] == "draft"
    assert result["deliverable_type"] == "fiche_cadrage"
    assert "BROUILLON" in result["content_markdown"]


def test_fiche_cadrage_uses_cadrage_requirements_when_present():
    result = render_fiche_cadrage("lancement projet test", [_pmo07_like_item()], [_citation()])
    assert "Parties prenantes" in result["content_markdown"]
    assert "Registre des risques" in result["content_markdown"]


def test_fiche_cadrage_falls_back_to_default_sections_when_absent():
    result = render_fiche_cadrage("sujet sans connaissance associee", [], [])
    assert "Objectifs et bénéfices attendus" in result["content_markdown"]


def test_fiche_cadrage_includes_risk_categories():
    result = render_fiche_cadrage(
        "lancement projet test", [_pmo07_like_item(), _risk_management_item()], [_citation()]
    )
    assert "Risques techniques" in result["content_markdown"]


def test_fiche_cadrage_cites_sources():
    result = render_fiche_cadrage("sujet", [_pmo07_like_item()], [_citation()])
    assert "PMO-07" in result["content_markdown"]
    assert "3.2" in result["content_markdown"]


def test_fiche_cadrage_flags_missing_sources():
    result = render_fiche_cadrage("sujet", [], [])
    assert "Aucune source documentaire" in result["content_markdown"]


def test_fiche_cadrage_records_knowledge_ids_used():
    item = _pmo07_like_item()
    result = render_fiche_cadrage("sujet", [item], [])
    assert result["knowledge_ids_used"] == [item.knowledge_id]


# ─── render_registre_risques ───────────────────────────────────────────────────

def test_registre_risques_is_marked_draft():
    result = render_registre_risques("projet test", [_risk_management_item()], [])
    assert result["status"] == "draft"
    assert result["deliverable_type"] == "registre_risques"


def test_registre_risques_lists_categories_as_table_rows():
    result = render_registre_risques("projet test", [_risk_management_item()], [])
    assert "Risques techniques" in result["content_markdown"]
    assert "à évaluer" in result["content_markdown"]


def test_registre_risques_lists_response_strategies():
    result = render_registre_risques("projet test", [_risk_management_item()], [])
    assert "Réduction" in result["content_markdown"]


def test_registre_risques_fallback_without_categories():
    result = render_registre_risques("projet test", [], [])
    assert "à compléter manuellement" in result["content_markdown"]


# ─── render_deliverable (dispatch) ─────────────────────────────────────────────

def test_render_deliverable_dispatches_fiche_cadrage():
    result = render_deliverable("fiche_cadrage", "sujet", [], [])
    assert result["deliverable_type"] == "fiche_cadrage"


def test_render_deliverable_dispatches_registre_risques():
    result = render_deliverable("registre_risques", "sujet", [], [])
    assert result["deliverable_type"] == "registre_risques"


def test_render_deliverable_unknown_type_raises():
    with pytest.raises(ValueError):
        render_deliverable("type_inexistant", "sujet", [], [])


def test_template_types_has_two_entries():
    assert set(TEMPLATE_TYPES) == {"fiche_cadrage", "registre_risques"}
