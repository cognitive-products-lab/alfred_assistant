"""
PROJECT      : ALFRED
BLOCK        : GLOBAL
FUNCTION     : XX.XX
FILE         : personality_adapter.py
ROLE         : TO_DEFINE

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-05-10
UPDATED      : 2026-05-13
VERSION      : V1.0
STATUS       : TESTED

DESCRIPTION :
Moteur d'adaptation de personnalite ALFRED.
Charge les profils JSON, detecte le mode contextuel, determine le ton
et construit le contexte de reponse pour response_generator.
"""

"""
personality_adapter.py
Moteur d'adaptation de personnalité pour ALFRED.

Rôle :
- Charger la personnalité stable d'ALFRED.
- Charger le profil utilisateur.
- Empêcher l'utilisation directe des templates publics.
- Adapter le ton, le niveau émotionnel et le mode de réponse.
- Préparer un contexte exploitable par response_generator.py.
"""

import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

# Import optionnel — évite la dépendance circulaire si health n'est pas disponible
try:
    from src.health.profile_loader import UserAdaptationContext
    _PROFILE_LOADER_AVAILABLE = True
except ImportError:
    UserAdaptationContext = None          # type: ignore
    _PROFILE_LOADER_AVAILABLE = False


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

    # Mapping nomenclature emotion_detector → modes personality_adapter
    _EMOTION_TO_MODE = {
        "distress":   "emotional_support_light",
        "stressed":   "emotional_support_light",
        "anxious":    "emotional_support_light",
        "sad":        "emotional_support_light",
        "grieving":   "emotional_support_light",
        "tired":      "low_energy_mode",
        "confused":   "emotional_support_light",
        "frustrated": "emotional_support_light",
        "motivated":  "technical_mode",
        "happy":      "neutral_assistant",
        "focused":    "technical_mode",
        "curious":    "learning_mode",
        "content":    "neutral_assistant",
        "neutral":    "neutral_assistant",
        # Ancienne nomenclature (rétrocompatibilité)
        "stress":     "emotional_support_light",
        "anxiety":    "emotional_support_light",
        "sadness":    "emotional_support_light",
        "fear":       "emotional_support_light",
    }

    _EMOTION_LEVEL = {
        "distress":   3,
        "grieving":   3,
        "stressed":   2,
        "anxious":    2,
        "sad":        2,
        "tired":      2,
        "frustrated": 1,
        "confused":   1,
        "motivated":  0,
        "happy":      0,
        "focused":    0,
        "curious":    0,
        "content":    0,
        "neutral":    0,
        # Ancienne nomenclature
        "stress":     2,
        "anxiety":    2,
        "sadness":    2,
        "fear":       3,
        "mild_concern": 1,
    }

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

        if detected_emotion and detected_emotion in self._EMOTION_TO_MODE:
            mode = self._EMOTION_TO_MODE[detected_emotion]
            if mode != "neutral_assistant":
                return mode

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
        """Retourne un niveau émotionnel de 0 à 3."""
        if energy_level in ["low", "fatigue"]:
            return 2
        if detected_emotion:
            return self._EMOTION_LEVEL.get(detected_emotion, 0)
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
        user_adaptation: Optional[Any] = None,   # UserAdaptationContext (optionnel)
    ) -> Dict[str, Any]:
        """
        Produit le contexte complet à transmettre au générateur de réponse.

        Args:
            user_message     : Message brut de l'utilisateur
            detected_emotion : Émotion détectée (depuis emotion_detector)
            energy_level     : Niveau d'énergie (depuis wellbeing_tracker)
            user_adaptation  : UserAdaptationContext (depuis profile_loader) — applique
                               les surcharges MBTI, préférences communication et frontières

        Returns:
            Dict contexte complet pour response_generator
        """
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

        # Déchiffrement transparent des champs Fernet
        user = dict(user)  # copie pour ne pas muter le profil chargé
        for field in ("preferred_name",):
            val = user.get(field, "")
            if isinstance(val, str) and val.startswith("gAAAAA"):
                try:
                    from src.security.encryption_service import decrypt
                    user[field] = decrypt(val) or user[field]
                except Exception:
                    pass

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
            "onboarding": {}   # peuplé si user_adaptation fourni
        }

        # Surcharges depuis le profil d'onboarding (MBTI, préférences, frontières)
        if user_adaptation is not None and _PROFILE_LOADER_AVAILABLE:
            self._merge_user_adaptation(context, user_adaptation)

        return context

    # ─────────────────────────────────────────────────────
    # Fusion profil onboarding → contexte
    # ─────────────────────────────────────────────────────

    def _merge_user_adaptation(self, context: Dict[str, Any], uc: Any) -> None:
        """
        Applique les surcharges du UserAdaptationContext au contexte de réponse.

        Règles de priorité :
          - Les préférences explicites de l'utilisateur (onboarding) priment
            sur les inférences mode/émotion pour humour, validation, ton, profondeur.
          - Les flags MBTI enrichissent response_rules et adaptation sans les écraser.
          - Les topics_avoid et behaviors_avoid enrichissent les boundaries.
        """
        rules  = context["response_rules"]
        adapt  = context["adaptation"]
        bounds = context["boundaries"]

        # ── Humour ────────────────────────────────────────
        if not uc.humor_enabled:
            rules["use_humor"] = False

        # ── Validation d'abord (TF + émotionnel) ─────────
        if uc.validate_first:
            rules["use_empathy"]           = True
            adapt["validate_first"]        = True

        # ── Profondeur de réponse ─────────────────────────
        length_map = {
            "very_short": "minimal",
            "short":      "short",
            "medium":     "medium",
            "adapt":      adapt.get("response_depth", "medium"),
        }
        pref_length = getattr(uc, "response_length_pref", "adapt")
        adapt["response_depth"] = length_map.get(pref_length, adapt["response_depth"])

        # ── Style cognitif MBTI → response_rules ─────────
        if getattr(uc, "concrete_first", False):
            rules["use_examples"]      = True
            rules["use_step_by_step"]  = True
        if getattr(uc, "structured_resp", False):
            rules["be_structured"]     = True
        if getattr(uc, "direct_feedback", False):
            rules["be_direct"]         = True
        if getattr(uc, "flexible_tone", False):
            adapt["flexible_tone"]     = True

        # ── Ton enrichi (formalité utilisateur) ──────────
        formality = getattr(uc, "formality_level", 2)
        adapt["formality_level"] = formality
        if formality <= 2 and "empathique" not in adapt["tone"]:
            adapt["tone"] = adapt["tone"] + ", chaleureux"

        # ── Challenge preference ──────────────────────────
        adapt["challenge_pref"] = getattr(uc, "challenge_pref", "ask_question")

        # ── Proactivité ────────────────────────────────────
        adapt["proactivity_pref"] = getattr(uc, "proactivity_pref", "moderately_proactive")

        # ── Frontières — sujets à éviter ─────────────────
        topics_avoid = getattr(uc, "topics_avoid", [])
        if topics_avoid:
            if isinstance(bounds, dict):
                bounds.setdefault("topics_avoid", [])
                bounds["topics_avoid"] = list(set(bounds["topics_avoid"] + topics_avoid))

        behaviors_avoid = getattr(uc, "behaviors_avoid", [])
        if behaviors_avoid:
            if isinstance(bounds, dict):
                bounds.setdefault("behaviors_avoid", [])
                bounds["behaviors_avoid"] = list(set(bounds["behaviors_avoid"] + behaviors_avoid))

        # ── Rumination — stratégie ─────────────────────────
        rum_tendency = getattr(uc, "rumination_tendency", "sometimes")
        adapt["rumination_tendency"] = rum_tendency
        if rum_tendency in ("often", "very_often"):
            adapt["rumination_alert"] = True

        # ── Rôle émotionnel ALFRED ────────────────────────
        adapt["alfred_emotional_roles"] = getattr(uc, "alfred_emotional_roles", [])
        adapt["when_distressed"]        = getattr(uc, "when_distressed", "ask_once")

        # ── Section onboarding (résumé lisible) ───────────
        context["onboarding"] = {
            "loaded":        True,
            "mbti":          getattr(uc, "mbti_type", ""),
            "health_active": getattr(uc, "health_active", False),
            "conditions":    getattr(uc, "conditions", []),
            "profiles":      getattr(uc, "profiles_loaded", []),
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
