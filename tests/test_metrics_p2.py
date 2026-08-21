"""
PROJECT      : ALFRED
FILE         : tests/test_metrics_p2.py
ROLE         : Tests KPI (Lean Six Sigma Define/Measure) — voir
               docs/architecture/vision_knowledge_training_finetuning_alfred.md

Couvre : request_log (dénominateur des taux), kpi_catalog (Define),
kpi_compute (Measure) et le branchement dans response_generator.py.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


# ─────────────────────────────────────────────────────────
# request_log
# ─────────────────────────────────────────────────────────

class TestRequestLog:

    @pytest.fixture
    def log(self, tmp_path, monkeypatch):
        import src.metrics.request_log as rl
        monkeypatch.setattr(rl, "REQUEST_LOG_FILE", tmp_path / "request_log.jsonl")
        monkeypatch.setattr(rl, "ARCHIVE_DIR", tmp_path / "archives")
        return rl

    def test_import(self, log):
        assert log.record_request is not None

    def test_record_creates_file(self, log):
        log.record_request(local_success=True, used_knowledge=False)
        assert log.REQUEST_LOG_FILE.exists()

    def test_record_never_stores_query_text(self, log):
        """Différence structurelle avec gap_dataset.py : aucun champ texte."""
        event = log.record_request(local_success=True, used_knowledge=True, route="focus")
        assert "query" not in event
        assert "text" not in event

    def test_count_requests(self, log):
        log.record_request(local_success=True, used_knowledge=False)
        log.record_request(local_success=False, used_knowledge=False, external_source="openai")
        assert log.count_requests() == 2

    def test_read_requests_roundtrip(self, log):
        log.record_request(local_success=True, used_knowledge=True)
        events = log.read_requests()
        assert len(events) == 1
        assert events[0]["local_success"] is True
        assert events[0]["used_knowledge"] is True

    def test_read_requests_respects_limit(self, log):
        for i in range(5):
            log.record_request(local_success=True, used_knowledge=False)
        assert len(log.read_requests(limit=2)) == 2

    def test_empty_log_returns_empty(self, log):
        assert log.read_requests() == []
        assert log.count_requests() == 0


# ─────────────────────────────────────────────────────────
# kpi_catalog (Define)
# ─────────────────────────────────────────────────────────

class TestKpiCatalog:

    def test_import(self):
        from src.metrics.kpi_catalog import KPI_CATALOG
        assert len(KPI_CATALOG) > 0

    def test_every_kpi_has_unique_id(self):
        from src.metrics.kpi_catalog import KPI_CATALOG
        ids = [k.kpi_id for k in KPI_CATALOG]
        assert len(ids) == len(set(ids))

    def test_every_kpi_has_valid_base_status(self):
        from src.metrics.kpi_catalog import KPI_CATALOG
        for kpi in KPI_CATALOG:
            assert kpi.base_status in ("OFF", "KO")

    def test_every_kpi_has_status_reason(self):
        from src.metrics.kpi_catalog import KPI_CATALOG
        for kpi in KPI_CATALOG:
            assert kpi.status_reason.strip() != ""

    def test_off_kpis_have_no_data_source_dependency_left_unresolved(self):
        """Un KPI OFF documente pourquoi, jamais un chiffre implicite."""
        from src.metrics.kpi_catalog import list_by_status
        off_kpis = list_by_status("OFF")
        assert len(off_kpis) > 0
        for kpi in off_kpis:
            assert kpi.status_reason.strip() != ""

    def test_get_kpi_returns_known_id(self):
        from src.metrics.kpi_catalog import get_kpi
        kpi = get_kpi("knowledge_reuse_rate")
        assert kpi is not None
        assert kpi.category == "Knowledge"

    def test_get_kpi_unknown_returns_none(self):
        from src.metrics.kpi_catalog import get_kpi
        assert get_kpi("bogus_kpi") is None

    def test_list_by_category(self):
        from src.metrics.kpi_catalog import list_by_category
        rag_kpis = list_by_category("RAG")
        assert len(rag_kpis) >= 4

    def test_finetuning_kpis_are_off(self):
        """Cohérent avec P3 : aucun entraînement réel n'a eu lieu."""
        from src.metrics.kpi_catalog import list_by_category
        for kpi in list_by_category("Fine-Tuning"):
            assert kpi.base_status == "OFF"

    def test_rag_recall_precision_are_ko_pending_ground_truth(self):
        """KO, pas OFF : l'infrastructure (relevant_knowledge_ids) existe,
        volume de cas labellisés insuffisant."""
        from src.metrics.kpi_catalog import get_kpi
        assert get_kpi("rag_recall_at_k").base_status == "KO"
        assert get_kpi("rag_precision_at_k").base_status == "KO"

    def test_rag_grounded_rate_stays_off(self):
        """Vrai blocage structurel : nécessite un jugement humain/LLM-judge,
        aucune vérité terrain ne le débloquerait."""
        from src.metrics.kpi_catalog import get_kpi
        assert get_kpi("rag_grounded_rate").base_status == "OFF"


