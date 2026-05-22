# ============================================================
# ALFRED — src/security/security_config.py
# Bloc 20.01 — Gouvernance cybersécurité
#
# 📚 NOTION EXAM :
#   D53-2 — Capsule 8 : Séparation config/code et variables d'environnement
#
# 🎯 UTILITÉ ALFRED :
#   Centralise la lecture des paramètres de sécurité depuis .env :
#   SESSION_TIMEOUT, MAX_LOGIN_ATTEMPTS, API_HOST, APP_ENV.
#
# 🔐 BLOC SÉCURITÉ :
#   Security by Design — aucun secret en dur ; séparation stricte config/code
# ============================================================

import os
from pathlib import Path

try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = None

BASE_DIR = Path(__file__).resolve().parents[2]

if load_dotenv:
    load_dotenv(BASE_DIR / ".env")

def get_config(key: str, default=None):
    """Retourne une variable d'environnement ou une valeur par défaut."""
    return os.getenv(key, default)

APP_ENV = get_config("APP_ENV", "local")
API_HOST = get_config("API_HOST", "127.0.0.1")
SESSION_TIMEOUT = int(get_config("SESSION_TIMEOUT", 900))
MAX_LOGIN_ATTEMPTS = int(get_config("MAX_LOGIN_ATTEMPTS", 5))
