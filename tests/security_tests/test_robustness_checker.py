from src.reasoning.reasoning_engine import ReasoningResult
from src.security.robustness_checker import RobustnessChecker


def test_clean_exchange_is_robust():
    checker = RobustnessChecker()
    report = checker.check(user_input="salut", candidate_response="Bonjour, comment puis-je aider ?")
    assert report.is_robust is True
    assert report.issues == []


def test_empty_input_flagged():
    checker = RobustnessChecker()
    report = checker.check(user_input="", candidate_response="ok")
    assert report.is_robust is False
    assert "empty_input" in report.issues


def test_repeat_pattern_flagged():
    checker = RobustnessChecker()
    report = checker.check(user_input="a" * 30, candidate_response="ok bien reçu")
    assert "input_repeat_pattern" in report.issues


def test_empty_output_flagged():
    checker = RobustnessChecker()
    report = checker.check(user_input="salut", candidate_response="")
    assert "empty_output" in report.issues


def test_confidence_complexity_mismatch_detected():
    checker = RobustnessChecker()
    reasoning_result = ReasoningResult(raw_input="x", complexity="critical", confidence_score=0.9)
    report = checker.check(
        user_input="question complexe",
        candidate_response="réponse suffisamment longue pour ne pas déclencher d'autre alerte",
        reasoning_result=reasoning_result,
    )
    assert "confidence_complexity_mismatch" in report.issues
    assert report.confidence_adjusted == 0.54


def test_ethics_block_propagates_as_issue():
    checker = RobustnessChecker()
    report = checker.check(
        user_input="salut",
        candidate_response="réponse suffisamment longue pour ne pas déclencher d'autre alerte",
        ethics_verdict="BLOCK",
    )
    assert "ethics_blocked" in report.issues
