"""
PROJECT      : ALFRED
BLOCK        : B11 -- Intelligence Cognitive
FILE         : src/v3/proactive/reminder_detector.py
ROLE         : Détection automatique de rappels dans la conversation

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-05-14
VERSION      : V1.0
STATUS       : STABLE
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from src.v3.proactive.date_parser import find_all_dates


# ── Patterns déclencheurs de rappels ─────────────────────
_TRIGGER_PATTERNS = [
    re.compile(p, re.IGNORECASE) for p in [
        r"rappelle.?moi",
        r"n[' ]oublie pas",
        r"pense à",
        r"je dois .{3,60} dans \d",
        r"je dois .{3,60} dans (un|une|deux|trois|quatre|cinq|six|sept|huit|neuf|dix|onze|douze)",
        r"il faut .{3,60} dans",
        r"prévoir .{3,60} dans",
        r"planifie",
        r"à faire dans",
    ]
]

# Verbes d'action courants (pour extraire la tâche)
_ACTION_VERBS = re.compile(
    r"\b(vermifuger|vacciner|vaccin|antipuce|antiparasitaire|médicament|"
    r"rendez.vous|rdv|réunion|appeler|appel|payer|renouveler|acheter|"
    r"vérifier|contrôle|bilan|rappel|rappeler|faire|envoyer|contacter)\b",
    re.IGNORECASE,
)


@dataclass
class DetectedReminder:
    title:    str
    due_at:   datetime
    fragment: str     # portion de texte source


def detect_reminders(text: str, reference: Optional[datetime] = None) -> list[DetectedReminder]:
    """
    Analyse un message utilisateur et extrait les rappels implicites.

    Détecte :
    - Commandes explicites : "rappelle-moi de X dans N mois"
    - Mentions passives  : "je dois vermifuger dans 5 mois"
    - Plusieurs rappels dans une même phrase
    """
    if reference is None:
        reference = datetime.now()

    dates = find_all_dates(text, reference)
    if not dates:
        return []

    # Vérifie qu'il y a un déclencheur ou un verbe d'action
    has_trigger = any(p.search(text) for p in _TRIGGER_PATTERNS)
    has_action  = bool(_ACTION_VERBS.search(text))

    if not (has_trigger or has_action):
        return []

    results: list[DetectedReminder] = []

    for fragment, due_dt in dates:
        title = _extract_title(text, fragment)
        if title:
            results.append(DetectedReminder(
                title    = title,
                due_at   = due_dt,
                fragment = fragment,
            ))

    return results


def _extract_title(text: str, date_fragment: str) -> str:
    """
    Extrait le titre du rappel depuis la clause immédiatement avant la date.
    Découpe sur 'et', virgule, point-virgule pour isoler la bonne clause.
    """
    low = text.lower()
    idx = low.find(date_fragment.lower())

    # Texte avant le fragment de date
    before = text[:idx].strip() if idx > 0 else text.strip()

    # Découpe la clause la plus proche (après "et", ",", ";", ".")
    clauses = re.split(r"\bet\b|[,;.]", before, flags=re.IGNORECASE)
    clause  = clauses[-1].strip() if clauses else before.strip()

    # Supprime les mots d'amorce
    clause = re.sub(
        r"^(je dois|il faut|rappelle.?moi de?|pense à|n[' ]oublie pas de?|"
        r"planifie|à faire|prévoir|leur mettre de l[' ]?|mettre de l[' ]?)\s*",
        "",
        clause,
        flags=re.IGNORECASE,
    ).strip(" ,.")

    # Capitalise
    if clause:
        clause = clause[0].upper() + clause[1:]

    return clause if len(clause) >= 3 else ""
