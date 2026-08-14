"""
════════════════════════════════════════════════════════════
PROJECT      : ALFRED
BLOCK        : B10 — Collaboration & Coordination (volet CPL)
FUNCTION     : 10.xx — Orchestrateur de workflows de collaboration pro
FILE         : src/v3/orchestrator/__init__.py
ROLE         : Charge config/v3/workflow_rules.json + orchestrator_rules.json,
               exécute des workflows de collaboration multi-étapes
               (brainstorming, revue documentaire, co-rédaction) et déclenche
               la génération du livrable CPL correspondant.

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-08-12
VERSION      : V1.0
STATUS       : VALIDÉ — 13/13 tests passés (tests/b10_tests/test_orchestrator.py, 12/08/2026)

DESCRIPTION :
CollaborationOrchestrator est le point d'entrée du mode "collaborateur pro"
côté ALFRED_PC (Bloc 10). Il ne réimplémente pas la génération de livrable :
il délègue à alfred_cpl.assistant_actions.deliverable_generator.generate_deliverable
(dépôt ALFRED_CPL), exactement comme alfred_cpl/__init__.py délègue au moteur
core ALFRED_PC dans l'autre sens (recherche de connaissances, Zero Trust).

Import cross-dépôt : même mécanisme que celui utilisé par ALFRED_CPL pour
retrouver ALFRED_PC (alfred_cpl/__init__.py) — variable d'environnement
ALFRED_CPL_ROOT, sinon dossier frère "ALFRED_CPL" (layout par défaut :
ALFRED_PC et ALFRED_CPL côte à côte). Si le dépôt ALFRED_CPL est introuvable
au runtime, une erreur explicite (AlfredCplUnavailableError) est levée —
jamais d'échec silencieux.

fail_fast (config/v3/orchestrator_rules.json) :
  - True  : la première étape en erreur arrête immédiatement le workflow.
  - False : les étapes continuent malgré une erreur, les erreurs sont
    collectées et retournées ; la génération du livrable final n'a lieu que
    si aucune étape n'a échoué.
════════════════════════════════════════════════════════════
"""
from __future__ import annotations

import importlib
import json
import os
import sys
from pathlib import Path
from typing import Any, Callable

ROOT = Path(__file__).resolve().parents[3]  # racine du dépôt ALFRED_PC
CONFIG_DIR = ROOT / "config" / "v3"
ORCHESTRATOR_RULES_PATH = CONFIG_DIR / "orchestrator_rules.json"
WORKFLOW_RULES_PATH = CONFIG_DIR / "workflow_rules.json"


class OrchestratorConfigError(RuntimeError):
    """Configuration orchestrateur (rules JSON) manquante ou invalide."""


class WorkflowNotFoundError(RuntimeError):
    """Le workflow demandé n'existe pas dans workflow_rules.json."""


class AlfredCplUnavailableError(RuntimeError):
    """Le dépôt ALFRED_CPL n'est pas trouvable (ou pas importable) au runtime."""


