"""
security_governance.py
Gouvernance sécurité ALFRED — Bloc 20.

Évalue la posture de sécurité, génère une matrice de risques
et des recommandations prioritisées.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

try:
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).resolve().parents[2] / ".env")
except ImportError:
    pass

_BASE = Path(__file__).resolve().parents[2]

_SEVERITY_ORDER = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}
_SEVERITY_SCORE = {"CRITICAL": 4, "HIGH": 3, "MEDIUM": 2, "LOW": 1}


class SecurityGovernance:
    """Évalue la posture sécurité et produit des recommandations prioritisées."""

    def __init__(self) -> None:
        self._findings: list[dict[str, Any]] = []

    def _chk(self, title: str, ok: bool, severity: str, recommendation: str, category: str) -> None:
        self._findings.append({
            "title": title,
            "passed": ok,
            "severity": severity,
            "recommendation": recommendation,
            "category": category,
        })

    # ── Vérifications de durcissement ────────────────────────────────────────

    def run_hardening_checks(self) -> list[dict]:
        """Exécute l'ensemble des vérifications de durcissement."""
        self._findings = []

        # ── Authentification ─────────────────────────────────────────────────
        self._chk(
            "Module d'authentification PIN",
            (_BASE / "src/auth/authenticator.py").exists(),
            "CRITICAL", "Implémenter src/auth/authenticator.py (bcrypt + rate limiter)",
            "AUTHENTIFICATION",
        )

        # ── Chiffrement ──────────────────────────────────────────────────────
        has_env_key = bool(os.getenv("FERNET_KEY"))
        key_file_exists = (_BASE / "data/security/fernet.key").exists()
        self._chk(
            "Clé Fernet dans variable d'environnement (et non fichier disque)",
            has_env_key,
            "HIGH",
            "Stocker FERNET_KEY dans .env et supprimer data/security/fernet.key",
            "CHIFFREMENT",
        )
        self._chk(
            "Module de protection des données au repos",
            (_BASE / "src/security/data_protection.py").exists(),
            "HIGH", "Utiliser data_protection.py pour chiffrer les JSON sensibles",
            "CHIFFREMENT",
        )

        # ── Autorisation / RBAC ──────────────────────────────────────────────
        rbac = _BASE / "config/security/roles_permissions.json"
        rbac_ok = False
        if rbac.exists():
            try:
                rbac_ok = bool(json.loads(rbac.read_text()).get("roles"))
            except json.JSONDecodeError:
                pass
        self._chk(
            "RBAC configuré avec des rôles réels",
            rbac_ok,
            "CRITICAL", "Remplir config/security/roles_permissions.json",
            "AUTORISATION",
        )

        # ── Politique Zero Trust ─────────────────────────────────────────────
        zt = _BASE / "config/security/zero_trust_rules.json"
        zt_ok = False
        if zt.exists():
            try:
                zt_ok = len(json.loads(zt.read_text()).get("rules", [])) > 0
            except json.JSONDecodeError:
                pass
        self._chk(
            "Règles Zero Trust définies",
            zt_ok,
            "HIGH", "Définir les règles dans config/security/zero_trust_rules.json",
            "POLITIQUE",
        )

        # ── Résilience ───────────────────────────────────────────────────────
        self._chk(
            "Rate limiter avec backoff exponentiel",
            (_BASE / "src/security/rate_limiter.py").exists(),
            "HIGH", "Créer src/security/rate_limiter.py",
            "RÉSILIENCE",
        )

        # ── Validation des entrées ───────────────────────────────────────────
        self._chk(
            "Validateur d'entrée robuste (patterns étendus)",
            (_BASE / "src/security/input_validator.py").exists(),
            "HIGH", "Vérifier que input_validator.py couvre SQL, XSS, prompt injection",
            "VALIDATION",
        )

        # ── Traçabilité ──────────────────────────────────────────────────────
        audit_file = _BASE / "logs/security/audit_trail.jsonl"
        self._chk(
            "Audit trail actif et non vide",
            audit_file.exists() and audit_file.stat().st_size > 0,
            "MEDIUM", "S'assurer que les événements sont journalisés",
            "TRAÇABILITÉ",
        )
        self._chk(
            "Registre d'incidents",
            (_BASE / "data/security/incident_register.json").exists(),
            "MEDIUM", "Vérifier que incident_manager.py enregistre les incidents",
            "TRAÇABILITÉ",
        )

        # ── Tests de sécurité ────────────────────────────────────────────────
        sec_tests = _BASE / "tests/security"
        self._chk(
            "Suite de tests d'intrusion",
            sec_tests.exists() and any(sec_tests.glob("test_pentest*.py")),
            "MEDIUM", "Créer tests/security/ avec des tests pytest de pénétration",
            "TESTS",
        )

        # ── MFA ──────────────────────────────────────────────────────────────
        sec_settings = _BASE / "config/security/security_settings.json"
        mfa_ok = False
        if sec_settings.exists():
            try:
                mfa_ok = json.loads(sec_settings.read_text()).get("mfa_required", False)
            except json.JSONDecodeError:
                pass
        self._chk(
            "MFA activé dans les paramètres",
            mfa_ok,
            "MEDIUM", "Mettre mfa_required=true dans config/security/security_settings.json",
            "AUTHENTIFICATION",
        )

        # ── Secrets dans .gitignore ──────────────────────────────────────────
        gitignore = _BASE / ".gitignore"
        gi_ok = False
        if gitignore.exists():
            content = gitignore.read_text()
            gi_ok = ".env" in content and "*.key" in content
        self._chk(
            ".gitignore protège .env et *.key",
            gi_ok,
            "CRITICAL", "Ajouter .env et *.key dans .gitignore",
            "SECRETS",
        )

        # ── Filtre de sortie ─────────────────────────────────────────────────
        self._chk(
            "Filtre de sortie des données sensibles",
            (_BASE / "src/security/output_filter.py").exists(),
            "MEDIUM", "Appliquer filter_output() à toutes les réponses générées",
            "DONNÉES",
        )

        return self._findings

    # ── Matrice de risques ────────────────────────────────────────────────────

    def get_risk_matrix(self) -> list[dict]:
        """Retourne les risques non conformes triés par score de risque décroissant."""
        if not self._findings:
            self.run_hardening_checks()

        risks = []
        for f in self._findings:
            if f["passed"]:
                continue
            likelihood = 3 if f["severity"] in ("CRITICAL", "HIGH") else 2
            impact = _SEVERITY_SCORE.get(f["severity"], 1)
            risks.append({
                "risk": f["title"],
                "category": f["category"],
                "severity": f["severity"],
                "likelihood": likelihood,
                "impact": impact,
                "risk_score": likelihood * impact,
                "recommendation": f["recommendation"],
            })

        return sorted(risks, key=lambda r: -r["risk_score"])

    # ── Recommandations ───────────────────────────────────────────────────────

    def get_recommendations(self, priority: str | None = None) -> list[dict]:
        """Retourne les recommandations triées par priorité (CRITICAL > HIGH > MEDIUM > LOW)."""
        if not self._findings:
            self.run_hardening_checks()

        recs = [
            {
                "priority": f["severity"],
                "category": f["category"],
                "finding": f["title"],
                "action": f["recommendation"],
            }
            for f in self._findings if not f["passed"]
        ]

        if priority:
            recs = [r for r in recs if r["priority"] == priority.upper()]

        return sorted(recs, key=lambda r: _SEVERITY_ORDER.get(r["priority"], 99))

    # ── Rapport de gouvernance ────────────────────────────────────────────────

    def generate_governance_report(self) -> str:
        """Génère un rapport de gouvernance texte complet."""
        findings = self.run_hardening_checks()
        risks = self.get_risk_matrix()
        recs = self.get_recommendations()

        passed = sum(1 for f in findings if f["passed"])
        total = len(findings)
        score = round(passed / total * 100, 1) if total else 0.0

        lines = [
            "=" * 62,
            "  RAPPORT GOUVERNANCE SECURITE ALFRED",
            "=" * 62,
            "",
            f"  Controles reussis : {passed}/{total}  ({score}%)",
            "",
            "── Controles de durcissement " + "─" * 33,
        ]

        for f in findings:
            icon = "+" if f["passed"] else "-"
            sev = f"[{f['severity']:8}]"
            cat = f"[{f['category']:20}]"
            lines.append(f"  [{icon}] {sev} {cat} {f['title']}")

        if risks:
            lines += ["", "── Matrice de risques " + "─" * 41]
            lines.append(f"  {'Score':>5}  {'Sev':8}  {'Categorie':20}  Risque")
            lines.append("  " + "-" * 58)
            for r in risks:
                lines.append(
                    f"  {r['risk_score']:>5}  {r['severity']:8}  {r['category']:20}  {r['risk']}"
                )

        if recs:
            lines += ["", "── Recommandations prioritaires " + "─" * 30]
            for i, rec in enumerate(recs[:12], 1):
                lines.append(f"  {i:2}. [{rec['priority']:8}] [{rec['category']:20}] {rec['finding']}")
                lines.append(f"       Acton : {rec['action']}")

        lines += ["", "=" * 62]
        return "\n".join(lines)


if __name__ == "__main__":
    gov = SecurityGovernance()
    print(gov.generate_governance_report())
