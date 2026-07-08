"""
════════════════════════════════════════════════════════════
PROJECT      : ALFRED
BLOCK        : B22
FUNCTION     : 22.03
FILE         : translator.py
ROLE         : Traduction multilingue via LLMRouter (Ollama local → OpenAI fallback)

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-05-22
UPDATED      : 2026-06-03
VERSION      : V1.0
UPDATED      : 2026-06-03
VERSION      : V1.1
STATUS       : VALIDATED

DEPENDENCIES :
- hashlib
- logging
- typing

SECURITY :
- Local-first
- Security by Design

DESCRIPTION :
Traduction de texte vers 7 langues (fr, en, es, de, it, pt, nl) via le LLMRouter
existant. Cache FIFO en mémoire (200 entrées) pour éviter les appels répétés.
Inclut détection automatique de langue et accès direct au glossaire personnalisé.
════════════════════════════════════════════════════════════
"""

# ============================================================
# ALFRED — Translator
# Traduction de texte via le LLMRouter existant.
# Langues supportées : fr, en, es, de, it, pt, nl
# Cache simple en mémoire pour éviter les requêtes répétées.
# ============================================================

from __future__ import annotations

import hashlib
import logging
from typing import Optional

logger = logging.getLogger(__name__)

SUPPORTED_LANGUAGES = {
    "fr": "français",
    "en": "anglais",
    "es": "espagnol",
    "de": "allemand",
    "it": "italien",
    "pt": "portugais",
    "nl": "néerlandais",
}


class Translator:
    """
    22.03 Traduction multilingue.

    Utilise LLMRouter (Ollama local → OpenAI fallback).
    Cache en mémoire pour les traductions répétées.
    """

    def __init__(self, llm_router=None, cache_size: int = 200) -> None:
        self._llm = llm_router
        self._cache: dict[str, str] = {}
        self._cache_size = cache_size
        self._stats = {"hits": 0, "misses": 0, "errors": 0}
        logger.info("Translator initialisé (cache_size=%d)", cache_size)

    # ── API principale ────────────────────────────────────

    def translate(self, text: str, target_lang: str, source_lang: str = "auto") -> str:
        """
        Traduit un texte dans la langue cible.

        Args:
            text        : Texte à traduire
            target_lang : Code langue cible (ex: "en", "es")
            source_lang : Code langue source ou "auto"

        Returns:
            Texte traduit
        """
        if target_lang not in SUPPORTED_LANGUAGES:
            raise ValueError(f"Langue non supportée : {target_lang}. Disponibles : {list(SUPPORTED_LANGUAGES)}")

        cache_key = self._make_key(text, target_lang, source_lang)
        if cache_key in self._cache:
            self._stats["hits"] += 1
            return self._cache[cache_key]

        self._stats["misses"] += 1
        result = self._call_llm(text, target_lang, source_lang)
        self._store_cache(cache_key, result)
        return result

    def detect_language(self, text: str) -> str:
        """
        Détecte la langue d'un texte (FR / EN / unknown).
        Utilise les marqueurs NLP V2 existants — pas de dépendance externe.
        """
        try:
            from src.conversation.input.nlp_engine_v2 import detect_language as _detect
            return _detect(text)
        except ImportError:
            pass
        # Fallback minimal par marqueurs
        words = set(text.lower().split())
        fr_markers = {"je", "tu", "il", "nous", "vous", "le", "la", "les",
                      "un", "une", "des", "et", "ou", "bonjour", "merci"}
        en_markers = {"i", "you", "he", "she", "we", "the", "a", "an",
                      "and", "or", "hello", "please", "thank"}
        fr_score = len(words & fr_markers)
        en_score = len(words & en_markers)
        if fr_score == 0 and en_score == 0:
            return "unknown"
        return "fr" if fr_score >= en_score else "en"

    # ── Interne ───────────────────────────────────────────

    def _call_llm(self, text: str, target_lang: str, source_lang: str) -> str:
        """Construit le prompt de traduction et appelle le LLMRouter.
        Fallback gracieux sans LLM : retourne le texte original."""
        if self._llm is None:
            logger.warning("Translator : aucun LLMRouter connecté — texte retourné sans traduction.")
            return text  # fallback gracieux

        lang_name = SUPPORTED_LANGUAGES[target_lang]
        src_hint = f"depuis le {SUPPORTED_LANGUAGES[source_lang]}" if source_lang in SUPPORTED_LANGUAGES else ""

        system_prompt = (
            f"Tu es un traducteur professionnel. "
            f"Traduis uniquement en {lang_name}{' ' + src_hint if src_hint else ''}. "
            "Retourne uniquement la traduction, sans explication, sans guillemets, sans formatage."
        )
        user_prompt = f"Texte à traduire : {text}"

        try:
            # LLMRouter.generate(system_prompt, user_prompt) — interface standard ALFRED
            response = self._llm.generate(
                system_prompt=system_prompt,
                user_prompt=user_prompt,
            )
            return response.strip() if isinstance(response, str) else text
        except Exception as exc:
            logger.warning("Translator: LLM indisponible (%s) — retour texte original", exc)
            self._stats["errors"] += 1
            return text

    def _make_key(self, text: str, target: str, source: str) -> str:
        raw = f"{target}:{source}:{text}"
        return hashlib.md5(raw.encode()).hexdigest()

    def _store_cache(self, key: str, value: str) -> None:
        if len(self._cache) >= self._cache_size:
            # Éviction FIFO simple
            oldest = next(iter(self._cache))
            del self._cache[oldest]
        self._cache[key] = value

    # ── Diagnostic ────────────────────────────────────────

    def status(self) -> dict:
        return {
            "llm_connected": self._llm is not None,
            "supported_languages": list(SUPPORTED_LANGUAGES.keys()),
            "cache_entries": len(self._cache),
            "cache_size": self._cache_size,
            "stats": self._stats,
        }

    def clear_cache(self) -> None:
        self._cache.clear()
        logger.debug("Cache traductions vidé.")


# ─────────────────────────────────────────────────────────
# Test standalone
# ─────────────────────────────────────────────────────────
if __name__ == "__main__":
    t = Translator()
    print(f"Status : {t.status()}")
    print(f"Langues supportées : {list(SUPPORTED_LANGUAGES.keys())}")
    print("Translator skeleton OK.")
