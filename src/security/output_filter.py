SENSITIVE_TERMS = [
    "FERNET_KEY",
    "SECRET_KEY",
    "PIN_SALT",
    "api_key",
    "password",
    ".env",
]

def filter_output(response: str) -> str:
    """Masque les termes sensibles dans une réponse."""
    filtered = response

    for term in SENSITIVE_TERMS:
        filtered = filtered.replace(term, "[DONNÉE_PROTÉGÉE]")

    return filtered
