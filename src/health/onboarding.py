"""
PROJECT      : ALFRED
BLOCK        : 03 / 13
FUNCTION     : 13.05 — Interaction adaptée / Onboarding
FILE         : src/health/onboarding.py
ROLE         : Orchestrateur des questionnaires d'onboarding et écriture des profils utilisateur

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-05-26
VERSION      : V1.0
STATUS       : VALIDATED

DESCRIPTION :
Module gérant les trois questionnaires d'onboarding (santé, personnalité, émotionnel).
Charge les JSON de config, présente les questions, calcule les scores MBTI,
et écrit les profils dans data/health/ et data/profile/.

Utilisation :
    from src.health.onboarding import OnboardingSession
    session = OnboardingSession(user_id="user_001")
    session.run_health()
    session.run_personality()
    session.run_emotional()
    session.save_all()
"""

import json
import copy
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, field
from typing import Any

try:
    from paths import CONFIG_DIR, DATA_HEALTH, DATA_PROFILE
except ImportError:
    _base = Path(__file__).resolve().parent.parent.parent
    CONFIG_DIR  = _base / "config"
    DATA_HEALTH = _base / "data" / "health"
    DATA_PROFILE = _base / "data" / "profile"

_CONFIG_Q = CONFIG_DIR / "questionnaire"

# ── Chargement des questionnaires ──────────────────────────────────────────────

def _load_q(filename: str) -> dict:
    path = _CONFIG_Q / filename
    with open(path, encoding="utf-8") as f:
        return json.load(f)

_Q_HEALTH       = _load_q("onboarding_health.json")
_Q_PERSONALITY  = _load_q("onboarding_personality.json")
_Q_EMOTIONAL    = _load_q("onboarding_emotional.json")


# ── Dataclasses de résultat ────────────────────────────────────────────────────

@dataclass
class HealthProfileData:
    user_id: str
    consent_given: bool = False
    consent_scope: list[str] = field(default_factory=list)
    profile_status: dict = field(default_factory=dict)
    conditions: dict = field(default_factory=lambda: {"primary": [], "secondary": [], "self_declared": []})
    symptoms_profile: dict = field(default_factory=dict)
    treatment_context: dict = field(default_factory=dict)
    interaction_preferences: dict = field(default_factory=dict)
    caregiver_mode: dict = field(default_factory=dict)
    completed_at: str = ""


@dataclass
class PersonalityProfileData:
    user_id: str
    mbti: dict = field(default_factory=dict)
    cognitive_style: dict = field(default_factory=dict)
    communication: dict = field(default_factory=dict)
    values: dict = field(default_factory=dict)
    alfred_adaptations: dict = field(default_factory=dict)
    completed_at: str = ""


@dataclass
class EmotionalProfileData:
    user_id: str
    emotional_baseline: dict = field(default_factory=dict)
    regulation: dict = field(default_factory=dict)
    alfred_role: dict = field(default_factory=dict)
    boundaries: dict = field(default_factory=dict)
    completed_at: str = ""


# ── Moteur de présentation des questions ──────────────────────────────────────

