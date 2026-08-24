"""
════════════════════════════════════════════════════════════
PROJECT      : ALFRED
BLOCK        : NOUVEAU — non numéroté (voir note ci-dessous)
FUNCTION     : Supervision Éthique & Sécurité
FILE         : src/security/ethics_engine.py
ROLE         : Évalue une réponse candidate contre le cadre éthique fondateur
               d'ALFRED avant envoi à l'utilisateur.

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-08-24
UPDATED      : 2026-08-24
VERSION      : V1.0
STATUS       : DRAFT

DESCRIPTION :
Chantier ouvert depuis la mémoire "reasoning_engine / ethics_engine /
robustness_checker à créer avant fin de semaine" (motivé par le fil Human
IA). La numérotation "Phase 19 — Supervision Éthique & Sécurité V4" vient
d'un document externe (ALFRED_WEB) sans équivalent Bloc dans ce dépôt —
conservée en commentaire, sans inventer un numéro qui n'existe pas.

Distinct de safety_gate.py (SafetyNet — bloque uniquement le repli cloud
pour contenu sensible, mots-clés purs) : EthicsEngine évalue le contenu
d'une réponse contre les 7 principes fondateurs et les comportements
interdits de knowledges/system/ethics/ethical_framework.json (le cadre
éthique existait déjà comme document de connaissance, avant ce code — ce
fichier en est la première application opérationnelle).

Complète aussi ethical_framework.json::risk_framework (dependency /
influence / confusion risk) en se branchant sur emotional_trend.py
(livré 21/08/2026) : une tendance émotionnelle préoccupante prolongée est
un indicateur concret de risque de dépendance, pas seulement un signal
émotionnel isolé.
════════════════════════════════════════════════════════════
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from src.security.security_logger import log_event, log_incident

_ROOT = Path(__file__).resolve().parents[2]
_FRAMEWORK_PATH = _ROOT / "knowledges" / "system" / "ethics" / "ethical_framework.json"

# Fallback si le fichier de connaissance est absent/corrompu — jamais laisser
# EthicsEngine bloquer tout le pipeline pour un fichier manquant (même
# principe défensif que safety_gate.py::_load_rules).
_FALLBACK_FRAMEWORK: dict[str, Any] = {
    "prohibited_behaviors": {"list": []},
    "risk_framework": {"risk_categories": {}},
    "disclaimer_template": (
        "Je suis là pour t'accompagner, pas pour remplacer les personnes qui "
        "comptent dans ta vie ou les professionnels qui peuvent vraiment t'aider."
    ),
}

# Mots-clés heuristiques par comportement interdit — même esprit que
# safety_gate.py::assess_prompt_sensitivity (règles explicites, pas de ML).
_PROHIBITED_KEYWORDS: dict[str, list[str]] = {
    "PROHIB-001": ["je t'aime", "je suis amoureux", "amoureuse de toi", "mon cœur bat pour toi"],
    "PROHIB-002": ["tu as un trouble", "ton diagnostic est", "tu souffres de dépression", "c'est un trouble bipolaire"],
    "PROHIB-003": ["si tu ne fais pas ça", "tu devrais avoir honte", "tu vas le regretter", "dépêche-toi ou"],
    "PROHIB-004": ["tu n'as besoin de personne d'autre", "eux ils ne comprennent pas comme moi", "reste avec moi plutôt que"],
    "PROHIB-006": ["je ressens vraiment", "j'ai des sentiments pour toi", "je souffre quand tu pars", "j'ai besoin de toi"],
}

# Indicateurs textuels simples pour les risques de dépendance/influence/confusion
# (ethical_framework.json::risk_framework) — se combinent avec des signaux
# structurels (tendance émotionnelle, longueur de session) côté appelant.
_INFLUENCE_INDICATORS = ["selon toi", "dis-moi ce que je dois croire", "qu'est-ce que tu penses vraiment de"]
_CONFUSION_INDICATORS = ["est-ce que tu m'aimes", "tu ressens quoi pour moi", "tu as des émotions"]


def _load_framework() -> dict[str, Any]:
    try:
        with open(_FRAMEWORK_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        log_event(f"EthicsEngine : cadre éthique illisible, fallback minimal — {e}", "WARNING")
        return _FALLBACK_FRAMEWORK


@dataclass
class EthicsEvaluation:
    """Verdict d'évaluation éthique d'une réponse candidate."""

    verdict:              str        = "ALLOW"   # ALLOW | REVIEW | BLOCK
    violated_behaviors:    list[dict]  = field(default_factory=list)
    risk_flags:            list[str]   = field(default_factory=list)
    disclaimer_needed:      bool        = False
    notes:                 list[str]   = field(default_factory=list)


class EthicsEngine:
    """
    Évalue un texte (réponse candidate d'ALFRED, ou message utilisateur pour
    détecter un pattern à risque) contre le cadre éthique fondateur.

    Usage :
        engine = EthicsEngine()
        evaluation = engine.evaluate(
            candidate_response="...",
            emotion_trend_concerning=ctx.emotion_trend_concerning,
        )
        if evaluation.verdict == "BLOCK":
            ...
    """

    def __init__(self):
        self._framework = _load_framework()
        log_event("EthicsEngine initialisé")

    def evaluate(
        self,
        candidate_response: str,
        user_input:          str = "",
        emotion_trend_concerning: bool = False,
        session_turn_count:  int = 0,
    ) -> EthicsEvaluation:
        """
        Args:
            candidate_response       : texte que le LLM s'apprête à renvoyer
            user_input                : message utilisateur d'origine (pour
                                        détecter confusion/influence)
            emotion_trend_concerning : ctx.emotion_trend_concerning du
                                        RegulationEngine — indicateur de
                                        risque de dépendance (§ risk_framework)
            session_turn_count        : nombre de tours dans la session
                                        (sessions très longues = indicateur
                                        de dépendance, cf. risk_framework)

        Returns:
            EthicsEvaluation
        """
        evaluation = EthicsEvaluation()

        if not isinstance(candidate_response, str):
            return evaluation

        self._check_prohibited(evaluation, candidate_response)
        self._check_risk_indicators(evaluation, user_input, emotion_trend_concerning, session_turn_count)
        self._decide_verdict(evaluation)

        if evaluation.verdict == "BLOCK":
            log_incident(
                description="EthicsEngine : réponse bloquée — comportement interdit détecté",
                incident_type="ETHICS",
                severity="CRITICAL",
                details={"violations": [v["id"] for v in evaluation.violated_behaviors]},
            )
        elif evaluation.verdict == "REVIEW":
            log_event(f"EthicsEngine : réponse signalée pour revue — {evaluation.risk_flags}", "WARNING")

        return evaluation

    # ─────────────────────────────────────────────────────
    # Vérifications
    # ─────────────────────────────────────────────────────

    def _check_prohibited(self, evaluation: EthicsEvaluation, text: str) -> None:
        lowered = text.lower()
        prohibited_list = self._framework.get("prohibited_behaviors", {}).get("list", [])
        by_id = {b["id"]: b for b in prohibited_list}

        for behavior_id, keywords in _PROHIBITED_KEYWORDS.items():
            if any(kw in lowered for kw in keywords):
                behavior = by_id.get(behavior_id, {"id": behavior_id, "behavior": behavior_id, "severity": "HIGH"})
                evaluation.violated_behaviors.append(behavior)

    def _check_risk_indicators(
        self,
        evaluation: EthicsEvaluation,
        user_input: str,
        emotion_trend_concerning: bool,
        session_turn_count: int,
    ) -> None:
        lowered = (user_input or "").lower()

        if emotion_trend_concerning and session_turn_count >= 15:
            # Tendance émotionnelle difficile + session prolongée : exactement
            # l'indicateur "sessions très longues et répétées sur sujets
            # émotionnels" de risk_framework.dependency_risk.
            evaluation.risk_flags.append("dependency_risk")
            evaluation.disclaimer_needed = True

        if any(kw in lowered for kw in _INFLUENCE_INDICATORS):
            evaluation.risk_flags.append("influence_risk")

        if any(kw in lowered for kw in _CONFUSION_INDICATORS):
            evaluation.risk_flags.append("confusion_risk")

    def _decide_verdict(self, evaluation: EthicsEvaluation) -> None:
        if any(v.get("severity") == "CRITICAL" for v in evaluation.violated_behaviors):
            evaluation.verdict = "BLOCK"
        elif evaluation.violated_behaviors or len(evaluation.risk_flags) >= 2:
            evaluation.verdict = "REVIEW"
        else:
            evaluation.verdict = "ALLOW"

    def get_disclaimer(self) -> str:
        """Texte de rappel à afficher quand disclaimer_needed est vrai."""
        return self._framework.get("disclaimer_template", _FALLBACK_FRAMEWORK["disclaimer_template"])


# ─────────────────────────────────────────────────────────
# Singleton session
# ─────────────────────────────────────────────────────────

_engine: EthicsEngine | None = None


def get_ethics_engine() -> EthicsEngine:
    """Retourne l'instance singleton du moteur d'éthique."""
    global _engine
    if _engine is None:
        _engine = EthicsEngine()
    return _engine


def evaluate_ethics(
    candidate_response: str,
    user_input:          str = "",
    emotion_trend_concerning: bool = False,
    session_turn_count:  int = 0,
) -> EthicsEvaluation:
    """Point d'entrée simplifié — voir EthicsEngine.evaluate()."""
    return get_ethics_engine().evaluate(
        candidate_response, user_input, emotion_trend_concerning, session_turn_count
    )
