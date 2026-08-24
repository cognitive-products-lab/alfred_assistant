from src.reasoning.reasoning_engine import ReasoningEngine, ReasoningResult


def test_empty_input_gives_zero_confidence():
    engine = ReasoningEngine()
    result = engine.analyze("")
    assert result.confidence_score == 0.0
    assert result.confidence_band == "low"


def test_simple_input_is_not_decomposed():
    engine = ReasoningEngine()
    result = engine.analyze("salut")
    assert result.complexity == "simple"
    assert result.sub_questions == []


def test_multi_clause_input_is_decomposed():
    engine = ReasoningEngine()
    result = engine.analyze(
        "pourquoi je suis fatiguée l'après-midi et comment corriger ça et que puis-je changer dans mes habitudes"
    )
    assert result.complexity in ("complex", "critical")
    assert len(result.sub_questions) >= 2


def test_reasoning_mode_detected_by_keyword():
    engine = ReasoningEngine()
    result = engine.analyze("et si j'arrêtais le café le matin ?")
    assert result.reasoning_mode == "counterfactual"


def test_contradictions_lower_confidence():
    engine = ReasoningEngine()
    result = ReasoningResult(raw_input="x")
    result.contradictions = [{"a": 1}]
    engine._evaluate(result, emotion_trend_concerning=False)
    assert result.confidence_score <= 0.4


def test_llm_reasoning_context_mentions_low_confidence():
    engine = ReasoningEngine()
    result = ReasoningResult(raw_input="x", confidence_band="low")
    engine._synthesize(result)
    assert "CONFIANCE FAIBLE" in result.llm_reasoning_context
