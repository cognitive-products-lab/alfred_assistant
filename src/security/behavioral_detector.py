"""
════════════════════════════════════════════════════════════
PROJECT      : ALFRED
BLOCK        : B20
FUNCTION     : 20.04
FILE         : behavioral_detector.py
ROLE         : Détection d'anomalies comportementales avec baseline persistée

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-05-23
UPDATED      : 2026-06-01
VERSION      : V2.0
STATUS       : ACTIVE

DESCRIPTION :
Détecte les écarts comportementaux par comparaison à une baseline
persistée en JSON. Supporte la mise à jour incrémentale de la baseline
(moyenne glissante), la fenêtre temporelle et le scoring pondéré.
════════════════════════════════════════════════════════════
"""
from __future__ import annotations

import json
import threading
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from src.security.security_logger import log_event

_ROOT          = Path(__file__).resolve().parents[2]
_BASELINE_FILE = _ROOT / "data" / "security" / "behavior_baseline.json"
_BASELINE_FILE.parent.mkdir(parents=True, exist_ok=True)

_lock = threading.Lock()

# ─── Baseline en mémoire (chargée au démarrage, persistée à chaque mise à jour) ──

_baseline: dict[str, dict[str, float]] = {}   # {metric_name: {mean, std, samples}}
_session_log: dict[str, list[float]] = {}      # {metric_name: [valeur, ...]}
_WINDOW_SIZE = 100   # nombre max de valeurs en mémoire par métrique


def _load_baseline() -> None:
    global _baseline
    if _BASELINE_FILE.exists():
        try:
            with _BASELINE_FILE.open(encoding="utf-8") as f:
                _baseline = json.load(f)
        except Exception:
            _baseline = {}


def _save_baseline() -> None:
    try:
        _BASELINE_FILE.write_text(
            json.dumps(_baseline, indent=2, ensure_ascii=False), encoding="utf-8"
        )
    except Exception as exc:
        log_event(f"behavioral_detector: impossible de sauvegarder la baseline — {exc}", "ERROR")


# Chargement au démarrage
_load_baseline()


# ─── Mise à jour incrémentale Welford ─────────────────────────────────────────

def update_baseline(metric_name: str, value: float) -> None:
    """
    Met à jour la baseline d'une métrique avec une nouvelle observation.
    Utilise l'algorithme de Welford pour la moyenne et variance en ligne.
    """
    with _lock:
        if metric_name not in _baseline:
            _baseline[metric_name] = {"mean": value, "m2": 0.0, "samples": 1,
                                       "updated": datetime.now(timezone.utc).isoformat()}
        else:
            b = _baseline[metric_name]
            n    = b["samples"] + 1
            delta = value - b["mean"]
            mean  = b["mean"] + delta / n
            delta2 = value - mean
            m2    = b.get("m2", 0.0) + delta * delta2
            b.update({"mean": mean, "m2": m2, "samples": n,
                       "updated": datetime.now(timezone.utc).isoformat()})
        _save_baseline()


def get_baseline(metric_name: str) -> dict[str, float]:
    """Retourne la baseline d'une métrique (mean, std, samples)."""
    with _lock:
        b = _baseline.get(metric_name, {})
        if not b:
            return {"mean": 0.0, "std": 0.0, "samples": 0}
        n   = b.get("samples", 1)
        m2  = b.get("m2", 0.0)
        std = (m2 / n) ** 0.5 if n > 1 else 0.0
        return {"mean": b.get("mean", 0.0), "std": round(std, 4),
                "samples": n, "updated": b.get("updated", "")}


def reset_baseline(metric_name: str | None = None) -> None:
    """Réinitialise la baseline d'une métrique ou toutes si None."""
    with _lock:
        if metric_name:
            _baseline.pop(metric_name, None)
        else:
            _baseline.clear()
        _save_baseline()


# ─── Détection d'anomalie ─────────────────────────────────────────────────────

def detect_behavior_anomaly(
    current_value: float,
    baseline_value: float,
    threshold: float = 20.0,
) -> bool:
    """Détecte un écart comportemental simple par rapport à un seuil absolu."""
    return abs(current_value - baseline_value) > threshold


def detect_statistical_anomaly(
    metric_name: str,
    current_value: float,
    sigma_threshold: float = 3.0,
) -> dict[str, Any]:
    """
    Détecte une anomalie statistique (Z-score) basée sur la baseline persistée.

    Args:
        metric_name     : nom de la métrique
        current_value   : valeur courante à évaluer
        sigma_threshold : nombre de déviations standard pour déclencher une alerte

    Returns:
        dict avec is_anomaly, z_score, baseline_mean, baseline_std, severity
    """
    b = get_baseline(metric_name)
    mean, std = b["mean"], b["std"]

    if std > 0:
        z_score = abs(current_value - mean) / std
    elif b["samples"] >= 10 and current_value != mean:
        # std=0 : toutes les valeurs sont identiques → toute déviation = anomalie
        z_score = float("inf")
    else:
        z_score = 0.0

    is_anomaly = b["samples"] >= 10 and (
        z_score >= sigma_threshold or z_score == float("inf")
    )

    if is_anomaly:
        severity = "CRITICAL" if z_score >= sigma_threshold * 2 else "HIGH" if z_score >= sigma_threshold * 1.5 else "MEDIUM"
        log_event(
            f"behavioral_detector: anomalie '{metric_name}' "
            f"val={current_value:.2f} mean={mean:.2f} std={std:.2f} z={z_score:.2f}",
            "WARNING",
        )
    else:
        severity = "LOW"

    return {
        "metric_name":    metric_name,
        "current_value":  current_value,
        "baseline_mean":  round(mean, 4),
        "baseline_std":   round(std, 4),
        "baseline_samples": b["samples"],
        "z_score":        round(z_score, 4),
        "is_anomaly":     is_anomaly,
        "severity":       severity,
        "sigma_threshold": sigma_threshold,
    }


