# -*- coding: utf-8 -*-
"""
pipeline.py — ALFRED V3 Processing Pipeline

14 étapes ordonnées, chacune avec fallback gracieux.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from src.v3.orchestrator.state_manager import SessionState
from src.v3.orchestrator.context_builder import ContextBuilder


@dataclass
class OrchestratorResponse:
    text: str
    mode: str
    emotion_detected: str
    session_id: str
    turn: int
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    rag_hits: int = 0
    fallback: bool = False
    blocked: bool = False


class ProcessingPipeline:
    """
    Pipeline de traitement ALFRED V3.
    Chaque module est chargé avec try/except — rien ne plante le pipeline.
    """

    def __init__(
        self,
        personality_path: str,
        user_profile_path: str,
        memory_path: str,
        config: Dict[str, Any],
        debug: bool = False,
    ):
        self.debug = debug
        self._m: Dict[str, Any] = {}
        self._ctx_builder = ContextBuilder()
        self._load_modules(personality_path, user_profile_path, memory_path)

    # ── Chargement modules ────────────────────────────────

    def _load_modules(
        self,
        personality_path: str,
        user_profile_path: str,
        memory_path: str,
    ) -> None:
        self._try_load("emotion_detect", "src.regulation.emotion_detector", "detect_emotion")
        self._try_load("mode_manager", "src.regulation.mode_manager", "get_mode_manager", call=True)
        self._try_load("analyze_wellbeing", "src.regulation.wellbeing_tracker", "analyze_wellbeing")
        self._try_load("wellbeing_suggest", "src.regulation.wellbeing_tracker", "get_wellbeing_suggestion")
        self._try_load("is_crisis", "src.regulation.protection_guard", "is_crisis")
        self._try_load("block_content", "src.regulation.protection_guard", "should_block_content")
        self._try_load("crisis_response", "src.regulation.protection_guard", "get_crisis_response")
        self._try_load("ethical_check", "src.regulation.protection_guard", "check_ethical_boundaries")
        self._try_load("answer_from_memory", "src.memory.memory_answer_engine", "answer_from_memory")
        # RetrievalEngine (remplace le deprecated knowledge_router)
        try:
            from src.knowledge.retrieval_engine import KnowledgeRetrievalEngine as RetrievalEngine
            import os
            project_root = str(Path(__file__).resolve().parent.parent.parent.parent)
            self._m["retrieval_engine"] = RetrievalEngine(project_root=project_root)
        except Exception as e:
            self._warn("retrieval_engine", e)

        # MemoryEngine
        try:
            from src.memory.memory_engine import MemoryEngine
            self._m["memory"] = MemoryEngine(history_path=memory_path)
        except Exception as e:
            self._warn("memory_engine", e)

        # LongTermMemory
        try:
            import src.memory.long_term_memory as ltm
            ltm.init_db()
            self._m["ltm"] = ltm
        except Exception as e:
            self._warn("long_term_memory", e)

        # RAG
        try:
            from src.rag.rag_engine import RAGEngine
            self._m["rag"] = RAGEngine()
        except Exception as e:
            self._warn("rag_engine", e)

        # PersonalityAdapter
        try:
            from src.core.personality_adapter import PersonalityAdapter
            self._m["personality"] = PersonalityAdapter(
                personality_path=personality_path,
                user_profile_path=user_profile_path,
            )
        except Exception as e:
            self._warn("personality_adapter", e)

        # BehaviorEngine — utilise le fichier personnalité comme identity par défaut
        try:
            from src.core.alfred_behavior_engine import AlfredBehaviorEngine, UserState
            self._m["behavior"] = AlfredBehaviorEngine(identity_path=personality_path)
            self._m["UserState"] = UserState
        except Exception as e:
            self._warn("behavior_engine", e)

        # LLM + ResponseGenerator
        try:
            from src.llm.llm_client_ollama import OllamaLLMClient
            from src.llm.llm_router import LLMRouter
            self._m["llm"] = LLMRouter(primary=OllamaLLMClient(), allow_cloud_fallback=False)
        except Exception as e:
            self._warn("llm_router", e)

        try:
            from src.core.response_generator import ResponseGenerator
            self._m["response_gen"] = ResponseGenerator(
                llm_client=self._m.get("llm"),
                debug=self.debug,
            )
        except Exception as e:
            self._warn("response_generator", e)

    def _try_load(
        self, key: str, module: str, attr: str, call: bool = False
    ) -> None:
        try:
            import importlib
            mod = importlib.import_module(module)
            obj = getattr(mod, attr)
            self._m[key] = obj() if call else obj
        except Exception as e:
            self._warn(key, e)

    def _warn(self, name: str, error: Exception) -> None:
        if self.debug:
            print(f"[PIPELINE] ⚠ {name} indisponible : {error}")

    # ── Pipeline principal ────────────────────────────────

    def run(self, user_input: str, state: SessionState) -> OrchestratorResponse:
        state.increment_turn()

        # ── 1. Crise / blocage input ──────────────────────
        if fn := self._m.get("is_crisis"):
            if fn(user_input):
                crisis_text = self._m["crisis_response"]() if "crisis_response" in self._m else (
                    "Je t'entends. Si tu traverses quelque chose de difficile, parles-en "
                    "à un professionnel de santé. Je suis là pour t'accompagner, pas te remplacer."
                )
                return OrchestratorResponse(
                    text=crisis_text,
                    mode=state.current_mode,
                    emotion_detected="crisis",
                    session_id=state.session_id,
                    turn=state.turn_count,
                    blocked=True,
                )

        if fn := self._m.get("block_content"):
            if fn(user_input):
                return OrchestratorResponse(
                    text="Je ne peux pas traiter cette demande.",
                    mode=state.current_mode,
                    emotion_detected=state.current_emotion,
                    session_id=state.session_id,
                    turn=state.turn_count,
                    blocked=True,
                )

        # ── 2. Détection émotion ──────────────────────────
        emotional_state = None
        if fn := self._m.get("emotion_detect"):
            try:
                emotional_state = fn(user_input)
                state.update_emotion(emotional_state.emotion, emotional_state.intensity)
            except Exception:
                pass

        # ── 3. Wellbeing ──────────────────────────────────
        wellbeing_suggestion: Optional[str] = None
        if fn := self._m.get("analyze_wellbeing"):
            try:
                wb = fn(
                    emotion=state.current_emotion,
                    intensity=state.emotion_intensity,
                    hour=datetime.now().hour,
                )
                state.wellbeing_energy = wb.energy_level
                if suggest := self._m.get("wellbeing_suggest"):
                    wellbeing_suggestion = suggest(wb)
            except Exception:
                pass

        # ── 4. Mode ───────────────────────────────────────
        mode_guidelines = ""
        if mm := self._m.get("mode_manager"):
            try:
                if emotional_state:
                    new_mode = mm.update_from_emotion(emotional_state)
                    state.update_mode(new_mode)
                mode_guidelines = mm.get_response_guidelines()
            except Exception:
                pass

        # ── 5. Mémoire épisodique ─────────────────────────
        memory_context = ""
        if mem := self._m.get("memory"):
            try:
                memory_context = mem.format_context_for_prompt()
            except Exception:
                pass

        # ── 6. Réponse directe depuis mémoire ─────────────
        if fn := self._m.get("answer_from_memory"):
            try:
                direct = fn(user_input, memory_context)
                if direct:
                    self._memorize(user_input, direct, state)
                    return OrchestratorResponse(
                        text=direct,
                        mode=state.current_mode,
                        emotion_detected=state.current_emotion,
                        session_id=state.session_id,
                        turn=state.turn_count,
                    )
            except Exception:
                pass

        # ── 7. RAG sémantique ─────────────────────────────
        rag_results: List[Dict[str, Any]] = []
        if rag := self._m.get("rag"):
            try:
                rag_results = rag.search_memories(user_input, n_results=3)
            except Exception:
                pass

        # ── 8. Knowledge routing ──────────────────────────
        knowledge_context: Dict[str, Any] = {}
        if re_engine := self._m.get("retrieval_engine"):
            try:
                result = re_engine.retrieve(query=user_input)
                knowledge_context = {
                    "prompt_block": result.prompt_block,
                    "domains": result.domains,
                    "knowledge_ids": result.knowledge_ids,
                }
            except Exception:
                pass

        # ── 9. Contexte enrichi (RAG + knowledge + état) ──
        extra_block = self._ctx_builder.build_extra_system_block(
            rag_results=rag_results,
            knowledge_context=knowledge_context,
            wellbeing_suggestion=wellbeing_suggestion,
            state_dict=state.to_dict(),
        )

        # ── 10. Personnalité ──────────────────────────────
        response_context: Dict[str, Any] = {}
        if pa := self._m.get("personality"):
            try:
                response_context = pa.build_response_context(
                    user_message=user_input,
                    detected_emotion=state.current_emotion if state.current_emotion != "neutral" else None,
                    energy_level=state.wellbeing_energy if state.wellbeing_energy != "normal" else None,
                )
            except Exception:
                pass

        # ── 11. Comportement ──────────────────────────────
        behavior_block = ""
        if be := self._m.get("behavior"):
            try:
                UserState = self._m["UserState"]
                us = UserState(
                    emotion=state.current_emotion,
                    intensity=state.emotion_intensity,
                    intent=state.last_intent,
                )
                decision = be.decide_behavior(us, user_message=user_input)
                behavior_block = be.build_prompt_context(decision)
            except Exception:
                pass

        # Injecter le bloc comportemental dans mode_guidelines
        full_guidelines = "\n\n".join(
            part for part in [mode_guidelines, behavior_block, extra_block] if part
        )

        # ── 12. Génération réponse ────────────────────────
        response_text = ""
        fallback = False
        if rg := self._m.get("response_gen"):
            try:
                response_text = rg.generate_response(
                    user_message=user_input,
                    response_context=response_context,
                    history_text=memory_context,
                    mode_guidelines=full_guidelines,
                )
            except Exception:
                fallback = True
        else:
            fallback = True

        if fallback or not response_text:
            response_text = self._offline_response(state)
            fallback = True

        # ── 13. Filtre éthique output ─────────────────────
        if fn := self._m.get("ethical_check"):
            try:
                check = fn(response_text)
                if not check.get("passed", True) and check.get("alerts"):
                    if self.debug:
                        print(f"[ETHICS] alertes : {check['alerts']}")
            except Exception:
                pass

        # ── 14. Mémorisation ──────────────────────────────
        self._memorize(user_input, response_text, state)

        return OrchestratorResponse(
            text=response_text,
            mode=state.current_mode,
            emotion_detected=state.current_emotion,
            session_id=state.session_id,
            turn=state.turn_count,
            rag_hits=len(rag_results),
            fallback=fallback,
        )

    # ── Helpers ───────────────────────────────────────────

    def _memorize(
        self, user_input: str, response: str, state: SessionState
    ) -> None:
        if mem := self._m.get("memory"):
            try:
                mem.save_exchange("user", user_input, intent=state.last_intent)
                mem.save_exchange("alfred", response)
            except Exception:
                pass

        if ltm := self._m.get("ltm"):
            try:
                ltm.save_exchange(
                    session_id=state.session_id,
                    role="user",
                    content=user_input,
                    intent=state.last_intent,
                    emotion=state.current_emotion,
                )
                ltm.save_exchange(
                    session_id=state.session_id,
                    role="alfred",
                    content=response,
                )
            except Exception:
                pass

        if rag := self._m.get("rag"):
            try:
                rag.index_exchange(
                    user_input=user_input,
                    response=response,
                    session_id=state.session_id,
                    turn=state.turn_count,
                )
            except Exception:
                pass

    def _offline_response(self, state: SessionState) -> str:
        prefixes = {
            "support": "Je t'entends.",
            "focus": "Voilà ce que je peux dire pour l'instant.",
            "challenge": "On va travailler ça ensemble.",
            "complicite": "Bonne question !",
        }
        return prefixes.get(state.current_mode, "Je suis là.") + " [mode hors ligne]"

    def get_module_status(self) -> Dict[str, bool]:
        keys = [
            "emotion_detect", "mode_manager", "analyze_wellbeing",
            "is_crisis", "memory", "ltm", "rag",
            "retrieval_engine", "personality", "behavior",
            "llm", "response_gen",
        ]
        return {k: k in self._m for k in keys}
