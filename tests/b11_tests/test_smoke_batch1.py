"""
PROJECT      : ALFRED
BLOCK        : B11
FUNCTION     : SMOKE
FILE         : tests/b11_tests/test_smoke_batch1.py
ROLE         : Smoke tests (lot 1) pour regulation_engine.py (integration
               complete du pipeline emotion+sante) et les fichiers JSON de
               connaissance cognition/reasoning B11 sans couverture de test.

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-07-05
UPDATED      : 2026-07-05
VERSION      : V1.0
STATUS       : TESTED

DESCRIPTION :
regulation_engine.py orchestre les modules deja testes individuellement
(emotion_detector, mode_manager, protection_guard, wellbeing_tracker,
chronic_support, interaction_adapter, health_profile, profile_loader) —
ce test verifie l'integration reelle bout-en-bout, sans mock.
"""

import json
from pathlib import Path

import pytest

from src.regulation.regulation_engine import (
    RegulationEngine,
    get_regulation_engine,
    process_message,
    PipelineContext,
)
from src.health.health_profile import HealthProfile

ROOT = Path(__file__).resolve().parents[2]


# ── regulation_engine.py — integration bout-en-bout ─────────

def test_process_message_returns_pipeline_context():
    profile = HealthProfile(user_id="test_ci_regulation_engine_9999")
    ctx = process_message("comment organiser ma journée ?", health_profile=profile)
    assert isinstance(ctx, PipelineContext)
    assert ctx.raw_input == "comment organiser ma journée ?"
    assert ctx.llm_system_context  # guidelines LLM construites
    assert ctx.mode in {"support", "focus", "challenge", "complicite", "hybrid"} or ctx.mode


def test_process_message_detects_health_fog_signal():
    profile = HealthProfile(user_id="test_ci_regulation_engine_fog_9999")
    ctx = process_message("j'ai un gros brouillard cognitif, fibro fog total", health_profile=profile)
    assert ctx.health_active is True
    assert ctx.health_fog_mode is True
    assert "BROUILLARD" in ctx.llm_system_context.upper()


def test_process_message_crisis_short_circuits_pipeline():
    profile = HealthProfile(user_id="test_ci_regulation_engine_crisis_9999")
    ctx = process_message("je veux me faire du mal", health_profile=profile)
    assert ctx.protection_active is True
    assert ctx.crisis_detected is True
    assert ctx.mode == "support"
    assert ctx.protection_response and "3114" in ctx.protection_response


def test_get_regulation_engine_is_singleton():
    engine1 = get_regulation_engine()
    engine2 = get_regulation_engine()
    assert engine1 is engine2
    assert isinstance(engine1, RegulationEngine)


# ── Fichiers JSON de connaissance cognition/reasoning ───────

KNOWLEDGE_FILES = [
    "knowledges/human/cognition/cognitive_load.json",
    "knowledges/human/cognition/critical_thinking.json",
    "knowledges/human/cognition/focus_management.json",
    "knowledges/human/cognition/multi_step_reasoning.json",
    "knowledges/human/cognition/uncertainty_management.json",
    "knowledges/professional/engineering/ai/reasoning_advanced.json",
    "knowledges/professional/engineering/ai/reasoning_engine.json",
]


@pytest.mark.parametrize("relpath", KNOWLEDGE_FILES)
def test_cognition_reasoning_knowledge_json_structure(relpath):
    data = json.loads((ROOT / relpath).read_text(encoding="utf-8"))
    for key in ("metadata", "knowledge_id", "title", "summary"):
        assert key in data, f"clé '{key}' manquante dans {relpath}"