class QuestionPresenter:
    """
    Gère l'affichage et la collecte de réponses pour un questionnaire JSON.
    Mode console par défaut — remplaçable par une interface Kivy.
    """

    def present(self, question: dict, context: dict) -> Any:
        """
        Présente une question et retourne la réponse de l'utilisateur.
        context = dict des réponses déjà données (pour les conditions).
        """
        if not self._check_condition(question, context):
            return None

        q_type = question.get("type", "text")

        if q_type == "boolean":
            return self._ask_boolean(question)
        elif q_type in ("single_select",):
            return self._ask_single_select(question)
        elif q_type in ("multi_select", "multi_select_with_other"):
            return self._ask_multi_select(question)
        elif q_type == "scale":
            return self._ask_scale(question)
        elif q_type == "scale_polar":
            return self._ask_scale_polar(question)
        elif q_type == "consent":
            return self._ask_consent(question)
        else:
            return self._ask_text(question)

    def _check_condition(self, question: dict, context: dict) -> bool:
        cond = question.get("condition_on")
        if not cond:
            return True
        for key, expected in cond.items():
            if context.get(key) != expected:
                return False
        return True

    def _ask_boolean(self, q: dict) -> bool:
        print(f"\n{q.get('label_fr', q['id'])}")
        if sub := q.get("sublabel_fr"):
            print(f"  ({sub})")
        while True:
            ans = input("  [o/n] : ").strip().lower()
            if ans in ("o", "oui", "y", "yes", "1"):
                return True
            if ans in ("n", "non", "no", "0"):
                return False
            print("  → Réponds par o (oui) ou n (non).")

    def _ask_single_select(self, q: dict) -> str:
        print(f"\n{q.get('label_fr', q['id'])}")
        if sub := q.get("sublabel_fr"):
            print(f"  ({sub})")
        options = q.get("options", [])
        for i, opt in enumerate(options, 1):
            print(f"  {i}. {opt.get('label_fr', opt['value'])}")
        while True:
            ans = input(f"  Choix [1-{len(options)}] : ").strip()
            try:
                idx = int(ans) - 1
                if 0 <= idx < len(options):
                    return options[idx]["value"]
            except ValueError:
                pass
            print(f"  → Entre un chiffre entre 1 et {len(options)}.")

    def _ask_multi_select(self, q: dict) -> list[str]:
        print(f"\n{q.get('label_fr', q['id'])}")
        if sub := q.get("sublabel_fr"):
            print(f"  ({sub})")
        options = q.get("options", [])
        for i, opt in enumerate(options, 1):
            print(f"  {i}. {opt.get('label_fr', opt['value'])}")
        other_label = q.get("other_label_fr")
        if other_label:
            print(f"  {len(options)+1}. {other_label}")
        print("  (Sépare les choix par des virgules, ex: 1,3,5)")
        while True:
            raw = input("  Choix : ").strip()
            if not raw and q.get("optional"):
                return []
            selected = []
            try:
                indices = [int(x.strip()) for x in raw.split(",") if x.strip()]
                for idx in indices:
                    if 1 <= idx <= len(options):
                        selected.append(options[idx - 1]["value"])
                    elif idx == len(options) + 1 and other_label:
                        other_val = input(f"  Précise ({other_label}) : ").strip()
                        if other_val:
                            selected.append(f"other:{other_val}")
                if selected:
                    return selected
            except ValueError:
                pass
            print("  → Entre des numéros séparés par des virgules.")

    def _ask_scale(self, q: dict) -> int:
        print(f"\n{q.get('label_fr', q['id'])}")
        s = q.get("scale", {})
        mn, mx = s.get("min", 1), s.get("max", 5)
        labels = s.get("labels", {})
        for k, v in labels.items():
            print(f"  {k} = {v}")
        while True:
            ans = input(f"  Valeur [{mn}-{mx}] : ").strip()
            try:
                val = int(ans)
                if mn <= val <= mx:
                    return val
            except ValueError:
                pass
            print(f"  → Entre un chiffre entre {mn} et {mx}.")

    def _ask_scale_polar(self, q: dict) -> int:
        print(f"\n{q.get('label_fr', q['id'])}")
        left  = q.get("pole_left", {})
        right = q.get("pole_right", {})
        print(f"  -2 : {left.get('label_fr', 'Gauche')}")
        print(f"  -1 : (plutôt à gauche)")
        print(f"   0 : {q.get('neutral_label_fr', 'Neutre / les deux')}")
        print(f"   1 : (plutôt à droite)")
        print(f"   2 : {right.get('label_fr', 'Droite')}")
        while True:
            ans = input("  Valeur [-2 à 2] : ").strip()
            try:
                val = int(ans)
                if -2 <= val <= 2:
                    return val
            except ValueError:
                pass
            print("  → Entre un chiffre entre -2 et 2.")

    def _ask_consent(self, q: dict) -> dict:
        print(f"\n{'='*50}")
        print(q.get("title_fr", "Consentement"))
        print(q.get("text_fr", ""))
        results = {}
        for item in q.get("consent_items", []):
            if item.get("info_only"):
                print(f"\n  ℹ {item['label_fr']}")
                results[item["id"]] = True
                continue
            while True:
                ans = input(f"\n  {item['label_fr']}\n  [o/n] : ").strip().lower()
                if ans in ("o", "oui", "y", "yes"):
                    results[item["id"]] = True
                    break
                if ans in ("n", "non", "no"):
                    results[item["id"]] = False
                    if item.get("required"):
                        print("  → Ce consentement est requis pour continuer.")
                    else:
                        break
        return results

    def _ask_text(self, q: dict) -> str:
        print(f"\n{q.get('label_fr', q['id'])}")
        return input("  Réponse : ").strip()


# ── Utilitaire : écriture imbriquée via clé dotted ────────────────────────────

def _set_nested(d: dict, dotted_key: str, value: Any) -> None:
    parts = dotted_key.split(".")
    for part in parts[:-1]:
        d = d.setdefault(part, {})
    d[parts[-1]] = value


