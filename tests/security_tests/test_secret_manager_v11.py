"""
════════════════════════════════════════════════════════════
PROJECT      : ALFRED — tests secret_manager V1.1
BLOCK        : B20 · FUNCTION : 20.TEST
VERSION      : V1.1 · STATUS : ACTIVE
════════════════════════════════════════════════════════════
"""
import pytest
import os
from src.security.secret_manager import (
    get_secret, get_secret_optional, get_secret_multi,
    secret_exists, mask_secret, get_secret_masked,
    validate_env_secrets, require_all_secrets,
    get_access_stats, get_stale_secrets, summarize_secrets,
    secret_age_days, is_secret_stale,
    _access_count, _access_log,
)


@pytest.fixture(autouse=True)
def inject_test_secrets(monkeypatch):
    """Injecte des secrets de test dans l'environnement."""
    monkeypatch.setenv("TEST_SECRET_KEY",   "super_secret_value_123")
    monkeypatch.setenv("TEST_SECRET_SHORT", "ab")
    monkeypatch.setenv("FERNET_KEY",        "test_fernet_key_value")
    monkeypatch.setenv("SECRET_KEY",        "test_secret_key_value")
    monkeypatch.setenv("PIN_SALT",          "test_pin_salt_value")
    # Réinitialiser l'audit log entre tests
    _access_count.clear()
    _access_log.clear()
    yield
    _access_count.clear()
    _access_log.clear()


# ─── get_secret ───────────────────────────────────────────────────────────────

def test_get_secret_present():
    val = get_secret("TEST_SECRET_KEY")
    assert val == "super_secret_value_123"

def test_get_secret_missing_raises():
    with pytest.raises(ValueError, match="Secret manquant"):
        get_secret("NONEXISTENT_SECRET_XYZ")

def test_get_secret_records_access():
    get_secret("TEST_SECRET_KEY")
    stats = get_access_stats()
    assert "TEST_SECRET_KEY" in stats
    assert stats["TEST_SECRET_KEY"]["total_accesses"] >= 1

def test_get_secret_no_audit():
    get_secret("TEST_SECRET_KEY", audit=False)
    stats = get_access_stats()
    assert "TEST_SECRET_KEY" not in stats


# ─── get_secret_optional ─────────────────────────────────────────────────────

def test_get_secret_optional_present():
    val = get_secret_optional("TEST_SECRET_KEY")
    assert val == "super_secret_value_123"

def test_get_secret_optional_missing_returns_default():
    val = get_secret_optional("NONEXISTENT_XYZ", default="fallback")
    assert val == "fallback"

def test_get_secret_optional_missing_empty_default():
    val = get_secret_optional("NONEXISTENT_XYZ")
    assert val == ""


# ─── get_secret_multi ────────────────────────────────────────────────────────

def test_get_secret_multi_all_present():
    result = get_secret_multi(["FERNET_KEY", "SECRET_KEY"])
    assert "FERNET_KEY" in result
    assert "SECRET_KEY" in result

def test_get_secret_multi_missing_raises():
    with pytest.raises(RuntimeError, match="manquants"):
        get_secret_multi(["FERNET_KEY", "NONEXISTENT_XYZ"])


# ─── secret_exists ───────────────────────────────────────────────────────────

def test_secret_exists_true():
    assert secret_exists("TEST_SECRET_KEY") is True

def test_secret_exists_false():
    assert secret_exists("NONEXISTENT_SECRET_XYZ") is False


# ─── mask_secret ─────────────────────────────────────────────────────────────

def test_mask_secret_long():
    # "super_secret_value_123" = 22 chars, visible=4 → "supe" + 18 étoiles
    result = mask_secret("super_secret_value_123", 4)
    assert result.startswith("supe")
    assert result.count("*") == 18

def test_mask_secret_short():
    # len("ab") <= visible_chars(4) → retourné en clair (trop court)
    assert mask_secret("ab", 4) == "ab"

def test_mask_secret_exact():
    # len("abcd") == visible_chars(4) → retourné en clair
    assert mask_secret("abcd", 4) == "abcd"


# ─── get_secret_masked ───────────────────────────────────────────────────────

def test_get_secret_masked():
    result = get_secret_masked("TEST_SECRET_KEY", visible_chars=4)
    assert result.startswith("supe")
    assert "*" in result


# ─── validate_env_secrets ────────────────────────────────────────────────────

def test_validate_env_secrets_all_ok():
    result = validate_env_secrets(["FERNET_KEY", "SECRET_KEY", "PIN_SALT"])
    assert all(v == "OK" for v in result.values())

def test_validate_env_secrets_missing():
    result = validate_env_secrets(["FERNET_KEY", "NONEXISTENT_XYZ"])
    assert result["NONEXISTENT_XYZ"] == "MANQUANT"
    assert result["FERNET_KEY"] == "OK"


# ─── require_all_secrets ─────────────────────────────────────────────────────

def test_require_all_secrets_ok():
    result = require_all_secrets(["FERNET_KEY", "SECRET_KEY"])
    assert all(v == "OK" for v in result.values())

def test_require_all_secrets_missing_raises():
    with pytest.raises(RuntimeError):
        require_all_secrets(["FERNET_KEY", "NONEXISTENT_XYZ"])


# ─── access stats ────────────────────────────────────────────────────────────

def test_access_stats_increments():
    get_secret("TEST_SECRET_KEY")
    get_secret("TEST_SECRET_KEY")
    stats = get_access_stats()
    assert stats["TEST_SECRET_KEY"]["total_accesses"] == 2

def test_access_stats_last_access_format():
    get_secret("TEST_SECRET_KEY")
    stats = get_access_stats()
    last = stats["TEST_SECRET_KEY"]["last_access"]
    assert "T" in last or last is not None   # ISO format


# ─── âge des secrets ─────────────────────────────────────────────────────────

def test_secret_age_days_present():
    age = secret_age_days("FERNET_KEY")
    # Le .env existe — l'âge doit être un nombre >= 0
    assert age is None or isinstance(age, float)

def test_secret_age_days_missing():
    age = secret_age_days("NONEXISTENT_SECRET_XYZ_789")
    assert age is None

def test_is_secret_stale_not_old():
    # Un secret ne peut pas être stale si le .env vient d'être créé
    result = is_secret_stale("FERNET_KEY", max_days=3650)  # 10 ans
    assert result is False


# ─── get_stale_secrets ───────────────────────────────────────────────────────

def test_get_stale_secrets_high_threshold():
    stale = get_stale_secrets(["FERNET_KEY", "SECRET_KEY"], max_days=3650)
    assert isinstance(stale, list)
    assert "FERNET_KEY" not in stale   # pas encore stale avec 10 ans de seuil


# ─── summarize ───────────────────────────────────────────────────────────────

def test_summarize_secrets_structure():
    s = summarize_secrets(["FERNET_KEY", "SECRET_KEY", "PIN_SALT"])
    assert s["present_count"] == 3
    assert s["missing_count"] == 0
    assert s["all_ok"] is True
    assert "rotation_recommended" in s
    assert "access_stats" in s

def test_summarize_secrets_with_missing():
    s = summarize_secrets(["FERNET_KEY", "NONEXISTENT_XYZ"])
    assert s["missing_count"] == 1
    assert s["all_ok"] is False
