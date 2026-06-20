"""
PROJECT      : ALFRED
BLOCK        : B04 — Vision
FUNCTION     : 04.02 — Analyse visuelle temps réel
FILE         : src/vision/vision_analyzer.py
ROLE         : Orchestrateur des 3 capacités vision d'ALFRED :
               description de scène, analyse d'expression, détection mouvement/chute

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-06-20
UPDATED      : 2026-06-20
VERSION      : V1.0
STATUS       : TO_TEST

DESCRIPTION :
Trois capacités indépendantes, utilisables séparément ou combinées :

  1. describe_scene(frame_b64)
       → llava:7b analyse l'arrière-plan et la scène visible
       → utilisé quand l'utilisateur demande "qu'est-ce que tu vois ?"

  2. analyze_expression(frame_b64)
       → llava:7b décrit l'expression faciale et l'état émotionnel apparent
       → le résultat est injecté dans le contexte ALFRED pour adapter le ton

  3. detect_motion(prev_bgr, curr_bgr)
       → OpenCV diff de frames — 100% local, 0 LLM
       → retourne un MotionResult (niveau low/medium/high + pourcentage)

  4. start_monitoring(snapshot_fn, on_alert, interval_s)
       → thread daemon : surveille le flux en continu
       → si mouvement fort → snapshot → llava vérifie si situation d'urgence
       → si urgence détectée → callback on_alert(VisionEvent)

Usage rapide :
    analyzer = VisionAnalyzer()
    if analyzer.is_vision_available():
        desc = analyzer.describe_scene(frame_b64)
    analyzer.start_monitoring(snapshot_fn=cam.capture_snapshot_jpeg_b64,
                              on_alert=lambda e: print(e.description))
"""

from __future__ import annotations

import base64
import threading
import time
from dataclasses import dataclass, field
from datetime import datetime
from typing import Callable, Optional

try:
    import numpy as np
    import cv2
    _CV2_OK = True
except ImportError:
    _CV2_OK = False

from src.llm.vision_client_ollama import OllamaVisionClient


# ─────────────────────────────────────────────────────────────────────────────
# Structures de données
# ─────────────────────────────────────────────────────────────────────────────

@dataclass
class MotionResult:
    """Résultat de la détection de mouvement par diff OpenCV."""
    level: str           # "none" | "low" | "medium" | "high"
    changed_pct: float   # % de pixels ayant changé (0.0–100.0)
    is_alert: bool       # True si level == "high"
    description: str     # phrase lisible


@dataclass
class VisionEvent:
    """Événement vision émis par le monitoring ou une analyse manuelle."""
    type: str            # "scene" | "expression" | "motion" | "fall_detected" | "emergency"
    severity: str        # "info" | "warning" | "critical"
    description: str     # texte lisible, prêt à être lu par ALFRED
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat(timespec="seconds"))
    raw_llm_output: str = ""
    emotion_hint: str = ""   # si type==expression : émotion détectée (fatigue, stress…)


# ─────────────────────────────────────────────────────────────────────────────
# Seuils détection mouvement
# ─────────────────────────────────────────────────────────────────────────────

_MOTION_THRESH_LOW    = 1.5    # % pixels modifiés → mouvement faible
_MOTION_THRESH_MEDIUM = 6.0    # % → mouvement moyen
_MOTION_THRESH_HIGH   = 18.0   # % → mouvement fort (chute, agitation soudaine)
_PIXEL_DIFF_THRESH    = 25     # seuil absolu par canal (0-255)

# Mots-clés llava indiquant une urgence dans la réponse de surveillance
_EMERGENCY_KEYWORDS = [
    "oui", "chute", "tombé", "tombe", "malaise", "inconscient",
    "danger", "urgence", "blessé", "blessée", "accident", "secours",
    "appeler", "aide", "sol", "fallen", "emergency",
]

# Mots-clés émotions négatifs pour adapter le ton ALFRED
_EMOTION_MAP = {
    "fatigue": ["fatiguée", "fatigue", "épuisée", "épuisement", "yeux lourds", "lasse"],
    "stress":  ["stressée", "tendue", "anxieuse", "anxieux", "stress", "crispée", "crispé", "inquiète", "inquiet"],
    "tristesse": ["triste", "abattue", "mélancolique", "pleure", "larmes"],
    "joie":    ["sourit", "souriante", "heureuse", "joyeuse", "détendue"],
    "neutre":  ["neutre", "calme", "concentrée"],
}


