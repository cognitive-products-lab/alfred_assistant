"""
PROJECT      : ALFRED
BLOCK        : B29
FUNCTION     : XX.XX
FILE         : tests/b29_tests/test_run_hadoop_poc.py
ROLE         : Tests unitaires — scripts/run_hadoop_poc.py

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-07-09
VERSION      : V1.0
STATUS       : VALIDATED

Les appels Docker/HDFS réels ne sont pas exécutés ici (subprocess.run
mocké) — ce module teste la logique d'orchestration (garde-fou "pas de
données", propagation du code retour) indépendamment de l'infrastructure.
Le run réel de bout en bout est couvert manuellement (cf.
docs/hadoop_poc_bilan.md).
"""

from __future__ import annotations

import subprocess

import pytest

from scripts import run_hadoop_poc as poc


def test_run_prints_stdout_on_success(monkeypatch, capsys):
    monkeypatch.setattr(
        poc.subprocess, "run",
        lambda cmd, capture_output, text: subprocess.CompletedProcess(cmd, 0, stdout="ok\n", stderr=""),
    )
    result = poc.run(["echo", "ok"])
    assert result.returncode == 0
    assert "ok" in capsys.readouterr().out


def test_run_exits_on_failure_when_check_true(monkeypatch):
    monkeypatch.setattr(
        poc.subprocess, "run",
        lambda cmd, capture_output, text: subprocess.CompletedProcess(cmd, 1, stdout="", stderr="boom"),
    )
    with pytest.raises(SystemExit) as exc_info:
        poc.run(["false"])
    assert exc_info.value.code == 1


def test_run_does_not_exit_on_failure_when_check_false(monkeypatch):
    monkeypatch.setattr(
        poc.subprocess, "run",
        lambda cmd, capture_output, text: subprocess.CompletedProcess(cmd, 1, stdout="", stderr="boom"),
    )
    result = poc.run(["false"], check=False)
    assert result.returncode == 1


def test_main_aborts_when_no_anonymized_data(tmp_path, monkeypatch):
    monkeypatch.setattr(poc, "INPUT_DIR", tmp_path / "empty_input")
    (tmp_path / "empty_input").mkdir()

    with pytest.raises(SystemExit) as exc_info:
        poc.main()
    assert exc_info.value.code == 1


def test_main_does_not_abort_when_data_present(tmp_path, monkeypatch):
    input_dir = tmp_path / "input"
    input_dir.mkdir()
    (input_dir / "api_access.jsonl").write_text("{}\n", encoding="utf-8")
    monkeypatch.setattr(poc, "INPUT_DIR", input_dir)
    monkeypatch.setattr(poc, "OUTPUT_DIR", tmp_path / "output")

    calls: list[list[str]] = []
    monkeypatch.setattr(
        poc, "run",
        lambda cmd, check=True: (calls.append(cmd), subprocess.CompletedProcess(cmd, 0, stdout="", stderr=""))[1],
    )

    poc.main()
    assert len(calls) > 0
