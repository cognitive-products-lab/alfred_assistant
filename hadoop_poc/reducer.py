#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PROJECT      : ALFRED
BLOCK        : B29
FUNCTION     : XX.XX
FILE         : hadoop_poc/reducer.py
ROLE         : Reducer Hadoop Streaming — somme des comptages par clé

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-07-09
UPDATED      : 2026-07-09
VERSION      : V1.0
STATUS       : VALIDATED — testé en conditions réelles le 09/07/2026

DESCRIPTION :
Reducer classique word-count : Hadoop Streaming trie et regroupe les
paires (clé, valeur) du mapper par clé avant de les transmettre ici —
il suffit de sommer les valeurs consécutives pour une même clé.

Portabilité : pas de f-strings ni de `from __future__ import annotations`
(PEP 563, Python 3.7+) — l'image Hadoop utilisée (Debian 9 stretch,
bde2020/hadoop-nodemanager) ne fournit que Python 3.5.
"""

import sys


def main():
    current_key = None
    current_count = 0

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        key, _, value = line.partition("\t")
        try:
            value = int(value)
        except ValueError:
            continue

        if key == current_key:
            current_count += value
        else:
            if current_key is not None:
                print("{0}\t{1}".format(current_key, current_count))
            current_key = key
            current_count = value

    if current_key is not None:
        print("{0}\t{1}".format(current_key, current_count))


if __name__ == "__main__":
    main()
