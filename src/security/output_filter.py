# ============================================================
# ALFRED — src/security/output_filter.py
# Bloc 20.05 — Chiffrement & protection des données
#
# 📚 NOTION EXAM :
#   D42-2 — Capsule 6 : Prévention des fuites de données (DLP)
#
# 🎯 UTILITÉ ALFRED :
#   Masque automatiquement les données sensibles dans les réponses
#   avant de les transmettre à l'utilisateur (clés, secrets, mots de passe).
#
# 🔐 BLOC SÉCURITÉ :
#   DLP (Data Loss Prevention) — aucun secret ou variable critique n'est exposé
# ============================================================

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
