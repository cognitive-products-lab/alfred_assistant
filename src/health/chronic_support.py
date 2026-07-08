"""
════════════════════════════════════════════════════════════
PROJECT      : ALFRED
BLOCK        : B13
FUNCTION     : 13.02
FILE         : src/health/chronic_support.py
ROLE         : Soutien émotionnel chronique et gestion fatigue/stress

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-05-10
UPDATED      : 2026-05-28
VERSION      : V1.0
STATUS       : TESTED
════════════════════════════════════════════════════════════
"""
# ============================================================
# ALFRED — src/health/chronic_support.py
# Bloc 13.02 / 13.03 — Soutien émotionnel chronique & gestion fatigue/stress santé
#
# Fonctions couvertes :
#   13.02.001 Détection signaux fragilité/santé dans le texte  ✅ V2
#   13.02.002 Identification contexte condition chronique       ✅ V2
#   13.02.003 Détection patterns cognitifs (stress, anxiété…)  ✅ V2
#   13.03.001 Distinction fatigue chronique vs passagère        ✅ V2
#   13.03.002 Détection fog cognitif                           ✅ V2
#   13.03.003 Détection poussée / rechute                      ✅ V2
#   13.03.004 Détection gestion enveloppe énergétique          ✅ V2
#   13.03.005 Détection ruminations / hyperfocus / bipolaire    ✅ V2
# ============================================================

import json
import re
from dataclasses import dataclass, field
from pathlib import Path

from paths import CONFIG_HEALTH
from src.security.security_logger import log_event

# ── Chargement JSON (une seule fois au démarrage du module) ──

def _load(filename: str) -> dict:
    path = CONFIG_HEALTH / filename
    if not path.exists():
        log_event(f"[chronic_support] JSON manquant : {filename}", "WARNING")
        return {}
    return json.loads(path.read_text(encoding="utf-8"))

_CONDITIONS      = _load("chronic_conditions.json").get("conditions", {})
_SIGNALS_CFG     = _load("fragility_signals.json")
_PROTOCOLS       = _load("health_protocols.json").get("protocols", {})
_WEIGHTS         = _load("fragility_signals.json").get("signal_weights", {})
_COGNITIVE_CFG   = _load("cognitive_patterns.json").get("patterns", {})


# ─────────────────────────────────────────────────────────
# Résultat de détection
# ─────────────────────────────────────────────────────────

@dataclass
class HealthSignalResult:
    """Résultat de l'analyse des signaux de santé dans un texte."""
    detected:              bool       = False
    signal_type:           str | None = None   # Type de signal dominant
    protocol_id:           str | None = None   # Protocole à activer
    priority:              int        = 0
    fog_detected:          bool       = False
    pain_detected:         bool       = False
    flare_detected:        bool       = False
    pacing_detected:       bool       = False
    crisis_health:         bool       = False
    invisible_illness:     bool       = False
    caregiver:             bool       = False
    bipolar_episode:       bool       = False
    rumination_active:     bool       = False
    hyperfocus_active:     bool       = False
    hypersomnia_active:    bool       = False
    hyperactivity_active:  bool       = False
    cognitive_patterns:    list[str]  = field(default_factory=list)  # patterns cognitifs détectés
    condition_hints:       list[str]  = field(default_factory=list)
    signals_matched:       list[str]  = field(default_factory=list)
    adaptation_rules:      dict       = field(default_factory=dict)


# ─────────────────────────────────────────────────────────
# Détection signaux de santé
# ─────────────────────────────────────────────────────────

