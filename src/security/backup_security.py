"""
════════════════════════════════════════════════════════════
PROJECT      : ALFRED
BLOCK        : B20
FUNCTION     : 20.03
FILE         : backup_security.py
ROLE         : Sauvegarde sécurisée — chiffrement Fernet + intégrité SHA-256 + rotation TTL

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-05-23
UPDATED      : 2026-06-01
VERSION      : V2.0
STATUS       : ACTIVE

DESCRIPTION :
V2 : chiffrement Fernet optionnel des backups, vérification intégrité
SHA-256 avant/après, rotation TTL configurable, restore sécurisé.
Rétrocompatible V1 (secure_backup, backup_many, list_backups, summarize_backups).
════════════════════════════════════════════════════════════
"""
from __future__ import annotations

import hashlib
import json
import shutil
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any

from src.security.security_logger import log_event

# ─── Configuration ────────────────────────────────────────────────────────────

_ROOT       = Path(__file__).resolve().parents[2]
BACKUP_DIR  = _ROOT / "backup" / "security"
BACKUP_DIR.mkdir(parents=True, exist_ok=True)

MAX_BACKUPS_DEFAULT = 10       # rotation : garder au plus N backups par fichier
TTL_DAYS_DEFAULT    = 30       # suppression des backups > N jours
MANIFEST_FILE       = BACKUP_DIR / ".manifest.json"  # index des backups + hashes


# ─── Intégrité ────────────────────────────────────────────────────────────────

def _sha256(path: Path) -> str:
    """Calcule le SHA-256 d'un fichier."""
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def _load_manifest() -> dict[str, Any]:
    if not MANIFEST_FILE.exists():
        return {}
    try:
        return json.loads(MANIFEST_FILE.read_text(encoding="utf-8"))
    except Exception:
        return {}


def _save_manifest(data: dict) -> None:
    try:
        MANIFEST_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    except Exception as exc:
        log_event(f"backup_security: impossible de sauvegarder le manifeste — {exc}", "ERROR")


# ─── Chiffrement optionnel ────────────────────────────────────────────────────

def _encrypt_file(src: Path, dst: Path) -> bool:
    """Chiffre src vers dst avec Fernet. Retourne True si succès, False si chiffrement indisponible."""
    try:
        from src.security.encryption_service import encrypt, is_available
        if not is_available():
            return False
        data = src.read_bytes()
        token = encrypt(data.decode("latin-1"))   # encode bytes via latin-1 pour passer par Fernet str
        dst.write_bytes(token.encode("utf-8"))
        return True
    except Exception as exc:
        log_event(f"backup_security: chiffrement impossible — {exc}", "WARNING")
        return False


def _decrypt_file(src: Path, dst: Path) -> bool:
    """Déchiffre src vers dst. Retourne True si succès."""
    try:
        from src.security.encryption_service import decrypt, is_available
        if not is_available():
            return False
        token = src.read_text(encoding="utf-8")
        plain = decrypt(token)
        if not plain:
            return False
        dst.write_bytes(plain.encode("latin-1"))
        return True
    except Exception as exc:
        log_event(f"backup_security: déchiffrement impossible — {exc}", "WARNING")
        return False


# ─── API principale ───────────────────────────────────────────────────────────

