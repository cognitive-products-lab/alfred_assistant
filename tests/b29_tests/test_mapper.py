"""
PROJECT      : ALFRED
BLOCK        : B29
FUNCTION     : XX.XX
FILE         : tests/b29_tests/test_mapper.py
ROLE         : Tests unitaires — hadoop_poc/mapper.py

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-07-09
VERSION      : V1.0
STATUS       : VALIDATED
"""

from __future__ import annotations

import io
import json

from hadoop_poc import mapper


def _run_mapper(records: list[dict], capsys) -> list[str]:
    lines = "\n".join(json.dumps(r, ensure_ascii=False) for r in records)
    mapper.sys.stdin = io.StringIO(lines + "\n")
    mapper.main()
    out = capsys.readouterr().out.strip()
    return out.splitlines() if out else []


def test_mapper_api_access_key_format(capsys):
    output = _run_mapper(
        [{"log_type": "api_access", "date": "2026-07-09", "endpoint": "/api/chat", "result": "ALLOW"}],
        capsys,
    )
    assert output == ["api_access|2026-07-09|/api/chat|ALLOW\t1"]


def test_mapper_audit_trail_key_format(capsys):
    output = _run_mapper(
        [{"log_type": "audit_trail", "date": "2026-07-06", "action": "admin", "decision": "DENY_PERMISSION"}],
        capsys,
    )
    assert output == ["audit_trail|2026-07-06|admin|DENY_PERMISSION\t1"]


def test_mapper_soc_alerts_key_format(capsys):
    output = _run_mapper(
        [{"log_type": "soc_alerts", "date": "2026-05-31", "soc_level": "CRITICAL"}],
        capsys,
    )
    assert output == ["soc_alerts|2026-05-31|CRITICAL\t1"]


def test_mapper_unknown_log_type_uses_fallback(capsys):
    output = _run_mapper([{"log_type": "mystery", "date": "2026-07-09"}], capsys)
    assert output == ["mystery|2026-07-09|n/a\t1"]


def test_mapper_skips_blank_and_malformed_lines(capsys):
    mapper.sys.stdin = io.StringIO(
        '{"log_type": "api_access", "date": "2026-07-09", "endpoint": "/api/chat", "result": "ALLOW"}\n'
        "\n"
        "not json\n"
    )
    mapper.main()
    out = capsys.readouterr().out.strip().splitlines()
    assert out == ["api_access|2026-07-09|/api/chat|ALLOW\t1"]


def test_mapper_emits_one_line_per_input_record(capsys):
    output = _run_mapper(
        [
            {"log_type": "api_access", "date": "2026-07-09", "endpoint": "/api/chat", "result": "ALLOW"},
            {"log_type": "api_access", "date": "2026-07-09", "endpoint": "/api/chat", "result": "ALLOW"},
        ],
        capsys,
    )
    assert len(output) == 2
