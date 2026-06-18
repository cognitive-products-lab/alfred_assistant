"""
════════════════════════════════════════════════════════════
PROJECT      : ALFRED
BLOCK        : B20
FUNCTION     : 20.11
FILE         : mfa_manager.py
ROLE         : Authentification multi-facteurs TOTP (RFC 6238)

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-05-23
UPDATED      : 2026-05-23
VERSION      : V1.0
STATUS       : ACTIVE

DESCRIPTION :
Setup TOTP, vérification token, cache session MFA avec TTL et calcul de score MFA.
════════════════════════════════════════════════════════════
"""
from __future__ import annotations
"""
mfa_manager.py
Gestionnaire MFA (Multi-Factor Authentication) — Bloc 20.

Implémente TOTP (RFC 6238) via pyotp.
Secrets chiffrés Fernet au repos.
Vérification cachée par session avec TTL.

Architecture :
  1. setup_totp(user_id)              → génère secret TOTP, retourne URI pour QR code
  2. verify_totp(user_id, token)      → vérifie le code à 6 chiffres
  3. mark_verified(user_id, session_id) → cache la vérification en session
  4. is_verified(user_id, session_id)   → vérifie si MFA valide pour la session
  5. is_mfa_required(role)            → consulte roles_permissions.json
"""


import json
import threading
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any

try:
    import pyotp
    _PYOTP_AVAILABLE = True
except ImportError:
    _PYOTP_AVAILABLE = False

from src.security.security_logger import log_event, log_auth
from src.security.data_protection import protect_field, expose_field

# ─── Configuration ────────────────────────────────────────────────────────────

_ROOT         = Path(__file__).resolve().parents[2]
_SECRETS_FILE = _ROOT / "data" / "security" / "mfa_secrets.json"
_ROLES_FILE   = _ROOT / "config" / "security" / "roles_permissions.json"
_SETTINGS_FILE = _ROOT / "config" / "security" / "security_settings.json"

_APP_NAME    = "ALFRED"
_TOTP_WINDOW = 1       # tolérance ±1 intervalle de 30s
_DEFAULT_TTL = 3600    # durée de vie MFA en session (secondes)

# Cache en mémoire : {user_id: {session_id: expires_at}}
_verified_sessions: dict[str, dict[str, datetime]] = {}
_lock = threading.Lock()


# ─── Persistance secrets ──────────────────────────────────────────────────────

def _load_secrets() -> dict[str, str]:
    if not _SECRETS_FILE.exists():
        return {}
    try:
        raw = json.loads(_SECRETS_FILE.read_text(encoding="utf-8"))
        return {uid: expose_field(secret) for uid, secret in raw.items()}
    except Exception:
        return {}


