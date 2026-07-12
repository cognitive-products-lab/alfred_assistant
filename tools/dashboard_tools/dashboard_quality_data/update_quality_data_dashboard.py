"""
════════════════════════════════════════════════════════════
PROJECT      : ALFRED
BLOCK        : Bloc 11.05 — Gouvernance data
FUNCTION     : 11.05
FILE         : tools/dashboard_tools/dashboard_quality_data/update_quality_data_dashboard.py
ROLE         : Génère dashboard_quality_data.json depuis data_quality_registry.json

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-07-12
VERSION      : V1.0
STATUS       : ACTIVE

DESCRIPTION :
Lit le registre éditable data_quality_registry.json (une fiche par donnée/actif
data : documentée ? définie ? statut, type, sensibilité, usage prévu, durée de
conservation, fréquence de mise à jour, niveau de sécurité prévu 1→5, rôles
autorisés, dates de création/modif/purge prévue), calcule les alertes de
gouvernance (accès non autorisé, donnée non définie, statut obsolète, donnée
créée mais non utilisée, purge en retard) et écrit le résultat consommé par
dashboard_quality_data_dynamique.html.

⚠️ DASHBOARD INTERNE — ne jamais ajouter ce fichier à tools/sync_dashboards.py :
il ne doit jamais être copié vers ALFRED_WEB/static/dashboard/ ni publié sur le
site public. Les statistiques publiables seront sélectionnées manuellement plus
tard, au cas par cas, par un autre mécanisme.

Usage :
    cd D:/PROJET_ALFRED/ALFRED_PC
    python tools/dashboard_tools/dashboard_quality_data/update_quality_data_dashboard.py
════════════════════════════════════════════════════════════
"""

from __future__ import annotations

import json
from datetime import datetime, date, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[3]

DASHBOARD_DIR = ROOT / "dashboard" / "dashboard_quality_data"
REGISTRY_PATH = DASHBOARD_DIR / "data_quality_registry.json"
OUTPUT_PATH = DASHBOARD_DIR / "dashboard_quality_data.json"
ROLES_PATH = ROOT / "config" / "security" / "roles_permissions.json"

# Nombre de jours au-delà duquel une donnée "à créer / à connecter / utilisable"
# non encore utilisée est considérée comme "créée mais non utilisée" (alerte).
STALE_UNUSED_DAYS = 90

# Ordre de séniorité des niveaux d'habilitation (config/security/roles_permissions.json)
CLEARANCE_ORDER = {"LOW": 1, "MEDIUM": 2, "CRITICAL": 3}

# Habilitation minimale requise pour lire une donnée selon son security_level_planned (1→5)
MIN_CLEARANCE_BY_SECURITY_LEVEL = {
    1: "LOW",
    2: "LOW",
    3: "MEDIUM",
    4: "CRITICAL",
    5: "CRITICAL",
}

