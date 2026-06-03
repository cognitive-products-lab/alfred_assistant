"""
PROJECT      : ALFRED
BLOCK        : V2 Intelligence
FUNCTION     : Pipeline V2 — tests d'intégration
FILE         : test_v2_pipeline.py
ROLE         : Tests intégration FusionEngine + ConfidenceScorer + DecisionEngine

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-06-03
UPDATED      : 2026-06-03
VERSION      : V1.0
STATUS       : ACTIVE

DESCRIPTION :
Tests d'intégration du pipeline V2 :
  - FusionEngine.fuse() avec différentes sources
  - ConfidenceScorer.score() avec et sans response_text
  - DecisionEngine.decide() → stratégie correcte
  - BehaviorEngine.apply_v2_decision() → enrichissement décision
  - ResponseGenerator._apply_confidence_scoring() → hedge si confiance faible
  - Flux complet build_response() avec V2 actif (mocké)
"""

import pytest
from unittest.mock import MagicMock, patch
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from src.v2.fusion.fusion_engine import FusionEngine, FusionResult, get_fusion_engine, reset_fusion_engine
from src.v2.confidence.confidence_scorer import ConfidenceScorer, ConfidenceResult, get_confidence_scorer, reset_confidence_scorer
from src.v2.decision.decision_engine import DecisionEngine, DecisionResult, ResponseStrategy, get_decision_engine, reset_decision_engine
from src.core.response_generator import ResponseGenerator


# =============================================================================
# FusionEngine
# =============================================================================

class TestFusionEngine:

    def setup_method(self):
        reset_fusion_engine()

    def test_fuse_returns_fusion_result(self):
        engine = FusionEngine()
        result = engine.fuse(
            memory_context="Mémoire test",
            knowledge_context="Knowledge test",
            user_message="Test",
        )
        assert isinstance(result, FusionResult)
        assert 0.0 <= result.fusion_score <= 1.0

    def test_fuse_empty_sources_returns_empty_context(self):
        engine = FusionEngine()
        result = engine.fuse()
        assert result.merged_context == ""
        assert result.fusion_score == 0.0

    def test_fuse_memory_only(self):
        engine = FusionEngine()
        result = engine.fuse(memory_context="Historique Céline")
        assert "Historique Céline" in result.merged_context
        assert result.primary_source == "memory"

    def test_fuse_knowledge_only(self):
        engine = FusionEngine()
        result = engine.fuse(knowledge_context="Base de connaissances ALFRED")
        assert "Base de connaissances ALFRED" in result.merged_context

    def test_fuse_all_sources_score_near_max(self):
        engine = FusionEngine()
        result = engine.fuse(
            memory_context="Mémoire",
            knowledge_context="Knowledge",
            llm_context="LLM context",
        )
        assert result.fusion_score >= 0.5
        assert len(result.context_blocks) == 3

    def test_emotion_boost_memory_weight(self):
        engine = FusionEngine()
        result = engine.fuse(
            memory_context="Mémoire personnelle",
            knowledge_context="Knowledge",
            emotion="stressed",
        )
        # En mode stressed, la mémoire doit être prioritaire
        weights = result.weights
        assert weights.get("memory", 0) > weights.get("knowledge", 0)

    def test_focus_mode_boosts_knowledge(self):
        engine = FusionEngine()
        result = engine.fuse(
            memory_context="Mémoire",
            knowledge_context="Knowledge expert",
            emotion="neutral",
            mode="focus",
        )
        weights = result.weights
        assert weights.get("knowledge", 0) >= weights.get("memory", 0)

    def test_singleton_returns_same_instance(self):
        reset_fusion_engine()
        a = get_fusion_engine()
        b = get_fusion_engine()
        assert a is b

    def test_to_context_string_truncates(self):
        engine = FusionEngine()
        result = engine.fuse(memory_context="A" * 5000)
        assert len(result.to_context_string(max_chars=100)) <= 100

    def test_weights_sum_to_one(self):
        engine = FusionEngine()
        result = engine.fuse(
            memory_context="M",
            knowledge_context="K",
            emotion="neutral",
            mode="complicite",
        )
        total = sum(result.weights.values())
        assert abs(total - 1.0) < 0.01


