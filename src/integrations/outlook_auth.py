# ============================================================
# ALFRED — src/integrations/outlook_auth.py
# BLOC GLOBAL — Intégrations externes
# ROLE : Flux OAuth desktop Microsoft (MSAL) + persistance chiffrée du jeton
#
# Même rôle que google_auth.py pour Google Agenda, adapté à Microsoft Graph :
# application "publique" (mobile & desktop) enregistrée dans Azure AD/Entra ID
# — contrairement à Google, aucun client secret n'est nécessaire pour ce type
# d'application. Le cache de jetons MSAL (SerializableTokenCache) est chiffré
# au repos avec le même service Fernet que le reste du projet
# (src/security/encryption_service.py).
#
# Nécessite un fichier de config avec le client_id Azure, placé à
# auth/outlook_client_config.json (PATHS.auth, jamais commité — voir
# .gitignore). Format attendu : {"client_id": "...", "tenant": "common"}
# ("common" accepte les comptes Microsoft personnels ET professionnels —
# suffisant pour un compte Outlook.com personnel, pas besoin du tenant ID
# réel sauf usage professionnel spécifique).
# ============================================================

from __future__ import annotations

import json
import logging

try:
    from paths import PATHS
    _CLIENT_CONFIG_FILE = PATHS.auth / "outlook_client_config.json"
    _TOKEN_CACHE_FILE = PATHS.data_security / "outlook_calendar_token.json"
except Exception:
    from pathlib import Path
    _BASE = Path(__file__).resolve().parents[2]
    _CLIENT_CONFIG_FILE = _BASE / "auth" / "outlook_client_config.json"
    _TOKEN_CACHE_FILE = _BASE / "data" / "security" / "outlook_calendar_token.json"

logger = logging.getLogger(__name__)

SCOPES = ["Calendars.ReadWrite"]


class OutlookAuthError(Exception):
    """Erreur d'authentification Outlook — message déjà en français, affichable tel quel."""


def _load_client_config() -> dict | None:
    if not _CLIENT_CONFIG_FILE.exists():
        return None
    try:
        return json.loads(_CLIENT_CONFIG_FILE.read_text(encoding="utf-8"))
    except Exception as exc:
        logger.warning("outlook_auth: lecture config client échouée : %s", exc)
        return None


def _read_token_cache_blob() -> str | None:
    if not _TOKEN_CACHE_FILE.exists():
        return None
    try:
        from src.security.encryption_service import decrypt
        raw = decrypt(_TOKEN_CACHE_FILE.read_text(encoding="utf-8"))
        return raw or None
    except Exception as exc:
        logger.warning("outlook_auth: lecture jeton échouée : %s", exc)
        return None


def _write_token_cache_blob(blob: str) -> None:
    from src.security.encryption_service import encrypt
    _TOKEN_CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
    _TOKEN_CACHE_FILE.write_text(encrypt(blob), encoding="utf-8")


def _build_app():
    """Retourne (msal.PublicClientApplication, SerializableTokenCache) ou
    (None, None) si la config Azure (client_id) n'existe pas encore."""
    config = _load_client_config()
    if not config or not config.get("client_id"):
        return None, None

    import msal

    cache = msal.SerializableTokenCache()
    existing = _read_token_cache_blob()
    if existing:
        try:
            cache.deserialize(existing)
        except Exception as exc:
            logger.warning("outlook_auth: cache jeton corrompu, ignoré : %s", exc)

    tenant = config.get("tenant", "common")
    app = msal.PublicClientApplication(
        config["client_id"],
        authority=f"https://login.microsoftonline.com/{tenant}",
        token_cache=cache,
    )
    return app, cache


def _persist_cache_if_changed(cache) -> None:
    if cache is not None and cache.has_state_changed:
        _write_token_cache_blob(cache.serialize())


def is_connected() -> bool:
    """True si un jeton Microsoft valide (ou rafraîchissable) est présent."""
    return get_credentials() is not None


def get_credentials() -> str | None:
    """
    Charge le compte Microsoft depuis le cache de jetons chiffré et
    rafraîchit silencieusement l'access token si besoin (équivalent de
    google_auth.get_credentials(), mais MSAL retourne directement une
    chaîne access_token plutôt qu'un objet Credentials — outlook_calendar_client.py
    l'utilise tel quel dans l'en-tête Authorization).

    Returns:
        L'access token (str), ou None si pas connecté / jeton irrécupérable.
    """
    app, cache = _build_app()
    if not app:
        return None

    accounts = app.get_accounts()
    if not accounts:
        return None

    try:
        result = app.acquire_token_silent(SCOPES, account=accounts[0])
    except Exception as exc:
        logger.warning("outlook_auth: rafraîchissement du jeton échoué : %s", exc)
        return None
    finally:
        _persist_cache_if_changed(cache)

    if not result or "access_token" not in result:
        return None
    return result["access_token"]


def start_auth_flow() -> dict:
    """
    Lance le flux OAuth desktop (ouvre le navigateur système, bloquant
    jusqu'à autorisation ou fermeture par l'utilisateur).

    Returns:
        {"success": bool, "error": str | None}
    """
    if not _CLIENT_CONFIG_FILE.exists():
        return {
            "success": False,
            "error": (
                "Configuration Outlook absente : dépose le fichier de "
                f"config Azure sous {_CLIENT_CONFIG_FILE}."
            ),
        }

    app, cache = _build_app()
    if not app:
        return {
            "success": False,
            "error": f"Configuration Outlook invalide dans {_CLIENT_CONFIG_FILE} (client_id manquant).",
        }

    try:
        result = app.acquire_token_interactive(scopes=SCOPES)
        _persist_cache_if_changed(cache)
        if not result or "access_token" not in result:
            error_desc = (result or {}).get("error_description", "raison inconnue")
            return {"success": False, "error": f"Connexion Outlook échouée : {error_desc}"}
        return {"success": True, "error": None}
    except Exception as exc:
        logger.error("outlook_auth: échec du flux OAuth : %s", exc)
        return {"success": False, "error": f"Connexion Outlook échouée : {exc}"}


def disconnect() -> None:
    """Supprime le cache de jetons local — révoque l'accès côté ALFRED (pas côté Microsoft)."""
    try:
        if _TOKEN_CACHE_FILE.exists():
            _TOKEN_CACHE_FILE.unlink()
    except Exception as exc:
        logger.error("outlook_auth: suppression du jeton échouée : %s", exc)
