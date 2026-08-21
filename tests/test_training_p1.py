"""
PROJECT      : ALFRED
FILE         : tests/test_training_p1.py
ROLE         : Tests P1 "officiel" (ALFRED_DATA) + P3 scaffolding — voir
               docs/architecture/vision_knowledge_training_finetuning_alfred.md

Couvre : dataset_store (store JSONL versionné générique), training_quality
(privacy/duplication), instruction_dataset, preference_dataset,
adapter_registry (P3, bookkeeping) et lora_pipeline (P3, contrat non
implémenté).
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


# ─────────────────────────────────────────────────────────
# dataset_store
# ─────────────────────────────────────────────────────────

class TestDatasetStore:

    @pytest.fixture
    def store(self, tmp_path, monkeypatch):
        import src.training.dataset_store as ds
        monkeypatch.setattr(ds, "TRAINING_ROOT", tmp_path)
        return ds

    def test_import(self, store):
        assert store.append_entry is not None

    def test_append_and_read_roundtrip(self, store):
        store.append_entry("instructions", {"instruction": "q1", "response": "r1"})
        entries = store.read_current("instructions")
        assert len(entries) == 1
        assert entries[0]["instruction"] == "q1"

    def test_read_current_empty_category(self, store):
        assert store.read_current("nope") == []

    def test_current_count(self, store):
        store.append_entry("preferences", {"prompt": "p"})
        store.append_entry("preferences", {"prompt": "p2"})
        assert store.current_count("preferences") == 2

    def test_read_current_respects_limit(self, store):
        for i in range(5):
            store.append_entry("instructions", {"instruction": f"q{i}"})
        entries = store.read_current("instructions", limit=2)
        assert len(entries) == 2
        assert entries[-1]["instruction"] == "q4"

    def test_bump_version_creates_archive_and_resets_current(self, store):
        store.append_entry("instructions", {"instruction": "q1"})
        archived = store.bump_version("instructions", "v0.1")
        assert archived.exists()
        assert store.read_current("instructions") == []
        assert store.read_version("instructions", "v0.1")[0]["instruction"] == "q1"

    def test_bump_version_raises_on_empty(self, store):
        with pytest.raises(ValueError, match="Rien à figer"):
            store.bump_version("instructions", "v0.1")

    def test_bump_version_raises_on_duplicate(self, store):
        store.append_entry("instructions", {"instruction": "q1"})
        store.bump_version("instructions", "v0.1")
        store.append_entry("instructions", {"instruction": "q2"})
        with pytest.raises(ValueError, match="existe déjà"):
            store.bump_version("instructions", "v0.1")

    def test_list_versions(self, store):
        store.append_entry("instructions", {"instruction": "q1"})
        store.bump_version("instructions", "v0.1")
        versions = store.list_versions("instructions")
        assert len(versions) == 1
        assert versions[0]["version"] == "v0.1"
        assert versions[0]["count"] == 1

    def test_read_version_unknown_returns_empty(self, store):
        assert store.read_version("instructions", "v9.9") == []


# ─────────────────────────────────────────────────────────
# training_quality
# ─────────────────────────────────────────────────────────

class TestTrainingQuality:

    @pytest.fixture
    def quality_env(self, tmp_path, monkeypatch):
        import src.training.dataset_store as ds
        import src.training.training_quality as tq
        monkeypatch.setattr(ds, "TRAINING_ROOT", tmp_path)
        return tq, ds

    def test_import(self, quality_env):
        tq, _ = quality_env
        assert tq.evaluate_training_entry is not None

    def test_duplicate_score_zero_when_no_existing_entries(self, quality_env):
        tq, _ = quality_env
        result = tq.evaluate_training_entry(
            text_for_privacy="une question neutre",
            text_for_duplicate="une question neutre",
            category="instructions",
        )
        assert result["duplicate_score"] == 0.0

    def test_duplicate_score_high_on_near_identical_entry(self, quality_env):
        tq, ds = quality_env
        ds.append_entry("instructions", {"instruction": "Comment fonctionne le RAG ?"})
        result = tq.evaluate_training_entry(
            text_for_privacy="Comment fonctionne le RAG ?",
            text_for_duplicate="Comment fonctionne le RAG ?",
            category="instructions",
        )
        assert result["duplicate_score"] >= tq.DUPLICATE_THRESHOLD

    def test_training_eligible_false_without_quality_score(self, quality_env):
        tq, _ = quality_env
        result = tq.evaluate_training_entry(
            text_for_privacy="question neutre",
            text_for_duplicate="question neutre",
            category="instructions",
        )
        assert result["training_eligible"] is False

    def test_training_eligible_true_with_good_quality_score(self, quality_env):
        tq, _ = quality_env
        result = tq.evaluate_training_entry(
            text_for_privacy="question neutre",
            text_for_duplicate="question neutre",
            category="instructions",
            quality_score=0.9,
        )
        assert result["training_eligible"] is True

    def test_training_eligible_false_below_quality_threshold(self, quality_env):
        tq, _ = quality_env
        result = tq.evaluate_training_entry(
            text_for_privacy="question neutre",
            text_for_duplicate="question neutre",
            category="instructions",
            quality_score=0.4,
        )
        assert result["training_eligible"] is False

    def test_privacy_check_reflects_safety_gate(self, quality_env, monkeypatch):
        tq, _ = quality_env
        monkeypatch.setattr(
            tq, "assess_prompt_sensitivity",
            lambda text: {"privacy_level": "LOCAL_ONLY", "cloud_allowed": False, "matched_categories": ["health"]},
        )
        result = tq.evaluate_training_entry(
            text_for_privacy="donnée sensible",
            text_for_duplicate="donnée sensible",
            category="instructions",
            quality_score=0.9,
        )
        assert result["privacy_check"] is False
        assert result["training_eligible"] is False


# ─────────────────────────────────────────────────────────
# instruction_dataset
# ─────────────────────────────────────────────────────────

class TestInstructionDataset:

    @pytest.fixture
    def env(self, tmp_path, monkeypatch):
        import src.training.dataset_store as ds
        import src.training.instruction_dataset as instr
        monkeypatch.setattr(ds, "TRAINING_ROOT", tmp_path)
        return instr, ds

    def test_import(self, env):
        instr, _ = env
        assert instr.record_instruction_candidate is not None

    def test_record_appends_to_instructions_category(self, env):
        instr, ds = env
        instr.record_instruction_candidate(instruction="q", response="r")
        assert ds.current_count("instructions") == 1

    def test_record_returns_full_entry(self, env):
        instr, _ = env
        entry = instr.record_instruction_candidate(
            instruction="Explique le RAG", response="Le RAG consiste à...",
            source="manual", quality_score=0.95,
        )
        assert entry["instruction"] == "Explique le RAG"
        assert entry["response"] == "Le RAG consiste à..."
        assert entry["validated"] is True
        assert entry["training_eligible"] is True

    def test_record_default_source_is_manual(self, env):
        instr, _ = env
        entry = instr.record_instruction_candidate(instruction="q", response="r")
        assert entry["source"] == "manual"


# ─────────────────────────────────────────────────────────
# preference_dataset
# ─────────────────────────────────────────────────────────

class TestPreferenceDataset:

    @pytest.fixture
    def env(self, tmp_path, monkeypatch):
        import src.training.dataset_store as ds
        import src.training.preference_dataset as pref
        monkeypatch.setattr(ds, "TRAINING_ROOT", tmp_path)
        return pref, ds

    def test_import(self, env):
        pref, _ = env
        assert pref.record_preference is not None

    def test_record_preference_schema(self, env):
        pref, _ = env
        entry = pref.record_preference(prompt="p", chosen="a", rejected="b")
        assert entry == {
            "prompt": "p", "chosen": "a", "rejected": "b",
            "preference_source": "user", "confidence": 1.0,
        }

    def test_record_preference_appends(self, env):
        pref, ds = env
        pref.record_preference(prompt="p", chosen="a", rejected="b")
        assert ds.current_count("preferences") == 1


# ─────────────────────────────────────────────────────────
# adapter_registry (P3 — bookkeeping)
# ─────────────────────────────────────────────────────────

class TestAdapterRegistry:

    @pytest.fixture
    def registry(self, tmp_path, monkeypatch):
        import src.training.adapter_registry as ar
        monkeypatch.setattr(ar, "REGISTRY_PATH", tmp_path / "adapter_registry.json")
        return ar

    def test_import(self, registry):
        assert registry.register_adapter is not None

    def test_register_adapter_default_staging(self, registry):
        entry = registry.register_adapter(
            adapter_version="v0.1", base_model="mistral:7b",
            dataset_versions={"instructions": "v0.1"}, training_config={"rank": 8},
        )
        assert entry["status"] == "staging"

    def test_register_adapter_rejects_direct_production(self, registry):
        with pytest.raises(ValueError, match="production"):
            registry.register_adapter(
                adapter_version="v0.1", base_model="mistral:7b",
                dataset_versions={}, training_config={}, status="production",
            )

    def test_register_adapter_rejects_duplicate_version(self, registry):
        registry.register_adapter(
            adapter_version="v0.1", base_model="mistral:7b",
            dataset_versions={}, training_config={},
        )
        with pytest.raises(ValueError, match="existe déjà"):
            registry.register_adapter(
                adapter_version="v0.1", base_model="mistral:7b",
                dataset_versions={}, training_config={},
            )

    def test_register_adapter_rejects_invalid_status(self, registry):
        with pytest.raises(ValueError, match="invalide"):
            registry.register_adapter(
                adapter_version="v0.1", base_model="mistral:7b",
                dataset_versions={}, training_config={}, status="bogus",
            )

    def test_get_adapter_roundtrip(self, registry):
        registry.register_adapter(
            adapter_version="v0.1", base_model="mistral:7b",
            dataset_versions={}, training_config={},
        )
        assert registry.get_adapter("v0.1")["base_model"] == "mistral:7b"

    def test_get_adapter_unknown_returns_none(self, registry):
        assert registry.get_adapter("v9.9") is None

    def test_list_adapters_filters_by_status(self, registry):
        registry.register_adapter(
            adapter_version="v0.1", base_model="m", dataset_versions={}, training_config={},
        )
        registry.register_adapter(
            adapter_version="v0.2", base_model="m", dataset_versions={}, training_config={},
        )
        assert len(registry.list_adapters(status="staging")) == 2
        assert registry.list_adapters(status="production") == []

    def test_promote_to_production_requires_evaluation(self, registry):
        registry.register_adapter(
            adapter_version="v0.1", base_model="m", dataset_versions={}, training_config={},
        )
        with pytest.raises(ValueError, match="rapport d'évaluation"):
            registry.promote_to_production("v0.1")

    def test_promote_to_production_after_evaluation(self, registry):
        registry.register_adapter(
            adapter_version="v0.1", base_model="m", dataset_versions={}, training_config={},
        )
        registry.record_evaluation("v0.1", {"score": 0.9})
        registry.promote_to_production("v0.1")
        assert registry.get_adapter("v0.1")["status"] == "production"
        assert registry.get_active_production_adapter()["adapter_version"] == "v0.1"

    def test_promote_disables_previous_production(self, registry):
        registry.register_adapter(
            adapter_version="v0.1", base_model="m", dataset_versions={}, training_config={},
        )
        registry.record_evaluation("v0.1", {"score": 0.9})
        registry.promote_to_production("v0.1")

        registry.register_adapter(
            adapter_version="v0.2", base_model="m", dataset_versions={}, training_config={},
        )
        registry.record_evaluation("v0.2", {"score": 0.95})
        registry.promote_to_production("v0.2")

        assert registry.get_adapter("v0.1")["status"] == "disabled"
        assert registry.get_adapter("v0.2")["status"] == "production"

    def test_disable_adapter(self, registry):
        registry.register_adapter(
            adapter_version="v0.1", base_model="m", dataset_versions={}, training_config={},
        )
        registry.disable_adapter("v0.1")
        assert registry.get_adapter("v0.1")["status"] == "disabled"

    def test_disable_unknown_adapter_raises(self, registry):
        with pytest.raises(ValueError, match="introuvable"):
            registry.disable_adapter("v9.9")

    def test_no_active_production_adapter_returns_none(self, registry):
        assert registry.get_active_production_adapter() is None


# ─────────────────────────────────────────────────────────
# lora_pipeline (P3 — contrat non implémenté)
# ─────────────────────────────────────────────────────────

class TestLoraPipelineContract:

    def test_import(self):
        from src.training.lora_pipeline import TrainingRunConfig, prepare_training_run, run_lora_finetuning
        assert TrainingRunConfig is not None
        assert prepare_training_run is not None
        assert run_lora_finetuning is not None

    def test_prepare_training_run_not_implemented(self):
        from src.training.lora_pipeline import TrainingRunConfig, prepare_training_run
        config = TrainingRunConfig(base_model="mistral:7b", dataset_category="instructions", dataset_version="v0.1")
        with pytest.raises(NotImplementedError, match="matériel compatible"):
            prepare_training_run(config)

    def test_run_lora_finetuning_not_implemented(self):
        from src.training.lora_pipeline import TrainingRunConfig, run_lora_finetuning
        config = TrainingRunConfig(base_model="mistral:7b", dataset_category="instructions", dataset_version="v0.1")
        with pytest.raises(NotImplementedError, match="matériel compatible"):
            run_lora_finetuning(config)

    def test_training_run_config_defaults(self):
        from src.training.lora_pipeline import TrainingRunConfig
        config = TrainingRunConfig(base_model="m", dataset_category="instructions", dataset_version="v0.1")
        assert config.method == "qlora"
        assert config.rank == 8
