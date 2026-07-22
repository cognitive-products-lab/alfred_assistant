# ============================================================
# ALFRED — src/conversation/input/context_builder.py
# Bloc 01.03 — Gestion du contexte
#
# 📚 NOTION EXAM :
#   D11-3 — Capsule 1 : Construction du contexte session et fusion
#
# 🎯 UTILITÉ ALFRED :
#   Construit et fusionne le contexte global de session : temporel,
#   device, conversation et localisation (V2+).
#
# 🏗️ DOMAINE :
#   Noyau conversationnel — contexte temps réel, device-aware
#
# STATUS  : VALIDATED
# ============================================================

import platform
import socket
from datetime import datetime
from zoneinfo import ZoneInfo

# ALFRED est un assistant francophone local (localisation confirmée par le
# code postal du profil / de la météo, toujours en France) : l'heure est
# ancrée explicitement sur "Europe/Paris" plutôt que de dépendre de l'horloge
# système, qui peut être mal réglée ou (sur Android/autre device) dans un
# fuseau différent.
_FRANCE_TZ = ZoneInfo("Europe/Paris")


# ─────────────────────────────────────────────────────────
# Contexte temporel
# ─────────────────────────────────────────────────────────

def get_time_context() -> dict:
    """
    Construit le contexte temporel courant (heure française, Europe/Paris).

    Returns:
        dict avec heure, période journée, jour semaine, date
    """
    now = datetime.now(_FRANCE_TZ)
    hour = now.hour

    if 5 <= hour < 12:
        period = "matin"
        greeting = "Bonjour"
    elif 12 <= hour < 14:
        period = "midi"
        greeting = "Bon après-midi"
    elif 14 <= hour < 18:
        period = "après-midi"
        greeting = "Bon après-midi"
    elif 18 <= hour < 22:
        period = "soirée"
        greeting = "Bonsoir"
    else:
        period = "nuit"
        greeting = "Bonsoir"

    # Niveau d'énergie probable selon l'heure
    if 8 <= hour < 12 or 15 <= hour < 18:
        energy_level = "high"
    elif 12 <= hour < 14 or 18 <= hour < 20:
        energy_level = "medium"
    else:
        energy_level = "low"

    jours_fr = {
        0: "lundi", 1: "mardi", 2: "mercredi", 3: "jeudi",
        4: "vendredi", 5: "samedi", 6: "dimanche"
    }
    mois_fr = {
        1: "janvier", 2: "février", 3: "mars", 4: "avril",
        5: "mai", 6: "juin", 7: "juillet", 8: "août",
        9: "septembre", 10: "octobre", 11: "novembre", 12: "décembre"
    }

    return {
        "datetime":     now.isoformat(),
        "time":         now.strftime("%H:%M"),
        "date":         f"{jours_fr[now.weekday()]} {now.day} {mois_fr[now.month]} {now.year}",
        "day_of_week":  jours_fr[now.weekday()],
        "period":       period,
        "greeting":     greeting,
        "energy_level": energy_level,
        "is_weekend":   now.weekday() >= 5,
        "hour":         hour,
    }


# ─────────────────────────────────────────────────────────
# Contexte device
# ─────────────────────────────────────────────────────────

def get_device_context(device_id: str = "local_pc") -> dict:
    """
    Construit le contexte de l'appareil courant.

    Args:
        device_id : Identifiant de l'appareil (par défaut PC local)

    Returns:
        dict avec infos système et device
    """
    return {
        "device_id":   device_id,
        "device_type": "desktop",
        "os":          platform.system(),
        "os_version":  platform.version()[:40],  # Tronqué pour les logs
        "hostname":    socket.gethostname(),
        "interface":   "terminal_v1",
    }


# ─────────────────────────────────────────────────────────
# Contexte conversation
# ─────────────────────────────────────────────────────────

def get_conversation_context(history: list[dict]) -> dict:
    """
    Construit le contexte basé sur l'historique de conversation.

    Args:
        history : Historique de la session (liste d'échanges)

    Returns:
        dict avec résumé conversationnel
    """
    count = len(history)

    if count == 0:
        stage = "opening"
        last_user_message = None
        last_intent = None
    elif count <= 3:
        stage = "early"
        last_user_message = history[-1].get("user")
        last_intent = history[-1].get("intent")
    elif count <= 10:
        stage = "active"
        last_user_message = history[-1].get("user")
        last_intent = history[-1].get("intent")
    else:
        stage = "deep"
        last_user_message = history[-1].get("user")
        last_intent = history[-1].get("intent")

    return {
        "exchange_count":     count,
        "conversation_stage": stage,
        "last_user_message":  last_user_message,
        "last_intent":        last_intent,
        "is_first_message":   count == 0,
    }


# ─────────────────────────────────────────────────────────
# Fusion contexte global
# ─────────────────────────────────────────────────────────

def build_context(
    history: list[dict],
    device_id: str = "local_pc",
    user_name: str = "Céline",
) -> dict:
    """
    Construit le contexte global complet pour une requête ALFRED.
    Point d'entrée principal du context builder.

    Args:
        history     : Historique session courant
        device_id   : Identifiant de l'appareil
        user_name   : Prénom de l'utilisateur

    Returns:
        dict contexte complet prêt à être injecté dans le prompt
    """
    time_ctx   = get_time_context()
    device_ctx = get_device_context(device_id)
    conv_ctx   = get_conversation_context(history)

    return {
        "user_name":    user_name,
        "time":         time_ctx,
        "device":       device_ctx,
        "conversation": conv_ctx,
        # Champs pratiques à la surface pour faciliter l'accès rapide
        "greeting":     time_ctx["greeting"],
        "period":       time_ctx["period"],
        "energy_level": time_ctx["energy_level"],
        "is_first":     conv_ctx["is_first_message"],
    }


def format_context_for_prompt(context: dict) -> str:
    """
    Formate le contexte en texte injectabl dans un prompt LLM.

    Args:
        context : Contexte construit par build_context()

    Returns:
        Bloc texte structuré pour injection système
    """
    t = context["time"]
    c = context["conversation"]

    lines = [
        f"[Contexte session]",
        f"Utilisatrice : {context['user_name']}",
        f"Heure        : {t['time']} ({t['period']}, {t['date']})",
        f"Énergie      : {t['energy_level']}",
        f"Échanges     : {c['exchange_count']}",
        f"Stade        : {c['conversation_stage']}",
    ]

    if c["last_user_message"]:
        lines.append(f"Dernier msg  : {c['last_user_message'][:80]}...")

    return "\n".join(lines)