def _load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise OrchestratorConfigError(f"Fichier de configuration introuvable : {path}")
    try:
        with path.open(encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as exc:
        raise OrchestratorConfigError(f"JSON invalide dans {path} : {exc}") from exc


def _resolve_alfred_cpl_root() -> Path:
    """
    Résout l'emplacement du dépôt ALFRED_CPL. Miroir exact du mécanisme
    utilisé par alfred_cpl/__init__.py pour retrouver ALFRED_PC :
      1. Variable d'environnement ALFRED_CPL_ROOT
      2. Dossier frère "ALFRED_CPL" (D:/PROJET_ALFRED/ALFRED_PC et
         D:/PROJET_ALFRED/ALFRED_CPL côte à côte)
    """
    env_root = os.environ.get("ALFRED_CPL_ROOT")
    if env_root:
        return Path(env_root).resolve()
    return (ROOT.parent / "ALFRED_CPL").resolve()


def _import_deliverable_generator():
    """
    Importe alfred_cpl.assistant_actions.deliverable_generator depuis le
    dépôt ALFRED_CPL. Lève AlfredCplUnavailableError avec un message clair si
    le dépôt est absent ou si le module ne peut pas être importé, plutôt que
    de laisser remonter une ImportError opaque ou de planter silencieusement.
    """
    cpl_root = _resolve_alfred_cpl_root()
    if not (cpl_root / "alfred_cpl").is_dir():
        raise AlfredCplUnavailableError(
            f"Dépôt ALFRED_CPL introuvable à '{cpl_root}' — impossible de générer "
            f"un livrable de collaboration. Définir la variable d'environnement "
            f"ALFRED_CPL_ROOT si ALFRED_CPL n'est pas au chemin par défaut "
            f"(dossier frère de ALFRED_PC)."
        )
    if str(cpl_root) not in sys.path:
        sys.path.insert(0, str(cpl_root))
    try:
        module = importlib.import_module("alfred_cpl.assistant_actions.deliverable_generator")
    except ImportError as exc:
        raise AlfredCplUnavailableError(
            f"Dépôt ALFRED_CPL trouvé à '{cpl_root}' mais le module "
            f"alfred_cpl.assistant_actions.deliverable_generator n'a pas pu être "
            f"importé : {exc}"
        ) from exc
    return module


class CollaborationOrchestrator:
    """
    Orchestrateur des workflows de collaboration pro (mode ALFRED CPL) :
    brainstorming, revue_documentaire, co_redaction. Charge les règles depuis
    config/v3/workflow_rules.json et config/v3/orchestrator_rules.json.
    """

    def __init__(
        self,
        workflow_rules_path: Path | None = None,
        orchestrator_rules_path: Path | None = None,
        deliverable_fn: Callable[..., dict[str, Any]] | None = None,
    ) -> None:
        self.orchestrator_rules = _load_json(orchestrator_rules_path or ORCHESTRATOR_RULES_PATH)
        self.workflow_rules = _load_json(workflow_rules_path or WORKFLOW_RULES_PATH)
        self.fail_fast: bool = bool(self.orchestrator_rules.get("fail_fast", False))
        self._workflows: dict[str, dict[str, Any]] = {
            wf["name"]: wf for wf in self.workflow_rules.get("workflows", [])
        }
        # Permet l'injection d'un générateur de livrable (tests, ou pour éviter
        # de réimporter alfred_cpl à chaque appel) ; sinon import réel paresseux
        # au premier workflow qui en a besoin.
        self._deliverable_fn = deliverable_fn

    # ------------------------------------------------------------------
    def list_workflows(self) -> list[str]:
        return list(self._workflows.keys())

    def _get_workflow(self, workflow_name: str) -> dict[str, Any]:
        workflow = self._workflows.get(workflow_name)
        if workflow is None:
            available = ", ".join(self.list_workflows()) or "aucun"
            raise WorkflowNotFoundError(
                f"Workflow inconnu : {workflow_name!r} (disponibles : {available})"
            )
        return workflow

    def _deliverable_generator(self) -> Callable[..., dict[str, Any]]:
        if self._deliverable_fn is not None:
            return self._deliverable_fn
        module = _import_deliverable_generator()
        return module.generate_deliverable

    # ------------------------------------------------------------------
    def run_workflow(self, workflow_name: str, context: dict[str, Any]) -> dict[str, Any]:
        """
        Exécute les étapes du workflow (ordre défini par workflow_rules.json),
        puis appelle le générateur de livrable CPL correspondant si toutes les
        étapes ont réussi.

        Args:
            workflow_name : "brainstorming" | "revue_documentaire" | "co_redaction"
            context : doit au minimum contenir "topic" ; peut aussi porter
                user_id/role/device_id/session_id/client_id/request_id,
                transmis tels quels à generate_deliverable().

        Returns:
            {
              "workflow": str,
              "status": "completed" | "failed" | "stopped",
              "steps_run": [str, ...],
              "errors": [{"step": str, "error": str}, ...],
              "deliverable": dict | None,
            }
        """
        workflow = self._get_workflow(workflow_name)
        steps: list[str] = list(workflow.get("steps", []))
        deliverable_type: str = workflow.get("deliverable_type", "")

        steps_run: list[str] = []
        errors: list[dict[str, str]] = []

        for step in steps:
            handler = getattr(self, f"_step_{step}", None)
            try:
                if handler is None:
                    raise ValueError(f"Étape inconnue sans gestionnaire : {step!r}")
                handler(context)
                steps_run.append(step)
            except Exception as exc:  # noqa: BLE001 - collecte volontaire de toute erreur d'étape
                errors.append({"step": step, "error": str(exc)})
                if self.fail_fast:
                    return {
                        "workflow": workflow_name,
                        "status": "stopped",
                        "steps_run": steps_run,
                        "errors": errors,
                        "deliverable": None,
                    }

        if errors:
            return {
                "workflow": workflow_name,
                "status": "failed",
                "steps_run": steps_run,
                "errors": errors,
                "deliverable": None,
            }

        deliverable_result = None
        if deliverable_type:
            generate = self._deliverable_generator()
            deliverable_result = generate(
                deliverable_type=deliverable_type,
                topic=context.get("topic", ""),
                user_id=context.get("user_id", ""),
                role=context.get("role", ""),
                device_id=context.get("device_id", ""),
                session_id=context.get("session_id", ""),
                client_id=context.get("client_id", ""),
                request_id=context.get("request_id", ""),
            )

        return {
            "workflow": workflow_name,
            "status": "completed",
            "steps_run": steps_run,
            "errors": errors,
            "deliverable": deliverable_result,
        }

    # ------------------------------------------------------------------
    # Gestionnaires d'étapes génériques. Volontairement simples : les 3
    # workflows CPL actuels partagent le même squelette collecte / brouillon /
    # revue / finalisation ; la logique métier fine (contenu du livrable)
    # reste dans deliverable_generator/deliverable_templates côté ALFRED_CPL.
    def _step_collect_input(self, context: dict[str, Any]) -> None:
        if not context.get("topic"):
            raise ValueError("collect_input : 'topic' manquant dans le contexte")

    def _step_generate_draft(self, context: dict[str, Any]) -> None:
        context.setdefault("draft_generated", True)

    def _step_review(self, context: dict[str, Any]) -> None:
        context.setdefault("reviewed", True)

    def _step_finalize(self, context: dict[str, Any]) -> None:
        context.setdefault("finalized", True)
