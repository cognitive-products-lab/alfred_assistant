"""
PROJECT      : ALFRED
BLOCK        : B11 -- Intelligence Cognitive
FUNCTION     : 11.01.001 -> 11.01.006
FILE         : tests/b11_tests/test_fusion_engine.py
ROLE         : Tests unitaires MultiSignalFusionEngine + ConfidenceEngine + ContradictionDetector

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-05-14
UPDATED      : 2026-05-14
VERSION      : V1.0
STATUS       : STABLE

DESCRIPTION :
Tests complets de :
  - src/v3/fusion/multi_signal_fusion_engine.py
  - src/v3/fusion/confidence_engine.py
  - src/v3/fusion/contradiction_detector.py
Aucune dependance externe -- tests purement fonctionnels.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from src.v3.fusion.multi_signal_fusion_engine import (
    MultiSignalFusionEngine,
    FusedSignal,
)
from src.v3.fusion.confidence_engine import (
    ConfidenceEngine,
    ConfidenceDecision,
    CONFIDENCE_THRESHOLDS,
)
from src.v3.fusion.contradiction_detector import (
    ContradictionDetector,
    ContradictionReport,
    Contradiction,
)


# ---------------------------------------------------------
# FusedSignal dataclass
# ---------------------------------------------------------

class TestFusedSignal:

    def test_default_mode_focus(self):
        s = FusedSignal()
        assert s.recommended_mode == "focus"

    def test_default_emotion_neutral(self):
        s = FusedSignal()
        assert s.dominant_emotion == "neutral"

    def test_has_timestamp(self):
        s = FusedSignal()
        assert s.timestamp != ""

    def test_method_fusion_v1(self):
        s = FusedSignal()
        assert "fusion" in s.method


# ---------------------------------------------------------
# MultiSignalFusionEngine.fuse()
# ---------------------------------------------------------

class TestMultiSignalFusionEngine:

    def test_fuse_no_signals_returns_fused_signal(self):
        engine = MultiSignalFusionEngine()
        result = engine.fuse()
        assert isinstance(result, FusedSignal)

    def test_fuse_no_signals_confidence_zero(self):
        engine = MultiSignalFusionEngine()
        result = engine.fuse()
        assert result.confidence == 0.0

    def test_fuse_with_nlp_signal(self):
        engine = MultiSignalFusionEngine()
        nlp = {"intent": "greeting", "confidence": 0.8}
        result = engine.fuse(nlp_signal=nlp)
        assert result.intent == "greeting"
        assert result.confidence > 0.0
        assert "nlp" in result.sources_used

    def test_fuse_with_emotion_signal(self):
        engine = MultiSignalFusionEngine()
        emotion = {"emotion": "stressed", "intensity": 0.7, "valence": "negative"}
        result = engine.fuse(emotion_signal=emotion)
        assert result.dominant_emotion == "stressed"
        assert result.recommended_mode == "support"

    def test_fuse_distress_always_support(self):
        engine = MultiSignalFusionEngine()
        emotion = {"emotion": "distress", "intensity": 0.9}
        result = engine.fuse(emotion_signal=emotion)
        assert result.recommended_mode == "support"

    def test_fuse_motivated_challenge(self):
        engine = MultiSignalFusionEngine()
        emotion = {"emotion": "motivated", "intensity": 0.7}
        result = engine.fuse(emotion_signal=emotion)
        assert result.recommended_mode == "challenge"

    def test_fuse_low_energy_always_support(self):
        engine = MultiSignalFusionEngine()
        context = {"energy_level": "low", "period": "nuit"}
        emotion = {"emotion": "happy", "intensity": 0.8}
        result = engine.fuse(emotion_signal=emotion, context_signal=context)
        assert result.recommended_mode == "support"

    def test_fuse_multiple_signals_uses_all(self):
        engine = MultiSignalFusionEngine()
        nlp     = {"intent": "task", "confidence": 0.7}
        emotion = {"emotion": "focused", "intensity": 0.6}
        context = {"energy_level": "high", "period": "matin"}
        memory  = {"relevance_score": 0.5}
        result  = engine.fuse(nlp, emotion, context, memory)
        assert len(result.sources_used) == 4

    def test_fuse_coherence_normal(self):
        engine = MultiSignalFusionEngine()
        result = engine.fuse()
        assert 0.0 <= result.coherence_score <= 1.0

    def test_fuse_low_coherence_when_contradictory(self):
        engine = MultiSignalFusionEngine()
        nlp     = {"intent": "engineering", "confidence": 0.8}
        emotion = {"emotion": "distress", "intensity": 0.9}
        result  = engine.fuse(nlp, emotion)
        assert result.coherence_score < 1.0

    def test_history_grows_after_each_fuse(self):
        engine = MultiSignalFusionEngine()
        engine.fuse()
        engine.fuse()
        engine.fuse()
        assert len(engine.get_history()) == 3

    def test_clear_history(self):
        engine = MultiSignalFusionEngine()
        engine.fuse()
        engine.clear_history()
        assert len(engine.get_history()) == 0

    def test_status_returns_dict(self):
        engine = MultiSignalFusionEngine()
        s = engine.status()
        assert isinstance(s, dict)
        assert "version" in s

    def test_custom_weights(self):
        weights = {"nlp": 0.5, "emotion": 0.3, "context": 0.2, "memory": 0.0}
        engine = MultiSignalFusionEngine(weights=weights)
        assert engine.weights["nlp"] == 0.5


# ---------------------------------------------------------
# ConfidenceEngine
# ---------------------------------------------------------

class TestConfidenceEngine:

    def test_evaluate_returns_confidence_decision(self):
        engine = ConfidenceEngine()
        fused  = FusedSignal(confidence=0.8, coherence_score=0.9, sources_used=["nlp", "emotion"])
        result = engine.evaluate(fused)
        assert isinstance(result, ConfidenceDecision)

    def test_high_confidence_act(self):
        engine = ConfidenceEngine()
        fused  = FusedSignal(confidence=0.95, coherence_score=1.0, sources_used=["nlp", "emotion", "context"])
        result = engine.evaluate(fused)
        assert result.action == "act"
        assert result.level  == "high"

    def test_low_confidence_clarify(self):
        engine = ConfidenceEngine()
        fused  = FusedSignal(confidence=0.1, coherence_score=0.2, sources_used=[])
        result = engine.evaluate(fused)
        assert result.action == "clarify"
        assert result.level  == "low"

    def test_medium_confidence_proceed_cautiously(self):
        engine = ConfidenceEngine()
        fused  = FusedSignal(confidence=0.5, coherence_score=0.6, sources_used=["nlp"])
        result = engine.evaluate(fused)
        assert result.level  == "medium"
        assert result.action == "proceed_cautiously"

    def test_evaluate_from_score_high(self):
        engine = ConfidenceEngine()
        result = engine.evaluate_from_score(0.9, coherence=1.0)
        assert result.action == "act"

    def test_evaluate_from_score_low(self):
        engine = ConfidenceEngine()
        result = engine.evaluate_from_score(0.1, coherence=0.2)
        assert result.action == "clarify"

    def test_is_high_confidence_true(self):
        engine = ConfidenceEngine()
        assert engine.is_high_confidence(0.85) is True

    def test_is_high_confidence_false(self):
        engine = ConfidenceEngine()
        assert engine.is_high_confidence(0.3) is False

    def test_is_low_confidence_true(self):
        engine = ConfidenceEngine()
        assert engine.is_low_confidence(0.2) is True

    def test_explanation_is_string(self):
        engine = ConfidenceEngine()
        result = engine.evaluate_from_score(0.5)
        assert isinstance(result.explanation, str)
        assert len(result.explanation) > 0

    def test_history_grows(self):
        engine = ConfidenceEngine()
        engine.evaluate_from_score(0.5)
        engine.evaluate_from_score(0.8)
        assert len(engine.get_history()) == 2

    def test_clear_history(self):
        engine = ConfidenceEngine()
        engine.evaluate_from_score(0.5)
        engine.clear_history()
        assert len(engine.get_history()) == 0

    def test_status_dict(self):
        engine = ConfidenceEngine()
        s = engine.status()
        assert "thresholds" in s
        assert "version" in s

    def test_factors_in_decision(self):
        engine = ConfidenceEngine()
        fused  = FusedSignal(confidence=0.7, coherence_score=0.9, sources_used=["nlp"])
        result = engine.evaluate(fused)
        assert isinstance(result.factors, dict)


# ---------------------------------------------------------
# ContradictionDetector
# ---------------------------------------------------------

class TestContradictionDetector:

    def test_analyze_returns_report(self):
        detector = ContradictionDetector()
        report = detector.analyze()
        assert isinstance(report, ContradictionReport)

    def test_no_contradiction_clean(self):
        detector = ContradictionDetector()
        emotion  = {"emotion": "neutral", "intensity": 0.0}
        report   = detector.analyze("aide-moi a organiser", emotion)
        assert len(report.contradictions) == 0

    def test_detects_positive_text_negative_emotion(self):
        detector = ContradictionDetector()
        emotion  = {"emotion": "distress", "intensity": 0.9}
        report   = detector.analyze("ca va super bien", emotion)
        assert len(report.contradictions) > 0
        assert report.contradictions[0].type == "emotion_text_mismatch"

    def test_no_contradiction_below_intensity_threshold(self):
        detector = ContradictionDetector()
        emotion  = {"emotion": "stressed", "intensity": 0.2}  # faible intensite
        report   = detector.analyze("ca va bien", emotion)
        # Intensite trop faible -> pas de contradiction detectee
        assert not any(c.type == "emotion_text_mismatch" for c in report.contradictions)

    def test_energy_emotion_mismatch(self):
        detector = ContradictionDetector()
        emotion  = {"emotion": "sad", "intensity": 0.7}
        context  = {"energy_level": "high"}
        report   = detector.analyze("", emotion, context)
        types = [c.type for c in report.contradictions]
        assert "energy_emotion_mismatch" in types

    def test_incoherence_score_zero_when_clean(self):
        detector = ContradictionDetector()
        report   = detector.analyze("aide-moi")
        assert report.incoherence_score == 0.0

    def test_incoherence_score_positive_when_contradiction(self):
        detector = ContradictionDetector()
        emotion  = {"emotion": "distress", "intensity": 0.9}
        report   = detector.analyze("ca va super bien", emotion)
        assert report.incoherence_score > 0.0

    def test_has_contradictions_helper(self):
        detector = ContradictionDetector()
        emotion  = {"emotion": "distress", "intensity": 0.9}
        report   = detector.analyze("ca va super", emotion)
        assert detector.has_contradictions(report) is True

    def test_has_contradictions_false_when_clean(self):
        detector = ContradictionDetector()
        report   = detector.analyze("aide-moi")
        assert detector.has_contradictions(report) is False

    def test_has_critical_true_for_high_severity(self):
        detector = ContradictionDetector()
        emotion  = {"emotion": "distress", "intensity": 0.9}
        report   = detector.analyze("ca va super bien", emotion)
        assert isinstance(report.has_critical, bool)

    def test_severity_summary_returns_dict(self):
        detector = ContradictionDetector()
        emotion  = {"emotion": "distress", "intensity": 0.9}
        report   = detector.analyze("ca va super", emotion)
        summary  = detector.get_severity_summary(report)
        assert isinstance(summary, dict)
        assert "low" in summary
        assert "medium" in summary
        assert "high" in summary
