"""
════════════════════════════════════════════════════════════
PROJECT      : ALFRED
BLOCK        : Bloc 11.05 — Gouvernance data
FUNCTION     : 11.05 — Automatisation (pilier 8 du framework DQbD, Mémoire M2)
FILE         : tools/dashboard_tools/dashboard_quality_data/scan_data_assets.py
ROLE         : Interroge les vrais moteurs de données d'ALFRED (SQLite ALFRED_PC,
               PostgreSQL/MongoDB ALFRED_WEB) et confronte ce qui existe réellement
               au registre de gouvernance édité à la main
               (dashboard/dashboard_quality_data/data_quality_registry.json).

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-08-11
VERSION      : V1.0
STATUS       : ACTIVE

DESCRIPTION :
Le registre de gouvernance (44 entrées) est aujourd'hui saisi et maintenu à la
main, et scopé à ALFRED_PC uniquement — aucune entrée ne référence les bases
PostgreSQL/MongoDB d'ALFRED_WEB (comptes utilisateurs, articles, conversations).
Ce script ferme cet écart pour le pilier "Automatisation" du framework DQbD
décrit dans le mémoire M2 : il n'affirme rien sur la base d'un document, il
interroge les moteurs réels et signale les divergences.

Ce script est strictement LECTURE SEULE : aucune écriture, aucune migration,
aucune modification sur SQLite/PostgreSQL/MongoDB.

Connexion "paresseuse et tolérante" (même principe que ALFRED_WEB/data/postgres.py
et data/mongo.py) : si une source est injoignable (conteneur Docker non démarré,
driver absent, identifiants manquants), le script le signale comme tel dans le
rapport au lieu d'échouer bruyamment.

⚠️ DASHBOARD INTERNE — comme data_quality_registry.json, ce rapport ne doit
jamais être copié vers ALFRED_WEB/static/dashboard/ ni publié sur le site public.

Usage :
    cd D:/PROJET_ALFRED/ALFRED_PC
    python tools/dashboard_tools/dashboard_quality_data/scan_data_assets.py

Prérequis pour un scan complet (PostgreSQL + MongoDB) :
    cd D:/PROJET_ALFRED/ALFRED_WEB
    docker compose up -d
Sans cela, le script fonctionne quand même (scan SQLite + registre) et signale
clairement les sources WEB comme injoignables, avec la cause.
════════════════════════════════════════════════════════════
"""

from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

PC_ROOT = Path(__file__).resolve().parents[3]
WEB_ROOT = PC_ROOT.parent / "ALFRED_WEB"

