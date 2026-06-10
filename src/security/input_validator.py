"""
════════════════════════════════════════════════════════════
PROJECT      : ALFRED
BLOCK        : B20
FUNCTION     : 20.10
FILE         : input_validator.py
ROLE         : Validation et assainissement des entrées utilisateur

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-05-23
UPDATED      : 2026-05-23
VERSION      : V1.0
STATUS       : ACTIVE

DESCRIPTION :
Détecte et bloque SQLi, XSS, path traversal, command injection et prompt injection.
════════════════════════════════════════════════════════════
"""
import re
import html
import unicodedata
from src.security.security_logger import log_event

MAX_INPUT_LENGTH = 1000

# Patterns appliqués sur le texte normalisé AVANT html.escape
_PATTERNS: list[tuple[re.Pattern, str]] = [
    # SQL injection
    (re.compile(r"(?:drop|truncate|alter|create)\s+(?:table|database|index|view|column)", re.I | re.S), "SQL DDL"),
    (re.compile(r"(?:insert|update|delete|merge|select)\s+.{0,60}\s+(?:from|into|set|where)\b", re.I | re.S), "SQL DML"),
    (re.compile(r"union\s+(?:all\s+)?select", re.I | re.S), "UNION SELECT"),
    (re.compile(r"(?:exec|execute|xp_|sp_)\w*\s*\(", re.I), "SQL EXEC"),
    (re.compile(r"--\s*$|;\s*--", re.M), "SQL comment injection"),
    (re.compile(r"'\s*(?:or|and)\s+['\d]", re.I), "SQL tautologie"),
    (re.compile(r"\bor\s+\d+\s*=\s*\d+", re.I), "SQL OR tautologie"),
    (re.compile(r"\band\s+\d+\s*=\s*\d+", re.I), "SQL AND tautologie"),
    # XSS / HTML injection — appliqués avant html.escape
    (re.compile(r"<\s*script[^>]*>", re.I | re.S), "script tag"),
    (re.compile(r"javascript\s*:", re.I), "javascript: URI"),
    (re.compile(r"on(?:load|error|click|mouse\w+|focus|blur|key\w+|submit|change)\s*=", re.I), "event handler"),
    (re.compile(r"<\s*(?:iframe|object|embed|applet|link|meta|base)[^>]*>", re.I | re.S), "dangerous HTML tag"),
    (re.compile(r"data:\s*text/html", re.I), "data URI HTML"),
    # Path traversal
    (re.compile(r"(?:\.{2,}[\\/]|[\\/]\.{2,})", re.S), "path traversal"),
    (re.compile(r"(?:etc/passwd|etc/shadow|windows/system32|boot\.ini)", re.I), "system path"),
    # Command injection
    (re.compile(r"[;&|`]\s*(?:rm|del|format|shutdown|reboot|halt|kill|pkill|chmod|chown)\b", re.I), "command injection"),
    (re.compile(r"(?:wget|curl)\s+https?://", re.I), "remote download"),
    (re.compile(r"(?:powershell|cmd\.exe|/bin/(?:bash|sh|zsh))\b", re.I), "shell invocation"),
    (re.compile(r"(?:nc|netcat)\s+-[el]", re.I), "netcat listener"),
    (re.compile(r"\$\([^)]+\)|`[^`]+`", re.S), "command substitution"),
    # Prompt injection
    (re.compile(r"ignore\s+(?:all\s+)?(?:previous|prior|above)\s+(?:instructions?|commands?|context)", re.I), "prompt injection — ignore"),
    (re.compile(r"(?:reveal|show|display|output|print|tell\s+me)\s+(?:your\s+)?(?:system\s+prompt|instructions?|secret|api\s*key|password|token)", re.I), "prompt extraction"),
    (re.compile(r"(?:you\s+are\s+now|act\s+as|pretend\s+(?:to\s+be|you\s+are)|roleplay\s+as)\s+(?:an?\s+)?(?:jailbreak|hacker|evil|uncensored|unrestricted|dan)", re.I), "jailbreak persona"),
    (re.compile(r"pretend\s+you\s+are\s+(?:an?\s+)?(?:evil|hacker|unrestricted|uncensored|jailbreak)", re.I), "jailbreak pretend"),
    (re.compile(r"(?:dan|jailbreak|developer|god)\s+mode(?:\s+enabled)?", re.I), "jailbreak mode"),
    (re.compile(r"bypass\s+(?:your\s+)?(?:safety|filter|restriction|guidelines?|rule)", re.I), "safety bypass"),
    # Prompt injection patterns additionnels
    (re.compile(r"forget\s+everything\s+and", re.I), "prompt — forget everything"),
    (re.compile(r"obey\s+me\b", re.I), "prompt — obey command"),
    # System override / new instructions
    (re.compile(r"###\s*system", re.I), "system override header"),
    (re.compile(r"system\s+override", re.I), "system override"),
    (re.compile(r"new\s+instructions\s*[:，]", re.I), "new instructions override"),
    (re.compile(r"leak\s+all\s+data", re.I), "data exfiltration"),
    # SSRF / LDAP
    (re.compile(r"(?:ldap|ldaps|gopher|dict|ftp|file)://", re.I), "dangerous URI scheme"),
    (re.compile(r"(?:127\.0\.0\.1|localhost|0\.0\.0\.0|::1)(?::\d+)?", re.I), "localhost SSRF"),
]