# ─────────────────────────────────────────────────────────────────────────────
# VisionAnalyzer
# ─────────────────────────────────────────────────────────────────────────────

class VisionAnalyzer:
    """
    Orchestrateur des capacités vision ALFRED (B04).

    Args:
        vision_model : modèle Ollama multimodal (défaut: llava:7b)
        base_url     : URL Ollama (défaut: http://localhost:11434)
        timeout      : timeout appels llava en secondes
    """

    def __init__(
        self,
        vision_model: str = "llava:7b",
        base_url: str = "http://localhost:11434",
        timeout: int = 60,
    ):
        self._client = OllamaVisionClient(
            model=vision_model,
            base_url=base_url,
            timeout=timeout,
        )
        self._monitoring_thread: Optional[threading.Thread] = None
        self._monitoring_active = False
        self._prev_frame_bgr = None   # frame précédente pour diff mouvement
        self._lock = threading.Lock()

    # ─────────────────────────────────────────────────────
    # Disponibilité
    # ─────────────────────────────────────────────────────

    def is_vision_available(self) -> bool:
        """Vérifie qu'Ollama et llava sont disponibles."""
        return self._client.is_available()

    def is_opencv_available(self) -> bool:
        return _CV2_OK

    # ─────────────────────────────────────────────────────
    # 1. Description de scène
    # ─────────────────────────────────────────────────────

    def describe_scene(self, frame_b64: str) -> VisionEvent:
        """
        Demande à llava de décrire la scène visible dans le flux caméra.
        Focalise sur l'arrière-plan et l'environnement.

        Returns:
            VisionEvent(type="scene", severity="info", description=...)
        """
        prompt = (
            "Décris en français et en 2-3 phrases ce que tu vois dans cette image. "
            "Concentre-toi sur l'environnement et l'arrière-plan visible. "
            "Sois factuel et concis."
        )
        try:
            raw = self._client.analyze_image(frame_b64, prompt)
            return VisionEvent(
                type="scene",
                severity="info",
                description=raw,
                raw_llm_output=raw,
            )
        except Exception as exc:
            return VisionEvent(
                type="scene",
                severity="info",
                description=f"Impossible de décrire la scène : {exc}",
            )

    # ─────────────────────────────────────────────────────
    # 2. Analyse d'expression faciale
    # ─────────────────────────────────────────────────────

    def analyze_expression(self, frame_b64: str) -> VisionEvent:
        """
        Analyse l'expression et l'état émotionnel apparent de la personne.
        Le résultat `emotion_hint` est utilisé pour adapter le ton d'ALFRED.

        Returns:
            VisionEvent(type="expression", emotion_hint="fatigue"|"stress"|...)
        """
        prompt = (
            "Décris en français et en 1-2 phrases l'expression faciale et l'état "
            "émotionnel apparent de la personne visible. "
            "Ex: fatiguée, stressée, concentrée, souriante, triste... "
            "Sois factuel et bienveillant. Ne diagnostique pas."
        )
        try:
            raw = self._client.analyze_image(frame_b64, prompt)
            emotion_hint = self._extract_emotion_hint(raw)
            return VisionEvent(
                type="expression",
                severity="info",
                description=raw,
                raw_llm_output=raw,
                emotion_hint=emotion_hint,
            )
        except Exception as exc:
            return VisionEvent(
                type="expression",
                severity="info",
                description=f"Impossible d'analyser l'expression : {exc}",
            )

    def _extract_emotion_hint(self, llm_text: str) -> str:
        """Mappe le texte llava vers une émotion ALFRED connue."""
        text = llm_text.lower()
        for emotion, keywords in _EMOTION_MAP.items():
            if any(kw in text for kw in keywords):
                return emotion
        return "neutre"

    # ─────────────────────────────────────────────────────
    # 3. Détection de mouvement (OpenCV, local)
    # ─────────────────────────────────────────────────────

    def detect_motion(
        self,
        prev_frame_bgr,
        curr_frame_bgr,
    ) -> MotionResult:
        """
        Calcule le pourcentage de pixels ayant significativement changé entre
        deux frames BGR (numpy arrays) et retourne un MotionResult.

        Fonctionne 100% en local — aucun appel LLM.
        """
        if not _CV2_OK:
            return MotionResult(
                level="none", changed_pct=0.0, is_alert=False,
                description="OpenCV non disponible."
            )

        if prev_frame_bgr is None or curr_frame_bgr is None:
            return MotionResult(
                level="none", changed_pct=0.0, is_alert=False,
                description="Frames insuffisantes pour calculer le mouvement."
            )

        # Redimensionner à la même taille si nécessaire
        if prev_frame_bgr.shape != curr_frame_bgr.shape:
            curr_frame_bgr = cv2.resize(
                curr_frame_bgr,
                (prev_frame_bgr.shape[1], prev_frame_bgr.shape[0])
            )

        # Diff absolue canal par canal
        diff = cv2.absdiff(prev_frame_bgr, curr_frame_bgr)
        # Masque : pixels ayant changé au-delà du seuil sur au moins 1 canal
        mask = np.any(diff > _PIXEL_DIFF_THRESH, axis=2)
        changed_pct = float(mask.sum()) / mask.size * 100.0

        if changed_pct >= _MOTION_THRESH_HIGH:
            level, is_alert = "high", True
            desc = f"Mouvement fort détecté ({changed_pct:.1f}% de l'image modifiée)."
        elif changed_pct >= _MOTION_THRESH_MEDIUM:
            level, is_alert = "medium", False
            desc = f"Mouvement modéré ({changed_pct:.1f}%)."
        elif changed_pct >= _MOTION_THRESH_LOW:
            level, is_alert = "low", False
            desc = f"Léger mouvement ({changed_pct:.1f}%)."
        else:
            level, is_alert = "none", False
            desc = f"Aucun mouvement significatif ({changed_pct:.1f}%)."

        return MotionResult(
            level=level,
            changed_pct=changed_pct,
            is_alert=is_alert,
            description=desc,
        )

    # ─────────────────────────────────────────────────────
    # 4. Analyse d'urgence (chute / danger)
    # ─────────────────────────────────────────────────────

    def analyze_emergency(self, frame_b64: str) -> VisionEvent:
        """
        Demande à llava si une situation d'urgence est visible (chute, malaise…).
        Utilisé par le monitoring après détection d'un mouvement fort.

        Returns:
            VisionEvent(type="fall_detected"|"emergency"|"motion", severity=...)
        """
        prompt = (
            "Regarde attentivement cette image. "
            "Est-ce qu'il y a une situation d'urgence visible ? "
            "Une personne qui tombe, qui a chuté, qui est au sol, qui semble en malaise ? "
            "Réponds OBLIGATOIREMENT par OUI ou NON en premier mot, "
            "suivi d'une phrase de description en français."
        )
        try:
            raw = self._client.analyze_image(frame_b64, prompt)
            raw_lower = raw.lower().strip()

            is_emergency = any(kw in raw_lower for kw in _EMERGENCY_KEYWORDS[:3])
            # Vérification plus stricte : "oui" doit être le premier mot
            first_word = raw_lower.split()[0] if raw_lower.split() else ""
            is_emergency = first_word in ("oui", "yes") or (
                is_emergency and any(kw in raw_lower for kw in _EMERGENCY_KEYWORDS[1:])
            )

            if is_emergency:
                event_type = "fall_detected"
                severity = "critical"
                description = (
                    f"⚠️ Situation d'urgence détectée ! {raw.lstrip('OUIOui').strip()}"
                )
            else:
                event_type = "motion"
                severity = "info"
                description = f"Mouvement fort détecté — pas de danger apparent. {raw}"

            return VisionEvent(
                type=event_type,
                severity=severity,
                description=description,
                raw_llm_output=raw,
            )

        except Exception as exc:
            # En cas d'échec llava → prudence : on signale quand même
            return VisionEvent(
                type="motion",
                severity="warning",
                description=f"Mouvement fort détecté — analyse d'urgence impossible ({exc}).",
            )

    # ─────────────────────────────────────────────────────
    # 5. Monitoring continu
    # ─────────────────────────────────────────────────────

    def start_monitoring(
        self,
        snapshot_fn: Callable[[], Optional[str]],
        on_alert: Callable[[VisionEvent], None],
        interval_s: float = 2.0,
        expression_interval_s: float = 30.0,
    ) -> None:
        """
        Lance un thread daemon de surveillance caméra.

        Args:
            snapshot_fn           : fonction qui retourne une frame JPEG base64 (ou None)
            on_alert              : callback appelé sur tout VisionEvent severity != "info"
                                    ET sur les analyses d'expression périodiques
            interval_s            : intervalle entre deux analyses mouvement (secondes)
            expression_interval_s : intervalle entre deux analyses expression (secondes)
        """
        if self._monitoring_active:
            return

        self._monitoring_active = True
        self._monitoring_thread = threading.Thread(
            target=self._monitoring_loop,
            args=(snapshot_fn, on_alert, interval_s, expression_interval_s),
            daemon=True,
            name="VisionMonitor",
        )
        self._monitoring_thread.start()

    def stop_monitoring(self) -> None:
        """Arrête le thread de monitoring."""
        self._monitoring_active = False
        self._monitoring_thread = None
        with self._lock:
            self._prev_frame_bgr = None

    @property
    def is_monitoring(self) -> bool:
        return self._monitoring_active

    def _monitoring_loop(
        self,
        snapshot_fn: Callable[[], Optional[str]],
        on_alert: Callable[[VisionEvent], None],
        interval_s: float,
        expression_interval_s: float,
    ) -> None:
        """Boucle principale du thread de surveillance."""
        last_expression_check = 0.0

        while self._monitoring_active:
            t0 = time.monotonic()

            try:
                frame_b64 = snapshot_fn()
                if frame_b64 is None:
                    time.sleep(interval_s)
                    continue

                # ── Détection mouvement ────────────────────────────────────────
                if _CV2_OK:
                    curr_bgr = self._b64_to_bgr(frame_b64)
                    with self._lock:
                        prev_bgr = self._prev_frame_bgr
                        self._prev_frame_bgr = curr_bgr

                    if prev_bgr is not None and curr_bgr is not None:
                        motion = self.detect_motion(prev_bgr, curr_bgr)

                        if motion.is_alert:
                            # Mouvement fort → analyse urgence avec llava
                            event = self.analyze_emergency(frame_b64)
                            on_alert(event)
                        elif motion.level == "medium":
                            # Mouvement modéré → signalement simple sans llava
                            on_alert(VisionEvent(
                                type="motion",
                                severity="info",
                                description=motion.description,
                            ))

                # ── Analyse expression périodique ──────────────────────────────
                now = time.monotonic()
                if now - last_expression_check >= expression_interval_s:
                    last_expression_check = now
                    if self.is_vision_available():
                        expr_event = self.analyze_expression(frame_b64)
                        # Toujours notifier pour l'adaptation tonale, même severity info
                        on_alert(expr_event)

            except Exception:
                pass  # monitoring ne doit jamais crasher

            elapsed = time.monotonic() - t0
            wait = max(0.0, interval_s - elapsed)
            if wait > 0:
                time.sleep(wait)

    # ─────────────────────────────────────────────────────
    # Utilitaires
    # ─────────────────────────────────────────────────────

    @staticmethod
    def _b64_to_bgr(image_b64: str):
        """Décode une image JPEG base64 en array BGR numpy."""
        if not _CV2_OK:
            return None
        try:
            raw = base64.b64decode(image_b64)
            arr = np.frombuffer(raw, dtype=np.uint8)
            return cv2.imdecode(arr, cv2.IMREAD_COLOR)
        except Exception:
            return None

    @staticmethod
    def frame_bgr_to_b64(frame_bgr, quality: int = 75) -> Optional[str]:
        """Encode un array BGR numpy en JPEG base64."""
        if not _CV2_OK or frame_bgr is None:
            return None
        try:
            ok, buf = cv2.imencode(".jpg", frame_bgr, [cv2.IMWRITE_JPEG_QUALITY, quality])
            if not ok:
                return None
            return base64.b64encode(buf.tobytes()).decode("ascii")
        except Exception:
            return None
