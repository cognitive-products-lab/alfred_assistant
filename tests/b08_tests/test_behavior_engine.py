"""
════════════════════════════════════════════════════════════
PROJECT      : ALFRED
BLOCK        : B08
FUNCTION     : 08.TEST
FILE         : tests/b08_tests/test_behavior_engine.py
ROLE         : Tests unitaires — AlfredBehaviorEngine

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-05-23
UPDATED      : 2026-05-23
VERSION      : V1.0
STATUS       : TESTED

DESCRIPTION :
Tests B08 — AlfredBehaviorEngine : validation du moteur de comportement,
décisions comportementales, correspondances softskills, états utilisateur.
════════════════════════════════════════════════════════════
"""

import json
import shutil
import tempfile
from pathlib import Path

import pytest

from src.core.alfred_behavior_engine import (
    AlfredBehaviorEngine,
    BehaviorDecision,
    SoftSkillMatch,
    UserState,
)


# ============================================================
# Fixtures JSON minimales
# ============================================================

IDENTITY_JSON = {
    "core_concept": {
        "formula": "Intelligence + Empathie + Structure = ALFRED"
    },
    "core_principles": [
        "respecter l'utilisateur",
        "structurer sans diriger",
        "agir avec discernement"
    ],
    "fusion_rules": [
        "intelligence + humain d'abord",
        "jamais de manipulation"
    ],
    "behavioral_modes": {
        "support_mode": {
            "dominant_layer": "emotional",
            "response_structure": ["reconnaitre", "rassurer", "proposer"]
        },
        "execution_mode": {
            "dominant_layer": "analytical",
            "response_structure": ["objectif", "solution", "action"]
        },
        "learning_mode": {
            "dominant_layer": "pedagogical",
            "response_structure": ["definition", "exemple", "resume"]
        },
        "hybrid_mode": {
            "dominant_layer": "balanced",
            "response_structure": ["contexte", "objectif", "solution"]
        },
        "ethics_mode": {
            "dominant_layer": "ethical",
            "response_structure": ["risque", "limite", "alternative"]
        }
    },
    "tone_guidelines": {
        "baseline": "clair, structure, humain",
        "variations": {
            "fatigue": "lent, simple, rassurant",
            "stress": "pose, structurant",
            "action": "direct, efficace",
            "apprentissage": "pedagogique, detaille",
            "ethics": "prudent, responsable"
        }
    },
    "anti_patterns": ["eviter la sur-sollicitation"],
    "relationship_with_user": {
        "boundaries": [
            "respecter la vie privee",
            "preserver l'autonomie"
        ]
    }
}

SOFTSKILLS_JSON = {
    "global_policy": {
        "max_actions_injected": 5
    },
    "softskill_rules": [
        {
            "id": "softskill_emotional_support",
            "name": "Soutien emotionnel",
            "priority": 10,
            "detected_need": "soutien face a la detresse",
            "triggers": ["fatiguee", "epuisee", "j'en peux plus", "debordee"],
            "actions": ["reconnaitre l'etat", "rassurer"],
            "response_style": "calme, rassurant",
            "avoid": ["minimiser", "donner des conseils immediats"]
        },
        {
            "id": "softskill_problem_solving",
            "name": "Resolution de probleme",
            "priority": 7,
            "detected_need": "aide pour resoudre un probleme",
            "triggers": ["comment faire", "je bloque", "probleme", "aide"],
            "actions": ["clarifier le probleme", "proposer des etapes"],
            "response_style": "direct, structure",
            "avoid": ["sur-complique"]
        },
        {
            "id": "softskill_decision_support",
            "name": "Aide a la decision",
            "priority": 8,
            "detected_need": "aide pour decider",
            "triggers": ["je ne sais pas quoi choisir", "decision", "choix"],
            "actions": ["poser le cadre", "presenter les options"],
            "response_style": "neutre, structure",
            "avoid": ["decider a la place"]
        }
    ],
    "combination_rules": [
        {
            "id": "combo_support_decision",
            "if_rules_match": [
                "softskill_emotional_support",
                "softskill_decision_support"
            ],
            "priority_boost": 5,
            "combined_behavior": ["rassurer avant de proposer des options"]
        }
    ]
}


# ============================================================
# Helpers
# ============================================================

def _write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def _make_engine(tmp: str, with_softskills: bool = True) -> AlfredBehaviorEngine:
    identity_path = Path(tmp) / "alfred_core_identity.json"
    _write_json(identity_path, IDENTITY_JSON)

    if with_softskills:
        ss_path = Path(tmp) / "softskills.json"
        _write_json(ss_path, SOFTSKILLS_JSON)
        return AlfredBehaviorEngine(str(identity_path), str(ss_path))

    return AlfredBehaviorEngine(str(identity_path))


