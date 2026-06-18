"""
PROJECT      : ALFRED
BLOCK        : B20
FUNCTION     : XX.XX
FILE         : test_security_config.py
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
Tests B20 — security_config.py
"""

from src.security.security_config import (
    get_config,
    get_int_config,
    get_bool_config,
    get_security_config,
    validate_security_config,
    summarize_security_config,
    APP_ENV,
    API_HOST,
    SESSION_TIMEOUT,
    MAX_LOGIN_ATTEMPTS,
)


def test_static_config_values_exist():
    assert APP_ENV
    assert API_HOST
    assert isinstance(SESSION_TIMEOUT, int)
    assert isinstance(MAX_LOGIN_ATTEMPTS, int)


def test_get_config_default():
    assert get_config("UNKNOWN_TEST_CONFIG", "default_value") == "default_value"


def test_get_int_config_default():
    assert get_int_config("UNKNOWN_INT_CONFIG", 42) == 42


def test_get_bool_config_default_false():
    assert get_bool_config("UNKNOWN_BOOL_CONFIG", False) is False


def test_get_security_config_returns_dict():
    config = get_security_config()

    assert isinstance(config, dict)
    assert "APP_ENV" in config
    assert "SESSION_TIMEOUT" in config
    assert "LOCAL_FIRST_MODE" in config


def test_validate_security_config_returns_structure():
    result = validate_security_config()

    assert "valid" in result
    assert "issues" in result
    assert "config" in result
    assert isinstance(result["issues"], list)


def test_summarize_security_config_returns_dashboard_fields():
    summary = summarize_security_config()

    assert "valid" in summary
    assert "issues_count" in summary
    assert "zero_trust_enabled" in summary
    assert "local_first_mode" in summary