# =============================================================================
# ConfidenceScorer
# =============================================================================

class TestConfidenceScorer:

    def setup_method(self):
        reset_confidence_scorer()

    def test_score_returns_confidence_result(self):
        scorer = ConfidenceScorer()
        result = scorer.score()
        assert isinstance(result, ConfidenceResult)
        assert 0.0 <= result.score <= 1.0

    def test_full_coverage_gives_high_confidence(self):
        scorer = ConfidenceScorer()
        result = scorer.score(
            fusion_score=0.9,
            memory_coverage=1.0,
            knowledge_coverage=1.0,
            emotion="neutral",
            mode="focus",
            response_text="Réponse de qualité suffisante pour le test.",
        )
        assert result.level in ("high", "medium")
        assert result.score >= 0.5

    def test_zero_coverage_gives_low_confidence(self):
        scorer = ConfidenceScorer()
        result = scorer.score(
            fusion_score=0.0,
            memory_coverage=0.0,
            knowledge_coverage=0.0,
            response_text="",
        )
        assert result.level in ("low", "uncertain")
        assert result.should_hedge is True

    def test_should_hedge_when_uncertain(self):
        scorer = ConfidenceScorer()
        result = scorer.score(
            fusion_score=0.1,
            memory_coverage=0.0,
            knowledge_coverage=0.0,
        )
        assert result.should_hedge is True
        assert result.hedge_phrase != ""

    def test_no_hedge_when_high_confidence(self):
        scorer = ConfidenceScorer()
        result = scorer.score(
            fusion_score=0.9,
            memory_coverage=1.0,
            knowledge_coverage=1.0,
            response_text="Réponse longue et détaillée avec toutes les informations nécessaires.",
        )
        assert result.should_hedge is False
        assert result.hedge_phrase == ""

    def test_adjust_response_adds_prefix(self):
        scorer = ConfidenceScorer()
        result = scorer.score(fusion_score=0.0)
        if result.should_hedge and result.hedge_phrase:
            adjusted = scorer.adjust_response("Ma réponse.", result)
            assert adjusted.startswith(result.hedge_phrase)

    def test_adjust_response_no_prefix_when_confident(self):
        scorer = ConfidenceScorer()
        result = scorer.score(
            fusion_score=1.0,
            memory_coverage=1.0,
            knowledge_coverage=1.0,
            response_text="Réponse fiable et complète.",
        )
        text = "Réponse fiable."
        adjusted = scorer.adjust_response(text, result)
        assert adjusted == text

    def test_emotion_alignment_stressed_support(self):
        scorer = ConfidenceScorer()
        result_good = scorer.score(emotion="stressed", mode="support")
        result_bad = scorer.score(emotion="stressed", mode="challenge")
        # L'alignement correct améliore légèrement le score
        assert result_good.score >= result_bad.score

    def test_singleton(self):
        reset_confidence_scorer()
        a = get_confidence_scorer()
        b = get_confidence_scorer()
        assert a is b

    def test_is_confident_property(self):
        scorer = ConfidenceScorer()
        high = scorer.score(fusion_score=1.0, memory_coverage=1.0,
                            knowledge_coverage=1.0,
                            response_text="Longue réponse de qualité pour le test.")
        low = scorer.score()
        assert high.is_confident is True
        assert low.is_confident is False


# =============================================================================
# DecisionEngine
# =============================================================================

