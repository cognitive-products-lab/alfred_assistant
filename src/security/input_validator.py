"""
PROJECT      : ALFRED
BLOCK        : B20
FUNCTION     : XX.XX
FILE         : input_validator.py
ROLE         : Validation et nettoyage des entrées utilisateur

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-05-10
P26-05-12
VERSION      : V1.0
STATUS       : STABLE

DESCRIPTION :
Valide et nettoie les entrées utilisateur. Vérifie longueur, patterns dangereux, puis échappe HTML.
"""

import html
import re
from typing import Dict, Any

from src.security.security_logger import log_event


MAX_INPUT_LENGTH = 1000

FORBIDDEN_PATTERNS = [
    r"<script.*?>",
    r"</script>",
    r"DROP\s+TABLE",
    r"UNION\s+SELECT",
    r"INSERT\s+INTO",
    r"DELETE\s+FROM",
    r";\s*rm\s+-rf",
    r"\.\./",
    r"powershell\s+-enc",
    r"cmd\.exe",
    r"curl\s+http",
    r"wget\s+http",
]


def sanitize_input(
    user_input: str,
    max_length: int = MAX_INPUT_LENGTH,
) -> Dict[str, Any]:
    """
    Nettoie et valide une entrée utilisateur.

    Returns:
        dict: {"valid": bool, "cleaned_input": str, "risk_score": int, "reasons": list[str]}
    """
    result = {
        "valid": False,
        "cleaned_input": "",
        "risk_score": 0,
        "reasons": [],
    }

    if not isinstance(user_input, str):
        result["risk_score"] += 50
        result["reasons"].append("Type invalide")
        log_event("Input rejeté : type invalide", "WARNING")
        return result

    raw_input = user_input.strip()

    if not raw_input:
        result["risk_score"] += 20
        result["reasons"].append("Input vide")
        log_event("Input rejeté : vide", "WARNING")
        return result

    if len(raw_input) > max_length:
        result["risk_score"] += 30
        result["reasons"].append("Input trop long")
        log_event("Input rejeté : longueur excessive", "WARNING")
        return result

    # Vérification sur le texte brut AVANT html.escape — correctif P1
    for pattern in FORBIDDEN_PATTERNS:
        if re.search(pattern, raw_input, re.IGNORECASE):
            result["risk_score"] += 60
            result["reasons"].append(f"Motif interdit détecté : {pattern}")
            log_event(f"Input rejeté : motif interdit détecté {pattern}", "WARNING")
            return result

    cleaned = html.escape(raw_input)

    result["valid"] = True
    result["cleaned_input"] = cleaned

    return result


def is_valid_input(user_input: str) -> bool:
    """Retourne uniquement True/False pour les appels simples."""
    return sanitize_input(user_input).get("valid", False)


def get_clean_input(user_input: str) -> str:
    """Retourne uniquement l'entrée nettoyée, ou une chaîne vide."""
    result = sanitize_input(user_input)
    return result.get("cleaned_input", "") if result.get("valid") else ""
