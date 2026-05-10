SUSPICIOUS_KEYWORDS = [
    "DROP TABLE",
    "UNION SELECT",
    "<script>",
    "../",
    "rm -rf",
    "powershell -enc",
    "ignore previous instructions",
    "reveal your secrets",
    "show api key",
]

def detect_threat(input_text: str) -> dict:
    """Détecte des motifs de menace simples dans une entrée texte."""
    score = 0
    reasons = []

    if len(input_text) > 1000:
        score += 2
        reasons.append("Input trop long")

    for keyword in SUSPICIOUS_KEYWORDS:
        if keyword.lower() in input_text.lower():
            score += 3
            reasons.append(f"Motif suspect : {keyword}")

    return {
        "is_threat": score >= 3,
        "score": score,
        "reasons": reasons,
    }