def detect_health_signals(text: str) -> HealthSignalResult:
    """
    Analyse le texte utilisateur et détecte les signaux de santé/fragilité.
    Distinct de la détection émotionnelle Bloc 03 — ici on cherche
    des signaux spécifiques aux conditions chroniques et à la fragilité.

    Args:
        text : Message utilisateur

    Returns:
        HealthSignalResult avec le contexte santé détecté
    """
    text_lower = text.lower()
    result     = HealthSignalResult()
    best_score = 0
    matched    = []

    signal_categories = {
        "crisis_health_signals":    ("health_crisis",                 10),
        "flare_signals":            ("flare_support",                  8),
        "cognitive_fog_signals":    ("cognitive_fog_mode",             9),
        "bipolar_mood_signals":     ("flare_support",                  8),
        "pain_signals":             ("pain_acknowledgment",            7),
        "invisible_illness_signals":("invisible_illness_validation",   7),
        "caregiver_signals":        ("caregiver_support",              7),
        "energy_envelope_signals":  ("energy_pacing",                  6),
        "rumination_signals":       ("cognitive_fog_mode",             5),
        "hypersomnia_signals":      ("treatment_context",              4),
        "hyperactivity_signals":    ("treatment_context",              4),
        "hyperfocus_signals":       ("energy_pacing",                  3),
        "treatment_signals":        ("treatment_context",              3),
    }

    for cfg_key, (protocol_id, base_priority) in signal_categories.items():
        cfg = _SIGNALS_CFG.get(cfg_key, {})
        score = 0
        local_matched = []

        for kw in cfg.get("keywords_fr", []) + cfg.get("keywords_en", []):
            if kw in text_lower:
                score += 1
                local_matched.append(kw)

        for pattern in cfg.get("patterns_fr", []) + cfg.get("patterns_en", []):
            if re.search(pattern, text_lower, re.IGNORECASE):
                score += 2
                local_matched.append(pattern)

        if score > 0 and score > best_score:
            best_score         = score
            result.detected    = True
            result.signal_type = cfg_key
            result.protocol_id = protocol_id
            result.priority    = base_priority
            matched            = local_matched

    result.signals_matched = matched

    # ── Flags spécifiques (peuvent coexister) ──
    result.fog_detected         = _has_signals("cognitive_fog_signals", text_lower)
    result.pain_detected        = _has_signals("pain_signals", text_lower)
    result.flare_detected       = _has_signals("flare_signals", text_lower)
    result.pacing_detected      = _has_signals("energy_envelope_signals", text_lower)
    result.crisis_health        = _has_signals("crisis_health_signals", text_lower)
    result.invisible_illness    = _has_signals("invisible_illness_signals", text_lower)
    result.caregiver            = _has_signals("caregiver_signals", text_lower)
    result.bipolar_episode      = _has_signals("bipolar_mood_signals", text_lower)
    result.rumination_active    = _has_signals("rumination_signals", text_lower)
    result.hyperfocus_active    = _has_signals("hyperfocus_signals", text_lower)
    result.hypersomnia_active   = _has_signals("hypersomnia_signals", text_lower)
    result.hyperactivity_active = _has_signals("hyperactivity_signals", text_lower)

    # ── Patterns cognitifs (cognitive_patterns.json) ──
    result.cognitive_patterns = detect_cognitive_patterns(text_lower)

    # ── Condition hints — conditions mentionnées explicitement ──
    result.condition_hints = _detect_condition_hints(text_lower)

    # ── Règles d'adaptation pour le signal dominant ──
    if result.signal_type and result.protocol_id in _PROTOCOLS:
        result.adaptation_rules = _PROTOCOLS[result.protocol_id].get("response_rules", {})

    if result.detected:
        log_event(
            f"Signal santé détecté : {result.signal_type} "
            f"(priorité {result.priority}, fog={result.fog_detected}, "
            f"rumination={result.rumination_active}, bipolaire={result.bipolar_episode})"
        )

    return result


def _has_signals(cfg_key: str, text_lower: str) -> bool:
    """Vérifie si des signaux d'une catégorie sont présents."""
    cfg = _SIGNALS_CFG.get(cfg_key, {})
    for kw in cfg.get("keywords_fr", []) + cfg.get("keywords_en", []):
        if kw in text_lower:
            return True
    return False


def _detect_condition_hints(text_lower: str) -> list[str]:
    """Détecte les conditions chroniques mentionnées explicitement."""
    hints = []
    for condition_id, cond_data in _CONDITIONS.items():
        signals = cond_data.get("signaux_détresse_spécifiques", [])
        if any(s.lower() in text_lower for s in signals):
            hints.append(condition_id)
    return hints


def detect_cognitive_patterns(text_or_lower: str) -> list[str]:
    """
    Détecte les patterns cognitifs actifs (stress chronique, anxiété, fibro fog,
    ruminations, hyperfocus, surcharge sensorielle) depuis cognitive_patterns.json.

    Args:
        text_or_lower : Texte ou texte déjà en minuscules

    Returns:
        Liste des IDs de patterns détectés (ordre décroissant de priorité)
    """
    text_lower = text_or_lower.lower()
    priority_order = [
        "fibro_fog", "surcharge_sensorielle", "ruminations",
        "hyperfocus_dissociatif", "anxiete_chronique", "stress_chronique"
    ]
    detection_cfg = {
        p.get("value", k): {
            "threshold": 1.5,
            "kw_score": 1.0,
            "pat_score": 1.5,
        }
        for k, p in [("x", {})]  # placeholder — on lit depuis le JSON
    }

    matched_patterns = []

    for pattern_id in priority_order:
        pattern_cfg = _COGNITIVE_CFG.get(pattern_id, {})
        if not pattern_cfg:
            continue

        score = 0.0
        for kw in pattern_cfg.get("keywords_fr", []) + pattern_cfg.get("keywords_en", []):
            if kw.lower() in text_lower:
                score += 1.0

        for pat in pattern_cfg.get("patterns_fr", []) + pattern_cfg.get("patterns_en", []):
            try:
                if re.search(pat, text_lower, re.IGNORECASE):
                    score += 1.5
            except re.error:
                pass

        if score >= 1.5:
            matched_patterns.append(pattern_id)

    return matched_patterns


