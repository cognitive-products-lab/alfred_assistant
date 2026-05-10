from src.security.threat_detector import detect_threat
from src.security.security_logger import log_event

def guard_prompt(prompt: str) -> bool:
    """Bloque les prompts suspects avant envoi à un module IA."""
    threat = detect_threat(prompt)

    if threat["is_threat"]:
        log_event(f"Prompt bloqué : {threat['reasons']}", "WARNING")
        return False

    return True
