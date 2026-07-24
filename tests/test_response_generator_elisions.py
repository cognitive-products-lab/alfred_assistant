"""
PROJECT      : ALFRED
BLOCK        : TESTS
FUNCTION     : B11
FILE         : tests/test_response_generator_elisions.py
ROLE         : Tests correction d'élision manquante (ResponseGenerator)

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-07-24
VERSION      : V1.0
STATUS       : TESTED

DESCRIPTION :
Observé en usage réel le 24/07/2026 : le LLM local produit parfois "de être"
au lieu de "d'être". _fix_elisions() corrige "de" + mot à voyelle initiale,
jamais "de" + "h" (pour ne pas fausse-élider un h aspiré, ex. "de haut").
"""

import sys
import os

sys.path.insert(0, os.path.abspath("."))

from src.core.response_generator import ResponseGenerator


def _clean(text: str) -> str:
    gen = ResponseGenerator()
    return gen._post_process(text, context={})


def test_de_etre_becomes_d_etre():
    assert ResponseGenerator._fix_elisions("capable de être présent") == "capable d'être présent"


def test_uppercase_de_preserves_case():
    assert ResponseGenerator._fix_elisions("De être honnête, c'est important.") == "D'être honnête, c'est important."


def test_de_avant_consonne_inchange():
    assert ResponseGenerator._fix_elisions("de faire quelque chose") == "de faire quelque chose"


def test_de_avant_h_aspire_inchange():
    """Jamais d'élision devant "h" — h aspiré vs h muet non distinguable
    sans dictionnaire, mieux vaut ne jamais élider que fausse-élider."""
    assert ResponseGenerator._fix_elisions("de haut en bas") == "de haut en bas"


def test_de_avant_accent_circonflexe():
    assert ResponseGenerator._fix_elisions("de être et de éviter") == "d'être et d'éviter"


def test_fix_elisions_applied_through_post_process():
    assert _clean("Tu es capable de être toi-même.") == "Tu es capable d'être toi-même."
