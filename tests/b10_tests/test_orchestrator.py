"""
════════════════════════════════════════════════════════════
PROJECT      : ALFRED
BLOCK        : B10 — Collaboration & Coordination (volet CPL)
FUNCTION     : B10.TEST
FILE         : tests/b10_tests/test_orchestrator.py
ROLE         : Tests unitaires — src/v3/orchestrator/__init__.py (CollaborationOrchestrator)

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-08-12
VERSION      : V1.0
STATUS       : VALIDATED

DESCRIPTION :
Le générateur de livrable réel (alfred_cpl.assistant_actions.deliverable_generator)
appelle le moteur de recherche de connaissances et le pipeline Zero Trust
d'ALFRED_PC (authentification, session) — hors périmètre d'un test unitaire de
l'orchestrateur. Les tests injectent donc un `deliverable_fn` factice
(paramètre prévu par CollaborationOrchestrator) pour isoler la logique
d'enchaînement des étapes / fail_fast, qui est ce que ce fichier couvre.

Un test d'intégration séparé (TestAlfredCplUnavailable) vérifie, lui, le vrai
mécanisme d'import cross-dépôt sans injection.
════════════════════════════════════════════════════════════
"""

import json
import sys
from pathlib import Path

import pytest

_ROOT = Path(__file__).resolve().parents[2]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from src.v3.orchestrator import (
    ORCHESTRATOR_RULES_PATH,
    WORKFLOW_RULES_PATH,
    CollaborationOrchestrator,
    AlfredCplUnavailableError,
    WorkflowNotFoundError,
)


def _fake_deliverable_fn(**kwargs):
    return {"authorized": True, "decision": "REVIEW", "pending": True,
            "deliverable": {"deliverable_type": kwargs.get("deliverable_type"),
                             "title": f"Brouillon — {kwargs.get('topic')}"}}


def _minimal_context(**overrides):
    context = {
        "topic": "automatisation du support client",
        "user_id": "u1",
        "role": "consultant",
        "device_id": "d1",
        "session_id": "s1",
    }
    context.update(overrides)
    return context


# ─── Chargement de la config réelle du dépôt ─────────────────────────────────

class TestRealConfigLoads:
    def test_orchestrator_rules_path_exists(self):
        assert ORCHESTRATOR_RULES_PATH.exists()

    def test_workflow_rules_path_exists(self):
        assert WORKFLOW_RULES_PATH.exists()

    def test_default_construction_loads_real_config(self):
        orch = CollaborationOrchestrator(deliverable_fn=_fake_deliverable_fn)
        assert orch.fail_fast is False  # orchestrator_rules.json réel : fail_fast=false
        assert set(orch.list_workflows()) == {"brainstorming", "revue_documentaire", "co_redaction"}

    def test_each_real_workflow_has_deliverable_type(self):
        orch = CollaborationOrchestrator(deliverable_fn=_fake_deliverable_fn)
        for name in orch.list_workflows():
            wf = orch._get_workflow(name)
            assert wf["deliverable_type"] in {"fiche_cadrage", "registre_risques"}
            assert wf["steps"], f"{name} n'a aucune étape"


# ─── Exécution de chaque workflow réel avec un contexte minimal valide ──────

class TestRunEachRealWorkflow:
    @pytest.mark.parametrize("workflow_name", ["brainstorming", "revue_documentaire", "co_redaction"])
    def test_workflow_runs_without_error(self, workflow_name):
        orch = CollaborationOrchestrator(deliverable_fn=_fake_deliverable_fn)
        result = orch.run_workflow(workflow_name, _minimal_context())
        assert result["status"] == "completed"
        assert result["errors"] == []
        assert result["deliverable"] is not None
        assert result["deliverable"]["deliverable"]["deliverable_type"] in {"fiche_cadrage", "registre_risques"}
        assert result["steps_run"] == ["collect_input", "generate_draft", "review", "finalize"]

    def test_unknown_workflow_raises(self):
        orch = CollaborationOrchestrator(deliverable_fn=_fake_deliverable_fn)
        with pytest.raises(WorkflowNotFoundError):
            orch.run_workflow("workflow_qui_n_existe_pas", _minimal_context())

    def test_missing_topic_fails_first_step(self):
        orch = CollaborationOrchestrator(deliverable_fn=_fake_deliverable_fn)
        result = orch.run_workflow("brainstorming", {})
        assert result["status"] == "failed"
        assert result["errors"][0]["step"] == "collect_input"
        assert result["deliverable"] is None