def get_cognitive_pattern_adaptation(pattern_id: str) -> dict:
    """
    Retourne les règles d'adaptation ALFRED pour un pattern cognitif donné.

    Args:
        pattern_id : ID du pattern (ex: 'ruminations', 'fibro_fog')

    Returns:
        Dict 'adaptation_alfred' du pattern, ou {} si non trouvé
    """
    pattern = _COGNITIVE_CFG.get(pattern_id, {})
    return pattern.get("adaptation_alfred", {})


# ─────────────────────────────────────────────────────────
# Adaptation selon condition
# ─────────────────────────────────────────────────────────

def get_condition_adaptations(condition_ids: list[str]) -> dict:
    """
    Retourne les règles d'adaptation fusionnées pour une liste de conditions.

    Args:
        condition_ids : Liste d'IDs de conditions (depuis chronic_conditions.json)

    Returns:
        Dict d'adaptations de communication fusionnées
    """
    if not condition_ids:
        return {}

    merged = {
        "response_length":    "medium",
        "cognitive_load":     "standard",
        "avoid":              [],
        "prefer":             [],
        "forbidden_phrases":  [],
    }

    for cid in condition_ids:
        cond = _CONDITIONS.get(cid, {})
        adaptations = cond.get("communication_adaptations", {})
        interaction  = adaptations.get("interaction_preferences", {})

        # Longueur : prendre la plus restrictive
        length_priority = {"very_short": 0, "très_courte": 0, "courte_à_moyenne": 1,
                           "short_to_medium": 1, "medium": 2, "adaptive": 3}
        current = merged["response_length"]
        new_len  = adaptations.get("longueur_réponse", "medium")
        if length_priority.get(new_len, 3) < length_priority.get(current, 3):
            merged["response_length"] = new_len

        # Charge cognitive
        if adaptations.get("charge_cognitive") in ["minimale", "minimale_absolue", "minimale_absolute"]:
            merged["cognitive_load"] = "minimal"
        elif adaptations.get("charge_cognitive") in ["réduite", "reduced"] and merged["cognitive_load"] != "minimal":
            merged["cognitive_load"] = "reduced"

        # Éviter / interdits
        merged["avoid"].extend(adaptations.get("éviter", []))
        merged["forbidden_phrases"].extend(cond.get("à_ne_jamais_dire", []))

        # Préférences communication (TDAH notamment)
        merged["prefer"].extend(interaction.get("préférer", []))

    # Déduplication
    merged["avoid"]            = list(set(merged["avoid"]))
    merged["forbidden_phrases"] = list(set(merged["forbidden_phrases"]))
    merged["prefer"]           = list(set(merged["prefer"]))

    return merged


def get_adapted_response(signal_result: HealthSignalResult, emotion: str | None = None) -> str | None:
    """
    Retourne une réponse adaptée au signal de santé détecté.
    Priorité : crise > fog > poussée > douleur > maladie invisible.

    Args:
        signal_result : Résultat de detect_health_signals()
        emotion       : Émotion détectée (Bloc 03) pour cohérence

    Returns:
        Template de réponse ou None
    """
    if signal_result.crisis_health:
        protocol = _PROTOCOLS.get("health_crisis", {})
        templates = protocol.get("response_templates", [])
        return templates[0] if templates else None

    if signal_result.fog_detected:
        protocol = _PROTOCOLS.get("cognitive_fog_mode", {})
        return protocol.get("announcement")

    if signal_result.flare_detected:
        protocol = _PROTOCOLS.get("flare_support", {})
        templates = protocol.get("response_templates", [])
        return templates[0] if templates else None

    if signal_result.pain_detected:
        protocol = _PROTOCOLS.get("pain_acknowledgment", {})
        templates = protocol.get("response_templates", [])
        return templates[0] if templates else None

    if signal_result.invisible_illness:
        return _SIGNALS_CFG.get("invisible_illness_signals", {}).get("response_template")

    return None


def get_condition_profile(condition_id: str) -> dict:
    """Retourne le profil complet d'une condition depuis la base de connaissances."""
    return _CONDITIONS.get(condition_id, {})
