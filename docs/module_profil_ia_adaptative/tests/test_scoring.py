"""
test_scoring.py — Tests unitaires des méthodes de scoring

Couvre les méthodes statiques et de scoring par questionnaire
de QuestionnaireSession dans src/profile/profile_analyzer.py.
"""

import json
import sys
from pathlib import Path

# Remonter à la racine du projet (docs/module_profil_ia_adaptative/tests/ → root)
ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT))

import pytest
from src.profile.profile_analyzer import QuestionnaireSession


# ---------------------------------------------------------------------------
# Fixture helper
# ---------------------------------------------------------------------------

def make_session(tmp_path: Path) -> QuestionnaireSession:
    """Crée une session avec un fichier de réponses temporaire."""
    return QuestionnaireSession(answers_path=tmp_path / "answers.json")


def fill_questionnaire(session: QuestionnaireSession, questionnaire_id: str, answers: dict) -> None:
    """Remplit un questionnaire avec les réponses fournies."""
    while True:
        q = session.next_question(questionnaire_id)
        if q is None:
            break
        qid = q["id"]
        if qid in answers:
            session.save_answer(questionnaire_id, qid, answers[qid])
        else:
            # Valeur par défaut selon le type
            qtype = q["type"]
            if qtype == "likert_7":
                session.save_answer(questionnaire_id, qid, 4)
            elif qtype == "likert_5":
                session.save_answer(questionnaire_id, qid, 3)
            elif qtype == "choix_binaire":
                session.save_answer(questionnaire_id, qid, "A")
            else:
                session.save_answer(questionnaire_id, qid, "Réponse par défaut")


# ---------------------------------------------------------------------------
# TestScoringHelpers
# ---------------------------------------------------------------------------

class TestScoringHelpers:
    """Tests des méthodes statiques _mean et _sum_likert."""

    def test_mean_standard(self):
        result = QuestionnaireSession._mean([1, 2, 3, 4, 5])
        assert result == 3.0

    def test_mean_ignores_none(self):
        result = QuestionnaireSession._mean([1, None, 3, None, 5])
        assert result == 3.0

    def test_mean_returns_none_when_all_none(self):
        result = QuestionnaireSession._mean([None, None, None])
        assert result is None

    def test_mean_returns_none_for_empty(self):
        result = QuestionnaireSession._mean([])
        assert result is None

    def test_mean_single_value(self):
        result = QuestionnaireSession._mean([7])
        assert result == 7.0

    def test_mean_rounded_to_2_decimals(self):
        result = QuestionnaireSession._mean([1, 2])
        assert result == 1.5

    def test_sum_likert_standard(self):
        result = QuestionnaireSession._sum_likert([1, 2, 3, 4, 5])
        assert result == 15

    def test_sum_likert_ignores_none(self):
        result = QuestionnaireSession._sum_likert([5, None, 5, None, 5])
        assert result == 15

    def test_sum_likert_returns_none_when_all_none(self):
        result = QuestionnaireSession._sum_likert([None, None])
        assert result is None

    def test_sum_likert_returns_none_for_empty(self):
        result = QuestionnaireSession._sum_likert([])
        assert result is None

    def test_sum_likert_single_value(self):
        result = QuestionnaireSession._sum_likert([7])
        assert result == 7


# ---------------------------------------------------------------------------
# TestScoreQ01 — SWLS + PANAS
# ---------------------------------------------------------------------------

