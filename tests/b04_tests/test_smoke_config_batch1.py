"""
PROJECT      : ALFRED
BLOCK        : B04
FUNCTION     : SMOKE
FILE         : tests/b04_tests/test_smoke_config_batch1.py
ROLE         : Smoke tests (lot 1) pour les fichiers de configuration/securite
               B04 sans couverture de test (.env.example, .gitignore,
               pyproject.toml, config ethics/settings, knowledge ethique).

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-07-05
UPDATED      : 2026-07-05
VERSION      : V1.0
STATUS       : TESTED

DESCRIPTION :
Verifie la structure/coherence des fichiers de configuration projet,
notamment que .env est bien ignore par Git (point de securite) et que
.env.example expose les cles attendues par le code.
"""

import json
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def _parse_env_example(text: str) -> dict:
    env = {}
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if "=" in stripped:
            key, _, value = stripped.partition("=")
            env[key.strip()] = value.strip()
    return env


def test_env_example_has_expected_keys():
    text = (ROOT / ".env.example").read_text(encoding="utf-8-sig")
    env = _parse_env_example(text)
    expected_keys = {
        "APP_ENV", "API_HOST", "SESSION_TIMEOUT", "MAX_LOGIN_ATTEMPTS",
        "FERNET_KEY", "SECRET_KEY", "PIN_SALT",
    }
    missing = expected_keys - env.keys()
    assert not missing, f"clés manquantes dans .env.example : {missing}"


def test_gitignore_blocks_env_and_secrets():
    text = (ROOT / ".gitignore").read_text(encoding="utf-8")
    lines = {line.strip() for line in text.splitlines()}
    assert ".env" in lines, ".env doit être ignoré par Git (fichier de secrets)"
    assert "__pycache__/" in lines


def test_pyproject_toml_is_valid_and_has_pytest_config():
    with (ROOT / "pyproject.toml").open("rb") as f:
        data = tomllib.load(f)
    assert data["project"]["name"] == "alfred"
    assert data["tool"]["pytest"]["ini_options"]["testpaths"] == ["tests"]


def test_ethics_rules_json_is_valid_structure():
    data = json.loads((ROOT / "config" / "ethics_rules.json").read_text(encoding="utf-8"))
    assert "rules" in data
    assert isinstance(data["rules"], list)


def test_settings_json_has_expected_keys():
    data = json.loads((ROOT / "config" / "settings.json").read_text(encoding="utf-8"))
    for key in ("app_env", "api_host", "session_timeout"):
        assert key in data


def test_ethical_framework_json_structure():
    data = json.loads(
        (ROOT / "knowledges" / "system" / "ethics" / "ethical_framework.json").read_text(encoding="utf-8")
    )
    for key in ("metadata", "core_philosophy", "foundational_principles", "prohibited_behaviors"):
        assert key in data
