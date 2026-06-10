"""
════════════════════════════════════════════════════════════
PROJECT      : ALFRED
BLOCK        : B20
FUNCTION     : 20.13
FILE         : policy_enforcement_point.py
ROLE         : PEP — Point d'application des politiques (Zero Trust)

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-05-23
UPDATED      : 2026-05-23
VERSION      : V1.0
STATUS       : ACTIVE

DESCRIPTION :
Applique la décision du PDP. Dernier verrou avant exécution d'une action.
════════════════════════════════════════════════════════════
"""
"""
policy_enforcement_point.py
PEP — Policy Enforcement Point pour ALFRED.

Applique la décision du PDP (Policy Decision Point).
Dans l'architecture Zero Trust :
    PDP (decide_access) → décide
    PEP (enforce_decision) → applique

Le PEP est le dernier verrou avant l'exécution d'une action.
"""

from src.security.security_logger import log_event

# ─────────────────────────────────────────────────────────
# Décisions reconnues
# ─────────────────────────────────────────────────────────

_ALLOW_DECISIONS  = {"ALLOW"}
_DENY_DECISIONS   = {
    "DENY", "DENY_INPUT", "DENY_THREAT", "DENY_DEVICE",
    "DENY_PERMISSION", "DENY_POLICY", "DENY_RISK", "DENY_MFA",
}
_REVIEW_DECISIONS = {"REVIEW", "PENDING"}


# ─────────────────────────────────────────────────────────
# API publique
# ─────────────────────────────────────────────────────────

def enforce_decision(decision: str) -> bool:
    """
    Applique une décision de politique d'accès.

    Args:
        decision : résultat du PDP ("ALLOW", "DENY", etc.)

    Returns:
        True si l'accès est autorisé, False sinon.
    """
    decision_upper = decision.upper() if decision else "DENY"

    if decision_upper in _ALLOW_DECISIONS:
        log_event(f"PEP : accès autorisé ({decision_upper})")
        return True

    if decision_upper in _DENY_DECISIONS:
        log_event(f"PEP : accès refusé ({decision_upper})", "WARNING")
        return False

    if decision_upper in _REVIEW_DECISIONS:
        log_event(f"PEP : décision en attente de revue ({decision_upper})", "WARNING")
        return False

    # Décision inconnue → refus par défaut (fail-secure)
    log_event(f"PEP : décision inconnue '{decision}' — refus par défaut", "ERROR")
    return False


def enforce_or_raise(decision: str) -> None:
    """
    Applique la décision et lève une exception si refus.
    Utile pour les contextes où un refus doit interrompre le flux.

    Raises:
        PermissionError : si l'accès est refusé
    """
    if not enforce_decision(decision):
        raise PermissionError(f"Accès refusé par le PEP : {decision}")


def explain_decision(decision: str) -> str:
    """
    Retourne une explication lisible de la décision.
    Utile pour les logs et les messages d'erreur utilisateur.
    """
    explanations = {
        "ALLOW":            "Accès autorisé.",
        "DENY":             "Accès refusé par la politique.",
        "DENY_INPUT":       "Entrée invalide ou vide.",
        "DENY_THREAT":      "Menace détectée dans la requête.",
        "DENY_DEVICE":      "Appareil non reconnu ou non approuvé.",
        "DENY_PERMISSION":  "Permission insuffisante pour ce rôle.",
        "DENY_POLICY":      "Accès refusé — sensibilité de la ressource trop élevée pour ce rôle.",
        "DENY_RISK":        "Accès refusé — score de risque trop élevé.",
        "DENY_MFA":         "Authentification multi-facteurs requise et non vérifiée.",
        "REVIEW":           "Décision en attente de revue manuelle.",
        "PENDING":          "Décision non encore rendue.",
    }
    return explanations.get(
        decision.upper() if decision else "",
        f"Décision non reconnue : {decision}"
    )


# ─────────────────────────────────────────────────────────
# Test standalone
# ─────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=== Test Policy Enforcement Point ===\n")

    for decision in ["ALLOW", "DENY", "DENY_THREAT", "DENY_DEVICE", "REVIEW", "UNKNOWN"]:
        result = enforce_decision(decision)
        expl   = explain_decision(decision)
        print(f"  {decision:20} → autorisé={result} | {expl}")
