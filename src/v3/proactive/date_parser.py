"""
PROJECT      : ALFRED
BLOCK        : B11 -- Intelligence Cognitive
FILE         : src/v3/proactive/date_parser.py
ROLE         : Parseur dates français naturelles -> datetime

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-05-14
VERSION      : V1.0
STATUS       : STABLE
"""

from __future__ import annotations

import re
from datetime import datetime, timedelta
from typing import Optional


# ── Mots-clés -> chiffres ─────────────────────────────────
_WORD_TO_INT: dict[str, int] = {
    "un": 1, "une": 1,
    "deux": 2, "trois": 3, "quatre": 4, "cinq": 5,
    "six": 6, "sept": 7, "huit": 8, "neuf": 9, "dix": 10,
    "onze": 11, "douze": 12, "quinze": 15, "vingt": 20,
    "trente": 30,
}


def _to_int(s: str) -> int:
    s = s.strip()
    if s.isdigit():
        return int(s)
    return _WORD_TO_INT.get(s.lower(), 1)


# ── Unités -> (attribut relativedelta, multiplicateur jours) ──
_UNIT_MAP: dict[str, str] = {
    "jour": "days", "jours": "days",
    "semaine": "weeks", "semaines": "weeks",
    "mois": "months",
    "an": "years", "ans": "years",
    "année": "years", "années": "years",
}

_NUMBER_PAT = r"(\d+|un|une|deux|trois|quatre|cinq|six|sept|huit|neuf|dix|onze|douze|quinze|vingt|trente)"
_UNIT_PAT   = r"(jours?|semaines?|mois|ans?|années?)"
_DANS_PAT   = re.compile(
    rf"dans\s+{_NUMBER_PAT}\s+{_UNIT_PAT}",
    re.IGNORECASE,
)


def _add_relative(base: datetime, n: int, unit: str) -> datetime:
    unit = _UNIT_MAP.get(unit.lower(), "days")
    if unit == "days":
        return base + timedelta(days=n)
    if unit == "weeks":
        return base + timedelta(weeks=n)
    if unit == "months":
        month = base.month - 1 + n
        year  = base.year + month // 12
        month = month % 12 + 1
        day   = min(base.day, [31,28,29,30,31,30,31,31,30,31,30,31][month-1])
        return base.replace(year=year, month=month, day=day)
    if unit == "years":
        return base.replace(year=base.year + n)
    return base + timedelta(days=n)


def parse_french_date(text: str, reference: Optional[datetime] = None) -> Optional[datetime]:
    """
    Extrait une date depuis du texte français naturel.
    Retourne None si aucune date trouvée.

    Exemples :
        "dans 5 mois"         -> aujourd'hui + 5 mois
        "dans 1 mois"         -> aujourd'hui + 1 mois
        "dans trois semaines" -> aujourd'hui + 3 semaines
        "demain"              -> aujourd'hui + 1 jour
        "après-demain"        -> aujourd'hui + 2 jours
        "la semaine prochaine"-> aujourd'hui + 7 jours
        "le mois prochain"    -> aujourd'hui + 1 mois
    """
    if reference is None:
        reference = datetime.now()

    low = text.lower()

    # Cas spéciaux
    if "après-demain" in low or "apres-demain" in low:
        return reference + timedelta(days=2)
    if "demain" in low:
        return reference + timedelta(days=1)
    if "semaine prochaine" in low:
        return reference + timedelta(weeks=1)
    if "mois prochain" in low:
        return _add_relative(reference, 1, "mois")
    if "année prochaine" in low or "an prochain" in low:
        return _add_relative(reference, 1, "années")

    # "dans N unité"
    m = _DANS_PAT.search(low)
    if m:
        n    = _to_int(m.group(1))
        unit = m.group(2)
        return _add_relative(reference, n, unit)

    return None


def find_all_dates(text: str, reference: Optional[datetime] = None) -> list[tuple[str, datetime]]:
    """
    Trouve toutes les occurrences de dates dans un texte.
    Retourne une liste de (fragment_texte, datetime).
    """
    if reference is None:
        reference = datetime.now()

    results: list[tuple[str, datetime]] = []
    low = text.lower()

    for m in _DANS_PAT.finditer(low):
        fragment = m.group(0)
        n        = _to_int(m.group(1))
        unit     = m.group(2)
        dt       = _add_relative(reference, n, unit)
        results.append((fragment, dt))

    if not results:
        simple = parse_french_date(text, reference)
        if simple:
            results.append((text, simple))

    return results
