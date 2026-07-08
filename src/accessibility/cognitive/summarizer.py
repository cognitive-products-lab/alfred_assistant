# ============================================================
# ALFRED — src/accessibility/cognitive/summarizer.py
# Bloc 22.04 — Reformulation simplifiée / Bloc 22.09 — Résumés intelligents
#
# 📚 NOTION EXAM :
#   D41-3 — Capsule 3 : Accessibilité, inclusion et adaptation cognitive
#
# 🎯 UTILITÉ ALFRED :
#   Génère des résumés courts et des reformulations simplifiées pour
#   réduire la charge cognitive de l'utilisateur face à un contenu dense.
#
# 🔐 BLOC SÉCURITÉ / DOMAINE :
#   Accessibilité & assistance cognitive (22.04 / 22.09)
#
# STATUS  : TESTED
# ============================================================

from __future__ import annotations


def summarize(text: str, max_sentences: int = 3, summarize_fn: callable = None) -> str:
    if not text.strip():
        return text
    if summarize_fn:
        return summarize_fn(text, max_sentences=max_sentences)
    sentences = [s.strip() for s in text.split(".") if s.strip()]
    return ". ".join(sentences[:max_sentences]) + ("." if sentences else "")


def simplify_for_reading(text: str, simplify_fn: callable) -> str:
    if not text.strip():
        return text
    return simplify_fn(text)


def summarize_for_voice(text: str, max_sentences: int = 3, summarize_fn: callable = None) -> str:
    summary = summarize(text, max_sentences=max_sentences, summarize_fn=summarize_fn)
    return summary.replace("\n", " ").strip()
