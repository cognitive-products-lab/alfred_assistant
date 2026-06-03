"""
════════════════════════════════════════════════════════════
PROJECT      : ALFRED
BLOCK        : B22
FUNCTION     : 22.15
FILE         : src/accessibility/wcag_checker.py
ROLE         : Vérification conformité WCAG 2.1 AA et audit accessibilité

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-05-23
UPDATED      : 2026-05-23
VERSION      : V1.0
STATUS       : ACTIVE

DEPENDENCIES :
- dataclasses
- typing

DESCRIPTION :
Vérifie la conformité WCAG 2.1 AA d'une interface ou d'un texte,
génère un rapport d'audit d'accessibilité et identifie les critères
non respectés avec recommandations.
════════════════════════════════════════════════════════════
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .web_a11y import check_contrast, check_dashboard_contrasts


@dataclass
class WcagIssue:
    criterion: str
    level: str          # A, AA, AAA
    description: str
    recommendation: str
    passed: bool = False


def check_wcag(component_data: dict[str, Any]) -> list[WcagIssue]:
    """
    Vérifie les critères WCAG 2.1 applicables sur `component_data`.
    `component_data` peut contenir : fg, bg, has_alt_text, has_label,
    has_keyboard_nav, has_focus_visible, lang, has_skip_link.
    Retourne la liste des vérifications (passées et échouées).
    """
    issues: list[WcagIssue] = []

    # 1.4.3 — Contraste minimum (AA)
    if "fg" in component_data and "bg" in component_data:
        result = check_contrast(component_data["fg"], component_data["bg"])
        issues.append(WcagIssue(
            criterion="1.4.3",
            level="AA",
            description=f"Contraste texte/fond : {result['ratio']}:1",
            recommendation="Ratio minimum requis : 4.5:1 pour le texte normal.",
            passed=result["passe_AA"],
        ))

    # 1.1.1 — Texte alternatif pour les images
    if "has_alt_text" in component_data:
        issues.append(WcagIssue(
            criterion="1.1.1",
            level="A",
            description="Présence de texte alternatif sur les images.",
            recommendation="Ajouter un attribut alt descriptif à chaque image informative.",
            passed=component_data["has_alt_text"],
        ))

    # 4.1.2 — Nom, rôle, valeur pour les composants interactifs
    if "has_label" in component_data:
        issues.append(WcagIssue(
            criterion="4.1.2",
            level="A",
            description="Présence d'un label ARIA ou natif sur les contrôles.",
            recommendation="Ajouter aria-label ou <label> associé à chaque champ/bouton.",
            passed=component_data["has_label"],
        ))

    # 2.1.1 — Navigation clavier
    if "has_keyboard_nav" in component_data:
        issues.append(WcagIssue(
            criterion="2.1.1",
            level="A",
            description="Tous les éléments interactifs sont accessibles au clavier.",
            recommendation="Assurer tabindex et gestionnaires keyboard sur tous les contrôles.",
            passed=component_data["has_keyboard_nav"],
        ))

    # 2.4.7 — Focus visible
    if "has_focus_visible" in component_data:
        issues.append(WcagIssue(
            criterion="2.4.7",
            level="AA",
            description="Indicateur de focus visible sur les éléments interactifs.",
            recommendation="Ne pas supprimer outline:none sans le remplacer par un style de focus visible.",
            passed=component_data["has_focus_visible"],
        ))

    # 3.1.1 — Langue de la page
    if "lang" in component_data:
        issues.append(WcagIssue(
            criterion="3.1.1",
            level="A",
            description=f"Langue déclarée : {component_data['lang']}",
            recommendation="Définir l'attribut lang sur la balise <html>.",
            passed=bool(component_data["lang"]),
        ))

    return issues


def wcag_report(component_data: dict[str, Any]) -> dict[str, Any]:
    """
    Génère un rapport WCAG complet avec score et liste des problèmes.
    """
    issues = check_wcag(component_data)
    passed = [i for i in issues if i.passed]
    failed = [i for i in issues if not i.passed]

    score = round(len(passed) / len(issues) * 100) if issues else 100

    return {
        "score": score,
        "total_checks": len(issues),
        "passed": len(passed),
        "failed": len(failed),
        "conformance_level": "AA" if score >= 80 else ("A" if score >= 50 else "Non conforme"),
        "issues": [
            {
                "criterion": i.criterion,
                "level": i.level,
                "description": i.description,
                "recommendation": i.recommendation,
                "status": "OK" if i.passed else "FAIL",
            }
            for i in issues
        ],
    }


def audit_dashboard() -> dict[str, Any]:
    """Audit rapide des contrastes du dashboard ALFRED."""
    contrasts = check_dashboard_contrasts()
    failed = {name: data for name, data in contrasts.items() if not data["passe_AA"]}
    return {
        "total_colors": len(contrasts),
        "passing_AA": len(contrasts) - len(failed),
        "failing_AA": len(failed),
        "details": contrasts,
        "recommendations": [
            f"Couleur {name} : ratio {data['ratio']}:1 — insuffisant (min 4.5:1)"
            for name, data in failed.items()
        ],
    }
