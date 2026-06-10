"""
════════════════════════════════════════════════════════════
PROJECT      : ALFRED
BLOCK        : B20
FUNCTION     : 20.20
FILE         : src/security/risk_engine.py
ROLE         : Moteur d'analyse de risques SSI (EBIOS RM simplifié)

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-06-02
UPDATED      : 2026-06-02
VERSION      : V1.0
STATUS       : ACTIVE

DESCRIPTION :
Urbanisation SSI — Phase 3.
Implémente une analyse de risques inspirée d'EBIOS RM :
- Inventaire des sources de menace (acteurs)
- Événements redoutés (scénarios de risque)
- Vraisemblance × Impact → score résiduel
- Matrice de risques exportable
- Intégration avec les modules de sécurité existants pour
  ajuster les scores en fonction de la posture réelle.
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

# ─── Niveaux de vraisemblance et impact ───────────────────────────────────────

LIKELIHOOD = {"MINIMAL": 1, "FAIBLE": 2, "SIGNIFICATIF": 3, "MAXIMAL": 4}
IMPACT     = {"NEGLIGEABLE": 1, "LIMITE": 2, "IMPORTANT": 3, "CRITIQUE": 4}


def risk_score(likelihood: str, impact: str) -> int:
    """Score de risque = vraisemblance × impact (1→16)."""
    return LIKELIHOOD.get(likelihood, 1) * IMPACT.get(impact, 1)


def risk_level(score: int) -> str:
    if score >= 12: return "CRITIQUE"
    if score >= 8:  return "ELEVE"
    if score >= 4:  return "MODERE"
    return "FAIBLE"


# ─── Modèle de scénario de risque ────────────────────────────────────────────

@dataclass
class RiskScenario:
    id:                 str
    threat_source:      str       # source de menace (acteur)
    feared_event:       str       # événement redouté
    attack_path:        str       # chemin d'attaque
    asset_targeted:     str       # actif ciblé
    likelihood:         str       # MINIMAL / FAIBLE / SIGNIFICATIF / MAXIMAL
    impact:             str       # NEGLIGEABLE / LIMITE / IMPORTANT / CRITIQUE
    existing_measures:  list[str] = field(default_factory=list)  # contrôles en place
    residual_measures:  list[str] = field(default_factory=list)  # mesures complémentaires
    category:           str = ""
    notes:              str = ""

    @property
    def raw_score(self) -> int:
        return risk_score(self.likelihood, self.impact)

    @property
    def level(self) -> str:
        return risk_level(self.raw_score)


# ─── Catalogue de risques ALFRED ─────────────────────────────────────────────

ALFRED_RISKS: list[RiskScenario] = [

    # ── Accès non autorisé ────────────────────────────────────────────────────
    RiskScenario(
        id="R01",
        threat_source="Attaquant externe / script automatisé",
        feared_event="Compromission du compte OWNER par force brute",
        attack_path="Tentatives répétées de connexion → bruteforce PIN",
        asset_targeted="Authentification (auth_manager.py, PIN)",
        likelihood="SIGNIFICATIF",
        impact="CRITIQUE",
        existing_measures=[
            "rate_limiter.py — 5 essais max, backoff exponentiel",
            "bcrypt pour le PIN — coût computationnel élevé",
            "MFA TOTP obligatoire (OWNER/ADMIN)",
        ],
        category="AUTHENTIFICATION",
    ),

    RiskScenario(
        id="R02",
        threat_source="Attaquant avec accès physique au PC",
        feared_event="Extraction des clés cryptographiques depuis le disque",
        attack_path="Accès au fichier .env ou data/security/ directement",
        asset_targeted="Clés Fernet, secrets MFA (C4)",
        likelihood="FAIBLE",
        impact="CRITIQUE",
        existing_measures=[
            "FERNET_KEY dans .env uniquement (pas sur disque)",
            "mfa_secrets.json chiffré Fernet",
            ".gitignore protège .env et *.key",
            "Backup chiffré optionnel",
        ],
        residual_measures=["Chiffrement disque complet (BitLocker/VeraCrypt) — V2"],
        category="CRYPTOGRAPHIE",
    ),

    # ── Injection et exploitation ─────────────────────────────────────────────
    RiskScenario(
        id="R03",
        threat_source="Utilisateur malveillant / test d'intrusion",
        feared_event="Injection SQL/XSS/commande via l'interface conversationnelle",
        attack_path="Saisie de payload malveillant → pipeline non filtré",
        asset_targeted="Pipeline conversationnel, base de données",
        likelihood="SIGNIFICATIF",
        impact="IMPORTANT",
        existing_measures=[
            "input_validator.py — 25+ patterns, Unicode homographes",
            "threat_detector.py — score cumulatif, null byte",
            "unicode_sanitizer.py — NFKC + translitération",
            "output_filter.py — masquage PII",
        ],
        category="INJECTION",
    ),

    RiskScenario(
        id="R04",
        threat_source="LLM / prompt injection indirecte",
        feared_event="Jailbreak ou exfiltration de données via manipulation du LLM",
        attack_path="Prompt crafté → LLM ignore ses instructions → fuite de secrets",
        asset_targeted="Réponses LLM, données personnelles C3",
        likelihood="SIGNIFICATIF",
        impact="IMPORTANT",
        existing_measures=[
            "prompt_guard.py — 4/4 jailbreaks bloqués (EN+FR)",
            "output_filter.py — secrets masqués dans les réponses",
            "zero_trust_orchestrator — pipeline avant envoi LLM",
        ],
        residual_measures=["Sandbox LLM isolé — V3", "Monitoring des réponses — V2"],
        category="IA",
    ),

    # ── Intégrité et disponibilité ────────────────────────────────────────────
    RiskScenario(
        id="R05",
        threat_source="Erreur humaine / bug logiciel",
        feared_event="Corruption ou perte des données de mémoire conversationnelle",
        attack_path="Bug dans memory_manager → écriture corrompue",
        asset_targeted="data/memory/ (C3)",
        likelihood="FAIBLE",
        impact="IMPORTANT",
        existing_measures=[
            "backup_security.py V2 — backup chiffré + SHA-256",
            "Vérification intégrité avant restore",
            "Rotation 10 derniers backups",
        ],
        residual_measures=["Backup automatique quotidien — daily_update.py V2"],
        category="DISPONIBILITE",
    ),

    RiskScenario(
        id="R06",
        threat_source="Ransomware / malware",
        feared_event="Chiffrement malveillant des données ALFRED",
        attack_path="Malware sur le PC → chiffrement de D:\\PROJET_ALFRED\\",
        asset_targeted="Ensemble des données locales",
        likelihood="FAIBLE",
        impact="CRITIQUE",
        existing_measures=[
            "Windows Defender actif",
            "Données non partagées sur réseau",
            "Backups locaux dans backup/security/",
        ],
        residual_measures=[
            "Backup externe chiffré — V2",
            "Snapshot VSS automatique — V2",
        ],
        category="DISPONIBILITE",
    ),

    # ── SSRF et réseau ────────────────────────────────────────────────────────
    RiskScenario(
        id="R07",
        threat_source="Attaquant réseau local",
        feared_event="SSRF — accès aux ressources réseau internes via ALFRED",
        attack_path="URL malveillante → ALFRED requête vers 192.168.x.x",
        asset_targeted="Réseau local, autres équipements",
        likelihood="FAIBLE",
        impact="IMPORTANT",
        existing_measures=[
            "network_security.py — blocage IPs privées et localhost",
            "check_url_ssrf() — schémas interdits (gopher, ldap, file)",
            "Domain reputation blocklist",
        ],
        category="RESEAU",
    ),

    # ── Vie privée ───────────────────────────────────────────────────────────
    RiskScenario(
        id="R08",
        threat_source="Tiers non autorisé / fuite accidentelle",
        feared_event="Exposition de données personnelles C3/C4 dans les dashboards web",
        attack_path="JSON avec données non anonymisées pushé sur ALFRED_WEB",
        asset_targeted="Données personnelles, secrets (C3/C4)",
        likelihood="SIGNIFICATIF",
        impact="IMPORTANT",
        existing_measures=[
            "Anonymisation automatique des JSON dashboard (device_id, user_id masqués)",
            "Notice 'Vue publique — données anonymisées' sur le site",
            "Règle CRITIQUE dans la PSSI : jamais de C3/C4 sur ALFRED_WEB",
            "daily_update.py sanitize avant push",
        ],
        category="VIE_PRIVEE",
    ),
]


# ─── Calcul de posture réelle ─────────────────────────────────────────────────

def get_real_posture() -> dict[str, Any]:
    """
    Interroge les modules de sécurité pour évaluer la posture réelle.
    Ajuste les scores de risque en conséquence.
    """
    posture: dict[str, Any] = {
        "mfa_active":          False,
        "backup_ok":           False,
        "audit_active":        False,
        "rate_limiter_ok":     True,
        "output_filter_ok":    True,
    }

    try:
        from src.security.mfa_manager import is_mfa_required
        posture["mfa_active"] = is_mfa_required("OWNER")
    except Exception:
        pass

    try:
        from src.security.backup_security import summarize_backups
        s = summarize_backups()
        posture["backup_ok"] = s.get("total_backups", 0) >= 1
    except Exception:
        pass

    try:
        from src.security.audit_trail import AUDIT_FILE
        posture["audit_active"] = AUDIT_FILE.exists()
    except Exception:
        pass

    return posture


# ─── Génération de la matrice de risques ──────────────────────────────────────

def build_risk_matrix(adjust_for_posture: bool = True) -> dict[str, Any]:
    """
    Construit la matrice de risques ALFRED.

    Args:
        adjust_for_posture : True pour ajuster les scores selon la posture réelle.

    Returns:
        dict avec matrice, stats par niveau, recommandations prioritaires.
    """
    posture = get_real_posture() if adjust_for_posture else {}

    scenarios_dict = []
    by_level: dict[str, int] = {"CRITIQUE": 0, "ELEVE": 0, "MODERE": 0, "FAIBLE": 0}

    for rs in ALFRED_RISKS:
        d = asdict(rs)
        d["raw_score"] = rs.raw_score
        d["level"]     = rs.level

        # Ajustement posture : MFA actif → réduit R01
        if adjust_for_posture:
            if rs.id == "R01" and posture.get("mfa_active"):
                d["level"]     = "MODERE"
                d["raw_score"] = 6
                d["posture_note"] = "MFA TOTP actif — risque réduit"
            if rs.id == "R05" and posture.get("backup_ok"):
                d["level"]     = "FAIBLE"
                d["raw_score"] = 2
                d["posture_note"] = "Backups présents et intègres — risque réduit"

        by_level[d["level"]] += 1
        scenarios_dict.append(d)

    # Trier par score décroissant
    scenarios_dict.sort(key=lambda x: -x["raw_score"])

    # Recommandations prioritaires (CRITIQUE + ELEVE)
    priority = [
        {
            "id": s["id"],
            "feared_event": s["feared_event"],
            "level": s["level"],
            "score": s["raw_score"],
            "next_measures": s.get("residual_measures", []),
        }
        for s in scenarios_dict
        if s["level"] in {"CRITIQUE", "ELEVE"} and s.get("residual_measures")
    ]

    return {
        "_meta": {
            "project": "ALFRED",
            "block":   "B20",
            "file":    "risk_matrix.json",
            "role":    "Matrice de risques SSI — EBIOS RM simplifié",
            "version": "V1.0",
            "status":  "ACTIVE",
        },
        "generated_at":      datetime.now(timezone.utc).isoformat(),
        "method":            "EBIOS RM simplifié",
        "scenarios_count":   len(ALFRED_RISKS),
        "by_level":          by_level,
        "risk_score":        sum(s["raw_score"] for s in scenarios_dict),
        "posture":           posture,
        "scenarios":         scenarios_dict,
        "priority_actions":  priority,
        "global_level":      "ELEVE" if by_level["CRITIQUE"] > 0 else "MODERE" if by_level["ELEVE"] > 0 else "FAIBLE",
    }


def export_risk_matrix(output_path: Path | None = None) -> Path:
    """Exporte la matrice de risques en JSON."""
    out = output_path or (_ROOT / "dashboard" / "dashboard_security" / "risk_matrix.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    matrix = build_risk_matrix()
    out.write_text(json.dumps(matrix, indent=2, ensure_ascii=False), encoding="utf-8")
    log_event(f"risk_engine: matrice exportée → {out} ({len(ALFRED_RISKS)} scénarios)")
    return out
