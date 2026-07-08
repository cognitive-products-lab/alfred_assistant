"""
PROJECT      : ALFRED
BLOCK        : B02
FUNCTION     : SMOKE
FILE         : tests/b02_tests/test_smoke_memory_batch1.py
ROLE         : Smoke tests (lot 1) pour les fichiers B02 sans couverture
               de test existante (RAG stub, pipeline bridge, profile analyzer,
               memory answer engine, fichiers JSON de connaissance mémoire).

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-07-05
UPDATED      : 2026-07-05
VERSION      : V1.0
STATUS       : TESTED

DESCRIPTION :
Verifie import + comportement de base. Pour ProfileAnalyzer, utilise des
fichiers de configuration synthetiques minimalistes (pas les vrais
questionnaires) pour rester rapide et independant des donnees utilisateur
reelles.
"""

import json
from pathlib import Path
from types import SimpleNamespace

import pytest

from src.rag.rag_engine import RAGEngine
from src.core.pipeline_bridge import (
    enrich_context_with_pipeline,
    get_pipeline_mode_guidelines,
    build_session_summary_from_pipeline,
    should_use_health_adapted_response,
    get_forced_response,
)
from src.core.profile_analyzer import ProfileAnalyzer, _get_level_from_score
from src.memory.memory_answer_engine import answer_from_memory

ROOT = Path(__file__).resolve().parents[2]


# ── src/rag/rag_engine.py (stub minimal) ────────────────────

def test_rag_engine_load_and_search():
    engine = RAGEngine()
    engine.load(["ALFRED connaît la RGPD", "Python est utilisé pour ALFRED"])
    results = engine.search("rgpd")
    assert results == ["ALFRED connaît la RGPD"]
    assert engine.search("inexistant") == []


# ── src/core/pipeline_bridge.py (duck-typing PipelineContext) ─

def _fake_pipeline_ctx(**overrides):
    defaults = dict(
        protection_active=False,
        protection_response=None,
        health_active=False,
        health_fog_mode=False,
        health_pain_mode=False,
        health_flare=False,
        health_bipolar_episode=False,
        health_rumination=False,
        health_hyperfocus=False,
        health_conditions=[],
        health_signal_type=None,
        health_protocol_id=None,
        health_adapted_response=None,
        cognitive_patterns=[],
        mode="focus",
        tone="neutre",
        response_length="medium",
        emotion_intensity=0.1,
        emotion="neutral",
        validation_first=False,
        humor_allowed=True,
        avoid_advice=False,
        forbidden_phrases=[],
        check_in_message=None,
        offer_pause=False,
        user_context_loaded=False,
        user_mbti=None,
        user_validate_first=False,
        user_humor_pref="leger",
        llm_system_context="",
        intent="general",
        energy_level="medium",
    )
    defaults.update(overrides)
    return SimpleNamespace(**defaults)


def test_pipeline_bridge_enrich_basic_mode():
    ctx = _fake_pipeline_ctx(mode="support", tone="doux")
    response_context = {}
    enrich_context_with_pipeline(response_context, ctx)
    assert response_context["adaptation"]["mode"] == "support_mode"
    assert response_context["adaptation"]["tone"] == "doux"
    assert response_context["health_context"]["active"] is False


def test_pipeline_bridge_protection_overrides_mode():
    ctx = _fake_pipeline_ctx(mode="focus", protection_active=True)
    response_context = {}
    enrich_context_with_pipeline(response_context, ctx)
    assert response_context["adaptation"]["mode"] == "support_mode"


def test_pipeline_bridge_guidelines_and_summary():
    ctx = _fake_pipeline_ctx(llm_system_context="contexte LLM")
    assert get_pipeline_mode_guidelines(ctx) == "contexte LLM"

    summary = build_session_summary_from_pipeline(ctx, exchange_count=3)
    assert summary["exchange_count"] == 3
    assert summary["dominant_emotion"] == "neutral"


def test_pipeline_bridge_forced_response_protection():
    ctx = _fake_pipeline_ctx(protection_active=True, protection_response="Je suis là.")
    assert should_use_health_adapted_response(ctx) is True
    assert get_forced_response(ctx) == "Je suis là."


def test_pipeline_bridge_forced_response_none_by_default():
    ctx = _fake_pipeline_ctx()
    assert should_use_health_adapted_response(ctx) is False
    assert get_forced_response(ctx) is None


# ── src/core/profile_analyzer.py (config synthetique minimale) ─

def test_get_level_from_score_default_buckets():
    assert _get_level_from_score(10, "dimension_inconnue") == "faible"
    assert _get_level_from_score(50, "dimension_inconnue") == "moyen"
    assert _get_level_from_score(90, "dimension_inconnue") == "élevé"


