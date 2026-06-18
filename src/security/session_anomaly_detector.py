"""
════════════════════════════════════════════════════════════
PROJECT      : ALFRED
BLOCK        : B20
FUNCTION     : 20.17
FILE         : src/security/session_anomaly_detector.py
ROLE         : Détection d'anomalies de session (patterns suspects)

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-06-01
UPDATED      : 2026-06-01
VERSION      : V1.0
STATUS       : ACTIVE

DESCRIPTION :
Analyse les patterns de sessions pour détecter des comportements anormaux :
- Rotation rapide de session (session hopping)
- Requêtes trop rapides (bot-like)
- Changement de device mid-session
- Volume de requêtes anormal
- Heure d'accès inhabituelle (hors profil baseline)
════════════════════════════════════════════════════════════
"""
from __future__ import annotations

import threading
import time
from collections import defaultdict, deque
from datetime import datetime, timezone
from typing import Any

from src.security.security_logger import log_event

_lock = threading.Lock()

# ─── État en mémoire ──────────────────────────────────────────────────────────

# {user_id: deque of (timestamp, session_id)}
_session_history: dict[str, deque] = defaultdict(lambda: deque(maxlen=50))

# {user_id: deque of (timestamp,) — timestamps des requêtes}
_request_log: dict[str, deque] = defaultdict(lambda: deque(maxlen=200))

# {user_id: set of device_ids vus dans la session courante}
_session_devices: dict[str, set] = defaultdict(set)

# Paramètres
MAX_SESSIONS_PER_HOUR    = 10    # rotations de session
MIN_REQUEST_INTERVAL_MS  = 200   # intervalle minimum entre requêtes (ms)
MAX_REQUESTS_PER_MINUTE  = 60
UNUSUAL_HOUR_START       = 0     # heure de début de plage inhabituelle (UTC)
UNUSUAL_HOUR_END         = 5     # heure de fin (minuit à 5h UTC)


# ─── Enregistrement ───────────────────────────────────────────────────────────

def record_session_start(user_id: str, session_id: str) -> None:
    """Enregistre le démarrage d'une session."""
    with _lock:
        _session_history[user_id].append((time.time(), session_id))


def record_request(user_id: str, session_id: str, device_id: str = "") -> None:
    """Enregistre une requête utilisateur."""
    with _lock:
        _request_log[user_id].append(time.time())
        if device_id:
            _session_devices[user_id].add(device_id)


def clear_user_state(user_id: str) -> None:
    """Réinitialise l'état d'un utilisateur (déconnexion propre)."""
    with _lock:
        _session_history.pop(user_id, None)
        _request_log.pop(user_id, None)
        _session_devices.pop(user_id, None)


# ─── Détections ───────────────────────────────────────────────────────────────

def detect_session_hopping(user_id: str, window_seconds: float = 3600.0) -> dict[str, Any]:
    """
    Détecte une rotation anormalement rapide de sessions.
    Un attaquant qui contourne les sessions crée beaucoup de sessions courtes.
    """
    with _lock:
        now = time.time()
        recent = [(ts, sid) for ts, sid in _session_history[user_id]
                  if now - ts < window_seconds]
    count = len(recent)
    is_anomaly = count >= MAX_SESSIONS_PER_HOUR
    if is_anomaly:
        log_event(f"session_anomaly: hopping détecté user={user_id} "
                  f"sessions={count}/{MAX_SESSIONS_PER_HOUR} en {window_seconds:.0f}s", "WARNING")
    return {
        "user_id":        user_id,
        "sessions_count": count,
        "max_allowed":    MAX_SESSIONS_PER_HOUR,
        "window_seconds": window_seconds,
        "is_anomaly":     is_anomaly,
        "severity":       "HIGH" if is_anomaly else "LOW",
    }