def _get_nested(d: dict, dotted_key: str, default=None) -> Any:
    parts = dotted_key.split(".")
    for part in parts:
        if not isinstance(d, dict):
            return default
        d = d.get(part, default)
        if d is default:
            return default
    return d


# ── Calcul du score MBTI ──────────────────────────────────────────────────────

def _compute_mbti(answers: dict, scoring_config: dict) -> dict:
    mbti_result = {}
    type_letters = []

    for dim, cfg in scoring_config.get("mbti_compute", {}).items():
        if dim == "full_type":
            continue
        fields = cfg.get("fields", [])
        values = [answers.get(f) for f in fields if answers.get(f) is not None]
        if not values:
            letter = "X"
        else:
            mean = sum(values) / len(values)
            interp1 = cfg.get("interpretation", {})
            interp2 = cfg.get("interpretation_2", {})
            r1 = interp1.get("range", [])
            r2 = interp2.get("range", [])
            if r1 and r1[0] <= mean <= r1[1]:
                letter = interp1.get("result", "X")
            elif r2 and r2[0] <= mean <= r2[1]:
                letter = interp2.get("result", "X")
            else:
                letter = cfg.get("neutral_result", "X")
        mbti_result[dim] = {"score": mean if values else 0, "letter": letter}
        type_letters.append(letter)

    mbti_result["full_type"] = "".join(type_letters)
    return mbti_result


# ── Matrice d'adaptation personnalité ─────────────────────────────────────────

def _apply_personality_matrix(mbti: dict, matrix: dict) -> dict:
    adaptations = {}
    type_str = mbti.get("full_type", "")
    for dim, mapping in matrix.items():
        letter = mbti.get(dim, {}).get("letter", "X")
        if letter in mapping:
            adaptations.update(mapping[letter])
    return adaptations


# ── Session d'onboarding ──────────────────────────────────────────────────────

