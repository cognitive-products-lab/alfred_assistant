"""
════════════════════════════════════════════════════════════
PROJECT      : ALFRED
BLOCK        : B20
FUNCTION     : 20.21
FILE         : src/security/key_rotation_scheduler.py
ROLE         : Planificateur de rotation des clés cryptographiques

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-06-02
UPDATED      : 2026-06-02
VERSION      : V1.0
STATUS       : ACTIVE

DESCRIPTION :
Phase 4 SSI — Rotation automatique des clés cryptographiques.
Vérifie l'âge des secrets, alerte si dépassement du seuil,
prépare la rotation Fernet (re-chiffrement des données existantes
avant de changer la clé) et journalise chaque opération.
La rotation effective de FERNET_KEY reste manuelle (modification .env)
mais ce module prépare et valide le processus.
════════════════════════════════════════════════════════════
"""
from __future__ import annotations

import json
import threading
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any

from src.security.security_logger import log_event

_ROOT          = Path(__file__).resolve().parents[2]
_ROTATION_LOG  = _ROOT / "data" / "security" / "key_rotation_log.json"
_ROTATION_LOG.parent.mkdir(parents=True, exist_ok=True)

# Seuils de rotation (jours)
ROTATION_THRESHOLDS: dict[str, int] = {
    "FERNET_KEY":     90,    # 3 mois
    "SECRET_KEY":     180,   # 6 mois
    "PIN_SALT":       365,   # 1 an
    "API_SECRET_KEY": 90,    # 3 mois
}

_lock = threading.Lock()


# ─── Journal de rotation ──────────────────────────────────────────────────────

def _load_rotation_log() -> list[dict]:
    if not _ROTATION_LOG.exists():
        return []
    try:
        return json.loads(_ROTATION_LOG.read_text(encoding="utf-8"))
    except Exception:
        return []


def _append_rotation_log(entry: dict) -> None:
    with _lock:
        log = _load_rotation_log()
        log.append(entry)
        _ROTATION_LOG.write_text(
            json.dumps(log[-100:], indent=2, ensure_ascii=False),   # garder 100 dernières entrées
            encoding="utf-8",
        )


def get_rotation_history(key: str | None = None) -> list[dict]:
    """Retourne l'historique de rotation (filtré par clé si fourni)."""
    log = _load_rotation_log()
    if key:
        return [e for e in log if e.get("key") == key]
    return log


def get_last_rotation(key: str) -> dict | None:
    """Retourne la dernière rotation enregistrée pour une clé."""
    history = get_rotation_history(key)
    return history[-1] if history else None


# ─── Vérification de l'âge ───────────────────────────────────────────────────

def check_key_age(key: str, threshold_days: int | None = None) -> dict[str, Any]:
    """
    Vérifie si une clé dépasse son seuil de rotation.

    Args:
        key            : nom de la variable d'environnement
        threshold_days : seuil en jours (défaut : ROTATION_THRESHOLDS[key])

    Returns:
        dict avec needs_rotation, age_days, threshold_days, last_rotation.
    """
    from src.security.secret_manager import secret_exists, secret_age_days

    threshold = threshold_days if threshold_days is not None else ROTATION_THRESHOLDS.get(key, 90)
    exists    = secret_exists(key)
    age       = secret_age_days(key)
    last_rot  = get_last_rotation(key)

    # Si rotation enregistrée, utiliser cette date comme référence
    if last_rot:
        try:
            rot_date  = datetime.fromisoformat(last_rot["rotated_at"])
            age_since = (datetime.now(timezone.utc) - rot_date).days
        except Exception:
            age_since = age
    else:
        age_since = age

    needs = exists and age_since is not None and age_since > threshold

    if needs:
        log_event(
            f"key_rotation: '{key}' âgée de {age_since}j "
            f"(seuil {threshold}j) — rotation recommandée",
            "WARNING",
        )

    return {
        "key":           key,
        "exists":        exists,
        "age_days":      round(age_since, 1) if age_since is not None else None,
        "threshold_days": threshold,
        "needs_rotation": needs,
        "last_rotation": last_rot,
        "status":        "ROTATION_REQUISE" if needs else "OK",
    }


