"""
════════════════════════════════════════════════════════════
PROJECT      : ALFRED
BLOCK        : B20
FUNCTION     : 20.06
FILE         : encryption_service.py
ROLE         : Service de chiffrement symétrique AES/Fernet

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-05-23
UPDATED      : 2026-05-23
VERSION      : V1.0
STATUS       : ACTIVE

DESCRIPTION :
Chiffrement et déchiffrement local via Fernet. Clé lue depuis .env (FERNET_KEY).
════════════════════════════════════════════════════════════
"""
"""
encryption_service.py
Service de chiffrement local pour ALFRED.

Utilise Fernet (cryptography) — chiffrement symétrique AES-128-CBC.
La clé est stockée dans .env (FERNET_KEY) ou générée automatiquement.

Pré-requis :
    pip install cryptography
"""

import os
from pathlib import Path

from src.security.security_logger import log_event

try:
    from cryptography.fernet import Fernet, InvalidToken
except ImportError:
    Fernet = None
    InvalidToken = Exception
    log_event("cryptography non installé — chiffrement désactivé", "WARNING")

try:
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).resolve().parents[2] / ".env")
except ImportError:
    pass

# ─────────────────────────────────────────────────────────
# Clé de chiffrement
# ─────────────────────────────────────────────────────────

_KEY_FILE = Path(__file__).resolve().parents[2] / "data" / "security" / "fernet.key"


def _load_or_generate_key() -> bytes:
    """
    Priorité 1 : FERNET_KEY dans l'env — aucun fichier disque écrit ou lu (ISO 27001 A.10.2).
    Priorité 2 : fichier local (fallback legacy / dev sans .env).
    Priorité 3 : génération + persistance sur disque uniquement si pas d'env var.
    """
    # Priorité 1 : variable d'environnement (pas de fichier disque)
    env_key = os.getenv("FERNET_KEY")
    if env_key:
        return env_key.encode()

    # Priorité 2 : fichier local (mode sans .env)
    if _KEY_FILE.exists():
        return _KEY_FILE.read_bytes().strip()

    # Priorité 3 : génération + persistance uniquement si pas d'env var
    if Fernet is None:
        log_event("Impossible de générer une clé : cryptography absent", "ERROR")
        return b""

    new_key = Fernet.generate_key()
    _KEY_FILE.parent.mkdir(parents=True, exist_ok=True)
    _KEY_FILE.write_bytes(new_key)
    log_event(
        "Clé Fernet générée sur disque. Déplacer vers FERNET_KEY=... dans .env puis supprimer ce fichier.",
        "WARNING",
    )
    return new_key


_FERNET_KEY = _load_or_generate_key()
_cipher = Fernet(_FERNET_KEY) if (Fernet and _FERNET_KEY) else None


# ─────────────────────────────────────────────────────────
# API publique
# ─────────────────────────────────────────────────────────

def encrypt(data: str) -> str:
    """
    Chiffre une chaîne de texte.
    Retourne le token chiffré en str (base64 URL-safe).
    """
    if _cipher is None:
        log_event("Chiffrement impossible : cipher non initialisé", "ERROR")
        return data  # fallback non chiffré

    try:
        token = _cipher.encrypt(data.encode("utf-8"))
        return token.decode("utf-8")
    except Exception as e:
        log_event(f"Erreur chiffrement : {e}", "ERROR")
        return data


def decrypt(token: str) -> str:
    """
    Déchiffre un token Fernet.
    Retourne la chaîne originale ou "" si invalide.
    """
    if _cipher is None:
        log_event("Déchiffrement impossible : cipher non initialisé", "ERROR")
        return ""

    try:
        data = _cipher.decrypt(token.encode("utf-8"))
        return data.decode("utf-8")
    except InvalidToken:
        log_event("Token invalide ou corrompu", "WARNING")
        return ""
    except Exception as e:
        log_event(f"Erreur déchiffrement : {e}", "ERROR")
        return ""


def is_available() -> bool:
    """Indique si le chiffrement est opérationnel."""
    return _cipher is not None


def rotate_key() -> str:
    """
    Génère une nouvelle clé et la persiste.
    ATTENTION : les données chiffrées avec l'ancienne clé
    ne seront plus lisibles. À utiliser avec précaution.
    Retourne la nouvelle clé en str.
    """
    if Fernet is None:
        log_event("Rotation impossible : cryptography absent", "ERROR")
        return ""

    new_key = Fernet.generate_key()
    _KEY_FILE.parent.mkdir(parents=True, exist_ok=True)
    _KEY_FILE.write_bytes(new_key)
    log_event("Clé Fernet renouvelée — données précédentes inaccessibles", "CRITICAL")
    return new_key.decode("utf-8")


# ─────────────────────────────────────────────────────────
# Test standalone
# ─────────────────────────────────────────────────────────
if __name__ == "__main__":
    print(f"Chiffrement disponible : {is_available()}")

    if is_available():
        message = "données sensibles test"
        token = encrypt(message)
        print(f"Chiffré  : {token[:40]}...")
        result = decrypt(token)
        print(f"Déchiffré : {result}")
        print(f"OK : {result == message}")

