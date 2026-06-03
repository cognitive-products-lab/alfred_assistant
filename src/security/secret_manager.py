# ============================================================
# ALFRED — src/security/secret_manager.py
# Bloc 20.05 — Chiffrement & protection des données
#
# 📚 NOTION EXAM :
#   D53-1 — Capsule 5 : Chiffrement, gestion des secrets et protection des données
#
# 🎯 UTILITÉ ALFRED :
#   Lecture sécurisée des secrets critiques (.env) — clés Fernet, PIN salt,
#   clé applicative. Garantit qu'aucune valeur par défaut n'est acceptée.
#
# 🔐 BLOC SÉCURITÉ / DOMAINE :
#   Chiffrement & protection des données (20.05)
# ============================================================

import os
from src.security.security_logger import log_event


def get_secret(key: str) -> str:
    """
    RÃ©cupÃ¨re un secret depuis les variables d'environnement.
    LÃ¨ve une erreur si absent â€” jamais de valeur par dÃ©faut pour les secrets.

    Args:
        key : Nom de la variable d'environnement

    Returns:
        La valeur du secret

    Raises:
        ValueError : Si le secret est absent
    """
    value = os.getenv(key)
    if not value:
        log_event(f"Secret manquant : {key}", "CRITICAL")
        raise ValueError(f"Secret manquant dans .env : {key}")
    return value


def secret_exists(key: str) -> bool:
    """VÃ©rifie si un secret est dÃ©fini sans le lever."""
    return bool(os.getenv(key))


def summarize_secrets() -> dict:
    """
    Retourne un résumé public des secrets requis (présence uniquement, jamais les valeurs).
    Utilisé par le dashboard de sécurité.

    Returns:
        dict : {
            "required_count": int,
            "present_count": int,
            "missing_count": int,
            "all_ok": bool,
            "validation": { "Clé principale": "OK"|"MANQUANT", ... }
        }
    """
    required = ["SECRET_KEY", "FERNET_KEY", "PIN_SALT"]
    labels = {
        "SECRET_KEY":  "Clé principale",
        "FERNET_KEY":  "Clé chiffrement",
        "PIN_SALT":    "Sel authentification",
    }
    validation = {}
    present_count = 0

    for key in required:
        present = bool(os.getenv(key))
        validation[labels[key]] = "OK" if present else "MANQUANT"
        if present:
            present_count += 1

    missing = len(required) - present_count
    return {
        "required_count": len(required),
        "present_count":  present_count,
        "missing_count":  missing,
        "all_ok":         missing == 0,
        "validation":     validation,
    }


def validate_env_secrets() -> dict:
    """
    VÃ©rifie que tous les secrets critiques sont prÃ©sents.
    AppelÃ© au dÃ©marrage d'ALFRED.

    Returns:
        dict avec statut de chaque secret requis
    """
    required = ["SECRET_KEY", "FERNET_KEY", "PIN_SALT"]
    result = {}
    all_ok = True

    for key in required:
        present = secret_exists(key)
        result[key] = "OK" if present else "MANQUANT"
        if not present:
            all_ok = False
            log_event(f"Secret requis absent au dÃ©marrage : {key}", "CRITICAL")

    if all_ok:
        log_event("Tous les secrets critiques sont prÃ©sents", "INFO")

    return result