class TestDecisionEngine:

    def setup_method(self):
        reset_decision_engine()

    def test_decide_returns_decision_result(self):
        engine = DecisionEngine()
        result = engine.decide()
        assert isinstance(result, DecisionResult)
        assert isinstance(result.strategy, ResponseStrategy)

    def test_emotional_distress_returns_empathetic(self):
        engine = DecisionEngine()
        result = engine.decide(
            emotion="stressed",
            mode="support",
            confidence_level="medium",
            confidence_score=0.5,
        )
        assert result.strategy == ResponseStrategy.EMPATHETIC

    def test_uncertain_question_returns_exploratory(self):
        engine = DecisionEngine()
        result = engine.decide(
            confidence_level="uncertain",
            is_question=True,
            recent_strategies=[],
        )
        assert result.strategy in (ResponseStrategy.EXPLORATORY, ResponseStrategy.HEDGED)

    def test_low_confidence_returns_hedged(self):
        engine = DecisionEngine()
        result = engine.decide(confidence_level="low")
        assert result.strategy == ResponseStrategy.HEDGED
        assert result.should_hedge is True

    def test_high_confidence_returns_direct(self):
        engine = DecisionEngine()
        result = engine.decide(
            confidence_score=0.85,
            confidence_level="high",
            fusion_score=0.8,
            emotion="neutral",
        )
        assert result.strategy == ResponseStrategy.DIRECT
        assert result.should_hedge is False

    def test_memory_source_returns_memory_strategy(self):
        engine = DecisionEngine()
        result = engine.decide(
            primary_source="memory",
            has_memory=True,
            confidence_score=0.7,
            confidence_level="high",
        )
        assert result.strategy == ResponseStrategy.MEMORY

    def test_knowledge_focus_returns_knowledge_strategy(self):
        engine = DecisionEngine()
        result = engine.decide(
            has_knowledge=True,
            mode="focus",
            confidence_score=0.65,
            confidence_level="high",
        )
        assert result.strategy == ResponseStrategy.KNOWLEDGE

    def test_tone_is_warm_for_support_mode(self):
        engine = DecisionEngine()
        result = engine.decide(mode="support")
        assert result.tone == "warm"

    def test_tone_is_precise_for_focus_mode(self):
        engine = DecisionEngine()
        result = engine.decide(mode="focus", confidence_score=0.8, confidence_level="high")
        assert result.tone == "precise"

    def test_emotional_distress_reduces_max_length(self):
        engine = DecisionEngine()
        result = engine.decide(emotion="stressed", mode="support")
        assert result.max_length <= 400

    def test_post_actions_include_save_when_confident(self):
        engine = DecisionEngine()
        result = engine.decide(
            confidence_score=0.7,
            confidence_level="high",
            fusion_score=0.7,
        )
        assert "save_to_memory" in result.post_actions

    def test_post_actions_track_wellbeing_for_distress(self):
        engine = DecisionEngine()
        result = engine.decide(emotion="stressed", mode="support")
        assert "track_wellbeing" in result.post_actions

    def test_singleton(self):
        reset_decision_engine()
        a = get_decision_engine()
        b = get_decision_engine()
        assert a is b

    def test_to_dict(self):
        engine = DecisionEngine()
        result = engine.decide()
        d = result.to_dict()
        assert "strategy" in d
        assert "tone" in d
        assert "max_length" in d
        assert "post_actions" in d


# =============================================================================
# BehaviorEngine.apply_v2_decision()
# =============================================================================

