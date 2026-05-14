"""
PROJECT      : ALFRED
BLOCK        : B20
FUNCTION     : XX.XX
FILE         : mfa_manager.py
ROLE         : Authentification multi-facteurs pondérée (face/voice/device/pin)

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-05-10
P26-05-12
VERSION      : V1.0
STATUS       : STABLE

DESCRIPTION :
Évalue l'authentification MFA pondérée (face=3, voice=2, device=2, pin=1) avec seuil configurable.
"""

from datetime import datetime, timezone
from typing import Dict, Any

from src.security.security_logger import log_event


MFA_WEIGHTS = {
    "face": 3,
    "voice": 2,
    "device": 2,
    "pin": 1,
}

DEFAULT_MFA_THRESHOLD = 5


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def calculate_mfa_score(
    face: bool = False,
    voice: bool = False,
    device: bool = False,
    pin: bool = False,
) -> int:
    """Calcule le score MFA pondéré. Score max = 8."""
    score = 0
    score += MFA_WEIGHTS["face"] if face else 0
    score += MFA_WEIGHTS["voice"] if voice else 0
    score += MFA_WEIGHTS["device"] if device else 0
    score += MFA_WEIGHTS["pin"] if pin else 0
    return score


def evaluate_mfa(
    face: bool = False,
    voice: bool = False,
    device: bool = False,
    pin: bool = False,
    threshold: int = DEFAULT_MFA_THRESHOLD,
    user_id: str = "unknown_user",
    request_id: str = "",
) -> Dict[str, Any]:
    """
    Évalue une authentification MFA.

    Returns:
        dict: {"authenticated": bool, "score": int, "threshold": int,
               "factors": dict, "missing_factors": list[str], "timestamp": str}
    """
    factors = {
        "face": bool(face),
        "voice": bool(voice),
        "device": bool(device),
        "pin": bool(pin),
    }

    score = calculate_mfa_score(**factors)
    authenticated = score >= threshold

    missing_factors = [factor for factor, enabled in factors.items() if not enabled]

    result = {
        "authenticated": authenticated,
        "score": score,
        "threshold": threshold,
        "factors": factors,
        "missing_factors": missing_factors,
        "user_id": user_id,
        "request_id": request_id,
        "timestamp": _now(),
    }

    log_event(
        f"MFA user={user_id} request_id={request_id} "
        f"score={score}/{threshold} authenticated={authenticated}",
        "INFO" if authenticated else "WARNING",
    )

    return result


def weighted_mfa(face: bool, voice: bool, device: bool, pin: bool) -> bool:
    """Compatibilité historique. Valide si le score atteint le seuil par défaut."""
    return evaluate_mfa(face=face, voice=voice, device=device, pin=pin)["authenticated"]


def explain_mfa_result(result: Dict[str, Any]) -> str:
    """Retourne une explication lisible du résultat MFA."""
    if result.get("authenticated"):
        return f"MFA validé : score {result.get('score')} sur {result.get('threshold')}."

    missing = ", ".join(result.get("missing_factors", [])) or "aucun détail"
    return (
        f"MFA refusé : score {result.get('score')} sur {result.get('threshold')}. "
        f"Facteurs manquants : {missing}."
    )
