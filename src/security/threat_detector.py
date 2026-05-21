SUSPICIOUS_KEYWORDS = [
    # SQL
    "DROP TABLE", "UNION SELECT", "OR 1=1", "EXEC(",
    "SELECT * FROM", "UPDATE users", "DELETE FROM",
    "xp_cmdshell", "'--", "' OR '", "'; EXEC",
    # XSS
    "<script>", "javascript:", "onerror=", "onload=",
    # Path traversal
    "../", "..\\", "etc/passwd",
    # Command injection
    "rm -rf", "powershell", "cmd.exe", "; wget ", "; curl ",
    # Prompt injection
    "ignore previous instructions", "reveal your secrets",
    "show api key", "bypass safety", "jailbreak mode",
    "you are now", "act as", "dan mode",
    "bypass your safety", "pretend you are an evil",
    # LDAP / SSRF
    "ldap://", "gopher://", "127.0.0.1",
]


def detect_threat(input_text: str) -> dict:
    """Détecte des motifs de menace dans une entrée texte."""
    score = 0
    reasons: list[str] = []
    lower = input_text.lower()

    if len(input_text) > 1000:
        score += 2
        reasons.append("Input trop long")

    # Null bytes — très suspect
    if "\x00" in input_text:
        score += 5
        reasons.append("Null byte détecté")

    # Caractères non-ASCII excessifs (tentative d'encodage)
    special_count = sum(1 for c in input_text if ord(c) > 127 and not c.isalpha())
    if special_count > 20:
        score += 2
        reasons.append(f"Caractères suspects excessifs ({special_count})")

    for keyword in SUSPICIOUS_KEYWORDS:
        if keyword.lower() in lower:
            score += 3
            reasons.append(f"Motif suspect : {keyword}")

    return {
        "is_threat": score >= 3,
        "score": score,
        "reasons": reasons,
    }
