# ============================================================
# ALFRED — src/regulation/wellbeing_tracker.py
# Bloc 03.05 — Suivi bien-être, énergie & fatigue
#
# Fonctions couvertes :
#   03.05.001 Détection fatigue (texte)         ✅ V1/V2
#   03.05.002 Mode low-energy                   ✅ V1/V2
#   03.05.003 Détection état flow               ✅ V2
#   03.05.004 Adaptation proactivité            ✅ V2
#   03.05.005 Suivi courbe énergie journée      ✅ V2
# ============================================================

import json
from datetime import datetime, timedelta
from pathlib import Path
from dataclasses import dataclass, field

from src.security.security_logger import log_event

# ── Stockage ──────────────────────────────────────────────
_WELLBEING_FILE = Path("data/memory/wellbeing_log.json")
_WELLBEING_FILE.parent.mkdir(parents=True, exist_ok=True)


# ─────────────────────────────────────────────────────────
# Modèle état bien-être
# ─────────────────────────────────────────────────────────

@dataclass
class WellbeingState:
    """État de bien-être estimé de l'utilisateur."""
    energy_level:  str   = "medium"   # low / medium / high
    fatigue_score: float = 0.0        # 0.0 → 1.0
    flow_detected: bool  = False
    mode_suggestion: str = "focus"    # Mode ALFRED recommandé
    timestamp:     str   = field(default_factory=lambda: datetime.now().isoformat())


# ─────────────────────────────────────────────────────────
# Signaux textuels
# ─────────────────────────────────────────────────────────

_FATIGUE_SIGNALS = {
    "high": [
        "épuisée", "lessivée", "crevée", "vidée", "à plat",
        "plus de jus", "je tombe de sommeil", "exténuée",
        "exhausted", "drained", "burned out", "wiped out",
    ],
    "medium": [
        "fatiguée", "pas très en forme", "un peu fatiguée",
        "pas au top", "sans énergie", "bof", "j'ai du mal",
        "tired", "not great", "low energy",
    ],
    "low": [
        "un peu", "légèrement fatiguée", "besoin d'une pause",
        "slightly tired", "could use a break",
    ],
}

_FLOW_SIGNALS = [
    "dans le flow", "dans le zone", "concentrée", "en mode focus",
    "ça avance bien", "productif", "super concentrée", "j'avance",
    "in the zone", "flow state", "focused", "productive", "on a roll",
]

_LOW_ENERGY_SIGNALS = [
    "pas envie", "la flemme", "pas motivée", "force pas",
    "laisse tomber", "plus tard", "demain",
    "no motivation", "can't be bothered", "not today",
]


# ─────────────────────────────────────────────────────────
# Analyse
# ─────────────────────────────────────────────────────────

def analyze_wellbeing(
    text: str,
    time_context: dict | None = None,
) -> WellbeingState:
    """
    Analyse le bien-être depuis le texte + contexte temporel.

    Args:
        text         : Message utilisateur
        time_context : Dict depuis context_builder.get_time_context()

    Returns:
        WellbeingState avec énergie, fatigue, flow, suggestion mode
    """
    text_lower = text.lower()

    # ── Détection fatigue ──────────────────────────────
    fatigue_score = 0.0
    for level, signals in _FATIGUE_SIGNALS.items():
        if any(s in text_lower for s in signals):
            if level == "high":
                fatigue_score = max(fatigue_score, 0.9)
            elif level == "medium":
                fatigue_score = max(fatigue_score, 0.6)
            else:
                fatigue_score = max(fatigue_score, 0.3)

    # ── Pénalité heure tardive ──────────────────────────
    if time_context:
        hour = time_context.get("hour", 12)
        energy_from_time = time_context.get("energy_level", "medium")
        if energy_from_time == "low":
            fatigue_score = min(1.0, fatigue_score + 0.15)

    # ── Détection low-energy (pas fatigue mais désengagement) ─
    low_energy = any(s in text_lower for s in _LOW_ENERGY_SIGNALS)
    if low_energy and fatigue_score < 0.4:
        fatigue_score = 0.4

    # ── Détection flow ──────────────────────────────────
    flow = any(s in text_lower for s in _FLOW_SIGNALS)

    # ── Niveau énergie global ───────────────────────────
    if flow:
        energy_level = "high"
    elif fatigue_score >= 0.6:
        energy_level = "low"
    elif fatigue_score >= 0.3:
        energy_level = "medium"
    else:
        # Fallback contexte temporel
        energy_level = time_context.get("energy_level", "medium") if time_context else "medium"

    # ── Mode suggéré ────────────────────────────────────
    if energy_level == "low":
        mode_suggestion = "support"
    elif flow:
        mode_suggestion = "focus"
    else:
        mode_suggestion = "focus"

    return WellbeingState(
        energy_level    = energy_level,
        fatigue_score   = round(fatigue_score, 2),
        flow_detected   = flow,
        mode_suggestion = mode_suggestion,
    )


