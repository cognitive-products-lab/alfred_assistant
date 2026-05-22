# ============================================================
# ALFRED — src/security/input_validator.py
# Bloc 20.10 — Gestion des vulnérabilités
#
# 📚 NOTION EXAM :
#   D42-2 — Capsule 6 : Validation des entrées — boundary validation (OWASP)
#
# 🎯 UTILITÉ ALFRED :
#   Nettoie et filtre toutes les entrées utilisateur ; bloque XSS,
#   injection SQL, injections shell et traversées de répertoire.
#
# 🔐 BLOC SÉCURITÉ :
#   Security by Design — validation à la frontière du système (input sanitization)
# ============================================================

import re
import html
from src.security.security_logger import log_event

FORBIDDEN_PATTERNS = [
    r"<script.*?>",
    r"DROP\s+TABLE",
    r"UNION\s+SELECT",
    r";\s*rm\s+-rf",
    r"\.\./",
    r"powershell\s+-enc",
    r"cmd\.exe",
]

def sanitize_input(user_input: str, max_length: int = 1000) -> str:
    """Nettoie une entrée utilisateur et bloque les motifs dangereux connus."""
    if not isinstance(user_input, str):
        log_event("Input rejeté : type invalide", "WARNING")
        return ""

    cleaned = html.escape(user_input.strip())

    if len(cleaned) > max_length:
        log_event("Input rejeté : longueur excessive", "WARNING")
        return ""

    for pattern in FORBIDDEN_PATTERNS:
        if re.search(pattern, cleaned, re.IGNORECASE):
            log_event(f"Input rejeté : motif interdit détecté {pattern}", "WARNING")
            return ""

    return cleaned
