"""
PROJECT      : ALFRED
BLOCK        : B18
FUNCTION     : SMOKE
FILE         : tests/b18_tests/test_smoke_knowledge_batch1.py
ROLE         : Smoke tests (lot 1) pour les 63 fichiers de connaissance
               generale B18 avec contenu reel (cinema, environnement,
               sociologie, economie, sport, linguistique, droit,
               architecture, nutrition, psychologie, softskills).

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-07-05
UPDATED      : 2026-07-05
VERSION      : V1.0
STATUS       : TESTED

DESCRIPTION :
Verifie la structure de base ET que le contenu n'est pas un stub vide
(summary non vide) — a la difference des 75 fichiers B18 restants qui
sont des placeholders auto-generes ("recreated_from_dashboard_manifest")
sans contenu reel, traites separement (non promus, voir validation_registry.json).
"""

import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]

KNOWLEDGE_FILES = [
    "knowledges/human/psychology/behavioral_patterns.json",
    "knowledges/human/psychology/motivation.json",
    "knowledges/human/skills/softskills/adaptability.json",
    "knowledges/human/skills/softskills/creativity.json",
    "knowledges/cinema/documentary_film.json",
    "knowledges/cinema/cinematography_basics.json",
    "knowledges/cinema/film_history.json",
    "knowledges/cinema/film_directors.json",
    "knowledges/cinema/film_genres.json",
    "knowledges/cinema/animation_history.json",
    "knowledges/environment/renewable_energy.json",
    "knowledges/environment/biodiversity_conservation.json",
    "knowledges/environment/environmental_policy.json",
    "knowledges/environment/climate_change_solutions.json",
    "knowledges/environment/water_resources.json",
    "knowledges/environment/sustainable_development.json",
    "knowledges/environment/circular_economy.json",
    "knowledges/sociology/cultural_sociology.json",
    "knowledges/sociology/social_stratification.json",
    "knowledges/sociology/sociology_fundamentals.json",
    "knowledges/sociology/sociology_of_organizations.json",
    "knowledges/sociology/collective_action.json",
    "knowledges/sociology/urban_sociology.json",
    "knowledges/sociology/deviance_social_control.json",
    "knowledges/economics/behavioral_economics.json",
    "knowledges/economics/macroeconomics_basics.json",
    "knowledges/economics/financial_markets.json",
    "knowledges/economics/international_trade.json",
    "knowledges/economics/microeconomics_basics.json",
    "knowledges/economics/personal_finance.json",
    "knowledges/economics/microeconomics_advanced.json",
    "knowledges/economics/history_of_economic_thought.json",
    "knowledges/economics/public_economics.json",
    "knowledges/sports_science/training_principles.json",
    "knowledges/sports_science/sports_psychology.json",
    "knowledges/sports_science/biomechanics_basics.json",
    "knowledges/sports_science/sports_physiology.json",
    "knowledges/sports_science/recovery_performance.json",
    "knowledges/linguistics/sociolinguistics.json",
    "knowledges/linguistics/syntax_morphology.json",
    "knowledges/linguistics/linguistics_fundamentals.json",
    "knowledges/linguistics/semantics_pragmatics.json",
    "knowledges/linguistics/phonetics_phonology.json",
    "knowledges/linguistics/language_acquisition.json",
    "knowledges/law/labor_law_basics.json",
    "knowledges/law/international_law.json",
    "knowledges/law/criminal_law_basics.json",
    "knowledges/law/law_basics.json",
    "knowledges/law/digital_law.json",
    "knowledges/law/constitutional_law.json",
    "knowledges/law/consumer_law.json",
    "knowledges/law/human_rights_law.json",
    "knowledges/architecture/architecture_history.json",
    "knowledges/architecture/interior_design_basics.json",
    "knowledges/architecture/sustainable_architecture.json",
    "knowledges/architecture/urban_planning.json",
    "knowledges/architecture/architectural_styles.json",
    "knowledges/nutrition/micronutrients_vitamins.json",
    "knowledges/nutrition/macronutrients_deep.json",
    "knowledges/nutrition/sports_nutrition.json",
    "knowledges/nutrition/nutrition_fundamentals.json",
    "knowledges/nutrition/dietary_patterns.json",
    "knowledges/nutrition/gut_microbiome.json",
]


@pytest.mark.parametrize("relpath", KNOWLEDGE_FILES)
def test_knowledge_json_has_real_content(relpath):
    data = json.loads((ROOT / relpath).read_text(encoding="utf-8"))
    for key in ("metadata", "knowledge_id", "title", "summary"):
        assert key in data, f"cle '{key}' manquante dans {relpath}"
    assert isinstance(data["summary"], str) and len(data["summary"].strip()) > 20, (
        f"summary suspicieusement vide/court dans {relpath}"
    )
