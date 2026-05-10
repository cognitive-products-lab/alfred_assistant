# ============================================================
# ALFRED â€” src/security/secret_manager.py
# Bloc 20.06 â€” Chiffrement / Gestion secrets
# Lecture sÃ©curisÃ©e des secrets depuis .env
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
