"""
════════════════════════════════════════════════════════════
PROJECT      : ALFRED
BLOCK        : B13
FUNCTION     : 13.01
FILE         : src/health/health_profile.py
ROLE         : Suivi bien-être et profil santé utilisateur

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-05-10
UPDATED      : 2026-05-28
VERSION      : V1.0
STATUS       : ACTIVE
════════════════════════════════════════════════════════════
"""
# ============================================================
# ALFRED — src/health/health_profile.py
# Bloc 13.01 — Suivi bien-être utilisateur
#
# Fonctions couvertes :
#   13.01.001 Chargement profil santé utilisateur     ✅ V1
#   13.01.002 Gestion sévérité et adaptations actives ✅ V1
#   13.01.003 Log état session (fog, douleur, énergie) ✅ V1
#   13.01.004 Consentement et protection données santé ✅ V1
# ============================================================

import json
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

from paths import CONFIG_HEALTH, DATA_HEALTH
from src.security.security_logger import log_event

_TEMPLATE_PATH = CONFIG_HEALTH / "user_health_profile_template.json"
DATA_HEALTH.mkdir(parents=True, exist_ok=True)


# ─────────────────────────────────────────────────────────
# Dataclass état de session santé
# ─────────────────────────────────────────────────────────

@dataclass
class HealthSessionState:
    """État de santé de l'utilisateur pour la session courante."""
    fog_mode_active:      bool  = False
    pain_mode_active:     bool  = False
    flare_detected:       bool  = False
    energy_pacing_active: bool  = False
    crisis_health:        bool  = False
    active_protocol:      str | None = None
    severity_override:    str | None = None  # mild / moderate / severe
    last_signal_type:     str | None = None
    turn_count:           int   = 0


# ─────────────────────────────────────────────────────────
# Profil santé utilisateur
# ─────────────────────────────────────────────────────────

