"""
PROJECT      : ALFRED
BLOCK        : B03
FUNCTION     : SMOKE
FILE         : tests/b03_tests/test_smoke_knowledge_batch1.py
ROLE         : Smoke tests (lot 1) pour les fichiers JSON de connaissance
               emotionnelle/psychologique B03 sans couverture de test.

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-07-05
UPDATED      : 2026-07-05
VERSION      : V1.0
STATUS       : TESTED

DESCRIPTION :
Verifie la structure de base (cles communes) des fichiers de connaissance
consommes par KnowledgeLoader. Ne remplace pas une validation semantique
complete du contenu.
"""

import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]

KNOWLEDGE_FILES = [
    "knowledges/human/cognition/decision_fatigue.json",
    "knowledges/human/emotional_intelligence/active_listening.json",
    "knowledges/human/emotional_intelligence/emotional_management.json",
    "knowledges/human/emotional_intelligence/emotional_patterns.json",
    "knowledges/human/psychology/burnout_prevention.json",
    "knowledges/human/psychology/resilience.json",
]


@pytest.mark.parametrize("relpath", KNOWLEDGE_FILES)
def test_knowledge_json_has_expected_structure(relpath):
    data = json.loads((ROOT / relpath).read_text(encoding="utf-8"))
    for key in ("metadata", "knowledge_id", "title", "summary"):
        assert key in data, f"clé '{key}' manquante dans {relpath}"
    assert isinstance(data["title"], str) and data["title"].strip()
    assert isinstance(data["summary"], str) and data["summary"].strip()
