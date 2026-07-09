"""
PROJECT      : ALFRED
BLOCK        : B29
FUNCTION     : XX.XX
FILE         : tests/b29_tests/test_reducer.py
ROLE         : Tests unitaires — hadoop_poc/reducer.py

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-07-09
VERSION      : V1.0
STATUS       : VALIDATED
"""

from __future__ import annotations

import io

from hadoop_poc import reducer


def _run_reducer(lines: list[str], capsys) -> list[str]:
    reducer.sys.stdin = io.StringIO("\n".join(lines) + "\n")
    reducer.main()
    out = capsys.readouterr().out.strip()
    return out.splitlines() if out else []


def test_reducer_sums_consecutive_same_key(capsys):
    output = _run_reducer(["a\t1", "a\t1", "a\t1"], capsys)
    assert output == ["a\t3"]


def test_reducer_groups_are_already_sorted_by_key(capsys):
    # Hadoop Streaming garantit le tri par clé avant le reducer — on
    # reproduit cette hypothèse (mêmes clés consécutives).
    output = _run_reducer(["a\t2", "a\t3", "b\t1"], capsys)
    assert output == ["a\t5", "b\t1"]


def test_reducer_single_key(capsys):
    output = _run_reducer(["x\t1"], capsys)
    assert output == ["x\t1"]


def test_reducer_ignores_blank_lines(capsys):
    output = _run_reducer(["a\t1", "", "a\t1"], capsys)
    assert output == ["a\t2"]


def test_reducer_ignores_non_numeric_value(capsys):
    output = _run_reducer(["a\t1", "a\tnot-a-number", "a\t1"], capsys)
    assert output == ["a\t2"]


def test_reducer_empty_input_emits_nothing(capsys):
    output = _run_reducer([], capsys)
    assert output == []
