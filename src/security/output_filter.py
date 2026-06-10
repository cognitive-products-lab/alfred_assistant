"""
════════════════════════════════════════════════════════════
PROJECT      : ALFRED
BLOCK        : B20
FUNCTION     : 20.12
FILE         : output_filter.py
ROLE         : Filtrage des données sensibles en sortie IA

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-05-23
UPDATED      : 2026-06-01
VERSION      : V1.1
STATUS       : ACTIVE

DESCRIPTION :
Masque les secrets, tokens et PII (téléphone, email, CB, IBAN, SS)
dans les réponses générées par l'IA.
════════════════════════════════════════════════════════════
"""
import re

SENSITIVE_TERMS = [
    "FERNET_KEY", "SECRET_KEY", "PIN_SALT", "api_key", "password",
    "PASSWORD", ".env", "private_key", "auth_token", "access_token",
    "refresh_token", "bearer ", "Bearer ",
]

# ── Regex tokens et clés ──────────────────────────────────────────────────────
_TOKEN_PATTERNS = [
    re.compile(r"(?:sk|pk|rk|ak)-[A-Za-z0-9_\-]{20,}", re.I),        # API keys OpenAI
    re.compile(r"eyJ[A-Za-z0-9_\-]{10,}\.[A-Za-z0-9_\-]{10,}", re.I),# JWT
    re.compile(r"(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{30,}", re.I),   # GitHub tokens
    re.compile(r"[A-Za-z0-9+/]{40,}={0,2}"),                          # Base64 long
]

# ── Regex PII ─────────────────────────────────────────────────────────────────
_PII_PATTERNS = [
    # Numéro de carte bancaire (Visa/MC/Amex/CB) — 13 à 19 chiffres, optionnellement séparés
    re.compile(r"\b(?:\d[ \-]?){13,19}\b"),
    # IBAN européen
    re.compile(r"\b[A-Z]{2}\d{2}[ ]?(?:[A-Z0-9]{4}[ ]?){4,7}\b"),
    # Numéro de sécurité sociale FR (15 chiffres avec espaces/tirets optionnels)
    re.compile(r"\b[12]\s?\d{2}\s?\d{2}\s?\d{2}\s?\d{3}\s?\d{3}\s?\d{2}\b"),
    # Numéro de téléphone FR/International
    re.compile(r"(?:\+33|0033|0)[1-9](?:[ .\-]?\d{2}){4}\b"),
    re.compile(r"\+\d{1,3}[ \-]?\(?\d{1,4}\)?[ \-]?\d{3,4}[ \-]?\d{4}"),
    # Email
    re.compile(r"\b[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}\b"),
    # Clés Fernet brutes (gAAAAAB...)
    re.compile(r"gAAAAA[A-Za-z0-9_\-]{60,}"),
]

_REPLACEMENT = "[DONNÉE_PROTÉGÉE]"


import re as _re

# Pattern pour masquer term=valeur (terme suivi d'un = et d'une valeur non-espace)
_TERM_VALUE_PATTERN = {
    term: _re.compile(_re.escape(term) + r"=\S+", _re.I)
    for term in SENSITIVE_TERMS
}

# Pattern Bearer token
_BEARER_PATTERN = _re.compile(r"Bearer\s+\S+", _re.I)


def filter_output(response) -> str:
    """Masque les termes sensibles et patterns de tokens dans une réponse."""
    if not isinstance(response, str):
        return ""
    filtered = response
    # Masquer "term=valeur" en priorité
    for term, pattern in _TERM_VALUE_PATTERN.items():
        filtered = pattern.sub(_REPLACEMENT, filtered)
    # Ensuite masquer le terme seul s'il reste
    for term in SENSITIVE_TERMS:
        filtered = filtered.replace(term, _REPLACEMENT)
    # Bearer token
    filtered = _BEARER_PATTERN.sub(_REPLACEMENT, filtered)
    # Patterns tokens
    for pattern in _TOKEN_PATTERNS:
        filtered = pattern.sub(_REPLACEMENT, filtered)
    # Patterns PII
    for pattern in _PII_PATTERNS:
        filtered = pattern.sub(_REPLACEMENT, filtered)
    return filtered


def safe_output(response) -> dict:
    """Analyse et filtre une réponse — retourne un dict structuré."""
    result = analyze_output(response)
    return {
        "safe": result["safe"],
        "filtered_response": result["filtered"],
        "risk_score": result["risk_score"],
        "findings": result["findings"],
    }


def analyze_output(response) -> dict:
    """Filtre la réponse et retourne un rapport structuré."""
    if not isinstance(response, str):
        return {"safe": False, "risk_score": 100, "findings": ["Type invalide"], "filtered": ""}
    filtered = filter_output(response)
    findings = []
    for term in SENSITIVE_TERMS:
        if term in response:
            findings.append(f"Terme sensible : {term}")
    for pattern in _TOKEN_PATTERNS:
        if pattern.search(response):
            findings.append("Pattern token détecté")
    return {
        "safe": len(findings) == 0,
        "risk_score": min(100, len(findings) * 20),
        "findings": findings,
        "filtered": filtered,
        "original_length": len(response),
        "replacements": filtered.count(_REPLACEMENT),
    }
