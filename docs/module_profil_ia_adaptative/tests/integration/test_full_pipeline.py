"""
test_full_pipeline.py — Tests d'intégration end-to-end

Simule des passations complètes de questionnaires pour valider
l'ensemble du pipeline : collecte → scoring → persistance → reprise.
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT))

import pytest
from src.profile.profile_analyzer import QuestionnaireSession, QUESTIONNAIRE_ITEMS, QUESTIONNAIRE_META


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_session(tmp_path: Path) -> QuestionnaireSession:
    return QuestionnaireSession(answers_path=tmp_path / "answers.json")


def answer_all(session: QuestionnaireSession, questionnaire_id: str, value_override: dict = None) -> None:
    """Répond à toutes les questions avec des valeurs par défaut valides."""
    value_override = value_override or {}
    while True:
        q = session.next_question(questionnaire_id)
        if q is None:
            break
        qid = q["id"]
        qtype = q["type"]
        if qid in value_override:
            answer = value_override[qid]
        elif qtype == "likert_7":
            answer = 5
        elif qtype == "likert_5":
            answer = 4
        elif qtype == "choix_binaire":
            answer = "A"
        else:
            answer = "Réponse de test"
        session.save_answer(questionnaire_id, qid, answer)


# ---------------------------------------------------------------------------
# Tests d'intégration
# ---------------------------------------------------------------------------

class TestFullPipeline:
    """Tests d'intégration bout en bout."""

    def test_full_questionnaire_q01(self, tmp_path):
        """Passation complète Q01 : next_question → save_answer → compute_scores."""
        session = make_session(tmp_path)
        qid = "q01_bien_etre_subjectif"

        # Avant passation : pas de scores
        assert session.compute_scores(qid) is None

        # Passation complète
        answer_all(session, qid)

        # Après passation : scores disponibles
        scores = session.compute_scores(qid)
        assert scores is not None
        assert "swls_total" in scores
        assert "panas_positif" in scores
        assert "panas_negatif" in scores
        assert scores["is_partial"] is False

        # Scores dans les plages attendues
        assert 5 <= scores["swls_total"] <= 35
        assert 5 <= scores["panas_positif"] <= 35
        assert 4 <= scores["panas_negatif"] <= 28

    def test_full_questionnaire_q02(self, tmp_path):
        """Passation complète Q02 : style cognitif."""
        session = make_session(tmp_path)
        answer_all(session, "q02_style_cognitif")
        scores = session.compute_scores("q02_style_cognitif")
        assert scores is not None
        assert scores["profil_ai"] in ["analytique", "intuitif", "mixte"]
        assert scores["profil_vvs"] in ["verbal", "visuel_spatial", "mixte"]

    def test_full_questionnaire_q03(self, tmp_path):
        """Passation complète Q03 : régulation émotionnelle."""
        session = make_session(tmp_path)
        answer_all(session, "q03_regulation_emotionnelle")
        scores = session.compute_scores("q03_regulation_emotionnelle")
        assert scores is not None
        assert "reevaluation_cognitive" in scores
        assert "suppression" in scores
        assert "stress_percu_pss" in scores

    def test_full_questionnaire_q04(self, tmp_path):
        """Passation complète Q04 : motivations SDT."""
        session = make_session(tmp_path)
        answer_all(session, "q04_motivations_valeurs")
        scores = session.compute_scores("q04_motivations_valeurs")
        assert scores is not None
        assert "autonomie" in scores
        assert "competence" in scores
        assert "appartenance" in scores
        assert scores["motivation_dominante"] in [
            "autonomie", "competence", "appartenance", "equilibre"
        ]

    def test_multiple_questionnaires_independent(self, tmp_path):
        """Q01 et Q02 peuvent être complétés indépendamment sur le même fichier."""
        session = make_session(tmp_path)

        # Compléter Q01
        answer_all(session, "q01_bien_etre_subjectif")
        assert session.compute_scores("q01_bien_etre_subjectif") is not None

        # Q02 pas encore commencé
        assert session.compute_scores("q02_style_cognitif") is None

        # Compléter Q02
        answer_all(session, "q02_style_cognitif")
        assert session.compute_scores("q02_style_cognitif") is not None

        # Q01 toujours disponible
        assert session.compute_scores("q01_bien_etre_subjectif") is not None

    def test_session_resume_after_partial(self, tmp_path):
        """Répondre 5 questions, créer une nouvelle session, vérifier que next_question reprend."""
        answers_file = tmp_path / "answers.json"
        qid = "q01_bien_etre_subjectif"

        # Session 1 : répondre 5 questions
        session1 = QuestionnaireSession(answers_path=answers_file)
        for _ in range(5):
            q = session1.next_question(qid)
            if q:
                session1.save_answer(qid, q["question_id"], 4)

        progress_after_5 = session1.get_progress()[qid]
        assert progress_after_5["answered"] == 5

        # Session 2 (nouvel objet, même fichier) : doit reprendre à la 6ème question
        session2 = QuestionnaireSession(answers_path=answers_file)
        progress_session2 = session2.get_progress()[qid]
        assert progress_session2["answered"] == 5

        # La prochaine question doit être à l'index 5 (6ème question, 0-based)
        next_q = session2.next_question(qid)
        assert next_q is not None
        assert next_q["index"] >= 5

    def test_complete_pipeline_q01_through_q04(self, tmp_path):
        """Compléter les 4 questionnaires en séquence sur le même fichier."""
        session = make_session(tmp_path)
        questionnaires = [
            "q01_bien_etre_subjectif",
            "q02_style_cognitif",
            "q03_regulation_emotionnelle",
            "q04_motivations_valeurs",
        ]

        for qid in questionnaires:
            answer_all(session, qid)

        # Vérifier que tous ont des scores
        for qid in questionnaires:
            scores = session.compute_scores(qid)
            assert scores is not None, f"Scores manquants pour {qid}"
            assert scores["is_partial"] is False

    def test_progress_pct_increases(self, tmp_path):
        """Le pourcentage de complétion augmente à chaque réponse."""
        session = make_session(tmp_path)
        qid = "q01_bien_etre_subjectif"
        prev_pct = 0.0

        while True:
            q = session.next_question(qid)
            if q is None:
                break
            session.save_answer(qid, q["question_id"], 4)
            pct = session.get_progress()[qid]["pct_complete"]
            assert pct >= prev_pct
            prev_pct = pct

        assert prev_pct == 100.0

    def test_is_complete_flag_set_after_full_passation(self, tmp_path):
        """is_complete passe à True une fois toutes les questions répondues."""
        session = make_session(tmp_path)
        qid = "q02_style_cognitif"

        # Pas encore commencé
        assert not session.get_progress()[qid]["is_complete"]

        # Compléter
        answer_all(session, qid)

        # Maintenant complet
        assert session.get_progress()[qid]["is_complete"]
        assert session.next_question(qid) is None

    def test_partial_scores_available_at_threshold(self, tmp_path):
        """can_compute_partial_scores devient True dès le seuil atteint."""
        session = make_session(tmp_path)
        qid = "q01_bien_etre_subjectif"
        threshold = QUESTIONNAIRE_META[qid]["min_for_partial"]

        # Avant le seuil
        assert not session.can_compute_partial_scores(qid)

        # Répondre exactement le nombre de questions = seuil
        for _ in range(threshold):
            q = session.next_question(qid)
            if q:
                session.save_answer(qid, q["question_id"], 4)

        assert session.can_compute_partial_scores(qid)

        # Le score partiel est calculable
        partial_scores = session.compute_scores(qid, partial=True)
        assert partial_scores is not None
        assert partial_scores["is_partial"] is True

    def test_data_persisted_in_json(self, tmp_path):
        """Les réponses sont effectivement persistées dans le fichier JSON."""
        answers_file = tmp_path / "answers.json"
        session = QuestionnaireSession(answers_path=str(answers_file))

        # Répondre à la première question
        q = session.next_question("q01_bien_etre_subjectif")
        session.save_answer("q01_bien_etre_subjectif", q["question_id"], 6)

        # Lire le fichier directement
        with open(answers_file, "r") as f:
            data = json.load(f)

        q01_data = data.get("q01_bien_etre_subjectif", {})
        answers = q01_data.get("answers", {})
        assert answers.get(q["question_id"]) == 6

    def test_qualitative_questionnaire_no_scores(self, tmp_path):
        """Q00 (qualitatif) ne produit pas de scores numériques."""
        session = make_session(tmp_path)
        qid = "q00_profil_complementaire"

        answer_all(session, qid)
        # compute_scores retourne None pour le qualitatif
        scores = session.compute_scores(qid)
        assert scores is None
