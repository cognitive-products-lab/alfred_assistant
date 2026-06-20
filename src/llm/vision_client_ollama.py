"""
PROJECT      : ALFRED
BLOCK        : B04 -- Vision
FUNCTION     : 04.01
FILE         : src/llm/vision_client_ollama.py
ROLE         : Client Ollama vision (llava) -- analyse d'image caméra

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-06-13
UPDATED      : 2026-06-20
VERSION      : V1.0
STATUS       : ACTIVE

DESCRIPTION :
Client minimal pour interroger un modèle vision Ollama (llava) avec une
image encodée en base64. Utilisé pour répondre aux questions du type
"décris ce que tu vois via la caméra".
Branchement vérifié le 15/06 : llava:7b présent (ollama list).
Validé le 20/06 via VisionAnalyzer + tests mock 43/43.
Test réel caméra : flux live OK (retour image validé en session 20/06).
"""

from __future__ import annotations

import json
import urllib.error
import urllib.request


class OllamaVisionClient:
    """
    Client Ollama pour modèles multimodaux (ex. llava:7b).

    Usage :
        client = OllamaVisionClient(model="llava:7b")
        if client.is_available():
            description = client.analyze_image(image_b64, "Décris cette image.")
    """

    def __init__(
        self,
        model: str = "llava:7b",
        base_url: str = "http://localhost:11434",
        timeout: int = 120,
    ):
        self.model = model
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def is_available(self) -> bool:
        """Vérifie qu'Ollama tourne et que le modèle vision est disponible."""
        try:
            url = f"{self.base_url}/api/tags"
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req, timeout=3) as resp:
                data = json.loads(resp.read().decode())
                models = [m["name"] for m in data.get("models", [])]
                return any(m.split(":")[0] == self.model.split(":")[0] for m in models)
        except Exception:
            return False

    def analyze_image(self, image_b64: str, prompt: str) -> str:
        """
        Envoie une image (base64, sans préfixe data:) et un prompt au modèle vision.

        Args:
            image_b64 : image encodée en base64 (JPEG/PNG)
            prompt    : question/instruction (ex. "Décris cette image en français.")

        Returns:
            Texte de réponse du modèle, ou message d'erreur lisible si échec.
        """
        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "user",
                    "content": prompt,
                    "images": [image_b64],
                }
            ],
            "stream": False,
            "options": {
                "temperature": 0.2,
                "num_predict": 300,
            },
        }

        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            f"{self.base_url}/api/chat",
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                result = json.loads(resp.read().decode())
                return result["message"]["content"].strip()
        except urllib.error.URLError as exc:
            raise ConnectionError(f"Ollama (vision) inaccessible : {exc}")
