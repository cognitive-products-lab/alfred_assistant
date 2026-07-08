"""
PROJECT      : ALFRED
BLOCK        : B08
FUNCTION     : SMOKE
FILE         : tests/b08_tests/test_smoke_batch1.py
ROLE         : Smoke tests (lot 1) pour src/profile/profile_analyzer.py
               (QuestionnaireSession — passation psychometrique) et les
               fichiers JSON de personnalite/profil/config B08.

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-07-05
UPDATED      : 2026-07-05
VERSION      : V1.0
STATUS       : TESTED

DESCRIPTION :
QuestionnaireSession est teste avec un fichier de reponses synthetique
(tmp_path), jamais les vraies donnees utilisateur. Les fichiers JSON de
profil/personnalite sont verifies uniquement sur leur structure (jamais
sur leur contenu personnel).
"""

import json
from pathlib import Path

import pytest

from src.profile.profile_analyzer import QuestionnaireSession, QUESTIONNAIRE_ITEMS

ROOT = Path(__file__).resolve().parents[2]


def _make_answers_file(tmp_path, questionnaire_id: str) -> Path:
    items = QUESTIONNAIRE_ITEMS[questionnaire_id]
    answers_path = tmp_path / "answers.json"
    data = {
        "_meta": {},
        "questionnaires": {
            questionnaire_id: {
                "answers": {qid: None for qid, _, _ in items},
                "session_state": {},
            }
        },
    }
    answers_path.write_text(json.dumps(data), encoding="utf-8")
    return answers_path


# ── QuestionnaireSession (src/profile/profile_analyzer.py) ──
# Fixe le 2026-07-05 : docstrings empilées fusionnées (bug systémique,
# cf. tools/profile_tools/generate_alfred_params.py et
# tools/profile_tools/test_alfred_profile_integration.py, même correctif).

def test_next_question_returns_first_unanswered(tmp_path):
    path = _make_answers_file(tmp_path, "q01_bien_etre_subjectif")
    session = QuestionnaireSession(answers_path=path)
    q = session.next_question("q01_bien_etre_subjectif")
    assert q["id"] == "swls_01"
    assert q["index"] == 0
    assert q["progress_pct"] == 0.0


def test_next_question_unknown_questionnaire_raises(tmp_path):
    path = _make_answers_file(tmp_path, "q01_bien_etre_subjectif")
    session = QuestionnaireSession(answers_path=path)
    with pytest.raises(ValueError):
        session.next_question("questionnaire_inexistant")


def test_save_answer_validates_likert_range(tmp_path):
    path = _make_answers_file(tmp_path, "q01_bien_etre_subjectif")
    session = QuestionnaireSession(answers_path=path)
    session.save_answer("q01_bien_etre_subjectif", "swls_01", 5)
    with pytest.raises(ValueError):
        session.save_answer("q01_bien_etre_subjectif", "swls_02", 99)


def test_save_answer_advances_next_question(tmp_path):
    path = _make_answers_file(tmp_path, "q01_bien_etre_subjectif")
    session = QuestionnaireSession(answers_path=path)
    session.save_answer("q01_bien_etre_subjectif", "swls_01", 5)
    q = session.next_question("q01_bien_etre_subjectif")
    assert q["id"] == "swls_02"


def test_get_progress_reflects_answers(tmp_path):
    path = _make_answers_file(tmp_path, "q01_bien_etre_subjectif")
    session = QuestionnaireSession(answers_path=path)
    session.save_answer("q01_bien_etre_subjectif", "swls_01", 5)
    progress = session.get_progress()
    assert progress["q01_bien_etre_subjectif"]["answered"] == 1
    assert progress["q01_bien_etre_subjectif"]["total"] == 14


def test_can_compute_partial_scores_threshold(tmp_path):
    path = _make_answers_file(tmp_path, "q01_bien_etre_subjectif")
    session = QuestionnaireSession(answers_path=path)
    assert session.can_compute_partial_scores("q01_bien_etre_subjectif") is False
    swls_keys = ["swls_01", "swls_02", "swls_03", "swls_04", "swls_05"]
    extra_keys = ["pan_p_01", "pan_p_02"]
    for k in swls_keys + extra_keys:
        session.save_answer("q01_bien_etre_subjectif", k, 5)
    assert session.can_compute_partial_scores("q01_bien_etre_subjectif") is True


def test_compute_scores_partial_q01(tmp_path):
    path = _make_answers_file(tmp_path, "q01_bien_etre_subjectif")
    session = QuestionnaireSession(answers_path=path)
    for k in ["swls_01", "swls_02", "swls_03", "swls_04", "swls_05", "pan_p_01", "pan_p_02"]:
        session.save_answer("q01_bien_etre_subjectif", k, 4)
    scores = session.compute_scores("q01_bien_etre_subjectif", partial=True)
    assert scores is not None
    assert scores["swls_total"] == 20  # 5 items * 4
    assert scores["is_partial"] is True


