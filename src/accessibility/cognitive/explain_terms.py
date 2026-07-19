# ============================================================
# ALFRED — src/accessibility/cognitive/explain_terms.py
# Bloc 22.05 — Assistance cognitive / Bloc 22.10 — Explication des termes techniques
#
# 📚 NOTION EXAM :
#   D41-3 — Capsule 3 : Accessibilité, inclusion et adaptation cognitive
#
# 🎯 UTILITÉ ALFRED :
#   Détecte et explique les termes techniques, acronymes et jargon dans
#   un texte afin de le rendre compréhensible pour tous les utilisateurs,
#   y compris les profils neuroatypiques ou en surcharge cognitive.
#
# 🔐 BLOC SÉCURITÉ / DOMAINE :
#   Accessibilité & assistance cognitive (22.05 / 22.10)
#
# STATUS  : VALIDATED
# ============================================================

from __future__ import annotations

_KNOWN_ACRONYMS: dict[str, str] = {
    "IA": "Intelligence Artificielle",
    "TTS": "Text-To-Speech (synthèse vocale)",
    "STT": "Speech-To-Text (reconnaissance vocale)",
    "RGPD": "Règlement Général sur la Protection des Données",
    "API": "Interface de Programmation d'Application",
    "MFA": "Authentification Multi-Facteurs",
    "RBAC": "Contrôle d'Accès Basé sur les Rôles",
    "RAG": "Retrieval-Augmented Generation",
    "WCAG": "Web Content Accessibility Guidelines",
}


def explain_term(term: str, knowledge_fn: callable | None = None) -> str | None:
    upper = term.upper()
    if upper in _KNOWN_ACRONYMS:
        return _KNOWN_ACRONYMS[upper]
    if knowledge_fn:
        return knowledge_fn(term)
    return None


def annotate_text(text: str, knowledge_fn: callable | None = None) -> dict:
    words = text.split()
    annotations: dict[str, str] = {}
    for word in words:
        clean = word.strip(".,;:!?()")
        explanation = explain_term(clean, knowledge_fn)
        if explanation:
            annotations[clean] = explanation
    return {"original": text, "annotations": annotations}


def list_known_acronyms() -> dict[str, str]:
    return dict(_KNOWN_ACRONYMS)
