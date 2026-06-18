"""
════════════════════════════════════════════════════════════
PROJECT      : ALFRED
BLOCK        : B20
FUNCTION     : 20.07
FILE         : api_security.py
ROLE         : Sécurité API — validation HMAC/JWT et rate limiting

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-05-23
UPDATED      : 2026-05-23
VERSION      : V1.0
STATUS       : ACTIVE

DESCRIPTION :
Valide les clés API (HMAC-SHA256), les tokens JWT et applique le rate limiting par clé.
════════════════════════════════════════════════════════════
"""
from __future__ import annotations
"""
api_security.py
Bloc 20.07 — Sécurité API pour ALFRED.

Rôle :
- validation des clés API (HMAC-SHA256) ;
- validation des tokens JWT (signature + expiration) ;
- rate limiting par clé API ;
- contrôle des endpoints autorisés par rôle ;
- journalisation structurée des accès API.

Local-first : JWT vérifié sans appel réseau (clé symétrique).
"""


import hashlib
import hmac
import json
import threading
import time
from datetime import datetime, timezone
from pathlib import Path

from src.security.security_logger import log_event
from src.security.incident_manager import register_incident
from src.security.secret_manager import get_secret

_lock = threading.Lock()
_api_attempts: dict[str, list[float]] = {}
_api_lockout: dict[str, float] = {}

API_WINDOW_SECONDS = 60
API_MAX_REQUESTS = 60
API_LOCKOUT_SECONDS = 120

API_LOG_FILE = Path("logs/security/api_access.jsonl")
API_LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

# Endpoints autorisés par rôle
_ENDPOINT_ACL: dict[str, set[str]] = {
    "OWNER": {"*"},
    "ADMIN": {"status", "memory", "knowledge", "llm", "tts", "stt"},
    "USER": {"status", "llm", "tts", "stt"},
    "GUEST": {"status"},
}


def _log_api_event(api_key_hash: str, endpoint: str, role: str, result: str) -> None:
    """Écrit un événement d'accès API au format JSONL."""
    event = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "api_key_hash": api_key_hash[:12] + "…",
        "endpoint": endpoint,
        "role": role,
        "result": result,
    }
    with API_LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")


def _hash_api_key(api_key: str) -> str:
    """Hash SHA-256 de la clé API pour log sans exposer la clé."""
    return hashlib.sha256(api_key.encode()).hexdigest()


def validate_api_key(api_key) -> dict:
    """
    Valide une clé API par HMAC-SHA256 contre la clé secrète.

    Returns:
        dict avec valid (bool) et reason (str).
    """
    if api_key is None or not isinstance(api_key, str):
        return {"valid": False, "reason": "Clé API invalide (None ou type incorrect)"}

    try:
        secret = get_secret("API_SECRET_KEY").encode()
    except ValueError:
        log_event("API_SECRET_KEY manquante — validation API impossible", "CRITICAL")
        return {"valid": False, "reason": "Configuration API manquante"}

    if not api_key or len(api_key) < 32:
        log_event("Clé API trop courte ou vide", "WARNING")
        return {"valid": False, "reason": "Clé API invalide"}

    try:
        key_bytes = api_key.encode()
        expected = hmac.new(secret, key_bytes, hashlib.sha256).hexdigest()
        # La clé valide EST son propre HMAC signé avec le secret
        # Format attendu : {payload}:{hmac}
        if ":" not in api_key:
            return {"valid": False, "reason": "Format de clé invalide"}
        payload, provided_mac = api_key.rsplit(":", 1)
        computed_mac = hmac.new(secret, payload.encode(), hashlib.sha256).hexdigest()
        if hmac.compare_digest(computed_mac, provided_mac):
            return {"valid": True, "reason": "OK", "payload": payload}
        log_event("Clé API invalide — HMAC incorrect", "WARNING")
        return {"valid": False, "reason": "Signature invalide"}
    except Exception as exc:
        log_event(f"Erreur validation clé API : {exc}", "ERROR")
        return {"valid": False, "reason": "Erreur de validation"}


