"""
test_profile_analyzer.py
Suite de tests pytest pour src/profile/profile_analyzer.py

Couvre : QuestionnaireSession (next_question, save_answer, get_progress,
         can_compute_partial_scores, compute_scores)

Usage :
    pytest docs/module_profil_ia_adaptative/tests/test_profile_analyzer.py -v
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

# ---------------------------------------------------------------------------
# Ajout de la racine du projet au PYTHONPATH
# ---------------------------------------------------------------------------
sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

from src.profile.profile_analyzer import (  # noqa: E402
    QUESTIONNAIRE_ITEMS,
    QUESTIONNAIRE_META,
    QuestionnaireSession,
)


# ---------------------------------------------------------------------------
# Helpers / fixtures pytest
# ---------------------------------------------------------------------------

def _make_blank_answers(tmp_path: Path) -> Path:
    """Crée un fichier answers.json vierge (toutes valeurs à null)."""
    data: dict = {
        "_meta": {"version": "1.0.0", "last_updated": None, "user_id": None},
        "questionnaires": {},
    }
    for qid, items in QUESTIONNAIRE_ITEMS.items():
        data["questionnaires"][qid] = {
            "session_state": {
                "current_question_index": 0,
                "started_at": None,
                "last_saved_at": None,
                "is_complete": False,
                "total_questions": len(items),
                "questions_answered": 0,
            },
            "answers": {qid_item: None for qid_item, _, _ in items},
            "scores": {},
        }
    path = tmp_path / "answers.json"
    path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    return path


def _make_session(tmp_path: Path) -> QuestionnaireSession:
    """Crée une QuestionnaireSession pointant sur un fichier temporaire vierge."""
    path = _make_blank_answers(tmp_path)
    return QuestionnaireSession(answers_path=path)


def _fill_questionnaire(session: QuestionnaireSession, qid: str) -> None:
    """Remplit complètement un questionnaire avec des réponses valides."""
    items = QUESTIONNAIRE_ITEMS[qid]
    for question_id, _, qtype in items:
        if qtype == "likert_7":
            session.save_answer(qid, question_id, 4)
        elif qtype == "likert_5":
            session.save_answer(qid, question_id, 3)
        elif qtype == "choix_binaire":
            session.save_answer(qid, question_id, "A")
        else:  # texte_libre
            session.save_answer(qid, question_id, "réponse libre")


# ---------------------------------------------------------------------------
# TestNextQuestion
# ---------------------------------------------------------------------------

class TestNextQuestion:
    """Tests pour QuestionnaireSession.next_question()."""

    def test_returns_first_question_when_nothing_answered(self, tmp_path):
        session = _make_session(tmp_path)
        result = session.next_question("q01_bien_etre_subjectif")
        assert result is not None
        assert result["id"] == "swls_01"
        assert result["index"] == 0

    def test_returns_none_when_questionnaire_complete(self, tmp_path):
        session = _make_session(tmp_path)
        _fill_questionnaire(session, "q01_bien_etre_subjectif")
        result = session.next_question("q01_bien_etre_subjectif")
        assert result is None

    def test_returns_correct_question_index(self, tmp_path):
        session = _make_session(tmp_path)
        # Répondre aux 3 premières questions
        session.save_answer("q01_bien_etre_subjectif", "swls_01", 5)
        session.save_answer("q01_bien_etre_subjectif", "swls_02", 6)
        session.save_answer("q01_bien_etre_subjectif", "swls_03", 4)
        result = session.next_question("q01_bien_etre_subjectif")
        assert result is not None
        assert result["index"] == 3
        assert result["id"] == "swls_04"

    def test_raises_on_unknown_questionnaire(self, tmp_path):
        session = _make_session(tmp_path)
        with pytest.raises(ValueError, match="inconnu"):
            session.next_question("q99_inexistant")

    def test_returns_dict_with_required_keys(self, tmp_path):
        session = _make_session(tmp_path)
        result = session.next_question("q01_bien_etre_subjectif")
        assert result is not None
        for key in ("id", "text", "type", "index", "total", "progress_pct"):
            assert key in result, f"Clé manquante : {key}"

    def test_progress_pct_zero_when_nothing_answered(self, tmp_path):
        session = _make_session(tmp_path)
        result = session.next_question("q01_bien_etre_subjectif")
        assert result is not None
        assert result["progress_pct"] == 0.0

    def test_progress_pct_increases_after_answers(self, tmp_path):
        session = _make_session(tmp_path)
        session.save_answer("q01_bien_etre_subjectif", "swls_01", 5)
        result = session.next_question("q01_bien_etre_subjectif")
        assert result is not None
        assert result["progress_pct"] > 0.0

    def test_total_matches_questionnaire_length(self, tmp_path):
        session = _make_session(tmp_path)
        result = session.next_question("q01_bien_etre_subjectif")
        assert result is not None
        expected_total = len(QUESTIONNAIRE_ITEMS["q01_bien_etre_subjectif"])
        assert result["total"] == expected_total

    def test_returns_correct_type_for_likert7(self, tmp_path):
        session = _make_session(tmp_path)
        result = session.next_question("q01_bien_etre_subjectif")
        assert result is not None
        assert result["type"] == "likert_7"

    def test_returns_correct_type_for_binary_choice(self, tmp_path):
        """fmt_01 et fmt_02 sont de type choix_binaire dans q02."""
        session = _make_session(tmp_path)
        # Remplir les 14 premières questions de q02 (likert_7)
        items = QUESTIONNAIRE_ITEMS["q02_style_cognitif"]
        for qid, _, qtype in items:
            if qtype != "choix_binaire":
                session.save_answer("q02_style_cognitif", qid, 4)
            else:
                break
        result = session.next_question("q02_style_cognitif")
        assert result is not None
        assert result["type"] == "choix_binaire"

    def test_advances_to_next_unanswered_question(self, tmp_path):
        session = _make_session(tmp_path)
        items = QUESTIONNAIRE_ITEMS["q01_bien_etre_subjectif"]
        # Répondre à toutes sauf la dernière
        for qid, _, qtype in items[:-1]:
            session.save_answer("q01_bien_etre_subjectif", qid, 3)
        result = session.next_question("q01_bien_etre_subjectif")
        assert result is not None
        assert result["id"] == items[-1][0]  # dernière question


# ---------------------------------------------------------------------------
# TestSaveAnswer
# ---------------------------------------------------------------------------

class TestSaveAnswer:
    """Tests pour QuestionnaireSession.save_answer()."""

    def test_saves_valid_likert7_answer(self, tmp_path):
        session = _make_session(tmp_path)
        session.save_answer("q01_bien_etre_subjectif", "swls_01", 5)
        # Recharger depuis fichier
        data = json.loads((tmp_path / "answers.json").read_text(encoding="utf-8"))
        assert data["questionnaires"]["q01_bien_etre_subjectif"]["answers"]["swls_01"] == 5

    def test_saves_valid_likert5_answer(self, tmp_path):
        session = _make_session(tmp_path)
        session.save_answer("q03_regulation_emotionnelle", "re_01", 3)
        data = json.loads((tmp_path / "answers.json").read_text(encoding="utf-8"))
        assert data["questionnaires"]["q03_regulation_emotionnelle"]["answers"]["re_01"] == 3

    def test_saves_valid_binary_choice(self, tmp_path):
        session = _make_session(tmp_path)
        session.save_answer("q02_style_cognitif", "fmt_01", "A")
        data = json.loads((tmp_path / "answers.json").read_text(encoding="utf-8"))
        assert data["questionnaires"]["q02_style_cognitif"]["answers"]["fmt_01"] == "A"

    def test_saves_free_text(self, tmp_path):
        session = _make_session(tmp_path)
        texte = "Matin, vers 9h, quand le café est encore chaud."
        session.save_answer("q00_profil_complementaire", "energie_01", texte)
        data = json.loads((tmp_path / "answers.json").read_text(encoding="utf-8"))
        assert data["questionnaires"]["q00_profil_complementaire"]["answers"]["energie_01"] == texte

    def test_raises_on_out_of_range_likert7_too_high(self, tmp_path):
        session = _make_session(tmp_path)
        with pytest.raises(ValueError, match="hors-échelle"):
            session.save_answer("q01_bien_etre_subjectif", "swls_01", 8)

    def test_raises_on_out_of_range_likert7_too_low(self, tmp_path):
        session = _make_session(tmp_path)
        with pytest.raises(ValueError, match="hors-échelle"):
            session.save_answer("q01_bien_etre_subjectif", "swls_01", 0)

    def test_raises_on_out_of_range_likert5(self, tmp_path):
        session = _make_session(tmp_path)
        with pytest.raises(ValueError, match="hors-échelle"):
            session.save_answer("q03_regulation_emotionnelle", "re_01", 6)

    def test_raises_on_invalid_binary_choice(self, tmp_path):
        session = _make_session(tmp_path)
        with pytest.raises(ValueError, match="choix_binaire"):
            session.save_answer("q02_style_cognitif", "fmt_01", "C")

    def test_raises_on_unknown_questionnaire(self, tmp_path):
        session = _make_session(tmp_path)
        with pytest.raises(ValueError, match="inconnu"):
            session.save_answer("q99_inexistant", "swls_01", 3)

    def test_raises_on_unknown_question_id(self, tmp_path):
        session = _make_session(tmp_path)
        with pytest.raises(ValueError, match="inconnue"):
            session.save_answer("q01_bien_etre_subjectif", "question_inexistante", 3)

    def test_updates_session_state_after_save(self, tmp_path):
        session = _make_session(tmp_path)
        session.save_answer("q01_bien_etre_subjectif", "swls_01", 4)
        data = json.loads((tmp_path / "answers.json").read_text(encoding="utf-8"))
        ss = data["questionnaires"]["q01_bien_etre_subjectif"]["session_state"]
        assert ss["questions_answered"] == 1
        assert ss["last_saved_at"] is not None

    def test_marks_complete_when_all_answered(self, tmp_path):
        session = _make_session(tmp_path)
        _fill_questionnaire(session, "q01_bien_etre_subjectif")
        data = json.loads((tmp_path / "answers.json").read_text(encoding="utf-8"))
        ss = data["questionnaires"]["q01_bien_etre_subjectif"]["session_state"]
        assert ss["is_complete"] is True

    def test_binary_choice_accepts_lowercase(self, tmp_path):
        """La validation normalise en majuscule."""
        session = _make_session(tmp_path)
        session.save_answer("q02_style_cognitif", "fmt_01", "b")
        data = json.loads((tmp_path / "answers.json").read_text(encoding="utf-8"))
        # Doit être normalisé en "B"
        assert data["questionnaires"]["q02_style_cognitif"]["answers"]["fmt_01"] == "B"

    def test_likert7_boundary_values_accepted(self, tmp_path):
        """Les valeurs limites 1 et 7 doivent être acceptées."""
        session = _make_session(tmp_path)
        session.save_answer("q01_bien_etre_subjectif", "swls_01", 1)
        session.save_answer("q01_bien_etre_subjectif", "swls_02", 7)
        data = json.loads((tmp_path / "answers.json").read_text(encoding="utf-8"))
        answers = data["questionnaires"]["q01_bien_etre_subjectif"]["answers"]
        assert answers["swls_01"] == 1
        assert answers["swls_02"] == 7


# ---------------------------------------------------------------------------
# TestGetProgress
# ---------------------------------------------------------------------------

class TestGetProgress:
    """Tests pour QuestionnaireSession.get_progress()."""

    def test_returns_all_questionnaires(self, tmp_path):
        session = _make_session(tmp_path)
        progress = session.get_progress()
        for qid in QUESTIONNAIRE_META:
            assert qid in progress, f"Questionnaire manquant : {qid}"

    def test_pct_zero_when_not_started(self, tmp_path):
        session = _make_session(tmp_path)
        progress = session.get_progress()
        assert progress["q01_bien_etre_subjectif"]["pct_complete"] == 0.0
        assert progress["q01_bien_etre_subjectif"]["answered"] == 0

    def test_pct_correct_after_partial_answers(self, tmp_path):
        session = _make_session(tmp_path)
        # q01 a 14 questions, on en répond 7
        items = QUESTIONNAIRE_ITEMS["q01_bien_etre_subjectif"]
        for qid, _, qtype in items[:7]:
            session.save_answer("q01_bien_etre_subjectif", qid, 4)
        progress = session.get_progress()
        p = progress["q01_bien_etre_subjectif"]
        assert p["answered"] == 7
        assert p["total"] == 14
        expected_pct = round(7 / 14 * 100, 1)
        assert p["pct_complete"] == expected_pct

    def test_pct_100_when_complete(self, tmp_path):
        session = _make_session(tmp_path)
        _fill_questionnaire(session, "q01_bien_etre_subjectif")
        progress = session.get_progress()
        assert progress["q01_bien_etre_subjectif"]["pct_complete"] == 100.0

    def test_estimated_remaining_decreases(self, tmp_path):
        session = _make_session(tmp_path)
        progress_before = session.get_progress()
        remaining_before = progress_before["q01_bien_etre_subjectif"]["estimated_remaining_min"]
        session.save_answer("q01_bien_etre_subjectif", "swls_01", 5)
        progress_after = session.get_progress()
        remaining_after = progress_after["q01_bien_etre_subjectif"]["estimated_remaining_min"]
        assert remaining_after <= remaining_before

    def test_is_complete_false_when_partial(self, tmp_path):
        session = _make_session(tmp_path)
        session.save_answer("q01_bien_etre_subjectif", "swls_01", 4)
        progress = session.get_progress()
        assert progress["q01_bien_etre_subjectif"]["is_complete"] is False

    def test_is_complete_true_when_finished(self, tmp_path):
        session = _make_session(tmp_path)
        _fill_questionnaire(session, "q01_bien_etre_subjectif")
        progress = session.get_progress()
        assert progress["q01_bien_etre_subjectif"]["is_complete"] is True

    def test_label_matches_meta(self, tmp_path):
        session = _make_session(tmp_path)
        progress = session.get_progress()
        for qid, meta in QUESTIONNAIRE_META.items():
            assert progress[qid]["label"] == meta["label"]

    def test_total_matches_items_count(self, tmp_path):
        session = _make_session(tmp_path)
        progress = session.get_progress()
        for qid in QUESTIONNAIRE_META:
            expected = len(QUESTIONNAIRE_ITEMS.get(qid, []))
            assert progress[qid]["total"] == expected


# ---------------------------------------------------------------------------
# TestCanComputePartialScores
# ---------------------------------------------------------------------------

class TestCanComputePartialScores:
    """Tests pour QuestionnaireSession.can_compute_partial_scores()."""

    def test_false_when_no_answers(self, tmp_path):
        session = _make_session(tmp_path)
        assert session.can_compute_partial_scores("q01_bien_etre_subjectif") is False

    def test_false_below_threshold(self, tmp_path):
        session = _make_session(tmp_path)
        # Seuil q01 = 7, on en répond 5
        items = QUESTIONNAIRE_ITEMS["q01_bien_etre_subjectif"]
        for qid, _, _ in items[:5]:
            session.save_answer("q01_bien_etre_subjectif", qid, 4)
        assert session.can_compute_partial_scores("q01_bien_etre_subjectif") is False

    def test_true_at_threshold(self, tmp_path):
        session = _make_session(tmp_path)
        threshold = QUESTIONNAIRE_META["q01_bien_etre_subjectif"]["min_for_partial"]  # 7
        items = QUESTIONNAIRE_ITEMS["q01_bien_etre_subjectif"]
        for qid, _, _ in items[:threshold]:
            session.save_answer("q01_bien_etre_subjectif", qid, 4)
        assert session.can_compute_partial_scores("q01_bien_etre_subjectif") is True

    def test_true_above_threshold(self, tmp_path):
        session = _make_session(tmp_path)
        threshold = QUESTIONNAIRE_META["q01_bien_etre_subjectif"]["min_for_partial"]
        items = QUESTIONNAIRE_ITEMS["q01_bien_etre_subjectif"]
        for qid, _, _ in items[:threshold + 2]:
            session.save_answer("q01_bien_etre_subjectif", qid, 4)
        assert session.can_compute_partial_scores("q01_bien_etre_subjectif") is True

    def test_raises_on_unknown_questionnaire(self, tmp_path):
        session = _make_session(tmp_path)
        with pytest.raises(ValueError, match="inconnu"):
            session.can_compute_partial_scores("q99_inexistant")

    def test_threshold_q04_correct(self, tmp_path):
        """q04 a un seuil min_for_partial de 9."""
        session = _make_session(tmp_path)
        threshold = QUESTIONNAIRE_META["q04_motivations_valeurs"]["min_for_partial"]  # 9
        items = QUESTIONNAIRE_ITEMS["q04_motivations_valeurs"]
        # Un de moins que le seuil
        for qid, _, _ in items[:threshold - 1]:
            session.save_answer("q04_motivations_valeurs", qid, 5)
        assert session.can_compute_partial_scores("q04_motivations_valeurs") is False
        # Exactement le seuil
        session.save_answer("q04_motivations_valeurs", items[threshold - 1][0], 5)
        assert session.can_compute_partial_scores("q04_motivations_valeurs") is True


# ---------------------------------------------------------------------------
# TestComputeScores
# ---------------------------------------------------------------------------

class TestComputeScores:
    """Tests pour QuestionnaireSession.compute_scores()."""

    # -- cas général --

    def test_returns_none_when_incomplete(self, tmp_path):
        session = _make_session(tmp_path)
        session.save_answer("q01_bien_etre_subjectif", "swls_01", 5)
        result = session.compute_scores("q01_bien_etre_subjectif")
        assert result is None

    def test_raises_on_unknown_questionnaire(self, tmp_path):
        session = _make_session(tmp_path)
        with pytest.raises(ValueError):
            session.compute_scores("q99_inexistant")

    # -- Q01 SWLS + PANAS --

    def _build_q01_session(self, tmp_path, answers: dict) -> QuestionnaireSession:
        """Crée une session avec des réponses Q01 prédéfinies."""
        session = _make_session(tmp_path)
        for qid, val in answers.items():
            session.save_answer("q01_bien_etre_subjectif", qid, val)
        return session

    def test_q01_swls_total_correct(self, tmp_path):
        answers = {
            "swls_01": 5, "swls_02": 6, "swls_03": 5, "swls_04": 6, "swls_05": 4,
            "pan_p_01": 6, "pan_p_02": 5, "pan_p_03": 7, "pan_p_04": 6, "pan_p_05": 5,
            "pan_n_01": 2, "pan_n_02": 3, "pan_n_03": 2, "pan_n_04": 1,
        }
        session = self._build_q01_session(tmp_path, answers)
        scores = session.compute_scores("q01_bien_etre_subjectif")
        assert scores is not None
        assert scores["swls_total"] == 26

    def test_q01_panas_positif_correct(self, tmp_path):
        answers = {
            "swls_01": 5, "swls_02": 6, "swls_03": 5, "swls_04": 6, "swls_05": 4,
            "pan_p_01": 6, "pan_p_02": 5, "pan_p_03": 7, "pan_p_04": 6, "pan_p_05": 5,
            "pan_n_01": 2, "pan_n_02": 3, "pan_n_03": 2, "pan_n_04": 1,
        }
        session = self._build_q01_session(tmp_path, answers)
        scores = session.compute_scores("q01_bien_etre_subjectif")
        assert scores is not None
        assert scores["panas_positif"] == 29

    def test_q01_panas_negatif_correct(self, tmp_path):
        answers = {
            "swls_01": 5, "swls_02": 6, "swls_03": 5, "swls_04": 6, "swls_05": 4,
            "pan_p_01": 6, "pan_p_02": 5, "pan_p_03": 7, "pan_p_04": 6, "pan_p_05": 5,
            "pan_n_01": 2, "pan_n_02": 3, "pan_n_03": 2, "pan_n_04": 1,
        }
        session = self._build_q01_session(tmp_path, answers)
        scores = session.compute_scores("q01_bien_etre_subjectif")
        assert scores is not None
        assert scores["panas_negatif"] == 8

    def test_q01_scores_contain_required_keys(self, tmp_path):
        answers = {
            "swls_01": 4, "swls_02": 4, "swls_03": 4, "swls_04": 4, "swls_05": 4,
            "pan_p_01": 4, "pan_p_02": 4, "pan_p_03": 4, "pan_p_04": 4, "pan_p_05": 4,
            "pan_n_01": 3, "pan_n_02": 3, "pan_n_03": 3, "pan_n_04": 3,
        }
        session = self._build_q01_session(tmp_path, answers)
        scores = session.compute_scores("q01_bien_etre_subjectif")
        assert scores is not None
        for key in ("swls_total", "panas_positif", "panas_negatif", "computed_at"):
            assert key in scores

    # -- Q02 Style cognitif --

    def _build_q02_session(self, tmp_path, answers: dict) -> QuestionnaireSession:
        session = _make_session(tmp_path)
        for qid, val in answers.items():
            session.save_answer("q02_style_cognitif", qid, val)
        return session

    def test_q02_profil_analytique(self, tmp_path):
        """score_a très élevé, score_i très bas → profil analytique."""
        answers = {
            "cog_a_01": 7, "cog_a_02": 7, "cog_a_03": 7, "cog_a_04": 7,
            "cog_i_01": 2, "cog_i_02": 2, "cog_i_03": 2, "cog_i_04": 2,
            "cog_v_01": 4, "cog_v_02": 4, "cog_v_03": 4,
            "cog_vs_01": 4, "cog_vs_02": 4, "cog_vs_03": 4,
            "fmt_01": "A", "fmt_02": "A",
        }
        session = self._build_q02_session(tmp_path, answers)
        scores = session.compute_scores("q02_style_cognitif")
        assert scores is not None
        assert scores["profil_ai"] == "analytique"

    def test_q02_profil_intuitif(self, tmp_path):
        """score_i très élevé, score_a très bas → profil intuitif."""
        answers = {
            "cog_a_01": 2, "cog_a_02": 2, "cog_a_03": 2, "cog_a_04": 2,
            "cog_i_01": 7, "cog_i_02": 7, "cog_i_03": 7, "cog_i_04": 7,
            "cog_v_01": 4, "cog_v_02": 4, "cog_v_03": 4,
            "cog_vs_01": 4, "cog_vs_02": 4, "cog_vs_03": 4,
            "fmt_01": "B", "fmt_02": "B",
        }
        session = self._build_q02_session(tmp_path, answers)
        scores = session.compute_scores("q02_style_cognitif")
        assert scores is not None
        assert scores["profil_ai"] == "intuitif"

    def test_q02_profil_mixte(self, tmp_path):
        """Scores proches (diff <= 1.5) → profil mixte."""
        answers = {
            "cog_a_01": 4, "cog_a_02": 4, "cog_a_03": 4, "cog_a_04": 4,
            "cog_i_01": 4, "cog_i_02": 4, "cog_i_03": 4, "cog_i_04": 4,
            "cog_v_01": 4, "cog_v_02": 4, "cog_v_03": 4,
            "cog_vs_01": 4, "cog_vs_02": 4, "cog_vs_03": 4,
            "fmt_01": "A", "fmt_02": "B",
        }
        session = self._build_q02_session(tmp_path, answers)
        scores = session.compute_scores("q02_style_cognitif")
        assert scores is not None
        assert scores["profil_ai"] == "mixte"

    def test_q02_sample_answers_scores(self, tmp_path):
        """Test avec les réponses de sample_answers.json → scores de expected_scores.json."""
        answers = {
            "cog_a_01": 6, "cog_a_02": 5, "cog_a_03": 6, "cog_a_04": 5,
            "cog_i_01": 3, "cog_i_02": 3, "cog_i_03": 2, "cog_i_04": 4,
            "cog_v_01": 5, "cog_v_02": 6, "cog_v_03": 5,
            "cog_vs_01": 3, "cog_vs_02": 3, "cog_vs_03": 4,
            "fmt_01": "A", "fmt_02": "A",
        }
        session = self._build_q02_session(tmp_path, answers)
        scores = session.compute_scores("q02_style_cognitif")
        assert scores is not None
        assert scores["score_analytique"] == 5.5
        assert scores["score_intuitif"] == 3.0
        assert scores["profil_ai"] == "analytique"
        assert scores["score_verbal"] == 5.33
        assert scores["score_visuel_spatial"] == 3.33
        assert scores["profil_vvs"] == "verbal"

    # -- Q03 Régulation émotionnelle --

    def _build_q03_session(self, tmp_path, answers: dict) -> QuestionnaireSession:
        session = _make_session(tmp_path)
        for qid, val in answers.items():
            session.save_answer("q03_regulation_emotionnelle", qid, val)
        return session

    def test_q03_pss_inversion_str04(self, tmp_path):
        """str_04 est un item positif : le score PSS applique 6 - valeur."""
        # Réponses minimales : uniquement les items Likert-5, pas les choix_binaire
        # str_04 = 1 (pleinement confiant → très peu de stress)
        # → dans PSS, 6-1 = 5 (contribution max au stress perçu)
        answers = {
            "re_01": 3, "re_02": 3, "re_03": 3, "re_04": 3, "re_05": 3,
            "sup_01": 3, "sup_02": 3, "sup_03": 3,
            "str_01": 1, "str_02": 1, "str_03": 1, "str_04": 1, "str_05": 1,
            "strat_01": "A", "strat_02": "A",
        }
        session = self._build_q03_session(tmp_path, answers)
        scores = session.compute_scores("q03_regulation_emotionnelle")
        assert scores is not None
        # PSS = str_01(1) + str_02(1) + str_03(1) + (6-str_04)(5) + str_05(1) = 9
        assert scores["stress_percu_pss"] == 9

    def test_q03_pss_total_correct(self, tmp_path):
        """Test avec les réponses de sample_answers.json → PSS = 11."""
        answers = {
            "re_01": 4, "re_02": 4, "re_03": 3, "re_04": 4, "re_05": 3,
            "sup_01": 2, "sup_02": 2, "sup_03": 3,
            "str_01": 2, "str_02": 2, "str_03": 3, "str_04": 4, "str_05": 2,
            "strat_01": "B", "strat_02": "A",
        }
        session = self._build_q03_session(tmp_path, answers)
        scores = session.compute_scores("q03_regulation_emotionnelle")
        assert scores is not None
        assert scores["stress_percu_pss"] == 11

    def test_q03_reevaluation_cognitive_correct(self, tmp_path):
        answers = {
            "re_01": 4, "re_02": 4, "re_03": 3, "re_04": 4, "re_05": 3,
            "sup_01": 2, "sup_02": 2, "sup_03": 3,
            "str_01": 2, "str_02": 2, "str_03": 3, "str_04": 4, "str_05": 2,
            "strat_01": "B", "strat_02": "A",
        }
        session = self._build_q03_session(tmp_path, answers)
        scores = session.compute_scores("q03_regulation_emotionnelle")
        assert scores is not None
        assert scores["reevaluation_cognitive"] == 3.6

    def test_q03_suppression_correct(self, tmp_path):
        answers = {
            "re_01": 4, "re_02": 4, "re_03": 3, "re_04": 4, "re_05": 3,
            "sup_01": 2, "sup_02": 2, "sup_03": 3,
            "str_01": 2, "str_02": 2, "str_03": 3, "str_04": 4, "str_05": 2,
            "strat_01": "B", "strat_02": "A",
        }
        session = self._build_q03_session(tmp_path, answers)
        scores = session.compute_scores("q03_regulation_emotionnelle")
        assert scores is not None
        assert scores["suppression"] == 2.33

    # -- Q04 Motivations SDT --

    def _build_q04_session(self, tmp_path, answers: dict) -> QuestionnaireSession:
        session = _make_session(tmp_path)
        for qid, val in answers.items():
            session.save_answer("q04_motivations_valeurs", qid, val)
        return session

    def test_q04_dominante_detection_autonomie(self, tmp_path):
        """Autonomie clairement dominante (diff >= 0.5)."""
        answers = {
            "sdt_aut_01": 7, "sdt_aut_02": 7, "sdt_aut_03": 7,
            "sdt_aut_04": 7, "sdt_aut_05": 7, "sdt_aut_06": 7,
            "sdt_comp_01": 4, "sdt_comp_02": 4, "sdt_comp_03": 4,
            "sdt_comp_04": 4, "sdt_comp_05": 4, "sdt_comp_06": 4,
            "sdt_app_01": 3, "sdt_app_02": 3, "sdt_app_03": 3,
            "sdt_app_04": 3, "sdt_app_05": 3, "sdt_app_06": 3,
        }
        session = self._build_q04_session(tmp_path, answers)
        scores = session.compute_scores("q04_motivations_valeurs")
        assert scores is not None
        assert scores["motivation_dominante"] == "autonomie"

    def test_q04_dominante_detection_competence(self, tmp_path):
        """Compétence clairement dominante."""
        answers = {
            "sdt_aut_01": 3, "sdt_aut_02": 3, "sdt_aut_03": 3,
            "sdt_aut_04": 3, "sdt_aut_05": 3, "sdt_aut_06": 3,
            "sdt_comp_01": 7, "sdt_comp_02": 7, "sdt_comp_03": 7,
            "sdt_comp_04": 7, "sdt_comp_05": 7, "sdt_comp_06": 7,
            "sdt_app_01": 3, "sdt_app_02": 3, "sdt_app_03": 3,
            "sdt_app_04": 3, "sdt_app_05": 3, "sdt_app_06": 3,
        }
        session = self._build_q04_session(tmp_path, answers)
        scores = session.compute_scores("q04_motivations_valeurs")
        assert scores is not None
        assert scores["motivation_dominante"] == "competence"

    def test_q04_equilibre_when_close(self, tmp_path):
        """Diff < 0.5 entre les deux premiers → équilibre."""
        # Autonomie et compétence très proches
        answers = {
            "sdt_aut_01": 6, "sdt_aut_02": 6, "sdt_aut_03": 5,
            "sdt_aut_04": 5, "sdt_aut_05": 6, "sdt_aut_06": 6,
            "sdt_comp_01": 5, "sdt_comp_02": 5, "sdt_comp_03": 6,
            "sdt_comp_04": 5, "sdt_comp_05": 6, "sdt_comp_06": 5,
            "sdt_app_01": 4, "sdt_app_02": 4, "sdt_app_03": 3,
            "sdt_app_04": 4, "sdt_app_05": 3, "sdt_app_06": 4,
        }
        session = self._build_q04_session(tmp_path, answers)
        scores = session.compute_scores("q04_motivations_valeurs")
        assert scores is not None
        assert scores["motivation_dominante"] == "equilibre"

    def test_q04_scores_contain_required_keys(self, tmp_path):
        answers = {k: 4 for k in [
            "sdt_aut_01", "sdt_aut_02", "sdt_aut_03", "sdt_aut_04", "sdt_aut_05", "sdt_aut_06",
            "sdt_comp_01", "sdt_comp_02", "sdt_comp_03", "sdt_comp_04", "sdt_comp_05", "sdt_comp_06",
            "sdt_app_01", "sdt_app_02", "sdt_app_03", "sdt_app_04", "sdt_app_05", "sdt_app_06",
        ]}
        session = self._build_q04_session(tmp_path, answers)
        scores = session.compute_scores("q04_motivations_valeurs")
        assert scores is not None
        for key in ("autonomie", "competence", "appartenance", "motivation_dominante"):
            assert key in scores

    # -- score partiel --

    def test_partial_score_returns_dict(self, tmp_path):
        session = _make_session(tmp_path)
        threshold = QUESTIONNAIRE_META["q01_bien_etre_subjectif"]["min_for_partial"]
        items = QUESTIONNAIRE_ITEMS["q01_bien_etre_subjectif"]
        for qid, _, _ in items[:threshold]:
            session.save_answer("q01_bien_etre_subjectif", qid, 4)
        result = session.compute_scores("q01_bien_etre_subjectif", partial=True)
        assert isinstance(result, dict)

    def test_partial_score_none_below_threshold(self, tmp_path):
        session = _make_session(tmp_path)
        session.save_answer("q01_bien_etre_subjectif", "swls_01", 4)
        result = session.compute_scores("q01_bien_etre_subjectif", partial=True)
        assert result is None

    def test_compute_scores_persists_to_file(self, tmp_path):
        """Les scores calculés doivent être persistés dans le fichier JSON."""
        session = _make_session(tmp_path)
        answers = {
            "swls_01": 5, "swls_02": 6, "swls_03": 5, "swls_04": 6, "swls_05": 4,
            "pan_p_01": 6, "pan_p_02": 5, "pan_p_03": 7, "pan_p_04": 6, "pan_p_05": 5,
            "pan_n_01": 2, "pan_n_02": 3, "pan_n_03": 2, "pan_n_04": 1,
        }
        for qid, val in answers.items():
            session.save_answer("q01_bien_etre_subjectif", qid, val)
        session.compute_scores("q01_bien_etre_subjectif")
        data = json.loads((tmp_path / "answers.json").read_text(encoding="utf-8"))
        scores = data["questionnaires"]["q01_bien_etre_subjectif"]["scores"]
        assert scores.get("swls_total") == 26
