"""
════════════════════════════════════════════════════════════
PROJECT      : ALFRED
BLOCK        : B10 (ALFRED CPL)
FUNCTION     : 10.08
FILE         : src/assistant_actions/deliverable_templates.py
ROLE         : Gabarits de livrables métier (fiche de cadrage, registre de risques)

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-07-11
VERSION      : V1.0
STATUS       : ACTIVE

DESCRIPTION :
Assemble un brouillon de livrable métier à partir des connaissances
réellement retrouvées par le Knowledge Retrieval Engine (B18), plutôt que
de générer du texte librement. Chaque section cite sa source quand elle
provient d'une connaissance sourcée (src/knowledge/context_merger.py).
Les champs qui exigent un jugement humain (probabilité, impact, décision)
sont explicitement laissés "à compléter" plutôt qu'inventés — cohérent
avec le principe "réponses sourcées, jamais hallucinées" (chantier 4).
════════════════════════════════════════════════════════════
"""
from __future__ import annotations

from typing import Any

TEMPLATE_TYPES = {
    "fiche_cadrage": "Fiche de cadrage projet",
    "registre_risques": "Registre initial des risques",
}


def _knowledge_field(ranked_knowledge: list, field: str) -> list[tuple[str, Any]]:
    """Retourne [(knowledge_id, valeur_du_champ), ...] pour chaque connaissance
    retrouvée qui porte ce champ dans sa section "knowledge"."""
    results: list[tuple[str, Any]] = []
    for item in ranked_knowledge:
        raw = item.data.get("data", {}) if item.data else {}
        knowledge_section = raw.get("knowledge", {})
        if isinstance(knowledge_section, dict) and field in knowledge_section:
            results.append((item.knowledge_id, knowledge_section[field]))
    return results


def _citation_line(citations: list[dict[str, Any]]) -> str:
    if not citations:
        return "_Aucune source documentaire spécifique identifiée — à valider manuellement._"
    lines = [
        f"- {c.get('reference')}, version {c.get('version')}, validée le {c.get('validated_date')}"
        f" (propriétaire : {c.get('owner') or 'non renseigné'})"
        for c in citations
    ]
    return "\n".join(lines)


def render_fiche_cadrage(
    topic: str,
    ranked_knowledge: list,
    citations: list[dict[str, Any]],
) -> dict[str, Any]:
    """
    Construit une fiche de cadrage projet brouillon à partir des connaissances
    retrouvées (procédure interne, gestion de projet, risques, sécurité).
    """
    cadrage_requirements = _knowledge_field(ranked_knowledge, "cadrage_requirements")
    process_steps = _knowledge_field(ranked_knowledge, "process_steps")
    risk_categories = _knowledge_field(ranked_knowledge, "risk_categories")

    required_sections = cadrage_requirements[0][1] if cadrage_requirements else [
        "Objectifs et bénéfices attendus",
        "Parties prenantes et responsabilités",
        "Registre initial des risques",
        "Exigences de sécurité et de conformité applicables",
        "Indicateurs de suivi",
    ]

    sections: list[str] = [
        f"# Fiche de cadrage (BROUILLON) — {topic}",
        "",
        "> Statut : **BROUILLON** — généré automatiquement à partir de la base de connaissances,"
        " ne doit pas être utilisé sans validation humaine.",
        "",
        "## Objectif du projet",
        "_À compléter par le porteur du projet : quel problème métier ce projet résout-il,"
        " pour quel bénéfice observable ?_",
        "",
        "## Sections de cadrage attendues (d'après la procédure interne)",
    ]
    sections.extend(f"- {s}" for s in required_sections)

    if process_steps:
        # Ne garder que la première liste d'étapes (connaissance la mieux classée) —
        # concaténer les process_steps de plusieurs procédures différentes créerait
        # une liste numérotée trompeuse (plusieurs "1." qui ne s'enchaînent pas).
        _, first_steps = process_steps[0]
        if isinstance(first_steps, list):
            sections.append("")
            sections.append("## Étapes du processus de lancement")
            sections.extend(f"{i + 1}. {step}" for i, step in enumerate(first_steps))

    sections.append("")
    sections.append("## Registre initial des risques (catégories à évaluer)")
    if risk_categories:
        for _, categories in risk_categories:
            if isinstance(categories, list):
                sections.extend(
                    f"- {cat} — probabilité : _à évaluer_ · impact : _à évaluer_"
                    for cat in categories
                )
    else:
        sections.append("_Aucune catégorie de risque type identifiée dans la base — à définir manuellement._")

    sections.extend([
        "",
        "## Parties prenantes (RACI)",
        "_À compléter : qui est Responsible / Accountable / Consulted / Informed sur ce projet ?_",
        "",
        "## Indicateurs de suivi",
        "_À compléter : comment mesurera-t-on le succès de ce projet ?_",
        "",
        "## Sources documentaires utilisées",
        _citation_line(citations),
        "",
        "---",
        "**Ce document reste un brouillon tant qu'il n'a pas été approuvé par un humain habilité"
        " (workflow de validation ALFRED CPL).**",
    ])

    return {
        "deliverable_type": "fiche_cadrage",
        "title": f"Fiche de cadrage — {topic}",
        "status": "draft",
        "content_markdown": "\n".join(sections),
        "citations": citations,
        "knowledge_ids_used": [item.knowledge_id for item in ranked_knowledge],
    }


