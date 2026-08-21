"""
PROJECT      : ALFRED
BLOCK        : B18
FILE         : src/metrics/__init__.py
ROLE         : KPI ALFRED — approche Lean Six Sigma (Define/Measure)

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-08-21
UPDATED      : 2026-08-21

DESCRIPTION :
Voir docs/architecture/vision_knowledge_training_finetuning_alfred.md, P2
(document source, section 26 — KPI à mettre en place).

Package séparé de src/knowledge/ et src/training/ (et non imbriqué dans
l'un des deux) : les KPI du document source couvrent transversalement
Knowledge, External Dependency, RAG, Training, Fine-Tuning et Routing —
aucun des deux autres packages n'est le bon foyer pour une gouvernance qui
lit les deux.

- kpi_catalog.py (Define) : un KPI par ligne du document source, avec
  formule, source de donnée et statut de suivi OK/KO/OFF — jamais un
  chiffre inventé pour un statut KO/OFF.
- kpi_compute.py (Measure) : fonctions de calcul réel, une seule par KPI de
  statut OK ou KO — aucune fonction pour un KPI OFF (structurellement non
  mesurable aujourd'hui, un stub renverrait un faux sentiment de mesure).
- request_log.py : dénominateur manquant identifié en Define — journal
  minimal de CHAQUE requête (pas seulement les échecs, à la différence de
  src.knowledge.gap_dataset), sans texte de requête pour rester sobre en
  données sur 100% du trafic.
"""
