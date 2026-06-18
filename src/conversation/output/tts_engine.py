# ============================================================
# ALFRED — src/conversation/output/tts_engine.py
# Bloc 04.02 — Synthèse vocale (TTS)
#
# 📚 NOTION EXAM :
#   D13-2 — Capsule 4 : Façade haut niveau de synthèse vocale
#
# 🎯 UTILITÉ ALFRED :
#   Interface stable TTSEngine.speak(text) — délègue la génération
#   vocale à tts_piper.py sans exposer les détails techniques.
#
# 🏗️ DOMAINE :
#   Interaction vocale — façade TTS découplée du moteur Piper
# ============================================================

from typing import Optional


class TTSEngine:
    """
    Interface haut niveau de synthèse vocale.

    Le moteur technique réel peut être :
    - Piper local
    - fallback texte
    - futur moteur TTS avancé
    """

    def __init__(self, backend: Optional[object] = None) -> None:
        """
        Initialise le moteur TTS.

        Args:
            backend: moteur technique optionnel.
                     Exemple attendu : instance issue de tts_piper.py
        """
        self.backend = backend

    def speak(self, text: str) -> bool:
        """
        Fait parler ALFRED à partir d'un texte.

        Args:
            text: Texte à vocaliser.

        Returns:
            bool: True si la sortie vocale ou fallback a fonctionné, False sinon.
        """
        if not text or not text.strip():
            return False

        try:
            if self.backend is not None:
                return bool(self.backend.speak(text.strip()))

            return self._fallback_print(text.strip())

        except Exception as error:
            print(f"❌ Erreur TTSEngine.speak() : {error}")
            return self._fallback_print(text.strip())

    def _fallback_print(self, text: str) -> bool:
        """
        Fallback texte si aucun moteur vocal n'est disponible.

        Cela évite qu'ALFRED devienne muet comme un majordome en panne de piles.
        """
        print(f"🗣️ ALFRED : {text}")
        return True