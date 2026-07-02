"""
PROJECT      : ALFRED
BLOCK        : Bloc 12.01 — Gestion de projet
DASHBOARD    : B10 — Collaboration & Coordination
FILE         : src/collaboration/project/__init__.py
ROLE         : Gestion de projet & stratégie — "cerveau projet" d'ALFRED

AUTHOR       : Cognitive Products Lab
CREATED      : 2026-07-02
VERSION      : V1.0
STATUS       : TO_TEST

DESCRIPTION :
Structure de données persistante (objectifs, tâches, jalons, dépendances,
statut, décisions, documents) qu'ALFRED peut lire et écrire pour raisonner
sur les projets suivis et se comporter en collaborateur stratégie / gestion
de projet (sous-code 12.01 du Bloc 12 — voir docs/ALFRED_BLOCS_REFERENCE.md).
"""
# ============================================================
# ALFRED — src/collaboration/project/__init__.py
# Bloc 12.01 — Gestion de projet (dashboard : B10)
#
# 🎯 UTILITÉ ALFRED :
#   Donne à ALFRED un état structuré des projets (au-delà de la mémoire
#   narrative) : objectifs, tâches, jalons, dépendances, blocages,
#   décisions et documents. Sert de base au raisonnement stratégique
#   (priorisation, prochaines actions, détection de blocages) et à
#   l'injection de contexte prompt.
#
# 🏗️ DOMAINE :
#   Collaboration professionnelle — SQLite local-first
# ============================================================