# ─────────────────────────────────────────────────────────
# kpi_compute (Measure)
# ─────────────────────────────────────────────────────────

class TestKpiCompute:

    @pytest.fixture
    def env(self, tmp_path, monkeypatch):
        import src.metrics.request_log as rl
        import src.training.dataset_store as ds
        monkeypatch.setattr(rl, "REQUEST_LOG_FILE", tmp_path / "request_log.jsonl")
        monkeypatch.setattr(rl, "ARCHIVE_DIR", tmp_path / "archives")
        monkeypatch.setattr(ds, "TRAINING_ROOT", tmp_path / "training")
        return rl, ds

    def test_import(self, env):
        from src.metrics.kpi_compute import get_kpi_status_report
        assert get_kpi_status_report is not None

    def test_report_covers_full_catalog(self, env):
        from src.metrics.kpi_compute import get_kpi_status_report
        from src.metrics.kpi_catalog import KPI_CATALOG
        report = get_kpi_status_report()
        assert len(report) == len(KPI_CATALOG)

    def test_off_kpi_has_no_value(self, env):
        from src.metrics.kpi_compute import get_kpi_status_report
        report = {r["kpi_id"]: r for r in get_kpi_status_report()}
        assert report["rag_grounded_rate"]["status"] == "OFF"
        assert report["rag_grounded_rate"]["value"] is None

    def test_ko_stays_ko_below_sample_threshold(self, env):
        rl, _ = env
        rl.record_request(local_success=True, used_knowledge=False)
        from src.metrics.kpi_compute import get_kpi_status_report
        report = {r["kpi_id"]: r for r in get_kpi_status_report()}
        # min_sample_size=30, on n'a qu'1 échantillon
        assert report["external_call_rate"]["status"] == "KO"

    def test_ko_becomes_ok_above_sample_threshold(self, env):
        rl, _ = env
        for i in range(35):
            rl.record_request(local_success=(i % 2 == 0), used_knowledge=False)
        from src.metrics.kpi_compute import get_kpi_status_report
        report = {r["kpi_id"]: r for r in get_kpi_status_report()}
        assert report["external_call_rate"]["status"] == "OK"
        assert report["external_call_rate"]["value"] is not None

    def test_external_call_rate_value_correct(self, env):
        rl, _ = env
        for _ in range(30):
            rl.record_request(local_success=True, used_knowledge=False)
        for _ in range(10):
            rl.record_request(local_success=False, used_knowledge=False, external_source="openai")
        from src.metrics.kpi_compute import compute_external_call_rate
        rate, n = compute_external_call_rate()
        assert n == 40
        assert rate == pytest.approx(10 / 40)

    def test_knowledge_reuse_rate_value_correct(self, env):
        rl, _ = env
        for _ in range(20):
            rl.record_request(local_success=True, used_knowledge=True)
        for _ in range(10):
            rl.record_request(local_success=True, used_knowledge=False)
        from src.metrics.kpi_compute import compute_knowledge_reuse_rate
        rate, n = compute_knowledge_reuse_rate()
        assert n == 30
        assert rate == pytest.approx(20 / 30)

    def test_training_candidate_count_zero_when_empty(self, env):
        from src.metrics.kpi_compute import compute_training_candidate_count
        value, count = compute_training_candidate_count()
        assert value == 0.0

    def test_training_candidate_count_reflects_entries(self, env):
        _, ds = env
        ds.append_entry("instructions", {"instruction": "q", "response": "r"})
        ds.append_entry("preferences", {"prompt": "p"})
        from src.metrics.kpi_compute import compute_training_candidate_count
        value, _ = compute_training_candidate_count()
        assert value == 2.0

    def test_training_acceptance_rate_none_when_empty(self, env):
        from src.metrics.kpi_compute import compute_training_acceptance_rate
        rate, n = compute_training_acceptance_rate()
        assert rate is None

    def test_training_acceptance_rate_computed(self, env):
        _, ds = env
        ds.append_entry("instructions", {"instruction": "q1", "training_eligible": True})
        ds.append_entry("instructions", {"instruction": "q2", "training_eligible": False})
        from src.metrics.kpi_compute import compute_training_acceptance_rate
        rate, n = compute_training_acceptance_rate()
        assert n == 2
        assert rate == pytest.approx(0.5)

    def test_training_duplicate_rate_computed(self, env):
        _, ds = env
        ds.append_entry("instructions", {"instruction": "q1", "duplicate_score": 0.2})
        ds.append_entry("instructions", {"instruction": "q2", "duplicate_score": 0.8})
        from src.metrics.kpi_compute import compute_training_duplicate_rate
        rate, n = compute_training_duplicate_rate()
        assert rate == pytest.approx(0.5)

    def test_stale_knowledge_rate_computable_on_real_corpus(self, env):
        """N'a pas besoin de volume d'usage — le corpus réel existe déjà."""
        from src.metrics.kpi_compute import compute_rag_stale_knowledge_rate
        rate, total = compute_rag_stale_knowledge_rate()
        assert total > 0
        assert rate == 0.0  # toutes les fiches réelles sont STATIC (knowledge_schema.py)

    def test_dataset_size_by_version_empty(self, env):
        from src.metrics.kpi_compute import compute_training_dataset_size_by_version
        sizes, total_versions = compute_training_dataset_size_by_version()
        assert total_versions == 0
        assert sizes == {"instructions": {}, "preferences": {}}

    def test_dataset_size_by_version_reflects_bump(self, env):
        _, ds = env
        ds.append_entry("instructions", {"instruction": "q"})
        ds.bump_version("instructions", "v0.1")
        from src.metrics.kpi_compute import compute_training_dataset_size_by_version
        sizes, total_versions = compute_training_dataset_size_by_version()
        assert sizes["instructions"]["v0.1"] == 1
        assert total_versions == 1


