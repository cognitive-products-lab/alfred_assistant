"""
PROJECT      : ALFRED
BLOCK        : B18
FUNCTION     : 18.TESTS
FILE         : tests/test_b18_knowledge.py
ROLE         : Suite de tests B18 — Knowledge & Intelligence System

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-06-03
UPDATED      : 2026-06-03
VERSION      : V1.0
STATUS       : ACTIVE

DESCRIPTION :
Tests unitaires et d'integration pour les modules du Bloc 18 :
KnowledgeLoader, DomainMatcher, TaxonomyRouter, KnowledgeRanker,
ContextMerger, RetrievalEngine, KnowledgeRouter.
"""

from __future__ import annotations

import sys
from pathlib import Path
import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


# ──────────────────────────────────────────────────────────────────────────────
# Fixtures
# ──────────────────────────────────────────────────────────────────────────────

@pytest.fixture(scope="module")
def loader():
    from src.knowledge.knowledge_loader import KnowledgeLoader
    return KnowledgeLoader(project_root=str(ROOT))


@pytest.fixture(scope="module")
def matcher(loader):
    from src.knowledge.domain_matcher import DomainMatcher
    return DomainMatcher(loader)


# ──────────────────────────────────────────────────────────────────────────────
# KnowledgeLoader
# ──────────────────────────────────────────────────────────────────────────────

class TestKnowledgeLoader:

    def test_import(self):
        from src.knowledge.knowledge_loader import KnowledgeLoader
        assert KnowledgeLoader is not None

    def test_instantiation(self, loader):
        assert loader is not None

    def test_stats_returns_dict(self, loader):
        stats = loader.stats()
        assert isinstance(stats, dict)
        assert "indexed_knowledge_count" in stats
        assert "registry_knowledge_count" in stats

    def test_list_ids_returns_list(self, loader):
        ids = loader.list_ids()
        assert isinstance(ids, list)

    def test_get_by_domain_returns_list(self, loader):
        result = loader.get_by_domain("human")
        assert isinstance(result, list)

    def test_get_by_subdomain_returns_list(self, loader):
        result = loader.get_by_subdomain("health")
        assert isinstance(result, list)

    def test_get_knowledge_unknown_returns_none(self, loader):
        assert loader.get_knowledge("__nonexistent_id__") is None

    def test_get_many_returns_list(self, loader):
        ids = loader.list_ids()[:3]
        result = loader.get_many(ids)
        assert isinstance(result, list)
        assert len(result) <= 3

    def test_reload(self, loader):
        loader.reload()
        assert isinstance(loader.knowledge_index, dict)


# ──────────────────────────────────────────────────────────────────────────────
# DomainMatcher
# ──────────────────────────────────────────────────────────────────────────────

class TestDomainMatcher:

    def test_import(self):
        from src.knowledge.domain_matcher import DomainMatcher, DomainMatch
        assert DomainMatcher is not None
        assert DomainMatch is not None

    def test_instantiation(self, matcher):
        assert matcher is not None

    def test_normalize_lowercase(self, matcher):
        assert matcher.normalize("HELLO WORLD") == "hello world"

    def test_normalize_strip(self, matcher):
        assert matcher.normalize("  spaces  ") == "spaces"

    def test_match_returns_list(self, matcher):
        results = matcher.match("Je suis fatiguée")
        assert isinstance(results, list)

    def test_match_empty_query(self, matcher):
        results = matcher.match("")
        assert isinstance(results, list)

    def test_match_top_k_respected(self, matcher):
        results = matcher.match("sécurité données RGPD", top_k=2)
        assert len(results) <= 2

    def test_match_score_ordered(self, matcher):
        results = matcher.match("je suis fatiguée et stressée", top_k=5)
        scores = [r.score for r in results]
        assert scores == sorted(scores, reverse=True)

    def test_get_priority_knowledge_ids(self, matcher):
        ids = matcher.get_priority_knowledge_ids("mémoire cognitive")
        assert isinstance(ids, list)

    def test_get_priority_domains(self, matcher):
        domains = matcher.get_priority_domains("cybersécurité RGPD")
        assert isinstance(domains, list)

    def test_compute_score_nonzero_for_keyword_match(self, matcher):
        route = {"keywords": ["fatigue"], "priority_domains": [], "intents": []}
        score = matcher.compute_score(["fatigue"], route, "je suis fatiguée")
        assert score > 0