def test_compute_scores_returns_none_when_incomplete_and_not_partial(tmp_path):
    path = _make_answers_file(tmp_path, "q01_bien_etre_subjectif")
    session = QuestionnaireSession(answers_path=path)
    session.save_answer("q01_bien_etre_subjectif", "swls_01", 5)
    assert session.compute_scores("q01_bien_etre_subjectif", partial=False) is None


def test_score_q09_hexaco_reverses_correct_items(tmp_path):
    path = _make_answers_file(tmp_path, "q09_hexaco_personnalite")
    session = QuestionnaireSession(answers_path=path)
    # hex_h_02 et hex_h_04 sont inverses (6 - valeur)
    session.save_answer("q09_hexaco_personnalite", "hex_h_01", 5)
    session.save_answer("q09_hexaco_personnalite", "hex_h_02", 1)  # -> 6-1=5
    session.save_answer("q09_hexaco_personnalite", "hex_h_03", 5)
    session.save_answer("q09_hexaco_personnalite", "hex_h_04", 1)  # -> 6-1=5
    items = QUESTIONNAIRE_ITEMS["q09_hexaco_personnalite"]
    for qid, _, qtype in items:
        if qid.startswith("hex_h_"):
            continue
        session.save_answer("q09_hexaco_personnalite", qid, 3)
    scores = session.compute_scores("q09_hexaco_personnalite", partial=False)
    assert scores["honnetete_humilite"] == 5.0


# ── Fichiers JSON de personnalite/profil (structure uniquement) ─

PERSONALITY_FILES = [
    "config/personality_core.json",
    "data/personality/instances/personality_core_instance.json",
    "data/personality/templates/personality_core.json",
    "data/personality/templates/personality_core_template_public.json",
]

USER_ADAPTATION_FILES = [
    "config/user_adaptation_profile.json",
    "data/users/templates/user_adaptation_profile.json",
]

CORE_KNOWLEDGE_FILES = [
    "knowledges/core/behavioral_modes.json",
    "knowledges/core/context_awareness.json",
    "knowledges/core/personalization_engine.json",
    "knowledges/core/system_rules.json",
    "knowledges/core/user_adaptation.json",
]


@pytest.mark.parametrize("relpath", PERSONALITY_FILES)
def test_personality_json_has_expected_structure(relpath):
    data = json.loads((ROOT / relpath).read_text(encoding="utf-8"))
    for key in ("assistant_identity", "stable_personality", "communication_style"):
        assert key in data, f"clé '{key}' manquante dans {relpath}"


@pytest.mark.parametrize("relpath", USER_ADAPTATION_FILES)
def test_user_adaptation_json_has_expected_structure(relpath):
    data = json.loads((ROOT / relpath).read_text(encoding="utf-8"))
    for key in ("user_profile", "needs", "preferred_tone", "activation_rules"):
        assert key in data, f"clé '{key}' manquante dans {relpath}"


def test_user_celine_instance_json_structure():
    data = json.loads(
        (ROOT / "data" / "users" / "instances" / "user_celine_instance.json").read_text(encoding="utf-8")
    )
    for key in ("user_profile", "preferences", "communication_style", "privacy_and_consent", "metadata"):
        assert key in data


def test_user_profile_template_public_json_structure():
    data = json.loads(
        (ROOT / "data" / "users" / "templates" / "user_profile_template_public.json").read_text(encoding="utf-8")
    )
    assert "_alfred_header" in data
    assert "user_profile" in data


def test_data_profile_user_profile_json_structure():
    data = json.loads((ROOT / "data" / "profile" / "user_profile.json").read_text(encoding="utf-8"))
    for key in ("name", "softskills", "personality_traits", "preferences"):
        assert key in data


@pytest.mark.parametrize("relpath", CORE_KNOWLEDGE_FILES)
def test_core_knowledge_json_has_metadata(relpath):
    data = json.loads((ROOT / relpath).read_text(encoding="utf-8"))
    assert "metadata" in data
    assert len(data) > 1  # pas juste un stub {"metadata": ...}


def test_discipline_knowledge_json_structure():
    data = json.loads(
        (ROOT / "knowledges" / "human" / "self_alignment" / "habits" / "discipline.json").read_text(encoding="utf-8")
    )
    for key in ("metadata", "knowledge_id", "title", "summary"):
        assert key in data


def test_feedback_loop_knowledge_json_structure():
    data = json.loads(
        (ROOT / "knowledges" / "human" / "self_alignment" / "routines" / "feedback_loop.json").read_text(encoding="utf-8")
    )
    assert "metadata" in data
    assert "feedback_types" in data or "feedback_philosophy" in data
