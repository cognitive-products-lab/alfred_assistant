"""
════════════════════════════════════════════════════════════
PROJECT      : ALFRED
BLOCK        : B20
FUNCTION     : 20.18
FILE         : src/security/asset_classifier.py
ROLE         : Cartographie et classification des actifs informationnels

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-06-02
UPDATED      : 2026-06-02
VERSION      : V1.0
STATUS       : ACTIVE

DESCRIPTION :
Urbanisation SSI — Phase 2.
Inventorie automatiquement les actifs informationnels du projet,
les classe selon 4 niveaux de sensibilité (C1→C4) et produit un
rapport JSON exploitable par le dashboard sécurité.

Niveaux de classification :
  C1 — PUBLIC        : données sans restriction (README, docs publics)
  C2 — INTERNE       : données internes (config, logs généraux)
  C3 — CONFIDENTIEL  : données sensibles (data utilisateur, sessions)
  C4 — SECRET        : données critiques (clés, secrets, credentials)
════════════════════════════════════════════════════════════
"""
from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from src.security.security_logger import log_event

# ─── Configuration ────────────────────────────────────────────────────────────

_ROOT = Path(__file__).resolve().parents[2]

# Niveaux de classification
C1_PUBLIC       = "C1_PUBLIC"
C2_INTERNE      = "C2_INTERNE"
C3_CONFIDENTIEL = "C3_CONFIDENTIEL"
C4_SECRET       = "C4_SECRET"

CLASSIFICATION_LABELS = {
    C1_PUBLIC:       "Public — aucune restriction",
    C2_INTERNE:      "Interne — usage projet uniquement",
    C3_CONFIDENTIEL: "Confidentiel — données sensibles utilisateur",
    C4_SECRET:       "Secret — clés cryptographiques et credentials",
}

CLASSIFICATION_ORDER = [C1_PUBLIC, C2_INTERNE, C3_CONFIDENTIEL, C4_SECRET]


# ─── Règles de classification ─────────────────────────────────────────────────
# Format : (regex_chemin, classification, justification)

_CLASSIFICATION_RULES: list[tuple[re.Pattern, str, str]] = [

    # C4 — SECRET
    (re.compile(r"\.env$"),                   C4_SECRET, "Fichier de variables d'environnement — clés et secrets"),
    (re.compile(r"\.env\."),                  C4_SECRET, "Variante .env"),
    (re.compile(r"fernet\.key$"),             C4_SECRET, "Clé de chiffrement Fernet"),
    (re.compile(r"mfa_secrets\.json$"),       C4_SECRET, "Secrets TOTP MFA chiffrés"),
    (re.compile(r"pin_hash\.json$"),          C4_SECRET, "Hash PIN authentification"),
    (re.compile(r"private.*key",    re.I),    C4_SECRET, "Clé privée"),
    (re.compile(r"credentials",     re.I),    C4_SECRET, "Fichier de credentials"),
    (re.compile(r"vault",           re.I),    C4_SECRET, "Coffre de secrets"),
    (re.compile(r"secret",          re.I),    C4_SECRET, "Fichier de secret"),
    (re.compile(r"\.pem$"),                   C4_SECRET, "Certificat/clé PEM"),
    (re.compile(r"\.p12$"),                   C4_SECRET, "Certificat PKCS#12"),
    (re.compile(r"api_key",         re.I),    C4_SECRET, "Clé API"),

    # C3 — CONFIDENTIEL
    (re.compile(r"data/users/",     re.I),    C3_CONFIDENTIEL, "Données utilisateur"),
    (re.compile(r"data/security/",  re.I),    C3_CONFIDENTIEL, "Données sécurité"),
    (re.compile(r"private_data/",   re.I),    C3_CONFIDENTIEL, "Données privées"),
    (re.compile(r"user.*profile",   re.I),    C3_CONFIDENTIEL, "Profil utilisateur"),
    (re.compile(r"personality.*instance", re.I), C3_CONFIDENTIEL, "Instance personnalité"),
    (re.compile(r"dialogue_history", re.I),   C3_CONFIDENTIEL, "Historique dialogues"),
    (re.compile(r"episodic_memory",  re.I),   C3_CONFIDENTIEL, "Mémoire épisodique"),
    (re.compile(r"long_term",        re.I),   C3_CONFIDENTIEL, "Mémoire long terme"),
    (re.compile(r"audit_trail",      re.I),   C3_CONFIDENTIEL, "Piste d'audit"),
    (re.compile(r"incident_register", re.I),  C3_CONFIDENTIEL, "Registre incidents"),
    (re.compile(r"logs/security/",   re.I),   C3_CONFIDENTIEL, "Logs sécurité"),
    (re.compile(r"session",          re.I),   C3_CONFIDENTIEL, "Données de session"),
    (re.compile(r"health_profile",   re.I),   C3_CONFIDENTIEL, "Profil santé"),
    (re.compile(r"preferences",      re.I),   C3_CONFIDENTIEL, "Préférences utilisateur"),

    # C2 — INTERNE
    (re.compile(r"config/",          re.I),   C2_INTERNE, "Configuration interne"),
    (re.compile(r"data/actions/",    re.I),   C2_INTERNE, "Actions et tâches"),
    (re.compile(r"data/memory/",     re.I),   C2_INTERNE, "Mémoire générale"),
    (re.compile(r"logs/",            re.I),   C2_INTERNE, "Journaux"),
    (re.compile(r"backup/",          re.I),   C2_INTERNE, "Sauvegardes"),
    (re.compile(r"dashboard/",       re.I),   C2_INTERNE, "Données dashboard"),
    (re.compile(r"src/",             re.I),   C2_INTERNE, "Code source"),
    (re.compile(r"tests/",           re.I),   C2_INTERNE, "Tests"),
    (re.compile(r"tools/",           re.I),   C2_INTERNE, "Outils"),

    # C1 — PUBLIC (ordre important : évalué en dernier)
    (re.compile(r"README",           re.I),   C1_PUBLIC, "Documentation publique"),
    (re.compile(r"LICENSE",          re.I),   C1_PUBLIC, "Licence"),
    (re.compile(r"knowledges/",      re.I),   C1_PUBLIC, "Base de connaissances"),
    (re.compile(r"ALFRED_WEB/",      re.I),   C1_PUBLIC, "Site web public"),
    (re.compile(r"\.md$"),                    C1_PUBLIC, "Documentation Markdown"),
]

