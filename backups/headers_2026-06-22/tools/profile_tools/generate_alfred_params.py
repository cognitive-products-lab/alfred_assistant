"""
generate_alfred_params.py — Mapping psychométrie → paramètres comportementaux ALFRED

Rôle :
  Lit data/profile/user_profile.json (données brutes des évaluations psychométriques)
  et dérive les paramètres comportementaux d'ALFRED pour Céline.

  Produit deux sorties :
  1. data/profile/alfred_behavioral_params.json  — paramètres dérivés documentés
  2. Mise à jour de data/users/instances/user_celine_instance.json

Usage :
  python tools/profile_tools/generate_alfred_params.py
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
USER_PROFILE_PATH   = ROOT / "data" / "profile" / "user_profile.json"
CELINE_INSTANCE_PATH = ROOT / "data" / "users" / "instances" / "user_celine_instance.json"
OUTPUT_PARAMS_PATH  = ROOT / "data" / "profile" / "alfred_behavioral_params.json"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print(f"  ✓ Écrit : {path.relative_to(ROOT)}")


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


# ---------------------------------------------------------------------------
# Extraction des données psychométriques brutes
# ---------------------------------------------------------------------------

def extract_psychometric_signals(profile: dict) -> dict:
    """Extrait les signaux clés des évaluations disponibles."""
    signals = {}

    # AssessFirst — style de personnalité
    prefs = profile.get("preferences", {})
    signals["assessfirst_style"]      = prefs.get("style_personnel", "")
    signals["assessfirst_decision"]   = prefs.get("prise_de_decision", "")
    signals["assessfirst_learning"]   = prefs.get("style_apprentissage", "")
    signals["assessfirst_traits"]     = profile.get("personality_traits", [])

    # DISC — profil comportemental
    disc = profile.get("disc_profile", {})
    test2 = disc.get("test_2", {})
    signals["disc_dominant"]    = test2.get("profil_dominant", "")
    signals["disc_secondary"]   = test2.get("profil_secondaire", "")
    disc_scores = test2.get("scores", {})
    signals["disc_C"] = disc_scores.get("conforme_C", 0)
    signals["disc_I"] = disc_scores.get("influent_I", 0)
    signals["disc_D"] = disc_scores.get("dominant_D", 0)
    signals["disc_S"] = disc_scores.get("stable_S", 0)

    # 32 personnalités orientaction
    p32 = profile.get("personnalite_32_types", {})
    signals["type_32"] = p32.get("profil", "")

    # 7 besoins professionnels
    besoins = profile.get("besoins_professionnels", {})
    signals["besoin_principal"] = besoins.get("besoin_principal", "")

    # Harmony — soft skills
    harmony = profile.get("harmony_soft_skills", {})
    top3 = harmony.get("top_3_scores", {})
    signals["harmony_communication"] = top3.get("Communication", 0)
    signals["harmony_gestion_temps"] = top3.get("Gestion_du_temps", 0)
    signals["harmony_gestion_stress"] = top3.get("Gestion_du_stress", 0)

    return signals


# ---------------------------------------------------------------------------
# Mapping psychométrie → paramètres ALFRED
# ---------------------------------------------------------------------------

def derive_alfred_parameters(signals: dict) -> dict:
    """
    Mappe les signaux psychométriques en paramètres comportementaux pour ALFRED.

    Logique de mapping :
    - DISC C (Conforme) élevé   → structure, précision, fiabilité, réduction du risque
    - DISC I (Influent) stable  → chaleur, expressivité, connexion
    - Besoin SÉCURITÉ           → prévisibilité, cohérence, cadre rassurant
    - Communication 100/100     → registre élaboré, vocabulaire riche
    - Gestion temps 90/100      → concision sur sujets maîtrisés
    - Gestion stress 90/100     → soutien émotionnel uniquement si dérive réelle
    - Leader Visionnaire        → accepte ambition et projections long terme
    - Empathique                → sensible aux dimensions humaines
    - Organisé                  → apprécie structure et plans
    - Décision Raisonnée        → présenter les options avec arguments
    - Style Innovante           → nouvelles approches bienvenues
    """
    params: dict = {}

    C = signals.get("disc_C", 0)
    I = signals.get("disc_I", 0)
    besoin = signals.get("besoin_principal", "")
    comm_score = signals.get("harmony_communication", 0)
    stress_score = signals.get("harmony_gestion_stress", 0)
    type_32 = signals.get("type_32", "")

    # ── Ton par défaut ──────────────────────────────────────────────
    # I élevé → chaleureux, C élevé → structuré et direct
    params["tone_default"] = "direct, chaleureux, structuré et motivant"

    # ── Ton selon l'état de fatigue ─────────────────────────────────
    # Besoin SÉCURITÉ → rassurant + cadre clair même en mode fatigué
    if besoin == "SÉCURITÉ":
        params["tone_when_fatigued"] = (
            "doux, rassurant, très synthétique — une étape à la fois, cadre clair, pas de surprise"
        )
    else:
        params["tone_when_fatigued"] = "doux, synthétique, guidant"

    # ── Ton stratégique ─────────────────────────────────────────────
    # Leader Visionnaire → ambition et long terme bienvenus
    if "Visionnaire" in type_32:
        params["tone_when_strategic"] = (
            "expert, ambitieux, orienté vision long terme et décision"
        )
    else:
        params["tone_when_strategic"] = "expert, structuré, orienté décision"

    # ── Ton apprentissage ───────────────────────────────────────────
    # Style Innovante + Décision Raisonnée → progressif avec logique claire
    params["tone_when_learning"] = (
        "pédagogique, progressif, logique explicite — exemple concret avant théorie"
    )

    # ── Profondeur de réponse ───────────────────────────────────────
    # C élevé → apprécie les détails ; mais Gestion temps 90 → pas de redondance
    params["response_length"] = "detailed"
    params["response_efficiency"] = (
        "détaillé sur les sujets nouveaux ou complexes, concis sur les sujets maîtrisés"
    )

    # ── Structure ───────────────────────────────────────────────────
    params["preferred_format"] = "structuré avec étapes numérotées et titres clairs"
    params["structure_preference"] = "très structuré"  # C dominant
    params["structure_level"] = round(C / 20, 1)  # C=19 → 0.95 (out of 1)

    # ── Registre linguistique ────────────────────────────────────────
    # Communication 100/100 → registre élaboré
    if comm_score >= 90:
        params["language_register"] = "élaboré — vocabulaire riche, pas de simplification excessive"
    else:
        params["language_register"] = "standard, clair"

    # ── Niveau d'humour ─────────────────────────────────────────────
    # I élevé → humour léger bienvenu ; C élevé → humour contextuel (pas systématique)
    params["humor"] = True
    params["humor_level"] = "léger et intelligent, contextuel — jamais au détriment de la précision"

    # ── Soutien émotionnel ──────────────────────────────────────────
    # Gestion stress 90/100 → résilience élevée
    # Soutien émotionnel actif seulement si PSS ou UWES indique une dérive
    if stress_score >= 85:
        params["emotional_support_trigger"] = (
            "soutien émotionnel actif uniquement si PSS > 10 ou UWES < 2.5, "
            "ou si Céline exprime explicitement une difficulté"
        )
        params["emotional_support_level"] = "modéré — résistance au stress élevée (Harmony 90/100)"
    else:
        params["emotional_support_level"] = "standard"
        params["emotional_support_trigger"] = "sur expression explicite de difficulté"

    # ── Prévisibilité / cohérence (besoin SÉCURITÉ) ─────────────────
    if besoin == "SÉCURITÉ":
        params["reliability_requirement"] = "critique"
        params["consistency_level"] = "maximale — comportement prévisible prioritaire"
        params["change_framing"] = (
            "toujours expliquer le POURQUOI d'un changement avant le QUOI — "
            "présenter les bénéfices concrets et les risques gérés"
        )
        params["surprise_policy"] = (
            "aucune surprise négative — signaler en amont si quelque chose ne va pas comme prévu"
        )

    # ── Vision et ambition ──────────────────────────────────────────
    if "Visionnaire" in type_32:
        params["vision_mode"] = (
            "projections long terme et objectifs ambitieux valorisés (Leader Visionnaire) — "
            "ALFRED peut proposer des perspectives stratégiques proactives"
        )
        params["challenge_level"] = "élevé — Leader Visionnaire, accepte les défis ambitieux"

    # ── Empathie ────────────────────────────────────────────────────
    if "Empathique" in type_32:
        params["empathy_level"] = (
            "présent mais non intrusif — Céline est sensible aux dimensions humaines, "
            "ALFRED reconnaît l'effort et l'aspect humain sans pathos"
        )

    # ── Prise de décision ───────────────────────────────────────────
    # Raisonnée (AssessFirst) + C Conforme → présenter les options avec arguments
    params["decision_support"] = (
        "présenter les options avec arguments structurés — "
        "Céline prend le temps d'évaluer, ne pas forcer une conclusion unique"
    )

    # ── Proactivité ─────────────────────────────────────────────────
    # I=16 → apprécie l'interaction ; mais C → cadre prévisible
    params["proactivity_level"] = "modéré à élevé — proactif sur les sujets déjà identifiés, "  \
                                   "attentif avant de proposer du nouveau"

    return params


# ---------------------------------------------------------------------------
# Génération du fichier alfred_behavioral_params.json
# ---------------------------------------------------------------------------

def build_behavioral_params_doc(signals: dict, params: dict) -> dict:
    """Construit le document complet des paramètres comportementaux."""
    return {
        "_meta": {
            "generated_by": "generate_alfred_params.py",
            "generated_at": now_iso(),
            "version": "1.0",
            "sources": [
                "AssessFirst SWIPE-DRIVE-BRAIN (2026-06-15)",
                "DISC e-orientaction (référence — test_2)",
                "32 personnalités e-orientaction",
                "Needs Pro — 7 besoins professionnels",
                "Harmony® test des 16 soft skills (2024-07-01)"
            ]
        },
        "psychometric_signals": signals,
        "alfred_behavioral_params": params,
        "interpretation_summary": {
            "profil_dominant": "Conforme (C) + Influent (I) → Organisé, précis, sociable, communicant",
            "besoin_ancrage": "SÉCURITÉ → prévisibilité et fiabilité comme prérequis",
            "forces_distinctives": [
                "Communication 100/100 — maîtrise élaborée",
                "Gestion du temps 90/100 — efficacité et organisation naturelles",
                "Gestion du stress 90/100 — résilience élevée",
                "Leader Visionnaire — vision long terme et ambition",
                "Empathique — dimension humaine importante"
            ],
            "alfred_posture": (
                "ALFRED se positionne comme un partenaire fiable, structuré et ambitieux. "
                "Il respecte le besoin de prévisibilité (SÉCURITÉ) tout en stimulant "
                "la vision long terme (Leader Visionnaire). "
                "Il adapte son registre élaboré (Communication 100) "
                "et maintient une chaleur sincère (Influent) sans flatterie (Conforme analytique)."
            )
        }
    }


# ---------------------------------------------------------------------------
# Mise à jour de user_celine_instance.json
# ---------------------------------------------------------------------------

def update_celine_instance(instance: dict, params: dict, signals: dict) -> dict:
    """Met à jour l'instance Céline avec les paramètres dérivés."""

    now = now_iso()

    # Mise à jour des préférences de ton
    prefs = instance.setdefault("preferences", {})
    prefs["tone"]                  = params["tone_default"]
    prefs["tone_when_fatigued"]    = params["tone_when_fatigued"]
    prefs["tone_when_strategic"]   = params["tone_when_strategic"]
    prefs["tone_when_learning"]    = params["tone_when_learning"]
    prefs["response_length"]       = params["response_length"]
    prefs["humor"]                 = params["humor"]
    prefs["preferred_format"]      = params["preferred_format"]

    # Ajout d'une section contexte psychométrique (documentaire)
    instance["psychometric_profile"] = {
        "last_updated": now,
        "disc_reference": f"Conforme C={signals['disc_C']} / Influent I={signals['disc_I']} (e-orientaction)",
        "personnalite_32": signals["type_32"],
        "besoin_principal": signals["besoin_principal"],
        "harmony_top3": {
            "Communication":      signals["harmony_communication"],
            "Gestion_du_temps":   signals["harmony_gestion_temps"],
            "Gestion_du_stress":  signals["harmony_gestion_stress"]
        },
        "derived_params": params
    }

    # Mise à jour des règles d'adaptation
    rules = instance.setdefault("adaptation_rules", {})
    rules["high_focus_mode"] = (
        "réponse structurée avec étapes numérotées, livrables clairs — "
        "pas de redondance"
    )
    rules["low_energy_mode"] = (
        "réponse très courte, rassurante, une étape à la fois — "
        "cadre clair, signal positif, pas de surprise"
    )
    rules["security_mode"] = (
        "expliquer le pourquoi avant le quoi — cadre rassurant, "
        "bénéfices concrets, risques gérés, cohérence garantie"
    )
    rules["vision_mode"] = (
        "projections long terme, objectifs ambitieux, stratégie claire — "
        "Leader Visionnaire : penser grand, structurer pour y arriver"
    )
    rules["technical_mode"] = (
        "code propre, fichiers, arborescence, logique d'intégration — "
        "précision Conforme : vérifier chaque détail"
    )
    rules["creative_mode"] = (
        "audace et propositions nouvelles — Innovante (AssessFirst) : "
        "nouvelles approches bienvenues"
    )
    rules["default_mode"] = "companion_mode"

    # Style de communication enrichi
    comm = instance.setdefault("communication_style", {})
    comm["preferred_format"] = params["preferred_format"]
    comm["language_register"] = params["language_register"]
    comm["structure_preference"] = params["structure_preference"]
    comm["response_efficiency"] = params["response_efficiency"]
    comm["avoid"] = [
        "réponses vagues ou sans structure",
        "trop de théorie sans application concrète",
        "ton froid ou robotique",
        "surprises négatives sans préavis (besoin SÉCURITÉ)",
        "simplifications excessives (Communication 100/100)",
        "flatterie creuse (Conforme analytique)",
        "questions inutiles quand une hypothèse raisonnable suffit",
        "réponses trop courtes sur les sujets complexes"
    ]

    # Style de travail enrichi
    ws = instance["user_profile"].setdefault("working_style", [])
    working_style_enrichi = [
        "structurée et organisée (DISC Conforme C=19)",
        "analytique et précise (DISC Conforme — réduction des risques)",
        "sociable et communicante naturelle (DISC Influent I=16, Harmony 100/100)",
        "exigeante sur la qualité et la cohérence",
        "orientée résultat et vision long terme (Leader Visionnaire)",
        "empathique — sensible à la dimension humaine",
        "besoin de sécurité et de prévisibilité comme ancrage",
        "décision raisonnée — évalue les options avant de conclure",
        "style d'apprentissage innovant — nouvelles approches bienvenues"
    ]
    instance["user_profile"]["working_style"] = working_style_enrichi

    # Mise à jour du timestamp
    instance["user_profile"]["updated_at"] = now
    instance.setdefault("metadata", {})["updated_at"] = now

    return instance


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    print("\n[ALFRED Profile → Params] Génération des paramètres comportementaux...")
    print(f"  ROOT = {ROOT}")

    if not USER_PROFILE_PATH.exists():
        print(f"  ✗ user_profile.json introuvable : {USER_PROFILE_PATH}")
        return

    profile = load_json(USER_PROFILE_PATH)
    print(f"  ✓ Profil chargé : {profile.get('name', '?')}")

    # Extraction des signaux
    signals = extract_psychometric_signals(profile)
    print(f"  ✓ Signaux extraits : DISC C={signals['disc_C']} I={signals['disc_I']}, "
          f"besoin={signals['besoin_principal']}, comm={signals['harmony_communication']}")

    # Dérivation des paramètres
    params = derive_alfred_parameters(signals)
    print(f"  ✓ {len(params)} paramètres ALFRED dérivés")

    # Sauvegarde alfred_behavioral_params.json
    doc = build_behavioral_params_doc(signals, params)
    save_json(OUTPUT_PARAMS_PATH, doc)

    # Mise à jour user_celine_instance.json
    if CELINE_INSTANCE_PATH.exists():
        instance = load_json(CELINE_INSTANCE_PATH)
        instance = update_celine_instance(instance, params, signals)
        save_json(CELINE_INSTANCE_PATH, instance)
    else:
        print(f"  ⚠ Instance Céline introuvable : {CELINE_INSTANCE_PATH}")

    # Résumé
    print(f"\n{'=' * 60}")
    print("  PARAMÈTRES ALFRED DÉRIVÉS")
    print(f"{'=' * 60}")
    for k, v in params.items():
        label = f"  {k:<35s}"
        val = str(v)[:60]
        print(f"{label} {val}")
    print(f"{'=' * 60}\n")


if __name__ == "__main__":
    main()
