# -*- coding: utf-8 -*-
from __future__ import annotations

"""
PROJECT      : ALFRED — main.py V1.2 + mémoire long terme + Bloc 20 Zero Trust
BLOCK        : GLOBAL
FILE         : main.py
ROLE         : Point d'entrée principal ALFRED — pipeline conversation V1.2
AUTHOR       : Cognitive Products Lab
VERSION      : V1.2
STATUS       : VALIDATED

Objectif :
  Conserver la V1 actuelle fonctionnelle, tout en préparant proprement la V2.

Ce fichier garde :
  - Pipeline conversation texte
  - PersonalityAdapter
  - ResponseGenerator
  - AlfredBehaviorEngine
  - KnowledgeLoader
  - MemoryEngine JSON existant
  - Ollama optionnel
  - Détection émotion + wellbeing + mode B03

Ce fichier ajoute :
  - sanitize_input()
  - commandes : exit / memoire / memoire_ltm / mode / stats / ltm_stats / reset / statut
  - affichage plus propre
  - mode dégradé contrôlé si Ollama indisponible
  - architecture d'import unique en src.*
  - branchement optionnel de src.memory.long_term_memory

Ce fichier NE branche PAS encore :
  - SpeechManager
  - micro
  - haut-parleur

Ce fichier branche maintenant :
  - mémoire long terme SQLite existante via src.memory.long_term_memory

Pourquoi ?
  Parce qu'une V1 stable vaut mieux qu'une V3 qui fait du trampoline dans les imports.

Usage :
  cd D:/PROJET_ALFRED/ALFRED_PC
  python src/main.py
"""

import sys
import time
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
USER_ID = "celine"   # identifiant onboarding — correspond aux fichiers data/profile/personality_celine.json

# ─────────────────────────────────────────────────────────────────────────────
# Modèle Ollama actif — changer ici pour switcher
#
#   "llama3.2"   → actuel, léger
#   "mistral:7b" → recommandé (meilleur en français)
#   "phi3:mini"  → ultra-rapide (conversationnel léger)
#
# Pré-requis : ollama pull <modele>
# ─────────────────────────────────────────────────────────────────────────────
MODEL = "llama3.2"   # mistral:7b trop lent sans GPU → llama3.2 recommandé sur CPU

MAX_INPUT_LENGTH = 2000
MAX_MEMORY_CONTEXT = 8
VOICE_RECORD_SECONDS = 10

_whisper_model = None  # singleton — chargé une seule fois


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
# 4. UTILITAIRES TEXTE / SECURITE — Bloc 20 Zero Trust
# =============================================================================