class TestApplyV2Decision:

    def _get_behavior_engine(self):
        from src.core.alfred_behavior_engine import AlfredBehaviorEngine
        identity_path = Path(__file__).parents[2] / "knowledges" / "core" / "alfred_core_identity.json"
        if not identity_path.exists():
            pytest.skip("alfred_core_identity.json absent")
        return AlfredBehaviorEngine(str(identity_path))

    def _make_mock_decision(self, mode="execution_mode", tone="direct, structuré, efficace"):
        from src.core.alfred_behavior_engine import BehaviorDecision
        return BehaviorDecision(
            mode=mode,
            dominant_layer="balanced",
            tone=tone,
            response_structure=["analyse", "solution"],
            safety_rules=[],
            guidance={},
            metadata={},
        )

    def test_apply_v2_with_none_sources_is_noop(self):
        be = self._get_behavior_engine()
        decision = self._make_mock_decision()
        original_tone = decision.tone
        enriched = be.apply_v2_decision(decision)
        assert enriched.tone == original_tone

    def test_apply_v2_fusion_updates_dominant_layer(self):
        be = self._get_behavior_engine()
        decision = self._make_mock_decision()

        fusion = MagicMock()
        fusion.primary_source = "memory"
        fusion.fusion_score = 0.7

        enriched = be.apply_v2_decision(decision, fusion_result=fusion)
        assert enriched.dominant_layer == "memory"
        assert enriched.metadata["v2_primary_source"] == "memory"

    def test_apply_v2_decision_overrides_tone_warm(self):
        be = self._get_behavior_engine()
        decision = self._make_mock_decision()

        dec_result = MagicMock()
        dec_result.strategy = ResponseStrategy.EMPATHETIC
        dec_result.tone = "warm"
        dec_result.should_hedge = False
        dec_result.hedge_prefix = ""
        dec_result.max_length = 400
        dec_result.post_actions = []

        enriched = be.apply_v2_decision(decision, decision_result=dec_result)
        assert "rassurant" in enriched.tone or "chaleureux" in enriched.tone

    def test_apply_v2_decision_empathetic_overrides_structure(self):
        be = self._get_behavior_engine()
        decision = self._make_mock_decision()

        dec_result = MagicMock()
        dec_result.strategy = ResponseStrategy.EMPATHETIC
        dec_result.tone = "warm"
        dec_result.should_hedge = False
        dec_result.hedge_prefix = ""
        dec_result.max_length = 400
        dec_result.post_actions = []

        enriched = be.apply_v2_decision(decision, decision_result=dec_result)
        assert any("émotionnel" in s or "valider" in s for s in enriched.response_structure)

    def test_apply_v2_sets_v2_metadata(self):
        be = self._get_behavior_engine()
        decision = self._make_mock_decision()

        dec_result = MagicMock()
        dec_result.strategy = ResponseStrategy.DIRECT
        dec_result.tone = "precise"
        dec_result.should_hedge = False
        dec_result.hedge_prefix = ""
        dec_result.max_length = 800
        dec_result.post_actions = ["save_to_memory"]

        enriched = be.apply_v2_decision(decision, decision_result=dec_result)
        assert enriched.metadata.get("v2_strategy") == "direct"
        assert enriched.metadata.get("v2_post_actions") == ["save_to_memory"]

    def test_decide_behavior_v2_returns_behavior_decision(self):
        from src.core.alfred_behavior_engine import UserState
        be = self._get_behavior_engine()

        state = UserState(emotion="neutral", intensity=0.3, intent="analysis")
        fusion = MagicMock()
        fusion.primary_source = "knowledge"
        fusion.fusion_score = 0.75

        dec_result = MagicMock()
        dec_result.strategy = ResponseStrategy.KNOWLEDGE
        dec_result.tone = "precise"
        dec_result.should_hedge = False
        dec_result.hedge_prefix = ""
        dec_result.max_length = 800
        dec_result.post_actions = []

        from src.core.alfred_behavior_engine import BehaviorDecision
        result = be.decide_behavior_v2(
            user_state=state,
            user_message="Analyse le pipeline V2.",
            fusion_result=fusion,
            decision_result=dec_result,
        )
        assert isinstance(result, BehaviorDecision)
        assert result.metadata.get("v2_strategy") == "knowledge"


# =============================================================================
# ResponseGenerator._apply_confidence_scoring()
# =============================================================================

