#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PROJECT      : ALFRED
BLOCK        : B29
FUNCTION     : XX.XX
FILE         : hadoop_poc/mapper.py
ROLE         : Mapper Hadoop Streaming — comptage d'événements par jour/catégorie

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-07-09
UPDATED      : 2026-07-09
VERSION      : V1.0
STATUS       : VALIDATED — testé en conditions réelles le 09/07/2026

DESCRIPTION :
Lit les logs anonymisés (JSONL, un objet par ligne, cf.
scripts/anonymize_logs_for_hadoop.py) sur stdin et émet une clé
"log_type|date|categorie" par événement, valeur 1 — pattern classique
word-count adapté à l'agrégation de logs. La clé de catégorie dépend du
type de log (endpoint+result pour api_access, action+decision pour
audit_trail, soc_level pour soc_alerts).

Usage (dans le conteneur Hadoop) :
    hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming*.jar \
        -input /poc/input -output /poc/output \
        -mapper hadoop_poc/mapper.py -reducer hadoop_poc/reducer.py \
        -file hadoop_poc/mapper.py -file hadoop_poc/reducer.py

Portabilité : pas de f-strings ni de `from __future__ import annotations`
(PEP 563, Python 3.7+) — l'image Hadoop utilisée (Debian 9 stretch,
bde2020/hadoop-nodemanager) ne fournit que Python 3.5.
"""

import json
import sys

_CATEGORY_FIELDS = {
    "api_access": ("endpoint", "result"),
    "audit_trail": ("action", "decision"),
    "soc_alerts": ("soc_level",),
}


def main():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            record = json.loads(line)
        except ValueError:
            continue

        log_type = record.get("log_type", "unknown")
        date = record.get("date", "unknown")
        fields = _CATEGORY_FIELDS.get(log_type, ())
        category = "|".join(str(record.get(f, "?")) for f in fields) or "n/a"

        key = "{0}|{1}|{2}".format(log_type, date, category)
        print("{0}\t1".format(key))


if __name__ == "__main__":
    main()
