"""
llm_client_ollama.py
Client Ollama local pour ALFRED.

Pré-requis :
    Ollama installé et lancé : https://ollama.com
    Modèle téléchargé : ollama pull llama3.2

Pas de clé API nécessaire — 100% local.
"""

import json
import urllib.request
import urllib.error
from typing import Optional


class OllamaLLMClient:

    def __init__(
        self,
        model: str = "llama3.2",
        temperature: float = 0.4,
        max_tokens: int = 1200,
        base_url: str = "http://localhost:11434"
    ):
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.base_url = base_url.rstrip("/")

    def is_available(self) -> bool:
        """Vérifie qu'Ollama tourne et que le modèle est disponible."""
        try:
            url = f"{self.base_url}/api/tags"
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req, timeout=3) as resp:
                data = json.loads(resp.read().decode())
                models = [m["name"].split(":")[0] for m in data.get("models", [])]
                return self.model.split(":")[0] in models
        except Exception:
            return False

    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        previous_response_id: Optional[str] = None
    ) -> str:
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "stream": False,
            "options": {
                "temperature": self.temperature,
                "num_predict": self.max_tokens
            }
        }

        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            f"{self.base_url}/api/chat",
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST"
        )

        try:
            with urllib.request.urlopen(req, timeout=300) as resp:
                result = json.loads(resp.read().decode())
                return result["message"]["content"].strip()
        except urllib.error.URLError as e:
            raise ConnectionError(f"Ollama inaccessible : {e}")
        except KeyError:
            raise ValueError(
                f"Modèle '{self.model}' introuvable. Lance : ollama pull {self.model}"
            )
