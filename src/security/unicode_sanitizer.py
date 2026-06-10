"""
════════════════════════════════════════════════════════════
PROJECT      : ALFRED
BLOCK        : B20
FUNCTION     : 20.16
FILE         : src/security/unicode_sanitizer.py
ROLE         : Normalisation Unicode et détection d'attaques homographes

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-06-01
UPDATED      : 2026-06-01
VERSION      : V1.0
STATUS       : ACTIVE

DESCRIPTION :
Normalise les entrées Unicode (NFC/NFKC), détecte les attaques
par homographes (caractères cyrilliques/grecs qui ressemblent à
des caractères latins), les caractères de contrôle et les encodages
suspects (URL-encoding, Unicode escape).
════════════════════════════════════════════════════════════
"""
from __future__ import annotations

import re
import unicodedata
from typing import Any

from src.security.security_logger import log_event

# ─── Mapping homographes Cyrillic → Latin ─────────────────────────────────────
# Caractères cyrilliques/grecs/arméniens qui ressemblent visuellement à des
# caractères ASCII — vecteur d'attaque IDN homograph.

_HOMOGRAPH_MAP: dict[str, str] = {
    # Cyrillique
    "а": "a", "е": "e", "о": "o", "р": "r", "с": "c", "х": "x",
    "А": "A", "В": "B", "Е": "E", "К": "K", "М": "M", "Н": "H",
    "О": "O", "Р": "P", "С": "C", "Т": "T", "У": "Y", "Х": "X",
    # Grec
    "α": "a", "β": "b", "ε": "e", "ο": "o", "ρ": "r", "υ": "u",
    "Α": "A", "Β": "B", "Ε": "E", "Η": "H", "Ι": "I", "Κ": "K",
    "Μ": "M", "Ν": "N", "Ο": "O", "Ρ": "R", "Τ": "T", "Υ": "Y",
    "Χ": "X",
    # Arménien
    "ա": "w", "ո": "n",
    # Latin étendu confusables
    "ℓ": "l", "℮": "e", "ℬ": "B",
}

# ─── Patterns suspects ────────────────────────────────────────────────────────

_URL_ENCODED   = re.compile(r"%[0-9A-Fa-f]{2}")          # %2e%2e%2f...
_UNICODE_ESC   = re.compile(r"\\u[0-9A-Fa-f]{4}")        # ‮ (RTL override)
_CONTROL_CHARS = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")  # sauf \t\n
_ZERO_WIDTH    = re.compile(r"[​‌‍‎‏﻿⁠⁡]")
_RTL_OVERRIDE  = re.compile(r"[‪-‮⁦-⁩]")       # Bidi overrides


def normalize(text: str, form: str = "NFKC") -> str:
    """
    Normalise un texte Unicode en forme NFKC (compatibilité + composition).
    NFKC décompose les caractères compatibles et recompose — élimine la
    plupart des variations visuelles (½ → 1/2, ﬁ → fi, etc.).
    """
    return unicodedata.normalize(form, text)


def transliterate_homographs(text: str) -> str:
    """
    Remplace les caractères homographes par leurs équivalents ASCII.
    Retourne le texte normalisé pour détection de mots-clés malveillants.
    """
    return "".join(_HOMOGRAPH_MAP.get(ch, ch) for ch in text)


def detect_homograph_attack(text: str) -> dict[str, Any]:
    """
    Détecte si le texte contient des caractères homographes suspects.

    Returns:
        dict avec is_suspicious, homograph_chars, transliterated, risk_score
    """
    found: list[str] = []
    for ch in text:
        if ch in _HOMOGRAPH_MAP:
            found.append(ch)

    is_suspicious = len(found) > 0
    risk_score    = min(100, len(found) * 15)

    if is_suspicious:
        log_event(
            f"unicode_sanitizer: homographes détectés — {len(found)} caractère(s) "
            f"suspects : {found[:5]}",
            "WARNING",
        )

    return {
        "is_suspicious":    is_suspicious,
        "homograph_chars":  found,
        "homograph_count":  len(found),
        "transliterated":   transliterate_homographs(text),
        "risk_score":       risk_score,
    }


def detect_control_chars(text: str) -> dict[str, Any]:
    """Détecte les caractères de contrôle, zero-width et RTL overrides."""
    control  = _CONTROL_CHARS.findall(text)
    zw       = _ZERO_WIDTH.findall(text)
    rtl      = _RTL_OVERRIDE.findall(text)

    all_found = control + zw + rtl
    is_suspicious = len(all_found) > 0

    if is_suspicious:
        log_event(
            f"unicode_sanitizer: caractères de contrôle/RTL — "
            f"control={len(control)} zero-width={len(zw)} rtl={len(rtl)}",
            "WARNING",
        )

    return {
        "is_suspicious":  is_suspicious,
        "control_chars":  len(control),
        "zero_width":     len(zw),
        "rtl_overrides":  len(rtl),
        "total_found":    len(all_found),
        "risk_score":     min(100, len(all_found) * 20),
    }


def detect_encoding_obfuscation(text: str) -> dict[str, Any]:
    """Détecte les tentatives d'encodage suspect (URL-encode, Unicode escape)."""
    url_matches     = _URL_ENCODED.findall(text)
    unicode_matches = _UNICODE_ESC.findall(text)

    all_found = url_matches + unicode_matches
    is_suspicious = len(all_found) > 0

    return {
        "is_suspicious":    is_suspicious,
        "url_encoded":      url_matches,
        "unicode_escapes":  unicode_matches,
        "total_found":      len(all_found),
        "risk_score":       min(100, len(all_found) * 10),
    }


def full_unicode_analysis(text: str) -> dict[str, Any]:
    """
    Analyse complète Unicode : normalisation + homographes + contrôle + encodage.

    Returns:
        dict avec is_safe, risk_score, normalized, findings, details
    """
    normalized      = normalize(text)
    transliterated  = transliterate_homographs(normalized)
    homograph       = detect_homograph_attack(text)
    control         = detect_control_chars(text)
    encoding        = detect_encoding_obfuscation(text)

    total_risk = min(100,
        homograph["risk_score"] +
        control["risk_score"] +
        encoding["risk_score"]
    )

    findings: list[str] = []
    if homograph["is_suspicious"]:
        findings.append(f"{homograph['homograph_count']} caractère(s) homographe(s)")
    if control["is_suspicious"]:
        findings.append(
            f"{control['control_chars']} ctrl + {control['zero_width']} zero-width "
            f"+ {control['rtl_overrides']} RTL"
        )
    if encoding["is_suspicious"]:
        findings.append(f"{encoding['total_found']} encodage(s) suspect(s)")

    return {
        "is_safe":        total_risk == 0,
        "risk_score":     total_risk,
        "normalized":     normalized,
        "transliterated": transliterated,
        "findings":       findings,
        "details": {
            "homograph": homograph,
            "control":   control,
            "encoding":  encoding,
        },
    }


def sanitize_unicode(text: str, strict: bool = False) -> str:
    """
    Nettoie un texte Unicode :
    - Normalise en NFKC
    - Supprime les caractères de contrôle (sauf \\n\\t)
    - Supprime les zero-width et RTL overrides
    - En mode strict : translittère les homographes

    Returns:
        Texte nettoyé.
    """
    text = normalize(text)
    text = _CONTROL_CHARS.sub("", text)
    text = _ZERO_WIDTH.sub("", text)
    text = _RTL_OVERRIDE.sub("", text)
    if strict:
        text = transliterate_homographs(text)
    return text