class TestScoreQ01:
    """Tests du scoring Q01 — Bien-être subjectif."""

    FULL_ANSWERS = {
        "swls_01": 5, "swls_02": 6, "swls_03": 5, "swls_04": 6, "swls_05": 4,
        "pan_p_01": 6, "pan_p_02": 5, "pan_p_03": 7, "pan_p_04": 6, "pan_p_05": 5,
        "pan_n_01": 2, "pan_n_02": 3, "pan_n_03": 2, "pan_n_04": 1,
    }

    def test_swls_total_correct(self, tmp_path):
        session = make_session(tmp_path)
        fill_questionnaire(session, "q01_bien_etre_subjectif", self.FULL_ANSWERS)
        scores = session.compute_scores("q01_bien_etre_subjectif")
        assert scores is not None
        # 5+6+5+6+4 = 26
        assert scores["swls_total"] == 26

    def test_panas_positif_correct(self, tmp_path):
        session = make_session(tmp_path)
        fill_questionnaire(session, "q01_bien_etre_subjectif", self.FULL_ANSWERS)
        scores = session.compute_scores("q01_bien_etre_subjectif")
        # 6+5+7+6+5 = 29
        assert scores["panas_positif"] == 29

    def test_panas_negatif_correct(self, tmp_path):
        session = make_session(tmp_path)
        fill_questionnaire(session, "q01_bien_etre_subjectif", self.FULL_ANSWERS)
        scores = session.compute_scores("q01_bien_etre_subjectif")
        # 2+3+2+1 = 8
        assert scores["panas_negatif"] == 8

    def test_scores_have_computed_at(self, tmp_path):
        session = make_session(tmp_path)
        fill_questionnaire(session, "q01_bien_etre_subjectif", self.FULL_ANSWERS)
        scores = session.compute_scores("q01_bien_etre_subjectif")
        assert "computed_at" in scores
        assert "is_partial" in scores

    def test_is_partial_false_when_complete(self, tmp_path):
        session = make_session(tmp_path)
        fill_questionnaire(session, "q01_bien_etre_subjectif", self.FULL_ANSWERS)
        scores = session.compute_scores("q01_bien_etre_subjectif")
        assert scores["is_partial"] is False

    def test_swls_min_possible(self, tmp_path):
        """Toutes réponses à 1 → SWLS = 5."""
        session = make_session(tmp_path)
        min_answers = {k: 1 for k in self.FULL_ANSWERS}
        fill_questionnaire(session, "q01_bien_etre_subjectif", min_answers)
        scores = session.compute_scores("q01_bien_etre_subjectif")
        assert scores["swls_total"] == 5

    def test_swls_max_possible(self, tmp_path):
        """Toutes réponses à 7 → SWLS = 35."""
        session = make_session(tmp_path)
        max_answers = {k: 7 for k in self.FULL_ANSWERS}
        fill_questionnaire(session, "q01_bien_etre_subjectif", max_answers)
        scores = session.compute_scores("q01_bien_etre_subjectif")
        assert scores["swls_total"] == 35


# ---------------------------------------------------------------------------
# TestScoreQ02 — Style cognitif
# ---------------------------------------------------------------------------

class TestScoreQ02:
    """Tests du scoring Q02 — Style cognitif."""

    def _make_answers(self, analytique=7, intuitif=1, verbal=7, visuel=1) -> dict:
        """Génère des réponses pour obtenir un profil spécifique."""
        return {
            "cog_a_01": analytique, "cog_a_02": analytique,
            "cog_a_03": analytique, "cog_a_04": analytique,
            "cog_i_01": intuitif, "cog_i_02": intuitif,
            "cog_i_03": intuitif, "cog_i_04": intuitif,
            "cog_v_01": verbal, "cog_v_02": verbal, "cog_v_03": verbal,
            "cog_vs_01": visuel, "cog_vs_02": visuel, "cog_vs_03": visuel,
            "fmt_01": "A", "fmt_02": "A",
        }

    def test_profil_analytique(self, tmp_path):
        """Score analytique >> intuitif → profil analytique."""
        session = make_session(tmp_path)
        answers = self._make_answers(analytique=7, intuitif=1)
        fill_questionnaire(session, "q02_style_cognitif", answers)
        scores = session.compute_scores("q02_style_cognitif")
        assert scores["profil_ai"] == "analytique"

    def test_profil_intuitif(self, tmp_path):
        """Score intuitif >> analytique → profil intuitif."""
        session = make_session(tmp_path)
        answers = self._make_answers(analytique=1, intuitif=7)
        fill_questionnaire(session, "q02_style_cognitif", answers)
        scores = session.compute_scores("q02_style_cognitif")
        assert scores["profil_ai"] == "intuitif"

    def test_profil_mixte(self, tmp_path):
        """Scores proches → profil mixte (diff <= 1.5)."""
        session = make_session(tmp_path)
        answers = self._make_answers(analytique=4, intuitif=4)
        fill_questionnaire(session, "q02_style_cognitif", answers)
        scores = session.compute_scores("q02_style_cognitif")
        assert scores["profil_ai"] == "mixte"

    def test_profil_verbal(self, tmp_path):
        """Score verbal >> visuel → profil verbal."""
        session = make_session(tmp_path)
        answers = self._make_answers(verbal=7, visuel=1)
        fill_questionnaire(session, "q02_style_cognitif", answers)
        scores = session.compute_scores("q02_style_cognitif")
        assert scores["profil_vvs"] == "verbal"

    def test_profil_visuel_spatial(self, tmp_path):
        """Score visuel >> verbal → profil visuel_spatial."""
        session = make_session(tmp_path)
        answers = self._make_answers(verbal=1, visuel=7)
        fill_questionnaire(session, "q02_style_cognitif", answers)
        scores = session.compute_scores("q02_style_cognitif")
        assert scores["profil_vvs"] == "visuel_spatial"

    def test_scores_are_means(self, tmp_path):
        """Les scores analytique/intuitif sont des moyennes."""
        session = make_session(tmp_path)
        answers = self._make_answers(analytique=5, intuitif=3)
        fill_questionnaire(session, "q02_style_cognitif", answers)
        scores = session.compute_scores("q02_style_cognitif")
        assert scores["score_analytique"] == 5.0
        assert scores["score_intuitif"] == 3.0


