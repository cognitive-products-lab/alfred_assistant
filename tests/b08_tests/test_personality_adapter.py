"""
════════════════════════════════════════════════════════════
PROJECT      : ALFRED
BLOCK        : B08
FUNCTION     : 08.TEST
FILE         : tests/b08_tests/test_personality_adapter.py
ROLE         : Tests unitaires — PersonalityAdapter

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-05-23
UPDATED      : 2026-05-23
VERSION      : V1.0
STATUS       : ACTIVE

DESCRIPTION :
Tests B08 — PersonalityAdapter : validation de l'adaptation de personnalité,
profils utilisateurs, ajustements contextuels.
════════════════════════════════════════════════════════════
"""

import json
import shutil
import tempfile
from pathlib import Path

import pytest

from src.core.personality_adapter import PersonalityAdapter


# ============================================================
# Fixtures JSON minimales
# ============================================================

PERSONALITY_CORE = {
    "assistant_identity": {
        "name": "ALFRED",
        "version": "V1",
        "role": "assistant virtuel adaptatif",
        "mission": "accompagner et structurer.",
        "core_positioning": "IA locale au service de l'humain"
    },
    "stable_personality": {
        "archetype": "assistant_protecteur",
        "dominant_traits": ["empathique", "structure"],
        "forbidden_traits": ["manipulateur"]
    },
    "communication_style": {
        "default_tone": "clair, direct, structure"
    },
    "emotional_behavior": {
        "support": True
    },
    "boundaries": {
        "no_medical_diagnosis": True
    },
    "safety": {
        "no_manipulation": True
    },
    "metadata": {
        "is_template": False
    }
}

USER_PROFILE = {
    "user_profile": {
        "user_id": "test-user-001",
        "preferred_name": "Celine",
        "language_preference": "fr",
        "profile_status": "active"
    },
    "preferences": {
        "tone": "direct et empathique",
        "response_length": "medium",
        "tone_when_fatigued": "doux et rassurant",
        "tone_when_strategic": "expert et direct",
        "tone_when_learning": "pedagogique"
    },
    "metadata": {
        "is_template": False
    },
    "privacy_and_consent": {
        "data_retention": "session_only"
    }
}

PERSONALITY_TEMPLATE = {
    **PERSONALITY_CORE,
    "metadata": {"is_template": True}
}

USER_PROFILE_TEMPLATE = {
    **USER_PROFILE,
    "metadata": {"is_template": True}
}


# ============================================================
# Helpers
# ============================================================

def _write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")


def _make_adapter(tmp: str, personality=None, user=None, allow_templates=False):
    p_path = Path(tmp) / "personality.json"
    u_path = Path(tmp) / "user_profile.json"
    _write_json(p_path, personality or PERSONALITY_CORE)
    _write_json(u_path, user or USER_PROFILE)
    return PersonalityAdapter(str(p_path), str(u_path), allow_templates=allow_templates)


# ============================================================
# Class TestPersonalityAdapterInit
# ============================================================

