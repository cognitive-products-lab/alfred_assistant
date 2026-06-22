"""
test_alfred_profile_integration.py — Smoke test : profil psychométrique → ALFRED

Vérifie que :
  1. user_profile.json est valide et complet
  2. alfred_behavioral_params.json existe et est cohérent
  3. user_celine_instance.json est à jour et chargeable
  4. PersonalityAdapter charge correctement les paramètres dérivés
  5. build_response_context() produit un contexte adapté pour chaque scénario type

Usage :
  python tools/profile_tools/test_alfred_profile_integration.py
"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

PASS = "  ✅"
FAIL = "  ❌"
WARN = "  ⚠️"

errors: list[str] = []
warnings: list[str] = []


def check(condition: bool, label: str, warn_only: bool = False) -> bool:
    if condition:
        print(f"{PASS} {label}")
    elif warn_only:
        print(f"{WARN} {label}")
        warnings.append(label)
    else:
        print(f"{FAIL} {label}")
        errors.append(label)
    return condition


def load_json(path: Path) -> dict | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"{FAIL} Impossible de charger {path.name} : {e}")
        errors.append(str(path.name))
        return None


# ---------------------------------------------------------------------------
# 1 — Fichiers JSON
# ---------------------------------------------------------------------------

print("\n" + "=" * 60)
print("  TEST 1 : Fichiers JSON")
print("=" * 60)

user_profile = load_json(ROOT / "data" / "profile" / "user_profile.json")
celine_instance = load_json(ROOT / "data" / "users" / "instances" / "user_celine_instance.json")
behavioral_params = load_json(ROOT / "data" / "profile" / "alfred_behavioral_params.json")
personality_instance = load_json(ROOT / "data" / "personality" / "instances" / "personality_core_instance.json")

check(user_profile is not None,         "user_profile.json chargé")
check(celine_instance is not None,       "user_celine_instance.json chargé")
check(behavioral_params is not None,     "alfred_behavioral_params.json chargé")
check(personality_instance is not None,  "personality_core_instance.json chargé")

# ---------------------------------------------------------------------------
# 2 — Contenu user_profile.json
# ---------------------------------------------------------------------------

print("\n" + "=" * 60)
print("  TEST 2 : Contenu user_profile.json")
print("=" * 60)

if user_profile:
    check("disc_profile"            in user_profile, "Section disc_profile présente")
    check("personnalite_32_types"   in user_profile, "Section personnalite_32_types présente")
    check("besoins_professionnels"  in user_profile, "Section besoins_professionnels présente")
    check("harmony_soft_skills"     in user_profile, "Section harmony_soft_skills présente")

    disc = user_profile.get("disc_profile", {})
    t2_scores = disc.get("test_2", {}).get("scores", {})
    check(t2_scores.get("conforme_C") == 19, f"DISC C=19 (référence e-orientaction) → {t2_scores.get('conforme_C')}")
    check(t2_scores.get("influent_I") == 16, f"DISC I=16 (stable) → {t2_scores.get('influent_I')}")

    besoins = user_profile.get("besoins_professionnels", {})
    check(besoins.get("besoin_principal") == "SÉCURITÉ",
          f"Besoin principal = SÉCURITÉ → {besoins.get('besoin_principal')}")

    harmony = user_profile.get("harmony_soft_skills", {}).get("top_3_scores", {})
    check(harmony.get("Communication") == 100, f"Communication 100/100 → {harmony.get('Communication')}")
    check(harmony.get("Gestion_du_temps") == 90, f"Gestion du temps 90/100 → {harmony.get('Gestion_du_temps')}")
    check(harmony.get("Gestion_du_stress") == 90, f"Gestion du stress 90/100 → {harmony.get('Gestion_du_stress')}")

# ---------------------------------------------------------------------------
# 3 — Contenu alfred_behavioral_params.json
# ---------------------------------------------------------------------------

print("\n" + "=" * 60)
print("  TEST 3 : Paramètres ALFRED dérivés")
print("=" * 60)

if behavioral_params:
    params = behavioral_params.get("alfred_behavioral_params", {})
    required_keys = [
        "tone_default", "tone_when_fatigued", "tone_when_strategic",
        "tone_when_learning", "response_length", "preferred_format",
        "structure_preference", "language_register",
        "reliability_requirement", "consistency_level",
        "change_framing", "vision_mode", "empathy_level"
    ]
    for k in required_keys:
        check(k in params, f"Paramètre '{k}' présent")

    check(
        params.get("reliability_requirement") == "critique",
        "reliability_requirement = critique (besoin SÉCURITÉ)"
    )
    check(
        "Visionnaire" in params.get("vision_mode", ""),
        "vision_mode mentionne Leader Visionnaire"
    )
    check(
        params.get("structure_preference") == "très structuré",
        "structure_preference = très structuré (DISC Conforme)"
    )

# ---------------------------------------------------------------------------
# 4 — Contenu user_celine_instance.json
# ---------------------------------------------------------------------------

print("\n" + "=" * 60)
print("  TEST 4 : Instance Céline enrichie")
print("=" * 60)

if celine_instance:
    check("psychometric_profile" in celine_instance, "Section psychometric_profile présente")
    psych = celine_instance.get("psychometric_profile", {})
    check(psych.get("besoin_principal") == "SÉCURITÉ", "besoin_principal = SÉCURITÉ")
    h3 = psych.get("harmony_top3", {})
    check(h3.get("Communication") == 100, "Harmony Communication=100 dans instance")

    prefs = celine_instance.get("preferences", {})
    check("tone" in prefs, "tone par défaut défini")
    check("tone_when_fatigued" in prefs, "tone_when_fatigued défini")
    check("tone_when_strategic" in prefs, "tone_when_strategic défini")
    check("tone_when_learning" in prefs, "tone_when_learning défini")

    rules = celine_instance.get("adaptation_rules", {})
    check("security_mode" in rules, "adaptation_rules.security_mode présent")
    check("vision_mode" in rules, "adaptation_rules.vision_mode présent")

    meta = celine_instance.get("metadata", {})
    check(meta.get("is_template") is False, "is_template = False (pas un template)")

# ---------------------------------------------------------------------------
# 5 — PersonalityAdapter
# ---------------------------------------------------------------------------

print("\n" + "=" * 60)
print("  TEST 5 : PersonalityAdapter — intégration complète")
print("=" * 60)

try:
    spec = importlib.util.spec_from_file_location(
        "personality_adapter",
        ROOT / "src" / "core" / "personality_adapter.py"
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    PersonalityAdapter = mod.PersonalityAdapter

    adapter = PersonalityAdapter(
        personality_path=str(ROOT / "data" / "personality" / "instances" / "personality_core_instance.json"),
        user_profile_path=str(ROOT / "data" / "users" / "instances" / "user_celine_instance.json"),
        allow_templates=False
    )
    adapter.validate_required_sections()
    check(True, f"PersonalityAdapter chargé : {repr(adapter)}")

    # Test des 6 scénarios types
    scenarios = [
        ("Bonjour, aide-moi a organiser ma semaine",          None,      None,   "neutral_assistant"),
        ("Strategie produit ALFRED pour B2B demain",          None,      None,   "strategic_mode"),
        ("je suis vraiment epuisee la",                       "stress",  "low",  "low_energy_mode"),
        ("Montre-moi comment coder le scoring Q09",           None,      None,   "technical_mode"),
        ("Cree-moi un concept de branding pour ALFRED",       None,      None,   "creative_mode"),
        ("je suis stressee et depassee par les evenements",   "stress",  None,   "emotional_support_light"),
    ]

    all_modes_ok = True
    for msg, emotion, energy, expected_mode in scenarios:
        ctx = adapter.build_response_context(msg, emotion, energy)
        actual_mode = ctx["adaptation"]["mode"]
        tone = ctx["adaptation"]["tone"]
        ok = (actual_mode == expected_mode)
        if not ok:
            all_modes_ok = False
        status = PASS if ok else WARN
        print(f"  {status} [{expected_mode:28s}] tone={tone[:45]!r}...")
        if not ok:
            warnings.append(f"Mode attendu '{expected_mode}', obtenu '{actual_mode}' pour: {msg[:40]!r}")

    check(all_modes_ok, "Tous les modes de détection corrects", warn_only=True)

    # Vérifier que le tone par défaut reflète le profil psychométrique
    ctx_default = adapter.build_response_context("Bonjour Alfred")
    tone_default = ctx_default["adaptation"]["tone"]
    check(
        "chaleureux" in tone_default or "direct" in tone_default,
        f"Tone par défaut contient 'chaleureux' ou 'direct' → {tone_default!r}"
    )
    check(
        ctx_default["user"]["preferred_name"] == "Céline",
        "Preferred name = Céline"
    )

except Exception as e:
    print(f"{FAIL} PersonalityAdapter erreur : {e}")
    errors.append(str(e))

# ---------------------------------------------------------------------------
# Résumé
# ---------------------------------------------------------------------------

print("\n" + "=" * 60)
print("  RÉSUMÉ")
print("=" * 60)
print(f"  Erreurs   : {len(errors)}")
print(f"  Warnings  : {len(warnings)}")

if errors:
    print("\n  ERREURS :")
    for e in errors:
        print(f"    - {e}")

if warnings:
    print("\n  WARNINGS :")
    for w in warnings:
        print(f"    - {w}")

if not errors:
    print("\n  Profil psychométrique → ALFRED : intégration complète et fonctionnelle.")
    print("  Prêt pour le test main.py ✓")
else:
    print("\n  Des erreurs sont à corriger avant le test main.py.")

sys.exit(0 if not errors else 1)
