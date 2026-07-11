"""
════════════════════════════════════════════════════════════
PROJECT      : ALFRED
BLOCK        : B10 (ALFRED CPL)
FUNCTION     : 10.06
FILE         : src/security/cpl_role_access.py
ROLE         : Filtrage de la base de connaissances selon les rôles métier CPL

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-07-11
VERSION      : V1.0
STATUS       : ACTIVE

DESCRIPTION :
Applique le principe du moindre privilège aux rôles métier ALFRED CPL
(Chef de projet, RH, ...) en filtrant les connaissances retournées par le
Knowledge Retrieval Engine (B18) selon les domaines autorisés pour chaque
rôle, définis dans config/security/cpl_business_roles.json.
Distinct des rôles système (OWNER, ADMIN...) gérés par role_manager.py :
un rôle non listé ici n'est pas concerné par ce filtre (accès non restreint
par ce module).
════════════════════════════════════════════════════════════
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

_ROOT = Path(__file__).resolve().parents[2]
_CONFIG_PATH = _ROOT / "config" / "security" / "cpl_business_roles.json"

_cache: dict[str, Any] | None = None


def _load_config() -> dict[str, Any]:
    global _cache
    if _cache is None:
        if _CONFIG_PATH.exists():
            with _CONFIG_PATH.open("r", encoding="utf-8") as f:
                _cache = json.load(f)
        else:
            _cache = {"roles": {}}
    return _cache


def reload_config() -> None:
    """Force le rechargement du fichier de configuration (utile pour les tests)."""
    global _cache
    _cache = None
    _load_config()


def is_business_role(role: str) -> bool:
    """True si le rôle est un rôle métier CPL soumis au filtrage par domaine."""
    return bool(role) and role in _load_config().get("roles", {})


def get_allowed_domains(role: str) -> list[str]:
    """Domaines de connaissance autorisés pour un rôle métier CPL. Liste vide si rôle inconnu."""
    role_config = _load_config().get("roles", {}).get(role)
    if not role_config:
        return []
    return list(role_config.get("allowed_knowledge_domains", []))


def is_domain_allowed(role: str, domain: str) -> bool:
    """
    True si le domaine est accessible pour ce rôle.
    Les rôles système (non déclarés comme rôles métier CPL) ne sont pas
    restreints par ce module — ils sont gérés par role_manager.py / access_control.py.
    """
    if not is_business_role(role):
        return True
    return domain in get_allowed_domains(role)


def filter_by_role_access(ranked_items: list, role: str) -> tuple[list, list]:
    """
    Filtre une liste d'objets RankedKnowledge (src.knowledge.knowledge_ranker) selon
    les domaines autorisés pour un rôle métier CPL.

    Retourne (items_autorisés, items_bloqués). Si le rôle n'est pas un rôle métier
    CPL reconnu, retourne la liste complète sans filtrage (items_bloqués vide).
    """
    if not is_business_role(role):
        return ranked_items, []

    allowed: list = []
    blocked: list = []

    for item in ranked_items:
        domain = item.data.get("domain") if item.data else None
        if domain and is_domain_allowed(role, domain):
            allowed.append(item)
        else:
            blocked.append(item)

    return allowed, blocked