def test_profile_analyzer_pipeline_end_to_end(tmp_path):
    answers = {
        "questionnaires": {
            "test_dim": {
                "completed": True,
                "answers": {"q1": 4, "q2": 2},
            }
        }
    }
    scoring_keys = {
        "questionnaires": {
            "test_dim": {
                "subscales": {
                    "sub_a": {
                        "items": ["q1", "q2"],
                        "reversed_items": [],
                        "scoring": "mean",
                        "score_min": 1,
                        "score_max": 5,
                        "normalization": "linear_0_100",
                    }
                }
            }
        }
    }
    matrix = {
        "default_params": {"alfred_params": {"tone": "chaleureux"}},
        "rules": [
            {
                "id": "rule_1",
                "dimension": "test_dim",
                "sub_dimension": "sub_a",
                "level": "élevé",
                "alfred_params": {"tone": "energique"},
            }
        ],
        "combination_rules": [],
    }

    answers_path = tmp_path / "answers.json"
    keys_path = tmp_path / "keys.json"
    matrix_path = tmp_path / "matrix.json"
    profile_path = tmp_path / "profile.json"

    answers_path.write_text(json.dumps(answers), encoding="utf-8")
    keys_path.write_text(json.dumps(scoring_keys), encoding="utf-8")
    matrix_path.write_text(json.dumps(matrix), encoding="utf-8")

    analyzer = ProfileAnalyzer(
        answers_path=answers_path,
        keys_path=keys_path,
        matrix_path=matrix_path,
        profile_path=profile_path,
    )
    analyzer.load_all()
    scores = analyzer.compute_scores()

    assert scores["test_dim"].completed is True
    # (4+2)/2 = 3 -> normalise sur [1,5] -> (3-1)/4*100 = 50
    assert scores["test_dim"].sub_scores["sub_a"].score_normalized == 50.0

    params = analyzer.generate_alfred_params(scores)
    assert params.tone == "chaleureux"  # regle "élevé" non déclenchée (niveau réel = "moyen")

    profile = analyzer.update_user_profile(scores, params)
    assert profile_path.exists()
    assert profile["alfred_derived_params"]["tone"] == "chaleureux"


def test_profile_analyzer_fernet_roundtrip(tmp_path, monkeypatch):
    answers_path = tmp_path / "answers.json"
    answers_path.write_text(json.dumps({"questionnaires": {}}), encoding="utf-8")

    fernet_key_path = tmp_path / "fernet.key"
    encrypted_dir = tmp_path / "encrypted"

    analyzer = ProfileAnalyzer(
        answers_path=answers_path,
        fernet_key_path=fernet_key_path,
    )

    encrypted_path = analyzer.encrypt_answers(
        answers_path=answers_path, output_dir=encrypted_dir
    )
    assert encrypted_path is not None
    assert encrypted_path.exists()

    decrypted = analyzer.decrypt_answers(encrypted_path)
    assert decrypted == {"questionnaires": {}}


# ── src/memory/memory_answer_engine.py (reponses deterministes) ─

def test_memory_answer_engine_detects_current_work_question():
    context = (
        "- [2026-07-01 10:00] Céline : je travaille actuellement sur le pipeline vocal ALFRED\n"
        "  ALFRED : d'accord\n"
    )
    answer = answer_from_memory("sur quoi je travaille ?", context)
    assert answer is not None
    assert "pipeline vocal ALFRED" in answer


def test_memory_answer_engine_returns_none_for_unrelated_question():
    assert answer_from_memory("quelle heure est-il ?", "peu importe") is None


def test_memory_answer_engine_no_context_available():
    answer = answer_from_memory("sur quoi je travaille ?", "")
    assert "pas encore d’information fiable" in answer


# ── Fichiers JSON de connaissance mémoire (structure) ───────

KNOWLEDGE_FILES_WITH_METADATA = [
    "knowledges/professional/engineering/ai/semantic_memory.json",
    "knowledges/system/memory/episodic_memory.json",
    "knowledges/system/memory/memory_context_linking.json",
    "knowledges/system/memory/memory_decay_rules.json",
    "knowledges/system/memory/memory_learning_rules.json",
    "knowledges/system/memory/memory_prioritization.json",
    "knowledges/system/memory/memory_system.json",
]


@pytest.mark.parametrize("relpath", KNOWLEDGE_FILES_WITH_METADATA)
def test_knowledge_json_has_expected_structure(relpath):
    data = json.loads((ROOT / relpath).read_text(encoding="utf-8"))
    for key in ("metadata", "knowledge_id", "title", "summary"):
        assert key in data, f"clé '{key}' manquante dans {relpath}"


def test_user_memory_json_meta_structure():
    data = json.loads((ROOT / "data" / "user_memory.json").read_text(encoding="utf-8"))
    assert "_meta" in data
    assert data["_meta"]["project"] == "ALFRED"
