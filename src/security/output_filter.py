import re

SENSITIVE_TERMS = [
    "FERNET_KEY",
    "SECRET_KEY",
    "PIN_SALT",
    "api_key",
    "password",
    ".env",
    "private_key",
    "auth_token",
    "access_token",
    "refresh_token",
    "bearer ",
]

# Regex pour les patterns de clés/tokens courants
_TOKEN_PATTERNS = [
    re.compile(r"(?:sk|pk|rk|ak)-[A-Za-z0-9_\-]{20,}", re.I),   # API keys style OpenAI
    re.compile(r"eyJ[A-Za-z0-9_\-]{10,}\.[A-Za-z0-9_\-]{10,}", re.I),  # JWT
    re.compile(r"(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{30,}", re.I),  # GitHub tokens
    re.compile(r"[A-Za-z0-9+/]{40,}={0,2}"),  # Base64 potentiellement sensible (>40 chars)
]

_REPLACEMENT = "[DONNÉE_PROTÉGÉE]"


def filter_output(response: str) -> str:
    """Masque les termes sensibles et patterns de tokens dans une réponse."""
    filtered = response

    for term in SENSITIVE_TERMS:
        filtered = filtered.replace(term, _REPLACEMENT)

    for pattern in _TOKEN_PATTERNS:
        filtered = pattern.sub(_REPLACEMENT, filtered)

    return filtered