# ─────────────────────────────────────────────────────────
# response_generator — branchement request_log
# ─────────────────────────────────────────────────────────

class TestResponseGeneratorRequestMetricWiring:

    def test_metric_recorded_on_local_success(self, monkeypatch):
        from src.core.response_generator import ResponseGenerator

        recorded = []
        import src.metrics.request_log as rl
        monkeypatch.setattr(rl, "record_request", lambda **kw: recorded.append(kw))

        class FakeLLM:
            last_provider = "ollama"

            def generate(self, system_prompt, user_prompt, **kwargs):
                return "réponse locale"

        gen = ResponseGenerator(llm_client=FakeLLM())
        gen.generate_response(user_message="Bonjour", response_context={"user": {"preferred_name": "Céline"}})

        assert len(recorded) == 1
        assert recorded[0]["local_success"] is True
        assert recorded[0]["external_source"] is None

    def test_metric_recorded_on_cloud_fallback(self, monkeypatch):
        from src.core.response_generator import ResponseGenerator

        recorded = []
        import src.metrics.request_log as rl
        monkeypatch.setattr(rl, "record_request", lambda **kw: recorded.append(kw))
        # Empêche gap_dataset/knowledge_candidates de vraiment écrire.
        import src.knowledge.gap_dataset as gap_dataset
        monkeypatch.setattr(gap_dataset, "record_gap_event", lambda **kw: None)
        monkeypatch.setattr(
            "src.knowledge.knowledge_quality_gate.evaluate_candidate",
            lambda query, source: {"status": "TO_VERIFY", "training_eligible": False, "privacy_level": "STANDARD"},
        )
        monkeypatch.setattr(
            "src.knowledge.knowledge_candidates.record_candidate",
            lambda **kw: "cand_fake",
        )

        class FakeLLM:
            last_provider = "openai"

            def generate(self, system_prompt, user_prompt, **kwargs):
                return "réponse cloud"

        gen = ResponseGenerator(llm_client=FakeLLM())
        gen.generate_response(user_message="question", response_context={"user": {"preferred_name": "Céline"}})

        assert len(recorded) == 1
        assert recorded[0]["local_success"] is False
        assert recorded[0]["external_source"] == "openai"

    def test_metric_uses_knowledge_ids_presence(self, monkeypatch):
        from src.core.response_generator import ResponseGenerator

        recorded = []
        import src.metrics.request_log as rl
        monkeypatch.setattr(rl, "record_request", lambda **kw: recorded.append(kw))

        class FakeLLM:
            last_provider = "ollama"

            def generate(self, system_prompt, user_prompt, **kwargs):
                return "réponse"

        gen = ResponseGenerator(llm_client=FakeLLM())
        gen.generate_response(
            user_message="question",
            response_context={"user": {"preferred_name": "Céline"}, "knowledge_ids": ["a.b.c"]},
        )

        assert recorded[0]["used_knowledge"] is True

    def test_metric_logging_failure_does_not_break_response(self, monkeypatch):
        from src.core.response_generator import ResponseGenerator

        import src.metrics.request_log as rl

        def _boom(**kw):
            raise OSError("disque plein")

        monkeypatch.setattr(rl, "record_request", _boom)

        class FakeLLM:
            last_provider = "ollama"

            def generate(self, system_prompt, user_prompt, **kwargs):
                return "réponse malgré tout"

        gen = ResponseGenerator(llm_client=FakeLLM())
        response = gen.generate_response(
            user_message="question", response_context={"user": {"preferred_name": "Céline"}}
        )
        assert "réponse malgré tout" in response