def _save_secrets(secrets: dict[str, str]) -> None:
    _SECRETS_FILE.parent.mkdir(parents=True, exist_ok=True)
    encrypted = {uid: protect_field(secret) for uid, secret in secrets.items()}
    _SECRETS_FILE.write_text(
        json.dumps(encrypted, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    log_event("mfa_manager: secrets MFA mis à jour")


# ─── Configuration rôles ─────────────────────────────────────────────────────

def _load_role_config(role: str) -> dict[str, Any]:
    if not _ROLES_FILE.exists():
        return {}
    try:
        data = json.loads(_ROLES_FILE.read_text(encoding="utf-8"))
        return data.get("roles", {}).get(role.upper(), {})
    except Exception:
        return {}


def _global_mfa_required() -> bool:
    if not _SETTINGS_FILE.exists():
        return False
    try:
        data = json.loads(_SETTINGS_FILE.read_text(encoding="utf-8"))
        return bool(
            data.get("authentication", {}).get("mfa_required", False)
            or data.get("mfa_required", False)
        )
    except Exception:
        return False


# ─── API publique ─────────────────────────────────────────────────────────────

# Rôles qui exigent toujours le MFA — indépendant de la config globale.
# Principe Zero Trust : privilège élevé = authentification forte systématique.
_ALWAYS_MFA_ROLES: frozenset[str] = frozenset({"OWNER", "ADMIN"})

# Rôles exemptés du MFA même si la config globale l'exige.
# GUEST = utilisateur public non authentifié (pas de TOTP possible).
# EMERGENCY = accès de crise (MFA bloquerait la réponse rapide).
_NO_MFA_ROLES: frozenset[str] = frozenset({"GUEST", "EMERGENCY"})


def is_mfa_required(role: str) -> bool:
    """
    Retourne True si le MFA est requis pour ce rôle.

    Priorité :
      1. Rôles exemptés (GUEST, EMERGENCY) — toujours False.
      2. Rôles à MFA systématique (OWNER, ADMIN) — toujours True.
      3. Flag MFA global activé dans security_settings.json — True pour tous les autres.
      4. Config spécifique du rôle dans roles_permissions.json.
    """
    role_upper = role.upper()
    if role_upper in _NO_MFA_ROLES:
        return False          # GUEST et EMERGENCY n'ont jamais de TOTP
    if role_upper in _ALWAYS_MFA_ROLES:
        return True
    if _global_mfa_required():
        return True
    return bool(_load_role_config(role).get("mfa_required", False))


def has_mfa_setup(user_id: str) -> bool:
    """Retourne True si un secret TOTP est enregistré pour cet utilisateur."""
    return user_id in _load_secrets()


def setup_totp(user_id: str, force: bool = False) -> dict[str, str]:
    """
    Génère un secret TOTP pour l'utilisateur et le stocke chiffré.

    Returns:
        {
          "secret": str,            # secret base32 (à conserver)
          "provisioning_uri": str,  # URI pour QR code (otpauth://)
          "manual_entry": str,      # code formaté pour saisie manuelle
        }
    """
    if not _PYOTP_AVAILABLE:
        return {"error": "pyotp non installé — pip install pyotp"}

    secrets = _load_secrets()
    if user_id in secrets and not force:
        secret = secrets[user_id]
    else:
        secret = pyotp.random_base32()
        secrets[user_id] = secret
        _save_secrets(secrets)
        log_auth(user_id, "MFA_SETUP", True)

    totp = pyotp.TOTP(secret)
    uri  = totp.provisioning_uri(name=user_id, issuer_name=_APP_NAME)
    formatted = "-".join(secret[i:i+4] for i in range(0, min(len(secret), 16), 4))

    return {
        "secret": secret,
        "provisioning_uri": uri,
        "manual_entry": formatted,
    }


def verify_totp(user_id: str, token: str) -> bool:
    """
    Vérifie un code TOTP à 6 chiffres.

    Returns:
        True si le token est valide, False sinon.
    """
    if not _PYOTP_AVAILABLE:
        return False

    secret = _load_secrets().get(user_id)
    if not secret:
        log_auth(user_id, "MFA_VERIFY", False)
        return False

    valid = pyotp.TOTP(secret).verify(str(token).strip(), valid_window=_TOTP_WINDOW)
    log_auth(user_id, "MFA_VERIFY", valid)
    return valid


def mark_verified(user_id: str, session_id: str, ttl_seconds: int | None = None) -> None:
    """Marque le MFA comme vérifié pour cette session (TTL en mémoire)."""
    ttl = ttl_seconds or _DEFAULT_TTL
    expires_at = datetime.now(timezone.utc) + timedelta(seconds=ttl)
    with _lock:
        if user_id not in _verified_sessions:
            _verified_sessions[user_id] = {}
        _verified_sessions[user_id][session_id] = expires_at
    log_event(f"mfa_manager: MFA vérifié — user={user_id} session={session_id[:8]}…")


def is_verified(user_id: str, session_id: str) -> bool:
    """Retourne True si le MFA a été vérifié pour cette session et n'a pas expiré."""
    with _lock:
        expires_at = _verified_sessions.get(user_id, {}).get(session_id)
    if not expires_at:
        return False
    if datetime.now(timezone.utc) > expires_at:
        revoke(user_id, session_id)
        return False
    return True


def revoke(user_id: str, session_id: str) -> None:
    """Révoque la vérification MFA d'une session."""
    with _lock:
        _verified_sessions.get(user_id, {}).pop(session_id, None)
    log_event(f"mfa_manager: MFA révoqué — user={user_id} session={session_id[:8]}…")


def revoke_all(user_id: str) -> None:
    """Révoque toutes les sessions MFA d'un utilisateur."""
    with _lock:
        _verified_sessions.pop(user_id, None)
    log_event(f"mfa_manager: toutes sessions MFA révoquées — user={user_id}")


def get_status(user_id: str) -> dict[str, Any]:
    """Retourne l'état MFA complet d'un utilisateur."""
    with _lock:
        active = len(_verified_sessions.get(user_id, {}))
    return {
        "user_id": user_id,
        "totp_configured": has_mfa_setup(user_id),
        "active_mfa_sessions": active,
        "pyotp_available": _PYOTP_AVAILABLE,
    }


_ROLE_WEIGHTS = {"OWNER": 30, "ADMIN": 20, "USER": 10, "TRUSTED_USER": 15,
                 "SERVICE": 10, "AI_MODULE": 5, "GUEST": 0, "EMERGENCY": 5}
_TOTP_BONUS   = 20
_DEVICE_BONUS = 30
_BASE_SCORE   = 20


def _calculate_mfa_score_v1(
    user_id: str,
    role: str,
    device_id: str,
    device_trusted: bool,
    totp_verified: bool = False,
) -> dict[str, Any]:
    """Score MFA pondéré V1 (0-100) par combinaison user/role/device — usage interne."""
    role_pts   = _ROLE_WEIGHTS.get(role.upper(), 0)
    device_pts = _DEVICE_BONUS if device_trusted else 0
    totp_pts   = _TOTP_BONUS if (totp_verified or is_verified(user_id, device_id)) else 0
    totp_setup = _TOTP_BONUS // 2 if has_mfa_setup(user_id) and not totp_pts else 0
    raw = _BASE_SCORE + role_pts + device_pts + totp_pts + totp_setup
    score = min(100, raw)
    return {
        "score": score,
        "factors": {
            "base": _BASE_SCORE,
            "role": role_pts,
            "device_trusted": device_pts,
            "totp_verified": totp_pts,
            "totp_setup": totp_setup,
        },
    }


def _evaluate_mfa_session(user_id: str, role: str, session_id: str) -> dict[str, Any]:
    """Évalue l'état MFA TOTP pour user/role/session — usage interne."""
    required = is_mfa_required(role)
    verified = is_verified(user_id, session_id)
    return {"required": required, "verified": verified, "passes": (not required) or verified}


# ── API publique attendue par les tests ────────────────────────────────────────
# Poids par facteur biométrique : face=3, voice=2, device=2, pin=1 → max=8
_MFA_WEIGHTS = {"face": 3, "voice": 2, "device": 2, "pin": 1}
_MFA_DEFAULT_THRESHOLD = 5


def calculate_mfa_score(
    face: bool = False,
    voice: bool = False,
    device: bool = False,
    pin: bool = False,
    # Paramètres V1 legacy (pour compatibilité pentest_auth)
    user_id: str = "",
    role: str = "",
    device_id: str = "",
    device_trusted: bool = False,
    totp_verified: bool = False,
) -> "int | dict":
    """
    Calcule un score MFA.
    - Si appelé avec user_id/role/device_id/device_trusted → API V1 (retourne dict)
    - Sinon → API V2 biométrique (retourne int)
    """
    if user_id or role or device_id or device_trusted or totp_verified:
        return _calculate_mfa_score_v1(user_id, role, device_id, device_trusted, totp_verified)
    return (
        (_MFA_WEIGHTS["face"] if face else 0)
        + (_MFA_WEIGHTS["voice"] if voice else 0)
        + (_MFA_WEIGHTS["device"] if device else 0)
        + (_MFA_WEIGHTS["pin"] if pin else 0)
    )


def evaluate_mfa(
    face: bool = False,
    voice: bool = False,
    device: bool = False,
    pin: bool = False,
    threshold: int = _MFA_DEFAULT_THRESHOLD,
    user_id: str = "",
    request_id: str = "",
) -> dict[str, Any]:
    """
    Évalue l'authentification multi-facteur.

    Returns:
        authenticated, score, threshold, user_id, missing_factors
    """
    score = calculate_mfa_score(face=face, voice=voice, device=device, pin=pin)
    authenticated = score >= threshold
    missing: list[str] = []
    for factor in ("face", "voice", "device", "pin"):
        if not locals()[factor]:
            missing.append(factor)
    return {
        "authenticated": authenticated,
        "score": score,
        "threshold": threshold,
        "user_id": user_id,
        "request_id": request_id,
        "missing_factors": missing,
    }


def weighted_mfa(
    face: bool = False,
    voice: bool = False,
    device: bool = False,
    pin: bool = False,
    threshold: int = _MFA_DEFAULT_THRESHOLD,
) -> bool:
    """Retourne True si le score MFA multi-facteur atteint le seuil."""
    return calculate_mfa_score(face=face, voice=voice, device=device, pin=pin) >= threshold


def explain_mfa_result(result: dict) -> str:
    """Génère une explication textuelle d'un résultat evaluate_mfa."""
    if result.get("authenticated"):
        return f"MFA validé — score {result['score']}/{result['threshold']} requis."
    missing = ", ".join(result.get("missing_factors", []))
    return (
        f"MFA refusé — score {result['score']}/{result['threshold']} requis. "
        f"Facteurs manquants : {missing or 'N/A'}."
    )


# ─── Standalone ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=== Test MFA Manager ===\n")

    info = setup_totp("demo_user", force=True)
    print(f"Secret     : {info['manual_entry']}")
    print(f"URI        : {info['provisioning_uri'][:70]}…\n")

    token = pyotp.TOTP(info["secret"]).now()
    print(f"Token TOTP : {token}")
    ok = verify_totp("demo_user", token)
    print(f"Vérif TOTP : {'✓ OK' if ok else '✗ ECHEC'}\n")

    mark_verified("demo_user", "session_demo_abc", ttl_seconds=60)
    print(f"Vérifié    : {is_verified('demo_user', 'session_demo_abc')}")
    revoke("demo_user", "session_demo_abc")
    print(f"Après révoc: {is_verified('demo_user', 'session_demo_abc')}")
    print(f"\nStatut     : {get_status('demo_user')}")
