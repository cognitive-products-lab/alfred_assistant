"""
Branchement complet des nouveaux domaines dans taxonomy.json et domain_links.json.

Corrections :
  - cuisine : structure malformee (liste au lieu de dict) -> remplacee par structure complete
  - culture/manga : absent -> ajoute avec intents + linked_knowledge
  - intent_routing_rules : manquant pour cuisine / manga / communication / cognition
  - loading_policy.optional_domains : manquant cuisine / cognition / communication
  - domain_links.json : liens cross-domaines pour tous les nouveaux domaines
"""
import json
from pathlib import Path

ROOT = Path("D:/PROJET_ALFRED/ALFRED_PC/knowledges")
TAXONOMY_PATH  = ROOT / "taxonomy.json"
LINKS_PATH     = ROOT / "domain_links.json"

# ─────────────────────────────────────────────────────────────────────────────
# 1. TAXONOMY.JSON
# ─────────────────────────────────────────────────────────────────────────────
tax = json.loads(TAXONOMY_PATH.read_text(encoding="utf-8"))

# ── 1a. Remplacer cuisine (malformee) par structure complete ─────────────────
tax["domains"]["cuisine"] = {
    "label": "Cuisine et art culinaire",
    "description": "Techniques de cuisine, recettes, cuisines du monde, patisserie et culture culinaire.",
    "priority": "medium",
    "safety_note": None,
    "subdomains": {
        "fondamentaux": {
            "label": "Fondamentaux culinaires",
            "intents": [
                "explain_cooking_technique",
                "recommend_equipment",
                "explain_seasoning",
                "explain_knife_skills",
                "explain_sauce",
                "explain_cooking_method"
            ],
            "linked_knowledge": [
                "cuisine.fondamentaux.assaisonnement",
                "cuisine.fondamentaux.couteaux_et_decoupe",
                "cuisine.fondamentaux.cuissons_fondamentales",
                "cuisine.fondamentaux.equipement_base",
                "cuisine.fondamentaux.sauces_bases"
            ]
        },
        "francaise": {
            "label": "Cuisine francaise",
            "intents": [
                "explain_french_cuisine",
                "recommend_french_recipe",
                "explain_pastry",
                "explain_french_technique"
            ],
            "linked_knowledge": [
                "cuisine.francaise.cuisine_francaise_bases",
                "cuisine.francaise.patisserie_bases"
            ]
        },
        "asiatique": {
            "label": "Cuisines asiatiques",
            "intents": [
                "explain_japanese_cuisine",
                "explain_chinese_cuisine",
                "explain_thai_cuisine",
                "explain_korean_cuisine",
                "explain_vietnamese_cuisine",
                "explain_indian_cuisine",
                "recommend_asian_recipe",
                "explain_asian_ingredient",
                "explain_dashi",
                "explain_ramen",
                "explain_curry",
                "explain_kimchi",
                "explain_pho",
                "explain_wok_technique"
            ],
            "linked_knowledge": [
                "cuisine.asiatique.cuisine_chinoise",
                "cuisine.asiatique.cuisine_coreenne",
                "cuisine.asiatique.cuisine_indienne",
                "cuisine.asiatique.cuisine_japonaise",
                "cuisine.asiatique.cuisine_thaie",
                "cuisine.asiatique.cuisine_vietnamienne"
            ]
        }
    }
}

