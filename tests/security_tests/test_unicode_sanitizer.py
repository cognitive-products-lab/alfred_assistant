"""
════════════════════════════════════════════════════════════
PROJECT      : ALFRED
BLOCK        : B20
FUNCTION     : 20.TEST
FILE         : tests/security_tests/test_unicode_sanitizer.py
ROLE         : Tests unitaires — unicode_sanitizer.py

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-06-01
VERSION      : V1.0
STATUS       : ACTIVE
════════════════════════════════════════════════════════════
"""

import pytest
from src.security.unicode_sanitizer import (
    normalize, transliterate_homographs, detect_homograph_attack,
    detect_control_chars, detect_encoding_obfuscation,
    full_unicode_analysis, sanitize_unicode,
)


# ─── normalize ────────────────────────────────────────────────────────────────

def test_normalize_nfkc_ligature():
    assert normalize("ﬁ") == "fi"

def test_normalize_nfkc_fraction():
    # NFKC décompose ½ en "1" + FRACTION SLASH + "2" (U+2044), pas le slash ASCII
    result = normalize("½")
    assert result.startswith("1") and result.endswith("2")

def test_normalize_idempotent():
    text = "Bonjour Alfred"
    assert normalize(normalize(text)) == normalize(text)

def test_normalize_accents_preserved():
    assert normalize("café") == "café"


# ─── Homographes ──────────────────────────────────────────────────────────────

def test_detect_cyrillic_homograph():
    # "а" cyrillique ressemble à "a" latin
    result = detect_homograph_attack("аdmin")
    assert result["is_suspicious"] is True
    assert result["homograph_count"] >= 1

def test_no_homograph_in_latin():
    result = detect_homograph_attack("hello world 123")
    assert result["is_suspicious"] is False

def test_transliterate_cyrillic():
    # "аdmin" avec "а" cyrillique → "admin"
    out = transliterate_homographs("аdmin")
    assert out == "admin"

def test_detect_greek_homograph():
    result = detect_homograph_attack("αlfred")  # α grec
    assert result["is_suspicious"] is True

def test_full_analysis_detects_homograph():
    r = full_unicode_analysis("аdmin")
    assert r["is_safe"] is False
    assert r["risk_score"] > 0
    assert any("homographe" in f.lower() for f in r["findings"])


# ─── Caractères de contrôle ───────────────────────────────────────────────────

def test_detect_null_byte():
    result = detect_control_chars("hello\x00world")
    assert result["is_suspicious"] is True
    assert result["control_chars"] >= 1

def test_detect_rtl_override():
    # U+202E RIGHT-TO-LEFT OVERRIDE
    result = detect_control_chars("safe‮text")
    assert result["is_suspicious"] is True
    assert result["rtl_overrides"] >= 1

def test_normal_text_no_control():
    result = detect_control_chars("Bonjour Alfred !")
    assert result["is_suspicious"] is False
    assert result["total_found"] == 0

def test_newline_not_flagged():
    result = detect_control_chars("ligne1\nligne2")
    assert result["control_chars"] == 0


# ─── Encodage suspect ─────────────────────────────────────────────────────────

def test_detect_url_encoding():
    result = detect_encoding_obfuscation("../../%2e%2e/etc/passwd")
    assert result["is_suspicious"] is True
    assert len(result["url_encoded"]) >= 2

def test_detect_unicode_escape():
    result = detect_encoding_obfuscation("\\u202e override")
    assert result["is_suspicious"] is True

def test_clean_url_not_flagged():
    result = detect_encoding_obfuscation("https://example.com/page")
    assert result["is_suspicious"] is False


# ─── sanitize_unicode ────────────────────────────────────────────────────────

def test_sanitize_removes_control():
    clean = sanitize_unicode("hello\x00world")
    assert "\x00" not in clean
    assert "hello" in clean

def test_sanitize_removes_rtl():
    clean = sanitize_unicode("text‮more")
    assert "‮" not in clean

def test_sanitize_strict_transliterates():
    clean = sanitize_unicode("аdmin", strict=True)
    assert clean == "admin"

def test_sanitize_normal_text_unchanged():
    text = "Bonjour Alfred, comment vas-tu ?"
    assert sanitize_unicode(text) == normalize(text)


# ─── full_unicode_analysis ────────────────────────────────────────────────────

def test_full_analysis_clean_text():
    r = full_unicode_analysis("Bonjour Alfred !")
    assert r["is_safe"] is True
    assert r["risk_score"] == 0
    assert r["findings"] == []

def test_full_analysis_structure():
    r = full_unicode_analysis("test")
    for k in {"is_safe","risk_score","normalized","transliterated","findings","details"}:
        assert k in r

def test_full_analysis_combined_attack():
    # null byte + cyrillic homograph
    r = full_unicode_analysis("аdmin\x00")
    assert r["risk_score"] > 0
    assert not r["is_safe"]
