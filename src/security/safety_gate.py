"""
════════════════════════════════════════════════════════════
PROJECT      : ALFRED
BLOCK        : B01
FUNCTION     : 01.04
FILE         : safety_gate.py
ROLE         : SafetyNet — blocage du cloud pour contenu sensible avant repli LLM externe

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-08-14
UPDATED      : 2026-08-14
VERSION      : V1.0
STATUS       : ACTIVE

DESCRIPTION :
Classe un prompt utilisateur par mots-clés (santé, sécurité domicile,
données de tiers) et détermine s'il peut partir vers un LLM cloud
(OpenAI/Anthropic) en cas de repli. Niveau 0 du principe de sobriété
cognitive (règles explicites, pas de ML) — voir
docs/architecture/vision_architecture_cognitive_alfred.md, section P0.
════════════════════════════════════════════════════════════
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from src.security.security_logger import log_event

_ROOT = Path(__file__).resolve().parents[2]
_RULES_PATH = _ROOT / "config" / "safety_rules.json"


def _load_rules() -> dict[str, Any]:
    try:
        with open(_RULES_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"cloud_blocked_categories": {}, "cloud_allowed_default": True}


def assess_prompt_sensitivity(text: str) -> dict[str, Any]:
    """
    Évalue si `text` déclenche un blocage du repli cloud.

    Retourne :
        {"privacy_level": "LOCAL_ONLY" | "STANDARD",
         "cloud_allowed": bool,
         "matched_categories": [str, ...]}
    """
    rules = _load_rules()
    categories: dict[str, list[str]] = rules.get("cloud_blocked_categories", {})
    default_allowed = rules.get("cloud_allowed_default", True)

    if not isinstance(text, str) or not text.strip():
        return {
            "privacy_level": "STANDARD",
            "cloud_allowed": default_allowed,
            "matched_categories": [],
        }

    lowered = text.lower()
    matched = [
        category
        for category, keywords in categories.items()
        if any(keyword.lower() in lowered for keyword in keywords)
    ]

    cloud_allowed = default_allowed and not matched
    privacy_level = "LOCAL_ONLY" if matched else "STANDARD"

    if matched:
        log_event(
            f"SafetyGate : repli cloud bloqué — catégories détectées {matched}",
            "WARNING",
        )

    return {
        "privacy_level": privacy_level,
        "cloud_allowed": cloud_allowed,
        "matched_categories": matched,
    }


def is_cloud_allowed(text: str) -> bool:
    """Raccourci booléen utilisé par ResponseGenerator avant l'appel LLM."""
    return assess_prompt_sensitivity(text)["cloud_allowed"]
