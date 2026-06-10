"""
PROJECT      : ALFRED
BLOCK        : TESTS
FUNCTION     : B11
FILE         : tests/test_response_generator_markdown.py
ROLE         : Tests post-processing Markdown -> texte brut (ResponseGenerator)

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-06-10
UPDATED      : 2026-06-10
VERSION      : V1.0
STATUS       : TESTED

DESCRIPTION :
Vérifie que _post_process() neutralise toutes les syntaxes Markdown
courantes produites par les LLM locaux (llama3.2 ignore parfois la
consigne "pas de Markdown").
"""

import sys
import os

sys.path.insert(0, os.path.abspath("."))

from src.core.response_generator import ResponseGenerator


def _clean(text: str) -> str:
    gen = ResponseGenerator()
    return gen._post_process(text, context={})


def test_bold_double_star_removed():
    assert _clean("Voici un mot **important** ici.") == "Voici un mot important ici."


def test_italic_underscore_removed():
    assert _clean("C'est _vraiment_ utile.") == "C'est vraiment utile."


def test_bullet_star_converted_to_dash():
    result = _clean("* premier point\n* deuxième point")
    assert result == "- premier point\n- deuxième point"


def test_heading_removed():
    assert _clean("## Titre important\nContenu") == "Titre important\nContenu"


def test_inline_code_removed():
    assert _clean("Lance la commande `pip install x`.") == "Lance la commande pip install x."


def test_code_block_removed():
    result = _clean("Voici :\n```python\nprint(1)\n```\nFin")
    assert "```" not in result
    assert "print(1)" in result


def test_link_kept_as_text():
    assert _clean("Va voir [le site](https://example.com) pour plus.") == \
        "Va voir le site pour plus."


def test_strikethrough_removed():
    assert _clean("Ce n'est ~~pas~~ très utile.") == "Ce n'est pas très utile."


def test_blockquote_removed():
    assert _clean("> citation importante\nsuite") == "citation importante\nsuite"


def test_horizontal_rule_removed():
    result = _clean("Avant\n---\nAprès")
    assert "---" not in result
    assert "Avant" in result and "Après" in result


def test_plain_text_unchanged():
    assert _clean("Bonjour, comment vas-tu aujourd'hui ?") == \
        "Bonjour, comment vas-tu aujourd'hui ?"


def test_empty_response_fallback():
    assert _clean("") == "Je n’ai pas de réponse fiable pour le moment."


def test_combined_markdown():
    raw = (
        "## Résumé\n"
        "* **Point 1** : voir `config.json`\n"
        "* Point 2 avec [lien](http://x.com) et _emphase_\n"
        "---\n"
        "> Note finale"
    )
    result = _clean(raw)
    for forbidden in ("##", "**", "`", "[", "](", "~~", "---"):
        assert forbidden not in result
    assert "Résumé" in result
    assert "Point 1" in result
    assert "config.json" in result
    assert "lien" in result
    assert "emphase" in result
    assert "Note finale" in result
