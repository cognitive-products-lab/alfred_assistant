"""
PROJECT      : ALFRED
BLOCK        : B08 — Personnalité & Adaptation
FUNCTION     : 08.01 — Moteur d'adaptation de personnalité
FILE         : src/core/personality_adapter.py
ROLE         : Moteur central reliant personnalité ALFRED + profil utilisateur.
               Adapte le ton, le niveau émotionnel et la profondeur de réponse.
               Intègre les préférences MBTI/onboarding via _apply_user_adaptation().

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-05-01
UPDATED      : 2026-06-20
VERSION      : V1.2
STATUS       : VALIDATED

CHANGELOG V1.2 (20/06/2026) :
  - build_response_context() accepte user_adaptation (UserAdaptationContext)
  - _apply_user_adaptation() : enrichit ton, profondeur, règles depuis MBTI/onboarding
  - Nouvelle clé mbti_adaptation dans le contexte retourné (pour response_generator)
"""

import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

# Racine projet — variable de module (pas une constante figée dans la
# fonction) pour rester monkeypatchable en test (voir tests/b08_tests/
# test_personality_adapter.py::TestPrivatePersona).
_PROJECT_ROOT = Path(__file__).resolve().parents[2]


class PersonalityAdapter:
    """
    Moteur central reliant :
    - personality_core_*.json  (ou personality_core.json privé)
    - user_profile_*.json      (ou user_adaptation_profile.json)
    """

    def __init__(
        self,
        personality_path: str,
        user_profile_path: str,
        allow_templates: bool = False
    ):
        self.personality_path = Path(personality_path)
        self.user_profile_path = Path(user_profile_path)
        self.allow_templates = allow_templates

        self.personality_core = self._load_json(self.personality_path)
        self.user_profile = self._load_json(self.user_profile_path)

        if not self.allow_templates:
            self._validate_not_template(self.personality_core, "personality")
            self._validate_not_template(self.user_profile, "user_profile")

    # ─────────────────────────────────────────────────────
    # JSON
    # ─────────────────────────────────────────────────────

    def _load_json(self, path: Path) -> Dict[str, Any]:
        if not path.exists():
            raise FileNotFoundError(f"Fichier introuvable : {path}")
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"JSON invalide : {path}") from e

    def _save_json(self, path: Path, data: Dict[str, Any]) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    def _load_private_persona(self) -> Dict[str, Any]:
        """
        Charge data/profile/persona_private_<user_id>.json si présent —
        réglages de persona strictement locaux (jamais commités, voir
        .gitignore), absents par construction hors de l'instance privée de
        Céline. Contrairement à personality_path/user_profile_path, ce
        fichier est optionnel : son absence est normale (autre instance,
        déploiement public ALFRED_WEB) et ne doit jamais lever d'erreur.
        Trouvé le 17/08/2026 : ce fichier existe et contient flirtation_style
        (persona taquin/charme demandée le 18/07/2026) mais n'était lu par
        aucun code — la persona restait sans effet.
        """
        try:
            base = _PROJECT_ROOT
            user_id = self.user_profile.get("user_profile", {}).get("user_id", "") or ""
            candidates = [
                base / "data" / "profile" / f"persona_private_{user_id}.json",
                base / "data" / "profile" / "persona_private_celine.json",
            ]
            for path in candidates:
                if path.exists():
                    with open(path, "r", encoding="utf-8") as f:
                        return json.load(f).get("persona", {})
        except Exception:
            pass
        return {}

    # ─────────────────────────────────────────────────────
    # Validation
    # ─────────────────────────────────────────────────────

    def _validate_not_template(self, data: Dict[str, Any], file_type: str) -> None:
        """Empêche l'utilisation directe d'un template public."""
        is_template = data.get("metadata", {}).get("is_template", False)
        if is_template:
            raise ValueError(
                f"Le fichier chargé est un template public ({file_type}). "
                "Crée une instance réelle avant utilisation."
            )

    def validate_required_sections(self) -> None:
        """
        Vérifie les sections minimales — assoupli pour accepter
        personality_core.json privé (sans metadata).
        """
        # Sections minimales personality — metadata optionnel
        personality_required = [
            "assistant_identity",
            "stable_personality",
            "communication_style",
            "emotional_behavior",
            "boundaries"
        ]

        # Sections minimales user_profile — on accepte le format simplifié
        user_required = ["user_profile"]

        for section in personality_required:
            if section not in self.personality_core:
                raise KeyError(
                    f"Section manquante dans personality_core : {section}"
                )

        for section in user_required:
            if section not in self.user_profile:
                raise KeyError(
                    f"Section manquante dans user_profile : {section}"
                )

    # ─────────────────────────────────────────────────────
    # Création d'instances depuis templates
    # ─────────────────────────────────────────────────────

    @staticmethod
    def create_user_profile_from_template(
        template_path: str,
        output_directory: str,
        preferred_language: str = "fr"
    ) -> Path:
        """Crée un profil utilisateur réel depuis le template public."""
        template = Path(template_path)
        output_dir = Path(output_directory)

        if not template.exists():
            raise FileNotFoundError(f"Template introuvable : {template}")

        user_id = str(uuid.uuid4())
        output_path = output_dir / f"user_{user_id}.json"

        with open(template, "r", encoding="utf-8") as f:
            data = json.load(f)

        now = datetime.now().isoformat(timespec="seconds")
        data["user_profile"]["user_id"] = user_id
        data["user_profile"]["profile_status"] = "created"
        data["user_profile"]["language_preference"] = preferred_language
        data["user_profile"]["created_at"] = now
        data["user_profile"]["updated_at"] = now
        data["preferences"]["preferred_language"] = preferred_language
        data["metadata"]["is_template"] = False
        data["metadata"]["environment"] = "public_instance"

        output_dir.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        return output_path

    @staticmethod
    def create_personality_from_template(
        template_path: str,
        output_path: str,
        version_name: str = "v1_public"
    ) -> Path:
        """Crée une personnalité réelle depuis le template public."""
        template = Path(template_path)
        output = Path(output_path)

        if not template.exists():
            raise FileNotFoundError(f"Template introuvable : {template}")

        with open(template, "r", encoding="utf-8") as f:
            data = json.load(f)

        data["assistant_identity"]["version"] = version_name
        data["metadata"]["is_template"] = False
        data["metadata"]["environment"] = "public_instance"
        data["metadata"]["created_at"] = datetime.now().isoformat(timespec="seconds")

        output.parent.mkdir(parents=True, exist_ok=True)
        with open(output, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        return output

    # ─────────────────────────────────────────────────────
    # Détection du mode
    # ─────────────────────────────────────────────────────

    def detect_context_mode(
        self,
        user_message: str,
        detected_emotion: Optional[str] = None,
        energy_level: Optional[str] = None
    ) -> str:
        """Détermine le mode de réponse selon le message et le contexte."""
        message = user_message.lower().strip()

        if energy_level in ["low", "fatigue", "épuisé", "épuisée"]:
            return "low_energy_mode"

        if detected_emotion in ["stress", "anxiety", "sadness", "distress"]:
            return "emotional_support_light"

        technical_keywords = [
            "code", "python", "json", "fichier", "module",
            "classe", "fonction", "script", "architecture",
            "debug", "erreur", "terminal", "powershell"
        ]
        strategic_keywords = [
            "stratégie", "business", "roadmap", "investisseur",
            "produit", "marché", "financement", "bpi"
        ]
        learning_keywords = [
            "explique", "définir", "cours", "comprendre",
            "exemple", "méthode", "corriger", "devoir"
        ]
        creative_keywords = [
            "visuel", "logo", "concept", "design",
            "image", "storytelling", "post", "branding"
        ]
        support_keywords = [
            "fatiguée", "épuisée", "stressée", "j'en peux plus",
            "découragée", "j'ai du mal", "je n'y arrive pas",
            "bloquée", "perdue", "submergée"
        ]

        if any(kw in message for kw in support_keywords):
            return "emotional_support_light"
        if any(kw in message for kw in technical_keywords):
            return "technical_mode"
        if any(kw in message for kw in strategic_keywords):
            return "strategic_mode"
        if any(kw in message for kw in learning_keywords):
            return "learning_mode"
        if any(kw in message for kw in creative_keywords):
            return "creative_mode"

        return "neutral_assistant"

    # ─────────────────────────────────────────────────────
    # Niveau émotionnel
    # ─────────────────────────────────────────────────────

    def determine_emotional_level(
        self,
        detected_emotion: Optional[str] = None,
        energy_level: Optional[str] = None
    ) -> int:
        """Retourne un niveau émotionnel de 0 à 3.
        3 = sévère (distress, fear), 2 = modéré (sadness, stress, fatigue),
        1 = léger (mild_concern), 0 = neutre.
        """
        if detected_emotion in ["distress", "fear"]:
            return 3
        if detected_emotion in ["sadness", "stress", "anxiety"] or energy_level in ["low", "fatigue"]:
            return 2
        if detected_emotion in ["mild_concern"]:
            return 1
        return 0

    # ─────────────────────────────────────────────────────
    # Ton
    # ─────────────────────────────────────────────────────

    def determine_tone(
        self, 
        mode: str, 
        emotional_level: int = 0
        ) -> str:
        
        """Détermine le ton adapté au mode et à l'état émotionnel."""
        prefs = self.user_profile.get("preferences", {})

        if mode in ["low_energy_mode", "emotional_support_light"] and prefs.get("tone_when_fatigued"):
            return prefs["tone_when_fatigued"]
        if mode in ["technical_mode", "strategic_mode"] and prefs.get("tone_when_strategic"):
            return prefs["tone_when_strategic"]
        if mode == "learning_mode" and prefs.get("tone_when_learning"):
            return prefs["tone_when_learning"]
        if prefs.get("tone"):
            return prefs["tone"]

        tone_map = {
            "technical_mode": "clair, structuré, précis et pédagogique",
            "strategic_mode": "expert, direct, structuré et orienté décision",
            "learning_mode": "pédagogique, progressif et encourageant",
            "creative_mode": "créatif, stimulant et accessible",
            "low_energy_mode": "doux, simple, rassurant et sans surcharge",
            "emotional_support_light": "empathique, calme et soutenant",
        }

        if mode in tone_map:
            return tone_map[mode]

        if emotional_level >= 2:
            return "empathique, calme et soutenant"

        return self.personality_core.get("communication_style", {}).get(
            "default_tone", "clair, direct, structuré"
        )

# ─────────────────────────────────────────────────────
    # Profondeur de réponse
    # ─────────────────────────────────────────────────────

    def determine_response_depth(self, mode: str) -> str:
        """Détermine la profondeur de réponse."""
        user_pref = self.user_profile.get("preferences", {})
        if isinstance(user_pref, dict) and user_pref.get("response_length"):
            return user_pref["response_length"]

        if mode in ["technical_mode", "strategic_mode", "learning_mode"]:
            return "detailed"
        if mode in ["low_energy_mode", "emotional_support_light"]:
            return "short"
        return "medium"

    # ─────────────────────────────────────────────────────
    # Règles de réponse
    # ─────────────────────────────────────────────────────

    def build_response_rules(
        self,
        mode: str,
        emotional_level: int
    ) -> Dict[str, Any]:
        """Construit les règles comportementales finales."""
        rules = {
            "be_clear": True,
            "be_structured": True,
            "be_direct": True,
            "use_examples": False,
            "use_step_by_step": False,
            "avoid_overload": False,
            "use_empathy": emotional_level >= 2,
            "use_humor": False,
            "ask_questions_only_if_needed": True,
            "do_not_diagnose": True,
            "do_not_replace_professional_advice": True,
            "respect_privacy": True
        }

        mode_rules = {
            "technical_mode": {"use_step_by_step": True, "use_examples": True},
            "strategic_mode": {"use_examples": True, "be_direct": True},
            "learning_mode": {"use_step_by_step": True, "use_examples": True},
            "creative_mode": {"use_humor": True, "use_examples": True},
            "low_energy_mode": {"avoid_overload": True, "use_step_by_step": True, "use_humor": False},
            "emotional_support_light": {"avoid_overload": True, "use_humor": False}
        }

        rules.update(mode_rules.get(mode, {}))
        return rules

    # ─────────────────────────────────────────────────────
    # Contexte final pour response_generator
    # ─────────────────────────────────────────────────────

    def build_response_context(
        self,
        user_message: str,
        detected_emotion: Optional[str] = None,
        energy_level: Optional[str] = None,
        user_adaptation: Optional[Any] = None,
    ) -> Dict[str, Any]:
        """Produit le contexte complet à transmettre au générateur de réponse."""
        self.validate_required_sections()

        mode = self.detect_context_mode(
            user_message=user_message,
            detected_emotion=detected_emotion,
            energy_level=energy_level
        )
        emotional_level = self.determine_emotional_level(
            detected_emotion=detected_emotion,
            energy_level=energy_level
        )
        tone = self.determine_tone(mode=mode, emotional_level=emotional_level)
        response_depth = self.determine_response_depth(mode)
        response_rules = self.build_response_rules(
            mode=mode, emotional_level=emotional_level
        )

        identity = self.personality_core.get("assistant_identity", {})
        personality = self.personality_core.get("stable_personality", {})
        user = self.user_profile.get("user_profile", {})

        metadata = self.personality_core.get("metadata", {})
        rm = metadata.get("research_mode", {})
        research_active = rm.get("active", False) if isinstance(rm, dict) else bool(rm)

        private_persona = self._load_private_persona()

        context = {
            "assistant": {
                "name": identity.get("name", "ALFRED"),
                "version": identity.get("version", "V1"),
                "role": identity.get("role", "assistant virtuel adaptatif"),
                "mission": identity.get("mission", "accompagner et structurer."),
                "positioning": identity.get("core_positioning") or identity.get("positioning", "")
            },
            "personality": {
                "archetype": personality.get("archetype", "assistant_protecteur"),
                "dominant_traits": personality.get("dominant_traits", []),
                "forbidden_traits": personality.get("forbidden_traits", [])
            },
            "user": {
                "user_id": user.get("user_id"),
                "preferred_name": user.get("preferred_name", "utilisateur"),
                "language_preference": user.get("language_preference", "fr"),
                "profile_status": user.get("profile_status", "active")
            },
            "adaptation": {
                "mode": mode,
                "tone": tone,
                "response_depth": response_depth,
                "emotional_level": emotional_level,
                "detected_emotion": detected_emotion,
                "energy_level": energy_level
            },
            "communication_style": self.personality_core.get("communication_style", {}),
            "boundaries": self.personality_core.get("boundaries", {}),
            "safety": self.personality_core.get("safety", {}),
            "privacy_and_consent": self.user_profile.get("privacy_and_consent", {}),
            "response_rules": response_rules,
            "research_mode": research_active,
            "private_persona": private_persona,
        }

        if user_adaptation is not None:
            self._apply_user_adaptation(context, user_adaptation)

        return context

    # ─────────────────────────────────────────────────────
    # Adaptation MBTI / profil onboarding
    # ─────────────────────────────────────────────────────

    def _apply_user_adaptation(self, context: Dict[str, Any], ua: Any) -> None:
        """
        Enrichit le contexte avec les préférences MBTI et comm issues de l'onboarding.
        Surcharge uniquement ce que le profil indique explicitement.
        """
        adaptation = context["adaptation"]
        rules = context["response_rules"]

        # ── Profondeur de réponse ──────────────────────────────────────────────
        # health profile response_length_pref > personality processing_pref
        length_pref = getattr(ua, "response_length_pref", "adapt")
        processing  = getattr(ua, "processing_pref", "adapt")

        if length_pref and length_pref != "adapt":
            _length_map = {"short": "short", "medium": "medium",
                           "long": "detailed", "detailed": "detailed"}
            adaptation["response_depth"] = _length_map.get(length_pref, adaptation["response_depth"])
        elif processing and processing != "adapt":
            _proc_map = {"fast_scan": "short", "deep": "detailed",
                         "interactive": "medium"}
            adaptation["response_depth"] = _proc_map.get(processing, adaptation["response_depth"])

        # ── Ton ───────────────────────────────────────────────────────────────
        # On enrichit le ton existant avec des qualificatifs MBTI sans l'écraser
        tone_qualifiers: list[str] = []

        formality = getattr(ua, "formality_level", 2)
        if formality <= 1:
            tone_qualifiers.append("très familier")
        elif formality >= 4:
            tone_qualifiers.append("formel")

        if getattr(ua, "validate_first", False):
            tone_qualifiers.append("validant")

        if getattr(ua, "flexible_tone", False) and adaptation["mode"] not in (
            "low_energy_mode", "emotional_support_light"
        ):
            tone_qualifiers.append("souple")

        if tone_qualifiers:
            adaptation["tone"] = adaptation["tone"] + ", " + ", ".join(tone_qualifiers)

        # ── Règles comportementales ───────────────────────────────────────────
        if getattr(ua, "concrete_first", False):
            rules["use_examples"] = True

        if getattr(ua, "structured_resp", False):
            rules["be_structured"] = True

        if getattr(ua, "direct_feedback", False):
            rules["be_direct"] = True

        if getattr(ua, "validate_first", False):
            rules["validate_before_solve"] = True

        humor = getattr(ua, "humor_enabled", True)
        # Ne pas activer l'humour si le mode l'interdit déjà
        if not humor:
            rules["use_humor"] = False

        challenge = getattr(ua, "challenge_pref", "ask_question")
        rules["challenge_mode"] = challenge  # never / suggest / ask_question / direct

        # ── Section mbti_adaptation (pour response_generator) ─────────────────
        context["mbti_adaptation"] = {
            "mbti_type":           getattr(ua, "mbti_type", ""),
            "concrete_first":      getattr(ua, "concrete_first", False),
            "conceptual_first":    getattr(ua, "conceptual_first", False),
            "validate_first":      getattr(ua, "validate_first", False),
            "direct_feedback":     getattr(ua, "direct_feedback", False),
            "structured_resp":     getattr(ua, "structured_resp", False),
            "humor_enabled":       humor,
            "formality_level":     formality,
            "proactivity_pref":    getattr(ua, "proactivity_pref", "moderately_proactive"),
            "decision_support":    getattr(ua, "decision_support", "pros_cons"),
            "topics_avoid":        getattr(ua, "topics_avoid", []),
            "behaviors_avoid":     getattr(ua, "behaviors_avoid", []),
            "alfred_emotional_roles": getattr(ua, "alfred_emotional_roles", []),
            "when_distressed":     getattr(ua, "when_distressed", "ask_once"),
        }

    # ─────────────────────────────────────────────────────
    # Debug
    # ─────────────────────────────────────────────────────

    def print_response_context(
        self,
        user_message: str,
        detected_emotion: Optional[str] = None,
        energy_level: Optional[str] = None
    ) -> None:
        context = self.build_response_context(
            user_message=user_message,
            detected_emotion=detected_emotion,
            energy_level=energy_level
        )
        print(json.dumps(context, indent=4, ensure_ascii=False))

    def __repr__(self) -> str:
        name = self.personality_core.get(
            "assistant_identity", {}
        ).get("name", "ALFRED")
        user = self.user_profile.get(
            "user_profile", {}
        ).get("preferred_name", "?")
        return f"PersonalityAdapter(assistant={name}, user={user})"
