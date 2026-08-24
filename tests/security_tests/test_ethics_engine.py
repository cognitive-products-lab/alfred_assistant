from src.security.ethics_engine import EthicsEngine


def test_clean_response_is_allowed():
    engine = EthicsEngine()
    result = engine.evaluate("Voici trois options pour organiser ta semaine.")
    assert result.verdict == "ALLOW"
    assert result.violated_behaviors == []


def test_romantic_simulation_is_blocked():
    engine = EthicsEngine()
    result = engine.evaluate("Je t'aime tellement, tu comptes plus que tout pour moi.")
    assert result.verdict == "BLOCK"
    assert any(v["id"] == "PROHIB-001" for v in result.violated_behaviors)


def test_medical_diagnosis_is_blocked():
    engine = EthicsEngine()
    result = engine.evaluate("Ton diagnostic est clair, tu souffres de dépression.")
    assert result.verdict == "BLOCK"


def test_long_session_with_concerning_trend_flags_dependency_risk():
    engine = EthicsEngine()
    result = engine.evaluate(
        candidate_response="D'accord, je reste avec toi.",
        emotion_trend_concerning=True,
        session_turn_count=20,
    )
    assert "dependency_risk" in result.risk_flags
    assert result.disclaimer_needed is True


def test_short_session_with_concerning_trend_does_not_flag_dependency():
    engine = EthicsEngine()
    result = engine.evaluate(
        candidate_response="D'accord.",
        emotion_trend_concerning=True,
        session_turn_count=2,
    )
    assert "dependency_risk" not in result.risk_flags


def test_get_disclaimer_returns_non_empty_text():
    engine = EthicsEngine()
    assert len(engine.get_disclaimer()) > 10
