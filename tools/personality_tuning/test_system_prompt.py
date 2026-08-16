"""
PROJECT      : ALFRED
BLOCK        : B01
FUNCTION     : Outil de reglage comportemental — test du prompt systeme
FILE         : tools/personality_tuning/test_system_prompt.py
ROLE         : Construit le vrai prompt systeme (ResponseGenerator._build_system_prompt,
               contexte realiste proche de src/main.py) et l'envoie a Ollama pour une
               liste de questions de test, sans lancer toute l'application. Detecte
               automatiquement les reponses degenerees (repetition en boucle) —
               symptome observe en conditions reelles le 16/08/2026 (ex. "L'artiste
               L'artiste L'artiste..." des dizaines de fois), imputable a un prompt
               systeme trop long/repetitif plutot qu'au modele seul.

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-08-16
VERSION      : V1.0
STATUS       : CODE

USAGE :
    python tools/personality_tuning/test_system_prompt.py
    python tools/personality_tuning/test_system_prompt.py --model llama3.2
    python tools/personality_tuning/test_system_prompt.py --query "quelle heure est-il ?"
    python tools/personality_tuning/test_system_prompt.py --show-prompt-only

DESCRIPTION :
Sert a valider un changement dans _build_system_prompt (ou un changement de modele
Ollama) sans devoir relancer toute l'appli ALFRED ni interagir avec un appareil reel —
utile pour iterer rapidement sur le reglage comportemental (personnalite, regles,
longueur du prompt). N'écrit rien en base, ne modifie aucun etat ALFRED reel.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

# Console Windows par défaut en cp1252 — incapable d'afficher les accents/emoji
# de ce script (français + symboles ✅/❌). Force UTF-8 en sortie, cohérent avec
# le reste du pipeline ALFRED qui écrit déjà de l'UTF-8 partout ailleurs.
sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.core.response_generator import ResponseGenerator  # noqa: E402
from src.llm.llm_client_ollama import OllamaLLMClient  # noqa: E402

# Contexte realiste (calque sur le bloc de test existant en bas de
# response_generator.py) — assez proche de ce que main.py construit reellement
# pour reproduire fidelement la longueur/structure du vrai prompt systeme.
DEFAULT_CONTEXT = {
    "assistant": {
        "name": "ALFRED",
        "role": "Assistant personnel adaptatif",
        "mission": "Accompagner Céline dans ses projets",
        "positioning": "Hybride : soutien + analyse",
    },
    "personality": {
        "archetype": "compagnon_strategique_empathique",
        "dominant_traits": ["chaleureux", "structuré", "intelligent"],
        "forbidden_traits": ["condescendant", "froid"],
    },
    "response_rules": {
        "be_clear": True,
        "be_structured": True,
        "be_direct": True,
        "use_step_by_step": True,
        "avoid_overload": True,
        "use_empathy": True,
        "use_humor": False,
    },
    "boundaries": {
        "medical": "orienter vers professionnel",
        "psychological": "écouter, ne pas diagnostiquer",
        "legal": "informer, ne pas conseiller",
        "privacy": "données locales uniquement",
    },
    "safety": {
        "anti_manipulation": True,
        "anti_dependency": True,
        "neutrality": True,
    },
    "user": {"preferred_name": "Céline"},
    "memory_context": (
        "[Mémoire long terme SQLite — messages utilisateur récents]\n"
        "- [2026-05-03 18:00] Céline : Je travaille actuellement sur l'injection mémoire dans Alfred."
    ),
}

DEFAULT_QUERIES = [
    "quelles sont tes connaissances en psychologie ?",
    "que sais-tu à mon propos ?",
    "quelle est la météo à Ascoux aujourd'hui ?",
    "résume mes tâches",
    "bonjour",
]


def _looks_degenerate(text: str) -> str | None:
    """Détection heuristique simple d'une réponse dégénérée : un même mot/groupe
    de mots répété en boucle, ou une proportion anormale de mots non-français
    évidents. Retourne une description du problème détecté, ou None si OK."""
    words = re.findall(r"\w+", text.lower())
    if len(words) < 8:
        return None

    # Répétition : un mot (>=4 lettres) représente plus de 20% des mots du texte.
    from collections import Counter

    counts = Counter(w for w in words if len(w) >= 4)
    if counts:
        word, n = counts.most_common(1)[0]
        ratio = n / len(words)
        if ratio > 0.20 and n >= 5:
            return f"répétition dégénérée : '{word}' répété {n}x ({ratio:.0%} des mots)"

    return None


def run(model: str, queries: list[str], show_prompt_only: bool = False) -> None:
    gen = ResponseGenerator(debug=False)
    system_prompt = gen._build_system_prompt(context=DEFAULT_CONTEXT)  # noqa: SLF001
    print(f"=== Prompt système ({len(system_prompt)} caractères, "
          f"{len(system_prompt.split())} mots) ===\n")
    print(system_prompt)
    print()

    if show_prompt_only:
        return

    client = OllamaLLMClient(model=model)
    if not client.is_available():
        print(f"❌ Modèle '{model}' indisponible (Ollama non lancé, ou modèle non téléchargé — "
              f"'ollama pull {model}').")
        return

    print(f"=== Test contre {queries.__len__()} question(s), modèle '{model}' ===\n")
    for query in queries:
        user_prompt = gen._build_user_prompt(query, DEFAULT_CONTEXT)  # noqa: SLF001
        try:
            response = client.generate(system_prompt, user_prompt)
        except Exception as exc:  # noqa: BLE001
            print(f"[ÉCHEC] {query!r} → exception : {exc}\n")
            continue

        verdict = _looks_degenerate(response)
        status = f"❌ SUSPECT — {verdict}" if verdict else "✅ OK"
        print(f"--- {query!r} — {status} ---")
        print(response[:400])
        print()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", default="mistral:7b", help="Modèle Ollama à tester (défaut : mistral:7b)")
    parser.add_argument("--query", action="append", dest="queries",
                         help="Question à tester (répétable). Défaut : liste de questions problématiques connues.")
    parser.add_argument("--show-prompt-only", action="store_true",
                         help="Affiche uniquement le prompt système construit, sans appeler Ollama.")
    args = parser.parse_args()

    run(
        model=args.model,
        queries=args.queries or DEFAULT_QUERIES,
        show_prompt_only=args.show_prompt_only,
    )