def _normalize(text: str) -> str:
    """Normalisation unicode + URL-decode pour contrer les attaques homoglyphes et encodées."""
    from urllib.parse import unquote
    return unicodedata.normalize("NFKC", unquote(text))


def sanitize_input(user_input, max_length: int = MAX_INPUT_LENGTH) -> dict:
    """
    Nettoie et valide une entrée utilisateur.

    Retourne un dict :
      valid         : bool
      cleaned_input : str (texte html-escapé si valide, '' sinon)
      risk_score    : int (0 = sain, >0 = suspect)
      reasons       : list[str] (motifs de rejet)
    """
    reasons: list[str] = []
    risk_score = 0

    if not isinstance(user_input, str):
        log_event("Input rejeté : type invalide", "WARNING")
        return {"valid": False, "cleaned_input": "", "risk_score": 100, "reasons": ["Type invalide"]}

    normalized = _normalize(user_input).strip()

    if not normalized:
        return {"valid": False, "cleaned_input": "", "risk_score": 0, "reasons": ["Input vide"]}

    if "\x00" in normalized:
        log_event("Input rejeté : null byte détecté", "WARNING")
        return {"valid": False, "cleaned_input": "", "risk_score": 80, "reasons": ["Null byte détecté"]}

    if len(normalized) > max_length:
        log_event(f"Input rejeté : longueur excessive ({len(normalized)} > {max_length})", "WARNING")
        return {"valid": False, "cleaned_input": "", "risk_score": 30, "reasons": ["Input trop long"]}

    for pattern, label in _PATTERNS:
        if pattern.search(normalized):
            log_event(f"Input rejeté : {label}", "WARNING")
            reasons.append(label)
            risk_score = max(risk_score, 80)

    if reasons:
        return {"valid": False, "cleaned_input": "", "risk_score": risk_score, "reasons": reasons}

    return {"valid": True, "cleaned_input": html.escape(normalized), "risk_score": 0, "reasons": []}


def is_valid_input(user_input: str, max_length: int = MAX_INPUT_LENGTH) -> bool:
    """Retourne True si l'entrée passe toutes les validations de sécurité."""
    return sanitize_input(user_input, max_length)["valid"]


def validate_input(user_input: str, max_length: int = MAX_INPUT_LENGTH) -> dict:
    """Alias de sanitize_input — retourne le dict complet."""
    return sanitize_input(user_input, max_length)


def get_clean_input(user_input: str, max_length: int = MAX_INPUT_LENGTH) -> str:
    """Retourne le texte nettoyé ou '' si invalide (pas d'exception)."""
    result = sanitize_input(user_input, max_length)
    return result["cleaned_input"]


def validate_field(value: str, field_name: str, max_length: int = 255, allow_html: bool = False) -> tuple[bool, str]:
    """Valide un champ individuel. Retourne (valide, message_erreur)."""
    if not isinstance(value, str):
        return False, f"{field_name}: type invalide"
    if len(value) > max_length:
        return False, f"{field_name}: trop long ({len(value)} > {max_length})"
    if not allow_html and re.search(r"<[^>]+>", value):
        return False, f"{field_name}: HTML non autorisé"
    return True, ""
