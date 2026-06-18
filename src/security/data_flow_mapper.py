"""
════════════════════════════════════════════════════════════
PROJECT      : ALFRED
BLOCK        : B20
FUNCTION     : 20.19
FILE         : src/security/data_flow_mapper.py
ROLE         : Cartographie des flux de données personnelles (RGPD Art. 30)

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-06-02
UPDATED      : 2026-06-02
VERSION      : V1.0
STATUS       : ACTIVE

DESCRIPTION :
Urbanisation SSI — Phase 2.
Cartographie les traitements de données personnelles conformément
à l'article 30 RGPD (registre des activités de traitement).
Identifie : finalité, base légale, catégories de données,
destinataires, durée de conservation, mesures de sécurité.
Produit un registre JSON exportable CNIL.
════════════════════════════════════════════════════════════
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from src.security.security_logger import log_event

_ROOT = Path(__file__).resolve().parents[2]


# ─── Modèle de traitement RGPD ────────────────────────────────────────────────

@dataclass
class DataTreatment:
    """Représente un traitement de données au sens de l'Art. 30 RGPD."""
    id:                   str
    name:                 str
    purpose:              str                    # finalité du traitement
    legal_basis:          str                    # base légale (consentement, intérêt légitime…)
    data_categories:      list[str] = field(default_factory=list)  # catégories de DCP
    data_subjects:        list[str] = field(default_factory=list)  # personnes concernées
    recipients:           list[str] = field(default_factory=list)  # destinataires
    retention_days:       int = 365              # durée de conservation (jours)
    storage_location:     str = "local"          # lieu de stockage
    security_measures:    list[str] = field(default_factory=list)  # mesures de sécurité
    files:                list[str] = field(default_factory=list)  # fichiers concernés
    cross_border:         bool = False           # transfert hors UE
    notes:                str = ""


# ─── Registre des traitements ALFRED ──────────────────────────────────────────

ALFRED_TREATMENTS: list[DataTreatment] = [

    DataTreatment(
        id="T01",
        name="Profil utilisateur et personnalisation",
        purpose="Adapter le comportement d'ALFRED aux préférences et besoins de l'utilisateur",
        legal_basis="Consentement explicite (Art. 6.1.a RGPD)",
        data_categories=["Identité", "Préférences", "Historique d'interaction", "Données comportementales"],
        data_subjects=["Utilisateur principal (Céline)"],
        recipients=["Aucun tiers — traitement 100% local"],
        retention_days=3650,
        storage_location="local — data/users/ + data/personality/",
        security_measures=["Chiffrement Fernet AES-128", "Accès par authentification PIN", "Zero Trust RBAC"],
        files=["data/users/instances/", "data/personality/instances/", "private_data/user_profiles/"],
        cross_border=False,
        notes="Données strictement locales. Aucune synchronisation cloud.",
    ),

    DataTreatment(
        id="T02",
        name="Mémoire conversationnelle",
        purpose="Conserver le contexte des échanges pour assurer la continuité de la relation",
        legal_basis="Consentement explicite + Intérêt légitime pour la qualité du service",
        data_categories=["Contenu des conversations", "Données émotionnelles", "Informations personnelles mentionnées"],
        data_subjects=["Utilisateur principal"],
        recipients=["Aucun"],
        retention_days=1825,
        storage_location="local — data/memory/",
        security_measures=["Accès restreint par authentification", "Chiffrement au repos", "Audit trail"],
        files=["data/memory/episodic/dialogue_history.json", "data/memory/long_term_memory.db"],
        cross_border=False,
        notes="Données épisodiques et long terme. L'utilisateur peut demander effacement (Art. 17 RGPD).",
    ),

    DataTreatment(
        id="T03",
        name="Journal de sécurité et audit",
        purpose="Traçabilité des événements de sécurité et détection des incidents",
        legal_basis="Intérêt légitime — sécurité du système (Art. 6.1.f RGPD)",
        data_categories=["Journaux d'accès", "Identifiants techniques", "Événements de sécurité"],
        data_subjects=["Utilisateur principal"],
        recipients=["Aucun tiers"],
        retention_days=90,
        storage_location="local — logs/security/",
        security_measures=["Fichiers JSONL immuables", "Rotation automatique", "Accès restreint"],
        files=["logs/security/audit_trail.jsonl", "logs/security/security.log"],
        cross_border=False,
        notes="Rotation à 10 000 lignes / 5 Mo. Archives horodatées.",
    ),

    DataTreatment(
        id="T04",
        name="Données de santé et bien-être",
        purpose="Adapter le support émotionnel et cognitif selon l'état de l'utilisateur",
        legal_basis="Consentement explicite renforcé (Art. 9.2.a RGPD — données de santé)",
        data_categories=["Données de santé", "Données émotionnelles", "État de fatigue/stress"],
        data_subjects=["Utilisateur principal"],
        recipients=["Aucun"],
        retention_days=730,
        storage_location="local — src/health/ + data/",
        security_measures=["Chiffrement renforcé", "Accès OWNER uniquement", "Pas de partage"],
        files=["src/health/", "data/health/"],
        cross_border=False,
        notes="Catégorie spéciale Art. 9. Traitement uniquement local. Supervision médicale recommandée.",
    ),

    DataTreatment(
        id="T05",
        name="Journalisation des incidents de sécurité",
        purpose="Gestion et traçabilité des incidents de sécurité",
        legal_basis="Obligation légale (Art. 6.1.c) + Intérêt légitime sécurité",
        data_categories=["Événements de sécurité", "Vecteurs d'attaque (anonymisés)"],
        data_subjects=["Utilisateur principal (données techniques uniquement)"],
        recipients=["Aucun tiers"],
        retention_days=365,
        storage_location="local — data/security/incident_register.json",
        security_measures=["Chiffrement", "Purge automatique des données de test"],
        files=["data/security/incident_register.json"],
        cross_border=False,
        notes="Incidents de démo purgés automatiquement après chaque session de test.",
    ),

    DataTreatment(
        id="T06",
        name="Authentification et gestion des sessions",
        purpose="Contrôle d'accès et authentification de l'utilisateur",
        legal_basis="Intérêt légitime sécurité + Consentement (Art. 6.1.a/f)",
        data_categories=["Credentials hashés (PIN bcrypt)", "Tokens de session", "Données MFA TOTP"],
        data_subjects=["Utilisateur principal"],
        recipients=["Aucun"],
        retention_days=30,
        storage_location="local — data/security/",
        security_measures=["bcrypt pour les PIN", "Fernet pour secrets MFA", "TTL session configurable"],
        files=["data/security/mfa_secrets.json", "data/security/pin_hash.json"],
        cross_border=False,
        notes="Secrets MFA chiffrés au repos. PIN jamais stocké en clair.",
    ),
]


