"""
PROJECT      : ALFRED
BLOCK        : B22
FUNCTION     : SMOKE
FILE         : tests/b22_tests/test_smoke_batch1.py
ROLE         : Smoke tests (lot 1) pour les modules d'accessibilité B22
               sans couverture de test (cognitive/, ui/, settings JSON).

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-07-05
UPDATED      : 2026-07-05
VERSION      : V1.0
STATUS       : TESTED

DESCRIPTION :
Verifie import + comportement de base des modules "skeleton" d'accessibilite.
Documente aussi un bug reel decouvert : wcag_checker.py ne peut pas s'importer
(chemin relatif errone + noms de fonctions inexistants dans web_a11y.py).
"""

import json
from pathlib import Path

import pytest

try:
    from pypdf import PdfReader
except ImportError:
    from PyPDF2 import PdfReader

from src.accessibility.cognitive.summarizer import summarize, simplify_for_reading, summarize_for_voice
from src.accessibility.cognitive.explain_terms import explain_term, annotate_text, list_known_acronyms
from src.accessibility.cognitive.fatigue_reducer import FatigueReducer
from src.accessibility.cognitive.neurodiversity import NeurodiversityAdapter
from src.accessibility.ui.visual_adapter import VisualAdapter
from src.accessibility.ui.android_a11y import AndroidA11y
from src.accessibility.ui.web_a11y import WebA11y

ROOT = Path(__file__).resolve().parents[2]


# ── summarizer.py ────────────────────────────────────────────

def test_summarize_truncates_to_max_sentences():
    text = "Phrase un. Phrase deux. Phrase trois. Phrase quatre."
    result = summarize(text, max_sentences=2)
    assert result == "Phrase un. Phrase deux."


def test_summarize_for_voice_strips_newlines():
    result = summarize_for_voice("Phrase un.\nPhrase deux.", max_sentences=2)
    assert "\n" not in result


def test_simplify_for_reading_uses_provided_function():
    result = simplify_for_reading("texte complexe", simplify_fn=lambda t: t.upper())
    assert result == "TEXTE COMPLEXE"


# ── explain_terms.py ─────────────────────────────────────────

def test_explain_term_known_acronym():
    assert explain_term("RGPD") == "Règlement Général sur la Protection des Données"


def test_explain_term_unknown_without_knowledge_fn():
    assert explain_term("XYZINCONNU") is None


def test_annotate_text_finds_acronyms():
    result = annotate_text("Le RAG et la RGPD sont importants.")
    assert "RAG" in result["annotations"]
    assert "RGPD" in result["annotations"]


def test_list_known_acronyms_returns_copy():
    acronyms = list_known_acronyms()
    acronyms["NEW"] = "test"
    assert "NEW" not in list_known_acronyms()


# ── fatigue_reducer.py ───────────────────────────────────────

def test_fatigue_reducer_chunks_long_text():
    fr = FatigueReducer(chunk_words=10)
    text = ("Ceci est une phrase test. " * 7).strip()
    result = fr.chunk(text)
    assert len(result.chunks) >= 2
    assert result.total_words == 35


def test_fatigue_reducer_format_with_pauses_inserts_message():
    fr = FatigueReducer(chunk_words=5)
    text = ("Une phrase courte. " * 12).strip()
    output = fr.format_with_pauses(text)
    assert any("pause" in line.lower() for line in output)


# ── neurodiversity.py ────────────────────────────────────────

def test_neurodiversity_adapter_replaces_metaphors_in_autism_mode():
    adapter = NeurodiversityAdapter("autism")
    result = adapter.apply("C'est comme une montagne de travail.")
    assert "très grand" in result
    assert "comme une montagne" not in result


def test_neurodiversity_adapter_unknown_mode_falls_back_to_standard():
    adapter = NeurodiversityAdapter("mode_inexistant")
    assert adapter.get_profile().mode == "standard"


def test_neurodiversity_adapter_set_mode():
    adapter = NeurodiversityAdapter("standard")
    adapter.set_mode("adhd")
    assert adapter.get_profile().mode == "adhd"
    assert adapter.get_profile().max_sentence_words == 15


# ── visual_adapter.py ────────────────────────────────────────

