"""
PROJECT      : ALFRED
BLOCK        : GLOBAL — Intégrations externes
FILE         : src/integrations/google_home_auth.py
ROLE         : Flux OAuth Device Access (Google Home / Nest) + persistance
                chiffrée du jeton

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-07-23
VERSION      : V1.0
STATUS       : DRAFT

DESCRIPTION :
Contrairement à src/integrations/google_auth.py (Calendar), le flux OAuth
Device Access ne peut pas passer par InstalledAppFlow.run_local_server() :
l'autorisation se fait via le Partner Connections Manager de Google
(nestservices.google.com/partnerconnections/{project_id}/auth), qui redirige
toujours vers https://www.google.com — une page Google, pas un serveur local
que ce module pourrait écouter. D'où un flux en deux appels explicites :
get_authorization_url() (à ouvrir dans un navigateur) puis exchange_code()
(l'utilisateur colle le "code" visible dans l'URL de redirection).

Nécessite un client OAuth de type "Application Web" (le seul type Google
acceptant https://www.google.com comme URI de redirection enregistré) —
fichier téléchargé depuis Google Cloud Console, placé à
auth/google_home_client_secret.json (PATHS.auth, jamais commité). Le JSON
d'un client Web a sa config sous la clé "web" (pas "installed" comme pour le
client Desktop de google_auth.py).

Jeton chiffré au repos via le même service Fernet que google_auth.py
(src/security/encryption_service.py), stocké séparément dans
data/security/google_home_token.json — connexions indépendantes de celle de
l'Agenda (scopes et OAuth client différents).
"""

from __future__ import annotations

import json
import logging
import urllib.error
import urllib.parse
import urllib.request

try:
    from paths import PATHS
    _CLIENT_SECRET_FILE = PATHS.auth / "google_home_client_secret.json"
    _TOKEN_FILE = PATHS.data_security / "google_home_token.json"
except Exception:
    from pathlib import Path
    _BASE = Path(__file__).resolve().parents[2]
    _CLIENT_SECRET_FILE = _BASE / "auth" / "google_home_client_secret.json"
    _TOKEN_FILE = _BASE / "data" / "security" / "google_home_token.json"

logger = logging.getLogger(__name__)

SCOPES = ["https://www.googleapis.com/auth/sdm.service"]
REDIRECT_URI = "https://www.google.com"
_AUTH_BASE = "https://nestservices.google.com/partnerconnections/{project_id}/auth"
_TOKEN_URI = "https://oauth2.googleapis.com/token"


class GoogleHomeAuthError(Exception):
    """Erreur d'authentification Device Access — message déjà en français, affichable tel quel."""


def _read_client_config() -> dict | None:
    if not _CLIENT_SECRET_FILE.exists():
        return None
    try:
        data = json.loads(_CLIENT_SECRET_FILE.read_text(encoding="utf-8"))
        return data.get("web") or data.get("installed")
    except Exception as exc:
        logger.warning("google_home_auth: lecture client secret échouée : %s", exc)
        return None


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
        logger.warning("google_home_auth: lecture jeton échouée : %s", exc)
        return None


def _write_encrypted_token(info: dict) -> None:
    from src.security.encryption_service import encrypt
    _TOKEN_FILE.parent.mkdir(parents=True, exist_ok=True)
    token = encrypt(json.dumps(info))
    _TOKEN_FILE.write_text(token, encoding="utf-8")


def get_authorization_url(project_id: str) -> dict:
    """
    Construit l'URL d'autorisation Device Access à ouvrir dans un navigateur.

    Returns:
        {"success": bool, "url": str | None, "error": str | None}
    """
    config = _read_client_config()
    if not config:
        return {
            "success": False,
            "url": None,
            "error": (
                "Identifiants Google Home absents : dépose le fichier téléchargé "
                f"depuis Google Cloud Console sous {_CLIENT_SECRET_FILE}."
            ),
        }

    params = urllib.parse.urlencode({
        "client_id": config["client_id"],
        "redirect_uri": REDIRECT_URI,
        "response_type": "code",
        "scope": " ".join(SCOPES),
        "access_type": "offline",
        "prompt": "consent",
    })
    url = f"{_AUTH_BASE.format(project_id=project_id)}?{params}"
    return {"success": True, "url": url, "error": None}


def exchange_code(code: str) -> dict:
    """
    Échange le code d'autorisation (collé par l'utilisateur depuis l'URL de
    redirection) contre un jeton d'accès, sauvegardé chiffré.

    Returns:
        {"success": bool, "error": str | None}
    """
    config = _read_client_config()
    if not config:
        return {
            "success": False,
            "error": (
                "Identifiants Google Home absents : dépose le fichier téléchargé "
                f"depuis Google Cloud Console sous {_CLIENT_SECRET_FILE}."
            ),
        }

    code = (code or "").strip()
    if not code:
        return {"success": False, "error": "Le code d'autorisation est requis."}

    body = urllib.parse.urlencode({
        "client_id": config["client_id"],
        "client_secret": config["client_secret"],
        "code": code,
        "grant_type": "authorization_code",
        "redirect_uri": REDIRECT_URI,
    }).encode("utf-8")

    req = urllib.request.Request(_TOKEN_URI, data=body, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            token_response = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="ignore")
        return {"success": False, "error": f"Échange du code refusé par Google : {detail}"}
    except urllib.error.URLError as exc:
        return {"success": False, "error": f"Connexion à Google impossible : {exc.reason}"}

    if "refresh_token" not in token_response:
        return {
            "success": False,
            "error": (
                "Google n'a pas renvoyé de jeton de rafraîchissement — réessaie "
                "le flux de connexion (le code d'autorisation ne peut servir "
                "qu'une seule fois)."
            ),
        }

    from datetime import datetime, timedelta, timezone
    expiry = datetime.now(timezone.utc) + timedelta(seconds=token_response.get("expires_in", 3600))

    info = {
        "token": token_response["access_token"],
        "refresh_token": token_response["refresh_token"],
        "token_uri": _TOKEN_URI,
        "client_id": config["client_id"],
        "client_secret": config["client_secret"],
        "scopes": SCOPES,
        "expiry": expiry.strftime("%Y-%m-%dT%H:%M:%SZ"),
    }
    _write_encrypted_token(info)
    return {"success": True, "error": None}


def is_connected() -> bool:
    """True si un jeton Google Home valide (ou rafraîchissable) est présent."""
    return get_credentials() is not None


def get_credentials():
    """
    Charge les identifiants Google Home depuis le jeton chiffré, les
    rafraîchit si expirés. Retourne None si aucun jeton ou irrécupérable.
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
            logger.warning("google_home_auth: rafraîchissement du jeton échoué : %s", exc)
            return None
    return creds if creds and creds.valid else None


def disconnect() -> None:
    """Supprime le jeton local — révoque l'accès côté ALFRED (pas côté Google)."""
    try:
        if _TOKEN_FILE.exists():
            _TOKEN_FILE.unlink()
    except Exception as exc:
        logger.error("google_home_auth: suppression du jeton échouée : %s", exc)