# ── 1b. Ajouter culture/manga (absent) ───────────────────────────────────────
tax["domains"]["culture"]["subdomains"]["manga"] = {
    "label": "Manga, anime et culture japonaise pop",
    "intents": [
        "recommend_manga",
        "explain_manga_genre",
        "discuss_one_piece",
        "discuss_naruto",
        "discuss_attack_on_titan",
        "discuss_demon_slayer",
        "discuss_dragon_ball",
        "discuss_berserk",
        "discuss_jujutsu_kaisen",
        "explain_ghibli",
        "explain_anime_culture",
        "explain_manga_history",
        "compare_manga_webtoon",
        "discuss_junji_ito",
        "explain_mangaka_profession",
        "compare_manga_bd_franco_belge"
    ],
    "linked_knowledge": [
        "culture.manga.anime_culture",
        "culture.manga.attack_on_titan",
        "culture.manga.berserk",
        "culture.manga.demon_slayer",
        "culture.manga.dragon_ball",
        "culture.manga.franco_belge_vs_manga",
        "culture.manga.jujutsu_kaisen",
        "culture.manga.junji_ito_horror",
        "culture.manga.manga_genres",
        "culture.manga.manga_history",
        "culture.manga.manga_vs_webtoon",
        "culture.manga.mangaka_creation",
        "culture.manga.naruto",
        "culture.manga.one_piece",
        "culture.manga.studio_ghibli_anime"
    ]
}

# ── 1c. intent_routing_rules — ajouter les nouvelles regles ──────────────────
routing = tax["intent_routing_rules"]

routing["communication_request"] = [
    "communication.verbal",
    "communication.written",
    "communication.influence",
    "communication.digital",
    "communication.nonverbal"
]
routing["cognition_thinking_request"] = [
    "cognition.systeme_pensee",
    "human.cognition",
    "human.psychology"
]
routing["cuisine_cooking_request"] = [
    "cuisine.fondamentaux",
    "cuisine.asiatique",
    "cuisine.francaise"
]
routing["manga_anime_culture_request"] = [
    "culture.manga",
    "culture.general"
]

# ── 1d. loading_policy — ajouter les nouveaux domaines ──────────────────────
optional = tax["loading_policy"]["optional_domains"]
for dom in ["communication", "cognition", "cuisine"]:
    if dom not in optional:
        optional.append(dom)

# ── 1e. Metadonnees ──────────────────────────────────────────────────────────
tax["version"] = "3.2.0"
tax["last_updated"] = "2026-06-23"

# Recompter les sous-domaines
count = 0
for domain in tax["domains"].values():
    subs = domain.get("subdomains", {})
    if isinstance(subs, dict):
        count += len(subs)
    elif isinstance(subs, list):
        count += len(subs)
tax["total_subdomains"] = count

