"""
PROJECT      : ALFRED
BLOCK        : B20
FUNCTION     : XX.XX
FILE         : test_input_validator.py
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
Tests B20 — input_validator.py
"""

from src.security.input_validator import sanitize_input, is_valid_input, get_clean_input


def test_valid_input_is_accepted():
    result = sanitize_input("Bonjour Alfred")

    assert result["valid"] is True
    assert result["cleaned_input"] == "Bonjour Alfred"
    assert result["risk_score"] == 0
    assert result["reasons"] == []


def test_empty_input_is_rejected():
    result = sanitize_input("   ")

    assert result["valid"] is False
    assert result["cleaned_input"] == ""
    assert "Input vide" in result["reasons"]


def test_non_string_input_is_rejected():
    result = sanitize_input(123)

    assert result["valid"] is False
    assert "Type invalide" in result["reasons"]


def test_too_long_input_is_rejected():
    result = sanitize_input("a" * 1001)

    assert result["valid"] is False
    assert "Input trop long" in result["reasons"]


def test_forbidden_pattern_is_rejected():
    result = sanitize_input("DROP TABLE users")

    assert result["valid"] is False
    assert result["risk_score"] >= 60
    assert result["reasons"]


def test_html_is_escaped():
    result = sanitize_input("<b>Bonjour</b>")

    assert result["valid"] is True
    assert result["cleaned_input"] == "&lt;b&gt;Bonjour&lt;/b&gt;"


def test_is_valid_input_helper():
    assert is_valid_input("Bonjour") is True
    assert is_valid_input("DROP TABLE users") is False


def test_get_clean_input_helper():
    assert get_clean_input("  Bonjour  ") == "Bonjour"
    assert get_clean_input("DROP TABLE users") == ""