class TestPersonalityAdapterInit:
    """Tests initialisation PersonalityAdapter."""

    def test_init_success(self):
        tmp = tempfile.mkdtemp()
        try:
            adapter = _make_adapter(tmp)
            assert adapter is not None
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_personality_core_loaded(self):
        tmp = tempfile.mkdtemp()
        try:
            adapter = _make_adapter(tmp)
            assert adapter.personality_core["assistant_identity"]["name"] == "ALFRED"
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_user_profile_loaded(self):
        tmp = tempfile.mkdtemp()
        try:
            adapter = _make_adapter(tmp)
            assert adapter.user_profile["user_profile"]["preferred_name"] == "Celine"
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_missing_personality_file_raises(self):
        tmp = tempfile.mkdtemp()
        try:
            u_path = Path(tmp) / "user_profile.json"
            _write_json(u_path, USER_PROFILE)
            with pytest.raises(FileNotFoundError):
                PersonalityAdapter(
                    str(Path(tmp) / "missing.json"),
                    str(u_path)
                )
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_missing_user_profile_raises(self):
        tmp = tempfile.mkdtemp()
        try:
            p_path = Path(tmp) / "personality.json"
            _write_json(p_path, PERSONALITY_CORE)
            with pytest.raises(FileNotFoundError):
                PersonalityAdapter(
                    str(p_path),
                    str(Path(tmp) / "missing.json")
                )
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_invalid_json_raises(self):
        tmp = tempfile.mkdtemp()
        try:
            p_path = Path(tmp) / "personality.json"
            u_path = Path(tmp) / "user_profile.json"
            p_path.write_text("not json", encoding="utf-8")
            _write_json(u_path, USER_PROFILE)
            with pytest.raises(ValueError):
                PersonalityAdapter(str(p_path), str(u_path))
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_template_personality_raises_by_default(self):
        tmp = tempfile.mkdtemp()
        try:
            with pytest.raises(ValueError, match="template"):
                _make_adapter(tmp, personality=PERSONALITY_TEMPLATE)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_template_user_profile_raises_by_default(self):
        tmp = tempfile.mkdtemp()
        try:
            with pytest.raises(ValueError, match="template"):
                _make_adapter(tmp, user=USER_PROFILE_TEMPLATE)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_allow_templates_bypasses_check(self):
        tmp = tempfile.mkdtemp()
        try:
            adapter = _make_adapter(
                tmp,
                personality=PERSONALITY_TEMPLATE,
                user=USER_PROFILE_TEMPLATE,
                allow_templates=True
            )
            assert adapter is not None
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_repr_contains_alfred(self):
        tmp = tempfile.mkdtemp()
        try:
            adapter = _make_adapter(tmp)
            r = repr(adapter)
            assert "ALFRED" in r
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


# ============================================================
# Class TestValidateRequiredSections
# ============================================================

class TestValidateRequiredSections:
    """Tests validation des sections requises."""

    def test_valid_profile_passes(self):
        tmp = tempfile.mkdtemp()
        try:
            adapter = _make_adapter(tmp)
            adapter.validate_required_sections()  # should not raise
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_missing_assistant_identity_raises(self):
        tmp = tempfile.mkdtemp()
        try:
            bad_personality = {k: v for k, v in PERSONALITY_CORE.items()
                               if k != "assistant_identity"}
            adapter = _make_adapter(tmp, personality=bad_personality, allow_templates=True)
            adapter.personality_core = bad_personality
            with pytest.raises(KeyError, match="assistant_identity"):
                adapter.validate_required_sections()
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_missing_user_profile_section_raises(self):
        tmp = tempfile.mkdtemp()
        try:
            adapter = _make_adapter(tmp)
            adapter.user_profile = {}  # Remove all sections
            with pytest.raises(KeyError, match="user_profile"):
                adapter.validate_required_sections()
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


# ============================================================
# Class TestDetectContextMode
# ============================================================