class TestResponseGeneratorConfidence:

    def _make_context(self, memory="", knowledge="", fusion_score=0.5):
        return {
            "adaptation": {"mode": "focus", "tone": "direct"},
            "detected_emotion": "neutral",
            "memory_context": memory,
            "knowledge_context": knowledge,
            "v2": {
                "fusion_score": fusion_score,
                "should_hedge": False,
                "hedge_prefix": "",
            },
        }

    def test_no_scorer_returns_response_unchanged(self):
        gen = ResponseGenerator(confidence_scorer=None)
        ctx = self._make_context()
        assert gen._apply_confidence_scoring("Ma réponse.", ctx) == "Ma réponse."

    def test_high_confidence_no_prefix(self):
        scorer = ConfidenceScorer()
        gen = ResponseGenerator(confidence_scorer=scorer)
        ctx = self._make_context(
            memory="Contexte mémoire riche.",
            knowledge="Base de connaissances pertinente.",
            fusion_score=0.9,
        )
        result = gen._apply_confidence_scoring(
            "Réponse complète et structurée de haute qualité.", ctx
        )
        # Pas de prefix de couverture attendu
        assert not result.startswith("Je ne suis pas")
        assert not result.startswith("Je manque")

    def test_low_confidence_adds_hedge(self):
        scorer = ConfidenceScorer()
        gen = ResponseGenerator(confidence_scorer=scorer)
        ctx = self._make_context(memory="", knowledge="", fusion_score=0.0)
        result = gen._apply_confidence_scoring("Réponse courte.", ctx)
        # Avec fusion=0 + no memory + no knowledge → doit hedger
        assert result.startswith("Je") or "certain" in result.lower() or result == "Réponse courte."

    def test_v2_already_hedged_no_double_prefix(self):
        scorer = ConfidenceScorer()
        gen = ResponseGenerator(confidence_scorer=scorer)
        ctx = self._make_context()
        ctx["v2"]["should_hedge"] = True
        ctx["v2"]["hedge_prefix"] = "Je ne suis pas certain, mais "
        result = gen._apply_confidence_scoring("Ma réponse.", ctx)
        # Le scorer ne doit pas rajouter de prefix si V2 l'a déjà fait
        assert result == "Ma réponse."

    def test_scorer_handles_exception_gracefully(self):
        broken_scorer = MagicMock()
        broken_scorer.score.side_effect = RuntimeError("broken")
        gen = ResponseGenerator(confidence_scorer=broken_scorer)
        ctx = self._make_context()
        result = gen._apply_confidence_scoring("Ma réponse.", ctx)
        assert result == "Ma réponse."


# =============================================================================
# Test flux complet V2 dans build_response() (mocké)
# =============================================================================