# ──────────────────────────────────────────────────────────────────────────────
# TaxonomyRouter
# ──────────────────────────────────────────────────────────────────────────────

class TestTaxonomyRouter:

    def test_import(self):
        from src.knowledge.taxonomy_router import TaxonomyRouter
        assert TaxonomyRouter is not None

    def test_instantiation(self, loader):
        from src.knowledge.taxonomy_router import TaxonomyRouter
        router = TaxonomyRouter(loader)
        assert router is not None


# ──────────────────────────────────────────────────────────────────────────────
# KnowledgeRanker
# ──────────────────────────────────────────────────────────────────────────────

class TestKnowledgeRanker:

    def test_import(self):
        from src.knowledge.knowledge_ranker import KnowledgeRanker, RankedKnowledge
        assert KnowledgeRanker is not None

    def test_instantiation(self, loader):
        from src.knowledge.knowledge_ranker import KnowledgeRanker
        ranker = KnowledgeRanker(loader)
        assert ranker is not None

    def test_rank_returns_list(self, loader):
        from src.knowledge.knowledge_ranker import KnowledgeRanker
        ranker = KnowledgeRanker(loader)
        result = ranker.rank("fatigue mémoire", knowledge_ids=loader.list_ids()[:5])
        assert isinstance(result, list)


# ──────────────────────────────────────────────────────────────────────────────
# ContextMerger
# ──────────────────────────────────────────────────────────────────────────────

class TestContextMerger:

    def test_import(self):
        from src.knowledge.context_merger import ContextMerger, MergedKnowledgeContext
        assert ContextMerger is not None

    def test_instantiation(self, loader):
        from src.knowledge.context_merger import ContextMerger
        merger = ContextMerger(loader)
        assert merger is not None

    def test_merge_empty_returns_object(self, loader):
        from src.knowledge.context_merger import ContextMerger
        merger = ContextMerger(loader)
        result = merger.merge(ranked_knowledge=[], query="test")
        assert result is not None


# ──────────────────────────────────────────────────────────────────────────────
# KnowledgeRouter
# ──────────────────────────────────────────────────────────────────────────────

class TestKnowledgeRouter:

    def test_import(self):
        from src.knowledge.knowledge_router import KnowledgeRouter
        assert KnowledgeRouter is not None


# ──────────────────────────────────────────────────────────────────────────────
# RetrievalEngine (integration)
# ──────────────────────────────────────────────────────────────────────────────

class TestRetrievalEngine:

    def test_import(self):
        from src.knowledge.retrieval_engine import RetrievalEngine, RetrievalResult
        assert RetrievalEngine is not None

    def test_instantiation(self, loader):
        from src.knowledge.retrieval_engine import RetrievalEngine
        engine = RetrievalEngine(loader)
        assert engine is not None

    def test_retrieve_returns_result(self, loader):
        from src.knowledge.retrieval_engine import RetrievalEngine, RetrievalResult
        engine = RetrievalEngine(loader)
        result = engine.retrieve("Je suis fatiguée")
        assert isinstance(result, RetrievalResult)
        assert result.query == "Je suis fatiguée"

    def test_prompt_block_is_string(self, loader):
        from src.knowledge.retrieval_engine import RetrievalEngine
        engine = RetrievalEngine(loader)
        result = engine.retrieve("cybersécurité données")
        assert isinstance(result.prompt_block, str)

    def test_knowledge_ids_is_list(self, loader):
        from src.knowledge.retrieval_engine import RetrievalEngine
        engine = RetrievalEngine(loader)
        result = engine.retrieve("mémoire cognitive")
        assert isinstance(result.knowledge_ids, list)