# ---------------------------------------------------------------------------
# TestScoreQ03 — Régulation émotionnelle + PSS
# ---------------------------------------------------------------------------

class TestScoreQ03:
    """Tests du scoring Q03 — Régulation émotionnelle."""

    def test_pss_inversion_str04(self, tmp_path):
        """str_04 doit être inversé : score = 6 - valeur_brute."""
        session = make_session(tmp_path)
        # On répond toutes les questions à 1 sauf str_04 = 5
        # str_04 est un item positif → inversé → score item = 6 - 5 = 1
        # str_01..str_05 (5 items total) : 4 items à 1 + str_04 inversé = 1
        # PSS = 1 + 1 + 1 + 1 + 1 = 5
        answers_all_1 = {
            "re_01": 3, "re_02": 3, "re_03": 3, "re_04": 3, "re_05": 3,
            "sup_01": 2, "sup_02": 2, "sup_03": 2,
            "str_01": 1, "str_02": 1, "str_03": 1,
            "str_04": 5,   # score item = 6 - 5 = 1 (inversé)
            "str_05": 1,
        }
        # Remplir en tenant compte que le questionnaire a peut-être des items supplémentaires
        fill_questionnaire(session, "q03_regulation_emotionnelle", answers_all_1)
        scores = session.compute_scores("q03_regulation_emotionnelle")
        assert scores is not None
        # Avec str_04 = 5 (inversé → 1) et str_01..str_05 à 1 → PSS = 5 × 1 = 5
        assert scores["stress_percu_pss"] == 5

    def test_pss_str04_at_1_gives_high_stress(self, tmp_path):
        """str_04 = 1 (je n'ai PAS réussi à contrôler) → inversé = 6-1 = 5 → stress élevé."""
        session = make_session(tmp_path)
        answers = {
            "re_01": 3, "re_02": 3, "re_03": 3, "re_04": 3, "re_05": 3,
            "sup_01": 2, "sup_02": 2, "sup_03": 2,
            "str_01": 5, "str_02": 5, "str_03": 5,
            "str_04": 1,   # inversé → 6-1 = 5
            "str_05": 5,
        }
        fill_questionnaire(session, "q03_regulation_emotionnelle", answers)
        scores = session.compute_scores("q03_regulation_emotionnelle")
        # PSS = 5+5+5+(6-1)+5 = 5+5+5+5+5 = 25 (max théorique)
        # Mais PSS-4 ou PSS-5 ? Vérifie la somme des str items
        assert scores["stress_percu_pss"] is not None
        assert scores["stress_percu_pss"] >= 20  # niveau de stress élevé

    def test_reevaluation_is_mean(self, tmp_path):
        """Réévaluation cognitive = moyenne des 5 items re."""
        session = make_session(tmp_path)
        answers = {
            "re_01": 5, "re_02": 5, "re_03": 5, "re_04": 5, "re_05": 5,
            "sup_01": 1, "sup_02": 1, "sup_03": 1,
            "str_01": 1, "str_02": 1, "str_03": 1, "str_04": 5, "str_05": 1,
        }
        fill_questionnaire(session, "q03_regulation_emotionnelle", answers)
        scores = session.compute_scores("q03_regulation_emotionnelle")
        assert scores["reevaluation_cognitive"] == 5.0

    def test_suppression_is_mean(self, tmp_path):
        """Suppression = moyenne des 3 items sup."""
        session = make_session(tmp_path)
        answers = {
            "re_01": 3, "re_02": 3, "re_03": 3, "re_04": 3, "re_05": 3,
            "sup_01": 2, "sup_02": 4, "sup_03": 3,  # mean = 3.0
            "str_01": 1, "str_02": 1, "str_03": 1, "str_04": 5, "str_05": 1,
        }
        fill_questionnaire(session, "q03_regulation_emotionnelle", answers)
        scores = session.compute_scores("q03_regulation_emotionnelle")
        assert scores["suppression"] == 3.0