def record_and_detect(
    metric_name: str,
    current_value: float,
    sigma_threshold: float = 3.0,
    auto_update_baseline: bool = True,
) -> dict[str, Any]:
    """
    Enregistre une valeur, met à jour la baseline, et détecte une anomalie.
    Méthode principale pour un usage courant.
    """
    result = detect_statistical_anomaly(metric_name, current_value, sigma_threshold)
    if auto_update_baseline:
        update_baseline(metric_name, current_value)
    return result


# ─── API historique (compatibilité V1) ───────────────────────────────────────

def calculate_behavior_score(anomalies: list[bool]) -> int:
    """Calcule un score à partir d'une liste d'anomalies."""
    return sum(1 for a in anomalies if a)


def analyze_behavior_metric(
    metric_name: str,
    current_value: float,
    baseline_value: float,
    threshold: float = 20.0,
) -> dict:
    """Analyse une métrique comportementale (API V1 — threshold absolu)."""
    deviation  = abs(current_value - baseline_value)
    is_anomaly = deviation > threshold
    return {
        "metric_name":        metric_name,
        "current_value":      current_value,
        "baseline_value":     baseline_value,
        "absolute_deviation": deviation,
        "threshold":          threshold,
        "is_anomaly":         is_anomaly,
        "metric":             metric_name,
        "anomaly":            is_anomaly,
        "deviation":          deviation,
    }


def _anomaly_score(abs_dev: float, threshold: float) -> int:
    if threshold <= 0:
        return 0
    return max(0, int((abs_dev - threshold) // threshold)) * 20


def calculate_weighted_behavior_score(analyses: list[dict]) -> int:
    total = 0
    for a in analyses:
        if a.get("is_anomaly") or a.get("anomaly"):
            dev = a.get("absolute_deviation", a.get("deviation", 0))
            thr = a.get("threshold", 20)
            total += _anomaly_score(dev, thr)
    return total


def assess_behavior_profile(metrics: dict | list) -> dict:
    """Évalue un profil comportemental."""
    if isinstance(metrics, list):
        count = sum(1 for m in metrics if m.get("is_anomaly") or m.get("anomaly"))
        score = min(100, sum(
            _anomaly_score(m.get("absolute_deviation", m.get("deviation", 0)),
                           m.get("threshold", 20))
            for m in metrics if m.get("is_anomaly") or m.get("anomaly")
        ))
    else:
        count, raw_score = 0, 0
        for name, vals in metrics.items():
            dev = abs(vals.get("current", 0) - vals.get("baseline", 0))
            thr = vals.get("threshold", 20)
            if dev > thr:
                count += 1
                raw_score += _anomaly_score(dev, thr)
        score = min(100, raw_score)
    level = "CRITICAL" if score >= 90 else "HIGH" if score >= 60 else "LOW"
    return {"behavior_level": level, "anomalies_count": count, "behavior_score": score}


# ─── Fenêtre temporelle ───────────────────────────────────────────────────────

def record_event_rate(metric_name: str, window_seconds: float = 60.0) -> dict[str, Any]:
    """
    Enregistre un événement et calcule le taux sur la fenêtre glissante.
    Utile pour détecter des rafales (login attempts, requêtes, erreurs…).
    """
    with _lock:
        now = time.time()
        _session_log.setdefault(metric_name, [])
        _session_log[metric_name] = [
            t for t in _session_log[metric_name] if now - t < window_seconds
        ]
        _session_log[metric_name].append(now)
        count = len(_session_log[metric_name])

    rate_per_min = count / (window_seconds / 60)
    return {
        "metric_name":    metric_name,
        "count_in_window": count,
        "window_seconds": window_seconds,
        "rate_per_minute": round(rate_per_min, 2),
    }


def get_event_rate(metric_name: str, window_seconds: float = 60.0) -> dict[str, Any]:
    """Retourne le taux d'événements courant sans ajouter de nouvel événement."""
    with _lock:
        now = time.time()
        recent = [t for t in _session_log.get(metric_name, [])
                  if now - t < window_seconds]
    rate = len(recent) / (window_seconds / 60)
    return {"metric_name": metric_name, "count_in_window": len(recent),
            "window_seconds": window_seconds, "rate_per_minute": round(rate, 2)}
