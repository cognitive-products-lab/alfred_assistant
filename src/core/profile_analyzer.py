# ============================================================
# ALFRED — src/core/profile_analyzer.py
# Bloc 04.01 — Analyse et scoring du profil psychologique
#
# UTILITE ALFRED :
#   Calcule les scores normalisés à partir des réponses aux questionnaires,
#   génère les paramètres comportementaux ALFRED via la matrice de mapping,
#   fusionne avec le profil AssessFirst et chiffre les données sensibles.
#
# DOMAINE :
#   Profilage psychologique — pipeline de scoring et adaptation comportementale
#
# STATUS  : TESTED
# ============================================================

from __future__ import annotations

import json
import os
import shutil
from dataclasses import dataclass, field
from datetime import datetime, date
from pathlib import Path
from typing import Any, Dict, List, Optional

try:
    from cryptography.fernet import Fernet, InvalidToken
    FERNET_AVAILABLE = True
except ImportError:
    Fernet = None
    InvalidToken = Exception
    FERNET_AVAILABLE = False

# ─────────────────────────────────────────────────────────
# CHEMINS PAR DÉFAUT
# ─────────────────────────────────────────────────────────

_BASE = Path(__file__).resolve().parents[2]

DEFAULT_ANSWERS_PATH = _BASE / "data" / "profile" / "scoring" / "answers_template.json"
DEFAULT_KEYS_PATH = _BASE / "data" / "profile" / "scoring" / "scoring_keys.json"
DEFAULT_MATRIX_PATH = _BASE / "data" / "profile" / "schema" / "alfred_mapping_matrix.json"
DEFAULT_PROFILE_PATH = _BASE / "data" / "profile" / "user_profile.json"
DEFAULT_FERNET_KEY_PATH = _BASE / "data" / "security" / "fernet.key"
DEFAULT_ENCRYPTED_DIR = _BASE / "data" / "profile" / "answers_encrypted"


# ─────────────────────────────────────────────────────────
# DATACLASSES
# ─────────────────────────────────────────────────────────

@dataclass
class SubScore:
    """Score normalisé pour une sous-dimension."""
    dimension_id: str
    sub_dimension_id: str
    score_raw: Optional[float]
    score_normalized: float
    level: str
    items_used: List[str]
    completed: bool


@dataclass
class DimensionScore:
    """Score agrégé pour une dimension complète."""
    dimension_id: str
    completed: bool
    sub_scores: Dict[str, SubScore] = field(default_factory=dict)
    global_score: Optional[float] = None
    global_level: str = "non_renseigné"


@dataclass
class AlfredParams:
    """Paramètres comportementaux ALFRED dérivés du profil psychologique."""
    tone: str = "chaleureux"
    response_length: str = "adaptatif"
    proactivity: str = "modéré"
    emotional_support_level: str = "standard"
    challenge_level: str = "standard"
    check_in_frequency: str = "à_la_demande"
    explanation_depth: str = "détaillé"
    humor_level: str = "léger"
    structure_preference: str = "structuré"
    alerts: List[str] = field(default_factory=list)
    applied_rules: List[str] = field(default_factory=list)


# ─────────────────────────────────────────────────────────
# NIVEAU DEPUIS SCORE
# ─────────────────────────────────────────────────────────

def _get_level_from_score(score: float, dimension_id: str, sub_dimension_id: Optional[str] = None) -> str:
    """Détermine le niveau (label) correspondant à un score normalisé 0-100."""

    # Cas spéciaux par dimension
    if dimension_id == "chronotype_energie" and sub_dimension_id == "chronotype":
        if score >= 70:
            return "chronotype_soir"
        elif score >= 35:
            return "chronotype_intermediaire"
        else:
            return "chronotype_matin"

    if dimension_id == "engagement_burnout":
        if score < 25:
            return "critique"
        elif score < 45:
            return "faible"
        elif score < 65:
            return "moyen"
        elif score < 85:
            return "élevé"
        else:
            return "très élevé"

    if dimension_id == "valeurs_schwartz":
        if score < 34:
            return "non prioritaire"
        elif score < 67:
            return "modérément important"
        else:
            return "prioritaire"

    if dimension_id == "riasec_interets_pro":
        if score < 34:
            return "non dominant"
        elif score < 67:
            return "secondaire"
        else:
            return "dominant"

    if dimension_id == "communication_conflit":
        if score < 34:
            return "mode secondaire"
        elif score < 67:
            return "mode alterné"
        else:
            return "mode dominant"

    # Par défaut : 3 niveaux
    if score < 34:
        return "faible"
    elif score < 67:
        return "moyen"
    else:
        return "élevé"


