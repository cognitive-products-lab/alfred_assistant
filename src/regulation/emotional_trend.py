"""
PROJECT      : ALFRED
BLOCK        : B03
FUNCTION     : 03.01 (continuité) — Tendance émotionnelle dans le temps
FILE         : src/regulation/emotional_trend.py
ROLE         : Passe d'une émotion "par message" (emotion_detector.py, sans
               mémoire) à une tendance perçue sur plusieurs jours — même
               principe que wellbeing_tracker.py::get_daily_energy_summary()
               mais appliqué à l'émotion plutôt qu'à l'énergie.

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-08-18
VERSION      : V1.0
STATUS       : TESTED

DESCRIPTION :
Session 4 (plan semaine 17-24/08/2026) : data/v3/emotion_state.json et
relational_state.json (schéma défini le 16/07/2026) n'ont jamais été
alimentés — src/v3/emotion/ est un stub vide, aucun code ne les lit ni ne
les écrit. Plutôt que de raccrocher ce schéma V3 orphelin, ce module
construit un vrai suivi, branché sur le pipeline réellement actif
(RegulationEngine.process(), lui-même appelé depuis main.py).

Principe : chaque détection d'émotion (emotion_detector.detect_emotion())
est journalisée avec sa valence (positive/negative/neutral, déjà calculée
par le catalogue d'émotions). get_emotion_trend() résume une fenêtre
glissante (3 jours par défaut) — pas juste l'instant présent.
"""

import json
from dataclasses import dataclass
from datetime import datetime, timedelta

from src.security.security_logger import log_event
from paths import DATA_MEMORY

_TREND_FILE = DATA_MEMORY / "emotion_trend_log.json"
_TREND_FILE.parent.mkdir(parents=True, exist_ok=True)

_RETENTION_DAYS = 30

# En dessous de ce nombre de points sur la fenêtre, pas assez de signal pour
# parler de "tendance" — éviter de réagir à 1-2 messages isolés comme si
# c'était un pattern.
_MIN_POINTS_FOR_TREND = 3

# Au-dessus de ce ratio de détections à valence négative sur la fenêtre,
# la tendance est jugée "difficile" — seuil délibérément > 50% (pas juste
# "plus de négatif que de positif sur 3 points", un vrai motif soutenu).
_CONCERNING_RATIO = 0.55


def log_emotion_point(emotion: str, valence: str, intensity: float, timestamp: str | None = None) -> None:
    """
    Enregistre un point de détection émotionnelle dans le log — appelé à
    chaque tour depuis RegulationEngine._apply_emotion(), même schéma que
    wellbeing_tracker.log_wellbeing_point().
    """
    try:
        log_data = []
        if _TREND_FILE.exists():
            log_data = json.loads(_TREND_FILE.read_text(encoding="utf-8"))

        log_data.append({
            "timestamp": timestamp or datetime.now().isoformat(),
            "emotion":   emotion,
            "valence":   valence,
            "intensity": intensity,
        })

        cutoff = (datetime.now() - timedelta(days=_RETENTION_DAYS)).isoformat()
        log_data = [e for e in log_data if e.get("timestamp", "") >= cutoff]

        _TREND_FILE.write_text(
            json.dumps(log_data, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
    except Exception as e:
        log_event(f"Erreur log tendance émotionnelle : {e}", "WARNING")


def get_emotion_points(days: int = 3) -> list[dict]:
    """Points de détection émotionnelle des N derniers jours, triés chronologiquement."""
    if not _TREND_FILE.exists():
        return []
    try:
        log_data = json.loads(_TREND_FILE.read_text(encoding="utf-8"))
        cutoff = (datetime.now() - timedelta(days=days)).isoformat()
        return [e for e in log_data if e.get("timestamp", "") >= cutoff]
    except Exception:
        return []


@dataclass
class EmotionTrend:
    window_days:      int   = 3
    total_points:      int   = 0
    negative_ratio:    float = 0.0
    dominant_emotion:  str   = "neutral"
    is_concerning:     bool  = False
    label:             str   = "pas assez de données"


def get_emotion_trend(window_days: int = 3) -> EmotionTrend:
    """
    Résume la tendance émotionnelle sur une fenêtre glissante — pas
    l'émotion de l'instant présent (déjà couverte par emotion_detector),
    mais un motif soutenu sur plusieurs jours.
    """
    points = get_emotion_points(window_days)
    total = len(points)

    if total < _MIN_POINTS_FOR_TREND:
        return EmotionTrend(window_days=window_days, total_points=total)

    negatives = [p for p in points if p.get("valence") == "negative"]
    ratio = len(negatives) / total

    counts: dict[str, int] = {}
    for p in points:
        e = p.get("emotion") or "neutral"
        counts[e] = counts.get(e, 0) + 1
    dominant = max(counts, key=counts.get)

    concerning = ratio >= _CONCERNING_RATIO
    label = (
        "plus difficile que d'habitude ces derniers jours"
        if concerning else
        "stable"
    )

    return EmotionTrend(
        window_days=window_days,
        total_points=total,
        negative_ratio=round(ratio, 2),
        dominant_emotion=dominant,
        is_concerning=concerning,
        label=label,
    )