def is_low_energy(state: WellbeingState) -> bool:
    """True si l'utilisateur est en basse énergie."""
    return state.energy_level == "low"


def is_in_flow(state: WellbeingState) -> bool:
    """True si l'utilisateur est en état de flow."""
    return state.flow_detected


# ─────────────────────────────────────────────────────────
# Suggestions bien-être
# ─────────────────────────────────────────────────────────

def get_wellbeing_suggestion(state: WellbeingState) -> str | None:
    """
    Génère une suggestion bien-être adaptée à l'état.
    Retourne None si aucune suggestion appropriée.

    Args:
        state : WellbeingState courant

    Returns:
        Suggestion textuelle ou None
    """
    import random

    if state.fatigue_score >= 0.8:
        suggestions = [
            "Tu as l'air vraiment épuisée. Une courte pause de 10 minutes peut tout changer.",
            "Ton cerveau a besoin de récupérer. On reprend dans quelques minutes ?",
            "Avant de continuer, bois quelque chose. Sérieusement.",
        ]
        return random.choice(suggestions)

    if state.fatigue_score >= 0.5:
        suggestions = [
            "Je sens de la fatigue. On garde un rythme doux pour l'instant.",
            "On avance tranquillement — pas besoin de tout faire d'un coup.",
            "Un peu de fatigue ? On peut s'arrêter quand tu veux.",
        ]
        return random.choice(suggestions)

    if is_in_flow(state):
        suggestions = [
            "Tu es dans le flow — je garde un profil bas pour ne pas te distraire.",
            "Bel élan. Je suis là si tu as besoin.",
        ]
        return random.choice(suggestions)

    return None


# ─────────────────────────────────────────────────────────
# Suivi courbe énergie journée (02.05.005)
# ─────────────────────────────────────────────────────────

def log_wellbeing_point(state: WellbeingState) -> None:
    """
    Enregistre un point de données bien-être dans le log journalier.
    Permet de tracer la courbe d'énergie sur la journée.

    Args:
        state : WellbeingState à enregistrer
    """
    try:
        log_data = []
        if _WELLBEING_FILE.exists():
            log_data = json.loads(_WELLBEING_FILE.read_text(encoding="utf-8"))

        log_data.append({
            "timestamp":     state.timestamp,
            "energy_level":  state.energy_level,
            "fatigue_score": state.fatigue_score,
            "flow":          state.flow_detected,
            "mode_suggested": state.mode_suggestion,
        })

        # Garder seulement les 30 derniers jours
        cutoff = (datetime.now() - timedelta(days=30)).isoformat()
        log_data = [e for e in log_data if e["timestamp"] >= cutoff]

        _WELLBEING_FILE.write_text(
            json.dumps(log_data, indent=2, ensure_ascii=False),
            encoding="utf-8"
        )
    except Exception as e:
        log_event(f"Erreur log wellbeing : {e}", "WARNING")


def get_energy_curve(hours: int = 24) -> list[dict]:
    """
    Retourne la courbe d'énergie des dernières N heures.

    Args:
        hours : Fenêtre temporelle en heures

    Returns:
        Liste de points énergie triés chronologiquement
    """
    if not _WELLBEING_FILE.exists():
        return []

    try:
        log_data = json.loads(_WELLBEING_FILE.read_text(encoding="utf-8"))
        cutoff = (datetime.now() - timedelta(hours=hours)).isoformat()
        return [e for e in log_data if e["timestamp"] >= cutoff]
    except Exception:
        return []


def get_daily_energy_summary() -> dict:
    """
    Résumé du niveau d'énergie sur la journée courante.

    Returns:
        dict avec distribution énergie et état dominant
    """
    points = get_energy_curve(hours=24)
    if not points:
        return {"data": "Aucune donnée aujourd'hui", "dominant": "unknown"}

    counts = {"low": 0, "medium": 0, "high": 0}
    flow_count = 0

    for p in points:
        level = p.get("energy_level", "medium")
        counts[level] = counts.get(level, 0) + 1
        if p.get("flow"):
            flow_count += 1

    dominant = max(counts, key=counts.get)
    return {
        "total_points":  len(points),
        "distribution":  counts,
        "dominant":      dominant,
        "flow_moments":  flow_count,
    }