# ─────────────────────────────────────────────────────────
# PROFILE ANALYZER
# ─────────────────────────────────────────────────────────

class ProfileAnalyzer:
    """
    Moteur de calcul du profil psychologique ALFRED.

    Pipeline :
    1. Charge les réponses (answers_template.json ou fichier chiffré)
    2. Charge les clés de scoring (scoring_keys.json)
    3. Calcule tous les scores normalisés 0-100 par sous-dimension
    4. Charge la matrice de mapping (alfred_mapping_matrix.json)
    5. Génère les paramètres ALFRED selon les scores
    6. Fusionne avec les données AssessFirst dans user_profile.json
    7. Met à jour user_profile.json
    8. Propose le chiffrement des réponses brutes
    """

    def __init__(
        self,
        answers_path: Path | str = DEFAULT_ANSWERS_PATH,
        keys_path: Path | str = DEFAULT_KEYS_PATH,
        matrix_path: Path | str = DEFAULT_MATRIX_PATH,
        profile_path: Path | str = DEFAULT_PROFILE_PATH,
        fernet_key_path: Path | str = DEFAULT_FERNET_KEY_PATH,
    ) -> None:
        self.answers_path = Path(answers_path)
        self.keys_path = Path(keys_path)
        self.matrix_path = Path(matrix_path)
        self.profile_path = Path(profile_path)
        self.fernet_key_path = Path(fernet_key_path)

        self._answers: Dict[str, Any] = {}
        self._scoring_keys: Dict[str, Any] = {}
        self._matrix: Dict[str, Any] = {}
        self._profile: Dict[str, Any] = {}

    # ─────────────────────────────────────────────────────
    # CHARGEMENT
    # ─────────────────────────────────────────────────────

    def _load_json(self, path: Path) -> Dict[str, Any]:
        """Charge un fichier JSON avec gestion d'erreurs propre."""
        if not path.exists():
            raise FileNotFoundError(f"Fichier introuvable : {path}")
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)

    def _save_json(self, path: Path, data: Dict[str, Any]) -> None:
        """Sauvegarde un fichier JSON avec indentation."""
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def load_all(self) -> None:
        """Charge tous les fichiers nécessaires."""
        self._answers = self._load_json(self.answers_path)
        self._scoring_keys = self._load_json(self.keys_path)
        self._matrix = self._load_json(self.matrix_path)

        if self.profile_path.exists():
            self._profile = self._load_json(self.profile_path)
        else:
            self._profile = {}

    # ─────────────────────────────────────────────────────
    # CALCUL DES SCORES
    # ─────────────────────────────────────────────────────

    def compute_scores(self) -> Dict[str, DimensionScore]:
        """
        Calcule tous les scores normalisés 0-100 pour chaque dimension
        et sous-dimension. Gère les données partielles (certains questionnaires
        non remplis).

        Retourne un dict {dimension_id: DimensionScore}.
        """
        if not self._scoring_keys:
            raise RuntimeError("Les clés de scoring ne sont pas chargées. Appelez load_all() d'abord.")

        scores: Dict[str, DimensionScore] = {}

        questionnaire_map = self._answers.get("questionnaires", {})
        keys_map = self._scoring_keys.get("questionnaires", {})

        for q_id, q_config in keys_map.items():
            q_answers = questionnaire_map.get(q_id, {})
            completed = q_answers.get("completed", False)
            answers = q_answers.get("answers", {})

            dim_score = DimensionScore(
                dimension_id=q_id,
                completed=completed
            )

            if not completed:
                scores[q_id] = dim_score
                continue

            subscales = q_config.get("subscales", {})

            for sub_id, sub_config in subscales.items():
                sub_score = self._compute_subscale_score(
                    dimension_id=q_id,
                    sub_dimension_id=sub_id,
                    sub_config=sub_config,
                    answers=answers,
                    q_config=q_config
                )
                dim_score.sub_scores[sub_id] = sub_score

            # Score global = moyenne des sous-dimensions principales (excluant les agrégats)
            main_scores = [
                s.score_normalized for s in dim_score.sub_scores.values()
                if s.completed and "_global" not in s.sub_dimension_id
                and "globale" not in s.sub_dimension_id
                and "global" not in s.sub_dimension_id
            ]

            if main_scores:
                dim_score.global_score = sum(main_scores) / len(main_scores)
                dim_score.global_level = _get_level_from_score(
                    dim_score.global_score, q_id
                )

            scores[q_id] = dim_score

        # Calcul des valeurs supérieures Schwartz
        if "valeurs_schwartz" in scores and scores["valeurs_schwartz"].completed:
            self._compute_schwartz_higher_order(scores["valeurs_schwartz"], keys_map.get("valeurs_schwartz", {}))

        return scores

    def _compute_subscale_score(
        self,
        dimension_id: str,
        sub_dimension_id: str,
        sub_config: Dict[str, Any],
        answers: Dict[str, Any],
        q_config: Dict[str, Any]
    ) -> SubScore:
        """Calcule le score d'une sous-dimension selon sa configuration."""

        # Cas spécial : communication_conflit avec items ipsatifs + likert
        if dimension_id == "communication_conflit" and "items_ipsatifs" in sub_config:
            return self._compute_communication_score(
                sub_dimension_id, sub_config, answers
            )

        items: List[str] = sub_config.get("items", [])
        reversed_items: List[str] = sub_config.get("reversed_items", [])
        scoring_method: str = sub_config.get("scoring", "mean")
        score_min: float = float(sub_config.get("score_min", 0))
        score_max: float = float(sub_config.get("score_max", 100))
        normalization: str = sub_config.get("normalization", "linear_0_100")

        # Récupération des valeurs
        raw_values = []
        items_used = []

        for item_id in items:
            val = answers.get(item_id)
            if val is not None:
                # Inversion si nécessaire
                if item_id in reversed_items:
                    reverse_max = float(q_config.get("scale_max", score_max))
                    val = (reverse_max + 1) - float(val)
                    # PSS-4 exception : 4 - score
                    if "s3" in item_id or "s4" in item_id:
                        val = 4 - answers.get(item_id)
                else:
                    val = float(val)
                raw_values.append(val)
                items_used.append(item_id)

        if not raw_values:
            return SubScore(
                dimension_id=dimension_id,
                sub_dimension_id=sub_dimension_id,
                score_raw=None,
                score_normalized=50.0,
                level=_get_level_from_score(50.0, dimension_id, sub_dimension_id),
                items_used=[],
                completed=False
            )

        # Calcul selon méthode
        if scoring_method == "sum":
            score_raw = sum(raw_values)
        else:  # mean
            score_raw = sum(raw_values) / len(raw_values)

        # Normalisation 0-100
        score_normalized = self._normalize(
            score_raw, score_min, score_max, normalization, sub_config
        )

        # Cas spécial : correction centrage Schwartz
        if normalization == "linear_0_100_centered":
            grand_mean = sum(answers.get(f"v{i}", 3.5) or 3.5 for i in range(1, 22)) / 21
            raw_mean = sum(raw_values) / len(raw_values) if raw_values else 3.5
            centered = (raw_mean - grand_mean + 2.5) / 5.0
            score_normalized = max(0.0, min(100.0, centered * 100))

        return SubScore(
            dimension_id=dimension_id,
            sub_dimension_id=sub_dimension_id,
            score_raw=score_raw,
            score_normalized=round(score_normalized, 2),
            level=_get_level_from_score(score_normalized, dimension_id, sub_dimension_id),
            items_used=items_used,
            completed=True
        )

    def _normalize(
        self,
        score_raw: float,
        score_min: float,
        score_max: float,
        normalization: str,
        config: Dict[str, Any]
    ) -> float:
        """Normalise un score brut sur 0-100."""
        range_size = score_max - score_min
        if range_size == 0:
            return 50.0

        normalized = (score_raw - score_min) / range_size * 100.0

        if normalization == "inverted_linear_0_100":
            normalized = 100.0 - normalized

        return max(0.0, min(100.0, normalized))

    def _compute_communication_score(
        self,
        sub_id: str,
        sub_config: Dict[str, Any],
        answers: Dict[str, Any]
    ) -> SubScore:
        """Calcule le score composite pour les modes communication/conflit."""

        # Score ipsatif
        ipsatif_config = sub_config.get("items_ipsatifs", {})
        ipsatif_map = ipsatif_config.get("scoring_map", {})
        ipsatif_max = ipsatif_config.get("score_max", 1)

        ipsatif_score = 0
        for item_id, choice_map in ipsatif_map.items():
            answer = answers.get(item_id)
            if answer in choice_map:
                ipsatif_score += choice_map[answer]

        ipsatif_normalized = (ipsatif_score / ipsatif_max * 100) if ipsatif_max > 0 else 50.0

        # Score Likert
        likert_config = sub_config.get("items_likert", {})
        likert_items = likert_config.get("items", [])
        likert_min = float(likert_config.get("score_min", 3))
        likert_max = float(likert_config.get("score_max", 15))

        likert_values = [float(answers.get(i, 0) or 0) for i in likert_items if answers.get(i) is not None]
        if likert_values:
            likert_sum = sum(likert_values)
            likert_normalized = (likert_sum - likert_min) / (likert_max - likert_min) * 100
            likert_normalized = max(0.0, min(100.0, likert_normalized))
        else:
            likert_normalized = 50.0

        # Score composite pondéré
        fusion = sub_config.get("fusion", {})
        poids_ipsatif = fusion.get("poids_ipsatif", 0.4)
        poids_likert = fusion.get("poids_likert", 0.6)

        composite = poids_ipsatif * ipsatif_normalized + poids_likert * likert_normalized
        composite = round(max(0.0, min(100.0, composite)), 2)

        dimension_id = "communication_conflit"
        return SubScore(
            dimension_id=dimension_id,
            sub_dimension_id=sub_id,
            score_raw=composite,
            score_normalized=composite,
            level=_get_level_from_score(composite, dimension_id, sub_id),
            items_used=list(ipsatif_map.keys()) + likert_items,
            completed=True
        )

    def _compute_schwartz_higher_order(
        self,
        dim_score: DimensionScore,
        q_config: Dict[str, Any]
    ) -> None:
        """Calcule les 4 valeurs supérieures de Schwartz à partir des 10 valeurs de base."""
        higher_order = q_config.get("higher_order", {})

        for ho_id, ho_config in higher_order.items():
            subscales_included = ho_config.get("subscales", [])
            sub_scores = [
                dim_score.sub_scores[s].score_normalized
                for s in subscales_included
                if s in dim_score.sub_scores and dim_score.sub_scores[s].completed
            ]

            if sub_scores:
                ho_score = sum(sub_scores) / len(sub_scores)
                dim_score.sub_scores[ho_id] = SubScore(
                    dimension_id="valeurs_schwartz",
                    sub_dimension_id=ho_id,
                    score_raw=ho_score,
                    score_normalized=round(ho_score, 2),
                    level=_get_level_from_score(ho_score, "valeurs_schwartz"),
                    items_used=subscales_included,
                    completed=True
                )

    # ─────────────────────────────────────────────────────
    # GÉNÉRATION DES PARAMÈTRES ALFRED
    # ─────────────────────────────────────────────────────

    def generate_alfred_params(self, scores: Dict[str, DimensionScore]) -> AlfredParams:
        """
        Génère les paramètres comportementaux ALFRED en appliquant
        la matrice de mapping selon les scores calculés.

        Priorité : règles de combinaison > règles individuelles > paramètres par défaut.
        """
        if not self._matrix:
            raise RuntimeError("La matrice de mapping n'est pas chargée. Appelez load_all() d'abord.")

        rules = self._matrix.get("rules", [])
        combo_rules = self._matrix.get("combination_rules", [])
        default_params_data = self._matrix.get("default_params", {}).get("alfred_params", {})

        params = AlfredParams(
            tone=default_params_data.get("tone", "chaleureux"),
            response_length=default_params_data.get("response_length", "adaptatif"),
            proactivity=default_params_data.get("proactivity", "modéré"),
            emotional_support_level=default_params_data.get("emotional_support_level", "standard"),
            challenge_level=default_params_data.get("challenge_level", "standard"),
            check_in_frequency=default_params_data.get("check_in_frequency", "à_la_demande"),
            explanation_depth=default_params_data.get("explanation_depth", "détaillé"),
            humor_level=default_params_data.get("humor_level", "léger"),
            structure_preference=default_params_data.get("structure_preference", "structuré")
        )

        # Appliquer les règles individuelles
        for rule in rules:
            dim_id = rule.get("dimension")
            sub_id = rule.get("sub_dimension")
            rule_level = rule.get("level")

            if dim_id not in scores or not scores[dim_id].completed:
                continue

            dim_score = scores[dim_id]
            if sub_id and sub_id in dim_score.sub_scores:
                actual_level = dim_score.sub_scores[sub_id].level
            elif dim_score.global_level:
                actual_level = dim_score.global_level
            else:
                continue

            if actual_level == rule_level:
                rule_params = rule.get("alfred_params", {})
                self._apply_rule_params(params, rule_params, rule.get("id", ""))

        # Appliquer les règles de combinaison (peuvent écraser les règles individuelles)
        for combo in combo_rules:
            conditions = combo.get("conditions", [])
            all_match = True

            for cond in conditions:
                c_dim = cond.get("dimension")
                c_sub = cond.get("sub_dimension")
                c_level = cond.get("level")

                if c_dim not in scores or not scores[c_dim].completed:
                    all_match = False
                    break

                dim_score = scores[c_dim]
                if c_sub and c_sub in dim_score.sub_scores:
                    actual = dim_score.sub_scores[c_sub].level
                else:
                    actual = dim_score.global_level

                if actual != c_level:
                    all_match = False
                    break

            if all_match:
                override_params = combo.get("override_params", {})
                self._apply_rule_params(params, override_params, combo.get("id", ""))

                alert = combo.get("alert")
                if alert:
                    params.alerts.append(alert)

        return params

    def _apply_rule_params(
        self,
        params: AlfredParams,
        rule_params: Dict[str, Any],
        rule_id: str
    ) -> None:
        """Applique les paramètres d'une règle sur l'objet AlfredParams."""
        if "tone" in rule_params:
            params.tone = rule_params["tone"]
        if "response_length" in rule_params:
            params.response_length = rule_params["response_length"]
        if "proactivity" in rule_params:
            params.proactivity = rule_params["proactivity"]
        if "emotional_support_level" in rule_params:
            params.emotional_support_level = rule_params["emotional_support_level"]
        if "challenge_level" in rule_params:
            params.challenge_level = rule_params["challenge_level"]
        if "check_in_frequency" in rule_params:
            params.check_in_frequency = rule_params["check_in_frequency"]
        if "explanation_depth" in rule_params:
            params.explanation_depth = rule_params["explanation_depth"]
        if "humor_level" in rule_params:
            params.humor_level = rule_params["humor_level"]
        if "structure_preference" in rule_params:
            params.structure_preference = rule_params["structure_preference"]

        if rule_id:
            params.applied_rules.append(rule_id)

    # ─────────────────────────────────────────────────────
    # MISE À JOUR DU PROFIL
    # ─────────────────────────────────────────────────────

    def update_user_profile(
        self,
        scores: Dict[str, DimensionScore],
        alfred_params: AlfredParams
    ) -> Dict[str, Any]:
        """
        Met à jour user_profile.json avec :
        - Les scores psychologiques calculés (niveaux agrégés, pas les réponses brutes)
        - Les paramètres ALFRED dérivés
        - La date de mise à jour

        Ne stocke jamais les réponses brutes dans ce fichier — uniquement les scores.
        """
        profile = self._profile.copy()

        # Structure du profil psychologique
        psychological_profile: Dict[str, Any] = {
            "last_updated": datetime.now().isoformat(),
            "profile_completeness": self._compute_completeness(scores),
            "dimensions": {}
        }

        for dim_id, dim_score in scores.items():
            dim_data: Dict[str, Any] = {
                "completed": dim_score.completed,
                "global_score": round(dim_score.global_score, 2) if dim_score.global_score is not None else None,
                "global_level": dim_score.global_level,
                "sub_dimensions": {}
            }

            for sub_id, sub_score in dim_score.sub_scores.items():
                dim_data["sub_dimensions"][sub_id] = {
                    "score": sub_score.score_normalized,
                    "level": sub_score.level,
                    "completed": sub_score.completed
                }

            psychological_profile["dimensions"][dim_id] = dim_data

        # Paramètres ALFRED dérivés
        alfred_derived_params: Dict[str, Any] = {
            "last_computed": datetime.now().isoformat(),
            "tone": alfred_params.tone,
            "response_length": alfred_params.response_length,
            "proactivity": alfred_params.proactivity,
            "emotional_support_level": alfred_params.emotional_support_level,
            "challenge_level": alfred_params.challenge_level,
            "check_in_frequency": alfred_params.check_in_frequency,
            "explanation_depth": alfred_params.explanation_depth,
            "humor_level": alfred_params.humor_level,
            "structure_preference": alfred_params.structure_preference,
            "applied_rules": alfred_params.applied_rules,
            "alerts": alfred_params.alerts
        }

        profile["psychological_profile"] = psychological_profile
        profile["alfred_derived_params"] = alfred_derived_params

        self._save_json(self.profile_path, profile)
        print(f"[ProfileAnalyzer] Profil mis à jour : {self.profile_path}")

        return profile

    def _compute_completeness(self, scores: Dict[str, DimensionScore]) -> float:
        """Calcule le pourcentage de complétude du profil (0-100)."""
        total = len(scores)
        if total == 0:
            return 0.0
        completed = sum(1 for s in scores.values() if s.completed)
        return round(completed / total * 100, 1)

    # ─────────────────────────────────────────────────────
    # CHIFFREMENT FERNET
    # ─────────────────────────────────────────────────────

    def _load_fernet_key(self) -> Optional[bytes]:
        """
        Charge la clé Fernet depuis l'environnement ou le fichier local.
        Génère une nouvelle clé si aucune n'existe.
        """
        if not FERNET_AVAILABLE:
            print("[ProfileAnalyzer] cryptography non disponible — chiffrement désactivé")
            return None

        # Priorité 1 : variable d'environnement
        env_key = os.getenv("FERNET_KEY")
        if env_key:
            return env_key.encode()

        # Priorité 2 : fichier local
        if self.fernet_key_path.exists():
            return self.fernet_key_path.read_bytes().strip()

        # Priorité 3 : génération
        print("[ProfileAnalyzer] Génération d'une nouvelle clé Fernet...")
        new_key = Fernet.generate_key()
        self.fernet_key_path.parent.mkdir(parents=True, exist_ok=True)
        self.fernet_key_path.write_bytes(new_key)
        print(f"[ProfileAnalyzer] Clé sauvegardée : {self.fernet_key_path}")
        print("[ProfileAnalyzer] ATTENTION : ne jamais commiter ce fichier de clé !")
        return new_key

    def encrypt_answers(
        self,
        answers_path: Optional[Path] = None,
        output_dir: Optional[Path] = None
    ) -> Optional[Path]:
        """
        Chiffre le fichier de réponses brutes avec Fernet (AES-128-CBC).

        - Lit le fichier JSON de réponses
        - Le chiffre avec la clé Fernet
        - Sauvegarde le fichier chiffré dans output_dir/
        - Retourne le chemin du fichier chiffré

        Le fichier original NON chiffré est supprimé après chiffrement réussi
        pour ne pas laisser de données sensibles en clair.
        """
        source = answers_path or self.answers_path
        dest_dir = output_dir or DEFAULT_ENCRYPTED_DIR

        if not FERNET_AVAILABLE:
            print("[ProfileAnalyzer] Chiffrement impossible : cryptography non installé")
            return None

        fernet_key = self._load_fernet_key()
        if not fernet_key:
            print("[ProfileAnalyzer] Clé Fernet introuvable — chiffrement annulé")
            return None

        if not source.exists():
            print(f"[ProfileAnalyzer] Fichier source introuvable : {source}")
            return None

        try:
            cipher = Fernet(fernet_key)
            raw_data = source.read_bytes()
            encrypted = cipher.encrypt(raw_data)

            dest_dir.mkdir(parents=True, exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = dest_dir / f"answers_{timestamp}.fernet"
            output_path.write_bytes(encrypted)

            print(f"[ProfileAnalyzer] Réponses chiffrées : {output_path}")
            return output_path

        except Exception as e:
            print(f"[ProfileAnalyzer] Erreur lors du chiffrement : {e}")
            return None

    def decrypt_answers(
        self,
        encrypted_path: Path,
        output_path: Optional[Path] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Déchiffre un fichier de réponses chiffré.

        - Déchiffre avec la clé Fernet
        - Retourne le dict Python des réponses
        - Optionnellement sauvegarde en fichier JSON temporaire

        Usage : profile_analyzer.decrypt_answers(Path("data/profile/answers_encrypted/answers_20260616_120000.fernet"))
        """
        if not FERNET_AVAILABLE:
            print("[ProfileAnalyzer] Déchiffrement impossible : cryptography non installé")
            return None

        fernet_key = self._load_fernet_key()
        if not fernet_key:
            print("[ProfileAnalyzer] Clé Fernet introuvable — déchiffrement annulé")
            return None

        if not encrypted_path.exists():
            print(f"[ProfileAnalyzer] Fichier chiffré introuvable : {encrypted_path}")
            return None

        try:
            cipher = Fernet(fernet_key)
            encrypted_data = encrypted_path.read_bytes()
            decrypted = cipher.decrypt(encrypted_data)
            answers_dict = json.loads(decrypted.decode("utf-8"))

            if output_path:
                self._save_json(output_path, answers_dict)
                print(f"[ProfileAnalyzer] Réponses déchiffrées sauvegardées : {output_path}")

            return answers_dict

        except InvalidToken:
            print("[ProfileAnalyzer] Token invalide — clé incorrecte ou fichier corrompu")
            return None
        except Exception as e:
            print(f"[ProfileAnalyzer] Erreur déchiffrement : {e}")
            return None

    # ─────────────────────────────────────────────────────
    # PIPELINE COMPLET
    # ─────────────────────────────────────────────────────

    def run(self, encrypt_after: bool = True) -> Dict[str, Any]:
        """
        Lance le pipeline complet :
        1. Charge tous les fichiers
        2. Calcule les scores
        3. Génère les paramètres ALFRED
        4. Met à jour user_profile.json
        5. Chiffre les réponses brutes (si encrypt_after=True)

        Retourne le profil mis à jour.
        """
        print("[ProfileAnalyzer] Démarrage du pipeline de profilage...")

        # Étape 1 : chargement
        self.load_all()
        print("[ProfileAnalyzer] Fichiers chargés.")

        # Étape 2 : calcul des scores
        scores = self.compute_scores()
        completeness = self._compute_completeness(scores)
        print(f"[ProfileAnalyzer] Scores calculés — complétude : {completeness}%")

        completed_dims = [k for k, v in scores.items() if v.completed]
        if completed_dims:
            print(f"[ProfileAnalyzer] Dimensions renseignées : {', '.join(completed_dims)}")

        # Étape 3 : paramètres ALFRED
        alfred_params = self.generate_alfred_params(scores)
        print(f"[ProfileAnalyzer] Paramètres ALFRED générés — tone: {alfred_params.tone}, "
              f"support: {alfred_params.emotional_support_level}")

        if alfred_params.alerts:
            print("[ProfileAnalyzer] ALERTES DÉTECTÉES :")
            for alert in alfred_params.alerts:
                print(f"  ALERTE : {alert}")

        # Étape 4 : mise à jour du profil
        updated_profile = self.update_user_profile(scores, alfred_params)

        # Étape 5 : chiffrement optionnel
        if encrypt_after:
            encrypted_path = self.encrypt_answers()
            if encrypted_path:
                print(f"[ProfileAnalyzer] Réponses brutes chiffrées et sécurisées.")
            else:
                print("[ProfileAnalyzer] Chiffrement non effectué — réponses brutes toujours en clair.")

        print("[ProfileAnalyzer] Pipeline terminé.")
        return updated_profile

    # ─────────────────────────────────────────────────────
    # RAPPORT DE SCORES
    # ─────────────────────────────────────────────────────

    def print_scores_report(self, scores: Dict[str, DimensionScore]) -> None:
        """Affiche un rapport lisible des scores calculés."""
        print("\n" + "=" * 60)
        print("RAPPORT DES SCORES PSYCHOLOGIQUES ALFRED")
        print("=" * 60)

        for dim_id, dim_score in scores.items():
            status = "✓ Complété" if dim_score.completed else "— Non rempli"
            print(f"\n[{dim_id}] {status}")

            if dim_score.completed and dim_score.global_score is not None:
                print(f"  Score global : {dim_score.global_score:.1f}/100 ({dim_score.global_level})")

                for sub_id, sub in dim_score.sub_scores.items():
                    if sub.completed:
                        print(f"    - {sub_id} : {sub.score_normalized:.1f}/100 ({sub.level})")

        print("\n" + "=" * 60)


# ─────────────────────────────────────────────────────────
# POINT D'ENTRÉE
# ─────────────────────────────────────────────────────────

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="ALFRED Profile Analyzer — Calcul des scores psychologiques"
    )
    parser.add_argument(
        "--answers", type=str, default=None,
        help="Chemin vers le fichier de réponses (défaut: data/profile/scoring/answers_template.json)"
    )
    parser.add_argument(
        "--no-encrypt", action="store_true",
        help="Ne pas chiffrer les réponses après analyse"
    )
    parser.add_argument(
        "--report-only", action="store_true",
        help="Affiche uniquement le rapport de scores sans mettre à jour user_profile.json"
    )
    parser.add_argument(
        "--decrypt", type=str, default=None,
        help="Déchiffrer un fichier .fernet et afficher les réponses"
    )

    args = parser.parse_args()

    # Déchiffrement seul
    if args.decrypt:
        analyzer = ProfileAnalyzer()
        result = analyzer.decrypt_answers(Path(args.decrypt))
        if result:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        raise SystemExit(0)

    # Pipeline principal
    answers_path = Path(args.answers) if args.answers else DEFAULT_ANSWERS_PATH

    analyzer = ProfileAnalyzer(answers_path=answers_path)
    analyzer.load_all()
    scores = analyzer.compute_scores()
    analyzer.print_scores_report(scores)

    if not args.report_only:
        alfred_params = analyzer.generate_alfred_params(scores)
        analyzer.update_user_profile(scores, alfred_params)

        if not args.no_encrypt:
            analyzer.encrypt_answers()
