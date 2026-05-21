"""
migrate_encrypt_data.py
Migration rétroactive — chiffrement Fernet des données sensibles existantes.

Fichiers migrés :
  data/security/pins.json              hash + salt de chaque utilisateur
  data/users/instances/*.json          champs PII (preferred_name, context)
  data/memory/episodic/dialogue_history.json  contenu user + alfred
  data/context/user_context.json       localisation

Usage :
  python tools/migrate_encrypt_data.py
  python tools/migrate_encrypt_data.py --dry-run   (aperçu sans écriture)
  python tools/migrate_encrypt_data.py --validate  (vérifie les fichiers déjà chiffrés)
"""

from __future__ import annotations

import json
import sys
import shutil
import argparse
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

try:
    from dotenv import load_dotenv
    load_dotenv(ROOT / ".env")
except ImportError:
    pass

from src.security.data_protection import (
    protect_nested, expose_nested,
    PINS_FIELDS, DIALOGUE_FIELDS, PROFILE_PII_FIELDS, CONTEXT_FIELDS,
    is_available,
)
from src.security.encryption_service import encrypt, decrypt

# ─── Couleurs terminal ────────────────────────────────────────────────────────
GREEN  = "\033[92m"
RED    = "\033[91m"
YELLOW = "\033[93m"
CYAN   = "\033[96m"
BOLD   = "\033[1m"
RESET  = "\033[0m"

BACKUP_DIR = ROOT / "data" / "_backups_pre_encryption"


# ─── Utilitaires ─────────────────────────────────────────────────────────────

def _ts() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")


def backup_file(path: Path) -> Path:
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    dest = BACKUP_DIR / f"{path.stem}_{_ts()}{path.suffix}"
    shutil.copy2(path, dest)
    return dest


