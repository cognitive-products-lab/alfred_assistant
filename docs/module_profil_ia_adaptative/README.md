# Module — Profil Utilisateur, IA Adaptative & Gouvernance 360°
## Documentation complète — Cognitive Products Lab

> Version 1.0 — 2026-06-16  
> Statut : En cours (phases 1-2 complètes, phase 3 en cours)  
> Produits couverts : ALFRED (B2C), ALFRED CPL (B2B), ARTHUR (enfants < 16 ans, V2 planifiée)

> **Non branché dans l'app live.** `QuestionnaireSession` (`src/profile/profile_analyzer.py`) coexiste volontairement avec `src/health/onboarding.py` (flux conversationnel réellement utilisé dans `main.py`) et `src/core/profile_analyzer.py` (CLI manuel, voir [`docs/profil_systeme/`](../profil_systeme/README.md)). Voir ce dernier README pour le tableau des 3 pipelines — clarifié le 17/08/2026, ce n'est pas un doublon à supprimer.

---

## Arborescence du dossier

```
docs/module_profil_ia_adaptative/
│
├── README.md                          ← Ce fichier — index et navigation
│
├── cadrage/
│   └── dossier_cadrage.html           ← Dossier de cadrage complet (export PDF)
│
├── conception/
│   ├── architecture_technique.md      ← Architecture globale du module
│   ├── dimensions_psychologiques.md   ← Les 9 dimensions avec justifications scientifiques
│   └── pipeline_scoring.md            ← Pipeline complet de scoring (D→M→A→I→C)
│
├── implementation/
│   ├── api_reference.md               ← Documentation des classes et méthodes Python
│   └── guide_integration.md           ← Comment intégrer dans ALFRED
│
├── gouvernance/
│   └── synthese_gouvernance.md        ← Vue synthétique gouvernance 360° du module
│
├── arthur/
│   └── conception_arthur.md           ← Architecture ARTHUR V2 (profil enfant)
│
└── tests/
    ├── README.md                      ← Guide de lancement des tests
    ├── test_profile_analyzer.py       ← Tests unitaires QuestionnaireSession
    ├── test_personality_adapter.py    ← Tests unitaires PersonalityAdapter
    ├── test_scoring.py                ← Tests du pipeline de scoring
    ├── fixtures/
    │   ├── sample_answers.json        ← Réponses de test pour les 4 questionnaires
    │   └── expected_scores.json       ← Scores attendus (référence de validation)
    └── integration/
        └── test_full_pipeline.py      ← Tests d'intégration end-to-end
```

---

## Liens rapides

