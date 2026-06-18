"""
PROJECT : ALFRED
BLOCK   : B20 / RGPD
FILE    : src/security/consent_art9.py
ROLE    : Gestion du consentement renforcé Art. 9 RGPD — données sensibles de santé

Enregistre, vérifie et révoque le consentement explicite de l'utilisateur
pour le traitement des données sensibles (Art. 9 §2.a RGPD).
Chaque consentement est horodaté, versionnéet stocké dans data/consents/consent_registry.json.

Usage :
    from src.security.consent_art9 import ConsentArt9Manager
    mgr = ConsentArt9Manager()
    mgr.record_consent("celine", "health_data", method="explicit_form")
    mgr.is_consent_valid("celine", "health_data")   # True / False
    mgr.revoke_consent("celine", "health_data")
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

ROOT = Path(__file__).resolve().parents[2]
CONSENT_FILE = ROOT / "data/consents/consent_registry.json"

CONSENT_SCHEMA_VERSION = "1.0"

# Durée de validité du consentement en jours (0 = permanent jusqu'à révocation)
CONSENT_TTL_DAYS: dict[str, int] = {
    "health_data": 0,       # permanent jusqu'à révocation explicite
    "behavioral_data": 0,
    "wellbeing_tracking": 0,
}

# Catégories Art. 9 reconnues
ART9_CATEGORIES = frozenset({
    "health_data",
    "behavioral_data",
    "wellbeing_tracking",
    "biometric_data",
    "mental_health_data",
})


class ConsentArt9Manager:
    """Gestionnaire de consentement explicite Art. 9 RGPD."""

    def __init__(self, registry_path: Path = CONSENT_FILE) -> None:
        self._path = registry_path
        self._registry: dict = self._load()

    def _load(self) -> dict:
        if self._path.exists():
            try:
                return json.loads(self._path.read_text(encoding="utf-8"))
            except Exception:
                pass
        return {
            "_meta": {
                "schema_version": CONSENT_SCHEMA_VERSION,
                "created_at": datetime.now(timezone.utc).isoformat(),
                "description": "Registre des consentements Art. 9 RGPD — données sensibles",
            },
            "consents": {},
        }

    def _save(self) -> None:
        self._path.parent.mkdir(parents=True, exist_ok=True)
        self._registry["_meta"]["last_updated"] = datetime.now(timezone.utc).isoformat()
        self._path.write_text(
            json.dumps(self._registry, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    def record_consent(
        self,
        user_id: str,
        category: str,
        method: str = "explicit_form",
        purpose: str = "",
        ip_hash: Optional[str] = None,
    ) -> dict:
        """
        Enregistre un consentement explicite Art. 9.

        Args:
            user_id:  Identifiant utilisateur (pseudonymisé)
            category: Catégorie de données sensibles (voir ART9_CATEGORIES)
            method:   Méthode de collecte ("explicit_form", "double_opt_in", "oral_confirmed")
            purpose:  Finalité du traitement
            ip_hash:  Hash IP (optionnel, pour traçabilité)

        Returns:
            dict avec consent_id, status, recorded_at
        """
        if category not in ART9_CATEGORIES:
            return {"status": "ERROR", "reason": f"Catégorie Art. 9 non reconnue : {category}"}

        now = datetime.now(timezone.utc).isoformat()
        consent_id = f"{user_id}_{category}_{now[:10].replace('-','')}"

        consent_record = {
            "consent_id": consent_id,
            "user_id": user_id,
            "category": category,
            "art9_basis": "Art. 9 §2.a — Consentement explicite",
            "method": method,
            "purpose": purpose or f"Traitement données sensibles ALFRED — {category}",
            "recorded_at": now,
            "revoked_at": None,
            "revoked": False,
            "ip_hash": ip_hash,
            "schema_version": CONSENT_SCHEMA_VERSION,
        }

        key = f"{user_id}::{category}"
        if key not in self._registry["consents"]:
            self._registry["consents"][key] = []
        self._registry["consents"][key].append(consent_record)
        self._save()

        return {
            "status": "OK",
            "consent_id": consent_id,
            "category": category,
            "recorded_at": now,
        }

    def is_consent_valid(self, user_id: str, category: str) -> bool:
        """Retourne True si l'utilisateur a un consentement actif non révoqué pour cette catégorie."""
        key = f"{user_id}::{category}"
        records = self._registry["consents"].get(key, [])
        active = [r for r in records if not r.get("revoked", False)]
        return len(active) > 0

    def revoke_consent(self, user_id: str, category: str) -> dict:
        """Révoque tous les consentements actifs pour user_id / category."""
        key = f"{user_id}::{category}"
        records = self._registry["consents"].get(key, [])
        revoked_count = 0
        now = datetime.now(timezone.utc).isoformat()
        for r in records:
            if not r.get("revoked", False):
                r["revoked"] = True
                r["revoked_at"] = now
                revoked_count += 1
        if revoked_count > 0:
            self._save()
        return {
            "status": "OK" if revoked_count > 0 else "NONE_ACTIVE",
            "user_id": user_id,
            "category": category,
            "revoked_count": revoked_count,
            "revoked_at": now,
        }

    def get_consent_history(self, user_id: str) -> list[dict]:
        """Retourne l'historique complet des consentements pour un utilisateur."""
        result = []
        for key, records in self._registry["consents"].items():
            uid, _ = key.split("::", 1)
            if uid == user_id:
                result.extend(records)
        return sorted(result, key=lambda r: r.get("recorded_at", ""), reverse=True)

    def get_summary(self) -> dict:
        """Résumé du registre de consentements — sans données personnelles."""
        total = sum(len(v) for v in self._registry["consents"].values())
        active = sum(
            1 for records in self._registry["consents"].values()
            for r in records if not r.get("revoked", False)
        )
        return {
            "total_consents_recorded": total,
            "active_consents": active,
            "revoked_consents": total - active,
            "categories_covered": list({
                key.split("::")[1] for key in self._registry["consents"]
            }),
            "schema_version": CONSENT_SCHEMA_VERSION,
        }


if __name__ == "__main__":
    mgr = ConsentArt9Manager()
    r = mgr.record_consent("celine", "health_data", method="explicit_form",
                            purpose="Suivi bien-être et coaching santé ALFRED")
    print(f"[Art.9] Consentement enregistré : {r}")
    print(f"[Art.9] Valide : {mgr.is_consent_valid('celine', 'health_data')}")
    print(f"[Art.9] Résumé : {mgr.get_summary()}")