class TestDetectContextMode:
    """Tests detection du mode contextuel."""

    def setup_method(self):
        self.tmp = tempfile.mkdtemp()
        self.adapter = _make_adapter(self.tmp)

    def teardown_method(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_low_energy_mode(self):
        mode = self.adapter.detect_context_mode("peu importe", energy_level="low")
        assert mode == "low_energy_mode"

    def test_fatigue_energy_mode(self):
        mode = self.adapter.detect_context_mode("ok", energy_level="fatigue")
        assert mode == "low_energy_mode"

    def test_stress_emotion_mode(self):
        mode = self.adapter.detect_context_mode("bonjour", detected_emotion="stress")
        assert mode == "emotional_support_light"

    def test_distress_emotion_mode(self):
        mode = self.adapter.detect_context_mode("bonjour", detected_emotion="distress")
        assert mode == "emotional_support_light"

    def test_technical_keyword_python(self):
        mode = self.adapter.detect_context_mode("comment faire un script python")
        assert mode == "technical_mode"

    def test_technical_keyword_code(self):
        mode = self.adapter.detect_context_mode("j'ai un code qui plante")
        assert mode == "technical_mode"

    def test_strategic_keyword(self):
        mode = self.adapter.detect_context_mode("analyse de la strategie business")
        assert mode == "strategic_mode"

    def test_learning_keyword(self):
        mode = self.adapter.detect_context_mode("explique-moi ce concept")
        assert mode == "learning_mode"

    def test_creative_keyword(self):
        mode = self.adapter.detect_context_mode("idee de design pour le logo")
        assert mode == "creative_mode"

    def test_neutral_fallback(self):
        mode = self.adapter.detect_context_mode("bonjour tout va bien")
        assert mode == "neutral_assistant"

    def test_support_keyword_in_message(self):
        # "j'ai du mal" is in support_keywords (no accent)
        mode = self.adapter.detect_context_mode("j'ai du mal a avancer")
        assert mode == "emotional_support_light"


# ============================================================
# Class TestDetermineEmotionalLevel
# ============================================================

class TestDetermineEmotionalLevel:
    """Tests determination du niveau emotionnel."""

    def setup_method(self):
        self.tmp = tempfile.mkdtemp()
        self.adapter = _make_adapter(self.tmp)

    def teardown_method(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_neutral_returns_0(self):
        level = self.adapter.determine_emotional_level("neutral")
        assert level == 0

    def test_none_returns_0(self):
        level = self.adapter.determine_emotional_level(None)
        assert level == 0

    def test_mild_concern_returns_1(self):
        level = self.adapter.determine_emotional_level("mild_concern")
        assert level == 1

    def test_stress_returns_2(self):
        level = self.adapter.determine_emotional_level("stress")
        assert level == 2

    def test_anxiety_returns_2(self):
        level = self.adapter.determine_emotional_level("anxiety")
        assert level == 2

    def test_low_energy_returns_2(self):
        level = self.adapter.determine_emotional_level(energy_level="low")
        assert level == 2

    def test_sadness_returns_2(self):
        # sadness = niveau 2 (modéré) — distress/fear = 3 (sévère)
        level = self.adapter.determine_emotional_level("sadness")
        assert level == 2

    def test_distress_returns_3(self):
        level = self.adapter.determine_emotional_level("distress")
        assert level == 3

    def test_fear_returns_3(self):
        level = self.adapter.determine_emotional_level("fear")
        assert level == 3


# ============================================================
# Class TestDetermineTone
# ============================================================

class TestDetermineTone:
    """Tests determination du ton."""

    def setup_method(self):
        self.tmp = tempfile.mkdtemp()
        self.adapter = _make_adapter(self.tmp)

    def teardown_method(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_low_energy_mode_uses_user_pref(self):
        tone = self.adapter.determine_tone("low_energy_mode", 0)
        assert tone == "doux et rassurant"  # from user preferences

    def test_technical_mode_uses_strategic_pref(self):
        # user has tone_when_strategic pref
        tone = self.adapter.determine_tone("strategic_mode", 0)
        assert tone == "expert et direct"

    def test_learning_mode_uses_learning_pref(self):
        tone = self.adapter.determine_tone("learning_mode", 0)
        assert tone == "pedagogique"

    def test_neutral_mode_uses_user_tone_pref(self):
        # user has generic "tone" preference
        tone = self.adapter.determine_tone("neutral_assistant", 0)
        assert tone == "direct et empathique"

    def test_high_emotional_level_empathique(self):
        # adapter with no user preferences
        tmp2 = tempfile.mkdtemp()
        try:
            minimal_user = {
                "user_profile": {"user_id": "x"},
                "metadata": {"is_template": False}
            }
            adapter2 = _make_adapter(tmp2, user=minimal_user)
            tone = adapter2.determine_tone("unknown_mode", emotional_level=2)
            assert "empathique" in tone or "calme" in tone or "soutenant" in tone
        finally:
            shutil.rmtree(tmp2, ignore_errors=True)

    def test_default_tone_from_personality(self):
        tmp2 = tempfile.mkdtemp()
        try:
            minimal_user = {
                "user_profile": {"user_id": "x"},
                "metadata": {"is_template": False}
            }
            adapter2 = _make_adapter(tmp2, user=minimal_user)
            tone = adapter2.determine_tone("neutral_assistant", emotional_level=0)
            assert "clair" in tone or "direct" in tone or "structure" in tone
        finally:
            shutil.rmtree(tmp2, ignore_errors=True)


# ============================================================
# Class TestDetermineResponseDepth
# ============================================================

class TestDetermineResponseDepth:
    """Tests profondeur de reponse."""

    def setup_method(self):
        self.tmp = tempfile.mkdtemp()

    def teardown_method(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_user_pref_overrides(self):
        # user has response_length = medium
        adapter = _make_adapter(self.tmp)
        depth = adapter.determine_response_depth("technical_mode")
        assert depth == "medium"  # user pref wins

    def test_no_pref_technical_mode_detailed(self):
        minimal_user = {
            "user_profile": {"user_id": "x"},
            "metadata": {"is_template": False}
        }
        adapter = _make_adapter(self.tmp, user=minimal_user)
        depth = adapter.determine_response_depth("technical_mode")
        assert depth == "detailed"

    def test_no_pref_low_energy_mode_short(self):
        minimal_user = {
            "user_profile": {"user_id": "x"},
            "metadata": {"is_template": False}
        }
        adapter = _make_adapter(self.tmp, user=minimal_user)
        depth = adapter.determine_response_depth("low_energy_mode")
        assert depth == "short"

    def test_no_pref_neutral_mode_medium(self):
        minimal_user = {
            "user_profile": {"user_id": "x"},
            "metadata": {"is_template": False}
        }
        adapter = _make_adapter(self.tmp, user=minimal_user)
        depth = adapter.determine_response_depth("neutral_assistant")
        assert depth == "medium"


# ============================================================
# Class TestBuildResponseRules
# ============================================================

class TestBuildResponseRules:
    """Tests construction des regles de reponse."""

    def setup_method(self):
        self.tmp = tempfile.mkdtemp()
        self.adapter = _make_adapter(self.tmp)

    def teardown_method(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_rules_is_dict(self):
        rules = self.adapter.build_response_rules("neutral_assistant", 0)
        assert isinstance(rules, dict)

    def test_base_rules_present(self):
        rules = self.adapter.build_response_rules("neutral_assistant", 0)
        assert rules["be_clear"] is True
        assert rules["respect_privacy"] is True
        assert rules["do_not_diagnose"] is True

    def test_technical_mode_step_by_step(self):
        rules = self.adapter.build_response_rules("technical_mode", 0)
        assert rules["use_step_by_step"] is True
        assert rules["use_examples"] is True

    def test_low_energy_avoid_overload(self):
        rules = self.adapter.build_response_rules("low_energy_mode", 2)
        assert rules["avoid_overload"] is True
        assert rules["use_humor"] is False

    def test_emotional_level_2_use_empathy(self):
        rules = self.adapter.build_response_rules("neutral_assistant", 2)
        assert rules["use_empathy"] is True

    def test_emotional_level_0_no_empathy(self):
        rules = self.adapter.build_response_rules("neutral_assistant", 0)
        assert rules["use_empathy"] is False

    def test_creative_mode_humor(self):
        rules = self.adapter.build_response_rules("creative_mode", 0)
        assert rules["use_humor"] is True


# ============================================================
# Class TestBuildResponseContext
# ============================================================

class TestBuildResponseContext:
    """Tests construction du contexte complet."""

    def setup_method(self):
        self.tmp = tempfile.mkdtemp()
        self.adapter = _make_adapter(self.tmp)

    def teardown_method(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_returns_dict(self):
        ctx = self.adapter.build_response_context("bonjour")
        assert isinstance(ctx, dict)

    def test_assistant_section_present(self):
        ctx = self.adapter.build_response_context("bonjour")
        assert "assistant" in ctx
        assert ctx["assistant"]["name"] == "ALFRED"

    def test_personality_section_present(self):
        ctx = self.adapter.build_response_context("bonjour")
        assert "personality" in ctx
        assert ctx["personality"]["archetype"] == "assistant_protecteur"

    def test_user_section_present(self):
        ctx = self.adapter.build_response_context("bonjour")
        assert "user" in ctx
        assert ctx["user"]["preferred_name"] == "Celine"

    def test_adaptation_section_present(self):
        ctx = self.adapter.build_response_context("bonjour", detected_emotion="stress")
        assert "adaptation" in ctx
        assert ctx["adaptation"]["detected_emotion"] == "stress"

    def test_response_rules_section_present(self):
        ctx = self.adapter.build_response_context("bonjour")
        assert "response_rules" in ctx

    def test_technical_message_triggers_technical_mode(self):
        ctx = self.adapter.build_response_context("debug mon script python")
        assert ctx["adaptation"]["mode"] == "technical_mode"

    def test_distress_triggers_support_mode(self):
        ctx = self.adapter.build_response_context(
            "je suis epuisee",
            detected_emotion="distress"
        )
        assert ctx["adaptation"]["mode"] in {"emotional_support_light", "low_energy_mode"}

    def test_emotional_level_in_adaptation(self):
        ctx = self.adapter.build_response_context(
            "tout va bien",
            detected_emotion="sadness"
        )
        assert ctx["adaptation"]["emotional_level"] == 2  # sadness = niveau 2

    def test_boundaries_section_from_personality(self):
        ctx = self.adapter.build_response_context("bonjour")
        assert "boundaries" in ctx


# ============================================================
# Class TestStaticMethods
# ============================================================

class TestStaticMethods:
    """Tests methodes statiques (creation depuis template)."""

    def test_create_user_profile_from_template(self):
        tmp = tempfile.mkdtemp()
        try:
            template_data = {
                "user_profile": {
                    "user_id": "TEMPLATE",
                    "preferred_name": "utilisateur",
                    "language_preference": "fr",
                    "profile_status": "template",
                    "created_at": "",
                    "updated_at": ""
                },
                "preferences": {
                    "preferred_language": "fr"
                },
                "metadata": {
                    "is_template": True,
                    "environment": "public_template"
                }
            }
            template_path = Path(tmp) / "template_user.json"
            _write_json(template_path, template_data)
            output_dir = Path(tmp) / "output"

            result_path = PersonalityAdapter.create_user_profile_from_template(
                str(template_path),
                str(output_dir),
                preferred_language="fr"
            )

            assert result_path.exists()
            data = json.loads(result_path.read_text(encoding="utf-8"))
            assert data["metadata"]["is_template"] is False
            assert data["user_profile"]["profile_status"] == "created"
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_create_personality_from_template(self):
        tmp = tempfile.mkdtemp()
        try:
            template_data = {
                "assistant_identity": {"name": "ALFRED", "version": "TEMPLATE"},
                "metadata": {"is_template": True, "environment": "public"}
            }
            template_path = Path(tmp) / "template_personality.json"
            _write_json(template_path, template_data)
            output_path = Path(tmp) / "personality_real.json"

            result_path = PersonalityAdapter.create_personality_from_template(
                str(template_path),
                str(output_path),
                version_name="v1_test"
            )

            assert result_path.exists()
            data = json.loads(result_path.read_text(encoding="utf-8"))
            assert data["metadata"]["is_template"] is False
            assert data["assistant_identity"]["version"] == "v1_test"
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_create_user_profile_missing_template_raises(self):
        with pytest.raises(FileNotFoundError):
            PersonalityAdapter.create_user_profile_from_template(
                "/nonexistent/template.json",
                "/tmp/output"
            )
