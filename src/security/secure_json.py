"""
════════════════════════════════════════════════════════════
PROJECT      : ALFRED
BLOCK        : B20
FUNCTION     : 20.15
FILE         : secure_json.py
ROLE         : Lecture/écriture JSON chiffrée au repos (fichier entier, Fernet)

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-10-05
VERSION      : V1.0
STATUS       : ACTIVE

DESCRIPTION :
Chiffre l'intégralité d'un fichier JSON sensible (profil santé art. 9,
profils utilisateurs, foyer) dans une enveloppe JSON :
    {"_alfred_encrypted": "fernet-v1", "payload": "gAAAA..."}
L'enveloppe reste un JSON valide (les outils génériques ne plantent pas)
mais ne révèle aucun contenu.

Règles fail-closed :
- save_json(..., encrypt=True) lève une erreur plutôt que d'écrire en clair.
- load_json lève SecureJsonError si l'enveloppe est indéchiffrable — jamais
  de profil vide silencieux qui pourrait ensuite être réécrit par-dessus.
- encrypt=None (défaut) : chiffre si le chemin est déclaré sensible
  (SENSITIVE_FILES) ou si le fichier existant est déjà chiffré — un fichier
  chiffré ne redevient jamais clair par simple réécriture.

Limite assumée : la clé (FERNET_KEY) vit dans .env sur le même poste.
Protège contre la fuite des fichiers (git, copies, sauvegardes, synchro
cloud), pas contre une compromission de la session Windows.
════════════════════════════════════════════════════════════
"""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from src.security.encryption_service import decrypt_strict, encrypt_strict

ENVELOPE_KEY = "_alfred_encrypted"
ENVELOPE_VERSION = "fernet-v1"

_ROOT = Path(__file__).resolve().parents[2]

# Fichiers qui doivent toujours être chiffrés au repos (chemins relatifs à la racine).
SENSITIVE_FILES: tuple[str, ...] = (
    "data/health/health_celine.json",
    "data/users/instances/user_celine_instance.json",
    "private_data/user_profiles/celine_profile.json",
    "private_data/user_profiles/seb_profile.json",
    "private_data/user_profiles/household_relationships.json",
    "private_data/user_profiles/celine_food_preferences.json",
    "private_data/user_profiles/seb_food_preferences.json",
)


class SecureJsonError(RuntimeError):
    """Fichier chiffré illisible (clé absente/différente, contenu corrompu)."""


def is_encrypted_envelope(obj: Any) -> bool:
    return isinstance(obj, dict) and obj.get(ENVELOPE_KEY) == ENVELOPE_VERSION and "payload" in obj


def is_sensitive_path(path: str | Path) -> bool:
    p = Path(path).resolve()
    if p.parent.name == "health" and p.name.startswith("health_"):
        return True
    return any(p == (_ROOT / rel).resolve() for rel in SENSITIVE_FILES)


def is_encrypted_file(path: str | Path) -> bool:
    p = Path(path)
    if not p.exists():
        return False
    try:
        return is_encrypted_envelope(json.loads(p.read_text(encoding="utf-8")))
    except (json.JSONDecodeError, OSError):
        return False


def load_json(path: str | Path) -> Any:
    """Lit un JSON, chiffré ou non. Lève FileNotFoundError / json.JSONDecodeError / SecureJsonError."""
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    if not is_encrypted_envelope(raw):
        return raw
    try:
        return json.loads(decrypt_strict(raw["payload"]))
    except RuntimeError as exc:
        raise SecureJsonError(f"{path} : {exc}") from exc


def save_json(path: str | Path, data: Any, encrypt: bool | None = None, indent: int = 2) -> None:
    """Écrit un JSON de façon atomique ; chiffré selon `encrypt` (voir règles du module)."""
    p = Path(path)
    if encrypt is None:
        encrypt = is_sensitive_path(p) or is_encrypted_file(p)
    text = json.dumps(data, indent=indent, ensure_ascii=False)
    if encrypt:
        envelope = {ENVELOPE_KEY: ENVELOPE_VERSION, "payload": encrypt_strict(text)}
        text = json.dumps(envelope, indent=2)
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_name(p.name + ".tmp")
    tmp.write_text(text, encoding="utf-8")
    os.replace(tmp, p)


def encrypt_file_in_place(path: str | Path) -> str:
    """Migration : chiffre un fichier clair existant. Retourne 'encrypted', 'already' ou 'missing'."""
    p = Path(path)
    if not p.exists():
        return "missing"
    if is_encrypted_file(p):
        return "already"
    data = load_json(p)
    save_json(p, data, encrypt=True)
    if load_json(p) != data:  # relecture de contrôle avant de considérer la migration faite
        raise SecureJsonError(f"{p} : vérification après chiffrement échouée")
    return "encrypted"
