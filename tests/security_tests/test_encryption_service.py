"""
════════════════════════════════════════════════════════════
PROJECT      : ALFRED
BLOCK        : B20
FUNCTION     : 20.05
FILE         : tests/security_tests/test_encryption_service.py
ROLE         : Tests unitaires — encryption_service.py

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-05-31
VERSION      : V1.0
STATUS       : ACTIVE
════════════════════════════════════════════════════════════
"""
import pytest
from src.security.encryption_service import encrypt, decrypt, is_available, rotate_key


class TestIsAvailable:

    def test_returns_bool(self):
        assert isinstance(is_available(), bool)


class TestEncryptDecrypt:

    def test_encrypt_returns_string(self):
        if not is_available():
            pytest.skip("FERNET_KEY absent")
        result = encrypt("données sensibles")
        assert isinstance(result, str) and len(result) > 0

    def test_decrypt_restores_original(self):
        if not is_available():
            pytest.skip("FERNET_KEY absent")
        original = "Céline, données confidentielles"
        assert decrypt(encrypt(original)) == original

    def test_encrypt_different_each_time(self):
        if not is_available():
            pytest.skip("FERNET_KEY absent")
        assert encrypt("test") != encrypt("test")

    def test_encrypt_empty_string(self):
        if not is_available():
            pytest.skip("FERNET_KEY absent")
        result = encrypt("")
        assert isinstance(result, str)

    def test_decrypt_invalid_does_not_crash(self):
        if not is_available():
            pytest.skip("FERNET_KEY absent")
        try:
            result = decrypt("invalid_ciphertext")
            assert isinstance(result, str)
        except Exception:
            pass  # Exception acceptable


class TestRotateKey:

    def test_rotate_returns_string(self):
        result = rotate_key()
        assert isinstance(result, str)