# ─── Génération du registre ───────────────────────────────────────────────────

def get_registry() -> list[DataTreatment]:
    """Retourne le registre complet des traitements."""
    return ALFRED_TREATMENTS


def get_treatment_by_id(treatment_id: str) -> DataTreatment | None:
    """Retourne un traitement par son identifiant."""
    return next((t for t in ALFRED_TREATMENTS if t.id == treatment_id), None)


def build_rgpd_report() -> dict[str, Any]:
    """
    Construit le registre RGPD Art. 30 au format JSON.

    Returns:
        dict conforme au format registre des activités de traitement CNIL.
    """
    now = datetime.now(timezone.utc).isoformat()

    treatments_dict = []
    for t in ALFRED_TREATMENTS:
        d = asdict(t)
        d["retention_human"] = f"{t.retention_days} jours ({t.retention_days // 365} an(s))" if t.retention_days >= 365 else f"{t.retention_days} jours"
        d["cross_border_text"] = "Oui" if t.cross_border else "Non — traitement 100% local"
        treatments_dict.append(d)

    # Stats
    has_health_data   = any(t.id == "T04" for t in ALFRED_TREATMENTS)
    cross_border_count = sum(1 for t in ALFRED_TREATMENTS if t.cross_border)

    return {
        "_meta": {
            "project": "ALFRED",
            "block":   "B20",
            "file":    "rgpd_register.json",
            "role":    "Registre des activités de traitement — Art. 30 RGPD",
            "version": "V1.0",
            "status":  "ACTIVE",
        },
        "organization":        "Cognitive Product Lab",
        "dpo_contact":         "fondatrice@cognitiveproductlab.fr",
        "generated_at":        now,
        "treatments_count":    len(ALFRED_TREATMENTS),
        "special_categories":  has_health_data,
        "cross_border_count":  cross_border_count,
        "legal_bases_used": list({t.legal_basis.split("(")[0].strip() for t in ALFRED_TREATMENTS}),
        "treatments": treatments_dict,
        "summary": {
            "total_treatments":    len(ALFRED_TREATMENTS),
            "local_only":          sum(1 for t in ALFRED_TREATMENTS if not t.cross_border),
            "max_retention_days":  max(t.retention_days for t in ALFRED_TREATMENTS),
            "data_subject_rights": [
                "Art. 15 — Droit d'accès",
                "Art. 16 — Droit de rectification",
                "Art. 17 — Droit à l'effacement",
                "Art. 20 — Droit à la portabilité",
                "Art. 21 — Droit d'opposition",
            ],
        },
    }


def export_rgpd_report(output_path: Path | None = None) -> Path:
    """Exporte le registre RGPD en JSON."""
    out = output_path or (_ROOT / "dashboard" / "dashboard_security" / "rgpd_register.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    report = build_rgpd_report()
    out.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    log_event(f"data_flow_mapper: registre RGPD exporté → {out} ({len(ALFRED_TREATMENTS)} traitements)")
    return out


def check_rgpd_compliance() -> dict[str, Any]:
    """
    Vérifie la conformité basique du registre RGPD.

    Returns:
        dict avec checks, score, recommandations.
    """
    checks = []
    score  = 0

    def chk(title: str, ok: bool, recommendation: str = "") -> None:
        checks.append({"title": title, "ok": ok, "recommendation": recommendation})
        nonlocal score
        if ok:
            score += 1

    total = len(ALFRED_TREATMENTS)
    chk("Registre des traitements présent",    total > 0)
    chk("Tous les traitements ont une base légale",
        all(t.legal_basis for t in ALFRED_TREATMENTS))
    chk("Tous les traitements ont une finalité",
        all(t.purpose for t in ALFRED_TREATMENTS))
    chk("Durées de conservation définies",
        all(t.retention_days > 0 for t in ALFRED_TREATMENTS))
    chk("Mesures de sécurité documentées",
        all(t.security_measures for t in ALFRED_TREATMENTS))
    chk("Aucun transfert hors UE non justifié",
        not any(t.cross_border for t in ALFRED_TREATMENTS),
        "Documenter la base légale pour chaque transfert hors UE")
    chk("Données de santé identifiées (Art. 9)",
        any("santé" in " ".join(t.data_categories).lower() for t in ALFRED_TREATMENTS))
    chk("Traitements locaux uniquement",
        all(not t.cross_border for t in ALFRED_TREATMENTS))

    max_score = len(checks)
    return {
        "score":           score,
        "max_score":       max_score,
        "compliance_rate": round(score / max_score * 100, 1) if max_score else 0,
        "checks":          checks,
        "grade":           "A" if score == max_score else "B" if score >= max_score * 0.85 else "C",
    }
