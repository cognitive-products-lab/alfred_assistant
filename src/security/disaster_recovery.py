"""
════════════════════════════════════════════════════════════
PROJECT      : ALFRED
BLOCK        : B20
FUNCTION     : 20.22
FILE         : src/security/disaster_recovery.py
ROLE         : Plan de Continuité et Reprise d'Activité (PCA/PRA)

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-06-02
UPDATED      : 2026-06-02
VERSION      : V1.0
STATUS       : ACTIVE

DESCRIPTION :
Phase 4 SSI — PCA/PRA automatisé.
Crée des snapshots complets du projet, teste la restauration,
vérifie l'intégrité du système post-restauration et génère
un rapport de conformité PCA.

RPO cible : 24h (données conversation) · 7j (données utilisateur)
RTO cible : 2h (ALFRED_PC) · 4h (données utilisateur)
════════════════════════════════════════════════════════════
"""
from __future__ import annotations

import json
import shutil
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from src.security.security_logger import log_event

_ROOT         = Path(__file__).resolve().parents[2]
_SNAPSHOT_DIR = _ROOT / "backup" / "snapshots"
_SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)
_DR_LOG       = _ROOT / "data" / "security" / "dr_log.json"
_DR_LOG.parent.mkdir(parents=True, exist_ok=True)

# Répertoires critiques à inclure dans les snapshots (RPO 24h)
CRITICAL_PATHS = [
    "data/users/instances/",
    "data/personality/instances/",
    "data/memory/episodic/",
    "data/security/",
    "config/security/",
    ".env",
]

# Répertoires importants (RPO 7j)
IMPORTANT_PATHS = [
    "data/",
    "config/",
    "knowledges/core/",
]


# ─── Journal PCA ──────────────────────────────────────────────────────────────

def _load_dr_log() -> list[dict]:
    if not _DR_LOG.exists():
        return []
    try:
        return json.loads(_DR_LOG.read_text(encoding="utf-8"))
    except Exception:
        return []


def _append_dr_log(entry: dict) -> None:
    log = _load_dr_log()
    log.append(entry)
    _DR_LOG.write_text(json.dumps(log[-50:], indent=2, ensure_ascii=False), encoding="utf-8")


# ─── Snapshot ────────────────────────────────────────────────────────────────

def create_snapshot(
    label: str = "",
    paths: list[str] | None = None,
    encrypt: bool = False,
) -> dict[str, Any]:
    """
    Crée un snapshot des répertoires critiques.

    Args:
        label   : étiquette du snapshot
        paths   : chemins à inclure (défaut : CRITICAL_PATHS)
        encrypt : chiffrer les fichiers du snapshot

    Returns:
        dict avec snapshot_id, files_saved, errors, size_bytes.
    """
    ts          = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    snapshot_id = f"snapshot_{ts}_{label}" if label else f"snapshot_{ts}"
    snap_dir    = _SNAPSHOT_DIR / snapshot_id
    snap_dir.mkdir(parents=True, exist_ok=True)

    target_paths = paths or CRITICAL_PATHS
    saved, errors = [], []
    total_bytes   = 0

    for rel_path in target_paths:
        src = _ROOT / rel_path
        if not src.exists():
            continue
        try:
            dst = snap_dir / rel_path
            if src.is_dir():
                shutil.copytree(src, dst, dirs_exist_ok=True)
                for f in dst.rglob("*"):
                    if f.is_file():
                        total_bytes += f.stat().st_size
                        saved.append(str(f.relative_to(snap_dir)))
            else:
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, dst)
                total_bytes += dst.stat().st_size
                saved.append(rel_path)
        except Exception as exc:
            errors.append({"path": rel_path, "error": str(exc)})
            log_event(f"disaster_recovery: erreur snapshot {rel_path} — {exc}", "ERROR")

    # Manifeste du snapshot
    manifest = {
        "snapshot_id":  snapshot_id,
        "created_at":   datetime.now(timezone.utc).isoformat(),
        "label":        label,
        "files_count":  len(saved),
        "total_bytes":  total_bytes,
        "errors_count": len(errors),
        "paths_included": target_paths,
    }
    (snap_dir / "_manifest.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    log_event(
        f"disaster_recovery: snapshot '{snapshot_id}' créé "
        f"({len(saved)} fichiers, {total_bytes // 1024}Ko)"
    )

    entry = {
        "type":       "SNAPSHOT",
        "snapshot_id": snapshot_id,
        "timestamp":  datetime.now(timezone.utc).isoformat(),
        "files":      len(saved),
        "bytes":      total_bytes,
        "errors":     len(errors),
        "ok":         len(errors) == 0,
    }
    _append_dr_log(entry)

    return {
        "snapshot_id": snapshot_id,
        "snapshot_dir": str(snap_dir),
        "files_saved":  saved,
        "errors":       errors,
        "size_bytes":   total_bytes,
        "manifest":     manifest,
        "ok":           len(errors) == 0,
    }


def list_snapshots() -> list[dict]:
    """Liste les snapshots disponibles."""
    snapshots = []
    for d in sorted(_SNAPSHOT_DIR.iterdir()):
        if not d.is_dir():
            continue
        manifest_f = d / "_manifest.json"
        if manifest_f.exists():
            try:
                m = json.loads(manifest_f.read_text(encoding="utf-8"))
                snapshots.append(m)
            except Exception:
                snapshots.append({"snapshot_id": d.name, "error": "manifest illisible"})
        else:
            snapshots.append({"snapshot_id": d.name, "files_count": "?"})
    return snapshots


