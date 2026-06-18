"""
PROJECT      : ALFRED
BLOCK        : B20
FUNCTION     : XX.XX
FILE         : test_output_filter.py
ROLE         : TO_DEFINE

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-05-10
UPDATED      : 2026-05-10
VERSION      : V1.0
STATUS       : DRAFT

DESCRIPTION :
TO_COMPLETE
"""

"""
Tests B20 — output_filter.py
"""

from src.security.output_filter import filter_output, analyze_output, safe_output


def test_safe_output_is_unchanged():
    response = "Bonjour Céline, tout est prêt."

    assert filter_output(response) == response


def test_sensitive_term_is_masked():
    response = "La variable FERNET_KEY est définie."

    filtered = filter_output(response)

    assert "FERNET_KEY" not in filtered
    assert "[DONNÉE_PROTÉGÉE]" in filtered


def test_api_key_pattern_is_masked():
    response = "Voici la clé api_key=abc123SECRET"

    filtered = filter_output(response)

    assert "abc123SECRET" not in filtered
    assert "[DONNÉE_PROTÉGÉE]" in filtered


def test_bearer_token_is_masked():
    response = "Authorization: Bearer abc.def.ghi"

    filtered = filter_output(response)

    assert "Bearer abc.def.ghi" not in filtered
    assert "[DONNÉE_PROTÉGÉE]" in filtered


def test_non_string_output_is_blocked():
    assert filter_output(123) == ""


def test_analyze_output_safe():
    result = analyze_output("Réponse normale.")

    assert result["safe"] is True
    assert result["risk_score"] == 0
    assert result["findings"] == []


def test_analyze_output_sensitive():
    result = analyze_output("password=secret123")

    assert result["safe"] is False
    assert result["risk_score"] > 0
    assert result["findings"]


def test_safe_output_returns_filtered_response():
    result = safe_output("password=secret123")

    assert result["safe"] is False
    assert "[DONNÉE_PROTÉGÉE]" in result["filtered_response"]