"""
PROJECT      : ALFRED  |  BLOCK : B01 V2  |  FUNCTION : 01.V2.01
FILE         : tests/b01_tests/test_fusion_engine.py
ROLE         : Tests FusionEngine V2
AUTHOR       : Cognitive Products Lab  |  CREATED : 2026-06-01  |  STATUS : VALIDATED
"""
import pytest
from src.v2.fusion.fusion_engine import (
    FusionEngine, FusionResult, SourceContribution,
    get_fusion_engine, reset_fusion_engine,
)


@pytest.fixture(autouse=True)
def reset():
    reset_fusion_engine()
    yield
    reset_fusion_engine()


class TestSourceContribution:
    def test_default_weight(self):
        sc = SourceContribution(source="memory", content="test")
        assert sc.weight == 1.0

    def test_custom_weight(self):
        sc = SourceContribution(source="knowledge", content="x", weight=0.5)
        assert sc.weight == 0.5


class TestFusionEngine:

    def test_fuse_all_sources_returns_result(self):
        engine = FusionEngine()
        result = engine.fuse(
            memory_context="J'ai mangé des pâtes hier",
            knowledge_context="Nutrition: pâtes = glucides",
            llm_context="contexte LLM initial",
        )
        assert isinstance(result, FusionResult)

    def test_fuse_empty_returns_result(self):
        engine = FusionEngine()
        result = engine.fuse()
        assert isinstance(result, FusionResult)
        assert result.merged_context == ""

    def test_fuse_with_memory_only(self):
        engine = FusionEngine()
        result = engine.fuse(memory_context="souvenir important")
        assert "souvenir" in result.merged_context
        assert result.primary_source == "memory"

    def test_fuse_with_knowledge_only(self):
        engine = FusionEngine()
        result = engine.fuse(knowledge_context="domaine: nutrition")
        assert "nutrition" in result.merged_context

    def test_merged_context_is_string(self):
        engine = FusionEngine()
        result = engine.fuse(memory_context="mem", knowledge_context="know")
        assert isinstance(result.merged_context, str)

    def test_weights_sum_to_one(self):
        engine = FusionEngine()
        result = engine.fuse(memory_context="x", knowledge_context="y", llm_context="z")
        total = sum(result.weights.values())
        assert abs(total - 1.0) < 0.01

    def test_fusion_score_between_0_and_1(self):
        engine = FusionEngine()
        result = engine.fuse(memory_context="m", knowledge_context="k", llm_context="l")
        assert 0.0 <= result.fusion_score <= 1.0

    def test_to_context_string_truncates(self):
        engine = FusionEngine()
        result = engine.fuse(memory_context="x" * 5000)
        truncated = result.to_context_string(max_chars=100)
        assert len(truncated) <= 100

    def test_emotion_boost_memory_weight(self):
        engine = FusionEngine()
        result = engine.fuse(
            memory_context="m", knowledge_context="k",
            emotion="stressed"
        )
        assert result.weights["memory"] > result.weights["knowledge"]

    def test_focus_mode_boost_knowledge(self):
        engine = FusionEngine()
        result = engine.fuse(
            memory_context="m", knowledge_context="k",
            mode="focus"
        )
        assert result.weights["knowledge"] >= result.weights["memory"]

    def test_priority_strategy_orders_by_weight(self):
        engine = FusionEngine(strategy="priority")
        result = engine.fuse(
            memory_context="memory content",
            knowledge_context="knowledge content",
            llm_context="llm content",
        )
        assert isinstance(result.merged_context, str)

    def test_update_weights(self):
        engine = FusionEngine()
        engine.update_weights(memory=0.8)
        assert engine.weights["memory"] == 0.8

    def test_update_weights_clamped(self):
        engine = FusionEngine()
        engine.update_weights(memory=5.0)
        assert engine.weights["memory"] == 1.0

    def test_context_blocks_count(self):
        engine = FusionEngine()
        result = engine.fuse(memory_context="m", knowledge_context="k")
        assert len(result.context_blocks) == 2


class TestSingleton:

    def test_get_fusion_engine_returns_same_instance(self):
        e1 = get_fusion_engine()
        e2 = get_fusion_engine()
        assert e1 is e2

    def test_reset_creates_new_instance(self):
        e1 = get_fusion_engine()
        reset_fusion_engine()
        e2 = get_fusion_engine()
        assert e1 is not e2