# ============================================================
# Class TestAlfredBehaviorEngineInit
# ============================================================

class TestAlfredBehaviorEngineInit:
    """Tests initialisation du moteur."""

    def test_init_with_identity_only(self):
        tmp = tempfile.mkdtemp()
        try:
            engine = _make_engine(tmp, with_softskills=False)
            assert engine is not None
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_init_with_softskills(self):
        tmp = tempfile.mkdtemp()
        try:
            engine = _make_engine(tmp, with_softskills=True)
            assert len(engine.softskills_rules) == 3
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_identity_loaded(self):
        tmp = tempfile.mkdtemp()
        try:
            engine = _make_engine(tmp)
            assert engine.identity["core_concept"]["formula"] is not None
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_missing_identity_raises(self):
        with pytest.raises(FileNotFoundError):
            AlfredBehaviorEngine("/nonexistent/path/identity.json")

    def test_softskills_optional(self):
        tmp = tempfile.mkdtemp()
        try:
            engine = _make_engine(tmp, with_softskills=False)
            assert engine.softskills_rules == []
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_combination_rules_loaded(self):
        tmp = tempfile.mkdtemp()
        try:
            engine = _make_engine(tmp)
            assert len(engine.combination_rules) == 1
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


# ============================================================
# Class TestUserState
# ============================================================

class TestUserState:
    """Tests le dataclass UserState."""

    def test_default_state(self):
        state = UserState()
        assert state.emotion == "neutral"
        assert state.intensity == 0.0
        assert state.intent == "general_discussion"
        assert state.fatigue_level is None
        assert state.stress_level is None

    def test_custom_state(self):
        state = UserState(
            emotion="stress",
            intensity=0.8,
            intent="planning",
            fatigue_level=0.6,
            stress_level=0.7
        )
        assert state.emotion == "stress"
        assert state.intensity == 0.8

    def test_context_field(self):
        state = UserState(context={"session": "morning"})
        assert state.context["session"] == "morning"


# ============================================================
# Class TestSelectMode
# ============================================================

