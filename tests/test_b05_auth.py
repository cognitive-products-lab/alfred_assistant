"""
════════════════════════════════════════════════════════════
PROJECT      : ALFRED
BLOCK        : B05
FUNCTION     : 05.TESTS
FILE         : tests/test_b05_auth.py
ROLE         : Tests unitaires authentification (B05)

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-06-15
UPDATED      : 2026-06-20
VERSION      : V1.1
STATUS       : VALIDATED

DESCRIPTION :
Couvre src/auth/auth_manager.py, src/auth/login_handler.py,
src/auth/user_session.py et src/auth/authenticator.py.
════════════════════════════════════════════════════════════
"""

from __future__ import annotations

import hashlib

import pytest

from src.auth import auth_manager, authenticator, login_handler, user_session
from src.security import rate_limiter, session_manager


@pytest.fixture(autouse=True)
def _clean_auth_state():
    """Réinitialise l'état global (session courante) avant/après chaque test."""
    auth_manager.logout()
    yield
    auth_manager.logout()


# ─────────────────────────────────────────────────────────
# user_session.py — profil et préférences
# ─────────────────────────────────────────────────────────

class TestUserSession:

    def test_load_profile_unknown_user_returns_default(self):
        profile = user_session.load_profile("user_does_not_exist_xyz")
        assert profile == {"user_id": "user_does_not_exist_xyz", "preferences": {}}

    def test_load_profile_existing_user(self):
        profile = user_session.load_profile("user_celine_instance")
        assert isinstance(profile, dict)
        assert profile.get("user_id") or "preferences" in profile

    def test_set_and_get_preference(self):
        user_session.load_profile("user_does_not_exist_xyz")
        user_session.set_preference("language", "en")
        assert user_session.get_preference("language") == "en"

    def test_get_preference_default_when_missing(self):
        user_session.load_profile("user_does_not_exist_xyz")
        assert user_session.get_preference("unknown_key", "fallback") == "fallback"

    def test_get_session_profile_is_a_copy(self):
        user_session.load_profile("user_does_not_exist_xyz")
        profile = user_session.get_session_profile()
        profile["preferences"]["language"] = "es"
        assert user_session.get_preference("language") != "es"

    def test_preferred_language_default(self):
        user_session.load_profile("user_does_not_exist_xyz")
        assert user_session.get_preferred_language() == "fr"

    def test_preferred_mode_default(self):
        user_session.load_profile("user_does_not_exist_xyz")
        assert user_session.get_preferred_mode() == "complicite"


# ─────────────────────────────────────────────────────────
# auth_manager.py — login / logout / session courante
# ─────────────────────────────────────────────────────────

class TestAuthManager:

    def test_auto_login_creates_active_session(self):
        session_id = auth_manager.auto_login(user_id="test_user_am1", role="OWNER")
        assert session_id
        assert auth_manager.is_authenticated()

    def test_get_current_user_after_login(self):
        auth_manager.auto_login(user_id="test_user_am2", role="USER")
        info = auth_manager.get_current_user()
        assert info["authenticated"] is True
        assert info["user_id"] == "test_user_am2"
        assert info["role"] == "USER"

    def test_get_current_role_returns_role(self):
        auth_manager.auto_login(user_id="test_user_am3", role="ADMIN")
        assert auth_manager.get_current_role() == "ADMIN"

    def test_not_authenticated_by_default(self):
        assert auth_manager.is_authenticated() is False

    def test_get_current_user_when_not_authenticated(self):
        info = auth_manager.get_current_user()
        assert info == {"user_id": "", "role": "", "authenticated": False}

    def test_get_current_role_guest_when_not_authenticated(self):
        assert auth_manager.get_current_role() == "GUEST"

    def test_logout_clears_session(self):
        auth_manager.auto_login(user_id="test_user_am4", role="OWNER")
        assert auth_manager.is_authenticated()

        assert auth_manager.logout() is True
        assert auth_manager.is_authenticated() is False
        assert auth_manager.get_current_role() == "GUEST"

    def test_login_without_pin_hash_succeeds(self, monkeypatch):
        monkeypatch.delenv("PIN_HASH", raising=False)
        monkeypatch.delenv("PIN_SALT", raising=False)

        result = auth_manager.login(user_id="test_user_am5", role="OWNER", pin="anything")
        assert result["success"] is True
        assert result["session_id"]

    def test_login_with_wrong_pin_fails(self, monkeypatch):
        correct_hash = hashlib.sha256(b"1234").hexdigest()
        monkeypatch.setenv("PIN_HASH", correct_hash)

        result = auth_manager.login(user_id="test_user_am6", role="OWNER", pin="0000")
        assert result["success"] is False
        assert result["session_id"] is None
        assert "PIN incorrect" in result["reason"]
        assert auth_manager.is_authenticated() is False

    def test_login_with_correct_pin_succeeds(self, monkeypatch):
        correct_hash = hashlib.sha256(b"1234").hexdigest()
        monkeypatch.setenv("PIN_HASH", correct_hash)

        result = auth_manager.login(user_id="test_user_am7", role="OWNER", pin="1234")
        assert result["success"] is True
        assert result["session_id"]
        assert auth_manager.is_authenticated() is True


