"""
════════════════════════════════════════════════════════════
PROJECT      : ALFRED
BLOCK        : B01
FUNCTION     : 01.04
FILE         : test_safety_gate.py
ROLE         : Tests du SafetyNet (src/security/safety_gate.py)

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-08-14
UPDATED      : 2026-08-14
VERSION      : V1.0
STATUS       : ACTIVE

DESCRIPTION :
Vérifie la classification de sensibilité par mots-clés (santé, sécurité
domicile, données tierces) et que cloud_allowed reste True par défaut sur
prompt neutre / vide / non-string.
════════════════════════════════════════════════════════════
"""

from src.security.safety_gate import assess_prompt_sensitivity, is_cloud_allowed


def test_neutral_prompt_allows_cloud():
    result = assess_prompt_sensitivity("Rappelle-moi mon rendez-vous demain.")

    assert result["cloud_allowed"] is True
    assert result["privacy_level"] == "STANDARD"
    assert result["matched_categories"] == []


def test_health_keyword_blocks_cloud():
    result = assess_prompt_sensitivity("Sébastien a fait une chute ce matin, je m'inquiète.")

    assert result["cloud_allowed"] is False
    assert result["privacy_level"] == "LOCAL_ONLY"
    assert "sante" in result["matched_categories"]


def test_home_security_keyword_blocks_cloud():
    result = assess_prompt_sensitivity("Affiche le flux de la caméra Tuya du salon.")

    assert result["cloud_allowed"] is False
    assert "securite_domicile" in result["matched_categories"]


def test_is_cloud_allowed_shortcut_matches_assess():
    assert is_cloud_allowed("Quel temps fait-il aujourd'hui ?") is True
    assert is_cloud_allowed("Mon médicament ne fait plus effet.") is False


def test_empty_or_non_string_defaults_to_allowed():
    assert assess_prompt_sensitivity("")["cloud_allowed"] is True
    assert assess_prompt_sensitivity(None)["cloud_allowed"] is True