class HealthProfile:
    """
    Gestionnaire du profil santé d'un utilisateur ALFRED.

    Charge un profil JSON existant ou retourne un profil vide
    si aucun profil santé n'est configuré pour cet utilisateur.

    Le profil santé est OPTIONNEL et toujours déclaratif —
    l'utilisateur déclare ses conditions, ALFRED ne diagnostique jamais.
    """

    def __init__(self, user_id: str | None = None):
        self.user_id      = user_id or "default"
        self._profile     = {}
        self._session     = HealthSessionState()
        self._loaded      = False
        self._load()

    # ─────────────────────────────────────────────────────
    # Chargement
    # ─────────────────────────────────────────────────────

    def _load(self) -> None:
        profile_path = DATA_HEALTH / f"health_{self.user_id}.json"
        if profile_path.exists():
            try:
                self._profile = json.loads(profile_path.read_text(encoding="utf-8"))
                self._loaded  = True
                log_event(f"Profil santé chargé — user: {self.user_id}")
            except Exception as e:
                log_event(f"Erreur chargement profil santé : {e}", "WARNING")
                self._profile = {}
        else:
            self._profile = {}
            log_event(f"Aucun profil santé — user: {self.user_id}")

    def save(self) -> None:
        """Persiste le profil santé (données chiffrées en production via Bloc 20)."""
        if not self._profile:
            return
        profile_path = DATA_HEALTH / f"health_{self.user_id}.json"
        try:
            profile_path.write_text(
                json.dumps(self._profile, indent=2, ensure_ascii=False),
                encoding="utf-8"
            )
        except Exception as e:
            log_event(f"Erreur sauvegarde profil santé : {e}", "WARNING")

    # ─────────────────────────────────────────────────────
    # Propriétés principales
    # ─────────────────────────────────────────────────────

    @property
    def is_active(self) -> bool:
        """True si un profil santé est configuré et actif."""
        return bool(self._profile) and self._profile.get("profile_status", {}).get("active", False)

    @property
    def conditions(self) -> list[str]:
        """Liste des conditions chroniques déclarées par l'utilisateur."""
        c = self._profile.get("conditions", {})
        primary   = [c["primary"]] if c.get("primary") else []
        secondary = c.get("secondary", [])
        return primary + secondary

    @property
    def severity(self) -> str:
        """Niveau de sévérité actuel : mild | moderate | severe."""
        if self._session.severity_override:
            return self._session.severity_override
        return self._profile.get("profile_status", {}).get("severity_level", "mild")

    @property
    def interaction_prefs(self) -> dict:
        return self._profile.get("interaction_preferences", {})

    @property
    def preferred_language(self) -> str:
        return self.interaction_prefs.get("language", "fr")

    @property
    def fog_auto_activate(self) -> bool:
        return self.interaction_prefs.get("fog_mode_auto_activate", True)

    @property
    def check_in_frequency(self) -> str:
        return self.interaction_prefs.get("preferred_check_in_frequency", "every_2_turns")

    # ─────────────────────────────────────────────────────
    # État de session
    # ─────────────────────────────────────────────────────

    @property
    def session(self) -> HealthSessionState:
        return self._session

    def activate_fog_mode(self) -> None:
        self._session.fog_mode_active = True
        log_event("Fog mode activé — Bloc 13")

    def deactivate_fog_mode(self) -> None:
        self._session.fog_mode_active = False

    def activate_pain_mode(self) -> None:
        self._session.pain_mode_active = True

    def activate_flare(self) -> None:
        self._session.flare_detected = True
        self._session.severity_override = "severe"
        log_event("Poussée détectée — Bloc 13", "WARNING")

    def activate_energy_pacing(self) -> None:
        self._session.energy_pacing_active = True

    def set_protocol(self, protocol_id: str) -> None:
        self._session.active_protocol  = protocol_id
        self._session.last_signal_type = protocol_id

    def increment_turn(self) -> None:
        self._session.turn_count += 1

    def reset_session(self) -> None:
        self._session = HealthSessionState()

    # ─────────────────────────────────────────────────────
    # Création d'un profil depuis template
    # ─────────────────────────────────────────────────────

    @classmethod
    def create_from_template(
        cls,
        user_id: str,
        conditions: list[str] | None = None,
        severity: str = "mild",
        consent: bool = True,
    ) -> "HealthProfile":
        """
        Crée un profil santé utilisateur depuis le template officiel.
        Consentement explicite requis — données sensibles.
        """
        if not consent:
            raise ValueError("Consentement explicite requis pour créer un profil santé.")

        if not _TEMPLATE_PATH.exists():
            raise FileNotFoundError(f"Template introuvable : {_TEMPLATE_PATH}")

        template = json.loads(_TEMPLATE_PATH.read_text(encoding="utf-8"))

        now = datetime.now().isoformat(timespec="seconds")
        template["metadata"]["is_template"]   = False
        template["metadata"]["profile_id"]    = str(uuid.uuid4())
        template["metadata"]["user_id"]       = user_id
        template["metadata"]["created_at"]    = now
        template["metadata"]["updated_at"]    = now
        template["metadata"]["consent_given"] = True
        template["metadata"]["consent_date"]  = now

        template["profile_status"]["active"]         = True
        template["profile_status"]["severity_level"] = severity
        template["profile_status"]["last_assessment"] = now

        if conditions:
            template["conditions"]["primary"]   = conditions[0] if conditions else None
            template["conditions"]["secondary"] = conditions[1:] if len(conditions) > 1 else []

        profile_path = DATA_HEALTH / f"health_{user_id}.json"
        DATA_HEALTH.mkdir(parents=True, exist_ok=True)
        profile_path.write_text(
            json.dumps(template, indent=2, ensure_ascii=False),
            encoding="utf-8"
        )

        instance = cls(user_id=user_id)
        log_event(f"Profil santé créé — user: {user_id}, conditions: {conditions}")
        return instance

    def __repr__(self) -> str:
        return (
            f"HealthProfile(user={self.user_id}, "
            f"active={self.is_active}, "
            f"conditions={self.conditions}, "
            f"severity={self.severity})"
        )