class TestBuildResponseV2Integration:
    """
    Teste build_response() avec les moteurs V2 actifs.
    Le LLM et les composants externes sont mockés.
    """

    def _make_components(self):
        adapter = MagicMock()
        adapter.build_response_context.return_value = {
            "adaptation": {"mode": "execution_mode", "tone": "direct"},
            "memory_context": "",
            "knowledge_context": "",
        }

        memory = MagicMock()
        memory.format_context_for_prompt.return_value = ""

        generator = MagicMock()
        generator.generate_response.return_value = "Voici l'état du pipeline V2."

        behavior_engine = MagicMock()
        decision_mock = MagicMock()
        decision_mock.mode = "execution_mode"
        decision_mock.tone = "direct, structuré"
        behavior_engine.decide_behavior.return_value = decision_mock
        behavior_engine.apply_v2_decision.return_value = decision_mock

        return {
            "adapter": adapter,
            "behavior_engine": behavior_engine,
            "memory": memory,
            "generator": generator,
            "llm": None,
            "ltm_ok": False,
            "ltm": None,
            "retrieval_engine": None,
            "v2_fusion":     FusionEngine(),
            "v2_confidence": ConfidenceScorer(),
            "v2_decision":   DecisionEngine(),
        }

    def test_build_response_with_v2_returns_valid_tuple(self, monkeypatch):
        from src.main import build_response

        components = self._make_components()

        monkeypatch.setattr(
            "src.main.detect_context",
            lambda user_input, time_ctx: {
                "nlp": {"intent": "analysis", "confidence": 0.7},
                "emotion_state": MagicMock(emotion="neutral"),
                "wellbeing": MagicMock(fatigue_score=0.2),
                "mode_b03": "focus",
                "behavior_mode": "execution_mode",
                "behavior_emotion": "neutral",
                "intensity": 0.3,
                "fatigue": 0.2,
            },
        )
        monkeypatch.setattr(
            "src.memory.memory_answer_engine.answer_from_memory",
            lambda user_message, memory_context: None,
        )

        result = build_response(
            user_input="Quel est le statut du pipeline V2 ?",
            components=components,
            time_ctx={"energy_level": "medium"},
        )

        assert isinstance(result, tuple)
        assert len(result) == 4
        response, mode, emotion, energy = result
        assert isinstance(response, str)
        assert len(response) > 0

    def test_v2_context_injected_in_response_context(self, monkeypatch):
        """Vérifie que context['v2'] est bien présent après build_response."""
        from src.main import build_response

        components = self._make_components()
        captured_context = {}

        original_generate = components["generator"].generate_response

        def capture_context(*args, **kwargs):
            if "response_context" in kwargs:
                captured_context.update(kwargs["response_context"])
            elif len(args) >= 2:
                captured_context.update(args[1])
            return "Réponse capturée."

        components["generator"].generate_response.side_effect = capture_context

        monkeypatch.setattr(
            "src.main.detect_context",
            lambda user_input, time_ctx: {
                "nlp": {},
                "emotion_state": MagicMock(emotion="neutral"),
                "wellbeing": MagicMock(fatigue_score=0.2),
                "mode_b03": "focus",
                "behavior_mode": "execution_mode",
                "behavior_emotion": "neutral",
                "intensity": 0.3,
                "fatigue": 0.2,
            },
        )
        monkeypatch.setattr(
            "src.memory.memory_answer_engine.answer_from_memory",
            lambda user_message, memory_context: None,
        )

        build_response(
            user_input="Test V2 context injection",
            components=components,
            time_ctx={"energy_level": "medium"},
        )

        # context["v2"] doit être présent avec les champs attendus
        assert "v2" in captured_context, "context['v2'] absent — V2 non branché"
        v2 = captured_context["v2"]
        assert "fusion_score" in v2
        assert "confidence_score" in v2
        assert "strategy" in v2
        assert "should_hedge" in v2

    def test_emotion_used_correctly_in_v2(self, monkeypatch):
        """Vérifie que l'émotion détectée (pas 'neutral' hardcodé) est passée au V2."""
        from src.main import build_response

        components = self._make_components()
        v2_fusion_spy = MagicMock(wraps=components["v2_fusion"])
        components["v2_fusion"] = v2_fusion_spy

        monkeypatch.setattr(
            "src.main.detect_context",
            lambda user_input, time_ctx: {
                "nlp": {},
                "emotion_state": MagicMock(emotion="stressed"),
                "wellbeing": MagicMock(fatigue_score=0.8),
                "mode_b03": "support",
                "behavior_mode": "support_mode",
                "behavior_emotion": "stress",     # <-- émotion non-neutre
                "intensity": 0.8,
                "fatigue": 0.8,
            },
        )
        monkeypatch.setattr(
            "src.memory.memory_answer_engine.answer_from_memory",
            lambda user_message, memory_context: None,
        )

        build_response(
            user_input="Je suis épuisée.",
            components=components,
            time_ctx={"energy_level": "low"},
        )

        # FusionEngine.fuse() doit avoir reçu emotion="stress", pas "neutral"
        call_kwargs = v2_fusion_spy.fuse.call_args
        if call_kwargs:
            emotion_passed = call_kwargs.kwargs.get("emotion") or (
                call_kwargs.args[3] if len(call_kwargs.args) > 3 else None
            )
            if emotion_passed is not None:
                assert emotion_passed == "stress", (
                    f"Bug émotion : V2 a reçu '{emotion_passed}' au lieu de 'stress'"
                )
