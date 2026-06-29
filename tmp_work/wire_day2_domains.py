"""
Branchement complet des domaines Day 2 dans taxonomy.json et domain_links.json.
Nouveaux domaines :
  - culture/webtoon       (10 KU)
  - human/humour          (10 KU)
  - human/seduction_relations (10 KU)
  - human/vie_privee      (10 KU)
  - cpl/usage_professionnel (12 KU)
  - culture/romance        (7 KU : sans booktok_community dans linked_knowledge direct)
"""
import json
from pathlib import Path

ROOT = Path("D:/PROJET_ALFRED/ALFRED_PC/knowledges")
TAXONOMY_PATH = ROOT / "taxonomy.json"
LINKS_PATH = ROOT / "domain_links.json"

tax = json.loads(TAXONOMY_PATH.read_text(encoding="utf-8"))
links_data = json.loads(LINKS_PATH.read_text(encoding="utf-8"))

# ═══════════════════════════════════════════════════════════════════════════
# 1. TAXONOMY.JSON — nouveaux subdomains
# ═══════════════════════════════════════════════════════════════════════════

# ── culture/webtoon ────────────────────────────────────────────────────────
tax["domains"]["culture"]["subdomains"]["webtoon"] = {
    "label": "Webtoon et manhwa coréen",
    "intents": [
        "recommend_webtoon", "explain_webtoon_format", "discuss_solo_leveling",
        "discuss_tower_of_god", "discuss_omniscient_reader", "discuss_webtoon_romance",
        "discuss_manhwa_romance_fantasy", "discuss_webtoon_horror", "explain_webtoon_creation",
        "discuss_bl_webtoon", "compare_webtoon_manga_industry", "recommend_manhwa_fantasy",
        "explain_booktok_books", "discuss_webtoon_platforms"
    ],
    "linked_knowledge": [
        "culture.webtoon.webtoon_overview",
        "culture.webtoon.solo_leveling",
        "culture.webtoon.tower_of_god",
        "culture.webtoon.omniscient_reader",
        "culture.webtoon.webtoon_romance",
        "culture.webtoon.webtoon_horror_thriller",
        "culture.webtoon.webtoon_creation",
        "culture.webtoon.manhwa_romance_fantasy",
        "culture.webtoon.webtoon_bl_genre",
        "culture.webtoon.webtoon_vs_manga_industry"
    ]
}

# ── culture/romance ────────────────────────────────────────────────────────
tax["domains"]["culture"]["subdomains"]["romance"] = {
    "label": "Romance littéraire et New Adult",
    "intents": [
        "recommend_romance_book", "discuss_jay_crownover", "discuss_marked_men",
        "discuss_saints_of_denver", "explain_new_adult_genre", "explain_romance_tropes",
        "discuss_enemies_to_lovers", "discuss_second_chance_romance", "discuss_booktok",
        "recommend_colleen_hoover", "explain_hea_romance", "discuss_fantasy_romance",
        "recommend_romance_by_mood", "discuss_romance_authors"
    ],
    "linked_knowledge": [
        "culture.romance.jay_crownover_overview",
        "culture.romance.marked_men_serie",
        "culture.romance.saints_of_denver",
        "culture.romance.new_adult_genre",
        "culture.romance.romance_tropes",
        "culture.romance.romance_lecture",
        "culture.romance.booktok_community"
    ]
}

# ── human/humour ──────────────────────────────────────────────────────────
if "humour" not in tax["domains"]["human"]["subdomains"]:
    tax["domains"]["human"]["subdomains"]["humour"] = {}

tax["domains"]["human"]["subdomains"]["humour"] = {
    "label": "Humour, rire et comédie",
    "intents": [
        "explain_humor_mechanics", "explain_self_deprecation", "explain_contextual_humor",
        "explain_irony_sarcasm", "explain_professional_humor", "discuss_standup_comedy",
        "explain_absurd_humor", "explain_french_humor", "explain_laughter_health",
        "explain_humor_seduction", "recommend_comedy", "explain_why_something_is_funny"
    ],
    "linked_knowledge": [
        "human.humour.humour_mecanismes",
        "human.humour.autodérision",
        "human.humour.humour_contextuel",
        "human.humour.ironie_sarcasme",
        "human.humour.humour_professionnel",
        "human.humour.stand_up_culture",
        "human.humour.humour_absurde",
        "human.humour.humour_francais",
        "human.humour.rire_et_sante",
        "human.humour.humour_seduction"
    ]
}

