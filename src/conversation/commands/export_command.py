"""
PROJECT : ALFRED
BLOCK   : B01 / RGPD
FILE    : src/conversation/commands/export_command.py
ROLE    : Droit d'accès Art. 15 RGPD — export lisible des données personnelles

Produit un rapport JSON horodaté contenant toutes les données
accessibles à l'utilisateur en lecture : profil, mémoire, préférences,
paramètres comportementaux.  Aucune clé cryptographique n'est exportée.

Usage :
    from src.conversation.commands.export_command import export_user_data
    result = export_user_data(output_path="data/exports/export_art15.json")
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[3]


def _safe_load(path: Path) -> Any:
    """Charge un JSON sans lever d'exception si absent ou invalide."""
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def _redact_sensitive(data: Any) -> Any:
    """Retire récursivement les champs sensibles (clés crypto, mots de passe)."""
    if isinstance(data, dict):
        return {
            k: "[REDACTED]" if any(s in k.lower() for s in ("key", "secret", "password", "salt", "token", "pin"))
            else _redact_sensitive(v)
            for k, v in data.items()
        }
    if isinstance(data, list):
        return [_redact_sensitive(i) for i in data]
    return data


def export_user_data(output_path: str | Path | None = None) -> dict:
    """
    Génère l'export Art. 15 des données personnelles accessibles.

    Returns:
        dict avec 'status', 'output_file', 'sections' listant les sources collectées.
    """
    exported_at = datetime.now(timezone.utc).isoformat()

    sources = {
        "user_profile":         ROOT / "data/profile/user_profile.json",
        "behavioral_params":    ROOT / "data/profile/alfred_behavioral_params.json",
        "episodes_memory":      ROOT / "data/memory/episodes.json",
        "wellbeing_log":        ROOT / "data/memory/wellbeing_log.json",
        "device_settings":      ROOT / "data/settings/device_settings.json",
    }

    payload: dict = {
        "_meta": {
            "right": "Art. 15 RGPD — Droit d'accès",
            "exported_at": exported_at,
            "generated_by": "src/conversation/commands/export_command.py",
            "note": "Export lisible des données personnelles. Champs cryptographiques retirés.",
        },
        "sections": {},
        "missing_sources": [],
    }

    collected = []
    for key, path in sources.items():
        raw = _safe_load(path)
        if raw is not None:
            payload["sections"][key] = _redact_sensitive(raw)
            collected.append(key)
        else:
            payload["missing_sources"].append(key)

    # Destination
    if output_path is None:
        export_dir = ROOT / "data/exports"
        export_dir.mkdir(parents=True, exist_ok=True)
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = export_dir / f"export_art15_{ts}.json"

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    return {
        "status": "OK",
        "right": "Art. 15",
        "output_file": str(output_path),
        "sections_collected": collected,
        "missing_sources": payload["missing_sources"],
        "exported_at": exported_at,
    }


if __name__ == "__main__":
    result = export_user_data()
    print(f"[Art.15] Export OK → {result['output_file']}")
    print(f"  Sections : {', '.join(result['sections_collected'])}")
