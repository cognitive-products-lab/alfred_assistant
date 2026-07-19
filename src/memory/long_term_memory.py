# ============================================================
# ALFRED — src/memory/long_term_memory.py
# Bloc 02.02 — Mémoire longue
#
# 📚 NOTION EXAM :
#   D21-2 — Capsule 2 : Mémoire persistante SQLite et compression
#
# 🎯 UTILITÉ ALFRED :
#   Stocke les souvenirs à long terme via SQLite local (HDD 4To) ;
#   indexe par date/sujet, compresse/résume et implémente l'oubli RGPD.
#
# 🏗️ DOMAINE :
#   Mémoire & contexte — SQLite local-first, recherche sémantique V3
#
# UPDATED : 2026-06-10 — chemins _DB_DIR/_DB_PATH ancrés sur paths.PATHS
# STATUS  : VALIDATED (auto: tests/test_b02_b03.py OK le 2026-07-05 ; cwd réel encore à reconfirmer)
# ============================================================

import json
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

from src.security.security_logger import log_event
from paths import PATHS

# ── Chemins ───────────────────────────────────────────────
# Ancré sur la racine du projet (paths.py, basé sur __file__) — ne dépend pas
# du répertoire de travail courant au lancement de main.py.
_DB_DIR  = PATHS.data_memory
_DB_PATH = _DB_DIR / "alfred_memory.db"
_DB_DIR.mkdir(parents=True, exist_ok=True)


# ─────────────────────────────────────────────────────────
# Init base SQLite
# ─────────────────────────────────────────────────────────

def _get_conn() -> sqlite3.Connection:
    """Retourne une connexion SQLite avec row_factory."""
    conn = sqlite3.connect(str(_DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    """
    Crée les tables SQLite si elles n'existent pas.
    Appelé au démarrage d'ALFRED.
    """
    with _get_conn() as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS memories (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id  TEXT NOT NULL,
                timestamp   TEXT NOT NULL,
                user_input  TEXT,
                alfred_resp TEXT,
                intent      TEXT DEFAULT 'general',
                emotion     TEXT DEFAULT 'neutral',
                topic       TEXT,
                importance  REAL DEFAULT 0.5,
                archived    INTEGER DEFAULT 0
            );

            CREATE TABLE IF NOT EXISTS facts (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                key         TEXT NOT NULL UNIQUE,
                value       TEXT NOT NULL,
                category    TEXT DEFAULT 'general',
                created_at  TEXT NOT NULL,
                updated_at  TEXT NOT NULL,
                source      TEXT DEFAULT 'user'
            );

            CREATE TABLE IF NOT EXISTS patterns (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                pattern_key TEXT NOT NULL,
                count       INTEGER DEFAULT 1,
                last_seen   TEXT NOT NULL,
                category    TEXT DEFAULT 'behavior'
            );

            CREATE INDEX IF NOT EXISTS idx_memories_intent   ON memories(intent);
            CREATE INDEX IF NOT EXISTS idx_memories_emotion  ON memories(emotion);
            CREATE INDEX IF NOT EXISTS idx_memories_session  ON memories(session_id);
            CREATE INDEX IF NOT EXISTS idx_facts_key         ON facts(key);
        """)
    log_event("Base mémoire long terme initialisée")


# ─────────────────────────────────────────────────────────
# Écriture mémoire (02.02.001)
# ─────────────────────────────────────────────────────────

def save_exchange(
    session_id: str,
    user_input: str,
    alfred_response: str,
    intent: str = "general",
    emotion: str = "neutral",
    topic: str | None = None,
    importance: float = 0.5,
) -> int:
    """
    Sauvegarde un échange en mémoire long terme SQLite.

    Args:
        session_id      : ID de session
        user_input      : Message utilisateur
        alfred_response : Réponse ALFRED
        intent          : Intention détectée
        emotion         : Émotion détectée
        topic           : Sujet principal
        importance      : Score importance (0.0 → 1.0)

    Returns:
        ID de la ligne insérée
    """
    with _get_conn() as conn:
        cursor = conn.execute("""
            INSERT INTO memories
            (session_id, timestamp, user_input, alfred_resp, intent, emotion, topic, importance)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            session_id,
            datetime.now().isoformat(),
            user_input,
            alfred_response,
            intent,
            emotion,
            topic or intent,
            importance,
        ))
        return cursor.lastrowid