def load_raw(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save_json(path: Path, data) -> None:
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def _looks_encrypted(value: str) -> bool:
    """Détecte si une valeur ressemble à un token Fernet (base64url, ~100+ chars)."""
    return isinstance(value, str) and len(value) > 80 and value.startswith("g")


def _count_fields(data, fields: frozenset) -> int:
    """Compte les champs sensibles (non encore chiffrés) dans une structure."""
    count = 0
    if isinstance(data, dict):
        for k, v in data.items():
            if k.lower() in fields and isinstance(v, str) and v and not _looks_encrypted(v):
                count += 1
            elif isinstance(v, (dict, list)):
                count += _count_fields(v, fields)
    elif isinstance(data, list):
        for item in data:
            count += _count_fields(item, fields)
    return count


def _validate_roundtrip(original, encrypted, fields: frozenset) -> bool:
    """Vérifie que déchiffrer l'encrypté redonne l'original."""
    decrypted = expose_nested(encrypted, fields)
    return json.dumps(decrypted, sort_keys=True) == json.dumps(original, sort_keys=True)


# ─── Migrations par fichier ───────────────────────────────────────────────────

def migrate_pins(dry_run: bool) -> dict:
    path = ROOT / "data" / "security" / "pins.json"
    result = {"file": str(path.relative_to(ROOT)), "fields": list(PINS_FIELDS)}

    if not path.exists():
        result["status"] = "SKIP"
        result["reason"] = "fichier inexistant"
        return result

    raw = load_raw(path)
    plain_count = _count_fields(raw, PINS_FIELDS)

    if plain_count == 0:
        result["status"] = "ALREADY_ENCRYPTED"
        result["records"] = len(raw)
        return result

    if not dry_run:
        bak = backup_file(path)
        encrypted = protect_nested(raw, PINS_FIELDS)
        if not _validate_roundtrip(raw, encrypted, PINS_FIELDS):
            result["status"] = "ERROR"
            result["reason"] = "round-trip validation échouée"
            return result
        save_json(path, encrypted)
        result["backup"] = str(bak.relative_to(ROOT))

    result["status"] = "OK" if not dry_run else "DRY_RUN"
    result["records"] = len(raw)
    result["fields_encrypted"] = plain_count
    return result


def migrate_user_instances(dry_run: bool) -> list[dict]:
    instances_dir = ROOT / "data" / "users" / "instances"
    results = []

    if not instances_dir.exists():
        return [{"file": str(instances_dir.relative_to(ROOT)), "status": "SKIP", "reason": "dossier inexistant"}]

    for path in instances_dir.glob("*.json"):
        result = {"file": str(path.relative_to(ROOT)), "fields": list(PROFILE_PII_FIELDS)}
        raw = load_raw(path)
        plain_count = _count_fields(raw, PROFILE_PII_FIELDS)

        if plain_count == 0:
            result["status"] = "ALREADY_ENCRYPTED"
            results.append(result)
            continue

        if not dry_run:
            bak = backup_file(path)
            encrypted = protect_nested(raw, PROFILE_PII_FIELDS)
            if not _validate_roundtrip(raw, encrypted, PROFILE_PII_FIELDS):
                result["status"] = "ERROR"
                result["reason"] = "round-trip validation échouée"
                results.append(result)
                continue
            save_json(path, encrypted)
            result["backup"] = str(bak.relative_to(ROOT))

        result["status"] = "OK" if not dry_run else "DRY_RUN"
        result["fields_encrypted"] = plain_count
        results.append(result)

    return results


def migrate_dialogue_history(dry_run: bool) -> dict:
    path = ROOT / "data" / "memory" / "episodic" / "dialogue_history.json"
    result = {"file": str(path.relative_to(ROOT)), "fields": list(DIALOGUE_FIELDS)}

    if not path.exists():
        result["status"] = "SKIP"
        result["reason"] = "fichier inexistant"
        return result

    raw = load_raw(path)
    if not isinstance(raw, list):
        result["status"] = "SKIP"
        result["reason"] = "format inattendu (non-liste)"
        return result

    plain_count = _count_fields(raw, DIALOGUE_FIELDS)

    if plain_count == 0:
        result["status"] = "ALREADY_ENCRYPTED"
        result["records"] = len(raw)
        return result

    if not dry_run:
        bak = backup_file(path)
        encrypted = protect_nested(raw, DIALOGUE_FIELDS)
        if not _validate_roundtrip(raw, encrypted, DIALOGUE_FIELDS):
            result["status"] = "ERROR"
            result["reason"] = "round-trip validation échouée"
            return result
        save_json(path, encrypted)
        result["backup"] = str(bak.relative_to(ROOT))

    result["status"] = "OK" if not dry_run else "DRY_RUN"
    result["records"] = len(raw)
    result["fields_encrypted"] = plain_count
    return result


def migrate_user_context(dry_run: bool) -> dict:
    path = ROOT / "data" / "context" / "user_context.json"
    result = {"file": str(path.relative_to(ROOT)), "fields": list(CONTEXT_FIELDS)}

    if not path.exists():
        result["status"] = "SKIP"
        result["reason"] = "fichier inexistant"
        return result

    raw = load_raw(path)
    plain_count = _count_fields(raw, CONTEXT_FIELDS)

    if plain_count == 0:
        result["status"] = "ALREADY_ENCRYPTED"
        return result

    if not dry_run:
        bak = backup_file(path)
        encrypted = protect_nested(raw, CONTEXT_FIELDS)
        if not _validate_roundtrip(raw, encrypted, CONTEXT_FIELDS):
            result["status"] = "ERROR"
            result["reason"] = "round-trip validation échouée"
            return result
        save_json(path, encrypted)
        result["backup"] = str(bak.relative_to(ROOT))

    result["status"] = "OK" if not dry_run else "DRY_RUN"
    result["fields_encrypted"] = plain_count
    return result


# ─── Validation post-migration ────────────────────────────────────────────────

def validate_file(path: Path, fields: frozenset, label: str) -> dict:
    if not path.exists():
        return {"file": label, "status": "MISSING"}
    raw = load_raw(path)
    plain_count = _count_fields(raw, fields)
    decryptable = 0
    total_encrypted = 0

    def _check(data):
        nonlocal decryptable, total_encrypted
        if isinstance(data, dict):
            for k, v in data.items():
                if k.lower() in fields and isinstance(v, str) and _looks_encrypted(v):
                    total_encrypted += 1
                    if decrypt(v):
                        decryptable += 1
                elif isinstance(v, (dict, list)):
                    _check(v)
        elif isinstance(data, list):
            for item in data:
                _check(item)

    _check(raw)
    status = "OK" if plain_count == 0 and total_encrypted > 0 else "PARTIAL" if total_encrypted > 0 else "NOT_ENCRYPTED"
    return {
        "file": label,
        "status": status,
        "champs_en_clair": plain_count,
        "champs_chiffrés": total_encrypted,
        "déchiffrables": decryptable,
    }


# ─── Rapport ──────────────────────────────────────────────────────────────────

def _status_color(status: str) -> str:
    if status in ("OK", "ALREADY_ENCRYPTED"):
        return GREEN
    if status in ("DRY_RUN", "PARTIAL"):
        return YELLOW
    return RED


def print_result(r: dict) -> None:
    color = _status_color(r.get("status", ""))
    print(f"  {color}{BOLD}[{r.get('status', '?')}]{RESET}  {r.get('file', '')}")
    if "fields_encrypted" in r:
        print(f"        Champs chiffrés : {r['fields_encrypted']}")
    if "records" in r:
        print(f"        Enregistrements : {r['records']}")
    if "backup" in r:
        print(f"        Sauvegarde      : {r['backup']}")
    if "reason" in r:
        print(f"        Raison          : {r['reason']}")
    if "champs_en_clair" in r:
        print(f"        En clair restants : {r['champs_en_clair']} | Chiffrés : {r.get('champs_chiffrés', 0)} | Déchiffrables : {r.get('déchiffrables', 0)}")
    print()


# ─── Point d'entrée ───────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(description="Migration chiffrement Fernet rétroactif ALFRED")
    parser.add_argument("--dry-run", action="store_true", help="Simulation sans écriture")
    parser.add_argument("--validate", action="store_true", help="Vérifie l'état de chiffrement")
    args = parser.parse_args()

    bar = "=" * 62
    print(f"\n{CYAN}{BOLD}{bar}{RESET}")
    if args.validate:
        print(f"{CYAN}{BOLD}  ALFRED — VALIDATION CHIFFREMENT AU REPOS{RESET}")
    elif args.dry_run:
        print(f"{YELLOW}{BOLD}  ALFRED — MIGRATION CHIFFREMENT (DRY-RUN){RESET}")
    else:
        print(f"{CYAN}{BOLD}  ALFRED — MIGRATION CHIFFREMENT RÉTROACTIF{RESET}")
    print(f"{CYAN}{BOLD}{bar}{RESET}\n")

    if not is_available():
        print(f"  {RED}{BOLD}[ERREUR]{RESET} Fernet indisponible — vérifiez FERNET_KEY dans .env\n")
        sys.exit(1)

    print(f"  {GREEN}[OK]{RESET}  Fernet disponible — chiffrement opérationnel\n")

    if args.validate:
        print(f"  {BOLD}État de chiffrement des fichiers sensibles :{RESET}\n")
        results = [
            validate_file(ROOT / "data/security/pins.json", PINS_FIELDS, "data/security/pins.json"),
            validate_file(ROOT / "data/users/instances/user_celine_instance.json", PROFILE_PII_FIELDS, "data/users/instances/user_celine_instance.json"),
            validate_file(ROOT / "data/memory/episodic/dialogue_history.json", DIALOGUE_FIELDS, "data/memory/episodic/dialogue_history.json"),
            validate_file(ROOT / "data/context/user_context.json", CONTEXT_FIELDS, "data/context/user_context.json"),
        ]
        for r in results:
            print_result(r)
        return

    if not args.dry_run:
        print(f"  {YELLOW}Sauvegardes dans : data/_backups_pre_encryption/{RESET}\n")

    print(f"  {BOLD}Migration en cours...{RESET}\n")

    all_results = []

    r = migrate_pins(args.dry_run)
    all_results.append(r)
    print_result(r)

    for r in migrate_user_instances(args.dry_run):
        all_results.append(r)
        print_result(r)

    r = migrate_dialogue_history(args.dry_run)
    all_results.append(r)
    print_result(r)

    r = migrate_user_context(args.dry_run)
    all_results.append(r)
    print_result(r)

    ok = sum(1 for r in all_results if r.get("status") in ("OK", "ALREADY_ENCRYPTED", "DRY_RUN"))
    errors = sum(1 for r in all_results if r.get("status") == "ERROR")

    print(f"{CYAN}{BOLD}{bar}{RESET}")
    print(f"  {BOLD}Résultat : {ok}/{len(all_results)} fichiers OK  |  {errors} erreur(s){RESET}")
    if not args.dry_run and errors == 0:
        print(f"  {GREEN}{BOLD}Données sensibles chiffrées au repos — Fernet AES-128-CBC{RESET}")
    print(f"{CYAN}{BOLD}{bar}{RESET}\n")


if __name__ == "__main__":
    main()