def render_registre_risques(
    topic: str,
    ranked_knowledge: list,
    citations: list[dict[str, Any]],
) -> dict[str, Any]:
    """
    Construit un registre de risques initial brouillon, structuré à partir des
    catégories de risques et stratégies de réponse connues de la base.
    """
    risk_categories = _knowledge_field(ranked_knowledge, "risk_categories")
    response_strategies = _knowledge_field(ranked_knowledge, "response_strategies")

    sections: list[str] = [
        f"# Registre initial des risques (BROUILLON) — {topic}",
        "",
        "> Statut : **BROUILLON** — les catégories ci-dessous sont issues de la base de"
        " connaissances ; la probabilité, l'impact et le plan de réponse restent à évaluer"
        " et valider par un humain.",
        "",
        "## Risques identifiés",
        "",
        "| Catégorie | Probabilité (1-5) | Impact (1-5) | Score | Stratégie de réponse |",
        "|---|---|---|---|---|",
    ]

    categories_flat: list[str] = []
    for _, categories in risk_categories:
        if isinstance(categories, list):
            categories_flat.extend(categories)

    if categories_flat:
        sections.extend(
            f"| {cat} | _à évaluer_ | _à évaluer_ | _à calculer_ | _à choisir_ |"
            for cat in categories_flat
        )
    else:
        sections.append("| _Aucune catégorie type identifiée — à compléter manuellement_ | | | | |")

    if response_strategies:
        sections.append("")
        sections.append("## Stratégies de réponse disponibles (référentiel)")
        for _, strategies in response_strategies:
            if isinstance(strategies, list):
                for s in strategies:
                    if isinstance(s, dict):
                        sections.append(f"- **{s.get('strategy')}** — {s.get('logic')}")

    sections.extend([
        "",
        "## Sources documentaires utilisées",
        _citation_line(citations),
        "",
        "---",
        "**Ce document reste un brouillon tant qu'il n'a pas été approuvé par un humain habilité"
        " (workflow de validation ALFRED CPL).**",
    ])

    return {
        "deliverable_type": "registre_risques",
        "title": f"Registre initial des risques — {topic}",
        "status": "draft",
        "content_markdown": "\n".join(sections),
        "citations": citations,
        "knowledge_ids_used": [item.knowledge_id for item in ranked_knowledge],
    }


_RENDERERS = {
    "fiche_cadrage": render_fiche_cadrage,
    "registre_risques": render_registre_risques,
}


def render_deliverable(
    deliverable_type: str,
    topic: str,
    ranked_knowledge: list,
    citations: list[dict[str, Any]],
) -> dict[str, Any]:
    """Point d'entrée générique : dispatch vers le bon gabarit."""
    renderer = _RENDERERS.get(deliverable_type)
    if renderer is None:
        raise ValueError(
            f"Type de livrable inconnu : {deliverable_type!r} "
            f"(types disponibles : {', '.join(TEMPLATE_TYPES)})"
        )
    return renderer(topic=topic, ranked_knowledge=ranked_knowledge, citations=citations)
