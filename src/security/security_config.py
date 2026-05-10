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
