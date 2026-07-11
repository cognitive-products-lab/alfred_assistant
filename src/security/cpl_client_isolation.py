"""
════════════════════════════════════════════════════════════
PROJECT      : ALFRED
BLOCK        : B10 (ALFRED CPL)
FUNCTION     : 10.07
FILE         : src/security/cpl_client_isolation.py
ROLE         : Isolation des bases de connaissances entre entreprises clientes

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-07-11
VERSION      : V1.0
STATUS       : ACTIVE

DESCRIPTION :
Applique la séparation stricte entre les bases de connaissances des
différentes entreprises clientes d'ALFRED CPL (spec section 3 —
"Personnalisation pour chaque entreprise cliente" / "Séparation stricte
entre les bases de connaissances des différents clients").

Une connaissance sans champ "client_scope" est transversale (socle métier
commun) et reste visible quel que soit le client. Une connaissance portant
"client_scope": "<client_id>" n'est visible que pour les requêtes de ce
client précis — jamais pour un autre client, jamais sans contexte client.

Distinct de src/security/cpl_role_access.py (filtrage par rôle métier au
sein d'un même client) : les deux filtres se cumulent dans le pipeline de
retrieval (src/knowledge/retrieval_engine.py).
════════════════════════════════════════════════════════════
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

_ROOT = Path(__file__).resolve().parents[2]
_CONFIG_PATH = _ROOT / "config" / "security" / "cpl_clients.json"

_cache: dict[str, Any] | None = None


def _load_config() -> dict[str, Any]:
    global _cache
    if _cache is None:
        if _CONFIG_PATH.exists():
            with _CONFIG_PATH.open("r", encoding="utf-8") as f:
                _cache = json.load(f)
        else:
            _cache = {"clients": {}}
    return _cache


def reload_config() -> None:
    """Force le rechargement du fichier de configuration (utile pour les tests)."""
    global _cache
    _cache = None
    _load_config()


def is_known_client(client_id: str) -> bool:
    """True si client_id est un client enregistré (registre config/security/cpl_clients.json)."""
    return bool(client_id) and client_id in _load_config().get("clients", {})


def get_client_label(client_id: str) -> str:
    """Libellé lisible d'un client, ou son identifiant brut s'il est inconnu."""
    client_config = _load_config().get("clients", {}).get(client_id)
    return client_config.get("label", client_id) if client_config else client_id


def is_client_scope_allowed(client_id: str, client_scope: str | None) -> bool:
    """
    True si une connaissance portant ce client_scope peut être exposée à ce client_id.

    - client_scope vide/absent → connaissance transversale (socle commun), toujours visible.
    - client_scope renseigné → visible uniquement si client_id correspond exactement.
      Sans client_id (contexte hors client, ex. ALFRED personnel), ces connaissances
      restent invisibles — pas d'accès par défaut aux données d'un client.
    """
    if not client_scope:
        return True
    return bool(client_id) and client_id == client_scope


def filter_by_client_access(ranked_items: list, client_id: str) -> tuple[list, list]:
    """
    Filtre une liste d'objets RankedKnowledge (src.knowledge.knowledge_ranker) selon
    le client_scope de chaque connaissance.

    Retourne (items_autorisés, items_bloqués).
    """
    allowed: list = []
    blocked: list = []

    for item in ranked_items:
        raw_data = item.data.get("data", {}) if item.data else {}
        client_scope = raw_data.get("client_scope")

        if is_client_scope_allowed(client_id, client_scope):
            allowed.append(item)
        else:
            blocked.append(item)

    return allowed, blocked
