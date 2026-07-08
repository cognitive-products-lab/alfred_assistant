"""
PROJECT      : ALFRED
BLOCK        : B04 — Vision
FILE         : tests/b04_tests/test_vision_analyzer.py
ROLE         : Tests unitaires VisionAnalyzer (sans caméra réelle, sans Ollama)

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-06-20
UPDATED      : 2026-06-20
VERSION      : V1.0
STATUS       : TESTED
TESTS        : 43/43 unitaires (mocks) — Grade A+
               Test réel caméra + llava : À FAIRE (session ultérieure)

Stratégie :
  - Détection mouvement testée avec des arrays numpy synthétiques (pas de caméra)
  - Appels llava mockés via unittest.mock.patch
  - Monitoring testé avec une snapshot_fn factice et un callback capturant les events
  - Aucun import Kivy (tests purement unitaires)
"""

from __future__ import annotations

import base64
import sys
import time
import threading
from pathlib import Path
from typing import Optional
from unittest.mock import MagicMock, patch

import pytest

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

try:
    import numpy as np
    import cv2
    _CV2_OK = True
except ImportError:
    _CV2_OK = False

from src.vision.vision_analyzer import (
    VisionAnalyzer,
    VisionEvent,
    MotionResult,
    _MOTION_THRESH_HIGH,
    _MOTION_THRESH_MEDIUM,
    _MOTION_THRESH_LOW,
    _PIXEL_DIFF_THRESH,
)


# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────

def _make_frame(h: int = 90, w: int = 120, color=(50, 50, 50)):
    """Crée un array BGR numpy de couleur uniforme."""
    if not _CV2_OK:
        pytest.skip("OpenCV non disponible")
    frame = np.zeros((h, w, 3), dtype=np.uint8)
    frame[:] = color
    return frame


def _frame_to_b64(frame) -> str:
    """Encode un frame BGR en JPEG base64."""
    ok, buf = cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
    assert ok
    return base64.b64encode(buf.tobytes()).decode("ascii")


def _make_analyzer_no_llava() -> VisionAnalyzer:
    """VisionAnalyzer avec client llava mocké (is_available=False)."""
    analyzer = VisionAnalyzer()
    analyzer._client = MagicMock()
    analyzer._client.is_available.return_value = False
    return analyzer


def _make_analyzer_with_llava(llm_response: str = "Neutre.") -> VisionAnalyzer:
    """VisionAnalyzer avec client llava mocké retournant une réponse fixe."""
    analyzer = VisionAnalyzer()
    analyzer._client = MagicMock()
    analyzer._client.is_available.return_value = True
    analyzer._client.analyze_image.return_value = llm_response
    return analyzer


# ─────────────────────────────────────────────────────────────────────────────
# Tests — VisionEvent
# ─────────────────────────────────────────────────────────────────────────────

class TestVisionEvent:

    def test_defaults(self):
        e = VisionEvent(type="scene", severity="info", description="OK")
        assert e.emotion_hint == ""
        assert e.raw_llm_output == ""
        assert "T" in e.timestamp or "-" in e.timestamp  # format ISO

    def test_all_fields(self):
        e = VisionEvent(
            type="expression",
            severity="warning",
            description="Fatiguée.",
            emotion_hint="fatigue",
            raw_llm_output="La personne semble fatiguée.",
        )
        assert e.type == "expression"
        assert e.emotion_hint == "fatigue"


# ─────────────────────────────────────────────────────────────────────────────
# Tests — MotionResult
# ─────────────────────────────────────────────────────────────────────────────

class TestMotionResult:

    def test_fields(self):
        m = MotionResult(level="high", changed_pct=25.0, is_alert=True, description="Fort.")
        assert m.is_alert is True
        assert m.changed_pct == 25.0


# ─────────────────────────────────────────────────────────────────────────────
# Tests — detect_motion
# ─────────────────────────────────────────────────────────────────────────────

