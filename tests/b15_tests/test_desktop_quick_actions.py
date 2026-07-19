"""
PROJECT      : ALFRED
BLOCK        : B15
FUNCTION     : 15.14
FILE         : tests/b15_tests/test_desktop_quick_actions.py
ROLE         : Tests unitaires src/ui/desktop_quick_actions.py

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-07-19
VERSION      : V1.0
STATUS       : TESTED

DESCRIPTION :
Actions rapides du dashboard : sauvegarde à la demande (backup_security.py
monkeypatché, aucune écriture disque réelle), résumé du jour (episodic_memory
+ reminder_engine + wellbeing_tracker monkeypatchés), recherche connaissances
(KnowledgeRetrievalEngine monkeypatché).
"""

import types
from datetime import datetime

import pytest

import src.main as main_module
from src.ui import desktop_quick_actions as qa


# =============================================================================
# run_backup
# =============================================================================

def test_run_backup_returns_error_when_no_files_exist(monkeypatch, tmp_path):
    from paths import PATHS
    monkeypatch.setattr(PATHS, "data", tmp_path / "data")  # aucun fichier cible n'existe
    result = qa.run_backup()
    assert result["ok"] is False
    assert "Aucun fichier" in result["error"]


def test_run_backup_calls_backup_many_with_existing_files(monkeypatch, tmp_path):
    from paths import PATHS
    data_dir = tmp_path / "data"
    profile_dir = data_dir / "profile"
    profile_dir.mkdir(parents=True)
    (profile_dir / "identity_celine.json").write_text("{}", encoding="utf-8")
    monkeypatch.setattr(PATHS, "data", data_dir)

    captured = {}

    def fake_backup_many(paths, label=""):
        captured["paths"] = paths
        captured["label"] = label
        return {"success": [{"source": paths[0], "backup": "x"}], "errors": []}

    monkeypatch.setattr("src.security.backup_security.backup_many", fake_backup_many)
    result = qa.run_backup()

    assert result == {"ok": True, "backed_up": 1, "errors": []}
    assert len(captured["paths"]) == 1
    assert captured["label"] == "dashboard_manuel"


def test_run_backup_reports_partial_errors(monkeypatch, tmp_path):
    from paths import PATHS
    data_dir = tmp_path / "data"
    profile_dir = data_dir / "profile"
    profile_dir.mkdir(parents=True)
    (profile_dir / "identity_celine.json").write_text("{}", encoding="utf-8")
    monkeypatch.setattr(PATHS, "data", data_dir)

    monkeypatch.setattr(
        "src.security.backup_security.backup_many",
        lambda paths, label="": {"success": [], "errors": [{"source": paths[0], "error": "disque plein"}]},
    )
    result = qa.run_backup()
    assert result["ok"] is False
    assert result["errors"] == ["disque plein"]


# =============================================================================
# summarize_today
# =============================================================================

def test_summarize_today_with_no_activity(monkeypatch):
    monkeypatch.setattr("src.memory.episodic_memory.get_timeline", lambda limit=50: [])
    monkeypatch.setattr(main_module, "get_live_components", lambda: None)
    monkeypatch.setattr(
        "src.regulation.wellbeing_tracker.get_daily_energy_summary",
        lambda: {"dominant": "unknown"},
    )
    result = qa.summarize_today()
    assert result["ok"] is True
    assert result["episode_count"] == 0
    assert "Aucun échange notable" in result["summary"]


def test_summarize_today_includes_todays_episodes_only(monkeypatch):
    today = datetime.now().date().isoformat()
    episodes = [
        {"created_at": f"{today}T09:00:00", "title": "Échange du matin"},
        {"created_at": "2020-01-01T09:00:00", "title": "Vieux souvenir"},
    ]
    monkeypatch.setattr("src.memory.episodic_memory.get_timeline", lambda limit=50: episodes)
    monkeypatch.setattr(main_module, "get_live_components", lambda: None)
    monkeypatch.setattr(
        "src.regulation.wellbeing_tracker.get_daily_energy_summary",
        lambda: {"dominant": "unknown"},
    )
    result = qa.summarize_today()
    assert result["episode_count"] == 1
    assert "Échange du matin" in result["summary"]
    assert "Vieux souvenir" not in result["summary"]


def test_summarize_today_includes_energy_when_known(monkeypatch):
    monkeypatch.setattr("src.memory.episodic_memory.get_timeline", lambda limit=50: [])
    monkeypatch.setattr(main_module, "get_live_components", lambda: None)
    monkeypatch.setattr(
        "src.regulation.wellbeing_tracker.get_daily_energy_summary",
        lambda: {"dominant": "high"},
    )
    result = qa.summarize_today()
    assert "high" in result["summary"]


# =============================================================================
# search_knowledge
# =============================================================================

def test_search_knowledge_rejects_empty_query():
    result = qa.search_knowledge("   ")
    assert result["ok"] is False


def test_search_knowledge_maps_ranked_results(monkeypatch):
    ranked = types.SimpleNamespace(
        knowledge_id="k1",
        score=0.87,
        data={"title": "RGPD et données de santé", "summary": "Un résumé assez long. " * 20},
    )
    retrieval_result = types.SimpleNamespace(ranked_knowledge=[ranked])
    fake_engine = types.SimpleNamespace(retrieve=lambda query, user_id="": retrieval_result)

    monkeypatch.setattr(
        "src.knowledge.retrieval_engine.KnowledgeRetrievalEngine",
        lambda: fake_engine,
    )
    result = qa.search_knowledge("rgpd santé")

    assert result["ok"] is True
    assert result["results"][0]["id"] == "k1"
    assert result["results"][0]["title"] == "RGPD et données de santé"
    assert len(result["results"][0]["summary"]) <= 200
    assert result["results"][0]["score"] == 0.87


def test_search_knowledge_handles_engine_exception(monkeypatch):
    def _boom():
        raise RuntimeError("index indisponible")

    monkeypatch.setattr("src.knowledge.retrieval_engine.KnowledgeRetrievalEngine", _boom)
    result = qa.search_knowledge("test")
    assert result["ok"] is False
    assert "index indisponible" in result["error"]
