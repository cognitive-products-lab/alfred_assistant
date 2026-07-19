"""
════════════════════════════════════════════════════════════
PROJECT      : ALFRED
BLOCK        : B22
FUNCTION     : 22.14
FILE         : web_a11y.py
ROLE         : Accessibilité Web & Dashboard — ARIA, contraste, helpers Jinja2

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-05-22
UPDATED      : 2026-05-22
VERSION      : V1.0
STATUS       : VALIDATED

DEPENDENCIES :
- typing

SECURITY :
- Local-first
- Security by Design

DESCRIPTION :
Helpers d'accessibilité web pour ALFRED_WEB (Flask/Jinja2) et le dashboard dynamique.
- Générateur d'attributs ARIA (role, label, live region)
- Calcul de contraste WCAG 2.1 (ratio, AA, AAA)
- Audit des couleurs du dashboard ALFRED
- Helpers injectables dans les templates Jinja2
════════════════════════════════════════════════════════════
"""

from __future__ import annotations

from typing import Any


class WebA11y:
    """
    22.14 Accessibilité Web & Dashboard.

    Génère les attributs ARIA et vérifie les contrastes pour le dashboard.
    """

    # Couleurs du dashboard ALFRED (CSS variables → valeurs réelles)
    DASHBOARD_COLORS: dict[str, tuple[str, str]] = {
        "--acc":  ("#00d4ff", "#07090f"),
        "--ok":   ("#00e096", "#07090f"),
        "--par":  ("#ffaa00", "#07090f"),
        "--gui":  ("#a78bfa", "#07090f"),
        "--todo": ("#ff4d6d", "#07090f"),
        "--txt":  ("#b8c4d8", "#07090f"),
        "--wh":   ("#f0f4ff", "#07090f"),
    }

    # ── ARIA ────────────────────────────────────────────

    def aria_attrs(self, role: str, label: str, **kwargs: Any) -> dict[str, str]:
        """
        Génère un dictionnaire d'attributs ARIA pour un composant HTML.

        Args:
            role  : Rôle ARIA ('button', 'alert', 'status', 'navigation', ...)
            label : Valeur aria-label
            **kwargs : expanded, live, atomic, hidden, describedby, controls

        Returns:
            dict {attr: value} prêt à passer à Jinja2 avec **attrs
        """
        attrs: dict[str, str] = {"role": role, "aria-label": label}
        _bool_attrs = {"expanded": "aria-expanded", "atomic": "aria-atomic", "hidden": "aria-hidden"}
        for key, aria_key in _bool_attrs.items():
            if key in kwargs:
                attrs[aria_key] = "true" if kwargs[key] else "false"
        if "live" in kwargs:
            attrs["aria-live"] = kwargs["live"]          # "polite" | "assertive" | "off"
        if "describedby" in kwargs:
            attrs["aria-describedby"] = kwargs["describedby"]
        if "controls" in kwargs:
            attrs["aria-controls"] = kwargs["controls"]
        return attrs

    def attrs_to_html(self, attrs: dict[str, str]) -> str:
        """Convertit un dict d'attributs en chaîne HTML inline."""
        return " ".join(f'{k}="{v}"' for k, v in attrs.items())

    # ── Contraste ──────────────────────────────────────

    @staticmethod
    def relative_luminance(hex_color: str) -> float:
        """Luminance relative WCAG 2.1."""
        hex_color = hex_color.lstrip("#")
        if len(hex_color) == 3:
            hex_color = "".join(c * 2 for c in hex_color)
        r, g, b = (int(hex_color[i:i+2], 16) / 255.0 for i in (0, 2, 4))

        def lin(c: float) -> float:
            return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

        return 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b)

    def contrast_ratio(self, fg: str, bg: str) -> float:
        """Ratio de contraste entre deux couleurs hex."""
        l1 = self.relative_luminance(fg)
        l2 = self.relative_luminance(bg)
        lighter, darker = max(l1, l2), min(l1, l2)
        return round((lighter + 0.05) / (darker + 0.05), 2)

    def check_contrast(self, fg: str, bg: str) -> dict[str, Any]:
        """Retourne le ratio et les niveaux WCAG (AA, AA_large, AAA)."""
        ratio = self.contrast_ratio(fg, bg)
        return {
            "ratio": ratio,
            "passe_AA": ratio >= 4.5,
            "passe_AA_large": ratio >= 3.0,
            "passe_AAA": ratio >= 7.0,
            "fg": fg, "bg": bg,
        }

    def audit_dashboard(self) -> dict[str, Any]:
        """Audit des contrastes de toutes les couleurs du dashboard ALFRED."""
        results = {
            name: self.check_contrast(fg, bg)
            for name, (fg, bg) in self.DASHBOARD_COLORS.items()
        }
        failing = {k: v for k, v in results.items() if not v["passe_AA"]}
        return {
            "total": len(results),
            "passing_AA": len(results) - len(failing),
            "failing_AA": len(failing),
            "details": results,
            "recommendations": [
                f"{name} : ratio {data['ratio']}:1 — insuffisant (min 4.5:1)"
                for name, data in failing.items()
            ],
        }

    def status(self) -> dict:
        return {"dashboard_colors_tracked": len(self.DASHBOARD_COLORS)}


# ─────────────────────────────────────────────────────────
# Test standalone
# ─────────────────────────────────────────────────────────
if __name__ == "__main__":
    wa = WebA11y()
    audit = wa.audit_dashboard()
    print(f"Couleurs auditées : {audit['total']}")
    print(f"Passent AA        : {audit['passing_AA']}")
    print(f"Échouent AA       : {audit['failing_AA']}")
    if audit["recommendations"]:
        for rec in audit["recommendations"]:
            print(f"  ⚠ {rec}")
    print("WebA11y skeleton OK.")