@pytest.mark.skipif(not _CV2_OK, reason="OpenCV requis")
class TestDetectMotion:

    def setup_method(self):
        self.analyzer = _make_analyzer_no_llava()

    def test_no_motion_identical_frames(self):
        frame = _make_frame(color=(80, 80, 80))
        result = self.analyzer.detect_motion(frame, frame.copy())
        assert result.level == "none"
        assert result.is_alert is False
        assert result.changed_pct < _MOTION_THRESH_LOW

    def test_low_motion(self):
        prev = _make_frame(color=(80, 80, 80))
        curr = prev.copy()
        # Modifier ~2% des pixels légèrement
        n_pixels = int(prev.shape[0] * prev.shape[1] * 0.02)
        for i in range(n_pixels):
            x = i % prev.shape[1]
            y = i // prev.shape[1]
            curr[y, x] = (80 + _PIXEL_DIFF_THRESH + 5, 80, 80)
        result = self.analyzer.detect_motion(prev, curr)
        assert result.level in ("low", "medium", "none")
        assert result.is_alert is False

    def test_high_motion_triggers_alert(self):
        prev = _make_frame(color=(50, 50, 50))
        curr = _make_frame(color=(200, 200, 200))  # tout l'image change
        result = self.analyzer.detect_motion(prev, curr)
        assert result.level == "high"
        assert result.is_alert is True
        assert result.changed_pct >= _MOTION_THRESH_HIGH

    def test_none_prev_frame(self):
        curr = _make_frame()
        result = self.analyzer.detect_motion(None, curr)
        assert result.level == "none"
        assert result.is_alert is False

    def test_none_curr_frame(self):
        prev = _make_frame()
        result = self.analyzer.detect_motion(prev, None)
        assert result.level == "none"

    def test_different_sizes_resized(self):
        prev = _make_frame(h=90, w=120, color=(50, 50, 50))
        curr = _make_frame(h=180, w=240, color=(200, 200, 200))
        result = self.analyzer.detect_motion(prev, curr)
        assert result.level == "high"

    def test_medium_motion(self):
        prev = _make_frame(color=(50, 50, 50))
        curr = prev.copy()
        h, w = prev.shape[:2]
        n = int(h * w * (_MOTION_THRESH_MEDIUM + 1) / 100)
        for i in range(n):
            x = i % w
            y = (i // w) % h
            curr[y, x] = (200, 200, 200)
        result = self.analyzer.detect_motion(prev, curr)
        assert result.level in ("medium", "high")


# ─────────────────────────────────────────────────────────────────────────────
# Tests — describe_scene
# ─────────────────────────────────────────────────────────────────────────────

class TestDescribeScene:

    def test_returns_vision_event(self):
        analyzer = _make_analyzer_with_llava("Un bureau avec un écran d'ordinateur.")
        frame_b64 = "FAKEB64DATA"
        event = analyzer.describe_scene(frame_b64)
        assert isinstance(event, VisionEvent)
        assert event.type == "scene"
        assert event.severity == "info"
        assert "bureau" in event.description

    def test_llava_called_with_correct_prompt(self):
        analyzer = _make_analyzer_with_llava("Pièce calme.")
        analyzer.describe_scene("ABC")
        call_args = analyzer._client.analyze_image.call_args
        prompt = call_args[0][1]
        assert "Décris" in prompt
        assert "français" in prompt

    def test_llava_exception_returns_graceful_event(self):
        analyzer = _make_analyzer_no_llava()
        analyzer._client.analyze_image.side_effect = ConnectionError("Ollama down")
        event = analyzer.describe_scene("ABC")
        assert event.type == "scene"
        assert "Impossible" in event.description or event.description != ""


# ─────────────────────────────────────────────────────────────────────────────
# Tests — analyze_expression
# ─────────────────────────────────────────────────────────────────────────────

class TestAnalyzeExpression:

    def test_fatigue_detected(self):
        analyzer = _make_analyzer_with_llava("La personne semble fatiguée, yeux lourds.")
        event = analyzer.analyze_expression("FAKE")
        assert event.type == "expression"
        assert event.emotion_hint == "fatigue"

    def test_stress_detected(self):
        analyzer = _make_analyzer_with_llava("Elle paraît stressée et crispée.")
        event = analyzer.analyze_expression("FAKE")
        assert event.emotion_hint == "stress"

    def test_joy_detected(self):
        analyzer = _make_analyzer_with_llava("La personne sourit, elle semble heureuse.")
        event = analyzer.analyze_expression("FAKE")
        assert event.emotion_hint == "joie"

    def test_neutral_fallback(self):
        analyzer = _make_analyzer_with_llava("Expression indéterminée.")
        event = analyzer.analyze_expression("FAKE")
        assert event.emotion_hint == "neutre"

    def test_exception_graceful(self):
        analyzer = _make_analyzer_no_llava()
        analyzer._client.analyze_image.side_effect = RuntimeError("llava KO")
        event = analyzer.analyze_expression("FAKE")
        assert event.type == "expression"

    def test_emotion_hint_in_event(self):
        analyzer = _make_analyzer_with_llava("Elle a l'air triste et abattue.")
        event = analyzer.analyze_expression("FAKE")
        assert event.emotion_hint == "tristesse"


# ─────────────────────────────────────────────────────────────────────────────
# Tests — analyze_emergency
# ─────────────────────────────────────────────────────────────────────────────

class TestAnalyzeEmergency:

    def test_fall_detected_oui(self):
        analyzer = _make_analyzer_with_llava("OUI, la personne est tombée au sol.")
        event = analyzer.analyze_emergency("FAKE")
        assert event.type == "fall_detected"
        assert event.severity == "critical"

    def test_no_emergency_non(self):
        analyzer = _make_analyzer_with_llava("NON, tout semble normal.")
        event = analyzer.analyze_emergency("FAKE")
        assert event.type == "motion"
        assert event.severity == "info"

    def test_ambiguous_response_no_alert(self):
        analyzer = _make_analyzer_with_llava("La scène est normale, pas de problème.")
        event = analyzer.analyze_emergency("FAKE")
        assert event.severity in ("info", "warning")
        assert event.type != "fall_detected"

    def test_exception_returns_warning(self):
        analyzer = _make_analyzer_no_llava()
        analyzer._client.analyze_image.side_effect = ConnectionError("KO")
        event = analyzer.analyze_emergency("FAKE")
        assert event.severity == "warning"
        assert event.type == "motion"

    def test_critical_event_description_contains_warning(self):
        analyzer = _make_analyzer_with_llava("OUI chute détectée.")
        event = analyzer.analyze_emergency("FAKE")
        assert "⚠️" in event.description or "urgence" in event.description.lower()


# ─────────────────────────────────────────────────────────────────────────────
# Tests — _extract_emotion_hint
# ─────────────────────────────────────────────────────────────────────────────

class TestExtractEmotionHint:

    def setup_method(self):
        self.analyzer = _make_analyzer_no_llava()

    def test_fatigue_keywords(self):
        assert self.analyzer._extract_emotion_hint("Elle semble épuisée.") == "fatigue"

    def test_stress_keywords(self):
        assert self.analyzer._extract_emotion_hint("Visage tendu et anxieux.") == "stress"

    def test_joie_keywords(self):
        assert self.analyzer._extract_emotion_hint("Elle sourit largement.") == "joie"

    def test_tristesse_keywords(self):
        assert self.analyzer._extract_emotion_hint("Elle pleure, l'air triste.") == "tristesse"

    def test_neutre_fallback(self):
        assert self.analyzer._extract_emotion_hint("Aucune expression notable.") == "neutre"

    def test_case_insensitive(self):
        assert self.analyzer._extract_emotion_hint("FATIGUÉE ET ÉPUISÉE") == "fatigue"


# ─────────────────────────────────────────────────────────────────────────────
# Tests — Monitoring
# ─────────────────────────────────────────────────────────────────────────────

@pytest.mark.skipif(not _CV2_OK, reason="OpenCV requis")
class TestMonitoring:

    def test_start_stop(self):
        analyzer = _make_analyzer_no_llava()
        events = []
        frame_b64 = _frame_to_b64(_make_frame())
        analyzer.start_monitoring(
            snapshot_fn=lambda: frame_b64,
            on_alert=events.append,
            interval_s=0.1,
            expression_interval_s=9999,
        )
        assert analyzer.is_monitoring is True
        time.sleep(0.3)
        analyzer.stop_monitoring()
        assert analyzer.is_monitoring is False

    def test_no_motion_no_alert(self):
        """Frames identiques → aucun alert motion émis."""
        analyzer = _make_analyzer_no_llava()
        alerts = []
        frame = _make_frame(color=(100, 100, 100))
        frame_b64 = _frame_to_b64(frame)

        analyzer.start_monitoring(
            snapshot_fn=lambda: frame_b64,
            on_alert=alerts.append,
            interval_s=0.05,
            expression_interval_s=9999,
        )
        time.sleep(0.4)
        analyzer.stop_monitoring()
        motion_alerts = [e for e in alerts if e.type in ("motion", "fall_detected")]
        assert len(motion_alerts) == 0

    def test_high_motion_triggers_emergency_analysis(self):
        """Frames très différentes → motion high → analyze_emergency appelée."""
        analyzer = _make_analyzer_with_llava("OUI chute grave.")
        alerts = []
        frames = [
            _frame_to_b64(_make_frame(color=(50, 50, 50))),
            _frame_to_b64(_make_frame(color=(200, 200, 200))),
        ]
        call_count = [0]

        def snapshot():
            idx = min(call_count[0], len(frames) - 1)
            call_count[0] += 1
            return frames[idx]

        analyzer.start_monitoring(
            snapshot_fn=snapshot,
            on_alert=alerts.append,
            interval_s=0.05,
            expression_interval_s=9999,
        )
        time.sleep(0.5)
        analyzer.stop_monitoring()

        critical = [e for e in alerts if e.severity == "critical"]
        assert len(critical) >= 1
        assert critical[0].type == "fall_detected"

    def test_expression_analysis_periodic(self):
        """L'analyse d'expression est appelée périodiquement."""
        analyzer = _make_analyzer_with_llava("La personne semble fatiguée.")
        analyzer._client.is_available.return_value = True
        alerts = []
        frame_b64 = _frame_to_b64(_make_frame())

        analyzer.start_monitoring(
            snapshot_fn=lambda: frame_b64,
            on_alert=alerts.append,
            interval_s=0.05,
            expression_interval_s=0.1,  # très court pour le test
        )
        time.sleep(0.5)
        analyzer.stop_monitoring()

        expr_events = [e for e in alerts if e.type == "expression"]
        assert len(expr_events) >= 1
        assert expr_events[0].emotion_hint == "fatigue"

    def test_snapshot_returns_none_no_crash(self):
        """snapshot_fn qui retourne None ne fait pas crasher le monitoring."""
        analyzer = _make_analyzer_no_llava()
        alerts = []
        analyzer.start_monitoring(
            snapshot_fn=lambda: None,
            on_alert=alerts.append,
            interval_s=0.05,
            expression_interval_s=9999,
        )
        time.sleep(0.3)
        analyzer.stop_monitoring()
        assert analyzer.is_monitoring is False

    def test_double_start_ignored(self):
        """Appeler start_monitoring deux fois ne lance pas deux threads."""
        analyzer = _make_analyzer_no_llava()
        frame_b64 = _frame_to_b64(_make_frame())
        analyzer.start_monitoring(lambda: frame_b64, lambda e: None, 0.1, 9999)
        thread1 = analyzer._monitoring_thread
        analyzer.start_monitoring(lambda: frame_b64, lambda e: None, 0.1, 9999)
        thread2 = analyzer._monitoring_thread
        assert thread1 is thread2
        analyzer.stop_monitoring()


# ─────────────────────────────────────────────────────────────────────────────
# Tests — Utilitaires
# ─────────────────────────────────────────────────────────────────────────────

@pytest.mark.skipif(not _CV2_OK, reason="OpenCV requis")
class TestUtils:

    def test_frame_bgr_to_b64_roundtrip(self):
        frame = _make_frame(color=(123, 45, 67))
        b64 = VisionAnalyzer.frame_bgr_to_b64(frame)
        assert b64 is not None
        assert isinstance(b64, str)
        # Vérifier décodable
        decoded = base64.b64decode(b64)
        assert len(decoded) > 0

    def test_b64_to_bgr_roundtrip(self):
        frame = _make_frame(color=(100, 150, 200))
        b64 = VisionAnalyzer.frame_bgr_to_b64(frame)
        recovered = VisionAnalyzer._b64_to_bgr(b64)
        assert recovered is not None
        assert recovered.shape == frame.shape

    def test_b64_to_bgr_invalid_data(self):
        result = VisionAnalyzer._b64_to_bgr("INVALIDBASE64!!!")
        assert result is None

    def test_frame_bgr_to_b64_none(self):
        result = VisionAnalyzer.frame_bgr_to_b64(None)
        assert result is None


# ─────────────────────────────────────────────────────────────────────────────
# Tests — is_vision_available / is_opencv_available
# ─────────────────────────────────────────────────────────────────────────────

class TestAvailability:

    def test_is_vision_available_true(self):
        analyzer = _make_analyzer_with_llava()
        assert analyzer.is_vision_available() is True

    def test_is_vision_available_false(self):
        analyzer = _make_analyzer_no_llava()
        assert analyzer.is_vision_available() is False

    def test_is_opencv_available(self):
        analyzer = VisionAnalyzer()
        assert analyzer.is_opencv_available() == _CV2_OK