TAXONOMY_PATH.write_text(json.dumps(tax, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"taxonomy.json mis a jour — version {tax['version']}, {count} sous-domaines")

# ─────────────────────────────────────────────────────────────────────────────
# 2. DOMAIN_LINKS.JSON — nouveaux liens cross-domaines
# ─────────────────────────────────────────────────────────────────────────────
links_data = json.loads(LINKS_PATH.read_text(encoding="utf-8"))

new_links = [
    # ── CUISINE → autres domaines ────────────────────────────────────────────
    {
        "source": "cuisine.asiatique.cuisine_japonaise",
        "targets": [
            "cuisine.fondamentaux.sauces_bases",
            "cuisine.fondamentaux.cuissons_fondamentales",
            "culture.manga.anime_culture"
        ],
        "relationship": "japanese_cuisine_and_culture"
    },
    {
        "source": "cuisine.fondamentaux.assaisonnement",
        "targets": [
            "cuisine.fondamentaux.sauces_bases",
            "cuisine.fondamentaux.cuissons_fondamentales",
            "lifestyle.health.fatigue_management"
        ],
        "relationship": "seasoning_and_cooking_basics"
    },
    {
        "source": "cuisine.francaise.patisserie_bases",
        "targets": [
            "cuisine.fondamentaux.assaisonnement",
            "cuisine.francaise.cuisine_francaise_bases",
            "cognition.systeme_pensee.attention_focus"
        ],
        "relationship": "patisserie_precision_and_focus"
    },
    {
        "source": "cuisine.asiatique.cuisine_coreenne",
        "targets": [
            "cuisine.asiatique.cuisine_japonaise",
            "cuisine.asiatique.cuisine_chinoise",
            "culture.manga.anime_culture"
        ],
        "relationship": "asian_cuisine_cross_reference"
    },
    # ── CULTURE/MANGA → autres domaines ─────────────────────────────────────
    {
        "source": "culture.manga.manga_history",
        "targets": [
            "culture.general.history_basics",
            "culture.general.art_culture_basics",
            "culture.manga.manga_genres"
        ],
        "relationship": "manga_cultural_history"
    },
    {
        "source": "culture.manga.attack_on_titan",
        "targets": [
            "cognition.systeme_pensee.critical_thinking",
            "human.emotional_intelligence.empathy",
            "culture.manga.manga_genres"
        ],
        "relationship": "dark_narrative_and_critical_thinking"
    },
    {
        "source": "culture.manga.berserk",
        "targets": [
            "human.psychology.resilience",
            "cognition.systeme_pensee.mental_models_toolkit",
            "culture.manga.manga_genres"
        ],
        "relationship": "dark_fantasy_and_resilience"
    },
    {
        "source": "culture.manga.studio_ghibli_anime",
        "targets": [
            "culture.general.art_culture_basics",
            "human.emotional_intelligence.emotional_support",
            "culture.manga.anime_culture"
        ],
        "relationship": "ghibli_art_and_emotion"
    },
    {
        "source": "culture.manga.franco_belge_vs_manga",
        "targets": [
            "culture.general.art_culture_basics",
            "culture.general.history_basics",
            "culture.manga.manga_history"
        ],
        "relationship": "comics_cultural_comparison"
    },
    # ── COGNITION → communication / professional ──────────────────────────────
    {
        "source": "cognition.systeme_pensee.system1_system2",
        "targets": [
            "communication.verbal.difficult_conversations",
            "communication.influence.negotiation",
            "human.psychology.cognitive_biases",
            "cognition.systeme_pensee.heuristiques"
        ],
        "relationship": "dual_process_and_communication"
    },
    {
        "source": "cognition.systeme_pensee.mental_models_toolkit",
        "targets": [
            "professional.decision.decision_models",
            "professional.decision.tradeoff_analysis",
            "cpl.strategy.strategy_fundamentals"
        ],
        "relationship": "mental_models_and_strategy"
    },
    {
        "source": "cognition.systeme_pensee.critical_thinking",
        "targets": [
            "communication.verbal.questioning_techniques",
            "communication.verbal.difficult_conversations",
            "professional.decision.root_cause_analysis"
        ],
        "relationship": "critical_thinking_and_argumentation"
    },
    # ── COMMUNICATION → cognition / professional ──────────────────────────────
    {
        "source": "communication.influence.persuasion_principles",
        "targets": [
            "cognition.systeme_pensee.cognitive_biases_extended",
            "cognition.systeme_pensee.heuristiques",
            "communication.influence.negotiation"
        ],
        "relationship": "persuasion_and_bias_awareness"
    },
    {
        "source": "communication.digital.social_media_communication",
        "targets": [
            "cpl.business_strategy.competitive_positioning",
            "cpl.human_communication.communication_principles",
            "communication.written.storytelling"
        ],
        "relationship": "social_media_and_brand"
    },
    {
        "source": "communication.verbal.conflict_resolution",
        "targets": [
            "human.interaction.de_escalation",
            "human.emotional_intelligence.emotional_regulation",
            "cognition.systeme_pensee.decision_making_cognitive"
        ],
        "relationship": "conflict_resolution_and_emotion"
    }
]

# Deduplication par source+targets
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
        print(f"  + link: {link['source']} -> {link['relationship']}")

links_data["version"] = "2.2.0"
links_data["last_update"] = "2026-06-23"

LINKS_PATH.write_text(json.dumps(links_data, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"\ndomain_links.json mis a jour — {added} nouveaux liens, {len(links_data['links'])} total")
print("\nDone. Tous les nouveaux domaines sont branches.")
