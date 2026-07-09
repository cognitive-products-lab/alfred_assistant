# -*- coding: utf-8 -*-
"""
PROJECT      : ALFRED
BLOCK        : B29
FUNCTION     : XX.XX
FILE         : scripts/anonymize_logs_for_hadoop.py
ROLE         : Anonymise/agrège les logs de sécurité avant tout chargement HDFS

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-07-09
UPDATED      : 2026-07-09
VERSION      : V1.0
STATUS       : VALIDATED — exécuté avec succès le 09/07/2026

DESCRIPTION :
PoC Hadoop (Bloc 29, cf. project_bdd_extension_deploiement_public) — étape
obligatoire avant tout chargement HDFS : anonymise/agrège
logs/security/{api_access,audit_trail,soc_alerts}.jsonl vers
data/hadoop_poc/input/. Jamais de log brut chargé dans le PoC.

Anonymisation appliquée (minimisation RGPD) :
- Timestamp tronqué au jour (YYYY-MM-DD) — granularité horaire non
  nécessaire pour une analyse d'usage agrégée.
- api_access : api_key_hash supprimé (déjà un hash, mais reste un
  identifiant stable — retiré car inutile à l'analyse).
- audit_trail : user_id, device_id, request_id supprimés (identifiants
  directs/quasi-directs) ; seuls action/resource/decision/role/risk_score
  sont conservés.
- soc_alerts : message (texte libre, risque de fuite incidentelle)
  supprimé ; seuls source/level/soc_score/soc_level sont conservés.

Usage :
    python scripts/anonymize_logs_for_hadoop.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
LOGS_DIR = ROOT / "logs" / "security"
OUTPUT_DIR = ROOT / "data" / "hadoop_poc" / "input"

_SOURCES = {
    "api_access.jsonl": {
        "keep": ("endpoint", "role", "result"),
    },
    "audit_trail.jsonl": {
        "keep": ("action", "resource", "decision", "role", "risk_score"),
    },
    "soc_alerts.jsonl": {
        "keep": ("source", "level", "soc_score", "soc_level"),
    },
}


def _day(timestamp: str) -> str:
    return timestamp[:10] if timestamp else "unknown"


def anonymize_file(filename: str, keep: tuple[str, ...]) -> int:
    src = LOGS_DIR / filename
    dst = OUTPUT_DIR / filename
    source_tag = filename.removesuffix(".jsonl")
    if not src.is_file():
        print(f"  {filename} — absent, ignoré.")
        return 0

    count = 0
    with src.open(encoding="utf-8") as f_in, dst.open("w", encoding="utf-8") as f_out:
        for line in f_in:
            line = line.strip()
            if not line:
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                continue

            anonymized = {"log_type": source_tag, "date": _day(record.get("timestamp", ""))}
            for field in keep:
                if field in record:
                    anonymized[field] = record[field]

            f_out.write(json.dumps(anonymized, ensure_ascii=False) + "\n")
            count += 1

    return count


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    total = 0
    for filename, config in _SOURCES.items():
        n = anonymize_file(filename, config["keep"])
        print(f"  {filename} — {n} lignes anonymisées.")
        total += n

    print(f"\n{total} lignes anonymisées au total -> {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