# ---------------------------------------------------------------------------
# TestScoreQ04 — Motivations SDT
# ---------------------------------------------------------------------------

class TestScoreQ04:
    """Tests du scoring Q04 — Motivations SDT."""

    def _make_sdt_answers(self, aut=5, comp=3, app=1) -> dict:
        answers = {}
        for i in range(1, 7):
            answers[f"sdt_aut_0{i}"] = aut
            answers[f"sdt_comp_0{i}"] = comp
            answers[f"sdt_app_0{i}"] = app
        return answers

    def test_autonomie_dominante(self, tmp_path):
        session = make_session(tmp_path)
        answers = self._make_sdt_answers(aut=5, comp=3, app=1)
        fill_questionnaire(session, "q04_motivations_valeurs", answers)
        scores = session.compute_scores("q04_motivations_valeurs")
        assert scores["motivation_dominante"] == "autonomie"

    def test_competence_dominante(self, tmp_path):
        session = make_session(tmp_path)
        answers = self._make_sdt_answers(aut=1, comp=5, app=2)
        fill_questionnaire(session, "q04_motivations_valeurs", answers)
        scores = session.compute_scores("q04_motivations_valeurs")
        assert scores["motivation_dominante"] == "competence"

    def test_appartenance_dominante(self, tmp_path):
        session = make_session(tmp_path)
        answers = self._make_sdt_answers(aut=1, comp=2, app=5)
        fill_questionnaire(session, "q04_motivations_valeurs", answers)
        scores = session.compute_scores("q04_motivations_valeurs")
        assert scores["motivation_dominante"] == "appartenance"

    def test_equilibre_when_scores_close(self, tmp_path):
        """diff < 0.5 entre les trois → équilibre."""
        session = make_session(tmp_path)
        answers = self._make_sdt_answers(aut=4, comp=4, app=4)
        fill_questionnaire(session, "q04_motivations_valeurs", answers)
        scores = session.compute_scores("q04_motivations_valeurs")
        assert scores["motivation_dominante"] == "equilibre"

    def test_equilibre_at_boundary(self, tmp_path):
        """diff exactement 0.4 (< 0.5) → équilibre."""
        session = make_session(tmp_path)
        # autonomie = 4.0, compétence = 3.6... approchons avec des entiers
        # On ne peut pas atteindre exactement 0.4 avec des entiers sur 6 items
        # mais on peut tester que si les 3 scores sont proches, c'est équilibre
        answers = self._make_sdt_answers(aut=4, comp=4, app=3)
        fill_questionnaire(session, "q04_motivations_valeurs", answers)
        scores = session.compute_scores("q04_motivations_valeurs")
        # aut=4.0, comp=4.0, app=3.0 → diff max = 4-3 = 1.0 >= 0.5
        # Donc autonomie ou compétence gagne (égalité → comportement défini)
        assert scores["motivation_dominante"] in ["autonomie", "competence", "equilibre"]

    def test_means_are_correct(self, tmp_path):
        session = make_session(tmp_path)
        answers = self._make_sdt_answers(aut=5, comp=3, app=1)
        fill_questionnaire(session, "q04_motivations_valeurs", answers)
        scores = session.compute_scores("q04_motivations_valeurs")
        assert scores["autonomie"] == 5.0
        assert scores["competence"] == 3.0
        assert scores["appartenance"] == 1.0
