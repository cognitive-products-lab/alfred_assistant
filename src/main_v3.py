# ============================================================
# ALFRED — src/main_v3.py
# Bloc 01.04 — Orchestration des modules
#
# 📚 NOTION EXAM :
#   D11-1 — Capsule 1 : Pipeline conversationnel et orchestration V3
#
# 🎯 UTILITÉ ALFRED :
#   Point d'entrée V3 — intègre le moteur vocal (STT/TTS Piper),
#   le pipeline NLP V2 et l'orchestrateur SpeechManager.
#
# 🏗️ DOMAINE :
#   Noyau conversationnel & orchestration — pipeline vocal V3
# ============================================================

from __future__ import annotations

import sys
from datetime import datetime
from pathlib import Path
from typing import Any

# =============================================================================
# 0. RACINE PROJET
# =============================================================================

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


# =============================================================================
# 1. CHEMINS PROJET
# =============================================================================

PERSONALITY_PATH = ROOT / "data" / "personality" / "instances" / "personality_core_instance.json"
USER_PROFILE_PATH = ROOT / "data" / "users" / "instances" / "user_celine_instance.json"
MEMORY_PATH = ROOT / "data" / "memory" / "episodic" / "dialogue_history.json"
IDENTITY_PATH = ROOT / "knowledges" / "core" / "alfred_core_identity.json"
KNOWLEDGE_ROOT = ROOT / "knowledges"
CONFIG_DIR = ROOT / "config"


# =============================================================================
# 2. CONFIGURATION GLOBALE
# =============================================================================

ALFRED_NAME = "ALFRED"
USER_FALLBACK_NAME = "Céline"
MODEL = "llama3.2"
MAX_INPUT_LENGTH = 2000
MAX_MEMORY_CONTEXT = 8
VOICE_RECORD_SECONDS = 10


# =============================================================================
# 3. BRIDGES B03 -> BEHAVIOR ENGINE
# =============================================================================

MODE_BRIDGE = {
    "support": "support_mode",
    "focus": "execution_mode",
    "challenge": "execution_mode",
    "complicite": "hybrid_mode",
    "default": "hybrid_mode",
}

EMOTION_BRIDGE = {
    "stressed": ("stress", 0.8),
    "tired": ("fatigue", 0.7),
    "sad": ("sadness", 0.7),
    "distress": ("overwhelm", 0.9),
    "confused": ("stress", 0.5),
    "motivated": ("motivation", 0.7),
    "happy": ("joy", 0.6),
    "focused": ("neutral", 0.3),
    "neutral": ("neutral", 0.2),
}


# =============================================================================
# 4. UTILITAIRES TEXTE / SECURITE BASIQUE
# =============================================================================

def sanitize_input(text: str) -> str:
    """
    Nettoie l'entrée utilisateur.

    - Supprime les caractères non imprimables
    - Garde les retours ligne et tabulations
    - Tronque les messages trop longs
    - Retourne une chaîne vide si l'entrée est inutilisable
    """
    if not text or not text.strip():
        return ""

    cleaned = "".join(
        char for char in text
        if char.isprintable() or char in ("\n", "\t")
    ).strip()

    if len(cleaned) > MAX_INPUT_LENGTH:
        cleaned = cleaned[:MAX_INPUT_LENGTH]
        print(f"  [INFO] Message tronqué à {MAX_INPUT_LENGTH} caractères.")

    return cleaned

def clean_for_tts(text: str) -> str:
    replacements = {
        "👉": "",
        "⚠️": "Attention.",
        "🧠": "",
        "🎤": "",
        "✅": "",
        "❌": "",
        "🔥": "",
        "—": "-",
        "’": "'",
        "“": '"',
        "”": '"',
        "«": "",
        "»": "",
    }

    cleaned = text
    for old, new in replacements.items():
        cleaned = cleaned.replace(old, new)

    return cleaned

def safe_getattr(obj: Any, attr: str, default: Any = None) -> Any:
    """Récupère un attribut sans faire tomber la boucle principale."""
    try:
        return getattr(obj, attr, default)
    except Exception:
        return default


