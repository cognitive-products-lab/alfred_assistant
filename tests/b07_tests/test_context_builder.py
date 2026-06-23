"""
════════════════════════════════════════════════════════════
PROJECT      : ALFRED
BLOCK        : B07 — Mobilité & Contexte externe
FUNCTION     : B07.TEST
FILE         : tests/b07_tests/test_context_builder.py
ROLE         : Tests unitaires — context_builder.py

AUTHOR       : Cognitive Products Lab — Céline Darras
CREATED      : 2026-06-20
UPDATED      : 2026-06-20
VERSION      : V1.0
STATUS       : ACTIVE

DESCRIPTION :
Teste toutes les fonctions de src/conversation/input/context_builder.py :
  - get_time_context()      : structure, périodes, énergie, weekend
  - get_device_context()    : structure, device_id
  - get_conversation_context() : stades (opening/early/active/deep)
  - build_context()         : fusion, champs de surface
  - format_context_for_prompt() : rendu texte
════════════════════════════════════════════════════════════
"""

import sys
from datetime import datetime
from pathlib import Path
from unittest.mock import patch

import pytest

_ROOT = Path(__file__).resolve().parents[2]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from src.conversation.input.context_builder import (
    build_context,
    format_context_for_prompt,
    get_conversation_context,
    get_device_context,
    get_time_context,
)


# ─── get_time_context ────────────────────────────────────────────────────────

class TestGetTimeContext:
    def test_returns_dict_with_required_keys(self):
        ctx = get_time_context()
        for key in ("datetime", "time", "date", "day_of_week", "period",
                    "greeting", "energy_level", "is_weekend", "hour"):
            assert key in ctx, f"Clé manquante : {key}"

    def test_hour_in_range(self):
        ctx = get_time_context()
        assert 0 <= ctx["hour"] <= 23

    def test_is_weekend_bool(self):
        ctx = get_time_context()
        assert isinstance(ctx["is_weekend"], bool)

    @pytest.mark.parametrize("hour,expected_period", [
        (6, "matin"),
        (11, "matin"),
        (12, "midi"),
        (13, "midi"),
        (15, "après-midi"),
        (17, "après-midi"),
        (19, "soirée"),
        (21, "soirée"),
        (23, "nuit"),
        (2, "nuit"),
    ])
    def test_period_by_hour(self, hour, expected_period):
        fake_now = datetime(2026, 6, 20, hour, 0, 0)  # vendredi
        with patch("src.conversation.input.context_builder.datetime") as mock_dt:
            mock_dt.now.return_value = fake_now
            ctx = get_time_context()
        assert ctx["period"] == expected_period

    @pytest.mark.parametrize("hour,expected_greeting", [
        (8, "Bonjour"),
        (12, "Bon après-midi"),
        (19, "Bonsoir"),
        (23, "Bonsoir"),
    ])
    def test_greeting_by_hour(self, hour, expected_greeting):
        fake_now = datetime(2026, 6, 20, hour, 0, 0)
        with patch("src.conversation.input.context_builder.datetime") as mock_dt:
            mock_dt.now.return_value = fake_now
            ctx = get_time_context()
        assert ctx["greeting"] == expected_greeting

    @pytest.mark.parametrize("hour,expected_energy", [
        (9, "high"),
        (16, "high"),
        (13, "medium"),
        (19, "medium"),
        (3, "low"),
        (22, "low"),
    ])
    def test_energy_level_by_hour(self, hour, expected_energy):
        fake_now = datetime(2026, 6, 20, hour, 0, 0)
        with patch("src.conversation.input.context_builder.datetime") as mock_dt:
            mock_dt.now.return_value = fake_now
            ctx = get_time_context()
        assert ctx["energy_level"] == expected_energy

    def test_is_weekend_saturday(self):
        fake_now = datetime(2026, 6, 20, 10, 0, 0)  # samedi
        with patch("src.conversation.input.context_builder.datetime") as mock_dt:
            mock_dt.now.return_value = fake_now
            ctx = get_time_context()
        assert ctx["is_weekend"] is True

    def test_is_weekend_monday(self):
        fake_now = datetime(2026, 6, 22, 10, 0, 0)  # lundi
        with patch("src.conversation.input.context_builder.datetime") as mock_dt:
            mock_dt.now.return_value = fake_now
            ctx = get_time_context()
        assert ctx["is_weekend"] is False

    def test_date_contains_day_name(self):
        fake_now = datetime(2026, 6, 22, 10, 0, 0)  # lundi
        with patch("src.conversation.input.context_builder.datetime") as mock_dt:
            mock_dt.now.return_value = fake_now
            ctx = get_time_context()
        assert "lundi" in ctx["date"]
        assert "juin" in ctx["date"]
        assert "2026" in ctx["date"]

    def test_time_format_hhmm(self):
        ctx = get_time_context()
        parts = ctx["time"].split(":")
        assert len(parts) == 2
        assert parts[0].isdigit() and parts[1].isdigit()


# ─── get_device_context ──────────────────────────────────────────────────────