class OnboardingSession:
    """
    Orchestre les trois questionnaires d'onboarding pour un utilisateur.
    Les réponses brutes sont collectées, les profils calculés, puis sauvegardés.
    """

    def __init__(self, user_id: str, presenter: QuestionPresenter = None):
        self.user_id    = user_id
        self.presenter  = presenter or QuestionPresenter()
        self._raw: dict = {}  # toutes les réponses brutes, clé = question id

        self.health_data      = HealthProfileData(user_id=user_id)
        self.personality_data = PersonalityProfileData(user_id=user_id)
        self.emotional_data   = EmotionalProfileData(user_id=user_id)

    # ── Exécution d'un questionnaire ──────────────────────────────────────────

    def _run_questionnaire(self, q_config: dict) -> dict:
        """Présente toutes les sections/questions, retourne le dict de réponses mappées."""
        mapped: dict = {}
        context: dict = {}  # réponses déjà données pour les skip_if

        # Bloc consentement
        if consent_block := q_config.get("consent_block"):
            consent_answers = self.presenter.present(consent_block, context)
            if isinstance(consent_answers, dict):
                all_required_ok = all(
                    consent_answers.get(item["id"], False)
                    for item in consent_block.get("consent_items", [])
                    if item.get("required") and not item.get("info_only")
                )
                if not all_required_ok:
                    print("\n  Questionnaire annulé (consentement non donné).")
                    return {}
                mapped["_consent"] = consent_answers
                context["_consent"] = consent_answers

        for section in q_config.get("sections", []):
            print(f"\n{'─'*50}")
            print(f"  {section.get('title_fr', section['id'])}")
            if sub := section.get("sublabel_fr"):
                print(f"  {sub}")

            for question in section.get("questions", []):
                q_id     = question["id"]
                maps_to  = question.get("maps_to")
                skip_if  = question.get("skip_if_no", [])

                # Vérification skip basé sur réponses précédentes
                if skip_if and context.get(q_id) is False:
                    for skipped_id in skip_if:
                        context[skipped_id] = None
                    continue

                answer = self.presenter.present(question, context)
                context[q_id] = answer
                self._raw[q_id] = answer

                if maps_to and answer is not None:
                    _set_nested(mapped, maps_to, answer)

        return mapped

    # ── Questionnaire santé ───────────────────────────────────────────────────

    def run_health(self) -> HealthProfileData:
        print("\n" + "="*55)
        intro = _Q_HEALTH.get("consent_block", {}).get("text_fr", "")
        print(intro)

        mapped = self._run_questionnaire(_Q_HEALTH)
        if not mapped:
            return self.health_data

        consent_ok = mapped.get("_consent", {})
        self.health_data.consent_given = bool(consent_ok)
        self.health_data.consent_scope = [k for k, v in consent_ok.items() if v]

        self.health_data.profile_status       = mapped.get("profile_status", {})
        self.health_data.conditions           = mapped.get("conditions", {"primary": [], "secondary": [], "self_declared": []})
        self.health_data.symptoms_profile     = mapped.get("symptoms_profile", {})
        self.health_data.treatment_context    = mapped.get("treatment_context", {})
        self.health_data.interaction_preferences = mapped.get("interaction_preferences", {})
        self.health_data.caregiver_mode       = mapped.get("caregiver_mode", {})
        self.health_data.completed_at         = datetime.now().isoformat()

        print("\n" + _Q_HEALTH.get("completion", {}).get("message_fr", "Profil santé enregistré."))
        return self.health_data

    # ── Questionnaire personnalité ─────────────────────────────────────────────

    def run_personality(self) -> PersonalityProfileData:
        print("\n" + "="*55)
        print(_Q_PERSONALITY.get("introduction", {}).get("text_fr", ""))

        mapped = self._run_questionnaire(_Q_PERSONALITY)
        if not mapped:
            return self.personality_data

        # Calcul MBTI
        mbti_raw = mapped.get("mbti", {})
        scoring  = _Q_PERSONALITY.get("scoring", {})
        mbti_result = _compute_mbti(
            {k: v for k, v in self._raw.items()},
            scoring
        )

        matrix       = _Q_PERSONALITY.get("personality_adaptation_matrix", {})
        adaptations  = _apply_personality_matrix(mbti_result, matrix)

        self.personality_data.mbti             = mbti_result
        self.personality_data.cognitive_style  = mapped.get("cognitive_style", {})
        self.personality_data.communication    = mapped.get("communication", {})
        self.personality_data.values           = mapped.get("values", {})
        self.personality_data.alfred_adaptations = adaptations
        self.personality_data.completed_at     = datetime.now().isoformat()

        mbti_type = mbti_result.get("full_type", "????")
        print(f"\n  Type MBTI calculé : {mbti_type}")
        print("\n" + _Q_PERSONALITY.get("completion", {}).get("message_fr", "Profil personnalité enregistré."))
        return self.personality_data

    # ── Questionnaire émotionnel ──────────────────────────────────────────────

    def run_emotional(self) -> EmotionalProfileData:
        print("\n" + "="*55)
        print(_Q_EMOTIONAL.get("introduction", {}).get("text_fr", ""))

        mapped = self._run_questionnaire(_Q_EMOTIONAL)
        if not mapped:
            return self.emotional_data

        self.emotional_data.emotional_baseline = mapped.get("emotional_baseline", {})
        self.emotional_data.regulation         = mapped.get("regulation", {})
        self.emotional_data.alfred_role        = mapped.get("alfred_role", {})
        self.emotional_data.boundaries         = mapped.get("boundaries", {})
        self.emotional_data.completed_at       = datetime.now().isoformat()

        print("\n" + _Q_EMOTIONAL.get("completion", {}).get("message_fr", "Profil émotionnel enregistré."))
        return self.emotional_data

    # ── Sauvegarde ────────────────────────────────────────────────────────────

    def save_all(self) -> dict[str, Path]:
        DATA_HEALTH.mkdir(parents=True, exist_ok=True)
        DATA_PROFILE.mkdir(parents=True, exist_ok=True)

        paths_saved = {}

        if self.health_data.completed_at:
            health_path = DATA_HEALTH / f"health_{self.user_id}.json"
            health_dict = {
                "metadata": {
                    "profile_id": f"health_{self.user_id}",
                    "user_id": self.user_id,
                    "consent_given": self.health_data.consent_given,
                    "consent_scope": self.health_data.consent_scope,
                    "encryption_required": True,
                    "completed_at": self.health_data.completed_at
                },
                "profile_status": self.health_data.profile_status,
                "conditions": self.health_data.conditions,
                "symptoms_profile": self.health_data.symptoms_profile,
                "treatment_context": self.health_data.treatment_context,
                "interaction_preferences": self.health_data.interaction_preferences,
                "caregiver_mode": self.health_data.caregiver_mode,
                "alfred_adaptations_active": bool(self.health_data.consent_given)
            }
            with open(health_path, "w", encoding="utf-8") as f:
                json.dump(health_dict, f, ensure_ascii=False, indent=2)
            paths_saved["health"] = health_path

        if self.personality_data.completed_at:
            pers_path = DATA_PROFILE / f"personality_{self.user_id}.json"
            pers_dict = {
                "metadata": {
                    "profile_id": f"personality_{self.user_id}",
                    "user_id": self.user_id,
                    "completed_at": self.personality_data.completed_at
                },
                "mbti": self.personality_data.mbti,
                "cognitive_style": self.personality_data.cognitive_style,
                "communication": self.personality_data.communication,
                "values": self.personality_data.values,
                "alfred_adaptations": self.personality_data.alfred_adaptations
            }
            with open(pers_path, "w", encoding="utf-8") as f:
                json.dump(pers_dict, f, ensure_ascii=False, indent=2)
            paths_saved["personality"] = pers_path

        if self.emotional_data.completed_at:
            emo_path = DATA_PROFILE / f"emotional_{self.user_id}.json"
            emo_dict = {
                "metadata": {
                    "profile_id": f"emotional_{self.user_id}",
                    "user_id": self.user_id,
                    "completed_at": self.emotional_data.completed_at
                },
                "emotional_baseline": self.emotional_data.emotional_baseline,
                "regulation": self.emotional_data.regulation,
                "alfred_role": self.emotional_data.alfred_role,
                "boundaries": self.emotional_data.boundaries
            }
            with open(emo_path, "w", encoding="utf-8") as f:
                json.dump(emo_dict, f, ensure_ascii=False, indent=2)
            paths_saved["emotional"] = emo_path

        return paths_saved

    # ── Chargement d'un profil existant ──────────────────────────────────────

    @staticmethod
    def load_personality_profile(user_id: str) -> dict:
        path = DATA_PROFILE / f"personality_{user_id}.json"
        if not path.exists():
            return {}
        with open(path, encoding="utf-8") as f:
            return json.load(f)

    @staticmethod
    def load_emotional_profile(user_id: str) -> dict:
        path = DATA_PROFILE / f"emotional_{user_id}.json"
        if not path.exists():
            return {}
        with open(path, encoding="utf-8") as f:
            return json.load(f)

    # ── Accès rapide aux adaptations calculées ────────────────────────────────

    def get_communication_params(self) -> dict:
        """Retourne les paramètres de communication fusionnés pour personality_adapter."""
        params = {}

        # MBTI
        mbti = self.personality_data.alfred_adaptations
        params.update(mbti)

        # Communication directe
        comm = self.personality_data.communication
        if formality := comm.get("formality_level"):
            params["formality"] = formality
        if humor := comm.get("humor_preference"):
            params["humor_enabled"] = humor not in ("none",)
        if validation := comm.get("validation_style"):
            params["validate_first"] = (validation == "validate_first")
        if proactivity := comm.get("proactivity_preference"):
            params["proactivity_high"] = proactivity in ("very_proactive",)

        # Frontières émotionnelles
        boundaries = self.emotional_data.boundaries
        if avoid := boundaries.get("behaviors_to_avoid"):
            params["behaviors_avoid"] = avoid
        if sensitive := boundaries.get("sensitive_topics_avoid"):
            params["topics_avoid"] = sensitive

        return params


