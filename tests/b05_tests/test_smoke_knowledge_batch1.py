"""
PROJECT      : ALFRED
BLOCK        : B05
FUNCTION     : SMOKE
FILE         : tests/b05_tests/test_smoke_knowledge_batch1.py
ROLE         : Smoke test structure pour knowledges/human/skills/softskills/organization.json

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-07-05
UPDATED      : 2026-07-05
VERSION      : V1.0
STATUS       : TESTED
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def test_organization_knowledge_json_structure():
    data = json.loads(
        (ROOT / "knowledges" / "human" / "skills" / "softskills" / "organization.json").read_text(encoding="utf-8")
    )
    for key in ("metadata", "knowledge_id", "title", "summary"):
        assert key in data