# =============================================================================
# 5. AFFICHAGE TERMINAL
# =============================================================================

def banner(name: str, memory_summary: str, llm_available: bool) -> None:
    """Affiche le bandeau de démarrage."""

    llm_status = (
        "LLM Router actif : Ollama local → OpenAI fallback"
        if llm_available
        else "⚠️ MODE DÉGRADÉ (LLM OFF)"
    )
    if not llm_available:
        print("⚠️ ATTENTION : ALFRED fonctionne sans LLM (mode dégradé)")

    print("")
    print("╔══════════════════════════════════════════════════╗")
    print("║        ALFRED — V1.2 + mémoire long terme        ║")
    print("║     Local-first | Security by Design             ║")
    print("╚══════════════════════════════════════════════════╝")
    print(f"  Base     : {ROOT}")
    print(f"  Mémoire  : {memory_summary}")
    print(f"  Moteur   : {llm_status}")
    print(f"  Bonjour {name} !")
    print("")


def print_help() -> None:
    """Affiche les commandes disponibles."""
    print("─" * 58)
    print("  Tape ton message normalement.")
    print("  Commandes disponibles :")
    print("    exit / quit / bye / au revoir  → quitter")
    print("    memoire                       → afficher l'historique récent JSON")
    print("    memoire_ltm                   → afficher la mémoire long terme SQLite")
    print("    mode                          → afficher le mode actuel")
    print("    stats                         → statistiques mémoire JSON")
    print("    ltm_stats                     → statistiques mémoire long terme")
    print("    reset                         → vider la mémoire de session JSON")
    print("    statut                        → état des composants")
    print("    aide                          → afficher cette aide")
    print("    vocal                         → activer/désactiver le mode vocal")
    print("    ecoute                        → dicter un message une seule fois")
    print("─" * 58)
    print("")

