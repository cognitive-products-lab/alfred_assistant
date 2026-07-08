"""
PROJECT      : ALFRED
BLOCK        : B01
FUNCTION     : XX.XX
FILE         : llm_client_ollama.py
ROLE         : Client LLM Ollama (streaming NDJSON + profils modeles)

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-05-10
UPDATED      : 2026-06-10
VERSION      : V1.1
STATUS       : VALIDATED

DESCRIPTION :
Restauration du streaming reel (on_sentence par phrase) apres incident de
perte de donnees. A re-valider en conditions reelles (test_reel) avant de
repasser en STABLE.
"""

"""
llm_client_ollama.py
Client Ollama local pour ALFRED.

Pré-requis :
    Ollama installé et lancé : https://ollama.com
    Modèle téléchargé : ollama pull llama3.2

Pas de clé API nécessaire — 100% local.
"""

import json
import re
import sys
import urllib.request
import urllib.error
from typing import Callable, Optional


# ─────────────────────────────────────────────────────────────────────────────
# Profils modèles : paramètres optimaux par modèle
# ─────────────────────────────────────────────────────────────────────────────
MODEL_PROFILES: dict[str, dict] = {
    # Modèle actuel — léger, anglophone par nature
    "llama3.2": {
        "temperature": 0.4,
        "max_tokens":  500,
        "num_ctx":     2048,
        "description": "Léger, rapide, anglophone — usage général",
    },
    # Très bon en français, meilleure compréhension des nuances
    "mistral:7b": {
        "temperature": 0.3,   # plus direct, moins de divagation
        "max_tokens":  600,
        "num_ctx":     4096,  # context plus long = meilleure mémoire conversationnelle
        "description": "Recommandé pour ALFRED — excellent en français",
    },
    # Ultra-rapide, idéal pour le conversationnel léger
    "phi3:mini": {
        "temperature": 0.5,
        "max_tokens":  400,
        "num_ctx":     2048,
        "description": "Ultra-rapide — bon pour réponses courtes et navigation commandes",
    },
    # Modèles lourds (Minisforum MS-S1 Max, 64-128 Go RAM unifiée) — a tester
    "llama3.3:70b": {
        "temperature": 0.3,
        "max_tokens":  700,
        "num_ctx":     8192,
        "keep_alive":  "30m",
        "timeout":     600,
        "description": "70B, excellent français — ~42 Go RAM en Q4",
    },
    "qwen2.5:72b": {
        "temperature": 0.3,
        "max_tokens":  700,
        "num_ctx":     8192,
        "keep_alive":  "30m",
        "timeout":     600,
        "description": "72B, très bon multilingue/français — ~45 Go RAM en Q4",
    },
    "command-r-plus:104b": {
        "temperature": 0.3,
        "max_tokens":  700,
        "num_ctx":     8192,
        "keep_alive":  "30m",
        "timeout":     600,
        "description": "104B, fort en RAG/contexte long — ~60 Go RAM en Q4",
    },
    "gpt-oss:120b": {
        "temperature": 0.4,
        "max_tokens":  800,
        "num_ctx":     8192,
        "keep_alive":  "30m",
        "timeout":     600,
        "description": "120B MoE, ~32 tok/s mesuré sur Ryzen AI Max+ 395 — ~65 Go RAM en Q4 (128 Go recommandés)",
    },
    # Fallback générique pour tout autre modèle
    "__default__": {
        "temperature": 0.4,
        "max_tokens":  500,
        "num_ctx":     2048,
        "description": "Profil générique",
    },
}


