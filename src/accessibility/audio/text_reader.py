# ============================================================
# ALFRED — src/accessibility/audio/text_reader.py
# Bloc 22.02 — Lecture vocale & restitution audio
#
# 📚 NOTION EXAM :
#   D41-3 — Capsule 3 : Accessibilité, inclusion et adaptation cognitive
#
# 🎯 UTILITÉ ALFRED :
#   Lecture à voix haute d'un texte, d'un document ou d'une page web.
#   Transmet le texte préparé au voice_output_manager pour synthèse
#   via la voix officielle d'ALFRED (Piper TTS).
#
# 🔐 BLOC SÉCURITÉ / DOMAINE :
#   Accessibilité & assistance cognitive (22.02)
# ============================================================

from __future__ import annotations


def prepare_text_for_reading(text: str, max_chars: int = 5000) -> str:
    text = text.strip()
    if len(text) > max_chars:
        text = text[:max_chars] + "…"
    return text


def split_into_chunks(text: str, chunk_size: int = 500) -> list[str]:
    words = text.split()
    chunks = []
    current: list[str] = []
    length = 0
    for word in words:
        length += len(word) + 1
        current.append(word)
        if length >= chunk_size:
            chunks.append(" ".join(current))
            current = []
            length = 0
    if current:
        chunks.append(" ".join(current))
    return chunks


def read_text(text: str, output_fn: callable) -> None:
    prepared = prepare_text_for_reading(text)
    for chunk in split_into_chunks(prepared):
        output_fn(chunk)