# ── human/seduction_relations ─────────────────────────────────────────────
tax["domains"]["human"]["subdomains"]["seduction_relations"] = {
    "label": "Séduction, relations amoureuses et attachement",
    "intents": [
        "explain_seduction_basics", "explain_first_impression", "explain_couple_communication",
        "explain_love_languages", "explain_long_term_relationship", "explain_attachment_styles",
        "explain_online_dating", "explain_breakup_grief", "explain_long_distance_relationship",
        "explain_sexuality_communication", "explain_attraction_psychology",
        "explain_dating_apps", "explain_anxious_avoidant_dynamic"
    ],
    "linked_knowledge": [
        "human.seduction_relations.seduction_bases",
        "human.seduction_relations.premier_contact",
        "human.seduction_relations.communication_amoureuse",
        "human.seduction_relations.langages_amour",
        "human.seduction_relations.relation_longue_duree",
        "human.seduction_relations.attachement_styles",
        "human.seduction_relations.seduction_en_ligne",
        "human.seduction_relations.rupture_deuil",
        "human.seduction_relations.relation_a_distance",
        "human.seduction_relations.sexualite_et_communication"
    ]
}

# ── human/vie_privee ─────────────────────────────────────────────────────
tax["domains"]["human"]["subdomains"]["vie_privee"] = {
    "label": "Vie privée, intimité et frontières personnelles",
    "intents": [
        "explain_personal_intimacy", "explain_personal_boundaries", "explain_digital_privacy",
        "explain_solitude_vs_isolation", "explain_secrets_trust", "explain_right_to_disconnect",
        "explain_body_autonomy", "explain_grief_loss", "explain_personal_space",
        "explain_identity_self_image", "explain_privacy_protection", "explain_saying_no"
    ],
    "linked_knowledge": [
        "human.vie_privee.intimite_personnelle",
        "human.vie_privee.frontieres_personnelles",
        "human.vie_privee.vie_privee_numerique",
        "human.vie_privee.solitude_et_isolement",
        "human.vie_privee.secrets_et_confiance",
        "human.vie_privee.droit_a_la_deconnexion",
        "human.vie_privee.corps_et_limites",
        "human.vie_privee.deuil_et_perte",
        "human.vie_privee.espace_personnel",
        "human.vie_privee.identite_et_image"
    ]
}

# ── cpl/usage_professionnel ───────────────────────────────────────────────
if "usage_professionnel" not in tax["domains"]["cpl"]["subdomains"]:
    tax["domains"]["cpl"]["subdomains"]["usage_professionnel"] = {}

tax["domains"]["cpl"]["subdomains"]["usage_professionnel"] = {
    "label": "Usages professionnels CPL et ALFRED",
    "intents": [
        "prepare_client_brief", "prepare_pitch", "manage_ia_project",
        "strategic_watch_ai", "prepare_direction_report", "handle_difficult_client",
        "alfred_internal_usage", "write_commercial_proposal", "onboard_team_member",
        "analyze_competitors_cpl", "negotiate_contract", "cpl_external_communication",
        "prepare_client_meeting", "cpl_positioning", "cpl_differentiation"
    ],
    "linked_knowledge": [
        "cpl.usage_professionnel.brief_client",
        "cpl.usage_professionnel.pitch_client",
        "cpl.usage_professionnel.gestion_projet_ia",
        "cpl.usage_professionnel.veille_strategique",
        "cpl.usage_professionnel.reporting_direction",
        "cpl.usage_professionnel.gestion_client_difficile",
        "cpl.usage_professionnel.alfred_usage_interne",
        "cpl.usage_professionnel.proposition_commerciale",
        "cpl.usage_professionnel.onboarding_collaborateur",
        "cpl.usage_professionnel.analyse_concurrents",
        "cpl.usage_professionnel.negociation_contrat",
        "cpl.usage_professionnel.communication_cpl"
    ]
}