def print_status(components: dict[str, Any]) -> None:
    """Affiche un état synthétique des composants."""
    print("\n  ── Statut ALFRED ──")
    print(f"  PersonalityAdapter : {'OK' if components.get('adapter') else 'NON'}")
    print(f"  BehaviorEngine     : {'OK' if components.get('behavior_engine') else 'NON'}")
    print(f"  KnowledgeLoader    : {'OK' if components.get('loader') else 'NON'}")
    print(f"  MemoryEngine       : {'OK' if components.get('memory') else 'NON'}")
    print(f"  LongTermMemory     : {'OK' if components.get('ltm_ok') else 'NON / optionnelle'}")

    llm = components.get("llm")

    if llm and hasattr(llm, "provider_status"):
        print(f"  LLM Router         : {llm.provider_status()}")
    else:
        print(f"  LLM Router         : NON / fallback offline")

    print(f"  Modèle             : {MODEL}")
    print(f"  Date session       : {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"  TTS Piper          : {'OK' if components.get('tts') else 'NON'}")
    print(f"  Mode vocal         : {'ACTIF' if components.get('voice_enabled') else 'INACTIF'}")
    print("  LTM SQLite         : branchée si src.memory.long_term_memory est disponible")
    print("")


# =============================================================================
# 6. DETECTION CONTEXTE B03
# =============================================================================

def detect_context(user_input: str, time_context: dict[str, Any]) -> dict[str, Any]:
    """
    Détecte émotion + wellbeing + mode depuis le message.

    Retourne un dictionnaire exploitable par :
      - PersonalityAdapter
      - AlfredBehaviorEngine
      - ResponseGenerator
    """
    from src.regulation.emotion_detector import detect_emotion
    from src.regulation.wellbeing_tracker import analyze_wellbeing
    from src.regulation.mode_manager import get_mode_manager
    from src.conversation.nlp.nlp_engine_v2 import analyze_v2

    nlp = analyze_v2(user_input)
    emotion_state = detect_emotion(user_input)
    wellbeing = analyze_wellbeing(user_input, time_context)

    manager = get_mode_manager()
    manager.update_from_emotion(emotion_state)
    mode_b03 = manager.current_mode

    behavior_mode = MODE_BRIDGE.get(mode_b03, "hybrid_mode")

    emotion_id = safe_getattr(emotion_state, "emotion", "neutral")
    behavior_emotion, intensity = EMOTION_BRIDGE.get(emotion_id, ("neutral", 0.2))

    fatigue_score = safe_getattr(wellbeing, "fatigue_score", 0.0)

    return {
        "nlp": nlp,
        "emotion_state": emotion_state,
        "wellbeing": wellbeing,
        "mode_b03": mode_b03,
        "behavior_mode": behavior_mode,
        "behavior_emotion": behavior_emotion,
        "intensity": intensity,
        "fatigue": fatigue_score,
    }


# =============================================================================
# 7. INITIALISATION COMPOSANTS
# =============================================================================

def init_components() -> dict[str, Any]:
    """Initialise les composants principaux d'ALFRED."""
    from src.core.personality_adapter import PersonalityAdapter
    from src.core.response_generator import ResponseGenerator
    from src.core.alfred_behavior_engine import AlfredBehaviorEngine
    from src.knowledge.knowledge_loader import KnowledgeLoader
    from src.memory.memory_engine import MemoryEngine
    from src.regulation.mode_manager import get_mode_manager
    from src.llm.llm_client_ollama import OllamaLLMClient
    from src.llm.llm_client_openai import OpenAILLMClient
    from src.llm.llm_router import LLMRouter
    from src.conversation.input.input_manager import HybridInputManager
    

    components: dict[str, Any] = {
        "adapter": None,
        "behavior_engine": None,
        "loader": None,
        "memory": None,
        "llm": None,
        "generator": None,
        "mode_manager": None,
        "ltm_ok": False,
        "ltm": None,
        "session_id": datetime.now().strftime("%Y%m%d_%H%M%S"),
        "user_name": USER_FALLBACK_NAME,
        "tts": None,
        "voice_enabled": True,
    }

    # Mémoire JSON existante
    try:
        components["memory"] = MemoryEngine(
            history_path=str(MEMORY_PATH),
            max_context_entries=MAX_MEMORY_CONTEXT,
        )
    except Exception as exc:
        print(f"  [ERREUR] MemoryEngine : {exc}")
        raise

    # Mémoire long terme SQLite existante
    try:
        from src.memory import long_term_memory as ltm
        ltm.init_db()
        components["ltm"] = ltm
        components["ltm_ok"] = True
    except Exception as exc:
        print(f"  [AVERT] LongTermMemory indisponible : {exc}")
        components["ltm"] = None
        components["ltm_ok"] = False

    # PersonalityAdapter
    try:
        adapter = PersonalityAdapter(
            personality_path=str(PERSONALITY_PATH),
            user_profile_path=str(USER_PROFILE_PATH),
            allow_templates=False,
        )
        components["adapter"] = adapter
        components["user_name"] = (
            adapter.user_profile
            .get("user_profile", {})
            .get("preferred_name", USER_FALLBACK_NAME)
        )
    except Exception as exc:
        print(f"  [ERREUR] PersonalityAdapter : {exc}")
        raise

    # BehaviorEngine optionnel mais important
    try:
        components["behavior_engine"] = AlfredBehaviorEngine(str(IDENTITY_PATH))
    except Exception as exc:
        print(f"  [AVERT] BehaviorEngine indisponible : {exc}")
        components["behavior_engine"] = None

    # KnowledgeLoader
    try:
        components["loader"] = KnowledgeLoader(
            knowledge_root=str(KNOWLEDGE_ROOT),
            config_dir=str(CONFIG_DIR),
            debug=False,
        )
    except Exception as exc:
        print(f"  [AVERT] KnowledgeLoader indisponible : {exc}")
        components["loader"] = None

    # LLM Router : Ollama local -> OpenAI fallback -> fallback offline
    try:
        ollama = OllamaLLMClient(model=MODEL)

        try:
            openai = OpenAILLMClient(model="gpt-4o")
         
        except Exception as exc:
            openai = None
            print(f"  [AVERT] OpenAI indisponible : {exc}")

        components["llm"] = LLMRouter(
            primary=ollama,
            secondary=openai,
            allow_cloud_fallback=True,
            debug=True,
        )

        status = components["llm"].provider_status()
        print(f"DEBUG LLM Router : {status}")

    except Exception as exc:
        print(f"  [AVERT] Aucun LLM disponible : {exc}")
        components["llm"] = None

    # ResponseGenerator
    try:
        components["generator"] = ResponseGenerator(
            llm_client=components["llm"],
            debug=False,
        )
    except Exception as exc:
        print(f"  [ERREUR] ResponseGenerator : {exc}")
        raise

    # ModeManager singleton
    try:
        components["mode_manager"] = get_mode_manager()
    except Exception as exc:
        print(f"  [AVERT] ModeManager indisponible : {exc}")
        components["mode_manager"] = None
    
    # TTS Piper CLI
    try:
        from src.conversation.output.tts_engine import TTSEngine
        from src.conversation.output.tts_piper import PiperTTS

        components["tts"] = TTSEngine(
            backend=PiperTTS(mode="complicite", blocking=True)
        )
    except Exception as exc:
        print(f"  [AVERT] TTS Piper indisponible : {exc}")
        components["tts"] = None

    return components




# =============================================================================
# 8. COMMANDES SPECIALES
# =============================================================================

def listen_voice_once(duration: int = VOICE_RECORD_SECONDS) -> str:
    """
    Capture le micro pendant quelques secondes et retourne le texte transcrit.
    V1 améliorée : écoute plus longue + Whisper small + réglages anti-hallucination.
    """
    import sounddevice as sd
    import numpy as np
    from faster_whisper import WhisperModel

    samplerate = 16000

    print(f"  🎤 Écoute pendant {duration} secondes...", end="\r")

    audio = sd.rec(
        int(duration * samplerate),
        samplerate=samplerate,
        channels=1,
        dtype="float32",
    )
    sd.wait()

    audio = np.squeeze(audio)

    print("  🧠 Transcription...")

    model = WhisperModel("small", compute_type="int8")

    segments, _ = model.transcribe(
        audio,
        language="fr",
        beam_size=5,
        vad_filter=True,
        temperature=0.0,
        initial_prompt=(
            "Conversation en français avec Alfred, assistant vocal personnel. "
            "Le prénom de l'utilisatrice est Céline. "
            "Le sujet actuel est le branchement du micro, du haut-parleur, du STT et du TTS."
        ),
    )

    text = " ".join(segment.text.strip() for segment in segments).strip()

    return text

def handle_command(command: str, components: dict[str, Any]) -> bool:
    """
    Gère les commandes spéciales.

    Retourne :
      True  -> commande traitée, on continue la boucle
      False -> ce n'était pas une commande spéciale
    """
    cmd = command.lower().strip()
    memory = components.get("memory")
    mode_manager = components.get("mode_manager")

    # Alias / compréhension naturelle du mode vocal
    if "activer" in cmd and "vocal" in cmd:
        components["voice_enabled"] = True
        print("\n  Mode vocal activé.\n")
        return True
    
    if (
        "desactiver" in cmd
        or "désactiver" in cmd
    ) and "vocal" in cmd:
        components["voice_enabled"] = False
        print("\n  Mode vocal désactivé.\n")
        return True

    if cmd in {"aide", "help", "?"}:
        print_help()
        return True

    if cmd == "memoire":
        try:
            ctx = memory.format_context_for_prompt(5) if memory else ""
            print("\n" + (ctx if ctx else "  Aucun échange en mémoire.") + "\n")
        except Exception as exc:
            print(f"\n  [ERREUR mémoire] {exc}\n")
        return True

    if cmd == "memoire_ltm":
        ltm = components.get("ltm")
        if not components.get("ltm_ok") or not ltm:
            print ("Mémoire long terme non disponible dans cette exécution.")
            return True
        try:
            memories = ltm.get_recent_memories(n=8)
            if not memories:
                print("Aucun échange en mémoire long terme pour l'instant.")
                return True

            print(" ── Mémoire long terme SQLite ──")
            for mem in memories:
                ts = mem.get("timestamp", "")[:16].replace("T", " ")
                user = mem.get("user_input", "")[:90]
                resp = mem.get("alfred_resp", "")[:120]
                emotion = mem.get("emotion", "neutral")
                intent = mem.get("intent", "general")
                print(f"[{ts}] intent={intent} | émotion={emotion}")
                print(f"  Toi    : {user}")
                print(f"  ALFRED : {resp}")
            print("")
        except Exception as exc:
            print(f"[ERREUR LTM] {exc}")
        return True

    if cmd == "ltm_stats":
        ltm = components.get("ltm")
        if not components.get("ltm_ok") or not ltm:
            print("Mémoire long terme non disponible dans cette exécution.")
            return True
        try:
            stats = ltm.get_memory_stats()
            print(" ── Stats mémoire long terme ──")
            print(f"  Actives   : {stats.get('memories_active', 0)}")
            print(f"  Archivées : {stats.get('memories_archived', 0)}")
            print(f"  Facts     : {stats.get('facts', 0)}")
            print(f"  Patterns  : {stats.get('patterns', 0)}")
            print(f"  DB        : {stats.get('db_path')}")
            print("")
        except Exception as exc:
            print(f" [ERREUR ltm_stats] {exc}")
        return True

    if cmd == "mode":
        if mode_manager:
            try:
                status = mode_manager.get_status()
                print(
                    f"\n  Mode actuel : {status.get('current_mode')} | "
                    f"Voix : {status.get('voice_profile', 'non branchée')} | "
                    f"Transitions : {status.get('transitions', 0)}\n"
                )
            except Exception as exc:
                print(f"\n  [ERREUR mode] {exc}\n")
        else:
            print("\n  ModeManager non disponible.\n")
        return True

    if cmd == "stats":
        try:
            if memory:
                stats = memory.stats()
                print(
                    f"\n  Échanges : {stats.get('total_exchanges', 0)} | "
                    f"Fichier : {stats.get('file', MEMORY_PATH)}\n"
                )
            else:
                print("\n  MemoryEngine non disponible.\n")
        except Exception as exc:
            print(f"\n  [ERREUR stats] {exc}\n")
        return True

    if cmd == "statut":
        print_status(components)
        return True

    if cmd == "reset":
        try:
            if memory and hasattr(memory, "clear_session"):
                memory.clear_session()
                components["session_id"] = datetime.now().strftime("%Y%m%d_%H%M%S")
                print("Mémoire de session JSON réinitialisée. Nouvelle session créée.")
            else:
                print("Reset automatique non disponible sur ce MemoryEngine.",
                    "Tu peux vider manuellement dialogue_history.json si nécessaire."
                )
        except Exception as exc:
            print(f"\n  [ERREUR reset] {exc}\n")
        return True

    if cmd == "vocal":
        components["voice_enabled"] = not components.get("voice_enabled", False)
        state = "activé" if components["voice_enabled"] else "désactivé"
        
        print(f"\n  Mode vocal {state}.\n")

        # 🔊 Feedback vocal
        tts = components.get("tts")
        if tts:
            try:
                tts.speak(f"Mode vocal {state}".replace("é", "e"))
            except Exception as exc:
                print(f"[AVERT TTS] {exc}")

        return True

    if (
        "desactiver vocal" in cmd
        or "désactiver vocal" in cmd
        or "coupe le vocal" in cmd
    ):
        components["voice_enabled"] = False

        print("\n  Mode vocal désactivé.\n")

        tts = components.get("tts")
        if tts:
            try:
                tts.speak("Mode vocal desactive")
            except Exception as exc:
                print(f"[AVERT TTS] {exc}")

        return True

    if cmd == "ecoute":
        try:
            text = listen_voice_once()
            if text:
                print(f"\n  Toi 🎤 : {text}\n")
                components["_voice_once_text"] = text
            else:
                print("\n  Aucun texte détecté.\n")
        except Exception as exc:
            print(f"\n  [ERREUR écoute] {type(exc).__name__} — {exc}\n")
        return True

    return False


# =============================================================================
# 9. PIPELINE REPONSE
# =============================================================================

def build_response(
    user_input: str,
    components: dict[str, Any],
    time_ctx: dict[str, Any],
) -> tuple[str, str, str, str]:
    """
    Construit la réponse ALFRED.

    Retourne :
      response, mode, emotion_label, energy_level
    """
    from src.core.alfred_behavior_engine import UserState

    try:
        ltm = components.get("ltm")
        if components.get("ltm_ok") and ltm:
            recent_memories = ltm.get_recent_memories(n=5)

            memory_lines = ["[Mémoire long terme SQLite — échanges récents]"]
            for mem in recent_memories:
                ts = mem.get("timestamp", "")[:16].replace("T", " ")
                user = mem.get("user_input", "")
                resp = mem.get("alfred_resp", "")
                memory_lines.append(f"- [{ts}] Céline : {user}")
                memory_lines.append(f"  ALFRED : {resp[:200]}")

            memory_context = "\n".join(memory_lines)
        else:
            memory_context = ""
    except Exception as exc:
        memory_context = ""
        print(f"  [AVERT LTM] contexte mémoire non injecté : {exc}")

    adapter = components["adapter"]
    behavior_engine = components["behavior_engine"]
    generator = components["generator"]

    detected = detect_context(user_input, time_ctx)

    emotion_state = detected["emotion_state"]
    emotion_label = safe_getattr(emotion_state, "emotion", "neutral")
    behavior_mode = detected["behavior_mode"]
    energy_level = "low" if detected["fatigue"] > 0.5 else "medium"

    # Contexte PersonalityAdapter
    context = adapter.build_response_context(
        user_message=user_input,
        detected_emotion=detected["behavior_emotion"],
        energy_level=energy_level,
    )
    context["memory_context"] = memory_context
    context["project_context"] = """
        Projet actuel :
        ALFRED V1.2 local-first.

        Travail en cours :
        - mode vocal et clavier
        - boucle conversationnelle
        - commandes système
        - STT Whisper
        - TTS Piper
        - mémoire JSON et SQLite
        - LLM Router Ollama local -> OpenAI fallback
        - stabilisation du pipeline conversationnel
        - préparation du Knowledge Retrieval Engine

        Priorités :
        - stabilité
        - faible latence
        - sécurité
        - architecture scalable
        - cohérence mémoire
        """
    user_input_for_llm = f"""
        CONTEXTE PROJET ACTUEL :
        Céline travaille actuellement sur ALFRED V1.2 local-first.

        Travail en cours :
        - mode vocal et clavier
        - boucle conversationnelle
        - commandes système
        - STT Whisper
        - TTS Piper
        - mémoire JSON et SQLite
        - LLM Router Ollama local -> OpenAI fallback
        - stabilisation du pipeline conversationnel
        - préparation du Knowledge Retrieval Engine

        Question utilisateur :
        {user_input}
        """
    from src.memory.memory_answer_engine import answer_from_memory
    
    memory_answer = answer_from_memory(
        user_message=user_input,
        memory_context=memory_context,
    )

    if memory_answer:
        # On évite que la mémoire réponde seule aux questions d'analyse technique.
        technical_keywords = [
            "risque",
            "risques",
            "technique",
            "techniques",
            "anticiper",
            "architecture",
            "problème",
            "bug",
            "pipeline",
            "stt",
            "tts",
            "vocal",
            "clavier",
            "retrieval",
            "knowledge"
        ]

        if not any(word in user_input.lower() for word in technical_keywords):
            mode = "memory_mode"
            return memory_answer, mode, emotion_label, energy_level
    

    # Override mode B03 -> behavior mode
    context.setdefault("adaptation", {})
    context["adaptation"]["mode"] = behavior_mode

    # BehaviorEngine enrichi
    if behavior_engine:
        try:
            user_state = UserState(
                emotion=detected["behavior_emotion"],
                intensity=detected["intensity"],
                intent=behavior_mode,
                fatigue_level=detected["fatigue"],
                stress_level=(
                    detected["intensity"]
                    if detected["behavior_emotion"] == "stress"
                    else 0.0
                ),
            )

            decision = behavior_engine.decide_behavior(
                user_state=user_state,
                user_message=user_input,
            )

            context["adaptation"]["mode"] = decision.mode
            context["adaptation"]["tone"] = decision.tone
            context["user_state"] = user_state

        except Exception as exc:
            print(f"  [AVERT behavior] {exc}")

    mode = context.get("adaptation", {}).get("mode", behavior_mode)
    
    response = generator.generate_response(
        user_message=user_input_for_llm,
        response_context=context,
    )
    return response, mode, emotion_label, energy_level


# =============================================================================
# 10. MAIN LOOP
# =============================================================================

def main() -> None:
    from src.conversation.input.context_builder import get_time_context

    components = init_components()
    memory = components["memory"]
    user_name = components.get("user_name", USER_FALLBACK_NAME)
    llm_available = components.get("llm") is not None

    try:
        memory_summary = memory.get_session_summary() if memory else "mémoire indisponible"
    except Exception:
        memory_summary = "mémoire indisponible"

    banner(user_name, memory_summary, llm_available)
    print_help()

    from src.conversation.input.input_manager import HybridInputManager
    
    # Accueil vocal automatique
    try:
        tts = components.get("tts")
        if tts and components.get("voice_enabled"):
            tts.speak(f"Bonjour {user_name}. Alfred est lancé. Je t'écoute.")
    except Exception as exc:
        print(f"  [AVERT TTS accueil] {exc}")

    while True:
        try:
            raw_input = input("  Toi ⌨️ : ").strip()

        except (KeyboardInterrupt, EOFError):
            print(f"\n\n  {ALFRED_NAME} : À bientôt, {user_name}.\n")
            break

        if not raw_input:
            continue

        cmd = raw_input.lower().strip()

        if cmd in {"exit", "quit", "au revoir", "bye", "quitter"}:
            print(f"\n  {ALFRED_NAME} : À bientôt, {user_name}.\n")
            break

        if handle_command(cmd, components):
            continue

        user_input = sanitize_input(raw_input)
        if not user_input:
            continue

        try:
            time_ctx = get_time_context()

            response, mode, emotion_label, energy_level = build_response(
                user_input=user_input,
                components=components,
                time_ctx=time_ctx,
            )

            print(
                f"  [mode: {mode} | émotion: {emotion_label} | "
                f"énergie: {time_ctx.get('energy_level', energy_level)}]"
            )
            print(f"\n  {ALFRED_NAME} : {response}\n")

            # 🔊 TTS
            try:
                tts = components.get("tts")
                if tts and components.get("voice_enabled"):
                    tts.speak(clean_for_tts(response))
            except Exception as exc:
                print(f"  [AVERT TTS] {exc}")

            # 💾 mémoire JSON
            try:
                memory.save_exchange(
                    user_message=user_input,
                    alfred_response=response,
                    mode=mode,
                    emotion=emotion_label,
                    energy=energy_level,
                )
            except Exception as exc:
                print(f"  [AVERT mémoire JSON] {exc}")

            # 🧠 mémoire long terme
            try:
                ltm = components.get("ltm")
                if components.get("ltm_ok") and ltm:
                    ltm.save_exchange(
                        session_id=components.get("session_id", "unknown"),
                        user_input=user_input,
                        alfred_response=response,
                        intent="general",
                        emotion=emotion_label,
                        topic=mode,
                        importance=0.5,
                    )
            except Exception as exc:
                print(f"  [AVERT mémoire LTM] {exc}")

        except (KeyboardInterrupt, EOFError):
            print(f"\n\n  {ALFRED_NAME} : À bientôt, {user_name}.\n")
            break


# =============================================================================
# 11. ENTREE PROGRAMME
# =============================================================================

if __name__ == "__main__":
    main()