"""
════════════════════════════════════════════════════════════
PROJECT      : ALFRED
BLOCK        : B20
FUNCTION     : 20.14
FILE         : prompt_guard.py
ROLE         : Filtrage des prompts suspects avant envoi à l'IA

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-05-23
UPDATED      : 2026-05-23
VERSION      : V1.0
STATUS       : ACTIVE

DESCRIPTION :
Bloque les prompts contenant des patterns de menace détectés par le ThreatDetector.
════════════════════════════════════════════════════════════
"""
from src.security.threat_detector import detect_threat
from src.security.security_logger import log_event

def guard_prompt(prompt: str) -> dict:
    """
    Analyse un prompt et retourne un rapport de garde.
    dict : allowed, action, severity, reasons, threat_score
    """
    threat = detect_threat(prompt)
    allowed = not threat["is_threat"]

    if not allowed:
        log_event(f"Prompt bloqué : {threat['reasons']}", "WARNING")

    severity = "LOW" if allowed else ("HIGH" if threat.get("threat_score", 0) >= 70 else "MEDIUM")

    return {
        "allowed": allowed,
        "action": "ALLOW" if allowed else "BLOCK",
        "severity": severity,
        "reasons": threat.get("reasons", []),
        "score": threat.get("score", threat.get("threat_score", 0)),
        "threat_score": threat.get("threat_score", threat.get("score", 0)),
        "threat_types": threat.get("threat_types", []),
    }


def is_prompt_allowed(prompt: str) -> bool:
    """Retourne True si le prompt est autorisé."""
    return guard_prompt(prompt)["allowed"]


def explain_prompt_guard(prompt: str) -> str:
    """Retourne une explication textuelle du résultat de guard_prompt."""
    result = guard_prompt(prompt)
    if result["allowed"]:
        return "Prompt autorisé."
    reasons = ", ".join(result["reasons"]) or "pattern suspect"
    return f"Prompt bloqué. Raisons : {reasons}."
