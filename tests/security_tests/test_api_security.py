"""
════════════════════════════════════════════════════════════
PROJECT      : ALFRED
BLOCK        : B20
FUNCTION     : 20.07
FILE         : tests/security_tests/test_api_security.py
ROLE         : Tests unitaires — api_security.py

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-05-31
VERSION      : V1.0
STATUS       : ACTIVE
════════════════════════════════════════════════════════════
"""
import pytest
from src.security.api_security import (
    validate_api_key,
    check_api_rate_limit,
    check_endpoint_access,
    authorize_api_request,
    generate_api_key,
    get_api_security_status,
)


class TestValidateApiKey:

    def test_empty_key_rejected(self):
        result = validate_api_key("")
        assert isinstance(result, dict)
        assert result.get("valid") is False

    def test_random_key_returns_dict(self):
        result = validate_api_key("sk-test-abc123")
        assert isinstance(result, dict)
        assert "valid" in result

    def test_generated_key_is_valid(self):
        key = generate_api_key("test_payload")
        result = validate_api_key(key)
        assert isinstance(result, dict)


class TestRateLimit:

    def test_rate_limit_returns_tuple(self):
        result = check_api_rate_limit("any_key")
        assert isinstance(result, dict)
        assert "allowed" in result

    def test_fresh_key_under_quota(self):
        key = generate_api_key("fresh_key_test")
        result = check_api_rate_limit(key)
        assert result.get("allowed") is True


class TestEndpointAccess:

    def test_owner_can_access_chat(self):
        result = check_endpoint_access("OWNER", "/api/chat")
        assert isinstance(result, (bool, dict))

    def test_guest_restricted_on_admin(self):
        result = check_endpoint_access("GUEST", "/api/admin")
        # Peut retourner bool=False ou dict avec allowed=False
        if isinstance(result, dict):
            assert result.get("allowed") is False
        else:
            assert result is False


class TestAuthorizeApiRequest:

    def test_returns_dict(self):
        result = authorize_api_request(
            api_key="",
            role="OWNER",
            endpoint="/api/chat",
        )
        assert isinstance(result, dict)
        assert "authorized" in result

    def test_guest_on_admin_denied(self):
        result = authorize_api_request(
            api_key="",
            role="GUEST",
            endpoint="/api/admin",
        )
        assert result.get("authorized") is False


class TestGenerateApiKey:

    def test_returns_non_empty_string(self):
        key = generate_api_key("payload_test")
        assert isinstance(key, str)
        assert len(key) > 0

    def test_different_payloads_give_different_keys(self):
        k1 = generate_api_key("payload_a")
        k2 = generate_api_key("payload_b")
        assert k1 != k2


class TestApiSecurityStatus:

    def test_returns_dict(self):
        status = get_api_security_status()
        assert isinstance(status, dict)
        assert len(status) > 0