def test_visual_adapter_dyslexia_profile_css():
    adapter = VisualAdapter("dyslexia")
    css = adapter.to_css()
    assert "OpenDyslexic" in css
    assert adapter.get_profile().name == "dyslexia"


def test_visual_adapter_unknown_profile_falls_back_to_standard():
    adapter = VisualAdapter("profil_inexistant")
    assert adapter.get_profile().name == "standard"


def test_visual_adapter_adapt_text_for_dyslexia_adds_breaks():
    adapter = VisualAdapter()
    result = adapter.adapt_text_for_dyslexia("Phrase un. Phrase deux.")
    assert "\n" in result


# ── android_a11y.py ──────────────────────────────────────────

def test_android_a11y_low_vision_profile():
    a11y = AndroidA11y("low_vision")
    config = a11y.get_config()
    assert config["font_scale"] == 1.4
    assert config["min_contrast_ratio"] == 7.0


def test_android_a11y_talkback_label_known_and_fallback():
    a11y = AndroidA11y()
    assert a11y.talkback_label("btn_send") == "Envoyer le message"
    assert a11y.talkback_label("bouton_inconnu") == "Bouton Inconnu"


def test_android_a11y_check_touch_target():
    a11y = AndroidA11y("motor")
    assert a11y.check_touch_target(64) is True
    assert a11y.check_touch_target(40) is False


# ── web_a11y.py ──────────────────────────────────────────────

def test_web_a11y_aria_attrs():
    wa = WebA11y()
    attrs = wa.aria_attrs("button", "Envoyer", expanded=True, live="polite")
    assert attrs["role"] == "button"
    assert attrs["aria-expanded"] == "true"
    assert attrs["aria-live"] == "polite"


def test_web_a11y_contrast_ratio_black_on_white():
    wa = WebA11y()
    result = wa.check_contrast("#000000", "#ffffff")
    assert result["passe_AAA"] is True


def test_web_a11y_audit_dashboard_returns_summary():
    wa = WebA11y()
    audit = wa.audit_dashboard()
    assert audit["total"] == len(wa.DASHBOARD_COLORS)


# ── accessibility_settings.json ──────────────────────────────

def test_accessibility_settings_json_structure():
    data = json.loads(
        (ROOT / "src" / "accessibility" / "accessibility_settings.json").read_text(encoding="utf-8")
    )
    assert "_alfred_header" in data
    assert "preferred_language" in data
    assert data["supported_languages"] == ["fr", "en", "es", "de", "it"]


# ── ALFRED_Accessibility_Policy.pdf ──────────────────────────

def test_accessibility_policy_pdf_is_valid_and_readable():
    path = ROOT / "docs" / "accessibility" / "ALFRED_Accessibility_Policy.pdf"
    reader = PdfReader(str(path))
    assert len(reader.pages) == 3
    text = reader.pages[0].extract_text()
    assert "Accessibility" in text


# ── wcag_checker.py (fixe le 2026-07-05 : import + delegation WebA11y) ─

from src.accessibility.wcag_checker import check_wcag, wcag_report, audit_dashboard


def test_check_wcag_contrast_criterion():
    issues = check_wcag({"fg": "#000000", "bg": "#ffffff"})
    assert len(issues) == 1
    assert issues[0].criterion == "1.4.3"
    assert issues[0].passed is True


def test_check_wcag_multiple_criteria():
    issues = check_wcag({
        "has_alt_text": False,
        "has_label": True,
        "has_keyboard_nav": True,
        "has_focus_visible": False,
        "lang": "fr",
    })
    by_criterion = {i.criterion: i for i in issues}
    assert by_criterion["1.1.1"].passed is False
    assert by_criterion["4.1.2"].passed is True
    assert by_criterion["2.4.7"].passed is False
    assert by_criterion["3.1.1"].passed is True


def test_wcag_report_score_and_conformance():
    report = wcag_report({"fg": "#000000", "bg": "#ffffff", "has_alt_text": True})
    assert report["score"] == 100
    assert report["conformance_level"] == "AA"
    assert report["failed"] == 0


def test_wcag_report_empty_component_data_defaults_to_full_score():
    report = wcag_report({})
    assert report["total_checks"] == 0
    assert report["score"] == 100


def test_audit_dashboard_delegates_to_web_a11y():
    result = audit_dashboard()
    assert "total" in result
    assert "passing_AA" in result
    assert "details" in result