# ─────────────────────────────────────────────────────────
# login_handler.py — orchestration login/logout
# ─────────────────────────────────────────────────────────

class TestLoginHandler:

    def test_start_auto_session_returns_session_id(self):
        session_id = login_handler.start_auto_session(user_id="test_user_lh1", role="OWNER")
        assert session_id
        assert auth_manager.is_authenticated()

    def test_session_status_reflects_active_session(self):
        login_handler.start_auto_session(user_id="test_user_lh2", role="OWNER")
        status = login_handler.session_status()
        assert status["authenticated"] is True
        assert status["user"]["user_id"] == "test_user_lh2"
        assert "profile" in status

    def test_session_status_when_not_authenticated(self):
        status = login_handler.session_status()
        assert status == {"authenticated": False, "user": {}, "profile": {}}

    def test_end_session_closes_session(self):
        login_handler.start_auto_session(user_id="test_user_lh3", role="OWNER")
        assert auth_manager.is_authenticated()

        assert login_handler.end_session(user_id="test_user_lh3") is True
        assert auth_manager.is_authenticated() is False

    def test_start_session_with_correct_pin(self, monkeypatch):
        correct_hash = hashlib.sha256(b"5678").hexdigest()
        monkeypatch.setenv("PIN_HASH", correct_hash)

        result = login_handler.start_session(
            user_id="test_user_lh4", role="OWNER", device_id="local_pc", pin="5678"
        )
        assert result["success"] is True
        assert result["session_id"]
        assert result["user"]["authenticated"] is True
        assert "profile" in result

    def test_start_session_with_wrong_pin_fails(self, monkeypatch):
        correct_hash = hashlib.sha256(b"5678").hexdigest()
        monkeypatch.setenv("PIN_HASH", correct_hash)

        result = login_handler.start_session(
            user_id="test_user_lh5", role="OWNER", device_id="local_pc", pin="0000"
        )
        assert result["success"] is False
        assert result["session_id"] is None
        assert result["user"] == {}
        assert result["profile"] == {}


# ─────────────────────────────────────────────────────────
# authenticator.py — authentification par PIN (bcrypt/PBKDF2)
# ─────────────────────────────────────────────────────────

class TestAuthenticator:

    @pytest.fixture(autouse=True)
    def _isolated_pin_store(self, tmp_path, monkeypatch):
        """Isole pins.json + rate limiter pour ne pas polluer les données réelles."""
        monkeypatch.setattr(authenticator, "_PIN_STORE", tmp_path / "pins.json")
        rate_limiter._attempts.clear()
        rate_limiter._lockout_until.clear()
        session_manager.FAILED_ATTEMPTS.clear()
        yield
        rate_limiter._attempts.clear()
        rate_limiter._lockout_until.clear()
        session_manager.FAILED_ATTEMPTS.clear()

    def test_register_and_authenticate_pin_success(self):
        assert authenticator.register_pin("user_auth1", "1234") is True
        result = authenticator.authenticate("user_auth1", "1234")
        assert result["success"] is True

    def test_authenticate_wrong_pin_fails(self):
        authenticator.register_pin("user_auth2", "1234")
        result = authenticator.authenticate("user_auth2", "0000")
        assert result["success"] is False
        assert result["reason"] == "PIN incorrect"

    def test_authenticate_unknown_user_fails(self):
        result = authenticator.authenticate("user_never_registered", "1234")
        assert result["success"] is False
        assert result["reason"] == "Utilisateur inconnu"

    def test_has_pin(self):
        assert authenticator.has_pin("user_auth3") is False
        authenticator.register_pin("user_auth3", "1234")
        assert authenticator.has_pin("user_auth3") is True

    def test_register_pin_rejects_invalid_length(self):
        assert authenticator.register_pin("user_auth4", "12") is False
        assert authenticator.has_pin("user_auth4") is False

    def test_change_pin_success(self):
        authenticator.register_pin("user_auth5", "1234")
        assert authenticator.change_pin("user_auth5", "1234", "5678") is True
        assert authenticator.authenticate("user_auth5", "5678")["success"] is True
        assert authenticator.authenticate("user_auth5", "1234")["success"] is False

    def test_change_pin_fails_with_wrong_old_pin(self):
        authenticator.register_pin("user_auth6", "1234")
        assert authenticator.change_pin("user_auth6", "0000", "5678") is False
        assert authenticator.authenticate("user_auth6", "1234")["success"] is True

    def test_rate_limiting_blocks_after_max_attempts(self):
        authenticator.register_pin("user_auth7", "1234")

        for _ in range(rate_limiter.MAX_ATTEMPTS):
            result = authenticator.authenticate("user_auth7", "0000")
            assert result["success"] is False

        blocked_result = authenticator.authenticate("user_auth7", "0000")
        assert blocked_result["success"] is False
        assert "Trop de tentatives" in blocked_result["reason"]

    def test_successful_auth_resets_rate_limit(self):
        authenticator.register_pin("user_auth8", "1234")

        for _ in range(rate_limiter.MAX_ATTEMPTS - 1):
            authenticator.authenticate("user_auth8", "0000")

        result = authenticator.authenticate("user_auth8", "1234")
        assert result["success"] is True

        limited, _ = rate_limiter.is_rate_limited("user_auth8")
        assert limited is False