REGISTRY_PATH = PC_ROOT / "dashboard" / "dashboard_quality_data" / "data_quality_registry.json"
OUTPUT_PATH = PC_ROOT / "dashboard" / "dashboard_quality_data" / "data_asset_scan_report.json"
SQLITE_DB_PATH = PC_ROOT / "data" / "memory" / "alfred_memory.db"
WEB_ENV_PATH = WEB_ROOT / ".env"


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def load_json(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def load_web_env(path: Path) -> dict[str, str]:
    """Parse minimaliste d'un fichier .env (clé=valeur), sans dépendance externe."""
    env: dict[str, str] = {}
    if not path.exists():
        return env
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        env[key.strip()] = value.strip()
    return env


# ── Scan SQLite (ALFRED_PC) ──────────────────────────────────────────────────

def scan_sqlite(db_path: Path) -> dict[str, Any]:
    if not db_path.exists():
        return {"reachable": False, "reason": f"fichier introuvable : {db_path}", "tables": []}
    try:
        conn = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
        cur = conn.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
        table_names = [r[0] for r in cur.fetchall()]
        tables = []
        for name in table_names:
            cur.execute(f"PRAGMA table_info({name})")
            columns = [r[1] for r in cur.fetchall()]
            cur.execute(f"SELECT COUNT(*) FROM {name}")
            row_count = cur.fetchone()[0]
            tables.append({"table": name, "columns": columns, "row_count": row_count})
        conn.close()
        return {"reachable": True, "engine": "SQLite", "source": str(db_path), "tables": tables}
    except sqlite3.Error as exc:
        return {"reachable": False, "reason": f"erreur SQLite : {exc}", "tables": []}


# ── Scan PostgreSQL (ALFRED_WEB) ─────────────────────────────────────────────

def scan_postgres(database_url: str | None) -> dict[str, Any]:
    if not database_url:
        return {"reachable": False, "reason": "DATABASE_URL absente de ALFRED_WEB/.env", "tables": []}
    try:
        import psycopg2
    except ImportError:
        return {"reachable": False, "reason": "driver psycopg2 non installé", "tables": []}

    try:
        conn = psycopg2.connect(database_url, connect_timeout=3)
    except Exception as exc:  # noqa: BLE001 — on veut capturer toute erreur driver ici
        return {
            "reachable": False,
            "reason": f"connexion impossible ({exc.__class__.__name__}) — le conteneur "
                      f"PostgreSQL d'ALFRED_WEB est-il démarré ? (`docker compose up -d postgres`)",
            "tables": [],
        }

    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT table_name FROM information_schema.tables
            WHERE table_schema = 'public'
            ORDER BY table_name
        """)
        table_names = [r[0] for r in cur.fetchall()]
        tables = []
        for name in table_names:
            cur.execute("""
                SELECT column_name FROM information_schema.columns
                WHERE table_schema = 'public' AND table_name = %s
                ORDER BY ordinal_position
            """, (name,))
            columns = [r[0] for r in cur.fetchall()]
            cur.execute(f'SELECT COUNT(*) FROM "{name}"')
            row_count = cur.fetchone()[0]
            tables.append({"table": name, "columns": columns, "row_count": row_count})
        return {"reachable": True, "engine": "PostgreSQL", "source": "ALFRED_WEB (DATABASE_URL)", "tables": tables}
    finally:
        conn.close()


# ── Scan MongoDB (ALFRED_WEB) ────────────────────────────────────────────────

def scan_mongo(uri: str | None, db_name: str | None) -> dict[str, Any]:
    if not uri:
        return {"reachable": False, "reason": "MONGODB_URI absente de ALFRED_WEB/.env", "collections": []}
    try:
        from pymongo import MongoClient
        from pymongo.errors import PyMongoError
    except ImportError:
        return {"reachable": False, "reason": "driver pymongo non installé", "collections": []}

    try:
        client = MongoClient(uri, serverSelectionTimeoutMS=1500)
        client.admin.command("ping")
    except PyMongoError as exc:
        return {
            "reachable": False,
            "reason": f"connexion impossible ({exc.__class__.__name__}) — le conteneur MongoDB "
                      f"d'ALFRED_WEB est-il démarré ? (`docker compose up -d mongo`)",
            "collections": [],
        }

    db = client[db_name or "alfred_web"]
    collections = []
    for name in sorted(db.list_collection_names()):
        coll = db[name]
        sample = coll.find_one()
        fields = sorted(sample.keys()) if sample else []
        collections.append({"collection": name, "sample_fields": fields, "doc_count": coll.estimated_document_count()})
    client.close()
    return {"reachable": True, "engine": "MongoDB", "source": f"ALFRED_WEB ({db_name})", "collections": collections}


# ── Confrontation avec le registre de gouvernance ────────────────────────────

def build_asset_index(sqlite_result: dict, postgres_result: dict, mongo_result: dict) -> list[dict]:
    """Liste plate de tous les actifs réels trouvés, indépendamment de leur moteur."""
    assets = []
    for t in sqlite_result.get("tables", []):
        assets.append({"engine": "SQLite", "asset": f"table:{t['table']}", "columns": t["columns"], "row_count": t["row_count"]})
    for t in postgres_result.get("tables", []):
        assets.append({"engine": "PostgreSQL", "asset": f"table:{t['table']}", "columns": t["columns"], "row_count": t["row_count"]})
    for c in mongo_result.get("collections", []):
        assets.append({"engine": "MongoDB", "asset": f"collection:{c['collection']}", "columns": c["sample_fields"], "row_count": c["doc_count"]})
    return assets


def check_registry_coverage(assets: list[dict], registry_entries: list[dict]) -> dict[str, Any]:
    """
    Le registre actuel ne référence que des chemins de fichiers ALFRED_PC
    (source_path), jamais des tables/collections ALFRED_WEB. On calcule donc,
    honnêtement, ce qui est réellement couvert vs non couvert plutôt que de
    forcer un matching approximatif texte-libre qui donnerait un faux sentiment
    de correspondance.
    """
    registered_paths = " ".join((e.get("source_path") or "") for e in registry_entries).lower()

    covered, uncovered = [], []
    for a in assets:
        needle = a["asset"].split(":", 1)[1].lower()
        if a["engine"] != "SQLite" and needle in registered_paths:
            covered.append(a)
        elif a["engine"] == "SQLite":
            # DQ-002 référence explicitement data/memory/... (mémoire épisodique)
            covered.append(a) if "memory" in registered_paths else uncovered.append(a)
        else:
            uncovered.append(a)
    return {
        "covered_count": len(covered),
        "uncovered_count": len(uncovered),
        "uncovered_assets": uncovered,
        "note": "Un actif 'non couvert' n'est pas forcément un manquement : ça signifie "
                "qu'aucune fiche DQ-xxx du registre ne le référence explicitement "
                "aujourd'hui. Pour PostgreSQL/MongoDB (ALFRED_WEB), c'est structurel "
                "tant que le registre reste scopé ALFRED_PC — action de suivi : ajouter "
                "des fiches DQ dédiées (comptes utilisateurs, articles, conversations).",
    }


def build_report() -> dict[str, Any]:
    registry = load_json(REGISTRY_PATH)
    registry_entries = registry.get("entries", [])

    web_env = load_web_env(WEB_ENV_PATH)

    sqlite_result = scan_sqlite(SQLITE_DB_PATH)
    postgres_result = scan_postgres(web_env.get("DATABASE_URL"))
    mongo_result = scan_mongo(web_env.get("MONGODB_URI"), web_env.get("MONGODB_DB"))

    assets = build_asset_index(sqlite_result, postgres_result, mongo_result)
    coverage = check_registry_coverage(assets, registry_entries)

    sources = {"sqlite_alfred_pc": sqlite_result, "postgresql_alfred_web": postgres_result, "mongodb_alfred_web": mongo_result}
    unreachable = {k: v["reason"] for k, v in sources.items() if not v.get("reachable")}

    return {
        "_alfred_header": {
            "file": "dashboard/dashboard_quality_data/data_asset_scan_report.json",
            "bloc": "Bloc 11.05 — Gouvernance data",
            "notion_exam": "D11-5 — Capsule Gouvernance de la donnée",
            "utilite_alfred": "Confronte le registre de gouvernance (saisi à la main) aux "
                               "moteurs de données réels (SQLite/PostgreSQL/MongoDB) — "
                               "implémentation du pilier Automatisation du framework DQbD.",
            "domaine": "Gouvernance de la donnée — automatisation, traçabilité",
        },
        "_meta": {
            "project": "ALFRED",
            "generated_at": _now_iso(),
            "generated_by": "scan_data_assets.py",
            "version": "V1.0",
            "visibility": "PRIVE",
            "visibility_note": "Dashboard interne — jamais publié sur ALFRED_WEB.",
            "read_only": True,
        },
        "sources_scanned": sources,
        "unreachable_sources": unreachable,
        "real_assets_found": {
            "total": len(assets),
            "by_engine": {
                "SQLite": sum(1 for a in assets if a["engine"] == "SQLite"),
                "PostgreSQL": sum(1 for a in assets if a["engine"] == "PostgreSQL"),
                "MongoDB": sum(1 for a in assets if a["engine"] == "MongoDB"),
            },
            "assets": assets,
        },
        "registry_coverage": coverage,
    }


if __name__ == "__main__":
    print("Scan des actifs de données réels (SQLite ALFRED_PC + PostgreSQL/MongoDB ALFRED_WEB)...")
    report = build_report()
    OUTPUT_PATH.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")

    for name, reason in report["unreachable_sources"].items():
        print(f"  [injoignable] {name} : {reason}")

    found = report["real_assets_found"]
    print(f"Actifs réels trouvés : {found['total']} ({found['by_engine']})")
    cov = report["registry_coverage"]
    print(f"Couverture registre : {cov['covered_count']} couverts / {cov['uncovered_count']} non couverts")
    print(f"Rapport : {OUTPUT_PATH}")
