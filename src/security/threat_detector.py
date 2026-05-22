# ============================================================
# ALFRED — src/security/threat_detector.py
# Bloc 20.08 — Détection d'intrusion
#
# 📚 NOTION EXAM :
#   D42-1 — Capsule 5 : Détection de menaces et scoring d'entrées suspectes
#
# 🎯 UTILITÉ ALFRED :
#   Analyse un texte d'entrée et calcule un score de menace
#   basé sur des mots-clés suspects (injections, XSS, prompt attacks).
#
# 🔐 BLOC SÉCURITÉ :
#   Détection d'intrusion (IDS) — barrière préventive avant le pipeline IA
# ============================================================

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
