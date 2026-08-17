"""
PROJECT      : ALFRED
BLOCK        : TESTS
FUNCTION     : B11
FILE         : tests/test_response_generator_tutoiement.py
ROLE         : Tests post-processing tutoiement forcé (ResponseGenerator)

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-07-22
UPDATED      : 2026-07-22
VERSION      : V1.0
STATUS       : TESTED

DESCRIPTION :
Vérifie que _enforce_tutoiement() corrige le vouvoiement résiduel produit
par le LLM local malgré la consigne du prompt système (filet de sécurité
déterministe, même principe que le nettoyage Markdown de
test_response_generator_markdown.py).
"""

import sys
import os

sys.path.insert(0, os.path.abspath("."))

from src.core.response_generator import ResponseGenerator


def _fix(text: str) -> str:
    return ResponseGenerator._enforce_tutoiement(text)


def test_subject_verb_etre():
    assert _fix("Vous êtes prêt.") == "Tu es prêt."


def test_subject_verb_avoir():
    assert _fix("Vous avez raison.") == "Tu as raison."


def test_subject_verb_pouvoir():
    assert _fix("Vous pouvez continuer.") == "Tu peux continuer."


def test_subject_verb_devoir_conditionnel():
    assert _fix("Vous devriez vérifier.") == "Tu devrais vérifier."


def test_preposition_pour():
    assert _fix("C'est prêt pour vous.") == "C'est prêt pour toi."


def test_preposition_avec():
    assert _fix("Je reste avec vous.") == "Je reste avec toi."


def test_object_pronoun_elision():
    assert _fix("Je vous aide.") == "Je t’aide."


def test_object_pronoun_no_elision():
    assert _fix("Je vous recommande ceci.") == "Je te recommande ceci."


def test_reflexive_pronoun_reconjugated():
    assert _fix("Vous vous inquiétez trop.") == "Tu t’inquiétes trop."


def test_generic_ez_verb_reconjugated():
    assert _fix("Vous confirmez votre choix ?") == "Tu confirmes ton choix ?"


def test_votre_to_ton():
    assert _fix("Votre planning est chargé.") == "Ton planning est chargé."


def test_vos_to_tes():
    assert _fix("Vérifie vos messages.") == "Vérifie tes messages."


def test_bare_vous_fallback():
    assert _fix("Vous ?") == "Tu ?"


def test_rendez_vous_noun_protected():
    assert _fix("N'oublie pas ton rendez-vous.") == "N'oublie pas ton rendez-vous."
    assert _fix("Vous avez un rendez-vous demain.") == "Tu as un rendez-vous demain."


def test_capitalization_preserved_at_sentence_start():
    result = _fix("Vous êtes prêt. Vous pouvez y aller.")
    assert result == "Tu es prêt. Tu peux y aller."


def test_already_tutoyant_text_unchanged():
    assert _fix("Tu es prêt, tu peux y aller.") == "Tu es prêt, tu peux y aller."


def test_no_naked_vous_survives_combined_sentence():
    raw = "Bien sûr, je vous explique votre planning pour vous et vos tâches."
    result = _fix(raw)
    for forbidden in (" vous ", " vous.", " vous,", " vous?", " vous!",
                      "votre", "vos "):
        assert forbidden not in result.lower(), (forbidden, result)


# ── Session 5 (17-24/08/2026) — bugs trouvés en vérifiant que le filet ne
# casse pas le ton taquin/charme de la persona privée (voir _build_persona_block).
# Pas une régression de la persona elle-même : le filet produisait déjà du
# français cassé sur ces tournures avant que la persona ne les rende courantes.

def test_preposition_a_vous():
    assert _fix("Je pense à vous.") == "Je pense à toi."


def test_object_vous_before_impersonal_verb():
    assert _fix("Ça vous étonne ?") == "Ça t’étonne ?"
    assert _fix("Cela vous dérange ?") == "Cela te dérange ?"


def test_subject_vous_with_intervening_object_pronoun_regular_verb():
    assert _fix("Vous me confirmez que ça marche ?") == "Tu me confirmes que ça marche ?"


def test_subject_vous_with_intervening_object_pronoun_irregular_faire():
    assert _fix("Vous me faites sourire.") == "Tu me fais sourire."


def test_subject_vous_with_intervening_object_pronoun_irregular_dire():
    assert _fix("Vous nous dites tout ?") == "Tu nous dis tout ?"


def test_combined_flirty_sentence_fully_tutoyant():
    raw = "Vous êtes charmante, et ça vous étonne que vous me fassiez sourire ?"
    result = _fix(raw)
    for forbidden in (" vous ", " vous?", " vous!", " vous."):
        assert forbidden not in result.lower(), (forbidden, result)
