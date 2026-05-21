"""
audio_listener.py
-----------------

Module d'écoute audio haut niveau pour ALFRED.

Ce fichier sert de façade entre l'orchestrateur principal d'ALFRED
et les modules techniques de capture audio.

Objectif :
- fournir une interface stable : AudioListener.listen()
- permettre un mode simulation pour les tests
- éviter que le reste de l'application dépende directement
  d'une implémentation technique précise

Note :
La capture audio réelle doit rester gérée par audio_capture.py.
"""

from typing import Optional


class AudioListener:
    """
    Interface haut niveau d'écoute audio pour ALFRED.

    Modes supportés :
    - simulation : saisie clavier pour tester sans micro
    - audio_capture : futur branchement vers le module audio_capture.py
    """

    def __init__(self, mode: str = "simulation") -> None:
        """
        Initialise le listener audio.

        Args:
            mode: Mode d'écoute utilisé.
                  Valeurs prévues : "simulation", "audio_capture".
        """
        self.mode = mode

    def listen(self) -> Optional[str]:
        """
        Lance l'écoute utilisateur et retourne le texte capté.

        Returns:
            str | None: Texte reconnu ou None en cas d'erreur / silence.
        """
        try:
            if self.mode == "simulation":
                return self._listen_simulation()

            if self.mode == "audio_capture":
                return self._listen_audio_capture()

            raise ValueError(f"Mode audio non supporté : {self.mode}")

        except KeyboardInterrupt:
            print("\n🛑 Écoute interrompue par l'utilisateur.")
            return None

        except Exception as error:
            print(f"❌ Erreur AudioListener.listen() : {error}")
            return None

    def _listen_simulation(self) -> Optional[str]:
        """
        Mode de simulation par saisie clavier.

        Utile pour tester ALFRED sans micro ni STT.
        """
        user_input = input("🎤 Simulation audio — saisie utilisateur : ").strip()

        if not user_input:
            return None

        return user_input

    def _listen_audio_capture(self) -> Optional[str]:
        """
        Point de connexion futur vers audio_capture.py.

        À brancher lorsque le module audio_capture.py expose une fonction
        stable de capture ou de transcription.
        """
        raise NotImplementedError(
            "Le mode 'audio_capture' doit être relié à src/input/audio_capture.py."
        )
