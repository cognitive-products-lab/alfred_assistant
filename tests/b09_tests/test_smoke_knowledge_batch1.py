"""
PROJECT      : ALFRED
BLOCK        : B09
FUNCTION     : SMOKE
FILE         : tests/b09_tests/test_smoke_knowledge_batch1.py
ROLE         : Smoke tests (lot 1) pour les fichiers JSON de connaissance
               decision/problem-solving B09 et le config Piper.

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
    "knowledges/human/skills/softskills/problem_solving.json",
    "knowledges/professional/decision/decision_models.json",
    "knowledges/professional/decision/decision_support.json",
    "knowledges/professional/decision/root_cause_analysis.json",
    "knowledges/professional/decision/tradeoff_analysis.json",
]


@pytest.mark.parametrize("relpath", KNOWLEDGE_FILES)
def test_decision_knowledge_json_structure(relpath):
    data = json.loads((ROOT / relpath).read_text(encoding="utf-8"))
    for key in ("metadata", "knowledge_id", "title", "summary"):
        assert key in data, f"clé '{key}' manquante dans {relpath}"


def test_piper_fr_voice_config_structure():
    data = json.loads(
        (ROOT / "tools" / "piper" / "models" / "fr_FR-upmc-medium.onnx.json").read_text(encoding="utf-8")
    )
    assert data["audio"]["sample_rate"] == 22050
    assert data["phoneme_type"] == "espeak"
    assert isinstance(data["phoneme_id_map"], dict) and data["phoneme_id_map"]