def check_all_keys() -> dict[str, Any]:
    """Vérifie l'âge de toutes les clés connues."""
    results = {}
    rotation_needed = []

    for key, threshold in ROTATION_THRESHOLDS.items():
        result = check_key_age(key, threshold)
        results[key] = result
        if result["needs_rotation"]:
            rotation_needed.append(key)

    return {
        "checked_at":       datetime.now(timezone.utc).isoformat(),
        "keys":             results,
        "rotation_needed":  rotation_needed,
        "all_ok":           len(rotation_needed) == 0,
        "urgent_count":     len(rotation_needed),
    }


# ─── Préparation de la rotation Fernet ───────────────────────────────────────

def prepare_fernet_rotation() -> dict[str, Any]:
    """
    Prépare la rotation de la clé Fernet.

    1. Vérifie que Fernet est disponible
    2. Liste les fichiers chiffrés à re-chiffrer
    3. Crée un backup sécurisé des données avant rotation
    4. Retourne les instructions pour l'opérateur

    Note : La modification de FERNET_KEY dans .env reste manuelle
    pour garantir que l'opérateur valide l'opération.
    """
    from src.security.encryption_service import is_available, Fernet as _Fernet
    from src.security.backup_security import backup_many

    result: dict[str, Any] = {
        "prepared_at":   datetime.now(timezone.utc).isoformat(),
        "fernet_ok":     is_available(),
        "files_to_reencrypt": [],
        "backup_created": False,
        "instructions":  [],
    }

    if not is_available():
        result["instructions"].append("❌ Fernet non disponible — impossible de préparer la rotation")
        return result

    # Fichiers sensibles chiffrés qui devront être re-chiffrés après rotation
    sensitive_files = [
        str(_ROOT / "data" / "security" / "mfa_secrets.json"),
        str(_ROOT / "data" / "security" / "behavior_baseline.json"),
    ]
    existing = [f for f in sensitive_files if Path(f).exists()]
    result["files_to_reencrypt"] = existing

    # Backup sécurisé avant rotation
    if existing:
        try:
            backup_result = backup_many(existing, label="pre-rotation", encrypt=True)
            result["backup_created"] = len(backup_result["success"]) > 0
            result["backup_details"] = backup_result
        except Exception as exc:
            result["backup_error"] = str(exc)

    # Instructions pour l'opérateur
    result["instructions"] = [
        "1. Générer une nouvelle clé : python -c \"from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())\"",
        "2. Remplacer FERNET_KEY dans .env par la nouvelle valeur",
        "3. Redémarrer ALFRED pour charger la nouvelle clé",
        "4. Re-chiffrer les données existantes avec rotate_encrypted_files()",
        "5. Enregistrer la rotation avec record_rotation('FERNET_KEY')",
    ]

    log_event("key_rotation: préparation rotation Fernet — backup créé, instructions générées")
    return result


def rotate_encrypted_files(old_key_bytes: bytes, new_key_bytes: bytes) -> dict[str, Any]:
    """
    Re-chiffre les fichiers sensibles avec la nouvelle clé Fernet.
    À appeler APRÈS avoir changé FERNET_KEY dans .env.

    Args:
        old_key_bytes : ancienne clé Fernet (bytes)
        new_key_bytes : nouvelle clé Fernet (bytes)

    Returns:
        dict avec success/errors par fichier.
    """
    try:
        from cryptography.fernet import Fernet, InvalidToken
    except ImportError:
        return {"ok": False, "error": "cryptography non installé"}

    old_f = Fernet(old_key_bytes)
    new_f = Fernet(new_key_bytes)

    sensitive_files = [
        _ROOT / "data" / "security" / "mfa_secrets.json",
        _ROOT / "data" / "security" / "behavior_baseline.json",
    ]

    results = {"success": [], "errors": [], "skipped": []}

    for path in sensitive_files:
        if not path.exists():
            results["skipped"].append(str(path))
            continue
        try:
            raw     = path.read_bytes()
            plain   = old_f.decrypt(raw)
            new_enc = new_f.encrypt(plain)
            path.write_bytes(new_enc)
            results["success"].append(str(path))
            log_event(f"key_rotation: re-chiffrement OK — {path.name}")
        except InvalidToken:
            results["skipped"].append(str(path) + " (pas chiffré avec l'ancienne clé)")
        except Exception as exc:
            results["errors"].append({"file": str(path), "error": str(exc)})
            log_event(f"key_rotation: erreur re-chiffrement {path.name} — {exc}", "ERROR")

    return results