def sanitize_input(text: str) -> str:
    """
    Nettoie l'entrée utilisateur (fallback si Bloc 20 indisponible).
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


def security_check(raw_input: str) -> str:
    """
    Passe l'entrée par la chaîne Zero Trust (Bloc 20).
    Retourne l'input nettoyé si autorisé, chaîne vide si refusé.
    Fallback sur sanitize_input() si le module sécurité est indisponible.
    """

    cleaned = sanitize_input(raw_input)

    if not cleaned:
        return ""

    try:
        from src.security.zero_trust_orchestrator import (
            quick_authorize_owner_local,
        )

        result = quick_authorize_owner_local(cleaned)

        if not result.get("authorized", False):
            reason = result.get("reason", "refus")

            if reason == "Appareil non reconnu ou non fiable":
                return cleaned

            print(f"  [SECURITE] Requête bloquée : {reason}")
            return ""

        return result.get("cleaned_input", cleaned)

    except Exception:
        return cleaned

def _safe_decrypt(value: str, fallback: str = USER_FALLBACK_NAME) -> str:
    """
    Déchiffre un token Fernet si détecté, retourne la valeur brute sinon.
    Utilisé pour lire les champs chiffrés des profils utilisateur.
    """
    if not isinstance(value, str) or not value.startswith("gAAAAA"):
        return value or fallback
    try:
        from src.security.encryption_service import decrypt
        return decrypt(value) or fallback
    except Exception:
        return fallback


_MEMORY_TRIGGERS = [
    "mémorise", "memorise", "mémoriser",
    "retiens que", "retiens :",
    "souviens-toi que", "souviens toi que",
    "n'oublie pas que", "noublie pas que",
    "enregistre cette", "enregistre que",
    "note que", "note cette",
    "garde en mémoire", "garde en memoire",
]

_PREFS_FILE      = ROOT / "data" / "preferences_profile.json"
_PRIVATE_PROFILE = ROOT / "private_data" / "user_profiles" / "celine_profile.json"
_PRIVATE_HOUSEHOLD = ROOT / "private_data" / "user_profiles" / "household_relationships.json"


def _detect_and_save_preference(user_input: str) -> str | None:
    """
    Détecte si l'utilisateur veut qu'ALFRED mémorise quelque chose.
    Si oui, sauvegarde dans preferences_profile.json et retourne le contenu sauvegardé.
    Retourne None si ce n'est pas une demande de mémorisation.
    """
    import json as _json
    import uuid as _uuid
    from datetime import datetime as _dt

    lower = user_input.lower()
    triggered = any(t in lower for t in _MEMORY_TRIGGERS)
    if not triggered:
        return None

    # Extraire le contenu à mémoriser
    content = user_input.strip()
    for prefix in [
        "mémorise cette information :", "mémorise cette information",
        "memorise cette information :", "memorise cette information",
        "mémorise :", "mémorise que", "mémoriser que",
        "retiens que", "retiens :",
        "souviens-toi que", "souviens toi que",
        "n'oublie pas que", "noublie pas que",
        "enregistre cette information :", "enregistre que",
        "note que", "note :", "note cette information :",
        "garde en mémoire que", "garde en memoire que",
        "mémorise", "memorise",
    ]:
        idx = lower.find(prefix)
        if idx != -1:
            content = user_input[idx + len(prefix):].strip(" :–-")
            break

    if not content or len(content) < 5:
        return None

    # Charger le fichier existant
    try:
        data = _json.loads(_PREFS_FILE.read_text(encoding="utf-8"))
    except Exception:
        data = {"_meta": {}, "preferences": []}

    if not isinstance(data.get("preferences"), list):
        data["preferences"] = []

    entry = {
        "id":        str(_uuid.uuid4())[:8],
        "content":   content,
        "timestamp": _dt.now().isoformat(),
        "source":    "user_explicit",
    }
    data["preferences"].append(entry)

    try:
        _PREFS_FILE.write_text(
            _json.dumps(data, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        print(f"  [🧠 Mémoire] Préférence enregistrée : {content[:80]}")
    except Exception as exc:
        print(f"  [AVERT mémoire] Impossible de sauvegarder : {exc}")
        return None

    return content


def _load_preferences() -> list[dict]:
    """Charge les préférences utilisateur depuis preferences_profile.json."""
    import json as _json
    try:
        data = _json.loads(_PREFS_FILE.read_text(encoding="utf-8"))
        prefs = data.get("preferences", [])
        return [p for p in prefs if isinstance(p, dict) and p.get("content")]
    except Exception:
        return []


def _load_user_profile_context() -> str:
    """
    Charge celine_profile.json et household_relationships.json pour injection
    dans le prompt LLM. Retourne un bloc texte résumé, ou '' si absent.
    """
    import json as _json
    lines = []
    try:
        data = _json.loads(_PRIVATE_PROFILE.read_text(encoding="utf-8"))
        u = data.get("user_profile", {})
        name = u.get("display_name", "Céline")
        identity = u.get("identity", {})
        lines.append(f"[Profil utilisateur principal : {name}]")
        for k, v in list(identity.items())[:12]:
            if isinstance(v, (str, int, float, bool)) and v:
                lines.append(f"- {k}: {v}")
    except Exception:
        pass
    try:
        data = _json.loads(_PRIVATE_HOUSEHOLD.read_text(encoding="utf-8"))
        members = data.get("household", {}).get("members", [])
        if members:
            lines.append("[Foyer]")
            for m in members:
                uid = m.get("user_id", "")
                role = m.get("role", "")
                rel = m.get("relationship_status", "")
                lines.append(f"- {uid} ({role}): {rel}")
    except Exception:
        pass
    return "\n".join(lines)


def clean_for_tts(text: str) -> str:
    replacements = {
        "**": "", "*": "",
        "’": "'", "‘": "'",
        """: '"', """: '"',
        "—": "-", "–": "-",
        "«": "", "»": "",
        "\U0001f449": "", "⚠️": "Attention.",
        "\U0001f9e0": "", "\U0001f3a4": "", "✅": "", "❌": "", "\U0001f525": "",
        "\U0001f504": "", "\U0001f4be": "", "\U0001f4c5": "", "\U0001f507": "", "\U0001f50a": "",
        "#": "", "##": "", "###": "",
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
    print("    onboarding                    → relancer la configuration personnalisee")
    print("    vocal                         → activer/désactiver le microphone")
    print("    son                           → activer/désactiver le son (TTS)")
    print("    ecoute                        → dicter un message une seule fois")
    print("    rappels                       → afficher les rappels actifs")
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
    reg = components.get("regulation_engine")
    uc  = components.get("user_adaptation_ctx")
    reg_label = "NON"
    if reg:
        if uc and uc.profile_complete:
            reg_label = f"OK — MBTI {uc.mbti_type or '?'} | {', '.join(uc.profiles_loaded)}"
        else:
            reg_label = "OK — pas de profil onboarding"
    print(f"  Pipeline B03/B13   : {reg_label}")
    print(f"  TTS Piper          : {'OK' if components.get('tts') else 'NON'}")
    print(f"  Son (TTS)          : {'COUPÉ 🔇' if components.get('tts_muted') else 'ACTIF 🔊'}")
    print(f"  Microphone         : {'ACTIF 🎤' if components.get('voice_enabled') else 'INACTIF'}")
    print("  LTM SQLite         : branchée si src.memory.long_term_memory est disponible")
    sec_ok = components.get("security_ok", False)
    sec_sid = components.get("security_session_id", "")
    if sec_ok and sec_sid:
        try:
            from src.security.session_manager import get_session
            sess = get_session("celine")
            if sess:
                elapsed = int(sess.get("elapsed_seconds", 0))
                valid_str = "valide" if sess.get("valid", False) else "expirée"
                sec_label = f"OK — session {sec_sid[:8]}... ({elapsed}s, {valid_str})"
            else:
                sec_label = f"OK — session {sec_sid[:8]}..."
        except Exception:
            sec_label = f"OK — session {sec_sid[:8]}..."
    else:
        sec_label = "NON"
    print(f"  Zero Trust B20     : {sec_label}")
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
    from src.knowledge.retrieval_engine import KnowledgeRetrievalEngine
    from src.memory.memory_engine import MemoryEngine
    from src.regulation.mode_manager import get_mode_manager
    from src.llm.llm_client_ollama import OllamaLLMClient
    from src.llm.llm_client_openai import OpenAILLMClient
    from src.llm.llm_router import LLMRouter
    from src.llm.llm_client_anthropic import AnthropicLLMClient
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
        "voice_enabled": False,   # vocal OFF au démarrage → taper "vocal" pour l'activer
        "retrieval_engine": None,
        "security_ok": False,
        "security_session_id": "",
        "output_filter": None,
        "fusion_engine": None,
        "proactive_engine": None,
        "avatar": None,
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
        raw_name = (
            adapter.user_profile
            .get("user_profile", {})
            .get("preferred_name", USER_FALLBACK_NAME)
        )
        components["user_name"] = _safe_decrypt(raw_name)
    except Exception as exc:
        print(f"  [ERREUR] PersonalityAdapter : {exc}")
        raise

    # BehaviorEngine optionnel mais important
    try:
        components["behavior_engine"] = AlfredBehaviorEngine(str(IDENTITY_PATH))
    except Exception as exc:
        print(f"  [AVERT] BehaviorEngine indisponible : {exc}")
        components["behavior_engine"] = None

    # =========================================================================
    # Knowledge Retrieval Engine (contient son propre KnowledgeLoader V2.0)
    # =========================================================================
    try:
        re = KnowledgeRetrievalEngine(
            project_root=str(ROOT),
            max_chars_per_knowledge=400,   # réduit pour LLM local (était 900)
        )
        components["retrieval_engine"] = re
        # Expose le loader interne pour le statut et les accès directs
        components["loader"] = re.loader
    except Exception as exc:
        print(f"  [AVERT] RetrievalEngine indisponible : {exc}")
        components["retrieval_engine"] = None
        components["loader"] = None

    # LLM Router : Ollama local -> OpenAI fallback -> fallback offline
    try:
        ollama = OllamaLLMClient(model=MODEL)

        try:
            openai = OpenAILLMClient(model="gpt-4o-mini")
        except Exception as exc:
            openai = None
            print(f"  [AVERT] OpenAI indisponible : {exc}")

        try:
            anthropic = AnthropicLLMClient(model="claude-haiku-4-5")
        except Exception as exc:
            anthropic = None
            print(f"  [AVERT] Anthropic indisponible : {exc}")

        components["llm"] = LLMRouter(
            primary=ollama,
            secondary=openai,
            tertiary=anthropic,
            allow_cloud_fallback=True,
            debug=True,
        )

        status = components["llm"].provider_status()
        print(f"DEBUG LLM Router : {status}")

    except Exception as exc:
        print(f"  [AVERT] Aucun LLM disponible : {exc}")
        components["llm"] = None

    # TTS Piper CLI — init avant ResponseGenerator pour que tts_available soit correct
    try:
        from src.conversation.output.tts_engine import TTSEngine
        from src.conversation.output.tts_piper import PiperTTS

        components["tts"] = TTSEngine(
            backend=PiperTTS(mode="complicite", blocking=True)
        )
    except Exception as exc:
        print(f"  [AVERT] TTS Piper indisponible : {exc}")
        components["tts"] = None

    # ResponseGenerator
    try:
        components["generator"] = ResponseGenerator(
            llm_client=components["llm"],
            debug=False,
            tts_available=components.get("tts") is not None,
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

    # =========================================================================
    # Blocs 03 + 13 — Pipeline émotionnel & santé + profil utilisateur
    # =========================================================================
    try:
        from src.regulation.regulation_engine import get_regulation_engine
        from src.health.profile_loader import get_user_context
        components["regulation_engine"]  = get_regulation_engine()
        components["user_adaptation_ctx"] = get_user_context(USER_ID)
        uc = components["user_adaptation_ctx"]
        if uc.profile_complete:
            print(f"  [B03/B13] Pipeline actif — profil chargé (MBTI: {uc.mbti_type or '?'}, "
                  f"santé: {'oui' if uc.health_active else 'non'}, "
                  f"profils: {', '.join(uc.profiles_loaded)})")
        else:
            print("  [B03/B13] Pipeline actif — aucun profil onboarding (lancez l'onboarding)")
    except Exception as exc:
        print(f"  [AVERT] Pipeline B03/B13 indisponible : {exc}")
        components["regulation_engine"]   = None
        components["user_adaptation_ctx"] = None

    # Onboarding — proposer si aucun profil personnalité détecté
    try:
        from paths import DATA_PROFILE
        pers_file = DATA_PROFILE / f"personality_{USER_ID}.json"
        components["_onboarding_pending"] = not pers_file.exists()
        if components["_onboarding_pending"]:
            print("\n  [ALFRED] Premiere utilisation detectee.")
            print("  Pour personnaliser ALFRED, tapez 'onboarding' dans la conversation.")
            try:
                from src.ui.alfred_app import set_ui_response
                set_ui_response(
                    "👋 Première utilisation détectée !\n"
                    "Tape 'onboarding' pour me personnaliser "
                    "(prénom, préférences, profil)."
                )
            except Exception:
                pass
    except Exception:
        components["_onboarding_pending"] = False

    # =========================================================================
    # Bloc 20 — Zero Trust Security
    # =========================================================================
    try:
        from src.security.device_registry import init_default_device
        from src.security.session_manager import create_session
        from src.security.output_filter import filter_output, analyze_output
        from src.security.zero_trust_orchestrator import build_security_context

        init_default_device("local_pc")
        sec_session_id = create_session("celine", "local_pc", "OWNER")
        components["security_ok"] = True
        components["security_session_id"] = sec_session_id
        components["output_filter"] = filter_output
        components["analyze_output"] = analyze_output
        components["security_context"] = build_security_context(
            "celine", "OWNER", "local_pc", sec_session_id
        )
        print(f"  [SÉCURITÉ] Zero Trust actif — session {sec_session_id[:8]}...")

        # SOC Monitor — watchdog daemon (cycle toutes les 5 min)
        try:
            from src.security.soc_monitor import start_watchdog
            start_watchdog(interval_seconds=300)
            print("  [SÉCURITÉ] SOC watchdog démarré (intervalle 5 min)")
        except Exception as exc_soc:
            print(f"  [AVERT] SOC watchdog indisponible : {exc_soc}")

    except Exception as exc:
        print(f"  [AVERT] Bloc 20 sécurité indisponible : {exc}")
        components["security_ok"] = False
        components["security_session_id"] = ""
        components["output_filter"] = None

    # =========================================================================
    # B11 — Fusion multi-signaux + Moteur proactif + Rappels
    # =========================================================================
    try:
        from src.v3.fusion.multi_signal_fusion_engine import MultiSignalFusionEngine
        from src.v3.proactive.proactive_engine import ProactiveEngine
        from src.v3.proactive.reminder_engine import ReminderEngine
        components["fusion_engine"]   = MultiSignalFusionEngine()
        components["proactive_engine"] = ProactiveEngine()
        components["reminder_engine"] = ReminderEngine()
        print("  [B11] Fusion multi-signaux + Proactif + Rappels actifs.")
    except Exception as exc:
        print(f"  [AVERT] B11 fusion/proactif indisponible : {exc}")

    # =========================================================================
    # B15 — Avatar Engine (headless V1 — renderer Kivy connecté par alfred_app)
    # =========================================================================
    try:
        from src.ui.avatar_engine import get_avatar_engine
        components["avatar"] = get_avatar_engine(headless=True)
        print("  [B15] Avatar Engine actif (headless).")
    except Exception as exc:
        print(f"  [AVERT] B15 avatar indisponible : {exc}")

    # =========================================================================
    # B05 — Auth V1 : auto-login local
    # =========================================================================
    try:
        from src.auth.login_handler import start_auto_session
        auth_sid = start_auto_session(user_id=USER_ID, role="OWNER")
        components["auth_session_id"] = auth_sid
        print(f"  [B05] Auth : session locale démarrée ({auth_sid[:8] if auth_sid else 'N/A'}...)")
    except Exception as exc:
        print(f"  [AVERT] B05 Auth indisponible : {exc}")
        components["auth_session_id"] = ""

    # =========================================================================
    # V2 — Fusion + Confidence + Decision (mode passif — enrichit la réponse)
    # =========================================================================
    try:
        from src.v2.fusion.fusion_engine import get_fusion_engine
        from src.v2.confidence.confidence_scorer import get_confidence_scorer
        from src.v2.decision.decision_engine import get_decision_engine
        components["v2_fusion"]     = get_fusion_engine()
        components["v2_confidence"] = get_confidence_scorer()
        components["v2_decision"]   = get_decision_engine()
        print("  [V2] Fusion + Confidence + Decision actifs.")

        # Brancher le ConfidenceScorer V2 dans le ResponseGenerator
        gen = components.get("generator")
        if gen is not None:
            gen.confidence_scorer = components["v2_confidence"]
            print("  [V2] ConfidenceScorer branché dans ResponseGenerator.")
    except Exception as exc:
        print(f"  [AVERT] V2 intelligence indisponible : {exc}")
        components["v2_fusion"]     = None
        components["v2_confidence"] = None
        components["v2_decision"]   = None

    # =========================================================================
    # B04 — VisionAnalyzer (monitoring caméra + analyse d'image)
    # =========================================================================
    try:
        from src.vision.vision_analyzer import VisionAnalyzer
        components["vision_analyzer"] = VisionAnalyzer()
        llava_ok = components["vision_analyzer"].is_vision_available()
        cv2_ok   = components["vision_analyzer"].is_opencv_available()
        print(f"  [B04] VisionAnalyzer actif (llava: {'✓' if llava_ok else '✗'}, "
              f"OpenCV: {'✓' if cv2_ok else '✗'})")
        # Snapshot headless (mode main.py sans Kivy)
        snap_fn = _make_headless_snapshot_fn(camera_index=0)
        components["_vision_snapshot_fn"] = snap_fn
    except Exception as exc:
        print(f"  [AVERT] B04 VisionAnalyzer indisponible : {exc}")
        components["vision_analyzer"] = None
        components["_vision_snapshot_fn"] = None

    return components




# =============================================================================
# 8. COMMANDES SPECIALES
# =============================================================================

def _get_whisper_model():
    """Charge le modèle Whisper une seule fois (singleton)."""
    global _whisper_model
    if _whisper_model is None:
        import warnings
        from faster_whisper import WhisperModel
        warnings.filterwarnings("ignore", category=RuntimeWarning, module="faster_whisper")
        _whisper_model = WhisperModel("small", compute_type="int8")
    return _whisper_model


def listen_voice_once(duration: int = VOICE_RECORD_SECONDS, silent: bool = False) -> str:
    """
    Capture le micro pendant quelques secondes et retourne le texte transcrit.
    V1 améliorée : écoute plus longue + Whisper small + réglages anti-hallucination.
    """
    import warnings
    import sounddevice as sd
    import numpy as np

    warnings.filterwarnings("ignore", category=RuntimeWarning, message=".*overflow.*")
    warnings.filterwarnings("ignore", category=RuntimeWarning, message=".*invalid value.*")

    samplerate = 16000

    if not silent:
        print(f"  🎤 Écoute pendant {duration} secondes...", end="\r")

    audio = sd.rec(
        int(duration * samplerate),
        samplerate=samplerate,
        channels=1,
        dtype="float32",
    )
    sd.wait()

    audio = np.squeeze(audio)

    if not silent:
        print("  🧠 Transcription...")

    model = _get_whisper_model()

    segments, _ = model.transcribe(
        audio,
        language="fr",
        beam_size=5,
        vad_filter=True,
        vad_parameters={"min_silence_duration_ms": 500},
        temperature=0.0,
        initial_prompt="Alfred, assistant personnel. Conversation en français.",
        no_speech_threshold=0.6,
        log_prob_threshold=-0.8,
    )

    text = " ".join(segment.text.strip() for segment in segments).strip()

    # Filtre hallucinations Whisper :
    # - texte vide ou trop court
    # - moins de 30% de lettres (ex: ")))))))", "...", bruits encodés)
    # - répétition excessive d'un même caractère
    if not text or len(text) < 3:
        return ""

    alpha_ratio = sum(c.isalpha() or c.isspace() for c in text) / len(text)
    if alpha_ratio < 0.4:
        return ""

    # Détecte répétition de caractère non-alphabétique (ex: ")))))))))")
    for char in set(text):
        if not char.isalpha() and text.count(char) > len(text) * 0.3:
            return ""

    return text

# =============================================================================
# B04 — Helpers vision
# =============================================================================

def _alfred_speak(text: str, components: dict[str, Any]) -> None:
    """Affiche et vocalise un message ALFRED (utilisé par les callbacks vision)."""
    print(f"\n  [ALFRED] {text}\n")
    tts = components.get("tts")
    if tts and not components.get("tts_muted", False):
        try:
            tts.speak(text)
        except Exception:
            pass
    try:
        from src.ui.alfred_app import set_ui_response
        set_ui_response(text)
    except Exception:
        pass


def _on_vision_alert(event, components: dict[str, Any]) -> None:
    """
    Callback appelé par VisionAnalyzer.start_monitoring() sur chaque VisionEvent.

    - expression  → stocke l'émotion pour que le pipeline adapte son ton
    - motion info → log silencieux uniquement
    - warning     → affiche une notification
    - critical    → ALFRED parle immédiatement (chute / urgence)
    """
    from src.vision.vision_analyzer import VisionEvent

    if event.type == "expression":
        # Mise à jour silencieuse de l'émotion visuelle détectée
        components["_last_vision_emotion"] = event.emotion_hint
        return

    if event.severity == "info":
        return  # mouvement modéré : log silencieux

    if event.severity == "warning":
        print(f"\n  [B04] ⚠ {event.description}\n")
        return

    if event.severity == "critical":
        # Chute / urgence → ALFRED intervient vocalement sans attendre la saisie
        msg = (
            "Céline, je t'ai vue tomber ! Es-tu blessée ? "
            "Réponds-moi ou appelle les secours si nécessaire."
        )
        _alfred_speak(msg, components)
        print(f"\n  [B04] 🚨 URGENCE — {event.description}\n")


def _make_headless_snapshot_fn(camera_index: int = 0):
    """
    Crée une snapshot_fn pour main.py (sans Kivy).
    Ouvre cv2.VideoCapture une seule fois en lazy init.
    Retourne une fonction () -> Optional[str] (JPEG base64).
    """
    try:
        import cv2, base64
    except ImportError:
        return None

    _state = {"cap": None}

    def snapshot() -> str | None:
        if _state["cap"] is None:
            backend = cv2.CAP_DSHOW if hasattr(cv2, "CAP_DSHOW") else cv2.CAP_ANY
            cap = cv2.VideoCapture(camera_index, backend)
            if not cap.isOpened():
                return None
            _state["cap"] = cap
        ret, frame = _state["cap"].read()
        if not ret or frame is None:
            return None
        ok, buf = cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, 75])
        if not ok:
            return None
        return base64.b64encode(buf.tobytes()).decode("ascii")

    return snapshot


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

    if cmd in {"onboarding", "configuration", "profil", "questionnaire"}:
        try:
            from src.health.onboarding import run_full_onboarding
            from src.health.profile_loader import invalidate_cache
            print("\n  Lancement du parcours de configuration personnalisée...\n")
            paths = run_full_onboarding(user_id=USER_ID)
            if paths:
                invalidate_cache(USER_ID)
                # Recharger le contexte dans les composants
                from src.health.profile_loader import get_user_context
                components["user_adaptation_ctx"] = get_user_context(USER_ID, force_reload=True)
                print("  Profil rechargé dans le pipeline.")
        except Exception as exc:
            print(f"\n  [ERREUR onboarding] {exc}\n")
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

        # Démarrer ou arrêter HybridInputManager selon l'état
        if components["voice_enabled"]:
            if not components.get("_hybrid"):
                try:
                    from src.conversation.input.input_manager import HybridInputManager
                    h = HybridInputManager(voice_func=lambda: listen_voice_once(silent=True))
                    h.start()
                    components["_hybrid"] = h
                    print("  Mode vocal hybride démarré.")
                except Exception as exc:
                    print(f"  [AVERT] HybridInputManager indisponible : {exc}")
        else:
            h = components.get("_hybrid")
            if h:
                try:
                    h.stop()
                except Exception:
                    pass
                components["_hybrid"] = None

        print(f"\n  Mode vocal {state}.\n")

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

    if cmd == "son":
        tts = components.get("tts")
        if not tts:
            print("\n  TTS Piper non disponible sur cette session.\n")
            return True

        # Toggle : on stocke l'état dans components
        son_actif = not components.get("tts_muted", False)
        components["tts_muted"] = son_actif   # True = muet
        state = "coupé" if son_actif else "activé"
        print(f"\n  Son {state}.\n")
        return True

    # ── B04 Vision — commandes explicites ─────────────────────────────────────
    _VISION_SCENE_TRIGGERS = {
        "regarde", "qu'est-ce que tu vois", "que vois-tu",
        "décris ce que tu vois", "dis-moi ce que tu vois",
    }
    _VISION_EXPR_TRIGGERS = {
        "mon expression", "comment j'ai l'air", "mon visage",
        "lis mon expression", "ma tête",
    }
    _VISION_MONITOR_ON  = {"surveille", "surveille-moi", "active surveillance"}
    _VISION_MONITOR_OFF = {"arrête surveillance", "stop surveillance"}

    if any(t in cmd for t in _VISION_SCENE_TRIGGERS):
        va   = components.get("vision_analyzer")
        snap = components.get("_vision_snapshot_fn")
        if va and snap:
            frame_b64 = snap()
            if frame_b64:
                event = va.describe_scene(frame_b64)
                _alfred_speak(event.description, components)
            else:
                print("\n  [B04] Aucune frame — active la caméra d'abord (📷).\n")
        else:
            print("\n  [B04] Caméra ou VisionAnalyzer non disponible.\n")
        return True

    if any(t in cmd for t in _VISION_EXPR_TRIGGERS):
        va   = components.get("vision_analyzer")
        snap = components.get("_vision_snapshot_fn")
        if va and snap:
            frame_b64 = snap()
            if frame_b64:
                event = va.analyze_expression(frame_b64)
                components["_last_vision_emotion"] = event.emotion_hint
                _alfred_speak(event.description, components)
            else:
                print("\n  [B04] Aucune frame — active la caméra d'abord.\n")
        else:
            print("\n  [B04] Caméra ou VisionAnalyzer non disponible.\n")
        return True

    if any(t in cmd for t in _VISION_MONITOR_ON):
        va   = components.get("vision_analyzer")
        snap = components.get("_vision_snapshot_fn")
        if va and snap:
            if not va.is_monitoring:
                va.start_monitoring(
                    snapshot_fn=snap,
                    on_alert=lambda e: _on_vision_alert(e, components),
                    interval_s=2.0,
                    expression_interval_s=30.0,
                )
                print("\n  [B04] Surveillance caméra activée.\n")
                _alfred_speak("Je surveille maintenant via la caméra.", components)
            else:
                print("\n  [B04] Surveillance déjà active.\n")
        else:
            print("\n  [B04] Caméra ou VisionAnalyzer non disponible.\n")
        return True

    if any(t in cmd for t in _VISION_MONITOR_OFF):
        va = components.get("vision_analyzer")
        if va and va.is_monitoring:
            va.stop_monitoring()
            print("\n  [B04] Surveillance arrêtée.\n")
            _alfred_speak("Surveillance arrêtée.", components)
        return True

    if cmd in {"rappels", "rappel"}:
        re_engine = components.get("reminder_engine")
        if not re_engine:
            print("\n  Module rappels non disponible.\n")
            return True
        actifs = re_engine.get_active()
        if not actifs:
            print("\n  Aucun rappel enregistré.\n")
        else:
            print(f"\n  ── {len(actifs)} rappel(s) actif(s) ──")
            for r in actifs:
                due = r.due_at[:10] if r.due_at else "?"
                print(f"  [{r.id}] {due}  {r.title}")
            print()
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
    on_sentence=None,
) -> tuple[str, str, str, str]:
    """
    Construit la réponse ALFRED.

    Retourne :
      response, mode, emotion_label, energy_level
    """
    from src.core.alfred_behavior_engine import UserState
    from src.memory.memory_answer_engine import answer_from_memory

    adapter = components["adapter"]
    behavior_engine = components["behavior_engine"]
    generator = components["generator"]

    # -------------------------------------------------------------------------
    # 0. Pipeline Blocs 03 + 13 (process_message unifié)
    # -------------------------------------------------------------------------
    pipeline_ctx  = None
    pipeline_guidelines = ""
    forced_resp   = None

    regulation_engine = components.get("regulation_engine")
    user_adaptation   = components.get("user_adaptation_ctx")

    if regulation_engine:
        try:
            from src.core.pipeline_bridge import (
                enrich_context_with_pipeline,
                get_pipeline_mode_guidelines,
                get_forced_response,
            )
            pipeline_ctx = regulation_engine.process(
                user_input=user_input,
                time_context=time_ctx,
                user_context=user_adaptation,
            )
            pipeline_guidelines = get_pipeline_mode_guidelines(pipeline_ctx)
            forced_resp = get_forced_response(pipeline_ctx)

            # Court-circuit : protection ou crise santé → réponse directe
            if forced_resp:
                return forced_resp, "support_mode", pipeline_ctx.emotion, "low"

        except Exception as exc:
            print(f"  [AVERT] Pipeline B03/B13 : {exc}")
            pipeline_ctx = None

    # -------------------------------------------------------------------------
    # 1. Détection contexte B03 (fallback si pipeline indisponible)
    # -------------------------------------------------------------------------
    detected = detect_context(user_input, time_ctx)

    emotion_state = detected["emotion_state"]
    emotion_label = (
        pipeline_ctx.emotion
        if pipeline_ctx
        else safe_getattr(emotion_state, "emotion", "neutral")
    )
    behavior_mode = detected["behavior_mode"]
    energy_level = "low" if detected["fatigue"] > 0.5 else "medium"

    # B04 — Émotion visuelle (analyse expression caméra) enrichit l'émotion détectée
    vision_emotion = components.get("_last_vision_emotion", "")
    _VISION_TO_ALFRED_EMOTION = {
        "fatigue":   ("fatigue", "low"),
        "stress":    ("stress", "medium"),
        "tristesse": ("sadness", "medium"),
        "joie":      ("joy", "medium"),
        "neutre":    ("", ""),
    }
    if vision_emotion and vision_emotion in _VISION_TO_ALFRED_EMOTION:
        v_emo, v_energy = _VISION_TO_ALFRED_EMOTION[vision_emotion]
        if v_emo and not detected.get("behavior_emotion"):
            detected["behavior_emotion"] = v_emo
        if v_energy == "low":
            energy_level = "low"

    # -------------------------------------------------------------------------
    # 1b. B11 — Fusion multi-signaux (NLP + émotion + contexte)
    # -------------------------------------------------------------------------
    fusion_engine = components.get("fusion_engine")
    if fusion_engine:
        try:
            nlp_raw = detected.get("nlp") or {}
            fused = fusion_engine.fuse(
                nlp_signal={
                    "intent": nlp_raw.get("intent", "general"),
                    "confidence": nlp_raw.get("confidence", 0.5),
                } if nlp_raw else None,
                emotion_signal={
                    "emotion": emotion_label,
                    "intensity": detected.get("intensity", 0.0),
                },
                context_signal={
                    "energy_level": energy_level,
                    "period": time_ctx.get("period", ""),
                },
            )
            if fused.confidence >= 0.4:
                behavior_mode = fused.recommended_mode
            components["_last_fused"] = fused
        except Exception:
            pass

    # -------------------------------------------------------------------------
    # 2. Construction contexte PersonalityAdapter (avec profil onboarding)
    # -------------------------------------------------------------------------
    context = adapter.build_response_context(
        user_message=user_input,
        detected_emotion=detected["behavior_emotion"],
        energy_level=energy_level,
        user_adaptation=user_adaptation,   # MBTI + préférences comm + frontières
    )

    # Fusion PipelineContext → response_context (mode santé, ton, règles)
    if pipeline_ctx:
        try:
            enrich_context_with_pipeline(context, pipeline_ctx)
        except Exception as exc:
            print(f"  [AVERT] pipeline_bridge : {exc}")

    # -------------------------------------------------------------------------
    # 3. Mémoire long terme SQLite
    # -------------------------------------------------------------------------
    try:
        ltm = components.get("ltm")
        if components.get("ltm_ok") and ltm:
            recent_memories = ltm.get_recent_memories(n=3)   # réduit pour LLM local

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

    context["memory_context"] = memory_context

    # -------------------------------------------------------------------------
    # 3a. Profil utilisateur privé (celine_profile + household)
    # -------------------------------------------------------------------------
    try:
        user_profile_ctx = _load_user_profile_context()
        context["user_profile_context"] = user_profile_ctx
    except Exception:
        context["user_profile_context"] = ""

    # -------------------------------------------------------------------------
    # 3b. Préférences utilisateur explicites
    # -------------------------------------------------------------------------
    try:
        prefs = _load_preferences()
        if prefs:
            pref_lines = ["[Préférences et instructions permanentes de l'utilisateur]"]
            for p in prefs[-20:]:   # max 20 entrées
                pref_lines.append(f"- {p['content']}")
            context["user_preferences"] = "\n".join(pref_lines)
        else:
            context["user_preferences"] = ""
    except Exception:
        context["user_preferences"] = ""

    # -------------------------------------------------------------------------
    # 4. Knowledge Retrieval Engine B18
    # -------------------------------------------------------------------------
    retrieval_engine = components.get("retrieval_engine")
    knowledge_context = ""

    if retrieval_engine:
        try:
            retrieval_result = retrieval_engine.retrieve(
                query=user_input,
                conversation_context={
                    "mode": behavior_mode,
                    "emotion": emotion_label,
                    "energy": energy_level,
                },
            )

            knowledge_context = retrieval_result.prompt_block

            context["knowledge_context"] = knowledge_context
            context["knowledge_ids"] = retrieval_result.knowledge_ids
            context["knowledge_domains"] = retrieval_result.domains

            # Debug retrieval — affiche les knowledges chargés
            if retrieval_result.knowledge_ids:
                print(f"  [B18] {len(retrieval_result.knowledge_ids)} knowledge(s) chargé(s) :")
                for kid in retrieval_result.knowledge_ids:
                    print(f"        → {kid}")
            else:
                print("  [B18] Aucun knowledge récupéré pour cette requête.")

        except Exception as exc:
            print(f"  [AVERT retrieval] {exc}")

    # -------------------------------------------------------------------------
    # 5. Contexte projet fixe
    # -------------------------------------------------------------------------
    project_context = """
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
- Knowledge Retrieval Engine B18 actif

