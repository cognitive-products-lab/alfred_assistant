"""
PROJECT      : ALFRED  |  BLOCK : B22  |  FUNCTION : 22.11
FILE         : tests/b15_tests/test_voice_output_manager.py
AUTHOR       : Cognitive Products Lab  |  CREATED : 2026-06-01  |  STATUS : ACTIVE
"""
import pytest
from src.accessibility.audio.voice_output_manager import (
    VoiceOutputManager, VoicePreset, PRESETS,
)


class TestVoicePreset:
    def test_preset_has_required_fields(self):
        p = VoicePreset("test", rate=1.0, volume=0.8, pitch=0.0, pause_factor=1.0)
        assert p.name == "test"
        assert 0.5 <= p.rate <= 2.0
        assert 0.0 <= p.volume <= 1.0


class TestPresets:
    def test_presets_not_empty(self):
        assert len(PRESETS) >= 4

    def test_required_presets_exist(self):
        for p in ("neutral", "calm", "clear", "informative"):
            assert p in PRESETS

    def test_calm_slower_than_informative(self):
        assert PRESETS["calm"].rate < PRESETS["informative"].rate

    def test_bedtime_lowest_volume(self):
        volumes = [p.volume for p in PRESETS.values()]
        assert PRESETS["bedtime"].volume <= min(volumes) + 0.1


class TestVoiceOutputManager:

    def test_init_headless(self):
        v = VoiceOutputManager()
        assert v._tts is None
        assert v.active_preset.name == "neutral"

    def test_set_preset_changes_active(self):
        v = VoiceOutputManager()
        v.set_preset("calm")
        assert v.active_preset.name == "calm"

    def test_set_invalid_preset_raises(self):
        v = VoiceOutputManager()
        with pytest.raises(ValueError):
            v.set_preset("not_a_preset")

    def test_adapt_to_emotion_stressed(self):
        v = VoiceOutputManager()
        preset = v.adapt_to_emotion("stressed")
        assert preset.name == "calm"

    def test_adapt_to_emotion_tired(self):
        v = VoiceOutputManager()
        preset = v.adapt_to_emotion("tired")
        assert preset.name == "clear"

    def test_adapt_to_unknown_emotion_gives_neutral(self):
        v = VoiceOutputManager()
        preset = v.adapt_to_emotion("UNKNOWN_XYZ")
        assert preset.name == "neutral"

    def test_set_custom_applies_override(self):
        v = VoiceOutputManager()
        v.set_custom(rate=1.5, volume=0.9)
        assert v.active_preset.rate == 1.5
        assert v.active_preset.volume == 0.9

    def test_reset_clears_override(self):
        v = VoiceOutputManager()
        v.set_custom(rate=1.5, volume=0.9)
        v.reset()
        assert v._override is None
        assert v.active_preset.name == "neutral"

    def test_list_presets_returns_list(self):
        v = VoiceOutputManager()
        presets = v.list_presets()
        assert isinstance(presets, list)
        assert len(presets) == len(PRESETS)

    def test_list_presets_has_required_keys(self):
        v = VoiceOutputManager()
        for p in v.list_presets():
            assert "name" in p and "rate" in p and "volume" in p

    def test_status_returns_dict(self):
        v = VoiceOutputManager()
        s = v.status()
        assert "active_preset" in s
        assert "rate" in s
        assert "tts_connected" in s

    def test_stats_count_changes(self):
        v = VoiceOutputManager()
        v.set_preset("calm")
        v.set_preset("clear")
        assert v._stats["preset_changes"] == 2

    def test_adapt_to_profile(self):
        v = VoiceOutputManager()
        v.adapt_to_profile(rate=0.8, volume=0.7)
        assert v.active_preset.rate == 0.8
        assert v.active_preset.volume == 0.7

    def test_apply_to_tts_with_mock(self):
        applied = []
        class MockTTS:
            def set_rate(self, r): applied.append(("rate", r))
            def set_volume(self, v): applied.append(("volume", v))
        v = VoiceOutputManager(tts_engine=MockTTS())
        v.set_preset("calm")
        assert any(a[0] == "rate" for a in applied)
