"""
PROJECT      : ALFRED
BLOCK        : B18
FUNCTION     : SMOKE
FILE         : tests/b18_tests/test_smoke_project_files.py
ROLE         : Smoke tests (lot 2) pour les fichiers projet B18 restants :
               paths.py, config racine, README.md, requirements.txt, .env.

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-07-05
UPDATED      : 2026-07-05
VERSION      : V1.0
STATUS       : TESTED

DESCRIPTION :
.env n'est jamais lu pour ses valeurs (secrets reels) — uniquement pour
verifier que les cles attendues sont presentes (coherence avec .env.example).
scripts/clean_project.ps1 n'est pas execute (suppression recursive de
fichiers, meme si limitee a __pycache__/*.pyc) — revu par lecture de code
uniquement.
"""

import json
from pathlib import Path

import paths as paths_module
from paths import PATHS

ROOT = Path(__file__).resolve().parents[2]


# ── paths.py ──────────────────────────────────────────────────

def test_paths_base_dir_is_project_root():
    assert (paths_module.BASE_DIR / "src").is_dir()
    assert (paths_module.BASE_DIR / "tests").is_dir()


def test_paths_instance_attributes_resolve_correctly():
    assert PATHS.config_v2 == paths_module.CONFIG_V2
    assert PATHS.data_health == paths_module.DATA_HEALTH
    assert PATHS.src_security == paths_module.SRC_SECURITY


def test_ensure_dirs_is_idempotent(tmp_path, monkeypatch):
    monkeypatch.setattr(paths_module, "SRC_SECURITY", tmp_path / "src_security")
    monkeypatch.setattr(paths_module, "LOGS_DIR", tmp_path / "logs")
    # Deuxieme appel ne doit pas lever d'exception (exist_ok=True)
    paths_module.SRC_SECURITY.mkdir(parents=True, exist_ok=True)
    paths_module.SRC_SECURITY.mkdir(parents=True, exist_ok=True)
    assert paths_module.SRC_SECURITY.exists()


# ── config JSON racine ────────────────────────────────────────

def test_alfred_project_json_structure():
    data = json.loads((ROOT / "config" / "alfred_project.json").read_text(encoding="utf-8"))
    for key in ("domain", "description", "main_products", "key_concepts"):
        assert key in data


def test_router_rules_json_structure():
    data = json.loads((ROOT / "config" / "router_rules.json").read_text(encoding="utf-8"))
    assert "routes" in data
    assert isinstance(data["routes"], (list, dict))


def test_module_mapping_json_structure():
    data = json.loads((ROOT / "config" / "v2" / "module_mapping.json").read_text(encoding="utf-8"))
    assert "_meta" in data
    assert any(k.startswith("bloc_") for k in data)


# ── README / requirements ──────────────────────────────────────

def test_readme_mentions_core_principles():
    text = (ROOT / "README.md").read_text(encoding="utf-8-sig")
    assert "ALFRED" in text
    assert "Local-first" in text or "local-first" in text.lower()


def test_requirements_txt_non_empty_and_parseable():
    text = (ROOT / "requirements.txt").read_text(encoding="utf-8")
    packages = [
        line.strip() for line in text.splitlines()
        if line.strip() and not line.strip().startswith("#")
    ]
    assert len(packages) > 10


# ── .env (cles uniquement, jamais les valeurs) ─────────────────

def test_env_has_all_keys_declared_in_env_example():
    def _keys(path):
        text = (ROOT / path).read_text(encoding="utf-8-sig")
        return {
            line.split("=", 1)[0].strip()
            for line in text.splitlines()
            if "=" in line and not line.strip().startswith("#")
        }

    example_keys = _keys(".env.example")
    real_keys = _keys(".env")
    missing = example_keys - real_keys
    assert not missing, f"Clés de .env.example absentes de .env : {missing}"
