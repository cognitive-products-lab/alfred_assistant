# ============================================================
# ALFRED — src/security/mfa_manager.py
# Bloc 20.03 — Authentification & MFA
#
# 📚 NOTION EXAM :
#   D41-1 — Capsule 2 : Authentification forte — MFA pondéré multi-biométrique
#
# 🎯 UTILITÉ ALFRED :
#   Implémente un MFA pondéré (face×3, voix×2, appareil×2, PIN×1)
#   avec seuil de score configurable (défaut : ≥5).
#
# 🔐 BLOC SÉCURITÉ :
#   Zero Trust Identity — plusieurs facteurs requis simultanément (MFA)
# ============================================================

def weighted_mfa(face: bool, voice: bool, device: bool, pin: bool) -> bool:
    """MFA pondéré : valide si le score atteint le seuil."""
    score = 0

    score += 3 if face else 0
    score += 2 if voice else 0
    score += 2 if device else 0
    score += 1 if pin else 0

    return score >= 5