def secure_backup(
    source_path: str,
    label: str = "",
    encrypt: bool = False,
    max_keep: int = MAX_BACKUPS_DEFAULT,
) -> str:
    """
    Crée une sauvegarde horodatée d'un fichier sensible.

    Args:
        source_path : chemin du fichier source
        label       : étiquette optionnelle dans le nom du backup
        encrypt     : True pour chiffrer le backup avec Fernet
        max_keep    : nombre max de backups à conserver pour ce fichier

    Returns:
        Chemin absolu du fichier de backup créé.
    """
    if not source_path:
        raise ValueError("Chemin source vide")
    source = Path(source_path)
    if not source.exists():
        raise FileNotFoundError(f"Fichier introuvable : {source_path}")
    if source.is_dir():
        raise ValueError(f"Impossible de sauvegarder un dossier : {source_path}")

    # ── Hash source avant backup ──────────────────────────────────────────────
    src_hash = _sha256(source)

    # ── Nom destination ───────────────────────────────────────────────────────
    timestamp  = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    suffix     = f".{label}" if label else ""
    enc_suffix = ".enc" if encrypt else ""
    destination = BACKUP_DIR / f"{source.name}{suffix}.{timestamp}.bak{enc_suffix}"

    # ── Copie ou chiffrement ──────────────────────────────────────────────────
    if encrypt:
        encrypted = _encrypt_file(source, destination)
        if not encrypted:
            # Fallback : copie non chiffrée
            shutil.copy2(source, destination.with_suffix(""))
            destination = destination.with_suffix("")
            log_event(f"backup_security: backup non chiffré (Fernet indisponible) : {destination}", "WARNING")
    else:
        shutil.copy2(source, destination)

    # ── Hash destination ──────────────────────────────────────────────────────
    dst_hash = _sha256(destination)

    # ── Manifeste ────────────────────────────────────────────────────────────
    manifest = _load_manifest()
    key = source.name
    if key not in manifest:
        manifest[key] = []
    manifest[key].append({
        "backup":    str(destination),
        "source":    str(source),
        "src_hash":  src_hash,
        "dst_hash":  dst_hash,
        "encrypted": encrypt,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    })
    _save_manifest(manifest)

    log_event(f"backup_security: backup créé — {destination} sha256={src_hash[:16]}…")

    # ── Rotation ──────────────────────────────────────────────────────────────
    _rotate_backups(key, max_keep)

    return str(destination)


def verify_backup_integrity(backup_path: str) -> dict[str, Any]:
    """
    Vérifie l'intégrité d'un backup en comparant le hash courant avec celui du manifeste.

    Returns:
        dict avec ok (bool), current_hash, expected_hash, message.
    """
    bp = Path(backup_path)
    if not bp.exists():
        return {"ok": False, "message": f"Fichier backup introuvable : {backup_path}"}

    current_hash = _sha256(bp)
    manifest = _load_manifest()

    # Chercher dans le manifeste
    for key, entries in manifest.items():
        for entry in entries:
            if entry.get("backup") == str(bp):
                expected = entry.get("dst_hash", "")
                ok = current_hash == expected
                if not ok:
                    log_event(
                        f"backup_security: intégrité compromise — {bp.name} "
                        f"hash_attendu={expected[:16]}… hash_actuel={current_hash[:16]}…",
                        "CRITICAL",
                    )
                return {
                    "ok": ok,
                    "current_hash":  current_hash,
                    "expected_hash": expected,
                    "message": "Intégrité OK" if ok else "HASH DIFFÉRENT — backup potentiellement altéré",
                    "encrypted": entry.get("encrypted", False),
                }

    # Non trouvé dans le manifeste
    return {
        "ok": None,
        "current_hash": current_hash,
        "expected_hash": None,
        "message": "Backup non référencé dans le manifeste — impossible de vérifier",
    }


def restore_backup(backup_path: str, destination_path: str, verify: bool = True) -> dict[str, Any]:
    """
    Restaure un backup vers sa destination, avec vérification d'intégrité optionnelle.

    Returns:
        dict avec ok (bool) et message.
    """
    bp  = Path(backup_path)
    dst = Path(destination_path)

    if not bp.exists():
        return {"ok": False, "message": f"Backup introuvable : {backup_path}"}

    # Vérification intégrité avant restore
    if verify:
        check = verify_backup_integrity(backup_path)
        if check["ok"] is False:
            return {
                "ok": False,
                "message": f"Restore annulé — intégrité compromise : {check['message']}",
                "integrity": check,
            }

    # Déchiffrement si nécessaire
    manifest = _load_manifest()
    is_encrypted = False
    for entries in manifest.values():
        for entry in entries:
            if entry.get("backup") == str(bp):
                is_encrypted = entry.get("encrypted", False)
                break

    dst.parent.mkdir(parents=True, exist_ok=True)

    if is_encrypted:
        ok = _decrypt_file(bp, dst)
        if not ok:
            return {"ok": False, "message": "Déchiffrement échoué — vérifier la clé Fernet"}
    else:
        shutil.copy2(bp, dst)

    log_event(f"backup_security: restauration OK — {bp.name} → {dst}")
    return {"ok": True, "message": f"Restauré vers {dst}", "source": str(bp)}