def record_rotation(key: str, notes: str = "") -> None:
    """Enregistre une rotation de clé dans le journal."""
    entry = {
        "key":        key,
        "rotated_at": datetime.now(timezone.utc).isoformat(),
        "notes":      notes,
    }
    _append_rotation_log(entry)
    log_event(f"key_rotation: rotation enregistrée pour '{key}'")


# ─── Dashboard SMSI ───────────────────────────────────────────────────────────

def get_smsi_summary() -> dict[str, Any]:
    """
    Retourne un résumé SMSI (Système de Management SSI) pour le dashboard.
    Agrège : âge des clés, backups, conformité RGPD, risques.
    """
    key_status = check_all_keys()

    # Conformité RGPD
    try:
        from src.security.data_flow_mapper import check_rgpd_compliance
        rgpd = check_rgpd_compliance()
    except Exception:
        rgpd = {"compliance_rate": 0, "grade": "?"}

    # Matrice de risques
    try:
        from src.security.risk_engine import build_risk_matrix
        risks = build_risk_matrix(adjust_for_posture=True)
        risk_summary = {
            "global_level":  risks.get("global_level", "?"),
            "critique":      risks["by_level"].get("CRITIQUE", 0),
            "eleve":         risks["by_level"].get("ELEVE", 0),
        }
    except Exception:
        risk_summary = {"global_level": "?", "critique": 0, "eleve": 0}

    # Score SMSI global
    smsi_score = 100
    if key_status["urgent_count"] > 0:
        smsi_score -= key_status["urgent_count"] * 10
    if rgpd.get("compliance_rate", 100) < 90:
        smsi_score -= 15
    if risk_summary["critique"] > 0:
        smsi_score -= risk_summary["critique"] * 15
    smsi_score = max(0, smsi_score)

    return {
        "_meta": {
            "generated": datetime.now(timezone.utc).isoformat(),
            "version": "V1.0",
        },
        "smsi_score":       smsi_score,
        "smsi_grade":       "A" if smsi_score >= 90 else "B" if smsi_score >= 75 else "C",
        "key_rotation":     key_status,
        "rgpd_compliance":  rgpd,
        "risk_summary":     risk_summary,
        "rotation_history": _load_rotation_log()[-5:],   # 5 dernières rotations
    }


# ─── Classe façade (compatibilité import OO) ──────────────────────────────────

class KeyRotationScheduler:
    """
    Façade orientée-objet sur les fonctions de rotation du module.
    Permet l'import : from src.security.key_rotation_scheduler import KeyRotationScheduler
    """

    def check_all_keys(self) -> dict:
        return check_all_keys()

    def check_key_age(self, key: str, threshold_days: int | None = None) -> dict:
        return check_key_age(key, threshold_days)

    def get_rotation_history(self, key: str | None = None) -> list:
        return get_rotation_history(key)

    def get_last_rotation(self, key: str) -> dict | None:
        return get_last_rotation(key)

    def prepare_fernet_rotation(self) -> dict:
        return prepare_fernet_rotation()

    def record_rotation(self, key: str, notes: str = "") -> None:
        record_rotation(key, notes)

    def get_smsi_summary(self) -> dict:
        return get_smsi_summary()
