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
from src.security import behavioral_detector
from src.security import device_registry
from src.security import human_validation
from src.security import incident_manager
from src.security import mfa_manager
from src.security import policy_decision_point


@pytest.fixture(autouse=True)
def isolate_security_state_files(tmp_path, monkeypatch):
    """Redirige les fichiers d'état sécurité vers un répertoire temporaire par test.

    05/10/2026 : ajout du registre des appareils, des secrets MFA, du registre
    d'incidents, de l'historique des décisions d'accès et de la baseline
    comportementale — tests/security/test_pentest_zero_trust.py inscrivait
    zt_test_device_001 comme appareil de confiance dans le VRAI registre, et
    des comptes de test (test_mfa_session_user, admin1, guest...) se
    retrouvaient dans le vrai mfa_secrets.json.
    """
    monkeypatch.setattr(audit_trail, "AUDIT_FILE", tmp_path / "audit_trail.jsonl")
    monkeypatch.setattr(human_validation, "APPROVALS_FILE", tmp_path / "pending_approvals.json")
    monkeypatch.setattr(device_registry, "_REGISTRY_FILE", tmp_path / "trusted_devices.json")
    monkeypatch.setattr(mfa_manager, "_SECRETS_FILE", tmp_path / "mfa_secrets.json")
    monkeypatch.setattr(incident_manager, "INCIDENT_FILE", tmp_path / "incident_register.json")
    monkeypatch.setattr(policy_decision_point, "_HISTORY_FILE", tmp_path / "access_decisions_history.json")
    monkeypatch.setattr(behavioral_detector, "_BASELINE_FILE", tmp_path / "behavior_baseline.json")
    yield