# ── Point d'entrée console ────────────────────────────────────────────────────

def run_full_onboarding(user_id: str = "default") -> dict[str, Path]:
    """Lance le parcours d'onboarding complet en console."""
    print("\n" + "="*55)
    print("  ALFRED — Configuration personnalisée")
    print("="*55)
    print("\nCes questionnaires sont optionnels et modifiables à tout moment.")
    print("Réponds du mieux que tu peux. Appuie sur Entrée pour passer une question optionnelle.\n")

    session = OnboardingSession(user_id=user_id)

    run_health = input("Veux-tu remplir le questionnaire santé & bien-être ? [o/n] : ").strip().lower()
    if run_health in ("o", "oui", "y"):
        session.run_health()

    run_pers = input("\nVeux-tu remplir le questionnaire personnalité & communication ? [o/n] : ").strip().lower()
    if run_pers in ("o", "oui", "y"):
        session.run_personality()

    run_emo = input("\nVeux-tu remplir le questionnaire profil émotionnel ? [o/n] : ").strip().lower()
    if run_emo in ("o", "oui", "y"):
        session.run_emotional()

    paths = session.save_all()

    print("\n" + "="*55)
    print("  Configuration terminée. Fichiers sauvegardés :")
    for k, p in paths.items():
        print(f"  - {k}: {p}")
    print("="*55 + "\n")

    return paths


if __name__ == "__main__":
    run_full_onboarding(user_id="user_001")
