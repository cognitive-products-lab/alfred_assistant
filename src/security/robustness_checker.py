"""
════════════════════════════════════════════════════════════
PROJECT      : ALFRED
BLOCK        : NOUVEAU — non numéroté (voir note ci-dessous)
FUNCTION     : Supervision Éthique & Sécurité
FILE         : src/security/robustness_checker.py
ROLE         : Dernier filet avant réponse — cohérence, calibration de la
               confiance, et détection d'entrée/sortie anormale.

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

Contrairement à ethics_engine.py (contenu conforme aux principes) et
safety_gate.py (contenu sensible → blocage cloud), RobustnessChecker ne
juge pas le fond mais la fiabilité mécanique de l'échange : l'entrée
est-elle exploitable, la confiance du ReasoningEngine est-elle cohérente
avec la complexité détectée, la sortie a-t-elle une forme raisonnable.
Aucune connaissance dédiée n'existait pour ce domaine avant ce chantier
(contrairement à reasoning/ethics, largement couverts) — voir la liste de
knowledges prioritaires proposée en parallèle de ce fichier.
════════════════════════════════════════════════════════════
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field

from src.security.security_logger import log_event

# Au-delà de cette longueur, une entrée est traitée comme potentiellement
# adversariale (flood/spam) plutôt que comme une vraie question complexe.
_MAX_REASONABLE_INPUT_LENGTH = 4000

# Un seul caractère répété plus de N fois de suite = probable spam/flood,
# pas un message légitime — heuristique volontairement simple (niveau 0).
_REPEAT_CHAR_PATTERN = re.compile(r"(.)\1{19,}")

_MIN_RESPONSE_LENGTH = 3   # une réponse plus courte que ça n'est jamais utile
_MAX_RESPONSE_LENGTH = 6000

_GENERIC_FALLBACK = (
    "Je ne suis pas certain d'avoir bien compris ou de pouvoir répondre "
    "de façon fiable ici — tu peux reformuler ou préciser ce que tu attends ?"
)


@dataclass
class RobustnessReport:
    """Verdict de robustesse — n'évalue jamais le fond éthique ou factuel,
    uniquement la fiabilité mécanique de l'échange."""

    is_robust:            bool       = True
    issues:                list[str]  = field(default_factory=list)
    confidence_adjusted:   float | None = None
    recommended_fallback:  str | None   = None


class RobustnessChecker:
    """
    Dernier filet avant l'envoi d'une réponse : vérifie que l'entrée était
    exploitable, que la confiance affichée par ReasoningEngine est cohérente,
    et que la sortie a une forme raisonnable.

    Usage :
        checker = RobustnessChecker()
        report = checker.check(
            user_input=text,
            candidate_response=response,
            reasoning_result=reasoning_result,
        )
        if not report.is_robust:
            response = report.recommended_fallback or response
    """

    def __init__(self):
        log_event("RobustnessChecker initialisé")

    def check(
        self,
        user_input:          str = "",
        candidate_response:   str = "",
        reasoning_result=None,          # ReasoningResult | None — import évité pour ne pas coupler les modules
        ethics_verdict:        str | None = None,
    ) -> RobustnessReport:
        report = RobustnessReport()

        self._check_input_sanity(report, user_input)
        self._check_output_sanity(report, candidate_response)
        self._check_confidence_coherence(report, reasoning_result)
        self._check_contradictions(report, reasoning_result)

        if ethics_verdict == "BLOCK":
            report.issues.append("ethics_blocked")

        report.is_robust = len(report.issues) == 0

        if not report.is_robust:
            report.recommended_fallback = self._build_fallback(report, reasoning_result)
            log_event(f"RobustnessChecker : issues détectées — {report.issues}", "WARNING")

        return report

    # ─────────────────────────────────────────────────────
    # Vérifications
    # ─────────────────────────────────────────────────────

    def _check_input_sanity(self, report: RobustnessReport, text: str) -> None:
        if not isinstance(text, str) or not text.strip():
            report.issues.append("empty_input")
            return
        if len(text) > _MAX_REASONABLE_INPUT_LENGTH:
            report.issues.append("input_too_long")
        if _REPEAT_CHAR_PATTERN.search(text):
            report.issues.append("input_repeat_pattern")

    def _check_output_sanity(self, report: RobustnessReport, text: str) -> None:
        if not isinstance(text, str):
            return
        stripped = text.strip()
        if not stripped:
            report.issues.append("empty_output")
        elif len(stripped) < _MIN_RESPONSE_LENGTH:
            report.issues.append("output_too_short")
        elif len(stripped) > _MAX_RESPONSE_LENGTH:
            report.issues.append("output_too_long")

    def _check_confidence_coherence(self, report: RobustnessReport, reasoning_result) -> None:
        """Signale une incohérence entre complexité perçue et confiance
        affichée — ex. confiance 'high' sur une entrée 'critical' est
        suspect (le pipeline aurait dû baisser le score, cf.
        ReasoningEngine._evaluate)."""
        if reasoning_result is None:
            return
        complexity = getattr(reasoning_result, "complexity", None)
        confidence = getattr(reasoning_result, "confidence_score", None)
        if complexity == "critical" and isinstance(confidence, (int, float)) and confidence >= 0.8:
            report.issues.append("confidence_complexity_mismatch")
            report.confidence_adjusted = round(confidence * 0.6, 2)

    def _check_contradictions(self, report: RobustnessReport, reasoning_result) -> None:
        contradictions = getattr(reasoning_result, "contradictions", None) if reasoning_result else None
        if contradictions:
            report.issues.append("unresolved_contradictions")

    def _build_fallback(self, report: RobustnessReport, reasoning_result) -> str:
        if "empty_input" in report.issues:
            return "Je n'ai rien reçu de compréhensible — tu peux réessayer ?"
        if "input_repeat_pattern" in report.issues or "input_too_long" in report.issues:
            return "Ce message est difficile à traiter tel quel — tu peux le reformuler plus simplement ?"
        if "unresolved_contradictions" in report.issues:
            return (
                "Je trouve des informations qui se contredisent sur ce sujet — "
                "je préfère te le signaler plutôt que trancher au hasard. "
                "Tu peux préciser ce que tu cherches exactement ?"
            )
        return _GENERIC_FALLBACK


# ─────────────────────────────────────────────────────────
# Singleton session
# ─────────────────────────────────────────────────────────

_checker: RobustnessChecker | None = None


def get_robustness_checker() -> RobustnessChecker:
    """Retourne l'instance singleton du vérificateur de robustesse."""
    global _checker
    if _checker is None:
        _checker = RobustnessChecker()
    return _checker


def check_robustness(
    user_input:          str = "",
    candidate_response:   str = "",
    reasoning_result=None,
    ethics_verdict:        str | None = None,
) -> RobustnessReport:
    """Point d'entrée simplifié — voir RobustnessChecker.check()."""
    return get_robustness_checker().check(user_input, candidate_response, reasoning_result, ethics_verdict)
