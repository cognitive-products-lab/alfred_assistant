"""
════════════════════════════════════════════════════════════
PROJECT      : ALFRED
BLOCK        : B22
FUNCTION     : 22.01 / 22.05 / 22.08 / 22.15
FILE         : accessibility_manager.py
ROLE         : Coordinateur central accessibilité — politique, adaptation utilisateur, conformité WCAG

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-05-22
UPDATED      : 2026-06-03
VERSION      : V1.0
STATUS       : ACTIVE

DEPENDENCIES :
- pathlib
- json
- dataclasses
- logging
- typing

SECURITY :
- Local-first
- Security by Design

DESCRIPTION :
Gestionnaire central du Bloc 22. Coordonne la politique d'accessibilité ALFRED,
les profils utilisateur adaptatifs (AccessibilityProfile) et la conformité WCAG 2.1 AA.
Point d'entrée unique pour tous les modules B22.
════════════════════════════════════════════════════════════
"""

# ============================================================
# ALFRED — AccessibilityManager
# Gère la politique d'accessibilité, les profils utilisateur
# et la conformité WCAG 2.1 niveau AA
# ============================================================

from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from paths import PATHS

logger = logging.getLogger(__name__)

# ── Config ───────────────────────────────────────────────
_SETTINGS_PATH = PATHS.config / "accessibility" / "accessibility_settings.json"


# ── Profil d'accessibilité utilisateur ───────────────────

@dataclass
class AccessibilityProfile:
    """Préférences d'accessibilité d'un utilisateur."""
    language: str = "fr"
    tts_enabled: bool = False
    tts_rate: float = 1.0          # 0.5 → 2.0
    tts_volume: float = 1.0
    simplify_text: bool = False
    dyslexia_font: bool = False
    high_contrast: bool = False
    reduce_motion: bool = False
    neurodiversity_mode: Optional[str] = None   # "adhd" | "autism" | "dyslexia" | None
    cognitive_load_level: str = "normal"        # "low" | "normal" | "high"
    auto_summarize: bool = False
    explain_terms: bool = False
    extra: dict = field(default_factory=dict)


# ── Manager principal ─────────────────────────────────────

