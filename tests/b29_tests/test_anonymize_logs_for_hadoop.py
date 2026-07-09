"""
PROJECT      : ALFRED
BLOCK        : B29
FUNCTION     : XX.XX
FILE         : tests/b29_tests/test_anonymize_logs_for_hadoop.py
ROLE         : Tests unitaires — scripts/anonymize_logs_for_hadoop.py

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-07-09
VERSION      : V1.0
STATUS       : VALIDATED
"""

from __future__ import annotations

import json

from scripts import anonymize_logs_for_hadoop as anon


def _write_jsonl(path, records: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


def test_day_truncates_timestamp():
    assert anon._day("2026-07-09T12:34:56.789+00:00") == "2026-07-09"


def test_day_handles_missing_timestamp():
    assert anon._day("") == "unknown"


def test_anonymize_file_drops_identifiers_and_tags_log_type(tmp_path, monkeypatch):
    monkeypatch.setattr(anon, "LOGS_DIR", tmp_path / "logs")
    monkeypatch.setattr(anon, "OUTPUT_DIR", tmp_path / "out")
    (tmp_path / "out").mkdir(parents=True)

    _write_jsonl(
        tmp_path / "logs" / "audit_trail.jsonl",
        [
            {
                "timestamp": "2026-07-06T16:43:02.462985+00:00",
                "user_id": "guest",
                "device_id": "abc123",
                "request_id": "req-42",
                "action": "admin",
                "resource": "alfred_core",
                "decision": "DENY_PERMISSION",
                "role": "",
                "risk_score": 30,
            }
        ],
    )

    count = anon.anonymize_file("audit_trail.jsonl", anon._SOURCES["audit_trail.jsonl"]["keep"])
    assert count == 1

    out_lines = (tmp_path / "out" / "audit_trail.jsonl").read_text(encoding="utf-8").splitlines()
    record = json.loads(out_lines[0])

    assert record == {
        "log_type": "audit_trail",
        "date": "2026-07-06",
        "action": "admin",
        "resource": "alfred_core",
        "decision": "DENY_PERMISSION",
        "role": "",
        "risk_score": 30,
    }
    # Identifiants directs/quasi-directs bien supprimés (minimisation RGPD)
    assert "user_id" not in record
    assert "device_id" not in record
    assert "request_id" not in record


def test_anonymize_file_soc_alerts_own_source_field_not_overwritten(tmp_path, monkeypatch):
    """Régression : soc_alerts.jsonl a son propre champ "source" (ex.
    "incident_correlation") qui ne doit pas être écrasé par l'étiquette
    de provenance du fichier (log_type)."""
    monkeypatch.setattr(anon, "LOGS_DIR", tmp_path / "logs")
    monkeypatch.setattr(anon, "OUTPUT_DIR", tmp_path / "out")
    (tmp_path / "out").mkdir(parents=True)

    _write_jsonl(
        tmp_path / "logs" / "soc_alerts.jsonl",
        [
            {
                "source": "incident_correlation",
                "level": "CRITICAL",
                "message": "texte libre à ne pas conserver",
                "soc_score": 381,
                "soc_level": "CRITICAL",
                "timestamp": "2026-05-31T10:00:00+00:00",
            }
        ],
    )

    anon.anonymize_file("soc_alerts.jsonl", anon._SOURCES["soc_alerts.jsonl"]["keep"])
    record = json.loads((tmp_path / "out" / "soc_alerts.jsonl").read_text(encoding="utf-8"))

    assert record["log_type"] == "soc_alerts"
    assert record["source"] == "incident_correlation"
    assert "message" not in record


def test_anonymize_file_skips_malformed_lines(tmp_path, monkeypatch):
    monkeypatch.setattr(anon, "LOGS_DIR", tmp_path / "logs")
    monkeypatch.setattr(anon, "OUTPUT_DIR", tmp_path / "out")
    (tmp_path / "out").mkdir(parents=True)

    log_path = tmp_path / "logs" / "api_access.jsonl"
    log_path.parent.mkdir(parents=True)
    log_path.write_text(
        '{"timestamp": "2026-07-09T00:00:00+00:00", "endpoint": "/api/chat", '
        '"role": "OWNER", "result": "ALLOW"}\n'
        "not valid json\n"
        "\n",
        encoding="utf-8",
    )

    count = anon.anonymize_file("api_access.jsonl", anon._SOURCES["api_access.jsonl"]["keep"])
    assert count == 1


def test_anonymize_file_missing_source_returns_zero(tmp_path, monkeypatch):
    monkeypatch.setattr(anon, "LOGS_DIR", tmp_path / "logs")
    monkeypatch.setattr(anon, "OUTPUT_DIR", tmp_path / "out")
    (tmp_path / "out").mkdir(parents=True)

    count = anon.anonymize_file("api_access.jsonl", anon._SOURCES["api_access.jsonl"]["keep"])
    assert count == 0


def test_main_processes_all_sources(tmp_path, monkeypatch):
    monkeypatch.setattr(anon, "LOGS_DIR", tmp_path / "logs")
    monkeypatch.setattr(anon, "OUTPUT_DIR", tmp_path / "out")

    _write_jsonl(
        tmp_path / "logs" / "api_access.jsonl",
        [{"timestamp": "2026-07-09T00:00:00+00:00", "endpoint": "/api/chat",
          "role": "OWNER", "result": "ALLOW"}],
    )

    anon.main()

    assert (tmp_path / "out").is_dir()
    assert (tmp_path / "out" / "api_access.jsonl").is_file()