def get_latest_snapshot() -> dict | None:
    """Retourne le snapshot le plus récent."""
    snaps = list_snapshots()
    return snaps[-1] if snaps else None


# ─── Test de restauration ────────────────────────────────────────────────────

def verify_restore(snapshot_id: str, test_dir: Path | None = None) -> dict[str, Any]:
    """
    Teste la restauration d'un snapshot dans un répertoire temporaire.
    Vérifie l'intégrité sans écraser les données réelles.

    Returns:
        dict avec ok, files_restored, integrity_check, duration_s.
    """
    snap_dir = _SNAPSHOT_DIR / snapshot_id
    if not snap_dir.exists():
        return {"ok": False, "error": f"Snapshot introuvable : {snapshot_id}"}

    import tempfile
    restore_root = test_dir or Path(tempfile.mkdtemp(prefix="alfred_dr_test_"))
    t0 = time.perf_counter()
    restored, errors = [], []

    try:
        shutil.copytree(snap_dir, restore_root / snapshot_id, dirs_exist_ok=True)

        # Vérifier que les fichiers critiques sont présents
        manifest_f = snap_dir / "_manifest.json"
        if manifest_f.exists():
            manifest = json.loads(manifest_f.read_text(encoding="utf-8"))
            expected = manifest.get("files_count", 0)
            actual   = sum(1 for _ in (restore_root / snapshot_id).rglob("*") if _.is_file())
            integrity_ok = actual >= expected * 0.9   # tolérance 10%
        else:
            integrity_ok = True

        duration = round(time.perf_counter() - t0, 2)

        log_event(
            f"disaster_recovery: test restore '{snapshot_id}' "
            f"{'OK' if integrity_ok else 'KO'} ({duration}s)"
        )

        entry = {
            "type":        "RESTORE_TEST",
            "snapshot_id": snapshot_id,
            "timestamp":   datetime.now(timezone.utc).isoformat(),
            "ok":          integrity_ok,
            "duration_s":  duration,
        }
        _append_dr_log(entry)

        return {
            "ok":             integrity_ok,
            "snapshot_id":    snapshot_id,
            "restore_path":   str(restore_root / snapshot_id),
            "integrity_check": integrity_ok,
            "duration_s":     duration,
            "errors":         errors,
        }

    except Exception as exc:
        log_event(f"disaster_recovery: erreur test restore — {exc}", "ERROR")
        return {"ok": False, "error": str(exc)}
    finally:
        # Nettoyage du répertoire de test
        if test_dir is None and restore_root.exists():
            try:
                shutil.rmtree(restore_root, ignore_errors=True)
            except Exception:
                pass


# ─── Rapport PCA ──────────────────────────────────────────────────────────────

def build_pca_report() -> dict[str, Any]:
    """
    Construit le rapport PCA/PRA avec état des snapshots et conformité.
    """
    snapshots   = list_snapshots()
    latest      = snapshots[-1] if snapshots else None
    dr_log      = _load_dr_log()
    last_test   = next((e for e in reversed(dr_log) if e.get("type") == "RESTORE_TEST"), None)

    # Calcul RPO actuel
    rpo_hours = None
    if latest and latest.get("created_at"):
        try:
            snap_date = datetime.fromisoformat(latest["created_at"])
            rpo_hours = round((datetime.now(timezone.utc) - snap_date).total_seconds() / 3600, 1)
        except Exception:
            pass

    checks = []

    def chk(title: str, ok: bool, detail: str = "") -> None:
        checks.append({"title": title, "ok": ok, "detail": detail})

    chk("Snapshots présents",          len(snapshots) >= 1,
        f"{len(snapshots)} snapshot(s) disponible(s)")
    chk("RPO < 24h atteint",           rpo_hours is not None and rpo_hours < 24,
        f"RPO actuel : {rpo_hours}h" if rpo_hours else "Aucun snapshot")
    chk("Test de restauration effectué", last_test is not None,
        f"Dernier test : {last_test['timestamp'][:10] if last_test else 'jamais'}")
    chk("Dernier test de restauration OK", last_test is not None and last_test.get("ok", False),
        "Test passé" if (last_test and last_test.get("ok")) else "Test échoué ou absent")
    chk("Journal PCA actif",           len(dr_log) > 0)

    score = sum(1 for c in checks if c["ok"])

    return {
        "_meta": {
            "project": "ALFRED",
            "block":   "B20",
            "file":    "pca_report.json",
            "role":    "Rapport PCA/PRA",
            "version": "V1.0",
        },
        "generated_at":     datetime.now(timezone.utc).isoformat(),
        "snapshots_count":  len(snapshots),
        "latest_snapshot":  latest,
        "rpo_hours_current": rpo_hours,
        "rpo_target_hours": 24,
        "rto_target_hours": 2,
        "rpo_met":          rpo_hours is not None and rpo_hours < 24,
        "last_restore_test": last_test,
        "dr_log_entries":   len(dr_log),
        "checks":           checks,
        "compliance_score": score,
        "compliance_max":   len(checks),
        "compliance_rate":  round(score / len(checks) * 100, 1) if checks else 0,
        "grade":            "A" if score == len(checks) else "B" if score >= len(checks) * 0.6 else "C",
    }


def export_pca_report(output_path: Path | None = None) -> Path:
    """Exporte le rapport PCA en JSON."""
    out = output_path or (_ROOT / "dashboard" / "dashboard_security" / "pca_report.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    report = build_pca_report()
    out.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    log_event(f"disaster_recovery: rapport PCA exporté → {out}")
    return out
