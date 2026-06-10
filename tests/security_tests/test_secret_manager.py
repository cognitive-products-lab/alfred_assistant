"""
PROJECT      : ALFRED
BLOCK        : B20
FUNCTION     : XX.XX
FILE         : test_secret_manager.py
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
Tests B20 — secret_manager.py
"""

import os

import pytest

from src.security.secret_manager import (
    get_secret,
    secret_exists,
    mask_secret,
    get_secret_masked,
    validate_env_secrets,
    summarize_secrets,
    require_all_secrets,
)


def test_get_secret_success(monkeypatch):
    monkeypatch.setenv("TEST_SECRET", "secret-value")

    assert get_secret("TEST_SECRET") == "secret-value"


def test_get_secret_missing_raises(monkeypatch):
    monkeypatch.delenv("MISSING_SECRET_TEST", raising=False)

    with pytest.raises(ValueError):
        get_secret("MISSING_SECRET_TEST")


def test_get_secret_empty_key_raises():
    with pytest.raises(ValueError):
        get_secret("")


def test_secret_exists_true(monkeypatch):
    monkeypatch.setenv("EXISTING_SECRET_TEST", "value")

    assert secret_exists("EXISTING_SECRET_TEST") is True


def test_secret_exists_false(monkeypatch):
    monkeypatch.delenv("UNKNOWN_SECRET_TEST", raising=False)

    assert secret_exists("UNKNOWN_SECRET_TEST") is False


def test_mask_secret():
    assert mask_secret("abcdef", visible_chars=2) == "ab****"


def test_mask_secret_short_value():
    assert mask_secret("abc", visible_chars=4) == "abc"


def test_get_secret_masked(monkeypatch):
    monkeypatch.setenv("MASKED_SECRET_TEST", "abcdef")

    assert get_secret_masked("MASKED_SECRET_TEST") == "abcd**"


def test_validate_env_secrets(monkeypatch):
    monkeypatch.setenv("REQ_SECRET_A", "value")
    monkeypatch.delenv("REQ_SECRET_B", raising=False)

    result = validate_env_secrets(["REQ_SECRET_A", "REQ_SECRET_B"])

    assert result["REQ_SECRET_A"] == "OK"
    assert result["REQ_SECRET_B"] == "MANQUANT"


def test_summarize_secrets(monkeypatch):
    monkeypatch.setenv("REQ_SECRET_A", "value")
    monkeypatch.delenv("REQ_SECRET_B", raising=False)

    summary = summarize_secrets(["REQ_SECRET_A", "REQ_SECRET_B"])

    assert summary["required_count"] == 2
    assert summary["present_count"] == 1
    assert summary["missing_count"] == 1
    assert summary["all_ok"] is False


def test_require_all_secrets_success(monkeypatch):
    monkeypatch.setenv("REQ_SECRET_A", "value")

    require_all_secrets(["REQ_SECRET_A"])


def test_require_all_secrets_failure(monkeypatch):
    monkeypatch.delenv("REQ_SECRET_MISSING", raising=False)

    with pytest.raises(RuntimeError):
        require_all_secrets(["REQ_SECRET_MISSING"])