# ── intent_routing_rules — nouveaux domaines ─────────────────────────────
routing = tax["intent_routing_rules"]

routing["webtoon_manhwa_request"] = [
    "culture.webtoon",
    "culture.manga"
]
routing["romance_literature_request"] = [
    "culture.romance",
    "culture.general"
]
routing["humor_comedy_request"] = [
    "human.humour",
    "human.social_behavior"
]
routing["seduction_relations_request"] = [
    "human.seduction_relations",
    "human.emotional_intelligence",
    "human.psychology"
]
routing["vie_privee_intimacy_request"] = [
    "human.vie_privee",
    "human.social_behavior",
    "system.privacy"
]
routing["cpl_professional_request"] = [
    "cpl.usage_professionnel",
    "cpl.strategy",
    "professional.product_management"
]

# ── loading_policy — ajouter les nouveaux domaines ────────────────────────
optional = tax["loading_policy"]["optional_domains"]
for dom in ["culture", "human", "cpl"]:
    if dom not in optional:
        optional.append(dom)

# ── Metadonnées ───────────────────────────────────────────────────────────
# Recompter les sous-domaines
count = 0
for domain in tax["domains"].values():
    subs = domain.get("subdomains", {})
    if isinstance(subs, dict):
        count += len(subs)
    elif isinstance(subs, list):
        count += len(subs)

tax["version"] = "3.3.0"
tax["last_updated"] = "2026-06-23"
tax["total_subdomains"] = count

