# ============================================================
# ALFRED — src/accessibility/translation/translator.py
# Bloc 22.03 — Traduction multilingue
#
# 📚 NOTION EXAM :
#   D41-3 — Capsule 3 : Accessibilité, inclusion et adaptation cognitive
#
# 🎯 UTILITÉ ALFRED :
#   Traduction de texte entre langues (FR ↔ EN prioritaire, extensible).
#   Reformulation simplifiée. Prépare la sortie pour lecture vocale ou
#   affichage utilisateur.
#
# 🔐 BLOC SÉCURITÉ / DOMAINE :
#   Accessibilité & assistance cognitive (22.03)
# ============================================================

from __future__ import annotations

_SUPPORTED_PAIRS = {("fr", "en"), ("en", "fr")}


def is_translation_supported(source: str, target: str) -> bool:
    return (source, target) in _SUPPORTED_PAIRS


def translate(text: str, source_lang: str, target_lang: str, engine_fn: callable) -> str:
    if not text.strip():
        return text
    if not is_translation_supported(source_lang, target_lang):
        raise ValueError(f"Paire de langues non supportée : {source_lang} → {target_lang}")
    return engine_fn(text, source=source_lang, target=target_lang)


def simplify(text: str, simplify_fn: callable) -> str:
    if not text.strip():
        return text
    return simplify_fn(text)