STATUS_VALUES = {"a_creer", "a_connecter", "utilisable", "utilisee", "obsolete"}
NON_CREATED_STATUSES = {"a_creer"}  # pas encore de donnée physique → pas d'alerte "non utilisée"


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def load_json(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def _parse_date(value: str | None) -> date | None:
    if not value:
        return None
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError:
        return None


def load_roles() -> dict[str, dict]:
    data = load_json(ROLES_PATH)
    return data.get("roles", {})


# ── Alertes ─────────────────────────────────────────────────────────────────

def check_undefined(entry: dict) -> list[dict]:
    """Donnée non documentée et/ou non définie."""
    alerts = []
    if not entry.get("documented"):
        alerts.append(_alert(
            entry, "donnee_non_documentee",
            "critical" if entry.get("status") == "utilisee" else "warning",
            f"Donnée non documentée : {entry.get('name')}",
        ))
    if not entry.get("defined"):
        alerts.append(_alert(
            entry, "donnee_non_definie",
            "critical" if entry.get("status") == "utilisee" else "warning",
            f"Donnée non définie (schéma/périmètre à préciser) : {entry.get('name')}",
        ))
    return alerts


def check_obsolete(entry: dict) -> list[dict]:
    if entry.get("status") == "obsolete":
        return [_alert(
            entry, "statut_obsolete", "warning",
            f"Statut obsolète — à archiver ou supprimer : {entry.get('name')}",
        )]
    return []


def check_created_but_unused(entry: dict, today: date) -> list[dict]:
    status = entry.get("status")
    if status not in {"a_connecter", "utilisable"}:
        return []
    created = _parse_date(entry.get("created_at"))
    if not created:
        return []
    age_days = (today - created).days
    if age_days < STALE_UNUSED_DAYS:
        return []
    return [_alert(
        entry, "donnee_creee_non_utilisee", "warning",
        f"Créée il y a {age_days} jours et toujours '{status}' — jamais branchée en "
        f"usage courant : {entry.get('name')}. Parfois normal en cours de "
        f"construction, parfois signe d'une collecte finalement inutile.",
    )]


def check_access_control(entry: dict, roles: dict[str, dict]) -> list[dict]:
    alerts = []
    status = entry.get("status")
    authorized = entry.get("authorized_roles") or {}
    read_roles = authorized.get("read") or []
    write_roles = authorized.get("write") or []
    level = entry.get("security_level_planned")

    if status in {"utilisable", "utilisee"} and not read_roles:
        alerts.append(_alert(
            entry, "controle_acces_absent", "critical",
            f"Aucun rôle autorisé en lecture défini pour une donnée '{status}' : {entry.get('name')}",
        ))

    if isinstance(level, int):
        min_clearance = MIN_CLEARANCE_BY_SECURITY_LEVEL.get(level, "CRITICAL")
        min_rank = CLEARANCE_ORDER.get(min_clearance, 3)
        for role_name in set(read_roles) | set(write_roles):
            role_info = roles.get(role_name)
            if role_info is None:
                alerts.append(_alert(
                    entry, "acces_role_inconnu", "warning",
                    f"Rôle '{role_name}' référencé pour {entry.get('name')} mais absent de "
                    f"config/security/roles_permissions.json",
                ))
                continue
            role_rank = CLEARANCE_ORDER.get(role_info.get("max_resource_sensitivity", "LOW"), 1)
            if role_rank < min_rank:
                alerts.append(_alert(
                    entry, "acces_non_autorise", "critical",
                    f"Rôle '{role_name}' (habilitation {role_info.get('max_resource_sensitivity')}) "
                    f"a accès à '{entry.get('name')}' qui exige au moins {min_clearance} "
                    f"(niveau de sécurité prévu {level}/5)",
                ))
    return alerts


def check_deletion_overdue(entry: dict, today: date) -> list[dict]:
    planned = _parse_date(entry.get("planned_deletion_at"))
    if not planned:
        return []
    if planned < today and entry.get("status") != "obsolete":
        return [_alert(
            entry, "purge_en_retard", "warning",
            f"Date d'effacement prévue dépassée ({entry.get('planned_deletion_at')}) : {entry.get('name')}",
        )]
    return []


def _alert(entry: dict, alert_type: str, severity: str, message: str) -> dict:
    return {
        "entry_id": entry.get("id"),
        "entry_name": entry.get("name"),
        "type": alert_type,
        "severity": severity,
        "message": message,
    }


def compute_alerts(entries: list[dict], roles: dict[str, dict], today: date) -> list[dict]:
    alerts: list[dict] = []
    for entry in entries:
        alerts.extend(check_undefined(entry))
        alerts.extend(check_obsolete(entry))
        alerts.extend(check_created_but_unused(entry, today))
        alerts.extend(check_access_control(entry, roles))
        alerts.extend(check_deletion_overdue(entry, today))
    severity_rank = {"critical": 0, "warning": 1, "info": 2}
    alerts.sort(key=lambda a: severity_rank.get(a["severity"], 9))
    return alerts


# ── Agrégats ───────────────────────────────────────────────────────────────

def _count_by(entries: list[dict], key: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for entry in entries:
        value = entry.get(key)
        if isinstance(value, list):
            for v in value:
                counts[v] = counts.get(v, 0) + 1
        else:
            label = str(value) if value is not None else "non_renseigne"
            counts[label] = counts.get(label, 0) + 1
    return counts


def build_dashboard() -> dict[str, Any]:
    registry = load_json(REGISTRY_PATH)
    entries = registry.get("entries", [])
    roles = load_roles()
    today = datetime.now(timezone.utc).date()

    alerts = compute_alerts(entries, roles, today)
    alerts_by_severity = _count_by(alerts, "severity")

    data: dict[str, Any] = {
        "_alfred_header": {
            "file": "dashboard/dashboard_quality_data/dashboard_quality_data.json",
            "bloc": "Bloc 11.05 — Gouvernance data",
            "notion_exam": "D11-5 — Capsule Gouvernance de la donnée",
            "utilite_alfred": "Dashboard interne de gouvernance/qualité des données ALFRED (documentation, "
                               "définition, statut, sensibilité, sécurité, accès, cycle de vie).",
            "domaine": "Gouvernance de la donnée — qualité, cycle de vie, sécurité",
        },
        "_meta": {
            "project": "ALFRED",
            "file": "dashboard_quality_data.json",
            "generated_at": _now_iso(),
            "generated_by": "update_quality_data_dashboard.py",
            "version": "V1.0",
            "visibility": "PRIVE",
            "visibility_note": "Dashboard interne — jamais publié sur ALFRED_WEB. Les statistiques "
                                "publiables seront sélectionnées manuellement au cas par cas.",
            "source_registry": "dashboard/dashboard_quality_data/data_quality_registry.json",
            "stale_unused_threshold_days": STALE_UNUSED_DAYS,
        },
        "global": {
            "total_entries": len(entries),
            "by_status": _count_by(entries, "status"),
            "by_data_type": _count_by(entries, "data_type"),
            "by_sensitivity_classification": _count_by(entries, "sensitivity_classification"),
            "by_security_level_planned": _count_by(entries, "security_level_planned"),
            "by_intended_use": _count_by(entries, "intended_use"),
            "documented_count": sum(1 for e in entries if e.get("documented")),
            "defined_count": sum(1 for e in entries if e.get("defined")),
            "undocumented_count": sum(1 for e in entries if not e.get("documented")),
            "undefined_count": sum(1 for e in entries if not e.get("defined")),
        },
        "alerts": {
            "total": len(alerts),
            "by_severity": alerts_by_severity,
            "items": alerts,
        },
        "entries": entries,
        "scales": registry.get("scales", {}),
    }
    return data


if __name__ == "__main__":
    DASHBOARD_DIR.mkdir(parents=True, exist_ok=True)
    print("Génération dashboard_quality_data.json (interne — non publiable)...")
    dashboard = build_dashboard()
    OUTPUT_PATH.write_text(
        json.dumps(dashboard, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    g = dashboard["global"]
    a = dashboard["alerts"]
    print(f"Entrées : {g['total_entries']} — non documentées : {g['undocumented_count']} — non définies : {g['undefined_count']}")
    print(f"Alertes : {a['total']} (par sévérité : {a['by_severity']})")
    print(f"Fichier : {OUTPUT_PATH}")
