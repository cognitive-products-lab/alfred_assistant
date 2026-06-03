"""
PROJECT      : ALFRED
BLOCK        : B20
FUNCTION     : 20.15
FILE         : tests/security_tests/test_html_report.py
ROLE         : Tests unitaires html_report.py
AUTHOR       : Cognitive Products Lab
CREATED      : 2026-06-01
VERSION      : V1.0
STATUS       : ACTIVE
"""
import tempfile
from pathlib import Path
import pytest
from src.security.html_report import generate_html_report


def test_generate_returns_path():
    with tempfile.TemporaryDirectory() as tmp:
        result = generate_html_report(output_path=Path(tmp) / "report.html")
        assert isinstance(result, Path)

def test_generated_file_exists():
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / "report.html"
        generate_html_report(output_path=out)
        assert out.exists()

def test_generated_file_not_empty():
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / "report.html"
        generate_html_report(output_path=out)
        assert out.stat().st_size > 100

def test_generated_contains_html():
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / "report.html"
        generate_html_report(output_path=out)
        content = out.read_text(encoding="utf-8", errors="replace")
        assert "<html" in content.lower() or "<!doctype" in content.lower()

def test_generate_without_path_returns_path():
    result = generate_html_report()
    assert isinstance(result, Path)
