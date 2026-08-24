"""
════════════════════════════════════════════════════════════
PROJECT      : ALFRED
BLOCK        : NOUVEAU — non numéroté (voir note ci-dessous)
FUNCTION     : Data & Pilotage Comportemental
FILE         : src/reasoning/reasoning_engine.py
ROLE         : Scaffolding de raisonnement avant appel LLM — décompose,
               récupère le contexte pertinent, estime une confiance, et
               prépare des directives de raisonnement pour le prompt.

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-08-24
UPDATED      : 2026-08-24
VERSION      : V1.0
STATUS       : DRAFT

DESCRIPTION :
Chantier ouvert depuis la mémoire "reasoning_engine / ethics_engine /
robustness_checker à créer avant fin de semaine" (motivé par le fil Human
IA, RAG sémantique + tendance émotionnelle livrés le 21/08/2026). La
numérotation "Phase 16 — Data & Pilotage Comportemental" vient d'un
document externe (page /projet/cadrage, ALFRED_WEB) : elle ne correspond
à aucun Bloc numéroté de ce dépôt (docs/ALFRED_BLOCS_REFERENCE.md n'a pas
de Phase 16). Conservée en commentaire pour traçabilité, sans inventer un
numéro de Bloc qui n'existe pas.

Suit fidèlement le pipeline déjà documenté dans
knowledges/professional/engineering/ai/reasoning_engine.json (intake →
classify → decompose → retrieve → reason → evaluate → synthesize) — ce
fichier de connaissance existait avant ce code, il en est la spec.

Comme RegulationEngine (src/regulation/regulation_engine.py), ce moteur ne
répond pas lui-même : il produit un ReasoningResult que
response_generator/tool_calling peuvent injecter dans le prompt LLM. Niveau
0 de sobriété cognitive (heuristiques explicites, pas de ML) — cohérent
avec safety_gate.py et emotional_trend.py.
════════════════════════════════════════════════════════════
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any

from src.security.security_logger import log_event

# ─────────────────────────────────────────────────────────
# Constantes — modes de raisonnement et seuils de complexité
# (repris tels quels de knowledges/professional/engineering/ai/reasoning_engine.json,
# section reasoning_modes / complexity_thresholds / confidence_scoring)
# ─────────────────────────────────────────────────────────

REASONING_MODES = {
    "deductive":     "De règles générales vers cas particuliers — si A alors B",
    "inductive":      "De cas particuliers vers généralisation",
    "abductive":      "De l'observation vers l'explication la plus probable",
    "analogical":     "Par analogie avec une situation connue",
    "causal":         "Identifier causes et effets dans une chaîne",
    "counterfactual": "Et si… ? Exploration d'alternatives",
}

# Mots-clés déclencheurs par mode — heuristique simple, pas de classification ML
# (même esprit que safety_gate.py::assess_prompt_sensitivity).
_MODE_KEYWORDS = {
    "counterfactual": ["et si", "que se passerait-il", "si jamais", "à la place de"],
    "causal":         ["pourquoi", "à cause de", "provoque", "entraîne", "cause"],
    "abductive":       ["j'imagine que", "probablement parce que", "explique pourquoi"],
    "analogical":      ["comme", "similaire à", "de la même façon que", "pareil que"],
    "inductive":       ["en général", "à chaque fois que", "d'habitude"],
    "deductive":       ["donc", "il faut", "je dois", "quelle est la meilleure"],
}

_COMPLEXITY_THRESHOLDS = {
    "simple":   {"max_steps": 2, "mode": "direct_response"},
    "medium":   {"max_steps": 4, "mode": "structured_response"},
    "complex":  {"max_steps": 7, "mode": "full_pipeline"},
    "critical": {"max_steps": 7, "mode": "full_pipeline + uncertainty_flag"},
}

# Bornes de score de confiance → bande d'action, cf. reasoning_engine.json::confidence_scoring
_CONFIDENCE_BANDS = (
    (0.8, "high",   "répondre directement"),
    (0.5, "medium", "répondre avec nuances"),
    (0.0, "low",    "signaler incertitude + demander clarification"),
)

# Séparateurs utilisés pour la décomposition heuristique en sous-questions
_DECOMPOSE_SPLIT = re.compile(r"\s*(?:\bet\b|\bpuis\b|;|\?)\s*", re.IGNORECASE)


@dataclass
class ReasoningResult:
    """Scaffolding de raisonnement produit pour un message utilisateur —
    consommé par response_generator/tool_calling, jamais affiché tel quel."""

    raw_input:          str        = ""
    complexity:          str        = "simple"   # simple | medium | complex | critical
    reasoning_mode:       str        = "deductive"
    sub_questions:        list[str]  = field(default_factory=list)
    retrieved_knowledge_ids: list[str] = field(default_factory=list)
    retrieved_memory_hits:   list[dict] = field(default_factory=list)
    contradictions:       list[dict]  = field(default_factory=list)
    confidence_score:      float      = 0.5
    confidence_band:       str        = "medium"
    confidence_action:      str        = "répondre avec nuances"
    llm_reasoning_context:  str        = ""


class ReasoningEngine:
    """
    Prépare le raisonnement en amont de la génération de réponse : classifie
    la complexité, décompose si besoin, récupère le contexte pertinent
    (knowledge base + mémoire épisodique), et estime une confiance.

    Usage :
        engine = ReasoningEngine()
        result = engine.analyze("pourquoi je suis toujours fatiguée l'après-midi ?")
        result.llm_reasoning_context  # à injecter dans le prompt système
    """

    def __init__(self):
        self._retrieval_engine = None
        self._retrieval_available = True
        log_event("ReasoningEngine initialisé")

    # ─────────────────────────────────────────────────────
    # Pipeline principal
    # ─────────────────────────────────────────────────────

    def analyze(
        self,
        user_input:    str,
        emotion_trend_concerning: bool = False,
        conversation_context:     dict[str, Any] | None = None,
    ) -> ReasoningResult:
        """
        Traite un message utilisateur et produit un ReasoningResult.

        Args:
            user_input                : message brut de l'utilisateur
            emotion_trend_concerning  : ctx.emotion_trend_concerning du
                                        RegulationEngine — une tendance
                                        difficile abaisse la confiance et
                                        pousse vers un mode plus prudent
            conversation_context      : contexte conversationnel optionnel
                                        transmis tel quel au retrieval engine

        Returns:
            ReasoningResult — prêt à être injecté dans le prompt LLM
        """
        result = ReasoningResult(raw_input=user_input)

        if not isinstance(user_input, str) or not user_input.strip():
            result.confidence_score = 0.0
            self._apply_confidence(result)
            return result

        self._classify(result, user_input)
        self._decompose(result, user_input)
        self._retrieve(result, user_input, conversation_context)
        self._reason(result, user_input)
        self._evaluate(result, emotion_trend_concerning)
        self._synthesize(result)

        return result

    # ─────────────────────────────────────────────────────
    # Étapes internes
    # ─────────────────────────────────────────────────────

    def _classify(self, result: ReasoningResult, text: str) -> None:
        """Estime la complexité par heuristique — longueur, ponctuation,
        nombre de propositions. Pas de ML (sobriété niveau 0)."""
        length = len(text)
        n_clauses = len(_DECOMPOSE_SPLIT.split(text))
        n_questions = text.count("?")

        if length < 40 and n_clauses <= 1:
            result.complexity = "simple"
        elif length < 150 and n_clauses <= 2:
            result.complexity = "medium"
        elif n_questions >= 2 or n_clauses >= 3:
            result.complexity = "critical"
        else:
            result.complexity = "complex"

    def _decompose(self, result: ReasoningResult, text: str) -> None:
        """Découpe en sous-questions si la complexité le justifie — jamais
        pour 'simple' (surcoût inutile pour une demande directe)."""
        if result.complexity == "simple":
            return
        parts = [p.strip() for p in _DECOMPOSE_SPLIT.split(text) if p.strip()]
        result.sub_questions = parts if len(parts) > 1 else []

    def _retrieve(
        self,
        result: ReasoningResult,
        text: str,
        conversation_context: dict[str, Any] | None,
    ) -> None:
        """Récupère le contexte pertinent — knowledge base (B18) + mémoire
        épisodique (RAG). Best-effort : chaque source est optionnelle et ne
        doit jamais faire échouer le pipeline (même principe que
        RegulationEngine._apply_emotion pour emotional_trend)."""
        try:
            if self._retrieval_available:
                if self._retrieval_engine is None:
                    from src.knowledge.retrieval_engine import KnowledgeRetrievalEngine
                    self._retrieval_engine = KnowledgeRetrievalEngine()
                retrieval = self._retrieval_engine.retrieve(
                    query=text, conversation_context=conversation_context or {}
                )
                result.retrieved_knowledge_ids = retrieval.knowledge_ids
                result.contradictions = retrieval.contradictions
        except Exception as e:
            self._retrieval_available = False
            log_event(f"ReasoningEngine : knowledge retrieval indisponible — {e}", "WARNING")

        try:
            from src.memory.rag_stub import is_rag_available, semantic_search
            if is_rag_available():
                result.retrieved_memory_hits = semantic_search(text, n_results=3)
        except Exception as e:
            log_event(f"ReasoningEngine : RAG sémantique indisponible — {e}", "WARNING")

    def _reason(self, result: ReasoningResult, text: str) -> None:
        """Sélectionne le mode de raisonnement par mots-clés — heuristique,
        pas une classification sémantique. 'deductive' par défaut."""
        lowered = text.lower()
        for mode, keywords in _MODE_KEYWORDS.items():
            if any(kw in lowered for kw in keywords):
                result.reasoning_mode = mode
                return
        result.reasoning_mode = "deductive"

    def _evaluate(self, result: ReasoningResult, emotion_trend_concerning: bool) -> None:
        """Score de confiance : part d'un score neutre, ajusté par les
        signaux disponibles. Volontairement conservateur — mieux vaut sous-
        estimer la confiance que sur-affirmer (cf. limites_ia/hallucinations)."""
        score = 0.6

        if result.retrieved_knowledge_ids:
            score += 0.15
        if result.retrieved_memory_hits:
            score += 0.1
        if result.contradictions:
            score -= 0.3
        if result.complexity == "critical":
            score -= 0.15
        if emotion_trend_concerning:
            # Pas un signal de fiabilité factuelle, mais une raison d'être
            # plus prudent et plus nuancé plutôt que sûr de soi.
            score -= 0.1

        result.confidence_score = max(0.0, min(1.0, round(score, 2)))
        self._apply_confidence(result)

    def _apply_confidence(self, result: ReasoningResult) -> None:
        for threshold, band, action in _CONFIDENCE_BANDS:
            if result.confidence_score >= threshold:
                result.confidence_band = band
                result.confidence_action = action
                return
        result.confidence_band = "low"
        result.confidence_action = _CONFIDENCE_BANDS[-1][2]

    def _synthesize(self, result: ReasoningResult) -> None:
        """Construit les directives à injecter dans le prompt LLM — même
        principe que RegulationEngine._build_llm_context."""
        lines = [f"[Raisonnement : complexité {result.complexity}, mode {result.reasoning_mode}]"]

        if result.sub_questions:
            lines.append("Sous-questions à traiter : " + " / ".join(result.sub_questions))

        if result.retrieved_knowledge_ids:
            lines.append(f"Connaissances pertinentes disponibles : {', '.join(result.retrieved_knowledge_ids[:5])}")

        if result.contradictions:
            lines.append(
                "ATTENTION : des contradictions ont été détectées entre plusieurs "
                "sources de connaissance — les signaler avec prudence plutôt que "
                "trancher arbitrairement."
            )

        if result.confidence_band == "low":
            lines.append(
                "CONFIANCE FAIBLE : signaler l'incertitude explicitement et, si "
                "pertinent, demander une clarification plutôt que d'affirmer."
            )
        elif result.confidence_band == "medium":
            lines.append("Confiance modérée : nuancer la réponse, éviter les affirmations catégoriques.")

        result.llm_reasoning_context = "\n".join(lines)


# ─────────────────────────────────────────────────────────
# Singleton session
# ─────────────────────────────────────────────────────────

_engine: ReasoningEngine | None = None


def get_reasoning_engine() -> ReasoningEngine:
    """Retourne l'instance singleton du moteur de raisonnement."""
    global _engine
    if _engine is None:
        _engine = ReasoningEngine()
    return _engine


def analyze_reasoning(
    user_input: str,
    emotion_trend_concerning: bool = False,
    conversation_context: dict[str, Any] | None = None,
) -> ReasoningResult:
    """Point d'entrée simplifié — voir ReasoningEngine.analyze()."""
    return get_reasoning_engine().analyze(user_input, emotion_trend_concerning, conversation_context)
