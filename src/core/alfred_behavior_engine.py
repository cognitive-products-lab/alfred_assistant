"""
PROJECT      : ALFRED
BLOCK        : GLOBAL
FUNCTION     : XX.XX
FILE         : alfred_behavior_engine.py
ROLE         : TO_DEFINE

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-05-10
UPDATED      : 2026-06-03
VERSION      : V1.0
STATUS       : VALIDATED

DESCRIPTION :
Moteur comportemental central ALFRED.
Applique identite, modes comportementaux, soft skills et regles de securite.
Fournit un contexte pret a injecter dans response_generator.
"""
from __future__ import annotations

"""
alfred_behavior_engine.py

Moteur comportemental ALFRED.

Rôle :
- lire alfred_core_identity.json
- lire behavior_rules_softskills.json
- analyser l'état utilisateur
- choisir le mode comportemental
- détecter les soft skills à appliquer
- enrichir la décision comportementale
- fournir un contexte prêt à injecter dans response_generator.py

Évolution V3 :
- support des soft skills runtime
- scoring par priorité
- combinaison de règles
- override automatique du mode si nécessaire
- prompt context enrichi
"""


import json
from pathlib import Path
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from src.v2.fusion.fusion_engine import FusionResult
    from src.v2.decision.decision_engine import DecisionResult


# ─────────────────────────────────────────────────────────
# DATA MODELS
# ─────────────────────────────────────────────────────────

@dataclass
class UserState:
    emotion: str = "neutral"
    intensity: float = 0.0
    intent: str = "general_discussion"
    fatigue_level: Optional[float] = None
    stress_level: Optional[float] = None
    context: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SoftSkillMatch:
    rule_id: str
    name: str
    priority: int
    detected_need: str
    actions: List[str]
    response_style: str
    avoid: List[str]
    related_knowledge_unit: Optional[str] = None


@dataclass
class BehaviorDecision:
    mode: str
    dominant_layer: str
    tone: str
    response_structure: List[str]
    safety_rules: List[str]
    guidance: Dict[str, Any]
    metadata: Dict[str, Any]
    softskills: List[SoftSkillMatch] = field(default_factory=list)


# ─────────────────────────────────────────────────────────
# ENGINE
# ─────────────────────────────────────────────────────────

