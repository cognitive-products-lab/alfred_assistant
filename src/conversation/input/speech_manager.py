# ============================================================
# ALFRED — src/input/speech_manager.py
# Bloc 01 V3 — Orchestrateur vocal complet
#
# Coordonne :
#   STT → stt_whisper.py   (écoute + transcription)
#   TTS → tts_piper.py     (synthèse + lecture)
#   NLP → nlp_engine_v2.py (intent + émotion)
#   CTX → context_builder  (contexte temps / énergie)
#
# C'est la pièce centrale du moteur vocal V3.
# main.py instancie SpeechManager et l'utilise comme interface unique.
# ============================================================

from src.input.audio_capture  import is_audio_available
from src.output.tts_output    import display_response, display_system


class SpeechManager:
    """
    Gestionnaire vocal unifié ALFRED.

    Gère automatiquement le mode d'interaction :
      - V1 : texte terminal uniquement
      - V2 : texte + NLP enrichi
      - V3 : vocal complet (STT Whisper + TTS Piper)

    Usage :
        manager = SpeechManager()
        text = manager.listen()          # Écoute (vocal ou texte)
        manager.speak("Bonjour.", ctx)   # Parle (vocal ou terminal)
    """

    def __init__(self, user_name: str = "Céline"):
        self.user_name  = user_name
        self._stt_ready = False
        self._tts_ready = False
        self._mode      = "text"   # "text" | "voice"
        self._init_engines()

    def _init_engines(self) -> None:
        """Initialise STT et TTS si disponibles."""

        # ── STT ───────────────────────────────────────
        try:
            from src.input.stt_whisper import is_stt_available
            self._stt_ready = is_stt_available()
        except ImportError:
            self._stt_ready = False

        # ── TTS ───────────────────────────────────────
        try:
            from src.output.tts_piper import is_tts_available
            self._tts_ready = is_tts_available()
        except ImportError:
            self._tts_ready = False

        # ── Mode global ───────────────────────────────
        if self._stt_ready and self._tts_ready:
            self._mode = "voice"
            display_system("Mode vocal activé — STT Whisper + TTS Piper Pierre ✅")
        elif self._tts_ready:
            self._mode = "tts_only"
            display_system("Mode TTS uniquement — saisie texte + voix Pierre")
        else:
            self._mode = "text"
            display_system("Mode terminal — saisie et affichage texte")

    # ─────────────────────────────────────────────────
    # ÉCOUTE
    # ─────────────────────────────────────────────────

    def listen(
        self,
        prompt: str = "Vous : ",
        duration: float = 6.0,
        language: str = "fr",
    ) -> str:
        """
        Écoute l'utilisateur — vocal si V3, texte sinon.

        Args:
            prompt   : Invite saisie (mode texte)
            duration : Durée max enregistrement (mode vocal)
            language : Langue cible pour Whisper

        Returns:
            Texte saisi ou transcrit
        """
        if self._mode == "voice" and self._stt_ready:
            return self._listen_voice(duration, language)
        return self._listen_text(prompt)

    def _listen_text(self, prompt: str) -> str:
        """Saisie clavier terminal (V1/V2)."""
        from src.input.text_input import read_user_input
        return read_user_input(prompt)

    def _listen_voice(self, duration: float, language: str) -> str:
        """Écoute micro + transcription Whisper (V3)."""
        from src.input.stt_whisper import listen_and_transcribe
        text = listen_and_transcribe(duration=duration, language=language)
        if not text:
            # Fallback texte si silence ou erreur
            display_system("(silence détecté — saisie texte)")
            return self._listen_text("Vous : ")
        return text

    # ─────────────────────────────────────────────────
    # PAROLE
    # ─────────────────────────────────────────────────

    def speak(
        self,
        text: str,
        context: dict | None = None,
        mode: str | None = None,
    ) -> None:
        """
        Fait parler ALFRED — vocal si V3, terminal sinon.

        Args:
            text    : Texte à prononcer
            context : Contexte session (context_builder.build_context())
            mode    : Mode explicite (override context)
        """
        # Toujours afficher dans le terminal (trace + fallback)
        display_response(text)

        if not self._tts_ready:
            return

        # Résolution du mode vocal
        if mode:
            vocal_mode = mode
        elif context:
            energy = context.get("energy_level", "medium")
            emotion = context.get("emotion", "neutral")
            vocal_mode = self._resolve_mode(energy, emotion)
        else:
            vocal_mode = "default"

        # Synthèse et lecture Piper
        from src.output.tts_piper import speak as piper_speak
        piper_speak(text, mode=vocal_mode, blocking=True)

    def _resolve_mode(self, energy_level: str, emotion: str) -> str:
        """Résout le mode vocal depuis énergie + émotion."""
        from src.input.voice_profile import EMOTION_TO_MODE, get_mode_from_energy
        if emotion != "neutral" and emotion in EMOTION_TO_MODE:
            return EMOTION_TO_MODE[emotion]
        return get_mode_from_energy(energy_level)

    # ─────────────────────────────────────────────────
    # PIPELINE COMPLET
    # ─────────────────────────────────────────────────

    def process_turn(
        self,
        context: dict,
        history: list[dict],
    ) -> dict:
        """
        Exécute un tour de conversation complet :
          1. Écoute utilisateur
          2. Analyse NLP V2
          3. Retourne le résultat pour le pipeline principal

        Args:
            context : Contexte courant (context_builder)
            history : Historique session

        Returns:
            dict avec user_input, analysis, is_exit
        """
        from src.input.text_input   import is_exit_command, is_valid_input
        from src.input.nlp_engine_v2 import analyze_v2

        # Écoute
        user_input = self.listen()

        # Gestion sortie
        if is_exit_command(user_input):
            return {"user_input": user_input, "analysis": None, "is_exit": True}

        # Validation
        if not is_valid_input(user_input):
            return {"user_input": "", "analysis": None, "is_exit": False}

        # Analyse NLP
        analysis = analyze_v2(user_input)

        return {
            "user_input": user_input,
            "analysis":   analysis,
            "is_exit":    False,
        }

    # ─────────────────────────────────────────────────
    # STATUS
    # ─────────────────────────────────────────────────

    def get_status(self) -> dict:
        """Retourne l'état complet du gestionnaire vocal."""
        return {
            "mode":      self._mode,
            "stt_ready": self._stt_ready,
            "tts_ready": self._tts_ready,
            "version":   "speech_manager_v3",
        }

    def __repr__(self) -> str:
        return (f"SpeechManager(mode={self._mode}, "
                f"stt={self._stt_ready}, tts={self._tts_ready})")
