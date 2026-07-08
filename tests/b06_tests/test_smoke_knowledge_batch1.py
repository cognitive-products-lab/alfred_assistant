"""
PROJECT      : ALFRED
BLOCK        : B06
FUNCTION     : SMOKE
FILE         : tests/b06_tests/test_smoke_knowledge_batch1.py
ROLE         : Smoke tests (lot 1) pour les fichiers JSON softskills B06
               sans couverture de test.

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-07-05
UPDATED      : 2026-07-05
VERSION      : V1.0
STATUS       : TESTED
"""

import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]

KNOWLEDGE_FILES = [
    "knowledges/human/skills/softskills/argumentation_frameworks.json",
    "knowledges/human/skills/softskills/assertiveness.json",
    "knowledges/human/skills/softskills/communication_clarity.json",
    "knowledges/human/skills/softskills/conflict_management.json",
    "knowledges/human/skills/softskills/leadership_personal.json",
    "knowledges/human/skills/softskills/negotiation.json",
]


@pytest.mark.parametrize("relpath", KNOWLEDGE_FILES)
def test_softskills_knowledge_json_structure(relpath):
    data = json.loads((ROOT / relpath).read_text(encoding="utf-8"))
    for key in ("metadata", "knowledge_id", "title", "summary"):
        assert key in data, f"clé '{key}' manquante dans {relpath}"
