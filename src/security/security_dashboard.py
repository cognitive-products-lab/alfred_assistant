"""
security_dashboard.py
Tableau de bord sécurité ALFRED — Bloc 20.

Agrège les métriques de sécurité, calcule un score et génère des rapports.
"""

from __future__ import annotations

import json
import os
from collections import Counter, defaultdict
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any

try:
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).resolve().parents[2] / ".env")
except ImportError:
    pass

from src.security.security_logger import log_event

_AUDIT_FILE = Path("logs/security/audit_trail.jsonl")
_INCIDENT_FILE = Path("data/security/incident_register.json")
_SECURITY_LOG = Path("logs/security/security.log")
_TRUSTED_DEVICES = Path("data/security/trusted_devices.json")


class SecurityDashboard:
    """Tableau de bord sécurité en lecture seule."""

    def __init__(self, lookback_hours: int = 24) -> None:
        self.lookback_hours = lookback_hours
        self._cutoff = datetime.now(timezone.utc) - timedelta(hours=lookback_hours)

    # ── Chargement des données ────────────────────────────────────────────────

    def _load_audit_events(self) -> list[dict]:
        if not _AUDIT_FILE.exists():
            return []
        events: list[dict] = []
        for line in _AUDIT_FILE.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                ev = json.loads(line)
                ts = datetime.fromisoformat(ev.get("timestamp", "1970-01-01T00:00:00+00:00"))
                if ts >= self._cutoff:
                    events.append(ev)
            except (json.JSONDecodeError, ValueError):
                continue
        return events

    def _load_incidents(self) -> list[dict]:
        if not _INCIDENT_FILE.exists():
            return []
        try:
            data = json.loads(_INCIDENT_FILE.read_text(encoding="utf-8"))
            return [
                inc for inc in data
                if datetime.fromisoformat(inc.get("timestamp", "1970-01-01T00:00:00+00:00")) >= self._cutoff
            ]
        except (json.JSONDecodeError, ValueError):
            return []

    # ── Métriques publiques ───────────────────────────────────────────────────

    def get_audit_summary(self) -> dict[str, Any]:
        """Résumé de l'audit trail sur la période de lookback."""
        events = self._load_audit_events()
        decisions = Counter(ev.get("decision", "UNKNOWN") for ev in events)
        actions = Counter(ev.get("action", "UNKNOWN") for ev in events)
        users = Counter(ev.get("user_id", "UNKNOWN") for ev in events)
        denials = sum(v for k, v in decisions.items() if "DENY" in k)

        return {
            "period_hours": self.lookback_hours,
            "total_events": len(events),
            "decisions": dict(decisions),
            "top_actions": dict(actions.most_common(5)),
            "top_users": dict(users.most_common(5)),
            "total_denials": denials,
            "denial_rate": round(denials / len(events) * 100, 1) if events else 0.0,
        }

    def get_threat_summary(self) -> dict[str, Any]:
        """Résumé des menaces détectées."""
        events = self._load_audit_events()
        threat_events = [ev for ev in events if ev.get("decision") == "DENY_THREAT"]
        by_user: dict[str, int] = defaultdict(int)
        for ev in threat_events:
            by_user[ev.get("user_id", "unknown")] += 1

        return {
            "total_threats": len(threat_events),
            "threats_by_user": dict(sorted(by_user.items(), key=lambda x: -x[1])[:5]),
        }

    def get_incident_summary(self) -> dict[str, Any]:
        """Résumé des incidents de sécurité."""
        incidents = self._load_incidents()
        by_level = Counter(inc.get("level", "UNKNOWN") for inc in incidents)
        by_status = Counter(inc.get("status", "UNKNOWN") for inc in incidents)

        return {
            "total_incidents": len(incidents),
            "by_level": dict(by_level),
            "by_status": dict(by_status),
            "open_critical": sum(
                1 for i in incidents
                if i.get("level") == "CRITICAL" and i.get("status") == "OPEN"
            ),
        }

    def get_device_summary(self) -> dict[str, Any]:
        """Résumé des appareils enregistrés."""
        if not _TRUSTED_DEVICES.exists():
            return {"total_devices": 0, "trusted": 0, "revoked": 0}
        try:
            devices: dict = json.loads(_TRUSTED_DEVICES.read_text(encoding="utf-8"))
            trusted = sum(1 for d in devices.values() if d.get("trusted", False))
            revoked = len(devices) - trusted
            return {"total_devices": len(devices), "trusted": trusted, "revoked": revoked}
        except (json.JSONDecodeError, AttributeError):
            return {"total_devices": 0, "trusted": 0, "revoked": 0}

    def get_security_score(self) -> dict[str, Any]:
        """
        Score de sécurité global (0–100) basé sur la posture de configuration.

        Returns:
            {"score": int, "grade": str, "max_score": 100, "deductions": list}
        """
        score = 100
        deductions: list[dict] = []

        def deduct(points: int, reason: str, category: str) -> None:
            nonlocal score
            score = max(0, score - points)
            deductions.append({"category": category, "reason": reason, "points": -points})

        # Chiffrement
        if not Path("data/security/fernet.key").exists() and not os.getenv("FERNET_KEY"):
            deduct(20, "Clé Fernet manquante", "CHIFFREMENT")

        # RBAC
        rbac = Path("config/security/roles_permissions.json")
        if rbac.exists():
            try:
                if not json.loads(rbac.read_text()).get("roles"):
                    deduct(15, "RBAC vide (roles non définis)", "AUTORISATION")
            except json.JSONDecodeError:
                deduct(15, "RBAC corrompu", "AUTORISATION")
        else:
            deduct(15, "Fichier RBAC absent", "AUTORISATION")

        # Zero Trust rules
        zt = Path("config/security/zero_trust_rules.json")
        if zt.exists():
            try:
                if not json.loads(zt.read_text()).get("rules"):
                    deduct(10, "Règles Zero Trust vides", "POLITIQUE")
            except json.JSONDecodeError:
                deduct(10, "Zero Trust corrompu", "POLITIQUE")
        else:
            deduct(10, "Fichier Zero Trust absent", "POLITIQUE")

        # Authentification
        if not Path("src/auth/authenticator.py").exists():
            deduct(20, "Module authentification absent", "AUTHENTIFICATION")

        # Rate limiter
        if not Path("src/security/rate_limiter.py").exists():
            deduct(10, "Rate limiter absent", "RÉSILIENCE")

        # Audit trail
        if not _AUDIT_FILE.exists() or _AUDIT_FILE.stat().st_size == 0:
            deduct(5, "Audit trail absent ou vide", "TRAÇABILITÉ")

        # Incidents critiques ouverts
        inc = self.get_incident_summary()
        if inc["open_critical"] > 0:
            deduct(15, f"{inc['open_critical']} incident(s) critique(s) ouvert(s)", "INCIDENTS")

        # Volume de menaces élevé
        threats = self.get_threat_summary()
        if threats["total_threats"] > 10:
            deduct(10, f"{threats['total_threats']} menaces en {self.lookback_hours}h", "MENACES")

        grade = "A" if score >= 90 else "B" if score >= 75 else "C" if score >= 60 else "D" if score >= 40 else "F"
        return {"score": score, "grade": grade, "max_score": 100, "deductions": deductions}

    def get_compliance_status(self) -> dict[str, Any]:
        """Vérifie la conformité GDPR / OWASP Top 10 de base."""
        checks: list[dict] = []

        def chk(name: str, ok: bool, detail: str, standard: str) -> None:
            checks.append({"name": name, "status": "OK" if ok else "KO", "detail": detail, "standard": standard})

        # GDPR
        chk("Local-first (pas de cloud)", True, "Données stockées localement", "GDPR")
        chk("Chiffrement au repos",
            Path("data/security/fernet.key").exists() or bool(os.getenv("FERNET_KEY")),
            "Clé Fernet disponible", "GDPR")
        chk("Audit trail", _AUDIT_FILE.exists(), "Journal d'audit présent", "GDPR")
        chk("Politique de rétention",
            Path("config/security/audit_retention_policy.json").exists(),
            "Fichier de politique présent", "GDPR")

        # OWASP Top 10
        chk("A01 – Contrôle d'accès",
            Path("config/security/roles_permissions.json").exists(),
            "RBAC configuré", "OWASP-A01")
        chk("A03 – Injection (validation entrée)",
            Path("src/security/input_validator.py").exists(),
            "input_validator.py présent", "OWASP-A03")
        chk("A04 – Rate limiting",
            Path("src/security/rate_limiter.py").exists(),
            "rate_limiter.py présent", "OWASP-A04")
        chk("A05 – Mauvaise configuration",
            bool(json.loads(Path("config/security/roles_permissions.json").read_text()).get("roles"))
            if Path("config/security/roles_permissions.json").exists() else False,
            "RBAC non vide", "OWASP-A05")
        chk("A07 – Identification/Authentification",
            Path("src/auth/authenticator.py").exists(),
            "authenticator.py présent", "OWASP-A07")
        chk("A09 – Logging et monitoring",
            _SECURITY_LOG.exists(),
            "security.log présent", "OWASP-A09")

        passed = sum(1 for c in checks if c["status"] == "OK")
        return {
            "total": len(checks),
            "passed": passed,
            "failed": len(checks) - passed,
            "compliance_rate": round(passed / len(checks) * 100, 1),
            "checks": checks,
        }

    def generate_report(self) -> str:
        """Génère un rapport texte complet de la posture de sécurité."""
        now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
        score_data = self.get_security_score()
        audit = self.get_audit_summary()
        threats = self.get_threat_summary()
        incidents = self.get_incident_summary()
        compliance = self.get_compliance_status()
        devices = self.get_device_summary()

        lines = [
            "=" * 62,
            f"  RAPPORT SECURITE ALFRED — {now}",
            "=" * 62,
            "",
            f"  SCORE GLOBAL : {score_data['score']}/100  (grade {score_data['grade']})",
            "",
            "── Audit trail (dernières 24h) " + "─" * 31,
            f"  Evenements : {audit['total_events']}",
            f"  Refus      : {audit['total_denials']}  ({audit['denial_rate']}%)",
            f"  Top actions: {list(audit['top_actions'].keys())[:3]}",
            "",
            "── Menaces " + "─" * 51,
            f"  Detectees  : {threats['total_threats']}",
            f"  Top sources: {list(threats['threats_by_user'].keys())[:3]}",
            "",
            "── Incidents " + "─" * 49,
            f"  Total      : {incidents['total_incidents']}",
            f"  Critiques  : {incidents['open_critical']} ouverts",
            f"  Par niveau : {incidents['by_level']}",
            "",
            "── Appareils " + "─" * 49,
            f"  Total      : {devices['total_devices']}",
            f"  Approuves  : {devices['trusted']}  |  Revoques : {devices['revoked']}",
            "",
            f"── Conformite ({compliance['passed']}/{compliance['total']} — {compliance['compliance_rate']}%) " + "─" * 18,
        ]
        for c in compliance["checks"]:
            icon = "+" if c["status"] == "OK" else "-"
            lines.append(f"  [{icon}] {c['standard']:12} {c['name']}")

        if score_data["deductions"]:
            lines += ["", "── Points de deduction " + "─" * 39]
            for d in score_data["deductions"]:
                lines.append(f"  [{d['points']:+3d}] {d['category']:20} {d['reason']}")

        lines += ["", "=" * 62]
        return "\n".join(lines)


def get_dashboard(lookback_hours: int = 24) -> SecurityDashboard:
    """Factory : retourne un dashboard initialisé."""
    return SecurityDashboard(lookback_hours)


if __name__ == "__main__":
    dashboard = get_dashboard()
    print(dashboard.generate_report())