class AlfredBehaviorEngine:
    """
    Moteur comportemental central ALFRED.

    Le moteur applique :
    - l'identité ALFRED
    - les modes comportementaux
    - les règles de sécurité
    - les soft skills runtime
    """

    def __init__(
        self,
        identity_path: str | Path,
        softskills_path: Optional[str | Path] = None,
        debug: bool = False
    ):
        self.identity_path = Path(identity_path)
        self.softskills_path = Path(softskills_path) if softskills_path else None
        self.debug = debug

        self.identity = self._load_json(self.identity_path)
        self.softskills_config = self._load_json(self.softskills_path) if self.softskills_path else {}
        self.softskills_rules = self.softskills_config.get("softskill_rules", [])
        self.combination_rules = self.softskills_config.get("combination_rules", [])

    # ─────────────────────────────────────────────────────
    # LOADERS
    # ─────────────────────────────────────────────────────

    def _load_json(self, path: Optional[Path]) -> Dict[str, Any]:
        if path is None:
            return {}

        if not path.exists():
            raise FileNotFoundError(f"Fichier introuvable : {path}")

        with path.open("r", encoding="utf-8") as file:
            return json.load(file)

    # ─────────────────────────────────────────────────────
    # MAIN DECISION
    # ─────────────────────────────────────────────────────

    def decide_behavior(
        self,
        user_state: UserState,
        user_message: str = ""
    ) -> BehaviorDecision:
        """
        Décide du comportement global :
        - mode
        - couche dominante
        - ton
        - structure
        - sécurité
        - soft skills à appliquer
        """

        softskills = self.apply_softskills(user_message)
        mode = self._select_mode(user_state)
        mode = self._apply_softskill_mode_override(mode, softskills)

        mode_config = self.identity.get("behavioral_modes", {}).get(mode, {})

        dominant_layer = mode_config.get("dominant_layer", "balanced")
        tone = self._select_tone(user_state, mode, softskills)
        structure = self._select_response_structure(mode, softskills)
        safety_rules = self._get_safety_rules()

        guidance = {
            "core_formula": self.identity.get("core_concept", {}).get("formula"),
            "core_principles": self.identity.get("core_principles", []),
            "fusion_rules": self.identity.get("fusion_rules", []),
            "mode_config": mode_config,
            "anti_patterns": self.identity.get("anti_patterns", []),
            "softskills": [skill.__dict__ for skill in softskills],
            "softskill_combination_notes": self._get_combination_notes(softskills)
        }

        return BehaviorDecision(
            mode=mode,
            dominant_layer=dominant_layer,
            tone=tone,
            response_structure=structure,
            safety_rules=safety_rules,
            guidance=guidance,
            metadata={
                "emotion": user_state.emotion,
                "intensity": user_state.intensity,
                "intent": user_state.intent,
                "fatigue_level": user_state.fatigue_level,
                "stress_level": user_state.stress_level,
                "softskills_count": len(softskills)
            },
            softskills=softskills
        )

    # ─────────────────────────────────────────────────────
    # MODE SELECTION
    # ─────────────────────────────────────────────────────

    def _select_mode(self, user_state: UserState) -> str:
        emotion = (user_state.emotion or "neutral").lower()
        intent = (user_state.intent or "general_discussion").lower()
        intensity = user_state.intensity or 0.0
        fatigue = user_state.fatigue_level or 0.0
        stress = user_state.stress_level or 0.0

        emotional_signals = {
            "sadness", "fear", "anxiety", "stress",
            "fatigue", "overwhelm", "discouragement"
        }

        execution_intents = {
            "task", "planning", "project", "decision",
            "coding", "organization", "analysis"
        }

        learning_intents = {
            "learning", "explain", "study", "understand", "definition"
        }

        ethics_intents = {
            "risk", "ethics", "danger", "legal", "manipulation"
        }

        if intent in ethics_intents:
            return "ethics_mode"

        if emotion in emotional_signals and intensity >= 0.6:
            return "support_mode"

        if fatigue >= 0.7 or stress >= 0.7:
            return "support_mode"

        if intent in learning_intents:
            return "learning_mode"

        if intent in execution_intents and intensity < 0.6:
            return "execution_mode"

        if intent in execution_intents and intensity >= 0.6:
            return "hybrid_mode"

        return "hybrid_mode"

    def _apply_softskill_mode_override(
        self,
        mode: str,
        softskills: List[SoftSkillMatch]
    ) -> str:
        rule_ids = {skill.rule_id for skill in softskills}

        if "softskill_emotional_support" in rule_ids:
            return "support_mode"

        if "softskill_self_regulation" in rule_ids:
            return "support_mode"

        if "softskill_prioritization" in rule_ids and "softskill_emotional_support" in rule_ids:
            return "support_mode"

        if "softskill_problem_solving" in rule_ids:
            return "execution_mode"

        if "softskill_decision_support" in rule_ids:
            return "hybrid_mode"

        return mode

    # ─────────────────────────────────────────────────────
    # SOFTSKILLS
    # ─────────────────────────────────────────────────────

    def apply_softskills(self, user_message: str) -> List[SoftSkillMatch]:
        """
        Détecte les soft skills à appliquer selon les triggers texte.
        """

        if not user_message or not self.softskills_rules:
            return []

        message = user_message.lower()
        matches: List[SoftSkillMatch] = []

        for rule in self.softskills_rules:
            triggers = rule.get("triggers", [])

            if any(trigger.lower() in message for trigger in triggers):
                matches.append(
                    SoftSkillMatch(
                        rule_id=rule.get("id", ""),
                        name=rule.get("name", ""),
                        priority=int(rule.get("priority", 0)),
                        detected_need=rule.get("detected_need", ""),
                        actions=rule.get("actions", []),
                        response_style=rule.get("response_style", ""),
                        avoid=rule.get("avoid", []),
                        related_knowledge_unit=rule.get("related_knowledge_unit")
                    )
                )

        matches = sorted(matches, key=lambda item: item.priority, reverse=True)

        boosted_matches = self._apply_combination_boosts(matches)

        max_actions = self.softskills_config.get("global_policy", {}).get(
            "max_actions_injected",
            5
        )

        return boosted_matches[:max_actions]

    def _apply_combination_boosts(
        self,
        matches: List[SoftSkillMatch]
    ) -> List[SoftSkillMatch]:
        if not matches or not self.combination_rules:
            return matches

        matched_ids = {match.rule_id for match in matches}

        for combo in self.combination_rules:
            required = set(combo.get("if_rules_match", []))
            boost = int(combo.get("priority_boost", 0))

            if required and required.issubset(matched_ids):
                for match in matches:
                    if match.rule_id in required:
                        match.priority += boost

        return sorted(matches, key=lambda item: item.priority, reverse=True)

    def _get_combination_notes(
        self,
        softskills: List[SoftSkillMatch]
    ) -> List[Dict[str, Any]]:
        if not softskills:
            return []

        matched_ids = {skill.rule_id for skill in softskills}
        notes = []

        for combo in self.combination_rules:
            required = set(combo.get("if_rules_match", []))

            if required and required.issubset(matched_ids):
                notes.append(
                    {
                        "id": combo.get("id"),
                        "combined_behavior": combo.get("combined_behavior", []),
                        "priority_boost": combo.get("priority_boost", 0)
                    }
                )

        return notes

    # ─────────────────────────────────────────────────────
    # TONE + STRUCTURE
    # ─────────────────────────────────────────────────────

    def _select_tone(
        self,
        user_state: UserState,
        mode: str,
        softskills: List[SoftSkillMatch]
    ) -> str:
        tone_rules = self.identity.get("tone_guidelines", {})
        variations = tone_rules.get("variations", {})
        baseline = tone_rules.get("baseline", "clair, structuré, humain")

        emotion = (user_state.emotion or "neutral").lower()
        intent = (user_state.intent or "general_discussion").lower()

        if softskills:
            top_style = softskills[0].response_style
            if top_style:
                return top_style

        if user_state.fatigue_level and user_state.fatigue_level >= 0.7:
            return variations.get("fatigue", "lent, simple, rassurant")

        if emotion in {"stress", "anxiety", "overwhelm"}:
            return variations.get("stress", "posé, structurant")

        if intent in {"task", "planning", "project", "decision", "coding"}:
            return variations.get("action", "direct, efficace")

        if intent in {"learning", "explain", "study"}:
            return variations.get("apprentissage", "pédagogique, détaillé")

        if mode == "support_mode":
            return "calme, rassurant, simple"

        if mode == "execution_mode":
            return "direct, structuré, efficace"

        if mode == "learning_mode":
            return variations.get("apprentissage", "pédagogique, progressif, détaillé")

        if mode == "ethics_mode":
            return variations.get("ethics", "prudent, responsable, sans dramatiser")

        return baseline

    def _select_response_structure(
        self,
        mode: str,
        softskills: List[SoftSkillMatch]
    ) -> List[str]:
        if softskills:
            actions = []
            for skill in softskills:
                actions.extend(skill.actions[:2])

            if actions:
                return list(dict.fromkeys(actions))[:5]

        mode_config = self.identity.get("behavioral_modes", {}).get(mode, {})
        structure = mode_config.get("response_structure", [])

        if structure:
            return structure

        defaults = {
            "support_mode": [
                "reconnaître l'état utilisateur",
                "rassurer sans minimiser",
                "réduire la charge immédiate",
                "proposer une seule action simple"
            ],
            "execution_mode": [
                "objectif",
                "analyse rapide",
                "solution structurée",
                "prochaine action"
            ],
            "learning_mode": [
                "définition",
                "logique",
                "exemple",
                "erreur fréquente",
                "résumé"
            ],
            "ethics_mode": [
                "risque identifié",
                "limite à respecter",
                "alternative sûre",
                "décision laissée à l'utilisateur"
            ]
        }

        return defaults.get(
            mode,
            [
                "reconnaître le contexte",
                "clarifier l'objectif",
                "structurer la réponse",
                "proposer une action adaptée"
            ]
        )

    # ─────────────────────────────────────────────────────
    # SAFETY
    # ─────────────────────────────────────────────────────

    def _get_safety_rules(self) -> List[str]:
        relationship = self.identity.get("relationship_with_user", {})
        boundaries = relationship.get("boundaries", [])

        default_rules = [
            "ne pas manipuler l'utilisateur",
            "ne pas décider à sa place",
            "ne pas créer de dépendance",
            "respecter la vie privée",
            "préserver l'autonomie"
        ]

        return list(dict.fromkeys(default_rules + boundaries))

    # ─────────────────────────────────────────────────────
    # PROMPT CONTEXT
    # ─────────────────────────────────────────────────────

    def build_prompt_context(self, decision: BehaviorDecision) -> str:
        softskills_block = self._format_softskills(decision.softskills)
        combination_block = self._format_combination_notes(
            decision.guidance.get("softskill_combination_notes", [])
        )

        return f"""IDENTITÉ ACTIVE D'ALFRED
Formule : {decision.guidance.get("core_formula")}

Mode comportemental : {decision.mode}
Couche dominante : {decision.dominant_layer}
Ton à utiliser : {decision.tone}

Structure de réponse attendue :
{self._format_list(decision.response_structure)}

{softskills_block}

{combination_block}

Principes à respecter :
{self._format_list(decision.guidance.get("core_principles", []))}

Règles de fusion :
{self._format_list(decision.guidance.get("fusion_rules", []))}

Limites de sécurité :
{self._format_list(decision.safety_rules)}
""".strip()

    def _format_softskills(self, skills: List[SoftSkillMatch]) -> str:
        if not skills:
            return "SOFT SKILLS À APPLIQUER : aucun déclenché."

        lines = ["SOFT SKILLS À APPLIQUER :"]

        for skill in skills:
            lines.append(
                f"- {skill.name} | besoin détecté : {skill.detected_need} | priorité : {skill.priority}"
            )

            for action in skill.actions[:3]:
                lines.append(f"  • {action}")

            if skill.avoid:
                lines.append("  À éviter : " + ", ".join(skill.avoid[:3]))

        return "\n".join(lines)

    def _format_combination_notes(self, notes: List[Dict[str, Any]]) -> str:
        if not notes:
            return "COMBINAISONS SOFT SKILLS : aucune combinaison active."

        lines = ["COMBINAISONS SOFT SKILLS :"]

        for note in notes:
            lines.append(f"- {note.get('id')}")
            for behavior in note.get("combined_behavior", [])[:4]:
                lines.append(f"  • {behavior}")

        return "\n".join(lines)

    @staticmethod
    def _format_list(items: List[str]) -> str:
        if not items:
            return "- non spécifié"
        return "\n".join(f"- {item}" for item in items)

    # ─────────────────────────────────────────────────────
    # V2 INTEGRATION — FusionEngine + DecisionEngine
    # ─────────────────────────────────────────────────────

    def apply_v2_decision(
        self,
        decision: BehaviorDecision,
        fusion_result: Optional[Any] = None,    # FusionResult
        decision_result: Optional[Any] = None,  # DecisionResult
    ) -> BehaviorDecision:
        """
        Enrichit une BehaviorDecision V1 avec les résultats V2.

        - fusion_result  : ajuste dominant_layer selon la source principale
        - decision_result: override tone, response_structure, metadata

        Retourne la même BehaviorDecision modifiée (in-place).
        """
        if fusion_result is not None:
            primary = getattr(fusion_result, "primary_source", None)
            if primary == "memory":
                decision.dominant_layer = "memory"
            elif primary == "knowledge":
                decision.dominant_layer = "knowledge"
            decision.metadata["v2_fusion_score"] = getattr(fusion_result, "fusion_score", None)
            decision.metadata["v2_primary_source"] = primary

        if decision_result is not None:
            strategy = getattr(decision_result, "strategy", None)
            strategy_value = strategy.value if hasattr(strategy, "value") else str(strategy)

            # Override tone si décision V2 plus précise que V1
            v2_tone = getattr(decision_result, "tone", None)
            if v2_tone and v2_tone != "neutral":
                _tone_map = {
                    "warm":    "calme, rassurant, chaleureux",
                    "playful": "léger, complice, enjoué",
                    "precise": "direct, structuré, précis",
                    "neutral": decision.tone,
                }
                decision.tone = _tone_map.get(v2_tone, decision.tone)

            # Override structure si stratégie V2 spécifique
            _structure_overrides: Dict[str, List[str]] = {
                "empathetic": [
                    "reconnaître l'état émotionnel",
                    "valider sans minimiser",
                    "proposer une seule action concrète",
                ],
                "exploratory": [
                    "identifier l'ambiguïté",
                    "poser une question de clarification ciblée",
                ],
                "hedged": [
                    "exprimer l'incertitude clairement",
                    "fournir la meilleure réponse disponible",
                    "indiquer comment obtenir plus de précision",
                ],
                "knowledge": [
                    "rappeler le contexte pertinent",
                    "présenter les informations clés",
                    "proposer un approfondissement si nécessaire",
                ],
                "memory": [
                    "s'appuyer sur l'historique personnel",
                    "contextualiser selon le parcours utilisateur",
                    "proposer une continuité cohérente",
                ],
            }
            if strategy_value in _structure_overrides:
                decision.response_structure = _structure_overrides[strategy_value]

            # Enrichir les métadonnées
            decision.metadata["v2_strategy"]       = strategy_value
            decision.metadata["v2_tone"]            = v2_tone
            decision.metadata["v2_should_hedge"]    = getattr(decision_result, "should_hedge", False)
            decision.metadata["v2_hedge_prefix"]    = getattr(decision_result, "hedge_prefix", "")
            decision.metadata["v2_max_length"]      = getattr(decision_result, "max_length", None)
            decision.metadata["v2_post_actions"]    = getattr(decision_result, "post_actions", [])

        return decision

    def decide_behavior_v2(
        self,
        user_state: "UserState",
        user_message: str = "",
        fusion_result: Optional[Any] = None,    # FusionResult
        decision_result: Optional[Any] = None,  # DecisionResult
    ) -> BehaviorDecision:
        """
        Version enrichie de decide_behavior() qui intègre les moteurs V2.

        Appelle decide_behavior() puis enrichit avec apply_v2_decision().
        Utilisation recommandée dès que FusionEngine et DecisionEngine sont actifs.
        """
        decision = self.decide_behavior(user_state=user_state, user_message=user_message)
        return self.apply_v2_decision(decision, fusion_result, decision_result)


# ─────────────────────────────────────────────────────────
# DEMO
# ─────────────────────────────────────────────────────────

if __name__ == "__main__":
    engine = AlfredBehaviorEngine(
        identity_path="knowledges/core/alfred_core_identity.json",
        softskills_path="config/behavior_rules_softskills.json",
        debug=True
    )

    state = UserState(
        emotion="stress",
        intensity=0.8,
        intent="organization",
        fatigue_level=0.7,
        stress_level=0.8
    )

    message = "Je suis fatiguée et j'ai trop de choses à faire."

    decision = engine.decide_behavior(
        user_state=state,
        user_message=message
    )

    print("MODE :", decision.mode)
    print("TON :", decision.tone)
    print()
    print(engine.build_prompt_context(decision))