# ─────────────────────────────────────────────────────────
# rag_evaluation
# ─────────────────────────────────────────────────────────

class TestRagEvaluation:

    @pytest.fixture
    def golden(self, tmp_path, monkeypatch):
        import src.training.golden_dataset as gd
        monkeypatch.setattr(gd, "GOLDEN_PATH", tmp_path / "golden_dataset.json")
        return gd

    def test_import(self, golden):
        from src.metrics.rag_evaluation import compute_recall_precision_at_k
        assert compute_recall_precision_at_k is not None

    def test_no_labeled_cases_returns_none(self, golden):
        from src.metrics.rag_evaluation import compute_recall_precision_at_k
        golden.add_golden_case(prompt="p", category="rag", expected_behavior="e")  # non labellisé
        result = compute_recall_precision_at_k(retriever=lambda p: ["x"])
        assert result["recall_at_k"] is None
        assert result["precision_at_k"] is None
        assert result["labeled_cases"] == 0

    def test_perfect_retrieval_scores_1(self, golden):
        from src.metrics.rag_evaluation import compute_recall_precision_at_k
        golden.add_golden_case(
            prompt="Explique le RAG", category="rag", expected_behavior="e",
            relevant_knowledge_ids=["a.b.c"],
        )
        result = compute_recall_precision_at_k(retriever=lambda p: ["a.b.c"], k=5)
        assert result["recall_at_k"] == pytest.approx(1.0)
        assert result["precision_at_k"] == pytest.approx(1.0)
        assert result["labeled_cases"] == 1

    def test_missed_retrieval_scores_0(self, golden):
        from src.metrics.rag_evaluation import compute_recall_precision_at_k
        golden.add_golden_case(
            prompt="p", category="rag", expected_behavior="e",
            relevant_knowledge_ids=["a.b.c"],
        )
        result = compute_recall_precision_at_k(retriever=lambda p: ["x.y.z"], k=5)
        assert result["recall_at_k"] == pytest.approx(0.0)
        assert result["precision_at_k"] == pytest.approx(0.0)

    def test_partial_retrieval(self, golden):
        from src.metrics.rag_evaluation import compute_recall_precision_at_k
        golden.add_golden_case(
            prompt="p", category="rag", expected_behavior="e",
            relevant_knowledge_ids=["a", "b"],  # 2 pertinentes
        )
        result = compute_recall_precision_at_k(retriever=lambda p: ["a", "x", "y"], k=3)
        assert result["recall_at_k"] == pytest.approx(0.5)  # 1/2 pertinentes trouvées
        assert result["precision_at_k"] == pytest.approx(1 / 3)  # 1/3 retournées pertinentes

    def test_k_limits_retrieved_window(self, golden):
        from src.metrics.rag_evaluation import compute_recall_precision_at_k
        golden.add_golden_case(
            prompt="p", category="rag", expected_behavior="e",
            relevant_knowledge_ids=["a"],
        )
        # "a" est en 3e position, hors du top-2
        result = compute_recall_precision_at_k(retriever=lambda p: ["x", "y", "a"], k=2)
        assert result["recall_at_k"] == pytest.approx(0.0)

    def test_unlabeled_cases_excluded_from_average(self, golden):
        from src.metrics.rag_evaluation import compute_recall_precision_at_k
        golden.add_golden_case(prompt="p1", category="rag", expected_behavior="e")  # non labellisé
        golden.add_golden_case(
            prompt="p2", category="rag", expected_behavior="e",
            relevant_knowledge_ids=["a"],
        )
        result = compute_recall_precision_at_k(retriever=lambda p: ["a"], k=5)
        assert result["labeled_cases"] == 1

    def test_category_filter(self, golden):
        from src.metrics.rag_evaluation import compute_recall_precision_at_k
        golden.add_golden_case(
            prompt="p1", category="rag", expected_behavior="e", relevant_knowledge_ids=["a"],
        )
        golden.add_golden_case(
            prompt="p2", category="privacy", expected_behavior="e", relevant_knowledge_ids=["b"],
        )
        result = compute_recall_precision_at_k(retriever=lambda p: ["a"], k=5, category="rag")
        assert result["labeled_cases"] == 1


class TestKpiComputeRagRecallPrecision:

    @pytest.fixture
    def golden(self, tmp_path, monkeypatch):
        import src.training.golden_dataset as gd
        monkeypatch.setattr(gd, "GOLDEN_PATH", tmp_path / "golden_dataset.json")
        return gd

    def test_recall_at_k_none_without_labeled_cases(self, golden):
        from src.metrics.kpi_compute import compute_rag_recall_at_k
        value, n = compute_rag_recall_at_k()
        assert value is None
        assert n == 0

    def test_report_shows_ko_without_labeled_cases(self, golden):
        from src.metrics.kpi_compute import get_kpi_status_report
        report = {r["kpi_id"]: r for r in get_kpi_status_report()}
        assert report["rag_recall_at_k"]["status"] == "KO"
        assert report["rag_precision_at_k"]["status"] == "KO"