def save_fact(key: str, value: Any, category: str = "general", source: str = "user") -> None:
    """
    Sauvegarde ou met à jour un fait connu sur l'utilisateur.

    Exemples :
        save_fact("prénom", "Céline")
        save_fact("projet_actuel", "ALFRED")
        save_fact("langages_maîtrisés", ["Python", "SQL"])

    Args:
        key      : Identifiant unique du fait
        value    : Valeur (sérialisée si non-str)
        category : Catégorie (profil / projet / préférence / contexte)
        source   : Origine de l'info (user / system / inference)
    """
    value_str = json.dumps(value, ensure_ascii=False) if not isinstance(value, str) else value
    now = datetime.now().isoformat()

    with _get_conn() as conn:
        conn.execute("""
            INSERT INTO facts (key, value, category, created_at, updated_at, source)
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(key) DO UPDATE SET
                value = excluded.value,
                updated_at = excluded.updated_at,
                source = excluded.source
        """, (key, value_str, category, now, now, source))


# ─────────────────────────────────────────────────────────
# Lecture mémoire (02.02.002)
# ─────────────────────────────────────────────────────────

def get_recent_memories(n: int = 20, intent: str | None = None) -> list[dict]:
    """
    Récupère les N mémoires les plus récentes.

    Args:
        n      : Nombre de mémoires
        intent : Filtre optionnel par intention

    Returns:
        Liste de dicts mémoire
    """
    with _get_conn() as conn:
        if intent:
            rows = conn.execute("""
                SELECT * FROM memories
                WHERE archived = 0 AND intent = ?
                ORDER BY timestamp DESC LIMIT ?
            """, (intent, n)).fetchall()
        else:
            rows = conn.execute("""
                SELECT * FROM memories
                WHERE archived = 0
                ORDER BY timestamp DESC LIMIT ?
            """, (n,)).fetchall()
    return [dict(r) for r in rows]


def get_fact(key: str) -> Any | None:
    """
    Récupère un fait connu.

    Args:
        key : Clé du fait

    Returns:
        Valeur désérialisée ou None
    """
    with _get_conn() as conn:
        row = conn.execute("SELECT value FROM facts WHERE key = ?", (key,)).fetchone()
    if row is None:
        return None
    try:
        return json.loads(row["value"])
    except (json.JSONDecodeError, TypeError):
        return row["value"]


def get_all_facts(category: str | None = None) -> dict:
    """
    Récupère tous les faits connus.

    Args:
        category : Filtre optionnel par catégorie

    Returns:
        Dict key → value
    """
    with _get_conn() as conn:
        if category:
            rows = conn.execute(
                "SELECT key, value FROM facts WHERE category = ?", (category,)
            ).fetchall()
        else:
            rows = conn.execute("SELECT key, value FROM facts").fetchall()

    result = {}
    for row in rows:
        try:
            result[row["key"]] = json.loads(row["value"])
        except (json.JSONDecodeError, TypeError):
            result[row["key"]] = row["value"]
    return result


def search_memories(keyword: str, limit: int = 10) -> list[dict]:
    """
    Recherche textuelle simple dans les mémoires.
    V3 : remplacée par recherche sémantique ChromaDB.

    Args:
        keyword : Mot-clé à chercher
        limit   : Nombre max de résultats

    Returns:
        Liste de mémoires correspondantes
    """
    with _get_conn() as conn:
        rows = conn.execute("""
            SELECT * FROM memories
            WHERE archived = 0
            AND (user_input LIKE ? OR alfred_resp LIKE ? OR topic LIKE ?)
            ORDER BY importance DESC, timestamp DESC
            LIMIT ?
        """, (f"%{keyword}%", f"%{keyword}%", f"%{keyword}%", limit)).fetchall()
    return [dict(r) for r in rows]