# ─── fail_fast=True / fail_fast=False, avec des rules de test dédiées ───────

@pytest.fixture
def custom_rules(tmp_path):
    """
    Workflow de test avec 2 étapes 'collect_input' d'affilée (contexte sans
    'topic' => les deux échouent) suivies de 'generate_draft' (réussit
    toujours). Permet de distinguer clairement fail_fast=True (arrêt après la
    1re erreur, 'generate_draft' jamais exécutée) de fail_fast=False (les 2
    erreurs sont collectées ET 'generate_draft' s'exécute quand même).
    """
    workflow_rules = {
        "workflows": [
            {
                "name": "test_double_fail",
                "steps": ["collect_input", "collect_input", "generate_draft"],
                "deliverable_type": "fiche_cadrage",
            }
        ]
    }
    workflow_path = tmp_path / "workflow_rules.json"
    workflow_path.write_text(json.dumps(workflow_rules), encoding="utf-8")
    return workflow_path


def test_fail_fast_true_stops_at_first_error(tmp_path, custom_rules):
    orchestrator_rules_path = tmp_path / "orchestrator_rules.json"
    orchestrator_rules_path.write_text(json.dumps({"fail_fast": True}), encoding="utf-8")

    orch = CollaborationOrchestrator(
        workflow_rules_path=custom_rules,
        orchestrator_rules_path=orchestrator_rules_path,
        deliverable_fn=_fake_deliverable_fn,
    )
    result = orch.run_workflow("test_double_fail", {})  # pas de 'topic' => échec immédiat

    assert orch.fail_fast is True
    assert result["status"] == "stopped"
    assert result["steps_run"] == []
    assert len(result["errors"]) == 1
    assert result["deliverable"] is None


def test_fail_fast_false_collects_errors_without_stopping(tmp_path, custom_rules):
    orchestrator_rules_path = tmp_path / "orchestrator_rules.json"
    orchestrator_rules_path.write_text(json.dumps({"fail_fast": False}), encoding="utf-8")

    orch = CollaborationOrchestrator(
        workflow_rules_path=custom_rules,
        orchestrator_rules_path=orchestrator_rules_path,
        deliverable_fn=_fake_deliverable_fn,
    )
    result = orch.run_workflow("test_double_fail", {})  # pas de 'topic'

    assert orch.fail_fast is False
    assert result["status"] == "failed"  # des erreurs existent => pas de livrable généré
    assert len(result["errors"]) == 2  # les 2 'collect_input' ont échoué, ni l'un ni l'autre n'a arrêté le workflow
    assert result["steps_run"] == ["generate_draft"]  # la 3e étape s'est bien exécutée malgré les erreurs précédentes
    assert result["deliverable"] is None


# ─── Import cross-dépôt : erreur claire si ALFRED_CPL est introuvable ───────

class TestAlfredCplUnavailable:
    def test_missing_alfred_cpl_raises_explicit_error(self, monkeypatch):
        # Pointe vers un dossier qui n'existe pas => sans deliverable_fn injecté,
        # l'orchestrateur doit lever une erreur claire, pas planter silencieusement
        # ni renvoyer un résultat vide.
        monkeypatch.setenv("ALFRED_CPL_ROOT", str(Path("Z:/chemin/qui/n_existe/pas")))
        orch = CollaborationOrchestrator()  # pas de deliverable_fn => import réel tenté
        with pytest.raises(AlfredCplUnavailableError, match="introuvable"):
            orch.run_workflow("brainstorming", _minimal_context())

    def test_real_alfred_cpl_repo_importable_if_present(self):
        """
        Si le dépôt frère ALFRED_CPL est présent sur ce poste (layout de
        développement standard), l'import réel doit réussir. Ce test se
        auto-skip si le dépôt n'est pas là (environnement CI sans le monorepo
        complet) plutôt que d'échouer à tort.
        """
        cpl_root = _ROOT.parent / "ALFRED_CPL"
        if not (cpl_root / "alfred_cpl").is_dir():
            pytest.skip("Dépôt ALFRED_CPL absent de ce poste — test d'intégration ignoré")

        orch = CollaborationOrchestrator()
        generate = orch._deliverable_generator()
        assert callable(generate)
