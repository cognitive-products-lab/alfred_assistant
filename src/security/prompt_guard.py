# ============================================================
# ALFRED — src/security/prompt_guard.py
# Bloc 20.08 — Détection d'intrusion
#
# 📚 NOTION EXAM :
#   D42-2 — Capsule 6 : AI Security — défense contre le prompt injection
#
# 🎯 UTILITÉ ALFRED :
#   Filtre les prompts avant envoi aux modules IA ; bloque toute
#   tentative de manipulation ou de détournement du modèle.
#
# 🔐 BLOC SÉCURITÉ :
#   Prompt Injection Defense — dernière barrière de sécurité avant le LLM
# ============================================================

from src.security.threat_detector import detect_threat
from src.security.security_logger import log_event

def guard_prompt(prompt: str) -> bool:
    """Bloque les prompts suspects avant envoi à un module IA."""
    threat = detect_threat(prompt)

    if threat["is_threat"]:
        log_event(f"Prompt bloqué : {threat['reasons']}", "WARNING")
        return False

    return True