class TestSelectMode:
    """Tests selection du mode comportemental."""

    def setup_method(self):
        self.tmp = tempfile.mkdtemp()
        self.engine = _make_engine(self.tmp, with_softskills=False)

    def teardown_method(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_ethics_intent_returns_ethics_mode(self):
        state = UserState(intent="ethics")
        mode = self.engine._select_mode(state)
        assert mode == "ethics_mode"

    def test_emotional_signal_high_intensity_returns_support_mode(self):
        state = UserState(emotion="stress", intensity=0.8)
        mode = self.engine._select_mode(state)
        assert mode == "support_mode"

    def test_high_fatigue_returns_support_mode(self):
        state = UserState(fatigue_level=0.9)
        mode = self.engine._select_mode(state)
        assert mode == "support_mode"

    def test_high_stress_level_returns_support_mode(self):
        state = UserState(stress_level=0.8)
        mode = self.engine._select_mode(state)
        assert mode == "support_mode"

    def test_learning_intent_returns_learning_mode(self):
        state = UserState(intent="learning", intensity=0.0)
        mode = self.engine._select_mode(state)
        assert mode == "learning_mode"

    def test_task_intent_low_intensity_returns_execution_mode(self):
        state = UserState(intent="task", intensity=0.0)
        mode = self.engine._select_mode(state)
        assert mode == "execution_mode"

    def test_task_intent_high_intensity_returns_hybrid_mode(self):
        state = UserState(intent="task", intensity=0.7)
        mode = self.engine._select_mode(state)
        assert mode == "hybrid_mode"

    def test_default_fallback_returns_hybrid_mode(self):
        state = UserState(emotion="neutral", intensity=0.0, intent="general_discussion")
        mode = self.engine._select_mode(state)
        assert mode == "hybrid_mode"

    def test_low_intensity_emotion_neutral_execution(self):
        state = UserState(emotion="neutral", intent="coding", intensity=0.1)
        mode = self.engine._select_mode(state)
        assert mode == "execution_mode"


# ============================================================
# Class TestApplySoftskills
# ============================================================

class TestApplySoftskills:
    """Tests application des soft skills."""

    def setup_method(self):
        self.tmp = tempfile.mkdtemp()
        self.engine = _make_engine(self.tmp, with_softskills=True)

    def teardown_method(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_no_message_returns_empty(self):
        result = self.engine.apply_softskills("")
        assert result == []

    def test_no_softskills_config_returns_empty(self):
        engine_no_ss = _make_engine(self.tmp, with_softskills=False)
        result = engine_no_ss.apply_softskills("fatiguee et debordee")
        assert result == []

    def test_emotional_trigger_detected(self):
        result = self.engine.apply_softskills("je suis fatiguee et debordee")
        rule_ids = [m.rule_id for m in result]
        assert "softskill_emotional_support" in rule_ids

    def test_problem_trigger_detected(self):
        result = self.engine.apply_softskills("j'ai un probleme comment faire")
        rule_ids = [m.rule_id for m in result]
        assert "softskill_problem_solving" in rule_ids

    def test_decision_trigger_detected(self):
        result = self.engine.apply_softskills("je dois faire un choix difficile")
        rule_ids = [m.rule_id for m in result]
        assert "softskill_decision_support" in rule_ids

    def test_softskill_match_structure(self):
        result = self.engine.apply_softskills("fatiguee")
        assert len(result) > 0
        match = result[0]
        assert isinstance(match, SoftSkillMatch)
        assert match.rule_id != ""
        assert match.name != ""
        assert isinstance(match.actions, list)

    def test_sorted_by_priority_descending(self):
        result = self.engine.apply_softskills("fatiguee et probleme et choix")
        if len(result) >= 2:
            assert result[0].priority >= result[1].priority

    def test_max_actions_respected(self):
        result = self.engine.apply_softskills("fatiguee debordee probleme choix")
        assert len(result) <= 5

    def test_combination_boost_applied(self):
        # Both emotional_support and decision triggers
        result = self.engine.apply_softskills("fatiguee et je dois faire un choix decision")
        # After combo boost, emotional_support priority should be higher
        if len(result) >= 2:
            emotional_matches = [m for m in result if m.rule_id == "softskill_emotional_support"]
            if emotional_matches:
                assert emotional_matches[0].priority >= 15  # 10 base + 5 boost


# ============================================================
# Class TestSoftskillModeOverride
# ============================================================

class TestSoftskillModeOverride:
    """Tests override du mode par les soft skills."""

    def setup_method(self):
        self.tmp = tempfile.mkdtemp()
        self.engine = _make_engine(self.tmp, with_softskills=True)

    def teardown_method(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_emotional_support_overrides_to_support_mode(self):
        skills = [SoftSkillMatch(
            rule_id="softskill_emotional_support",
            name="test", priority=10, detected_need="test",
            actions=[], response_style="test", avoid=[]
        )]
        result = self.engine._apply_softskill_mode_override("execution_mode", skills)
        assert result == "support_mode"

    def test_problem_solving_overrides_to_execution(self):
        skills = [SoftSkillMatch(
            rule_id="softskill_problem_solving",
            name="test", priority=7, detected_need="test",
            actions=[], response_style="test", avoid=[]
        )]
        result = self.engine._apply_softskill_mode_override("hybrid_mode", skills)
        assert result == "execution_mode"

    def test_decision_support_overrides_to_hybrid(self):
        skills = [SoftSkillMatch(
            rule_id="softskill_decision_support",
            name="test", priority=8, detected_need="test",
            actions=[], response_style="test", avoid=[]
        )]
        result = self.engine._apply_softskill_mode_override("support_mode", skills)
        assert result == "hybrid_mode"

    def test_no_softskills_keeps_mode(self):
        result = self.engine._apply_softskill_mode_override("learning_mode", [])
        assert result == "learning_mode"


# ============================================================
# Class TestDecideBehavior
# ============================================================

class TestDecideBehavior:
    """Tests decide_behavior -- integration complete."""

    def setup_method(self):
        self.tmp = tempfile.mkdtemp()
        self.engine = _make_engine(self.tmp, with_softskills=True)

    def teardown_method(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_returns_behavior_decision(self):
        state = UserState(emotion="neutral", intensity=0.0, intent="general_discussion")
        decision = self.engine.decide_behavior(state)
        assert isinstance(decision, BehaviorDecision)

    def test_decision_has_mode(self):
        state = UserState()
        decision = self.engine.decide_behavior(state)
        assert isinstance(decision.mode, str)
        assert decision.mode != ""

    def test_decision_has_tone(self):
        state = UserState()
        decision = self.engine.decide_behavior(state)
        assert isinstance(decision.tone, str)

    def test_decision_has_safety_rules(self):
        state = UserState()
        decision = self.engine.decide_behavior(state)
        assert isinstance(decision.safety_rules, list)
        assert len(decision.safety_rules) > 0

    def test_decision_has_response_structure(self):
        state = UserState()
        decision = self.engine.decide_behavior(state)
        assert isinstance(decision.response_structure, list)
        assert len(decision.response_structure) > 0

    def test_high_stress_leads_to_support_mode(self):
        state = UserState(emotion="stress", intensity=0.9, stress_level=0.9)
        decision = self.engine.decide_behavior(state)
        assert decision.mode == "support_mode"

    def test_learning_intent_leads_to_learning_mode(self):
        state = UserState(intent="learning")
        decision = self.engine.decide_behavior(state, user_message="explain python")
        assert decision.mode == "learning_mode"

    def test_metadata_has_emotion(self):
        state = UserState(emotion="joy", intensity=0.5)
        decision = self.engine.decide_behavior(state)
        assert decision.metadata["emotion"] == "joy"

    def test_fatigue_message_triggers_softskill(self):
        state = UserState(emotion="neutral", intensity=0.0)
        decision = self.engine.decide_behavior(state, user_message="je suis fatiguee")
        # Should override to support_mode via softskill
        assert decision.mode == "support_mode"

    def test_guidance_contains_core_formula(self):
        state = UserState()
        decision = self.engine.decide_behavior(state)
        assert decision.guidance["core_formula"] is not None
        assert "ALFRED" in decision.guidance["core_formula"]

    def test_decision_softskills_list(self):
        state = UserState()
        decision = self.engine.decide_behavior(state, user_message="")
        assert isinstance(decision.softskills, list)

    def test_ethics_intent_mode(self):
        state = UserState(intent="risk")
        decision = self.engine.decide_behavior(state)
        assert decision.mode == "ethics_mode"


# ============================================================
# Class TestBuildPromptContext
# ============================================================

class TestBuildPromptContext:
    """Tests construction du contexte prompt."""

    def setup_method(self):
        self.tmp = tempfile.mkdtemp()
        self.engine = _make_engine(self.tmp, with_softskills=True)

    def teardown_method(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_returns_string(self):
        state = UserState()
        decision = self.engine.decide_behavior(state)
        prompt = self.engine.build_prompt_context(decision)
        assert isinstance(prompt, str)
        assert len(prompt) > 0

    def test_contains_mode(self):
        state = UserState(intent="learning")
        decision = self.engine.decide_behavior(state)
        prompt = self.engine.build_prompt_context(decision)
        assert decision.mode in prompt

    def test_contains_tone(self):
        state = UserState()
        decision = self.engine.decide_behavior(state)
        prompt = self.engine.build_prompt_context(decision)
        assert decision.tone in prompt

    def test_contains_safety_rules(self):
        state = UserState()
        decision = self.engine.decide_behavior(state)
        prompt = self.engine.build_prompt_context(decision)
        # At least one safety rule should appear
        assert any(rule in prompt for rule in decision.safety_rules)

    def test_contains_formula(self):
        state = UserState()
        decision = self.engine.decide_behavior(state)
        prompt = self.engine.build_prompt_context(decision)
        assert "ALFRED" in prompt

    def test_no_softskills_message(self):
        engine_no_ss = _make_engine(self.tmp, with_softskills=False)
        state = UserState()
        decision = engine_no_ss.decide_behavior(state)
        prompt = engine_no_ss.build_prompt_context(decision)
        assert "aucun" in prompt.lower() or "SOFT SKILLS" in prompt

    def test_softskills_block_when_triggered(self):
        state = UserState()
        decision = self.engine.decide_behavior(state, user_message="fatiguee")
        prompt = self.engine.build_prompt_context(decision)
        assert "SOFT SKILLS" in prompt


# ============================================================
# Class TestGetSafetyRules
# ============================================================

class TestGetSafetyRules:
    """Tests regles de securite."""

    def setup_method(self):
        self.tmp = tempfile.mkdtemp()
        self.engine = _make_engine(self.tmp)

    def teardown_method(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_safety_rules_include_defaults(self):
        rules = self.engine._get_safety_rules()
        assert "ne pas manipuler l'utilisateur" in rules
        assert "respecter la vie privee" in rules or "respecter la vie privée" in rules

    def test_safety_rules_no_duplicates(self):
        rules = self.engine._get_safety_rules()
        assert len(rules) == len(set(rules))

    def test_identity_boundaries_included(self):
        rules = self.engine._get_safety_rules()
        # From IDENTITY_JSON relationship_with_user.boundaries
        assert any("autonomie" in r for r in rules)