Priorités :
- stabilité
- faible latence
- sécurité
- architecture scalable
- cohérence mémoire
"""
    context["project_context"] = project_context

    # -------------------------------------------------------------------------
    # 6. Réponse directe depuis mémoire si pertinent
    # -------------------------------------------------------------------------
    memory_answer = answer_from_memory(
        user_message=user_input,
        memory_context=memory_context,
    )

    if memory_answer:
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
            "knowledge",
            "json",
            "python",
            "code",
        ]

        if not any(word in user_input.lower() for word in technical_keywords):
            mode = "memory_mode"
            return memory_answer, mode, emotion_label, energy_level

    # -------------------------------------------------------------------------
    # 7. Override mode B03 -> BehaviorEngine
    # -------------------------------------------------------------------------
    context.setdefault("adaptation", {})
    context["adaptation"]["mode"] = behavior_mode

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
            context["_behavior_decision"] = decision   # stocké pour enrichissement V2

        except Exception as exc:
            print(f"  [AVERT behavior] {exc}")

    mode = context.get("adaptation", {}).get("mode", behavior_mode)

    # -------------------------------------------------------------------------
    # 7b. V2 Intelligence — Fusion + Confidence + Decision
    # -------------------------------------------------------------------------
    v2_fusion     = components.get("v2_fusion")
    v2_confidence = components.get("v2_confidence")
    v2_decision   = components.get("v2_decision")
    v2_result     = {}

    if v2_fusion and v2_confidence and v2_decision:
        try:
            # ── Correction bug : utiliser detected["behavior_emotion"] directement ──
            emotion_v2 = detected.get("behavior_emotion", "neutral")

            fusion = v2_fusion.fuse(
                memory_context=memory_context,
                knowledge_context=knowledge_context,
                user_message=user_input,
                emotion=emotion_v2,
                mode=mode,
            )

            # Pre-score sans response_text (réponse pas encore générée)
            # Le ResponseGenerator affinera le score avec le texte réel.
            confidence = v2_confidence.score(
                fusion_score=fusion.fusion_score,
                memory_coverage=1.0 if memory_context else 0.0,
                knowledge_coverage=1.0 if knowledge_context else 0.0,
                emotion=emotion_v2,
                mode=mode,
                response_text="",   # sera affiné dans ResponseGenerator
            )

            v2_dec = v2_decision.decide(
                confidence_score=confidence.score,
                confidence_level=confidence.level,
                fusion_score=fusion.fusion_score,
                primary_source=fusion.primary_source,
                emotion=emotion_v2,
                mode=mode,
                user_message=user_input,
                has_memory=bool(memory_context),
                has_knowledge=bool(knowledge_context),
                is_question="?" in user_input,
            )

            # ── Enrichir BehaviorDecision via apply_v2_decision() ────────────
            if behavior_engine:
                try:
                    decision_obj = context.get("_behavior_decision")
                    if decision_obj is not None:
                        enriched = behavior_engine.apply_v2_decision(
                            decision=decision_obj,
                            fusion_result=fusion,
                            decision_result=v2_dec,
                        )
                        # Sync : mettre à jour le tone si override V2
                        v2_tone_mapped = context["adaptation"].get("tone")
                        if enriched.metadata.get("v2_tone") and enriched.metadata["v2_tone"] != "neutral":
                            context["adaptation"]["tone"] = enriched.tone
                except Exception:
                    pass

            v2_result = {
                "fusion_score":      fusion.fusion_score,
                "confidence_score":  confidence.score,
                "confidence_level":  confidence.level,
                "strategy":          v2_dec.strategy.value,
                "should_hedge":      v2_dec.should_hedge,
                "hedge_prefix":      v2_dec.hedge_prefix,
                "post_actions":      v2_dec.post_actions,
                "merged_context":    fusion.merged_context,
            }
            context["v2"] = v2_result
            # Expose l'émotion détectée pour que le ConfidenceScorer du generator l'utilise
            context["detected_emotion"] = emotion_v2

        except Exception as exc_v2:
            pass   # V2 dégradé silencieusement — pipeline V1 continue

    # -------------------------------------------------------------------------
    # 8. Prompt enrichi envoyé au LLM
    # -------------------------------------------------------------------------
    user_input_for_llm = f"""