class TestGetDeviceContext:
    def test_returns_dict_with_required_keys(self):
        ctx = get_device_context()
        for key in ("device_id", "device_type", "os", "os_version", "hostname", "interface"):
            assert key in ctx, f"Clé manquante : {key}"

    def test_default_device_id(self):
        ctx = get_device_context()
        assert ctx["device_id"] == "local_pc"

    def test_custom_device_id(self):
        ctx = get_device_context("alfred_minisforum")
        assert ctx["device_id"] == "alfred_minisforum"

    def test_device_type_desktop(self):
        ctx = get_device_context()
        assert ctx["device_type"] == "desktop"

    def test_os_version_truncated(self):
        ctx = get_device_context()
        assert len(ctx["os_version"]) <= 40

    def test_interface_value(self):
        ctx = get_device_context()
        assert ctx["interface"] == "terminal_v1"

    def test_os_non_empty(self):
        ctx = get_device_context()
        assert ctx["os"]

    def test_hostname_non_empty(self):
        ctx = get_device_context()
        assert ctx["hostname"]


# ─── get_conversation_context ────────────────────────────────────────────────

class TestGetConversationContext:
    def test_empty_history_opening_stage(self):
        ctx = get_conversation_context([])
        assert ctx["conversation_stage"] == "opening"
        assert ctx["is_first_message"] is True
        assert ctx["exchange_count"] == 0
        assert ctx["last_user_message"] is None
        assert ctx["last_intent"] is None

    def test_early_stage_1_to_3(self):
        history = [{"user": "Salut", "intent": "greeting"}]
        ctx = get_conversation_context(history)
        assert ctx["conversation_stage"] == "early"
        assert ctx["is_first_message"] is False
        assert ctx["exchange_count"] == 1

    def test_early_stage_boundary(self):
        history = [{"user": f"msg {i}"} for i in range(3)]
        ctx = get_conversation_context(history)
        assert ctx["conversation_stage"] == "early"

    def test_active_stage_4_to_10(self):
        history = [{"user": f"msg {i}"} for i in range(5)]
        ctx = get_conversation_context(history)
        assert ctx["conversation_stage"] == "active"

    def test_deep_stage_over_10(self):
        history = [{"user": f"msg {i}"} for i in range(11)]
        ctx = get_conversation_context(history)
        assert ctx["conversation_stage"] == "deep"

    def test_last_user_message_extracted(self):
        history = [
            {"user": "Premier message"},
            {"user": "Dernier message", "intent": "question"},
        ]
        ctx = get_conversation_context(history)
        assert ctx["last_user_message"] == "Dernier message"
        assert ctx["last_intent"] == "question"

    def test_last_intent_none_if_missing(self):
        history = [{"user": "Bonjour"}]
        ctx = get_conversation_context(history)
        assert ctx["last_intent"] is None

    def test_exchange_count_correct(self):
        history = [{"user": f"msg {i}"} for i in range(7)]
        ctx = get_conversation_context(history)
        assert ctx["exchange_count"] == 7


# ─── build_context ───────────────────────────────────────────────────────────

class TestBuildContext:
    def test_returns_dict_with_top_level_keys(self):
        ctx = build_context([])
        for key in ("user_name", "time", "device", "conversation",
                    "greeting", "period", "energy_level", "is_first"):
            assert key in ctx, f"Clé manquante : {key}"

    def test_default_user_name(self):
        ctx = build_context([])
        assert ctx["user_name"] == "Céline"

    def test_custom_user_name(self):
        ctx = build_context([], user_name="Isabelle")
        assert ctx["user_name"] == "Isabelle"

    def test_custom_device_id(self):
        ctx = build_context([], device_id="alfred_minisforum")
        assert ctx["device"]["device_id"] == "alfred_minisforum"

    def test_is_first_true_on_empty_history(self):
        ctx = build_context([])
        assert ctx["is_first"] is True

    def test_is_first_false_with_history(self):
        ctx = build_context([{"user": "Bonjour"}])
        assert ctx["is_first"] is False

    def test_surface_fields_match_nested(self):
        ctx = build_context([])
        assert ctx["greeting"] == ctx["time"]["greeting"]
        assert ctx["period"] == ctx["time"]["period"]
        assert ctx["energy_level"] == ctx["time"]["energy_level"]

    def test_time_sub_dict_present(self):
        ctx = build_context([])
        assert isinstance(ctx["time"], dict)
        assert "period" in ctx["time"]

    def test_conversation_sub_dict_present(self):
        ctx = build_context([])
        assert isinstance(ctx["conversation"], dict)
        assert "conversation_stage" in ctx["conversation"]


# ─── format_context_for_prompt ───────────────────────────────────────────────

class TestFormatContextForPrompt:
    def _ctx(self, history=None, user_name="Céline"):
        return build_context(history or [], user_name=user_name)

    def test_returns_string(self):
        result = format_context_for_prompt(self._ctx())
        assert isinstance(result, str)

    def test_contains_context_header(self):
        result = format_context_for_prompt(self._ctx())
        assert "[Contexte session]" in result

    def test_contains_user_name(self):
        result = format_context_for_prompt(self._ctx(user_name="Isabelle"))
        assert "Isabelle" in result

    def test_contains_exchange_count(self):
        result = format_context_for_prompt(self._ctx(history=[{"user": "Salut"}]))
        assert "1" in result

    def test_contains_stage(self):
        result = format_context_for_prompt(self._ctx())
        assert "opening" in result

    def test_last_message_truncated_at_80_chars(self):
        long_msg = "A" * 100
        ctx = build_context([{"user": long_msg}])
        result = format_context_for_prompt(ctx)
        # Le message est tronqué à 80 chars + "..."
        assert "A" * 80 in result
        assert "A" * 81 not in result

    def test_no_last_message_line_when_empty_history(self):
        result = format_context_for_prompt(self._ctx())
        assert "Dernier msg" not in result
