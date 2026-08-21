"""
PROJECT      : ALFRED
FILE         : tests/test_knowledge_p0.py
ROLE         : Tests P0 du chantier Knowledge/Training/Fine-Tuning — voir
               docs/architecture/vision_knowledge_training_finetuning_alfred.md

Couvre : knowledge_schema (métadonnées additives), le branchement dans
KnowledgeLoader, gap_dataset (journal JSONL des échecs locaux),
knowledge_quality_gate (évaluation d'une connaissance candidate),
knowledge_candidates (stockage du contenu réel, filtré par confidentialité)
et gap_curation (promotion manuelle vers une vraie fiche knowledge).
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
        monkeypatch.setattr(
            "src.knowledge.knowledge_candidates.record_candidate",
            lambda **kw: "cand_fake123",
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
        assert recorded[0]["candidate_id"] == "cand_fake123"

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
        monkeypatch.setattr(
            "src.knowledge.knowledge_candidates.record_candidate",
            lambda **kw: "cand_fake",
        )

        class FakeLLM:
            last_provider = "openai"

            def generate(self, system_prompt, user_prompt, **kwargs):
                return "réponse malgré tout"

        gen = ResponseGenerator(llm_client=FakeLLM())
        response = gen.generate_response(
            user_message="question", response_context={"user": {"preferred_name": "Céline"}}
        )
        assert "réponse malgré tout" in response


# ─────────────────────────────────────────────────────────
# knowledge_candidates
# ─────────────────────────────────────────────────────────

class TestKnowledgeCandidates:

    @pytest.fixture
    def candidates_module(self, tmp_path, monkeypatch):
        import src.knowledge.knowledge_candidates as kc
        monkeypatch.setattr(kc, "CANDIDATES_FILE", tmp_path / "candidates.jsonl")
        return kc

    def test_import(self, candidates_module):
        assert candidates_module.record_candidate is not None

    def test_content_persisted_when_standard_privacy(self, candidates_module):
        cid = candidates_module.record_candidate(
            query="Explique le RAG", external_source="openai",
            response_text="Le RAG consiste à...", quality={"privacy_level": "STANDARD"},
        )
        candidate = candidates_module.get_candidate(cid)
        assert candidate["response_text"] == "Le RAG consiste à..."
        assert candidate["redacted"] is False

    def test_content_redacted_when_local_only_privacy(self, candidates_module):
        cid = candidates_module.record_candidate(
            query="donnée sensible", external_source="openai",
            response_text="contenu sensible", quality={"privacy_level": "LOCAL_ONLY"},
        )
        candidate = candidates_module.get_candidate(cid)
        assert candidate["response_text"] is None
        assert candidate["redacted"] is True

    def test_get_candidate_unknown_returns_none(self, candidates_module):
        assert candidates_module.get_candidate("cand_unknown") is None

    def test_read_pending_excludes_redacted(self, candidates_module):
        candidates_module.record_candidate(
            query="q1", external_source="openai", response_text="texte",
            quality={"privacy_level": "STANDARD"},
        )
        candidates_module.record_candidate(
            query="q2", external_source="openai", response_text="secret",
            quality={"privacy_level": "LOCAL_ONLY"},
        )
        pending = candidates_module.read_pending_candidates()
        assert len(pending) == 1
        assert pending[0]["query"] == "q1"

    def test_read_pending_excludes_promoted(self, candidates_module):
        cid = candidates_module.record_candidate(
            query="q1", external_source="openai", response_text="texte",
            quality={"privacy_level": "STANDARD"},
        )
        assert len(candidates_module.read_pending_candidates()) == 1
        candidates_module.mark_promoted(cid, "domaine.sous_domaine.fiche")
        assert candidates_module.read_pending_candidates() == []

    def test_mark_promoted_does_not_mutate_original_record(self, candidates_module):
        """Append-only : get_candidate() doit continuer à retourner
        l'enregistrement d'origine (pas le marqueur) après promotion."""
        cid = candidates_module.record_candidate(
            query="q1", external_source="openai", response_text="texte",
            quality={"privacy_level": "STANDARD"},
        )
        candidates_module.mark_promoted(cid, "domaine.sous_domaine.fiche")
        candidate = candidates_module.get_candidate(cid)
        assert candidate["response_text"] == "texte"


# ─────────────────────────────────────────────────────────
# gap_curation
# ─────────────────────────────────────────────────────────

class TestGapCuration:

    @pytest.fixture
    def curation_setup(self, tmp_path, monkeypatch):
        import src.knowledge.gap_curation as curation
        import src.knowledge.knowledge_candidates as kc
        import src.training.dataset_store as ds

        monkeypatch.setattr(kc, "CANDIDATES_FILE", tmp_path / "candidates.jsonl")
        monkeypatch.setattr(ds, "TRAINING_ROOT", tmp_path / "training")

        registry_path = tmp_path / "knowledge_registry.json"
        registry_path.write_text(
            '{"knowledges": [], "stats": {"total_json_files": 0}}', encoding="utf-8"
        )
        monkeypatch.setattr(curation, "_REGISTRY_PATH", registry_path)
        monkeypatch.setattr(curation, "_ROOT", tmp_path)

        return curation, kc, tmp_path

    def test_import(self, curation_setup):
        curation, _, _ = curation_setup
        assert curation.promote_candidate_to_knowledge is not None

    def test_unknown_candidate_raises(self, curation_setup):
        curation, _, _ = curation_setup
        with pytest.raises(ValueError, match="introuvable"):
            curation.promote_candidate_to_knowledge(
                candidate_id="cand_unknown", domain="d", subdomain="s",
                title="Titre", summary="résumé", content={},
            )

    def test_redacted_candidate_refused(self, curation_setup):
        curation, kc, _ = curation_setup
        cid = kc.record_candidate(
            query="q", external_source="openai", response_text="secret",
            quality={"privacy_level": "LOCAL_ONLY"},
        )
        with pytest.raises(ValueError, match="confidentialité"):
            curation.promote_candidate_to_knowledge(
                candidate_id=cid, domain="d", subdomain="s",
                title="Titre", summary="résumé", content={},
            )

    def test_successful_promotion_creates_file(self, curation_setup):
        curation, kc, tmp_path = curation_setup
        cid = kc.record_candidate(
            query="Explique le RAG", external_source="openai",
            response_text="Le RAG consiste à...", quality={"privacy_level": "STANDARD"},
        )
        knowledge_id = curation.promote_candidate_to_knowledge(
            candidate_id=cid, domain="test_domain", subdomain="test_sub",
            title="Le RAG expliqué", summary="Résumé du RAG",
            content={"definition": "..."}, tags=["rag"], purpose="Expliquer le RAG",
        )
        assert knowledge_id == "test_domain.test_sub.le_rag_explique"
        fiche_path = tmp_path / "knowledges" / "test_domain" / "test_sub" / "le_rag_explique.json"
        assert fiche_path.exists()

    def test_promoted_fiche_has_validated_provenance(self, curation_setup):
        curation, kc, tmp_path = curation_setup
        cid = kc.record_candidate(
            query="q", external_source="anthropic", response_text="texte",
            quality={"privacy_level": "STANDARD"},
        )
        import json
        knowledge_id = curation.promote_candidate_to_knowledge(
            candidate_id=cid, domain="d", subdomain="s",
            title="Titre", summary="résumé", content={},
        )
        fiche_path = tmp_path / "knowledges" / "d" / "s" / "titre.json"
        fiche = json.loads(fiche_path.read_text(encoding="utf-8"))
        assert fiche["provenance"]["status"] == "VALIDATED"
        assert fiche["provenance"]["training_eligible"] is False
        assert fiche["provenance"]["source_type"] == "anthropic"

    def test_successful_promotion_registers_in_registry(self, curation_setup):
        curation, kc, tmp_path = curation_setup
        cid = kc.record_candidate(
            query="q", external_source="openai", response_text="texte",
            quality={"privacy_level": "STANDARD"},
        )
        import json
        knowledge_id = curation.promote_candidate_to_knowledge(
            candidate_id=cid, domain="d", subdomain="s",
            title="Titre", summary="résumé", content={},
        )
        registry = json.loads(curation._REGISTRY_PATH.read_text(encoding="utf-8"))
        ids = [k["id"] for k in registry["knowledges"]]
        assert knowledge_id in ids
        assert registry["stats"]["total_json_files"] == 1

    def test_successful_promotion_marks_candidate_promoted(self, curation_setup):
        curation, kc, tmp_path = curation_setup
        cid = kc.record_candidate(
            query="q", external_source="openai", response_text="texte",
            quality={"privacy_level": "STANDARD"},
        )
        curation.promote_candidate_to_knowledge(
            candidate_id=cid, domain="d", subdomain="s",
            title="Titre", summary="résumé", content={},
        )
        assert kc.read_pending_candidates() == []

    def test_duplicate_file_path_refused(self, curation_setup):
        curation, kc, tmp_path = curation_setup
        cid1 = kc.record_candidate(
            query="q1", external_source="openai", response_text="texte",
            quality={"privacy_level": "STANDARD"},
        )
        curation.promote_candidate_to_knowledge(
            candidate_id=cid1, domain="d", subdomain="s",
            title="Même Titre", summary="résumé", content={},
        )
        cid2 = kc.record_candidate(
            query="q2", external_source="openai", response_text="autre texte",
            quality={"privacy_level": "STANDARD"},
        )
        with pytest.raises(ValueError, match="existe déjà"):
            curation.promote_candidate_to_knowledge(
                candidate_id=cid2, domain="d", subdomain="s",
                title="Même Titre", summary="résumé", content={},
            )

    def test_promote_to_training_example_unknown_candidate_raises(self, curation_setup):
        curation, _, _ = curation_setup
        with pytest.raises(ValueError, match="introuvable"):
            curation.promote_candidate_to_training_example(
                candidate_id="cand_unknown", response="réponse",
            )

    def test_promote_to_training_example_refuses_redacted(self, curation_setup):
        curation, kc, _ = curation_setup
        cid = kc.record_candidate(
            query="q", external_source="openai", response_text="secret",
            quality={"privacy_level": "LOCAL_ONLY"},
        )
        with pytest.raises(ValueError, match="confidentialité"):
            curation.promote_candidate_to_training_example(candidate_id=cid, response="réponse revue")

    def test_promote_to_training_example_creates_instruction_entry(self, curation_setup):
        curation, kc, _ = curation_setup
        import src.training.dataset_store as ds

        cid = kc.record_candidate(
            query="Explique le RAG", external_source="openai", response_text="brut",
            quality={"privacy_level": "STANDARD"},
        )
        entry = curation.promote_candidate_to_training_example(
            candidate_id=cid, response="Le RAG consiste à...", quality_score=0.9,
        )
        assert entry["instruction"] == "Explique le RAG"
        assert entry["response"] == "Le RAG consiste à..."
        assert entry["source"] == "gap_curation"
        assert entry["training_eligible"] is True
        assert ds.current_count("instructions") == 1