class AccessibilityManager:
    """
    22.01 Politique d'accessibilité
    22.05 Assistance cognitive
    22.08 Adaptation utilisateur
    22.15 Conformité WCAG 2.1 AA
    """

    WCAG_LEVEL = "AA"
    SUPPORTED_LANGUAGES = ["fr", "en", "es", "de", "it", "pt", "nl"]

    def __init__(self, settings_path: Path = _SETTINGS_PATH) -> None:
        self._settings = self._load_settings(settings_path)
        self._profiles: dict[str, AccessibilityProfile] = {}
        self._active_user: Optional[str] = None
        logger.info("AccessibilityManager initialisé.")

    # ── Paramètres ────────────────────────────────────────

    def _load_settings(self, path: Path) -> dict:
        if not path.exists():
            logger.warning("accessibility_settings.json introuvable — valeurs par défaut.")
            return {}
        with open(path, encoding="utf-8") as f:
            return json.load(f)

    # ── Profils utilisateur (22.08) ───────────────────────

    def set_user(self, user_id: str, profile: Optional[AccessibilityProfile] = None) -> None:
        """Active un profil utilisateur. Crée un profil vide si non existant."""
        self._active_user = user_id
        if user_id not in self._profiles:
            self._profiles[user_id] = profile or AccessibilityProfile()
        logger.debug("Profil accessibilité activé : %s", user_id)

    def get_profile(self, user_id: Optional[str] = None) -> AccessibilityProfile:
        """Retourne le profil actif ou celui du user_id donné."""
        uid = user_id or self._active_user
        if uid and uid in self._profiles:
            return self._profiles[uid]
        return AccessibilityProfile()

    def update_profile(self, user_id: str, **kwargs) -> AccessibilityProfile:
        """Met à jour les préférences d'un profil existant."""
        profile = self.get_profile(user_id)
        for key, value in kwargs.items():
            if hasattr(profile, key):
                setattr(profile, key, value)
        self._profiles[user_id] = profile
        return profile

    # ── Politique d'accessibilité (22.01) ─────────────────

    def get_policy_summary(self) -> dict:
        """Retourne les points clés de la politique d'accessibilité."""
        return {
            "wcag_level": self.WCAG_LEVEL,
            "supported_languages": self.SUPPORTED_LANGUAGES,
            "neurodiversity_modes": ["adhd", "autism", "dyslexia"],
            "features": [
                "tts", "simplification", "translation", "summarization",
                "dyslexia_font", "high_contrast", "reduce_motion",
                "term_explanation", "cognitive_load_adaptation",
            ],
        }

    # ── Assistance cognitive (22.05) ──────────────────────

    def should_simplify(self, user_id: Optional[str] = None) -> bool:
        return self.get_profile(user_id).simplify_text

    def should_explain_terms(self, user_id: Optional[str] = None) -> bool:
        return self.get_profile(user_id).explain_terms

    def get_cognitive_load(self, user_id: Optional[str] = None) -> str:
        return self.get_profile(user_id).cognitive_load_level

    # ── Conformité WCAG (22.15) ───────────────────────────

    def audit_wcag(self, component: str) -> dict:
        """
        Vérifie la conformité WCAG 2.1 AA d'un composant UI.
        Retourne un rapport {passed, failed, warnings, component, level}.

        V1 : audit statique basé sur la checklist connue.
        V2+ : checks dynamiques (contraste mesuré, ARIA, focus order, etc.)
        """
        checklist = self.get_wcag_checklist()

        passed   = [c for c in checklist if c["status"] == "PASS"]
        failed   = [c for c in checklist if c["status"] == "FAIL"]
        warnings = [c for c in checklist if c["status"] == "WARN"]
        todo     = [c for c in checklist if c["status"] == "TODO"]

        score = len(passed) / max(len(checklist), 1)
        compliant = len(failed) == 0 and score >= 0.5

        logger.info(
            "audit_wcag(%s) : %d/%d critères passés, %d échoués",
            component, len(passed), len(checklist), len(failed),
        )

        return {
            "component":  component,
            "level":      self.WCAG_LEVEL,
            "compliant":  compliant,
            "score":      round(score, 2),
            "passed":     passed,
            "failed":     failed,
            "warnings":   warnings,
            "todo":       todo,
            "summary": (
                f"{len(passed)} critères OK, {len(failed)} échoués, "
                f"{len(todo)} à vérifier"
            ),
        }

    def get_wcag_checklist(self) -> list[dict]:
        """Retourne la checklist WCAG 2.1 AA applicable au projet."""
        return [
            {"criterion": "1.1.1", "name": "Non-text Content", "level": "A", "status": "TODO"},
            {"criterion": "1.3.1", "name": "Info and Relationships", "level": "A", "status": "TODO"},
            {"criterion": "1.4.3", "name": "Contrast (Minimum)", "level": "AA", "status": "TODO"},
            {"criterion": "1.4.4", "name": "Resize text", "level": "AA", "status": "TODO"},
            {"criterion": "2.1.1", "name": "Keyboard", "level": "A", "status": "TODO"},
            {"criterion": "2.4.3", "name": "Focus Order", "level": "A", "status": "TODO"},
            {"criterion": "3.1.1", "name": "Language of Page", "level": "A", "status": "TODO"},
            {"criterion": "3.3.1", "name": "Error Identification", "level": "A", "status": "TODO"},
            {"criterion": "4.1.2", "name": "Name, Role, Value", "level": "A", "status": "TODO"},
        ]

    # ── Diagnostic ────────────────────────────────────────

    def status(self) -> dict:
        return {
            "active_user": self._active_user,
            "profiles_loaded": len(self._profiles),
            "wcag_level": self.WCAG_LEVEL,
            "settings_loaded": bool(self._settings),
        }


# ─────────────────────────────────────────────────────────
# Test standalone
# ─────────────────────────────────────────────────────────
if __name__ == "__main__":
    mgr = AccessibilityManager()
    mgr.set_user("celine", AccessibilityProfile(language="fr", tts_enabled=True, simplify_text=True))
    profile = mgr.get_profile("celine")
    print(f"Profil : {profile}")
    print(f"Politique : {mgr.get_policy_summary()}")
    print(f"Status : {mgr.status()}")