# ─────────────────────────────────────────────────────────
# Patterns comportementaux (02.02.002)
# ─────────────────────────────────────────────────────────

def record_pattern(pattern_key: str, category: str = "behavior") -> int:
    """
    Enregistre ou incrémente un pattern comportemental.

    Args:
        pattern_key : Identifiant du pattern (ex: "fatigue_soir")
        category    : Catégorie du pattern

    Returns:
        Nouveau compteur
    """
    now = datetime.now().isoformat()
    with _get_conn() as conn:
        existing = conn.execute(
            "SELECT id, count FROM patterns WHERE pattern_key = ?",
            (pattern_key,)
        ).fetchone()

        if existing:
            new_count = existing["count"] + 1
            conn.execute(
                "UPDATE patterns SET count = ?, last_seen = ? WHERE id = ?",
                (new_count, now, existing["id"])
            )
            return new_count
        else:
            conn.execute(
                "INSERT INTO patterns (pattern_key, count, last_seen, category) VALUES (?,?,?,?)",
                (pattern_key, 1, now, category)
            )
            return 1


def get_top_patterns(n: int = 5) -> list[dict]:
    """Retourne les patterns les plus fréquents."""
    with _get_conn() as conn:
        rows = conn.execute(
            "SELECT * FROM patterns ORDER BY count DESC LIMIT ?", (n,)
        ).fetchall()
    return [dict(r) for r in rows]


# ─────────────────────────────────────────────────────────
# Archivage / RGPD (02.02.005)
# ─────────────────────────────────────────────────────────

def archive_old_memories(days: int = 90) -> int:
    """
    Archive les mémoires plus anciennes que N jours.

    Args:
        days : Ancienneté seuil en jours

    Returns:
        Nombre de mémoires archivées
    """
    cutoff = (datetime.now() - timedelta(days=days)).isoformat()
    with _get_conn() as conn:
        cursor = conn.execute(
            "UPDATE memories SET archived = 1 WHERE timestamp < ? AND archived = 0",
            (cutoff,)
        )
        count = cursor.rowcount
    if count > 0:
        log_event(f"{count} mémoires archivées (>{days} jours)")
    return count


def delete_all_memories(confirm: bool = False) -> bool:
    """
    Supprime toutes les mémoires (droit RGPD à l'effacement).

    Args:
        confirm : Doit être True pour exécuter

    Returns:
        True si suppression effectuée
    """
    if not confirm:
        log_event("Suppression mémoires refusée : confirmation manquante", "WARNING")
        return False

    with _get_conn() as conn:
        conn.executescript("DELETE FROM memories; DELETE FROM facts; DELETE FROM patterns;")
    log_event("RGPD : toutes les mémoires supprimées", "WARNING")
    return True


# ─────────────────────────────────────────────────────────
# Stats mémoire
# ─────────────────────────────────────────────────────────

def get_memory_stats() -> dict:
    """Retourne des statistiques sur la mémoire long terme."""
    with _get_conn() as conn:
        total     = conn.execute("SELECT COUNT(*) FROM memories WHERE archived=0").fetchone()[0]
        archived  = conn.execute("SELECT COUNT(*) FROM memories WHERE archived=1").fetchone()[0]
        facts_cnt = conn.execute("SELECT COUNT(*) FROM facts").fetchone()[0]
        patterns  = conn.execute("SELECT COUNT(*) FROM patterns").fetchone()[0]

    return {
        "memories_active":   total,
        "memories_archived": archived,
        "facts":             facts_cnt,
        "patterns":          patterns,
        "db_path":           str(_DB_PATH),
        "version":           "sqlite_v1",
    }