def detect_request_flooding(user_id: str, window_seconds: float = 60.0) -> dict[str, Any]:
    """
    Détecte un volume de requêtes anormal (comportement bot).
    """
    with _lock:
        now = time.time()
        recent = [ts for ts in _request_log[user_id] if now - ts < window_seconds]
        count = len(recent)

        # Intervalle moyen entre requêtes
        if len(recent) >= 2:
            sorted_ts = sorted(recent)
            intervals = [(sorted_ts[i+1] - sorted_ts[i]) * 1000
                         for i in range(len(sorted_ts) - 1)]
            avg_interval_ms = sum(intervals) / len(intervals)
        else:
            avg_interval_ms = float("inf")

    rate = count / (window_seconds / 60)
    is_flooding   = count > MAX_REQUESTS_PER_MINUTE
    is_bot_like   = avg_interval_ms < MIN_REQUEST_INTERVAL_MS and count > 5

    is_anomaly = is_flooding or is_bot_like
    if is_anomaly:
        log_event(f"session_anomaly: flood détecté user={user_id} "
                  f"rate={rate:.1f}/min avg_interval={avg_interval_ms:.0f}ms", "WARNING")

    return {
        "user_id":           user_id,
        "requests_in_window": count,
        "rate_per_minute":   round(rate, 2),
        "avg_interval_ms":   round(avg_interval_ms, 1) if avg_interval_ms != float("inf") else None,
        "is_flooding":       is_flooding,
        "is_bot_like":       is_bot_like,
        "is_anomaly":        is_anomaly,
        "severity":          "CRITICAL" if is_bot_like and is_flooding else
                             "HIGH" if is_bot_like or is_flooding else "LOW",
    }


def detect_device_switching(user_id: str) -> dict[str, Any]:
    """
    Détecte un changement de device mid-session (possible session hijacking).
    """
    with _lock:
        devices = set(_session_devices.get(user_id, set()))
    count = len(devices)
    is_anomaly = count > 1
    if is_anomaly:
        log_event(f"session_anomaly: changement device user={user_id} "
                  f"devices={count}", "WARNING")
    return {
        "user_id":        user_id,
        "device_count":   count,
        "is_anomaly":     is_anomaly,
        "severity":       "HIGH" if count > 2 else "MEDIUM" if is_anomaly else "LOW",
    }


def detect_unusual_hour(user_id: str = "") -> dict[str, Any]:
    """
    Détecte un accès à une heure inhabituelle (UNUSUAL_HOUR_START à UNUSUAL_HOUR_END UTC).
    """
    now_utc  = datetime.now(timezone.utc)
    hour_utc = now_utc.hour
    is_unusual = UNUSUAL_HOUR_START <= hour_utc < UNUSUAL_HOUR_END
    return {
        "user_id":     user_id,
        "hour_utc":    hour_utc,
        "is_unusual":  is_unusual,
        "range":       f"{UNUSUAL_HOUR_START:02d}h-{UNUSUAL_HOUR_END:02d}h UTC",
        "severity":    "MEDIUM" if is_unusual else "LOW",
    }


# ─── Analyse globale ──────────────────────────────────────────────────────────

def analyze_session(
    user_id: str,
    session_id: str = "",
    device_id: str = "",
) -> dict[str, Any]:
    """
    Analyse complète du profil de session d'un utilisateur.
    Combine toutes les détections en un score de risque global.

    Returns:
        dict avec risk_score (0-100), risk_level, anomalies, details
    """
    hopping  = detect_session_hopping(user_id)
    flooding = detect_request_flooding(user_id)
    devices  = detect_device_switching(user_id)
    hour     = detect_unusual_hour(user_id)

    score = 0
    if hopping["is_anomaly"]:   score += 30
    if flooding["is_flooding"]: score += 25
    if flooding["is_bot_like"]: score += 35
    if devices["is_anomaly"]:   score += 20
    if hour["is_unusual"]:      score += 10

    score = min(100, score)
    level = "CRITICAL" if score >= 80 else "HIGH" if score >= 50 else \
            "MEDIUM"   if score >= 25 else "LOW"

    anomalies = [
        name for name, check in [
            ("session_hopping",    hopping["is_anomaly"]),
            ("request_flooding",   flooding["is_flooding"]),
            ("bot_like_pattern",   flooding["is_bot_like"]),
            ("device_switching",   devices["is_anomaly"]),
            ("unusual_hour",       hour["is_unusual"]),
        ] if check
    ]

    return {
        "user_id":     user_id,
        "session_id":  session_id,
        "risk_score":  score,
        "risk_level":  level,
        "anomalies":   anomalies,
        "is_suspicious": score >= 25,
        "timestamp":   datetime.now(timezone.utc).isoformat(),
        "details": {
            "session_hopping": hopping,
            "request_flooding": flooding,
            "device_switching": devices,
            "unusual_hour":     hour,
        },
    }