=== CONTEXTE PROJET ACTUEL ===

{project_context}

=== MÉMOIRE LONG TERME ===

{memory_context}

=== KNOWLEDGE RETRIEVAL B18 ===

{knowledge_context}

=== QUESTION UTILISATEUR ===

{user_input}
"""

    # -------------------------------------------------------------------------
    # 9. Génération réponse
    # -------------------------------------------------------------------------
    memory = components.get("memory")
    history_text = ""
    if memory:
        try:
            history_text = memory.format_context_for_prompt(3)   # réduit pour LLM local
        except Exception:
            history_text = ""

    response = generator.generate_response(
        user_message=user_input_for_llm,
        response_context=context,
        history_text=history_text,
        mode_guidelines=pipeline_guidelines,   # directives LLM B03+B13+MBTI
        on_sentence=on_sentence,
    )

    # ── V2 post-traitement : hedge prefix si confidence faible ────────────────
    if v2_result.get("should_hedge") and v2_result.get("hedge_prefix") and response:
        response = v2_result["hedge_prefix"] + response

    # ── V2 post-actions ───────────────────────────────────────────────────────
    for action in v2_result.get("post_actions", []):
        if action == "save_to_memory" and v2_result.get("confidence_score", 0) >= 0.6:
            pass  # déjà géré par le pipeline mémoire existant
        elif action == "track_wellbeing":
            pass  # déjà géré par B03/B13

    # -------------------------------------------------------------------------
    # 10. B11 — Suggestion proactive (après réponse LLM)
    # -------------------------------------------------------------------------
    proactive_engine = components.get("proactive_engine")
    if proactive_engine:
        try:
            suggestion = proactive_engine.check_and_suggest(
                context_signal={
                    "period": time_ctx.get("period", ""),
                    "energy_level": energy_level,
                },
                emotion_signal={
                    "emotion": emotion_label,
                    "intensity": detected.get("intensity", 0.0),
                },
                wellbeing_state=detected.get("wellbeing"),
            )
            components["_proactive_suggestion"] = suggestion
        except Exception:
            components["_proactive_suggestion"] = None

    # Expose les clés B03/B13 du context pour la boucle principale
    components["_last_check_in"]  = context.get("check_in_message") if isinstance(context, dict) else None
    components["_last_offer_pause"] = context.get("offer_pause", False) if isinstance(context, dict) else False

    return response, mode, emotion_label, energy_level


# =============================================================================
# 10. AUTHENTIFICATION AU DÉMARRAGE
# =============================================================================

_MAX_PIN_ATTEMPTS = 3
_AUTH_DONE = False


def _auth_already_done() -> bool:
    return _AUTH_DONE


def prompt_auth() -> bool:
    """
    Porte d'authentification PIN au démarrage d'ALFRED.

    - Aucun PIN enregistré → propose d'en créer un (skip autorisé pour la
      première utilisation afin de ne pas bloquer).
    - PIN enregistré → demande le PIN, 3 tentatives, exit si bloqué.

    Retourne True si l'accès est autorisé, False sinon.
    Met à jour _AUTH_DONE pour éviter un double appel depuis alfred_with_ui.py.
    """
    global _AUTH_DONE

    if _AUTH_DONE:
        return True

    import getpass
    from src.auth.authenticator import has_pin, register_pin, authenticate

    user_id = USER_ID

    print("\n  ── Authentification ALFRED ──")

    # ── Première utilisation : aucun PIN ──────────────────────────────────────
    if not has_pin(user_id):
        print("  Aucun code PIN enregistré pour cet utilisateur.")
        print("  Pour sécuriser ALFRED, vous pouvez créer un PIN maintenant.")
        choix = input("  Créer un PIN ? [o/N] : ").strip().lower()
        if choix in {"o", "oui", "y", "yes"}:
            while True:
                pin1 = getpass.getpass("  Nouveau PIN (4-32 caractères) : ")
                pin2 = getpass.getpass("  Confirmer le PIN : ")
                if pin1 != pin2:
                    print("  Les PINs ne correspondent pas. Recommencez.")
                    continue
                if register_pin(user_id, pin1):
                    print("  PIN enregistré avec succès.\n")
                    _AUTH_DONE = True
                    return True
                else:
                    print("  PIN invalide (longueur 4-32 chiffres/caractères). Recommencez.")
        else:
            print("  Démarrage sans PIN — pensez à en créer un (commande : pin).\n")
            _AUTH_DONE = True
            return True

    # ── PIN existant : demande vérification ───────────────────────────────────
    for attempt in range(1, _MAX_PIN_ATTEMPTS + 1):
        try:
            pin = getpass.getpass(f"  Code PIN ({attempt}/{_MAX_PIN_ATTEMPTS}) : ")
        except (KeyboardInterrupt, EOFError):
            print("\n  Authentification annulée.")
            return False

        result = authenticate(user_id, pin)
        if result["success"]:
            print("  Accès autorisé.\n")
            _AUTH_DONE = True
            return True

        reason = result.get("reason", "Échec")
        print(f"  {reason}.")

        if "Trop de tentatives" in reason or "bloqué" in reason.lower():
            break

    print("  Accès refusé. ALFRED ne peut pas démarrer.\n")
    return False


# =============================================================================
# 11. MAIN LOOP
# =============================================================================

def main() -> None:
    from src.conversation.input.context_builder import get_time_context
    from src.conversation.input.input_manager import HybridInputManager

    # prompt_auth() gère lui-même le flag _AUTH_DONE :
    # - lancé via alfred_with_ui.py → déjà validé avant Kivy, retourne True immédiatement
    # - lancé via main.py directement → demande le PIN ici
    if not prompt_auth():
        sys.exit(1)

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

    # ── Rappels dus au démarrage ───────────────────────────────────────────
    try:
        re_engine = components.get("reminder_engine")
        if re_engine:
            dus = re_engine.get_due_reminders()
            if dus:
                print(f"  ⏰ {len(dus)} rappel(s) arrivé(s) à échéance :")
                for r in dus:
                    print(f"     → {r.title}")
                print()
    except Exception as exc:
        print(f"  [AVERT] Vérification rappels indisponible : {exc}")

    # Initialisation HybridInputManager si mode vocal actif
    hybrid: HybridInputManager | None = None

    def _start_hybrid() -> HybridInputManager | None:
        try:
            h = HybridInputManager(voice_func=lambda: listen_voice_once(silent=True))
            h.start()
            print("  Mode vocal hybride actif — parle ou tape librement.")
            return h
        except Exception as exc:
            print(f"  [AVERT] HybridInputManager indisponible : {exc}")
            return None

    if components.get("voice_enabled"):
        hybrid = _start_hybrid()

    components["_hybrid"] = hybrid

    # ── Câblage callbacks audio → avatar (synchronisation haut-parleur) ──────
    # on_play_start / on_play_stop sont déclenchés par PiperTTS exactement
    # quand sd.play() démarre et quand sd.wait() revient — pas à l'écriture.
    _tts_backend = getattr(components.get("tts"), "backend", None)
    if _tts_backend and hasattr(_tts_backend, "on_play_start"):
        _avatar_cb = components.get("avatar")

        def _cb_play_start() -> None:
            if _avatar_cb:
                _avatar_cb.set_speaking(True)
            try:
                from src.ui.alfred_app import set_ui_speaking
                set_ui_speaking(True)
            except Exception:
                pass

        def _cb_play_stop() -> None:
            if _avatar_cb:
                _avatar_cb.on_tts_stop()   # respecte le verrou begin/end_response
            try:
                from src.ui.alfred_app import set_ui_speaking
                # SoundWave suit le même verrou : muet inter-phrases si réponse active
                if not (_avatar_cb and _avatar_cb._response_active):
                    set_ui_speaking(False)
            except Exception:
                pass

        _tts_backend.on_play_start = _cb_play_start
        _tts_backend.on_play_stop  = _cb_play_stop

    # Accueil vocal automatique
    try:
        tts = components.get("tts")
        if tts and components.get("voice_enabled"):
            msg = f"Bonjour {user_name}. Alfred est lancé."
            if hybrid:
                msg += " Mode vocal hybride actif."
            tts.speak(msg)
    except Exception as exc:
        print(f"  [AVERT TTS accueil] {exc}")

    def _read_input(prompt: str = "  Toi ⌨️ : ") -> str:
        """Lit l'input depuis la file UI (si active) ou le terminal."""
        try:
            from src.ui.ui_bridge import is_active as _ui_ok, wait_for_ui_input as _ui_get
            if _ui_ok():
                return _ui_get()
        except ImportError:
            pass
        return input(prompt).strip()

    while True:
        # B15 — Avatar : pret a ecouter
        _av = components.get("avatar")
        if _av:
            _av.set_listening(True)
        try:
            from src.ui.alfred_app import set_ui_input_enabled, set_ui_listening, set_ui_speaking
            set_ui_speaking(False)
            set_ui_listening(True)
            set_ui_input_enabled(True)
        except Exception:
            pass

        try:
            hybrid = components.get("_hybrid")
            voice_enabled = components.get("voice_enabled")

            # ── Vérifie d'abord si une transcription vocale est prête ──
            if hybrid and voice_enabled:
                voice_item = hybrid.get_voice_nowait()
                if voice_item:
                    source, raw_input = voice_item
                    if source == "voice":
                        print(f"\n  Toi 🎤 : {raw_input}")
                    elif source == "error":
                        print(f"  [AVERT vocal] {raw_input}")
                        continue
                    raw_input = (raw_input or "").strip()
                    if not raw_input:
                        continue
                else:
                    # Aucune voix en attente → UI ou clavier
                    raw_input = _read_input()
                    hybrid.last_keyboard_time = time.time()
            else:
                raw_input = _read_input()

        except (KeyboardInterrupt, EOFError):
            if components.get("security_ok"):
                try:
                    from src.security.session_manager import close_session
                    close_session("celine")
                except Exception:
                    pass
            print(f"\n\n  {ALFRED_NAME} : À bientôt, {user_name}.\n")
            break

        if not raw_input:
            continue

        cmd = raw_input.lower().strip()

        if cmd in {"exit", "quit", "au revoir", "bye", "quitter"}:
            h = components.get("_hybrid")
            if h:
                try:
                    h.stop()
                except Exception:
                    pass
            print(f"\n  {ALFRED_NAME} : À bientôt, {user_name}.\n")
            break

        if handle_command(cmd, components):
            # Si "ecoute" a transcrit un texte, le traiter comme une saisie utilisateur
            voice_text = components.pop("_voice_once_text", None)
            if voice_text:
                raw_input = voice_text
            else:
                continue

        user_input = security_check(raw_input)
        if not user_input:
            continue

        # ── Détection demandes de mémorisation ────────────────────────────
        _saved_pref = _detect_and_save_preference(user_input)

        # ── Détection automatique de rappels dans le message ──────────────
        try:
            re_engine = components.get("reminder_engine")
            if re_engine:
                from src.v3.proactive.reminder_detector import detect_reminders
                detected_reminders = detect_reminders(user_input)
                for dr in detected_reminders:
                    r = re_engine.add(title=dr.title, due_at=dr.due_at.isoformat())
                    due_str = dr.due_at.strftime("%d/%m/%Y")
                    print(f"  [📅 Rappel noté] {r.title} — {due_str} (id: {r.id})")
        except Exception as exc:
            print(f"  [AVERT rappels] {exc}")

        try:
            time_ctx = get_time_context()

            # B15 — Contexte lieu : fond cuisine si sujet cuisine/recette
            _COOKING_KEYWORDS = {
                "recette", "recettes", "cuisin", "cuisinier", "cuisinière",
                "ingrédient", "ingredient", "préparer", "preparer",
                "plat", "dessert", "gâteau", "gateau", "tarte", "soupe",
                "poulet", "pâtes", "pates", "riz", "gratin", "brownie",
                "fondant", "tiramisu", "crêpes", "crepes", "cookies",
                "mousse", "chocolat", "dîner", "diner", "déjeuner",
                "manger", "mange", "repas", "menu", "cuisinez",
            }
            _ui_loc = user_input.lower()
            _is_cooking = any(kw in _ui_loc for kw in _COOKING_KEYWORDS)
            try:
                from src.ui.alfred_app import set_ui_location
                set_ui_location("cuisine" if _is_cooking else "salon")
            except Exception:
                pass

            # B15 — Avatar : début séquence réponse (thinking + verrou speaking)
            avatar = components.get("avatar")
            if avatar:
                avatar.begin_response()
            try:
                from src.ui.alfred_app import set_ui_thinking, set_ui_input_enabled, set_ui_speaking
                set_ui_thinking(True)
                set_ui_input_enabled(False)
                set_ui_speaking(False)   # SoundWave muette pendant la réflexion
            except Exception:
                pass

            # 🔊 TTS streaming + UI streaming — callback phrase par phrase
            tts = components.get("tts")
            tts_muted = components.get("tts_muted", False)
            _tts_active = tts and not tts_muted
            _sec_ok = components.get("security_ok", False)
            _out_filter = components.get("output_filter")
            def on_sentence(phrase: str) -> None:
                s = phrase.strip()
                if not s:
                    return
                # 1. Filtre sécurité (Bloc 20)
                if _sec_ok and _out_filter:
                    s = _out_filter(s)
                # 2. Texte visible immédiatement
                try:
                    from src.ui.alfred_app import stream_ui_phrase
                    stream_ui_phrase(s)
                except Exception:
                    pass
                # 3. TTS — avatar + SoundWave synchronisés via on_play_start/stop
                if _tts_active:
                    try:
                        tts.speak(clean_for_tts(s))
                    except Exception as exc:
                        print(f"  [AVERT TTS stream] {exc}")

            response, mode, emotion_label, energy_level = build_response(
                user_input=user_input,
                components=components,
                time_ctx=time_ctx,
                on_sentence=on_sentence,
            )

            # B15 — Avatar : synchronise mode + émotion (verrou speaking encore actif)
            if avatar:
                try:
                    avatar.set_mode(mode.split("_")[0] if "_" in mode else mode)
                    avatar.set_emotion(emotion_label)
                except Exception:
                    pass

            # ── Filtre sécurité sortie IA (Bloc 20) ───────────────────────
            _analyze = components.get("analyze_output")
            if components.get("security_ok") and _analyze:
                _filtered = _analyze(response)
                response = _filtered["filtered"]
                if _filtered["replacements"] > 0:
                    from src.security.security_logger import log_event as _log_sec
                    _log_sec(f"output_filter: {_filtered['replacements']} donnée(s) masquée(s)", "WARNING")

            # B15 — UI Kivy : affiche la réponse filtrée dans la zone texte
            try:
                from src.ui.alfred_app import set_ui_response
                set_ui_response(response)
            except Exception:
                pass

            print(
                f"  [mode: {mode} | émotion: {emotion_label} | "
                f"énergie: {time_ctx.get('energy_level', energy_level)}]"
            )

            # Affichage texte (streaming = déjà affiché token par token)
            ollama = getattr(components.get("llm"), "primary", None)
            was_streamed = getattr(ollama, "last_was_streamed", False)
            if not was_streamed:
                print(f"\n  {ALFRED_NAME} : {response}\n")
                # TTS fallback pour réponses non-streamées (OpenAI ou forced)
                # avatar + SoundWave synchronisés via on_play_start/stop callbacks
                if tts and not tts_muted:
                    import re as _re
                    chunks = [c.strip() for c in _re.split(r'\n\n+', response) if c.strip()]
                    if not chunks:
                        chunks = [c.strip() for c in _re.split(r'(?<=[.!?])\s+', response) if c.strip()]
                    if not chunks:
                        chunks = [response]
                    for chunk in chunks:
                        if chunk:
                            tts.speak(clean_for_tts(chunk))
            else:
                print()  # saut de ligne après le stream

            # B15 — Fin séquence réponse (libère verrou speaking après tout le TTS)
            if avatar:
                try:
                    avatar.end_response()
                except Exception:
                    pass

            # ── Check-in santé Bloc 13 ─────────────────────────────────────
            _check_in = components.pop("_last_check_in", None)
            if _check_in:
                print(f"\n  {ALFRED_NAME} [bien-etre] : {_check_in}\n")
                if tts and not tts_muted:
                    try:
                        tts.speak(clean_for_tts(_check_in))
                    except Exception:
                        pass

            # ── Pause suggérée (fog / poussée) ────────────────────────────
            if components.pop("_last_offer_pause", False):
                _pause_msg = "Veux-tu faire une pause ? Je reste disponible quand tu veux."
                print(f"  {ALFRED_NAME} : {_pause_msg}\n")

            # B11 — Suggestion proactive
            proactive_suggestion = components.pop("_proactive_suggestion", None)
            if proactive_suggestion:
                print(f"\n  {ALFRED_NAME} [proactif] : {proactive_suggestion.content}\n")

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

    # ── Fermeture session sécurité ─────────────────────────────────────────
    if components.get("security_ok"):
        try:
            from src.security.session_manager import close_session
            close_session("celine")
        except Exception:
            pass


# =============================================================================
# 12. ENTREE PROGRAMME
# =============================================================================

if __name__ == "__main__":
    main()