| Document | Description | Statut |
|----------|-------------|--------|
| [Dossier de cadrage](cadrage/dossier_cadrage.html) | Introduction, enjeux, risques, ROI, RACI, livrables | ✅ Complet |
| [Architecture technique](conception/architecture_technique.md) | Diagrammes, flux de données, composants | ✅ Complet |
| [Dimensions psychologiques](conception/dimensions_psychologiques.md) | 9 dimensions, frameworks scientifiques, scoring | ✅ Complet |
| [Pipeline de scoring](conception/pipeline_scoring.md) | DMAIC appliqué, calculs, normalisation | ✅ Complet |
| [API Reference](implementation/api_reference.md) | Classes, méthodes, paramètres, exemples | ✅ Complet |
| [Guide d'intégration](implementation/guide_integration.md) | Comment utiliser dans ALFRED | ✅ Complet |
| [Synthèse gouvernance](gouvernance/synthese_gouvernance.md) | RGPD, AI Act, SOC, traçabilité | ✅ Complet |
| [Conception ARTHUR](arthur/conception_arthur.md) | Profil enfant V2, contrôle parental | ✅ Complet |
| [Tests](tests/README.md) | Suite de tests pytest | ✅ Complet |

---

## Fichiers sources associés

### Données
```
data/profile/
├── user_profile.json                  ← Profil réel Céline Rousselot (AssessFirst + questionnaires)
├── answers_template.json              ← Template de réponses aux questionnaires
├── questionnaire_profil_complementaire.md  ← Q00 — 23 questions qualitatives
├── questionnaires/                    ← 8 questionnaires scientifiques complets
│   ├── README.md
│   ├── 01_big_five_TIPI.md            ← TIPI (Big Five) — 10 items, Likert 7
│   ├── 02_intelligence_emotionnelle.md ← TEIQue-SF — 15 items, Likert 7
│   ├── 03_valeurs_schwartz.md          ← PVQ-21 — 21 items, Likert 6
│   ├── 04_chronotype_energie.md        ← rMEQ — 5 items + 10 items énergie
│   ├── 05_resilience_stress.md         ← CD-RISC-10 + PSS-4 — 14 items
│   ├── 06_riasec_interets_pro.md       ← RIASEC Holland — 18 items, Likert 5
│   ├── 07_engagement_burnout.md        ← UWES-9 + indicateur burnout — 12 items
│   └── 08_communication_conflit.md     ← TKI-inspiré — 5 modes, items hybrides
├── scoring/
│   ├── scoring_keys.json              ← Clés de scoring pour les 8 questionnaires (116 items)
│   └── answers_template.json          ← Template réponses avec session_state
└── schema/
    ├── dimensions_schema.json         ← 9 dimensions psychologiques + sous-dimensions
    ├── alfred_mapping_matrix.json     ← 40 règles + 4 combinaisons → 9 paramètres ALFRED
    └── periodicity_schema.json        ← Fréquences de re-passation
```

### Code source
```
src/
├── profile/
│   └── profile_analyzer.py            ← QuestionnaireSession — passation conversationnelle
└── core/
    ├── profile_analyzer.py            ← Analyseur complet avec CLI (variante)
    └── personality_adapter.py         ← PersonalityAdapter — adaptation comportementale ALFRED
```

### Gouvernance
```
docs/gouvernance/
├── blueprint_gouvernance_complet.md   ← Référentiel produit (1119 lignes)
├── cadre_reglementaire_CPL.md         ← RGPD, AI Act, NIS2, ANSSI, HDS
├── registre_traitements_CPL.md        ← Registre RGPD art.30 (7 traitements)
├── cartographie_donnees_CPL.md        ← 20 types de données, flux, accès
├── schema_tracabilite_donnees.json    ← Schéma audit trail complet
├── soc_cpl.md                         ← SOC 3 niveaux + playbooks
├── vision_performance_CPL.md          ← Triangle d'or + DMAIC + KPI
└── CHANTIER_AUDIT_CERTIFICATION.md    ← Roadmap certifications ISO/RGPD/AI Act
```

---

## Vue d'ensemble du module

### Objectif central
Personnaliser le comportement d'ALFRED selon un profil psychologique scientifiquement fondé de l'utilisateur, en respectant la vie privée et les réglementations les plus strictes.

### Les 9 dimensions psychologiques mesurées

| # | Dimension | Framework | Questionnaire |
|---|-----------|-----------|--------------|
| 1 | Big Five (personnalité) | TIPI / Gosling 2003 | 01_big_five_TIPI.md |
| 2 | Intelligence émotionnelle | TEIQue-SF / Petrides 2009 | 02_intelligence_emotionnelle.md |
| 3 | Valeurs fondamentales | PVQ-21 / Schwartz 2001 | 03_valeurs_schwartz.md |
| 4 | Chronotype & énergie | rMEQ / Adan & Almirall 1991 | 04_chronotype_energie.md |
| 5 | Résilience & stress | CD-RISC-10 + PSS-4 | 05_resilience_stress.md |
| 6 | Intérêts professionnels | RIASEC / Holland 1997 | 06_riasec_interets_pro.md |
| 7 | Engagement & burnout | UWES-9 / Schaufeli 2004 | 07_engagement_burnout.md |
| 8 | Communication & conflit | TKI / Thomas-Kilmann 1974 | 08_communication_conflit.md |
| 9 | Données AssessFirst | SWIPE-DRIVE-BRAIN | user_profile.json |

### Les 9 paramètres ALFRED dérivés

| Paramètre | Valeurs | Impact |
|-----------|---------|--------|
| `tone` | formel / équilibré / chaleureux / casual | Registre de langue |
| `response_length` | court / moyen / long / adaptatif | Longueur des réponses |
| `proactivity` | minimal / modéré / élevé | Initiative ALFRED |
| `emotional_support_level` | factuel / équilibré / empathique | Soutien émotionnel |
| `challenge_level` | confort / modéré / intense | Niveau de challenge |
| `check_in_frequency` | jamais / mensuel / hebdo / quotidien | Prise de nouvelles |
| `explanation_depth` | surface / standard / approfondi | Détail des explications |
| `humor_level` | aucun / sobre / présent | Humour dans les réponses |
| `structure_preference` | fluide / mixte / structuré | Format des réponses |

### Pipeline en 5 étapes (DMAIC)

```
QUESTIONNAIRES  →  SCORING  →  NORMALISATION  →  MAPPING  →  PARAMÈTRES ALFRED
(116 items)         (calculs      (0-100)          (matrice    (9 paramètres
                    par sous-                       40 règles)  comportementaux)
                    échelle)
```

---

## Démarrage rapide (pour les tests)

```bash
# Installer les dépendances de test
pip install pytest

# Lancer toute la suite de tests
pytest docs/module_profil_ia_adaptative/tests/ -v

# Lancer uniquement les tests unitaires
pytest docs/module_profil_ia_adaptative/tests/test_profile_analyzer.py -v

# Lancer les tests d'intégration
pytest docs/module_profil_ia_adaptative/tests/integration/ -v
```

---

## Roadmap du module

| Phase | Statut | Contenu |
|-------|--------|---------|
| Phase 1 — Fondations | ✅ Livré | Schémas, questionnaires, scoring_keys, templates |
| Phase 2 — Code | ✅ Livré | profile_analyzer.py, personality_adapter.py, answers_template |
| Phase 3 — Gouvernance | 🔄 En cours | PSSI formelle, AIPD T001/T004, SMSI |
| Phase 4 — ARTHUR V2 | 📋 Planifié | Profil enfant, contrôle parental, conformité renforcée |
| Phase 5 — Certification | 📋 Planifié (2027) | ISO 27001, audit ANSSI, HDS |

---

*Module créé le 2026-06-16 — Cognitive Products Lab*  
*Responsable : Céline Rousselot — DPO / RSSI / Lead Dev*