class OllamaLLMClient:

    def __init__(
        self,
        model: str = "llama3.2",
        temperature: float | None = None,
        max_tokens: int | None = None,
        base_url: str = "http://localhost:11434",
        stream: bool = True,
    ):
        self.model = model
        self.base_url = base_url.rstrip("/")
        self.stream = stream
        self.last_was_streamed = False

        # Applique le profil du modèle, surchargeable manuellement
        profile = MODEL_PROFILES.get(model, MODEL_PROFILES["__default__"])
        self.temperature = temperature if temperature is not None else profile["temperature"]
        self.max_tokens  = max_tokens  if max_tokens  is not None else profile["max_tokens"]
        self.num_ctx     = profile.get("num_ctx", 2048)
        self.keep_alive  = profile.get("keep_alive")
        self.timeout     = profile.get("timeout", 300)
        self.profile_desc = profile.get("description", "")

    @classmethod
    def from_profile(cls, model: str, **overrides) -> "OllamaLLMClient":
        """Instancie depuis un profil nommé avec surcharges optionnelles."""
        return cls(model=model, **overrides)

    def profile_info(self) -> dict:
        """Retourne les paramètres actifs du modèle."""
        return {
            "model":       self.model,
            "temperature": self.temperature,
            "max_tokens":  self.max_tokens,
            "num_ctx":     self.num_ctx,
            "keep_alive":  self.keep_alive,
            "description": self.profile_desc,
        }

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
        previous_response_id: Optional[str] = None,
        stream_prefix: str = "  ALFRED : ",
        on_sentence: Optional[Callable[[str], None]] = None,
    ) -> str:
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "stream": self.stream,
            "options": {
                "temperature": self.temperature,
                "num_predict": self.max_tokens,
                "num_ctx":     self.num_ctx,
            }
        }
        if self.keep_alive:
            payload["keep_alive"] = self.keep_alive

        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            f"{self.base_url}/api/chat",
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST"
        )

        try:
            if self.stream:
                self.last_was_streamed = True
                return self._generate_stream(req, stream_prefix, on_sentence)
            else:
                self.last_was_streamed = False
                return self._generate_blocking(req)
        except urllib.error.URLError as e:
            raise ConnectionError(f"Ollama inaccessible : {e}")

    def _generate_stream(
        self,
        req: urllib.request.Request,
        prefix: str,
        on_sentence: Optional[Callable[[str], None]] = None,
    ) -> str:
        """Affiche le texte token par token, retourne la réponse complète.
        Si on_sentence fourni, l'appelle sur chaque phrase complète pendant le stream."""
        full_text: list[str] = []
        first_token = True
        sentence_buf: list[str] = []

        with urllib.request.urlopen(req, timeout=self.timeout) as resp:
            for raw_line in resp:
                line = raw_line.decode("utf-8").strip()
                if not line:
                    continue
                try:
                    chunk = json.loads(line)
                except json.JSONDecodeError:
                    continue

                token = chunk.get("message", {}).get("content", "")
                if token:
                    if first_token:
                        print(prefix, end="", flush=True)
                        first_token = False
                    print(token, end="", flush=True)
                    full_text.append(token)

                    if on_sentence:
                        sentence_buf.append(token)
                        buf = "".join(sentence_buf)
                        # Découpe sur ponctuation forte suivie d'espace ou fin de ligne
                        parts = re.split(r'(?<=[.!?:])\s+', buf)
                        if len(parts) > 1:
                            for phrase in parts[:-1]:
                                phrase = phrase.strip()
                                if phrase:
                                    on_sentence(phrase)
                            sentence_buf = [parts[-1]]

                if chunk.get("done", False):
                    break

        # Parle le reste du buffer (dernière phrase incomplète ou sans ponctuation)
        if on_sentence and sentence_buf:
            remainder = "".join(sentence_buf).strip()
            if remainder:
                on_sentence(remainder)

        if full_text:
            print()  # saut de ligne final
        return "".join(full_text).strip()

    def _generate_blocking(self, req: urllib.request.Request) -> str:
        """Mode non-stream — retourne la réponse complète d'un coup."""
        with urllib.request.urlopen(req, timeout=self.timeout) as resp:
            result = json.loads(resp.read().decode())
            return result["message"]["content"].strip()