# Dossiers exclus du scan
_EXCLUDED = {
    "__pycache__", ".git", ".venv", "venv", "node_modules",
    "_BACKUPS", ".idea", ".vscode", ".pytest_cache",
}


# ─── Classification d'un fichier ──────────────────────────────────────────────

def classify_path(path: Path) -> tuple[str, str]:
    """
    Classe un fichier selon les règles définies.

    Returns:
        (classification, justification) — C1→C4 + raison textuelle.
    """
    rel = str(path.relative_to(_ROOT)).replace("\\", "/")

    # Priorité aux règles C4 d'abord (ordre décroissant de sensibilité)
    for pattern, level, justif in _CLASSIFICATION_RULES:
        if pattern.search(rel):
            return level, justif

    # Défaut : C2 (interne) pour tout ce qui n'est pas identifié
    return C2_INTERNE, "Fichier projet non classifié explicitement"


def classify_file(path: Path) -> dict[str, Any]:
    """
    Retourne la fiche complète de classification d'un fichier.
    """
    classification, justification = classify_path(path)
    stat = path.stat() if path.exists() else None
    rel  = str(path.relative_to(_ROOT)).replace("\\", "/")

    return {
        "path":           rel,
        "classification": classification,
        "label":          CLASSIFICATION_LABELS.get(classification, ""),
        "justification":  justification,
        "size_bytes":     stat.st_size if stat else 0,
        "exists":         path.exists(),
    }


# ─── Inventaire automatique ───────────────────────────────────────────────────

def scan_assets(
    scan_root: Path | None = None,
    extensions: set[str] | None = None,
    max_files: int = 5000,
) -> list[dict[str, Any]]:
    """
    Inventorie les fichiers du projet et les classe.

    Args:
        scan_root  : répertoire à scanner (défaut : racine projet)
        extensions : extensions à inclure (défaut : .py .json .md .env .key .pem)
        max_files  : limite du nombre de fichiers à scanner

    Returns:
        Liste de fiches de classification.
    """
    root  = scan_root or _ROOT
    exts  = extensions or {".py", ".json", ".md", ".env", ".key", ".pem",
                            ".p12", ".txt", ".yaml", ".toml", ".bat", ".ps1"}
    assets: list[dict] = []
    count = 0

    for path in root.rglob("*"):
        if count >= max_files:
            break
        # Exclure les dossiers
        if any(part in _EXCLUDED for part in path.parts):
            continue
        if not path.is_file():
            continue
        if path.suffix.lower() not in exts and path.name not in {".env", "fernet.key"}:
            continue

        assets.append(classify_file(path))
        count += 1

    log_event(f"asset_classifier: {count} actifs scannés depuis {root}")
    return assets


# ─── Rapport de classification ────────────────────────────────────────────────

def build_classification_report(assets: list[dict] | None = None) -> dict[str, Any]:
    """
    Construit un rapport de classification des actifs.

    Returns:
        dict avec stats par niveau, liste des actifs C3/C4, timestamp.
    """
    if assets is None:
        assets = scan_assets()

    by_level: dict[str, list[dict]] = {c: [] for c in CLASSIFICATION_ORDER}
    for a in assets:
        lvl = a.get("classification", C2_INTERNE)
        by_level.setdefault(lvl, []).append(a)

    # Stats
    stats = {
        lvl: {
            "count":      len(items),
            "label":      CLASSIFICATION_LABELS.get(lvl, ""),
            "total_bytes": sum(i.get("size_bytes", 0) for i in items),
        }
        for lvl, items in by_level.items()
    }

    # Actifs critiques (C3 + C4) pour revue
    critical = [
        a for a in assets
        if a["classification"] in {C3_CONFIDENTIEL, C4_SECRET}
    ]

    return {
        "_meta": {
            "project":    "ALFRED",
            "block":      "B20",
            "file":       "asset_classification_report.json",
            "role":       "Rapport de classification des actifs SSI",
            "version":    "V1.0",
            "status":     "ACTIVE",
            "generated":  datetime.now(timezone.utc).isoformat(),
        },
        "generated_at":  datetime.now(timezone.utc).isoformat(),
        "total_assets":  len(assets),
        "stats":         stats,
        "critical_assets": critical[:50],   # max 50 en rapport
        "critical_count":  len(critical),
        "classification_rules_count": len(_CLASSIFICATION_RULES),
    }


def export_report(output_path: Path | None = None) -> Path:
    """Génère et exporte le rapport de classification en JSON."""
    out = output_path or (_ROOT / "dashboard" / "dashboard_security" / "asset_classification.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    report = build_classification_report()
    out.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    log_event(f"asset_classifier: rapport exporté → {out} ({report['total_assets']} actifs)")
    return out
