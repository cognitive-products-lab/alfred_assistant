"""
PROJECT      : ALFRED
BLOCK        : B24
FUNCTION     : 24.02 — Intégration API compagnon
FILE         : interface/companion_api.py
ROLE         : API locale consommée par le PoC Compagnon ALFRED_ANDROID
               (GET /api/status, GET /api/notifications)

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-07-13
UPDATED      : 2026-08-14 — TLS local ajouté (tools/security/generate_local_tls_cert.py)
VERSION      : V1.1
STATUS       : CODÉ — À TESTER en conditions réelles (build + émulateur/téléphone,
                cf. ALFRED_ANDROID/README.md)

DESCRIPTION :
Ré-implémentation de l'API compagnon documentée dans ALFRED_ANDROID/README.md mais
absente du dépôt (point C4-F du plan d'action du 13/07/2026). Contrat calqué
exactement sur le client Android existant :
  - CompanionApiService.kt  : GET /api/status, GET /api/notifications,
                              header Authorization envoyé par le client
  - Models.kt               : StatusResponse{product,status,timestamp},
                              Reminder{id,title,due_at,recurrent,active},
                              NotificationsResponse{notifications}
  - CompanionViewModel.kt   : authHeader = "Bearer ${token}"

Authentification : jeton statique COMPANION_API_TOKEN (.env), comparé en
temps constant (hmac.compare_digest) pour éviter une attaque par timing.
Réutilise le moteur de rappels existant (src/v3/proactive/reminder_engine.py)
comme source des notifications — aucune nouvelle collecte de données créée.

⚠️ Écoute sur 0.0.0.0 par choix : nécessaire pour être joignable depuis
l'émulateur Android (10.0.2.2) ou un téléphone physique sur le même réseau
Wi-Fi local. Ne jamais exposer ce port au-delà du réseau local (jeton
statique — cf. limites documentées dans ALFRED_ANDROID/README.md).

TLS : si data/security/certs/companion_api/{server.crt,server.key} existent
(générés par tools/security/generate_local_tls_cert.py), le serveur démarre
en HTTPS. Sinon, avertissement explicite et démarrage en HTTP (pas de
régression silencieuse pour un poste où le certificat n'a pas encore été
généré). Le certificat est auto-signé et local — le client ALFRED_ANDROID
doit embarquer le .crt correspondant comme ancre de confiance
(network_security_config.xml) pour que la connexion aboutisse. JWT reste
hors scope de ce durcissement (cf. docs/mobilite/vision_mobilite_v2.md).

USAGE :
    python interface/companion_api.py
    (ou start_companion_api.bat sous Windows)
"""

from __future__ import annotations

import hmac
import os
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, Header, HTTPException

ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / ".env")

COMPANION_API_HOST = "0.0.0.0"
COMPANION_API_PORT = 8420

TLS_CERT_PATH = ROOT / "data" / "security" / "certs" / "companion_api" / "server.crt"
TLS_KEY_PATH = ROOT / "data" / "security" / "certs" / "companion_api" / "server.key"


def _tls_kwargs() -> dict:
    """Active HTTPS si le certificat local existe, sinon retombe sur HTTP (avec avertissement)."""
    if TLS_CERT_PATH.exists() and TLS_KEY_PATH.exists():
        return {"ssl_certfile": str(TLS_CERT_PATH), "ssl_keyfile": str(TLS_KEY_PATH)}
    print(
        "[ALFRED] ATTENTION : certificat TLS local introuvable "
        f"({TLS_CERT_PATH}) — démarrage en HTTP non chiffré. "
        "Générer avec : python tools/security/generate_local_tls_cert.py"
    )
    return {}

app = FastAPI(title="ALFRED Companion API", version="1.0.0")


def _expected_token() -> str:
    token = os.getenv("COMPANION_API_TOKEN", "")
    if not token:
        raise RuntimeError(
            "COMPANION_API_TOKEN manquant dans .env — générer avec : "
            "python -c \"import secrets; print(secrets.token_hex(32))\""
        )
    return token


def _require_token(authorization: str | None) -> None:
    expected = f"Bearer {_expected_token()}"
    if not authorization or not hmac.compare_digest(authorization, expected):
        raise HTTPException(status_code=401, detail="Jeton invalide ou manquant")


@app.get("/api/status")
def get_status(authorization: str | None = Header(default=None)) -> dict:
    _require_token(authorization)
    return {
        "product": "ALFRED",
        "status": "running",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.get("/api/notifications")
def get_notifications(authorization: str | None = Header(default=None)) -> dict:
    _require_token(authorization)
    from src.v3.proactive.reminder_engine import ReminderEngine

    engine = ReminderEngine()
    reminders = engine.get_active()
    return {
        "notifications": [
            {
                "id": r.id,
                "title": r.title,
                "due_at": r.due_at,
                "recurrent": r.recurrent,
                "active": r.active,
            }
            for r in reminders
        ]
    }


if __name__ == "__main__":
    import uvicorn

    _expected_token()  # échoue tôt et clairement si le jeton n'est pas configuré
    tls_kwargs = _tls_kwargs()
    scheme = "https" if tls_kwargs else "http"
    print(f"[ALFRED] API compagnon sur {scheme}://{COMPANION_API_HOST}:{COMPANION_API_PORT}")
    print(f"[ALFRED] Emulateur Android : {scheme}://10.0.2.2:8420")
    uvicorn.run(app, host=COMPANION_API_HOST, port=COMPANION_API_PORT, **tls_kwargs)
