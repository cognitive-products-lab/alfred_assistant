"""
PROJECT      : ALFRED
FILE         : tests/test_knowledge_p0.py
ROLE         : Tests P0 du chantier Knowledge/Training/Fine-Tuning — voir
               docs/architecture/vision_knowledge_training_finetuning_alfred.md

Couvre : knowledge_schema (métadonnées additives), le branchement dans
KnowledgeLoader, gap_dataset (journal JSONL des échecs locaux) et
knowledge_quality_gate (évaluation d'une connaissance candidate).
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


# ─────────────────────────────────────────────────────────
# knowledge_schema
# ─────────────────────────────────────────────────────────

class TestKnowledgeSchema:

    def test_import(self):
        from src.knowledge.knowledge_schema import normalize_knowledge_metadata
        assert normalize_knowledge_metadata is not None

    def test_defaults_on_empty_data(self):
        from src.knowledge.knowledge_schema import normalize_knowledge_metadata, DEFAULT_METADATA
        assert normalize_knowledge_metadata({}) == DEFAULT_METADATA

    def test_defaults_on_non_dict(self):
        from src.knowledge.knowledge_schema import normalize_knowledge_metadata, DEFAULT_METADATA
        assert normalize_knowledge_metadata(None) == DEFAULT_METADATA

    def test_status_default_is_validated(self):
        from src.knowledge.knowledge_schema import normalize_knowledge_metadata
        assert normalize_knowledge_metadata({})["status"] == "VALIDATED"

    def test_training_eligible_default_false(self):
        from src.knowledge.knowledge_schema import normalize_knowledge_metadata
        assert normalize_knowledge_metadata({})["training_eligible"] is False

    def test_explicit_provenance_field_overrides_default(self):
        from src.knowledge.knowledge_schema import normalize_knowledge_metadata
        meta = normalize_knowledge_metadata(
            {"provenance": {"source_type": "web", "confidence": 0.8}}
        )
        assert meta["source_type"] == "web"
        assert meta["confidence"] == 0.8

    def test_unrelated_data_keys_ignored(self):
        from src.knowledge.knowledge_schema import normalize_knowledge_metadata
        meta = normalize_knowledge_metadata({"title": "Une fiche", "tags": ["a", "b"]})
        assert "title" not in meta
        assert "tags" not in meta

    def test_top_level_status_never_read_as_lifecycle_status(self):
        """Régression : les fiches existantes ont leur propre data["status"]
        éditorial ("active"/"draft"...) — ne doit jamais fuiter dans
        metadata["status"] (cycle de vie VALIDATED/STALE/...)."""
        from src.knowledge.knowledge_schema import normalize_knowledge_metadata
        meta = normalize_knowledge_metadata({"status": "active"})
        assert meta["status"] == "VALIDATED"

    def test_provenance_must_be_dict_to_apply(self):
        from src.knowledge.knowledge_schema import normalize_knowledge_metadata, DEFAULT_METADATA
        meta = normalize_knowledge_metadata({"provenance": "not a dict"})
        assert meta == DEFAULT_METADATA


# ─────────────────────────────────────────────────────────
# KnowledgeLoader — branchement metadata
# ─────────────────────────────────────────────────────────

@pytest.fixture(scope="module")
def p0_loader():
    from src.knowledge.knowledge_loader import KnowledgeLoader
    return KnowledgeLoader(project_root=str(ROOT))


class TestKnowledgeLoaderMetadata:

    def test_every_indexed_item_has_metadata(self, p0_loader):
        assert p0_loader.knowledge_index
        for item in p0_loader.knowledge_index.values():
            assert "metadata" in item

    def test_metadata_has_expected_keys(self, p0_loader):
        from src.knowledge.knowledge_schema import DEFAULT_METADATA
        first_id = next(iter(p0_loader.knowledge_index))
        metadata = p0_loader.knowledge_index[first_id]["metadata"]
        assert set(metadata.keys()) == set(DEFAULT_METADATA.keys())

    def test_registry_status_untouched_by_metadata(self, p0_loader):
        # "status" registry (actif/existant, filtre de build_index) ne doit
        # jamais être confondu avec metadata["status"] (cycle de vie
        # VALIDATED/STALE/...).
        first_id = next(iter(p0_loader.knowledge_index))
        item = p0_loader.knowledge_index[first_id]
        assert item["status"] in ("active", "existing")
        assert item["metadata"]["status"] == "VALIDATED"


# ─────────────────────────────────────────────────────────
# gap_dataset
# ─────────────────────────────────────────────────────────

class TestGapDataset:

    @pytest.fixture
    def gap_module(self, tmp_path, monkeypatch):
        import src.knowledge.gap_dataset as gap_dataset
        monkeypatch.setattr(gap_dataset, "GAP_FILE", tmp_path / "gap_dataset.jsonl")
        monkeypatch.setattr(gap_dataset, "ARCHIVE_DIR", tmp_path / "archives")
        return gap_dataset

    def test_import(self, gap_module):
        assert gap_module.record_gap_event is not None

    def test_record_creates_file(self, gap_module):
        gap_module.record_gap_event(query="test", local_success=False)
        assert gap_module.GAP_FILE.exists()

    def test_record_returns_event_with_query(self, gap_module):
        event = gap_module.record_gap_event(query="pourquoi ça échoue ?", local_success=False)
        assert event["query"] == "pourquoi ça échoue ?"
        assert event["local_success"] is False
        assert "timestamp" in event

    def test_read_recent_gaps_roundtrip(self, gap_module):
        gap_module.record_gap_event(query="premier", local_success=False)
        gap_module.record_gap_event(query="second", local_success=False)
        events = gap_module.read_recent_gaps(limit=10)
        assert len(events) == 2
        assert events[-1]["query"] == "second"

    def test_read_recent_gaps_empty_when_no_file(self, gap_module):
        assert gap_module.read_recent_gaps() == []

    def test_read_recent_gaps_respects_limit(self, gap_module):
        for i in range(5):
            gap_module.record_gap_event(query=f"q{i}", local_success=False)
        events = gap_module.read_recent_gaps(limit=2)
        assert len(events) == 2
        assert events[-1]["query"] == "q4"

    def test_candidate_quality_persisted_when_provided(self, gap_module):
        quality = {"privacy_level": "STANDARD", "status": "TO_VERIFY", "training_eligible": False}
        gap_module.record_gap_event(
            query="test", local_success=False, external_source="openai",
            external_success=True, candidate_quality=quality,
        )
        events = gap_module.read_recent_gaps(limit=1)
        assert events[0]["candidate_quality"] == quality

    def test_candidate_quality_none_when_not_provided(self, gap_module):
        gap_module.record_gap_event(query="test", local_success=False)
        events = gap_module.read_recent_gaps(limit=1)
        assert events[0]["candidate_quality"] is None


# ─────────────────────────────────────────────────────────
# knowledge_quality_gate
# ─────────────────────────────────────────────────────────

class TestKnowledgeQualityGate:

    def test_import(self):
        from src.knowledge.knowledge_quality_gate import evaluate_candidate
        assert evaluate_candidate is not None

    def test_never_validated_at_acquisition(self):
        from src.knowledge.knowledge_quality_gate import evaluate_candidate
        result = evaluate_candidate("Explique-moi le RAG", "openai")
        assert result["status"] == "TO_VERIFY"

    def test_never_training_eligible_at_acquisition(self):
        from src.knowledge.knowledge_quality_gate import evaluate_candidate
        result = evaluate_candidate("Explique-moi le RAG", "openai")
        assert result["training_eligible"] is False

    def test_source_type_reflects_provider(self):
        from src.knowledge.knowledge_quality_gate import evaluate_candidate
        result = evaluate_candidate("une question", "anthropic")
        assert result["source_type"] == "anthropic"

    def test_privacy_level_standard_on_neutral_query(self):
        from src.knowledge.knowledge_quality_gate import evaluate_candidate
        result = evaluate_candidate("Comment fonctionne un moteur de recherche vectoriel ?", "openai")
        assert result["privacy_level"] == "STANDARD"

    def test_privacy_level_reflects_safety_gate_sensitivity(self, monkeypatch):
        import src.knowledge.knowledge_quality_gate as gate

        monkeypatch.setattr(
            gate, "assess_prompt_sensitivity",
            lambda text: {"privacy_level": "LOCAL_ONLY", "cloud_allowed": False, "matched_categories": ["health"]},
        )
        result = gate.evaluate_candidate("donnée sensible", "openai")
        assert result["privacy_level"] == "LOCAL_ONLY"


# ─────────────────────────────────────────────────────────
# response_generator — branchement Gap Dataset
# ─────────────────────────────────────────────────────────

class TestResponseGeneratorGapWiring:

    def test_no_gap_recorded_on_local_success(self, monkeypatch):
        from src.core.response_generator import ResponseGenerator

        recorded = []
        import src.knowledge.gap_dataset as gap_dataset
        monkeypatch.setattr(gap_dataset, "record_gap_event", lambda **kw: recorded.append(kw))

        class FakeLLM:
            last_provider = "ollama"

            def generate(self, system_prompt, user_prompt, **kwargs):
                return "réponse locale"

        gen = ResponseGenerator(llm_client=FakeLLM())
        gen.generate_response(user_message="Bonjour", response_context={"user": {"preferred_name": "Céline"}})

        assert recorded == []

    def test_gap_recorded_on_cloud_fallback_success(self, monkeypatch):
        from src.core.response_generator import ResponseGenerator

        recorded = []
        import src.knowledge.gap_dataset as gap_dataset
        monkeypatch.setattr(gap_dataset, "record_gap_event", lambda **kw: recorded.append(kw))
        monkeypatch.setattr(
            "src.knowledge.knowledge_quality_gate.evaluate_candidate",
            lambda query, source: {"status": "TO_VERIFY", "training_eligible": False,
                                    "privacy_level": "STANDARD", "source_type": source},
        )

        class FakeLLM:
            last_provider = "openai"

            def generate(self, system_prompt, user_prompt, **kwargs):
                return "réponse via cloud"

        gen = ResponseGenerator(llm_client=FakeLLM())
        gen.generate_response(user_message="question difficile", response_context={"user": {"preferred_name": "Céline"}})

        assert len(recorded) == 1
        assert recorded[0]["external_source"] == "openai"
        assert recorded[0]["external_success"] is True
        assert recorded[0]["candidate_quality"]["status"] == "TO_VERIFY"

    def test_gap_recorded_on_total_failure(self, monkeypatch):
        from src.core.response_generator import ResponseGenerator

        recorded = []
        import src.knowledge.gap_dataset as gap_dataset
        monkeypatch.setattr(gap_dataset, "record_gap_event", lambda **kw: recorded.append(kw))

        class FakeLLM:
            last_provider = "none"

            def generate(self, system_prompt, user_prompt, **kwargs):
                raise RuntimeError("aucun moteur disponible")

        gen = ResponseGenerator(llm_client=FakeLLM())
        gen.generate_response(user_message="question", response_context={"user": {"preferred_name": "Céline"}})

        assert len(recorded) == 1
        assert recorded[0]["external_success"] is False
        assert recorded[0]["candidate_quality"] is None

    def test_gap_logging_failure_does_not_break_response(self, monkeypatch):
        """La journalisation ne doit jamais faire planter la réponse à l'utilisateur."""
        from src.core.response_generator import ResponseGenerator

        import src.knowledge.gap_dataset as gap_dataset

        def _boom(**kw):
            raise OSError("disque plein")

        monkeypatch.setattr(gap_dataset, "record_gap_event", _boom)

        class FakeLLM:
            last_provider = "openai"

            def generate(self, system_prompt, user_prompt, **kwargs):
                return "réponse malgré tout"

        gen = ResponseGenerator(llm_client=FakeLLM())
        response = gen.generate_response(
            user_message="question", response_context={"user": {"preferred_name": "Céline"}}
        )
        assert "réponse malgré tout" in response