TAXONOMY_PATH.write_text(json.dumps(tax, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"taxonomy.json mis a jour — version {tax['version']}, {count} sous-domaines")

# ═══════════════════════════════════════════════════════════════════════════
# 2. DOMAIN_LINKS.JSON — nouveaux liens cross-domaines
# ═══════════════════════════════════════════════════════════════════════════

new_links = [
    # ── webtoon → manga + séduction + humour ──────────────────────────────
    {
        "source": "culture.webtoon.webtoon_romance",
        "targets": ["culture.romance.romance_tropes", "human.seduction_relations.langages_amour", "culture.manga.manga_genres"],
        "relationship": "webtoon_romance_and_tropes"
    },
    {
        "source": "culture.webtoon.solo_leveling",
        "targets": ["culture.manga.manga_vs_webtoon", "culture.webtoon.webtoon_vs_manga_industry", "cognition.systeme_pensee.flow_state"],
        "relationship": "solo_leveling_cross_media"
    },
    {
        "source": "culture.webtoon.manhwa_romance_fantasy",
        "targets": ["culture.romance.romance_tropes", "culture.romance.new_adult_genre", "culture.webtoon.webtoon_romance"],
        "relationship": "manhwa_romance_genre_connections"
    },
    # ── romance → humour + séduction ─────────────────────────────────────
    {
        "source": "culture.romance.romance_tropes",
        "targets": ["human.seduction_relations.seduction_bases", "culture.romance.new_adult_genre", "culture.webtoon.webtoon_romance"],
        "relationship": "romance_tropes_and_real_seduction"
    },
    {
        "source": "culture.romance.jay_crownover_overview",
        "targets": ["culture.romance.marked_men_serie", "culture.romance.new_adult_genre", "human.seduction_relations.attachement_styles"],
        "relationship": "crownover_universe_connections"
    },
    {
        "source": "culture.romance.booktok_community",
        "targets": ["culture.webtoon.webtoon_overview", "culture.romance.romance_lecture", "communication.digital.social_media_communication"],
        "relationship": "booktok_social_media_reading"
    },
    # ── humour → séduction + bien-être ────────────────────────────────────
    {
        "source": "human.humour.humour_seduction",
        "targets": ["human.seduction_relations.seduction_bases", "human.seduction_relations.premier_contact", "human.humour.humour_mecanismes"],
        "relationship": "humor_as_seduction_tool"
    },
    {
        "source": "human.humour.rire_et_sante",
        "targets": ["human.vie_privee.solitude_et_isolement", "lifestyle.health.stress_management", "human.humour.humour_mecanismes"],
        "relationship": "laughter_health_benefits"
    },
    {
        "source": "human.humour.humour_professionnel",
        "targets": ["cpl.usage_professionnel.communication_cpl", "communication.verbal.feedback_culture", "human.humour.autodérision"],
        "relationship": "professional_humor_leadership"
    },
    {
        "source": "human.humour.autodérision",
        "targets": ["human.vie_privee.identite_et_image", "human.seduction_relations.seduction_bases", "human.humour.humour_contextuel"],
        "relationship": "self_deprecation_confidence"
    },
    # ── séduction → vie privée + attachement ─────────────────────────────
    {
        "source": "human.seduction_relations.attachement_styles",
        "targets": ["human.vie_privee.intimite_personnelle", "human.seduction_relations.communication_amoureuse", "human.emotional_intelligence.emotional_regulation"],
        "relationship": "attachment_and_intimacy"
    },
    {
        "source": "human.seduction_relations.communication_amoureuse",
        "targets": ["communication.verbal.active_listening", "human.seduction_relations.langages_amour", "human.vie_privee.secrets_et_confiance"],
        "relationship": "couple_communication_skills"
    },
    {
        "source": "human.seduction_relations.rupture_deuil",
        "targets": ["human.vie_privee.deuil_et_perte", "human.emotional_intelligence.emotional_support", "human.vie_privee.solitude_et_isolement"],
        "relationship": "breakup_and_grief_connections"
    },
    # ── vie privée → digital + bien-être ─────────────────────────────────
    {
        "source": "human.vie_privee.vie_privee_numerique",
        "targets": ["professional.standards_iso.iso_27701_privacy_management", "human.vie_privee.droit_a_la_deconnexion", "system.privacy"],
        "relationship": "digital_privacy_and_governance"
    },
    {
        "source": "human.vie_privee.frontieres_personnelles",
        "targets": ["human.seduction_relations.seduction_bases", "human.vie_privee.corps_et_limites", "human.emotional_intelligence.emotional_regulation"],
        "relationship": "boundaries_in_relationships"
    },
    # ── CPL usage pro → cognition + communication ─────────────────────────
    {
        "source": "cpl.usage_professionnel.brief_client",
        "targets": ["communication.verbal.active_listening", "cognition.systeme_pensee.critical_thinking", "cpl.usage_professionnel.proposition_commerciale"],
        "relationship": "client_brief_methodology"
    },
    {
        "source": "cpl.usage_professionnel.gestion_client_difficile",
        "targets": ["communication.verbal.conflict_resolution", "communication.influence.negotiation", "cpl.usage_professionnel.negociation_contrat"],
        "relationship": "client_conflict_resolution"
    },
    {
        "source": "cpl.usage_professionnel.alfred_usage_interne",
        "targets": ["cpl.usage_professionnel.brief_client", "cpl.usage_professionnel.reporting_direction", "cpl.usage_professionnel.communication_cpl"],
        "relationship": "alfred_internal_productivity"
    },
    {
        "source": "cpl.usage_professionnel.communication_cpl",
        "targets": ["communication.written.storytelling", "communication.digital.social_media_communication", "cpl.strategy.value_proposition_framework"],
        "relationship": "cpl_brand_communication"
    }
]

# Deduplication
existing_sources = {
    (l["source"], tuple(sorted(l["targets"]))): True
    for l in links_data["links"]
}

added = 0
for link in new_links:
    key = (link["source"], tuple(sorted(link["targets"])))
    if key not in existing_sources:
        links_data["links"].append(link)
        existing_sources[key] = True
        added += 1
        print(f"  + {link['source']} -> {link['relationship']}")

links_data["version"] = "2.3.0"
links_data["last_update"] = "2026-06-23"

LINKS_PATH.write_text(json.dumps(links_data, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"\ndomain_links.json -> v{links_data['version']}, {added} nouveaux liens, {len(links_data['links'])} total")
print(f"taxonomy.json -> v{tax['version']}, {count} sous-domaines")
print("\nDone. 60 KU branches.")
