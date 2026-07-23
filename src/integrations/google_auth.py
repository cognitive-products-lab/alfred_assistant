"""
PROJECT      : ALFRED
BLOCK        : GLOBAL — Intégrations externes
FILE         : src/integrations/google_auth.py
ROLE         : Flux OAuth desktop Google + persistance chiffrée du jeton

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-07-23
VERSION      : V1.0
STATUS       : DRAFT

DESCRIPTION :
Deuxième appel réseau réellement externe du pipeline ALFRED après la météo
(cf. src/integrations/weather_client.py) — mais celui-ci porte sur des
données personnelles (agenda), donc gardé derrière un consentement explicite
(src/ui/google_calendar_prefs.py, pas ici : ce module ne connaît que l'OAuth,
pas le consentement) et un jeton chiffré au repos (Fernet, même service que
le reste du projet — src/security/encryption_service.py).

Nécessite un fichier d'identifiants client OAuth "Application de bureau"
téléchargé depuis Google Cloud Console, placé à auth/google_client_secret.json
(PATHS.auth, jamais commité — voir .gitignore). Sans ce fichier, is_connected()
reste False et start_auth_flow() échoue proprement (message FR explicite) :
ce module ne peut pas créer les identifiants à la place de l'utilisateur.

Le flux utilise InstalledAppFlow.run_local_server() de google-auth-oauthlib,
qui gère lui-même un serveur HTTP local éphémère pour le callback OAuth —
pas de réutilisation du serveur FastAPI d'interface/companion_api.py, dont le
cycle de vie (process séparé, port fixe 8420) ne convient pas à un callback
one-shot bloquant.
"""

from __future__ import annotations

import json
import logging

try:
    from paths import PATHS
    _CLIENT_SECRET_FILE = PATHS.auth / "google_client_secret.json"
    _TOKEN_FILE = PATHS.data_security / "google_calendar_token.json"
except Exception:
    from pathlib import Path
    _BASE = Path(__file__).resolve().parents[2]
    _CLIENT_SECRET_FILE = _BASE / "auth" / "google_client_secret.json"
    _TOKEN_FILE = _BASE / "data" / "security" / "google_calendar_token.json"

logger = logging.getLogger(__name__)

SCOPES = [
    "https://www.googleapis.com/auth/calendar",
    "https://www.googleapis.com/auth/calendar.events",
]


class GoogleAuthError(Exception):
    """Erreur d'authentification Google — message déjà en français, affichable tel quel."""


def _read_encrypted_token() -> dict | None:
    if not _TOKEN_FILE.exists():
        return None
    try:
        from src.security.encryption_service import decrypt
        raw = decrypt(_TOKEN_FILE.read_text(encoding="utf-8"))
        if not raw:
            return None
        return json.loads(raw)
    except Exception as exc:
        logger.warning("google_auth: lecture jeton échouée : %s", exc)
        return None


def _write_encrypted_token(info: dict) -> None:
    from src.security.encryption_service import encrypt
    _TOKEN_FILE.parent.mkdir(parents=True, exist_ok=True)
    token = encrypt(json.dumps(info))
    _TOKEN_FILE.write_text(token, encoding="utf-8")


def is_connected() -> bool:
    """True si un jeton Google valide (ou rafraîchissable) est présent."""
    return get_credentials() is not None


def get_credentials():
    """
    Charge les identifiants Google depuis le jeton chiffré, les rafraîchit
    si expirés. Retourne None si aucun jeton (pas encore connecté) ou si le
    jeton est irrécupérable (ex. accès révoqué côté Google).
    """
    info = _read_encrypted_token()
    if not info:
        return None

    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials

    creds = Credentials.from_authorized_user_info(info, SCOPES)
    if creds and creds.expired and creds.refresh_token:
        try:
            creds.refresh(Request())
            _write_encrypted_token(json.loads(creds.to_json()))
        except Exception as exc:
            logger.warning("google_auth: rafraîchissement du jeton échoué : %s", exc)
            return None
    return creds if creds and creds.valid else None


def start_auth_flow() -> dict:
    """
    Lance le flux OAuth desktop (ouvre le navigateur système, bloquant
    jusqu'à autorisation ou fermeture par l'utilisateur).

    Returns:
        {"success": bool, "error": str | None}
    """
    if not _CLIENT_SECRET_FILE.exists():
        return {
            "success": False,
            "error": (
                "Identifiants Google absents : dépose le fichier téléchargé "
                f"depuis Google Cloud Console sous {_CLIENT_SECRET_FILE}."
            ),
        }

    try:
        from google_auth_oauthlib.flow import InstalledAppFlow

        flow = InstalledAppFlow.from_client_secrets_file(str(_CLIENT_SECRET_FILE), SCOPES)
        creds = flow.run_local_server(port=0)
        _write_encrypted_token(json.loads(creds.to_json()))
        return {"success": True, "error": None}
    except Exception as exc:
        logger.error("google_auth: échec du flux OAuth : %s", exc)
        return {"success": False, "error": f"Connexion Google échouée : {exc}"}


def disconnect() -> None:
    """Supprime le jeton local — révoque l'accès côté ALFRED (pas côté Google)."""
    try:
        if _TOKEN_FILE.exists():
            _TOKEN_FILE.unlink()
    except Exception as exc:
        logger.error("google_auth: suppression du jeton échouée : %s", exc)
