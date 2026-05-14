"""
PROJECT      : ALFRED
BLOCK        : B20
FUNCTION     : XX.XX
FILE         : output_filter.py
ROLE         : Filtrage sorties IA — masque secrets et données sensibles

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-05-10
P26-05-12
VERSION      : V1.0
STATUS       : STABLE

DESCRIPTION :
Filtre les sorties IA pour masquer tokens, clés API, mots de passe et autres secrets.
"""

import re
from typing import Dict, Any

from src.security.security_logger import log_event


SENSITIVE_TERMS = [
    "FERNET_KEY",
    "SECRET_KEY",
    "PIN_SALT",
    "API_KEY",
    "OPENAI_API_KEY",
    "PASSWORD",
    ".env",
]

SENSITIVE_PATTERNS = [
    r"sk-[A-Za-z0-9_\-]{10,}",
    r"Bearer\s+[A-Za-z0-9_\-\.]+",
    r"api[_-]?key\s*[:=]\s*[A-Za-z0-9_\-\.]+",
    r"password\s*[:=]\s*[^ \n\r]+",
    r"token\s*[:=]\s*[A-Za-z0-9_\-\.]+",
    r"secret\s*[:=]\s*[A-Za-z0-9_\-\.]+",
    r"FERNET_KEY\s*[:=]\s*[A-Za-z0-9_\-=]+",
]


def filter_output(response: str) -> str:
    """Filtre une réponse avant affichage utilisateur. Masquage case-insensitive."""
    if not isinstance(response, str):
        log_event("Output filter : réponse non textuelle bloquée", "WARNING")
        return ""

    filtered = response

    # 1. Patterns complets en premier : api_key=xxx, token=xxx, sk-xxx, etc.
    for pattern in SENSITIVE_PATTERNS:
        filtered = re.sub(pattern, "[DONNÉE_PROTÉGÉE]", filtered, flags=re.IGNORECASE)

    # 2. Termes isolés — correctif P2 : re.IGNORECASE pour PASSWORD, Api_Key, etc.
    for term in SENSITIVE_TERMS:
        filtered = re.sub(re.escape(term), "[DONNÉE_PROTÉGÉE]", filtered, flags=re.IGNORECASE)

    if filtered != response:
        log_event("Filtrage sécurité appliqué sur sortie IA", "WARNING")

    return filtered


def analyze_output(response: str) -> Dict[str, Any]:
    """Analyse une sortie IA et indique si un filtrage est nécessaire."""
    result = {
        "safe": True,
        "risk_score": 0,
        "findings": [],
    }

    if not isinstance(response, str):
        result["safe"] = False
        result["risk_score"] = 50
        result["findings"].append("Réponse non textuelle")
        return result

    for term in SENSITIVE_TERMS:
        if term.lower() in response.lower():
            result["safe"] = False
            result["risk_score"] += 30
            result["findings"].append(f"Terme sensible détecté : {term}")

    for pattern in SENSITIVE_PATTERNS:
        if re.search(pattern, response, re.IGNORECASE):
            result["safe"] = False
            result["risk_score"] += 40
            result["findings"].append(f"Pattern sensible détecté : {pattern}")

    return result


def safe_output(response: str) -> Dict[str, Any]:
    """Retourne une réponse filtrée avec analyse de sécurité."""
    analysis = analyze_output(response)
    filtered = filter_output(response)

    return {
        "safe": analysis["safe"],
        "risk_score": analysis["risk_score"],
        "findings": analysis["findings"],
        "filtered_response": filtered,
    }