def cleanup_old_backups_by_ttl(ttl_days: int = TTL_DAYS_DEFAULT) -> dict[str, Any]:
    """
    Supprime les backups plus anciens que ttl_days jours.

    Returns:
        dict avec deleted (int), kept (int), errors (list).
    """
    cutoff  = datetime.now(timezone.utc) - timedelta(days=ttl_days)
    deleted = 0
    errors  = []
    manifest = _load_manifest()

    for key, entries in list(manifest.items()):
        new_entries = []
        for entry in entries:
            try:
                ts  = datetime.fromisoformat(entry.get("timestamp", ""))
                if ts.tzinfo is None:
                    ts = ts.replace(tzinfo=timezone.utc)
                if ts < cutoff:
                    bp = Path(entry["backup"])
                    if bp.exists():
                        bp.unlink()
                    deleted += 1
                else:
                    new_entries.append(entry)
            except Exception as exc:
                errors.append(str(exc))
                new_entries.append(entry)
        manifest[key] = new_entries

    _save_manifest(manifest)
    log_event(f"backup_security: TTL cleanup — {deleted} supprimé(s), TTL={ttl_days}j")
    return {"deleted": deleted, "kept": sum(len(v) for v in manifest.values()), "errors": errors}


def _rotate_backups(key: str, max_keep: int) -> None:
    """Conserve uniquement les max_keep backups les plus récents pour une clé."""
    manifest = _load_manifest()
    entries  = manifest.get(key, [])
    if len(entries) <= max_keep:
        return
    to_delete = entries[: len(entries) - max_keep]
    for entry in to_delete:
        try:
            bp = Path(entry["backup"])
            if bp.exists():
                bp.unlink()
        except Exception:
            pass
    manifest[key] = entries[len(entries) - max_keep:]
    _save_manifest(manifest)


# ─── API V1 compat ────────────────────────────────────────────────────────────

def backup_many(source_paths: list[str], label: str = "", encrypt: bool = False) -> dict:
    """Crée des sauvegardes pour plusieurs fichiers."""
    success, errors = [], []
    for path in source_paths:
        try:
            dest = secure_backup(path, label=label, encrypt=encrypt)
            success.append({"source": path, "backup": dest})
        except Exception as exc:
            errors.append({"source": path, "error": str(exc)})
    return {"success": success, "errors": errors}


def list_backups() -> list[dict]:
    """Liste les fichiers de sauvegarde présents."""
    if not BACKUP_DIR.exists():
        return []
    return [
        {"name": f.name, "path": str(f), "size_bytes": f.stat().st_size}
        for f in sorted(BACKUP_DIR.iterdir())
        if f.is_file() and f.name != ".manifest.json"
    ]


def summarize_backups() -> dict:
    """Synthèse du répertoire de backup."""
    backups   = list_backups()
    manifest  = _load_manifest()
    total_size = sum(b["size_bytes"] for b in backups)
    last       = backups[-1]["name"] if backups else ""
    enc_count  = sum(
        1 for entries in manifest.values()
        for e in entries if e.get("encrypted")
    )
    return {
        "total_backups":    len(backups),
        "count":            len(backups),
        "total_size_bytes": total_size,
        "encrypted_count":  enc_count,
        "last_backup":      last,
        "backup_dir":       str(BACKUP_DIR),
        "directory":        str(BACKUP_DIR),
        "manifest_entries": sum(len(v) for v in manifest.values()),
    }


def cleanup_old_backups(keep_last: int = 20) -> dict:
    """V1 compat — supprime les backups les plus anciens (sans TTL)."""
    backups   = list_backups()
    to_delete = backups[: max(0, len(backups) - keep_last)]
    for b in to_delete:
        Path(b["path"]).unlink(missing_ok=True)
    return {"deleted": len(to_delete), "kept": len(backups) - len(to_delete)}
