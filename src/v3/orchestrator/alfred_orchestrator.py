# -*- coding: utf-8 -*-
"""
alfred_orchestrator.py — ALFRED V3 Orchestrateur principal

Point d'entrée unique pour traiter une entrée utilisateur.
Coordonne tous les modules via ProcessingPipeline.
"""

from __future__ import annotations

import uuid
from typing import Any, Dict, Optional

from src.v3.orchestrator.pipeline import OrchestratorResponse, ProcessingPipeline
from src.v3.orchestrator.state_manager import SessionState


class AlfredOrchestrator:
    """
    Interface publique de l'orchestrateur ALFRED V3.

    Usage :
        orch = AlfredOrchestrator(personality_path=..., user_profile_path=...)
        resp = orch.process("Bonjour ALFRED")
        print(resp.text)
    """

    def __init__(
        self,
        personality_path: str,
        user_profile_path: str,
        memory_path: str = "data/memory/episodic/dialogue_history.json",
        config: Optional[Dict[str, Any]] = None,
        debug: bool = False,
    ):
        self.debug = debug
        self._session_id = str(uuid.uuid4())[:8]

        self._pipeline = ProcessingPipeline(
            personality_path=personality_path,
            user_profile_path=user_profile_path,
            memory_path=memory_path,
            config=config or {},
            debug=debug,
        )
        self._state = SessionState(session_id=self._session_id)

    # ── API publique ──────────────────────────────────────

    def process(self, user_input: str) -> OrchestratorResponse:
        """Traite une entrée utilisateur et retourne une réponse complète."""
        return self._pipeline.run(user_input.strip(), self._state)

    def reset_session(self) -> None:
        """Démarre une nouvelle session (réinitialise état + identifiant)."""
        self._session_id = str(uuid.uuid4())[:8]
        self._state = SessionState(session_id=self._session_id)

    def set_mode(self, mode: str) -> None:
        """Force un mode ALFRED (support / focus / challenge / complicite)."""
        self._state.update_mode(mode)
        if mm := self._pipeline._m.get("mode_manager"):
            try:
                mm.set_mode(mode, reason="manual_override")
            except Exception:
                pass

    def get_status(self) -> Dict[str, Any]:
        """Retourne l'état complet de l'orchestrateur et de ses modules."""
        return {
            "session": self._state.to_dict(),
            "modules": self._pipeline.get_module_status(),
            "rag": self._get_rag_status(),
        }

    # ── Helpers internes ──────────────────────────────────

    def _get_rag_status(self) -> Dict[str, Any]:
        if rag := self._pipeline._m.get("rag"):
            try:
                return rag.get_status()
            except Exception:
                pass
        return {"available": False}
