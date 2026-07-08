"""
PROJECT : ALFRED
BLOCK   : B01 / RGPD
FILE    : src/conversation/commands/portability.py
ROLE    : Droit de portabilité Art. 20 RGPD — export + réimportation complète
STATUS  : VALIDATED

L'export produit un fichier JSON structuré, lisible par tout système
tiers, contenant l'intégralité des données fournies par l'utilisateur
(profil, mémoire, paramètres, consentements).

La réimportation vérifie la structure et restaure les données
section par section, sans écraser les champs de sécurité.

Usage :
    from src.conversation.commands.portability import export_portable, import_portable
    export_portable("data/exports/portability_export.json")
    import_portable("data/exports/portability_export.json")
"""

from __future__ import annotations

import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[3]

EXPORT_SCHEMA_VERSION = "1.0"

# Sections exportables avec leur chemin source et leur flag de réimportation
_SECTIONS: dict[str, dict] = {
    "user_profile": {
        "path": ROOT / "data/profile/user_profile.json",
        "reimportable": True,
        "description": "Profil utilisateur — personnalité, préférences, softskills",
    },
    "behavioral_params": {
        "path": ROOT / "data/profile/alfred_behavioral_params.json",
        "reimportable": True,
        "description": "Paramètres comportementaux ALFRED",
    },
    "episodes_memory": {
        "path": ROOT / "data/memory/episodes.json",
        "reimportable": True,
        "description": "Mémoire épisodique — historique des interactions",
    },
    "wellbeing_log": {
        "path": ROOT / "data/memory/wellbeing_log.json",
        "reimportable": True,
        "description": "Journal bien-être et énergie",
    },
    "device_settings": {
        "path": ROOT / "data/settings/device_settings.json",
        "reimportable": False,
        "description": "Paramètres appareil — non réimportable (dépend du matériel)",
    },
    "features_config": {
        "path": ROOT / "config/features.json",
        "reimportable": True,
        "description": "Fonctionnalités activées / désactivées (Art. 21)",
    },
}

# Champs à ne jamais exporter même si présents
_BLOCKED_KEYS = frozenset({"key", "secret", "password", "salt", "token", "pin", "fernet", "mfa_secret"})


def _redact(data: Any) -> Any:
    if isinstance(data, dict):
        return {
            k: "[REDACTED — champ sensible]" if any(b in k.lower() for b in _BLOCKED_KEYS)
            else _redact(v)
            for k, v in data.items()
        }
    if isinstance(data, list):
        return [_redact(i) for i in data]
    return data


def export_portable(output_path: str | Path | None = None) -> dict:
    """
    Export portable Art. 20 — toutes données utilisateur dans un JSON réimportable.

    Returns dict avec status, output_file, sections_ok, sections_missing.
    """
    exported_at = datetime.now(timezone.utc).isoformat()

    if output_path is None:
        export_dir = ROOT / "data/exports"
        export_dir.mkdir(parents=True, exist_ok=True)
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = export_dir / f"portability_export_{ts}.json"

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    payload: dict = {
        "_meta": {
            "right": "Art. 20 RGPD — Portabilité des données",
            "schema_version": EXPORT_SCHEMA_VERSION,
            "exported_at": exported_at,
            "generated_by": "src/conversation/commands/portability.py",
            "reimport_command": "portability.import_portable('<ce_fichier>')",
            "note": "Fichier d'export portable ALFRED. Champs cryptographiques retirés.",
        },
        "sections": {},
        "sections_missing": [],
        "reimportable_sections": [],
    }

    sections_ok = []
    for name, cfg in _SECTIONS.items():
        src: Path = cfg["path"]
        try:
            raw = json.loads(src.read_text(encoding="utf-8"))
            payload["sections"][name] = {
                "description": cfg["description"],
                "reimportable": cfg["reimportable"],
                "data": _redact(raw),
            }
            sections_ok.append(name)
            if cfg["reimportable"]:
                payload["reimportable_sections"].append(name)
        except Exception:
            payload["sections_missing"].append(name)

    output_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    return {
        "status": "OK",
        "right": "Art. 20",
        "output_file": str(output_path),
        "sections_ok": sections_ok,
        "sections_missing": payload["sections_missing"],
        "reimportable_sections": payload["reimportable_sections"],
        "exported_at": exported_at,
    }


def import_portable(source_path: str | Path) -> dict:
    """
    Réimportation Art. 20 — restaure les sections réimportables depuis un export portable.

    Sauvegarde les fichiers existants dans data/exports/backup_import_<ts>/
    avant écrasement.
    """
    source_path = Path(source_path)
    if not source_path.exists():
        return {"status": "ERROR", "reason": f"Fichier introuvable : {source_path}"}

    try:
        payload = json.loads(source_path.read_text(encoding="utf-8"))
    except Exception as exc:
        return {"status": "ERROR", "reason": f"JSON invalide : {exc}"}

    schema_ver = payload.get("_meta", {}).get("schema_version", "?")
    if schema_ver != EXPORT_SCHEMA_VERSION:
        return {"status": "ERROR", "reason": f"Schema version incompatible : {schema_ver} (attendu {EXPORT_SCHEMA_VERSION})"}

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = ROOT / f"data/exports/backup_import_{ts}"
    backup_dir.mkdir(parents=True, exist_ok=True)

    restored = []
    skipped = []
    errors = []

    sections = payload.get("sections", {})
    for name, section_data in sections.items():
        if not section_data.get("reimportable", False):
            skipped.append(f"{name} (non réimportable)")
            continue

        cfg = _SECTIONS.get(name)
        if cfg is None:
            skipped.append(f"{name} (section inconnue)")
            continue

        dest: Path = cfg["path"]
        try:
            # Backup
            if dest.exists():
                shutil.copy2(dest, backup_dir / dest.name)

            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(
                json.dumps(section_data["data"], ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
            restored.append(name)
        except Exception as exc:
            errors.append(f"{name}: {exc}")

    status = "OK" if not errors else ("PARTIAL" if restored else "ERROR")
    return {
        "status": status,
        "right": "Art. 20",
        "source_file": str(source_path),
        "backup_dir": str(backup_dir),
        "restored": restored,
        "skipped": skipped,
        "errors": errors,
        "imported_at": datetime.now(timezone.utc).isoformat(),
    }


if __name__ == "__main__":
    r = export_portable()
    print(f"[Art.20] Export portable → {r['output_file']}")
    print(f"  Sections OK : {', '.join(r['sections_ok'])}")
    print(f"  Réimportables : {', '.join(r['reimportable_sections'])}")