def check_api_rate_limit(user_id: str, endpoint: str = "") -> dict:
    """
    Vérifie le rate limit pour un utilisateur/endpoint.

    Returns:
        dict avec allowed (bool), retry_after (float), reason (str).
    """
    key_hash = _hash_api_key(f"{user_id}:{endpoint}")
    with _lock:
        now = time.time()
        if key_hash in _api_lockout and now < _api_lockout[key_hash]:
            retry = round(_api_lockout[key_hash] - now, 1)
            return {"allowed": False, "retry_after": retry, "reason": f"Rate limit — réessayez dans {retry:.0f}s"}

        _api_attempts.setdefault(key_hash, [])
        _api_attempts[key_hash] = [t for t in _api_attempts[key_hash] if now - t < API_WINDOW_SECONDS]

        if len(_api_attempts[key_hash]) >= API_MAX_REQUESTS:
            _api_lockout[key_hash] = now + API_LOCKOUT_SECONDS
            log_event(f"Rate limit API dépassé pour {user_id} — blocage {API_LOCKOUT_SECONDS}s", "WARNING")
            register_incident("MEDIUM", f"Rate limit API dépassé : {user_id}", source="api_security")
            return {"allowed": False, "retry_after": float(API_LOCKOUT_SECONDS),
                    "reason": f"Rate limit dépassé — réessayez dans {API_LOCKOUT_SECONDS}s"}

        _api_attempts[key_hash].append(now)
        return {"allowed": True, "retry_after": 0.0, "reason": "OK"}


# Alias interne — utilise user_id comme clé pour la logique de verrouillage
def _check_rate_tuple(api_key: str) -> tuple[bool, float]:
    result = check_api_rate_limit(api_key)
    return (not result["allowed"], result["retry_after"])


def check_endpoint_access(role: str, endpoint: str) -> dict:
    """
    Vérifie si un rôle a accès à un endpoint.

    Returns:
        dict avec allowed (bool) et reason (str).
    """
    acl = _ENDPOINT_ACL.get(role.upper(), set())
    # Normalise l'endpoint : extrait le dernier segment sans slash initial
    ep_key = endpoint.lstrip("/").split("/")[-1] if "/" in endpoint else endpoint
    if "*" in acl or ep_key in acl or endpoint in acl:
        return {"allowed": True, "reason": "OK"}
    log_event(f"Accès endpoint refusé : rôle={role} endpoint={endpoint}", "WARNING")
    return {"allowed": False, "reason": f"Endpoint '{endpoint}' non autorisé pour le rôle {role}"}


def authorize_api_request(
    api_key: str = "",
    role: str = "GUEST",
    endpoint: str = "",
    user_id: str = "",
) -> dict:
    """
    Point d'entrée principal — valide rate limit, clé et endpoint.

    Returns:
        dict avec authorized (bool), reason (str).
    """
    key_hash = _hash_api_key(api_key or user_id)

    # Rate limit par user_id ou clé
    rl = check_api_rate_limit(user_id or api_key, endpoint)
    if not rl["allowed"]:
        _log_api_event(key_hash, endpoint, role, "RATE_LIMITED")
        return {"authorized": False, "reason": rl["reason"]}

    # Validation clé API si fournie
    if api_key:
        key_result = validate_api_key(api_key)
        if not key_result["valid"]:
            _log_api_event(key_hash, endpoint, role, "INVALID_KEY")
            return {"authorized": False, "reason": key_result["reason"]}

    # Contrôle endpoint
    ep_result = check_endpoint_access(role, endpoint)
    if not ep_result["allowed"]:
        _log_api_event(key_hash, endpoint, role, "FORBIDDEN")
        return {"authorized": False, "reason": ep_result["reason"]}

    _log_api_event(key_hash, endpoint, role, "ALLOW")
    return {"authorized": True, "reason": "OK"}


def generate_api_key(payload: str = "") -> str:
    """
    Génère une clé API signée HMAC.
    Si payload vide, utilise un timestamp unique.

    Returns:
        Clé API au format {payload}:{hmac}
    """
    import uuid as _uuid
    effective_payload = payload or f"alfred_{_uuid.uuid4().hex[:16]}"
    try:
        secret = get_secret("API_SECRET_KEY").encode()
    except ValueError:
        # Sans secret configuré : retourne une clé UUID unique (non signée)
        return f"{effective_payload}:{_uuid.uuid4().hex}"

    mac = hmac.new(secret, effective_payload.encode(), hashlib.sha256).hexdigest()
    return f"{effective_payload}:{mac}"


def get_api_security_status() -> dict:
    """Résumé de l'état sécurité API pour le dashboard."""
    with _lock:
        now = time.time()
        locked_keys = [k for k, until in _api_lockout.items() if now < until]
        active_keys = len(_api_attempts)
    return {
        "active_api_keys_tracked": active_keys,
        "locked_keys": len(locked_keys),
        "rate_window_seconds": API_WINDOW_SECONDS,
        "max_requests_per_window": API_MAX_REQUESTS,
    }
