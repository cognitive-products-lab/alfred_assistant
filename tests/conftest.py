"""
════════════════════════════════════════════════════════════
PROJECT      : ALFRED
BLOCK        : GLOBAL
FUNCTION     : TESTS
FILE         : tests/conftest.py
ROLE         : Isolation des fichiers d'état sécurité pour toute la suite de tests

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-07-11
VERSION      : V1.0
STATUS       : ACTIVE

DESCRIPTION :
Redirige les fichiers d'état sécurité (piste d'audit, file d'approbation
humaine) vers un répertoire temporaire pour CHAQUE test de la suite,
quel que soit le dossier. Corrige un défaut constaté : de nombreux tests
appellent write_audit_event (directement ou via authorize_request /
KnowledgeRetrievalEngine) sans isolation, ce qui polluait le vrai
logs/security/audit_trail.jsonl de production à chaque run de la suite.

Le monkeypatch cible l'attribut de module (audit_trail.AUDIT_FILE,
human_validation.APPROVALS_FILE) : toute fonction qui lit ce nom au moment
de l'appel (write_audit_event, submit_for_review, etc.) est protégée,
même si elle a été importée ailleurs via "from ... import ...", car la
résolution de variable globale se fait dans le module d'origine.
════════════════════════════════════════════════════════════
"""
import pytest

from src.security import audit_trail
from src.security import human_validation


@pytest.fixture(autouse=True)
def isolate_security_state_files(tmp_path, monkeypatch):
    """Redirige AUDIT_FILE et APPROVALS_FILE vers un répertoire temporaire par test."""
    monkeypatch.setattr(audit_trail, "AUDIT_FILE", tmp_path / "audit_trail.jsonl")
    monkeypatch.setattr(human_validation, "APPROVALS_FILE", tmp_path / "pending_approvals.json")
    yield
