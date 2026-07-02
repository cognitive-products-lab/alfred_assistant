"""
PROJECT      : ALFRED
BLOCK        : Client compagnon Android (PoC)
FILE         : interface/companion_api.py
ROLE         : API locale FastAPI consommée par l'app Android compagnon —
               statut ALFRED + rappels actifs, en lecture seule.

DEPENDENCIES : fastapi, uvicorn

SÉCURITÉ :
Local-first — écoute sur 127.0.0.1 par défaut. Authentification par jeton
partagé (COMPANION_API_TOKEN dans .env), même logique que le reste du
Bloc 20 (pas d'accès anonyme aux données ALFRED), journalisée via
src.security.security_logger.

Lancement :
    python interface/companion_api.py
    (ou start_companion_api.bat)
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime, timezone

from dotenv import load_dotenv
from fastapi import FastAPI, Header, HTTPException

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from paths import PATHS
from src.security.security_logger import log_event

load_dotenv()

COMPANION_API_TOKEN = os.environ.get("COMPANION_API_TOKEN")
COMPANION_API_PORT = int(os.environ.get("COMPANION_API_PORT", "8420"))

app = FastAPI(title="ALFRED Companion API", version="0.1.0")


def _check_token(authorization: str | None) -> None:
    if not COMPANION_API_TOKEN:
        raise HTTPException(status_code=503, detail="COMPANION_API_TOKEN non configuré")
    expected = f"Bearer {COMPANION_API_TOKEN}"
    if authorization != expected:
        log_event("companion_api: tentative d'accès avec jeton invalide", level="WARNING")
        raise HTTPException(status_code=401, detail="Jeton invalide")


@app.get("/api/status")
def get_status(authorization: str | None = Header(default=None)):
    _check_token(authorization)
    return {
        "product": "ALFRED",
        "status": "online",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.get("/api/notifications")
def get_notifications(authorization: str | None = Header(default=None)):
    _check_token(authorization)
    reminders_path = PATHS.data_memory / "reminders.json"
    try:
        with open(reminders_path, encoding="utf-8") as f:
            reminders = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        reminders = []

    active = [r for r in reminders if r.get("active")]
    active.sort(key=lambda r: r.get("due_at", ""))
    return {"notifications": active}


if __name__ == "__main__":
    import uvicorn

    log_event("companion_api: démarrage sur 127.0.0.1", level="INFO")
    uvicorn.run(app, host="127.0.0.1", port=COMPANION_API_PORT)
