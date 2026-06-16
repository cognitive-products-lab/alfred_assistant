# Conception technique — Système de profilage psychologique ALFRED

**Version** : 1.0  
**Date** : 2026-06-16  
**Auteur** : ALFRED Architecture Team  
**Statut** : Document de référence

---

## Table des matières

1. [Vue d'ensemble de l'architecture](#1-vue-densemble-de-larchitecture)
2. [Justification du choix des frameworks psychologiques](#2-justification-du-choix-des-frameworks-psychologiques)
3. [Décisions de conception et alternatives rejetées](#3-décisions-de-conception-et-alternatives-rejetées)
4. [Processus de collecte des réponses](#4-processus-de-collecte-des-réponses)
5. [Pipeline de calcul des scores](#5-pipeline-de-calcul-des-scores)
6. [Logique de la matrice de mapping](#6-logique-de-la-matrice-de-mapping)
7. [Système de périodicité](#7-système-de-périodicité)
8. [Intégration avec le moteur ALFRED existant](#8-intégration-avec-le-moteur-alfred-existant)
9. [Évolutions prévues](#9-évolutions-prévues)
10. [Limites et avertissements éthiques](#10-limites-et-avertissements-éthiques)

---

## 1. Vue d'ensemble de l'architecture

### Schéma ASCII — Architecture globale

```
╔══════════════════════════════════════════════════════════════════╗
║                    SYSTÈME DE PROFILAGE ALFRED                   ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                  ║
║  ┌─────────────────────────────────────────────────────────┐    ║
║  │  SOURCE EXTERNE                                          │    ║
║  │  data/profile/user_profile.json                         │    ║
║  │  ← AssessFirst (SWIPE + DRIVE + BRAIN)                  │    ║
║  │    [Source de vérité prioritaire pour Big Five]          │    ║
║  └─────────────────────────────────────────────────────────┘    ║
║                          │                                       ║
║                          ▼                                       ║
║  ┌─────────────────────────────────────────────────────────┐    ║
║  │  QUESTIONNAIRES (data/profile/questionnaires/)          │    ║
║  │                                                          │    ║
║  │  01_big_five_TIPI.md         (TIPI, 10 items)           │    ║
║  │  02_intelligence_emotionnelle.md  (TEIQue-SF, 15 items) │    ║
║  │  03_valeurs_schwartz.md      (PVQ-21, 21 items)         │    ║
║  │  04_chronotype_energie.md    (rMEQ+orig, 15 items)      │    ║
║  │  05_resilience_stress.md     (CD-RISC-10+PSS-4, 14)     │    ║
║  │  06_riasec_interets_pro.md   (Holland, 18 items)        │    ║
║  │  07_engagement_burnout.md    (UWES-9+orig, 14 items)    │    ║
║  │  08_communication_conflit.md (TKI-inspiré, 25 items)    │    ║
║  └────────────────────┬────────────────────────────────────┘    ║
║                       │ Réponses saisies                         ║
║                       ▼                                          ║
║  ┌─────────────────────────────────────────────────────────┐    ║
║  │  RÉPONSES BRUTES                                         │    ║
║  │  data/profile/scoring/answers_template.json             │    ║
║  │  [DONNÉES SENSIBLES — chiffrées après analyse]          │    ║
║  └────────────────────┬────────────────────────────────────┘    ║
║                       │                                          ║
║                       ▼                                          ║
║  ┌─────────────────────────────────────────────────────────┐    ║
║  │  SCORING ENGINE (src/core/profile_analyzer.py)          │    ║
║  │                                                          │    ║
║  │  ProfileAnalyzer                                         │    ║
║  │  ├── load_all()             ← charge les 4 sources      │    ║
║  │  ├── compute_scores()       ← calcul normalisé 0-100    │    ║
║  │  ├── generate_alfred_params() ← matrice de mapping      │    ║
║  │  ├── update_user_profile()  ← fusion + écriture JSON    │    ║
║  │  ├── encrypt_answers()      ← Fernet AES-128            │    ║
║  │  └── decrypt_answers()      ← déchiffrement             │    ║
║  └────────────────────┬────────────────────────────────────┘    ║
║                       │                                          ║
║          ┌────────────┼────────────┐                            ║
║          ▼            ▼            ▼                            ║
║  ┌──────────┐  ┌──────────┐  ┌─────────────────────────────┐   ║
║  │SCHEMA    │  │MAPPING   │  │  user_profile.json          │   ║
║  │dimensions│  │MATRIX    │  │  ← scores agrégés           │   ║
║  │_schema   │  │alfred_   │  │  ← alfred_derived_params    │   ║
║  │.json     │  │mapping_  │  │  ← fusion AssessFirst       │   ║
║  └──────────┘  │matrix    │  └────────────────┬────────────┘   ║
║                │.json     │                    │                ║
║  ┌──────────┐  └──────────┘                    ▼                ║
║  │PERIODICI-│                    ┌─────────────────────────┐    ║
║  │TY SCHEMA │                    │  BEHAVIOUR ENGINE       │    ║
║  │.json     │                    │  alfred_behavior_engine │    ║
║  └──────────┘                    │  .py                    │    ║
║                                  │  ← alfred_derived_params│    ║
║                                  └─────────────────────────┘    ║
╚══════════════════════════════════════════════════════════════════╝
```

### Composants principaux

| Composant | Fichier | Rôle |
|-----------|---------|------|
| Questionnaires | `data/profile/questionnaires/*.md` | Interface utilisateur — passation des tests |
| Réponses brutes | `data/profile/scoring/answers_template.json` | Stockage temporaire des réponses (chiffrées après analyse) |
| Clés de scoring | `data/profile/scoring/scoring_keys.json` | Configuration des calculs de scores |
| Schema dimensions | `data/profile/schema/dimensions_schema.json` | Référentiel des 9 dimensions |
| Matrice de mapping | `data/profile/schema/alfred_mapping_matrix.json` | Règles dimensions → paramètres ALFRED |
| Périodicité | `data/profile/schema/periodicity_schema.json` | Fréquences et déclencheurs de re-passation |
| Analyzer Python | `src/core/profile_analyzer.py` | Moteur de calcul et génération des paramètres |
| Profil utilisateur | `data/profile/user_profile.json` | Profil consolidé (scores + params ALFRED) |

---

## 2. Justification du choix des frameworks psychologiques

### 2.1 Big Five / TIPI — Gosling et al. (2003)

**Pourquoi le Big Five ?**
Le modèle Big Five (OCEAN) est le consensus scientifique le plus robuste en psychologie de la personnalité. Sa validité transculturelle est démontrée dans plus de 50 pays (McCrae & Costa, 1997). C'est le seul modèle de personnalité avec une base génétique et neurobiologique partiellement identifiée.

**Pourquoi le TIPI et pas un test plus long (NEO-PI-R, BFI-44) ?**
- Le TIPI est dans le domaine public ; les mesures plus longues sont propriétaires ou coûteuses en temps
- La corrélation TIPI-NEO-PI-R est de 0.65-0.77 selon les facettes (Gosling et al., 2003) — suffisante pour un usage personnel
- 5 minutes de passation vs 35-45 minutes pour le NEO-PI-R
- **Source principale : AssessFirst SWIPE** — le TIPI sert de vérification légère, pas de mesure de référence

### 2.2 Intelligence émotionnelle — TEIQue-SF (Petrides, 2009)

**Pourquoi l'IE comme trait (pas comme aptitude) ?**
Le modèle d'IE comme trait de personnalité (Petrides) est mesurable par auto-évaluation et prédit mieux les comportements quotidiens que le modèle d'aptitude (Mayer-Salovey-Caruso, mesuré sur tâches objectives). Pour un assistant personnel, la perception subjective de ses capacités émotionnelles est plus pertinente que les performances sur tests.

**Pourquoi le TEIQue-SF ?**
Validé dans 15+ langues, structure factorielle confirmée, items dans la littérature publique. Alternative principale rejetée : EQ-i (Bar-On) — propriétaire.

### 2.3 Valeurs — PVQ-21 (Schwartz, 2001)

**Pourquoi la théorie de Schwartz ?**
La théorie des valeurs de base de Schwartz est la plus validée transculturellement (67 pays). Les 10 valeurs sont motivationnellement distinctes avec une structure circulaire bien établie. Ses données normatives sont disponibles dans la littérature.

**Pourquoi le PVQ-21 plutôt que le SVS (Schwartz Value Survey) ?**
Le SVS demande d'évaluer des valeurs abstraites, ce qui crée un biais de désirabilité sociale. Le PVQ-21 utilise des portraits de personnes — méthode indirecte plus valide pour les études transculturelles et l'usage individuel.

### 2.4 Chronotype — rMEQ (Adan & Almirall, 1991)

**Pourquoi mesurer le chronotype ?**
Le chronotype influence directement les performances cognitives : la mémoire de travail, la résolution de problèmes et la prise de décision sont meilleures au pic circadien de chaque individu. ALFRED peut optimiser le moment des demandes de réflexion complexe selon ce profil.

**Pourquoi le rMEQ et pas le MEQ complet (19 items) ?**
Le rMEQ à 5 items corrèle à r=0.93 avec le MEQ original (Adan & Almirall, 1991). La réduction est justifiée pour un outil de profil personnel.

### 2.5 Résilience et stress — CD-RISC-10 + PSS-4

**Pourquoi deux échelles séparées ?**
La résilience et le stress perçu mesurent des construits distincts : la résilience est une disposition relativement stable (trait), le stress perçu est un état fluctuant (state). Un individu peut avoir une résilience élevée mais traverser une période de stress intense — les deux mesures sont nécessaires pour adapter le comportement ALFRED.

**Pourquoi ces deux outils en particulier ?**
CD-RISC-10 : validité et fidélité excellentes, version courte du CD-RISC complet, dans le domaine public depuis la publication de Campbell-Sills & Stein (2007). PSS-4 : la PSS est l'étalon-or de la mesure du stress perçu, traduite et validée en français (Lesage et al., 2012).

### 2.6 RIASEC — Holland (1997)

**Pourquoi RIASEC ?**
La théorie hexagonale de Holland est le modèle d'orientation professionnelle le plus utilisé au monde, intégré dans des milliers d'outils RH et d'orientation. Elle permet de prédire la satisfaction et les performances professionnelles via l'adéquation personne-environnement.

**Pourquoi des items originaux ?**
Le Self-Directed Search (SDS) officiel est propriétaire. Les 18 items ALFRED sont originaux, fidèles aux descripteurs officiels de chaque type Holland mais non soumis à copyright.

### 2.7 Engagement et burnout — UWES-9 + items originaux

**Pourquoi l'engagement et le burnout ensemble ?**
Ce sont les deux pôles d'un même continuum de santé au travail. La mesure conjointe permet de détecter des configurations complexes (vigueur élevée + cynisme croissant = burnout en développement). La fréquence mensuelle est cliniquement pertinente comme indicateur précoce.

**Pourquoi le UWES-9 et pas le MBI ?**
L'UWES-9 est dans le domaine public (Schaufeli & Bakker, 2004). Le MBI officiel (Maslach) est propriétaire. Les 5 items originaux d'indicateur de risque burnout sont fidèles aux construits de Maslach sans reproduire ses items.

### 2.8 Communication et conflits — TKI-inspiré

**Pourquoi le modèle Thomas-Kilmann ?**
Le modèle TKI est le plus utilisé en développement organisationnel pour la gestion des conflits. Les axes assertivité/coopération sont intuitifs et prédictifs des comportements interpersonnels. La structure ipsative (force ranking) réduit les biais de désirabilité sociale.

**Pourquoi des items originaux ?**
Le TKI officiel est propriétaire (Wiley). Les 25 items ALFRED (10 ipsatifs + 15 Likert) sont originaux et fidèles au modèle.

---

## 3. Décisions de conception et alternatives rejetées

### 3.1 Données partielles : acceptées et gérées

**Décision** : Le système fonctionne avec des données partielles. Un utilisateur peut ne remplir qu'un ou deux questionnaires et obtenir des paramètres ALFRED valides pour les dimensions renseignées.

**Justification** : L'obligation de remplir 8 questionnaires d'un coup serait un frein majeur à l'adoption. Les dimensions les plus critiques pour la santé (stress, burnout) sont prioritaires.

**Alternative rejetée** : Bloquer ALFRED si le profil est incomplet — trop rigide, inutile pour un assistant personnel.

### 3.2 Scores agrégés en niveaux, pas en valeurs brutes

**Décision** : user_profile.json stocke les **niveaux** (faible/moyen/élevé) et les scores normalisés 0-100, jamais les réponses individuelles.

**Justification** : Les réponses brutes (q1=6, q2=3...) sont des données hautement sensibles — elles permettent de reconstituer l'état psychologique exact. Les scores agrégés sont moins sensibles et suffisants pour alimenter les paramètres ALFRED.

**Alternative rejetée** : Stocker les réponses en clair dans user_profile.json — risque de fuite si le fichier est accidentellement partagé.

### 3.3 Matrice de règles JSON, pas de modèle ML

**Décision** : La matrice de mapping est un ensemble de règles déterministes encodées en JSON.

**Justification** :
- Transparence totale : l'utilisateur peut lire et comprendre pourquoi ALFRED adopte tel comportement
- Modifiable sans code : Céline peut ajuster les règles directement dans le JSON
- Pas de dépendances ML supplémentaires (numpy, sklearn) non prévues dans le projet
- Volume de données (1 utilisateur) insuffisant pour un apprentissage machine

**Alternative rejetée** : Modèle de scoring probabiliste (régression logistique, réseau de neurones) — complexité injustifiée pour un usage mono-utilisateur.

### 3.4 Chiffrement Fernet (symétrique), pas asymétrique

**Décision** : Chiffrement Fernet (AES-128-CBC + HMAC-SHA256) pour les réponses brutes.

**Justification** :
- Cohérence avec `encryption_service.py` déjà en place (Bloc 20.05)
- Usage solo : pas de besoin de chiffrement asymétrique (clé publique/privée)
- Fernet est plus simple à implémenter et à maintenir qu'OpenPGP
- `cryptography` est déjà dans requirements.txt

**Alternative rejetée** : Chiffrement asymétrique (RSA/ECC) — sur-engineering pour un usage local mono-utilisateur.

### 3.5 Pas d'interface graphique pour la passation

**Décision** : Les questionnaires sont en Markdown, les réponses saisies en JSON manuellement.

**Justification** :
- Cohérent avec la phase actuelle du projet (V1 local-first)
- Pas de dépendances GUI non prévues
- L'utilisateur lit le questionnaire une fois, saisit ses réponses une fois par an (ou par mois)

**Alternative rejetée** : Interface web ou TUI — prévu pour V2/V3.

---

## 4. Processus de collecte des réponses

### 4.1 Flux standard

```
Étape 1 : Céline ouvre le fichier questionnaire (.md) dans son éditeur
              ↓
Étape 2 : Elle lit les instructions et répond mentalement à chaque item
              ↓
Étape 3 : Elle ouvre answers_template.json
              ↓
Étape 4 : Elle saisit ses réponses (ex: "q1": 6, "q2": 3)
              ↓
Étape 5 : Elle met "completed": true et "date": "2026-06-16"
              ↓
Étape 6 : Elle lance : python src/core/profile_analyzer.py
              ↓
Étape 7 : Le module calcule les scores, met à jour user_profile.json
              ↓
Étape 8 : Le module chiffre answers_template.json (→ answers_encrypted/)
              ↓
Étape 9 : ALFRED lit user_profile.json et adapte son comportement
```

### 4.2 Conditions de passation optimales

- Lieu calme, sans interruption
- Durée totale disponible : au moins 20 minutes pour les questionnaires mensuels
- Éviter : immédiatement après un événement émotionnel fort, sous l'effet d'alcool ou de médicaments psychoactifs, en situation de fatigue extrême (sauf pour le questionnaire résilience/stress qui mesure justement cet état)
- Pour les questionnaires mensuels (stress, burnout) : refléter les 4 DERNIÈRES SEMAINES, pas uniquement l'humeur du jour

### 4.3 Gestion des données partielles

Si certaines questions ne sont pas répondues dans un questionnaire :
- Le module calcule les scores avec les items disponibles
- Si moins de 70% des items d'une sous-dimension sont remplis, la sous-dimension est marquée `completed: false`
- Les paramètres ALFRED pour cette dimension tombent sur les valeurs par défaut
- Le score global n'est pas calculé si moins de 2 sous-dimensions sont complètes

---

## 5. Pipeline de calcul des scores

### 5.1 Étapes détaillées

```
ENTRÉE : answers_template.json (réponses brutes)
    │
    ├─── Étape 1 : Validation
    │    - Vérification que toutes les réponses sont dans les plages valides
    │    - Détection des questionnaires complétés (completed: true)
    │
    ├─── Étape 2 : Inversion des items inversés
    │    - score_inversé = (scale_max + 1) - score_brut
    │    - Ex : TIPI q6 (Extraversion, item inversé) : 8 - score
    │    - Ex : PSS-4 s3, s4 : 4 - score
    │
    ├─── Étape 3 : Calcul par sous-dimension
    │    - Méthode 'mean' : moyenne des items
    │    - Méthode 'sum' : somme des items
    │    - Cas spécial Schwartz : correction centrage (Grand Mean Centering)
    │    - Cas spécial Communication : score composite ipsatif (40%) + Likert (60%)
    │
    ├─── Étape 4 : Normalisation 0-100
    │    - Linear : (score - min) / (max - min) * 100
    │    - Inverted : 100 - linear (pour stress, épuisement, cynisme)
    │    - Centered (Schwartz) : (score - grand_mean + 2.5) / 5 * 100
    │
    ├─── Étape 5 : Attribution du niveau
    │    - Règles par dimension (voir _get_level_from_score())
    │    - Cas spéciaux : chronotype (3 catégories), engagement (5 niveaux)
    │
    ├─── Étape 6 : Agrégats de niveau supérieur
    │    - Valeurs supérieures Schwartz (4 catégories)
    │    - Scores globaux par dimension (moyenne des sous-dimensions)
    │
    └─── SORTIE : Dict[str, DimensionScore] avec sous-scores normalisés
```

### 5.2 Formules de normalisation par questionnaire

| Questionnaire | Formule | Note |
|---------------|---------|------|
| TIPI | `(mean - 1) / 6 * 100` | Échelle 1-7 |
| TEIQue | `(mean - 1) / 6 * 100` | Échelle 1-7 |
| PVQ-21 | `(mean - grand_mean + 2.5) / 5 * 100` | Centré |
| rMEQ chrono | `100 - ((sum - 5) / 20 * 100)` | Inversé : élevé = soir |
| Énergie | `(mean - 1) / 4 * 100` | Échelle 1-5 |
| CD-RISC-10 | `sum / 40 * 100` | Échelle 0-4 |
| PSS-4 | `100 - (sum / 16 * 100)` | Inversé : élevé = calme |
| RIASEC | `(sum - 3) / 12 * 100` | Somme 3 items (3-15) |
| UWES-9 | `mean / 6 * 100` | Échelle 0-6 |
| Burnout | `100 - (mean / 4 * 100)` | Inversé : élevé = pas burnout |
| Communication | Score composite pondéré | 40% ipsatif + 60% Likert |

---

## 6. Logique de la matrice de mapping

### 6.1 Principe

La matrice `alfred_mapping_matrix.json` contient des règles qui mappent chaque niveau d'une dimension/sous-dimension sur un ensemble de paramètres comportementaux ALFRED.

### 6.2 Priorité des règles

```
Niveau de priorité (du plus fort au plus faible) :

1. RÈGLES DE COMBINAISON (combination_rules)
   → Écrasent toutes les règles individuelles
   → Exemple : stress élevé + résilience faible = mode soutien intensif
   → Déclenchent aussi des alertes

2. RÈGLES INDIVIDUELLES (rules)
   → Appliquées dans l'ordre du JSON
   → Chaque règle peut écraser les précédentes
   → La DERNIÈRE règle applicable pour un paramètre prévaut

3. PARAMÈTRES PAR DÉFAUT (default_params)
   → Appliqués si aucune dimension n'est renseignée
   → Comportement ALFRED "neutre" équilibré
```

### 6.3 Exemple concret de résolution

**Situation** : Céline a un stress perçu élevé (score PSS-4 = 5/100) + vigueur UWES moyenne (score = 55/100)

```
Étape 1 : Paramètres par défaut
  tone = chaleureux, proactivity = modéré, emotional_support = standard

Étape 2 : Application des règles individuelles

  Règle rule_resilience_stress_eleve :
    dimension: resilience_stress, sub: stress_percu, level: faible
    score 5/100 → niveau 'faible' ✓ match
    → tone = soutenant, proactivity = faible, emotional_support = intensif

  Règle rule_engagement_moyen :
    dimension: engagement_burnout, sub: vigueur, level: moyen
    score 55/100 → niveau 'moyen' ✓ match
    → tone = chaleureux (écrase soutenant), emotional_support = standard

  [Résultat intermédiaire : chaleureux, support = standard]

Étape 3 : Vérification des règles de combinaison
  combo_burnout_et_stress : vigueur critique (5/100 ≠ critique) → non applicable
  combo_stress_eleve_resilience_faible : stress faible + résilience ? → selon scores CD-RISC

  Si résilience aussi faible :
    → tone = soutenant, emotional_support = intensif, check_in = quotidienne

Résultat final si combo applicable : mode soutien renforcé
```

### 6.4 Paramètres ALFRED et leur impact comportemental

| Paramètre | Valeurs | Impact sur le comportement |
|-----------|---------|--------------------------|
| `tone` | directif / chaleureux / analytique / soutenant / énergisant | Style de communication global |
| `response_length` | court / moyen / long / adaptatif | Verbosité des réponses |
| `proactivity` | faible / modéré / élevé | Fréquence des suggestions proactives |
| `emotional_support_level` | minimal / standard / élevé / intensif | Prise en compte des émotions dans les réponses |
| `challenge_level` | minimal / standard / élevé | Niveau d'exigence des suggestions |
| `check_in_frequency` | à_la_demande / hebdomadaire / quotidienne | Fréquence des check-ins proactifs |
| `explanation_depth` | synthèse / détaillé / expert | Niveau de détail des explications |
| `humor_level` | désactivé / léger / modéré | Utilisation de l'humour |
| `structure_preference` | libre / structuré / très_structuré | Format des réponses |

---

## 7. Système de périodicité

### 7.1 Fréquences et justifications scientifiques

| Dimension | Fréquence | Stabilité temporelle | Source |
|-----------|-----------|---------------------|--------|
| Stress / Résilience | Mensuelle | Très variable | Cohen et al. (1983), PSS conçu pour monitoring continu |
| Engagement / Burnout | Mensuelle | Variable sur 4-6 semaines | Schaufeli & Bakker (2004) |
| Chronotype / Énergie | Trimestrielle | Varie avec les saisons | Roenneberg et al. (2004) |
| IE | Semestrielle | Modérément stable | Petrides (2009) |
| Communication | Semestrielle | Stable mais apprennable | Thomas & Kilmann (1974) |
| Big Five | Annuelle | Très stable (r > 0.70 sur 4 semaines) | McCrae & Costa (2003) |
| Valeurs | Annuelle | Très stable | Schwartz et al. (2012) |
| RIASEC | Annuelle | Stable (~0.80 sur 4 semaines) | Holland (1997) |
| AssessFirst | Sur changement de vie | Stable (Big Five, 0.60 sur 10 ans) | McCrae & Costa (2003) |

### 7.2 Calcul des dates de re-passation

```python
# Logique de calcul (implémentée dans la prochaine version du ProfileAnalyzer)

def compute_next_due(dimension_id: str, last_passed: date) -> date:
    periodicity = load_periodicity_schema()
    dim_config = periodicity["dimensions"][dimension_id]
    
    if dim_config["frequence_jours"] is None:
        return None  # Aucune date fixe (ex: AssessFirst)
    
    return last_passed + timedelta(days=dim_config["frequence_jours"])
```

### 7.3 Système de priorités en cas de plusieurs questionnaires dus simultanément

Règle principale : **ne pas proposer plus de 2 questionnaires par session**.

Ordre de priorité :
1. Questionnaires mensuels en retard (stress, burnout) — santé prioritaire
2. Questionnaires déclenchés par un événement de vie identifié
3. Questionnaires trimestriels en retard (chronotype)
4. Questionnaires semestriels en retard (IE, communication)
5. Questionnaires annuels en retard (Big Five, valeurs, RIASEC)

### 7.4 Déclencheurs anticipés (trigger_conditions)

En plus des fréquences régulières, le système prévoit des re-passations anticipées déclenchées par des événements de vie. Ces déclencheurs sont définis dans `periodicity_schema.json` pour chaque dimension.

Exemples :
- Stress/Résilience : événement stressant majeur, plainte répétée de fatigue
- Chronotype : changement de saison, voyage long-courrier
- Big Five : changement de vie radical, événement traumatique
- AssessFirst : reconversion majeure, délai minimum 3 ans entre passations

---

## 8. Intégration avec le moteur ALFRED existant

### 8.1 Point d'intégration principal

Le moteur comportemental `src/core/alfred_behavior_engine.py` (Bloc 03.02) reçoit un objet `UserState` et produit un `BehaviorDecision`. Les paramètres psychologiques viennent enrichir cette décision.

**Flux d'intégration prévu (V1) :**

```python
# Dans alfred_behavior_engine.py ou son orchestrateur

profile = load_user_profile("data/profile/user_profile.json")
alfred_params = profile.get("alfred_derived_params", {})

# Les paramètres psychologiques enrichissent les décisions
if alfred_params.get("emotional_support_level") == "intensif":
    # Forcer le support_mode même pour les requêtes d'exécution
    pass

if alfred_params.get("tone") == "analytique":
    # Surcharger le ton par défaut du mode
    pass
```

### 8.2 Paramètres communs avec alfred_behavior_engine.py

| Paramètre psychologique | Équivalent dans BehaviorDecision |
|------------------------|----------------------------------|
| `tone` | `BehaviorDecision.tone` |
| `response_length` | Paramètre du `response_generator` |
| `emotional_support_level` | Influence `dominant_layer` et mode |
| `proactivity` | Influence les `softskills` déclenchés |
| `structure_preference` | Influence `response_structure` |

### 8.3 Priorités de fusion

Quand le moteur comportemental et le profil psychologique suggèrent des comportements contradictoires :

1. **Situation d'urgence détectée par le moteur** (ethics_mode, stress aigu) : le moteur prend la priorité
2. **État émotionnel immédiat** (UserState.emotion, intensity) : prend la priorité sur le profil psychologique statique
3. **Profil psychologique** : s'applique quand aucun signal émotionnel fort n'est détecté

---

## 9. Évolutions prévues

### V2 — Interface de passation

- Interface TUI (Terminal User Interface) pour remplir les questionnaires interactivement
- Validation des réponses en temps réel (plage valide)
- Calcul et affichage des scores immédiatement après la passation
- Suggestion automatique du prochain questionnaire à remplir selon la périodicité

### V2 — Notifications de re-passation

- Module de suivi des dates de re-passation
- Notification ALFRED : "Ton questionnaire de stress est dû depuis 3 jours"
- Intégration avec le système de mémoire episodique

### V3 — Apprentissage adaptatif

- Détection des incohérences entre le profil déclaré et les comportements observés dans les interactions
- Ajustement progressif des paramètres ALFRED sans re-passation
- Modèle bayésien de mise à jour du profil

### V3 — Profil longitudinal

- Graphiques d'évolution des scores dans le temps
- Détection automatique des tendances (stress croissant, engagement déclinant)
- Alertes proactives basées sur les trajectoires

### V4 — Multi-profils

- Gestion de plusieurs profils (ex : Céline en mode professionnel vs mode perso)
- Profils contextuels (travail, famille, projets personnels)

---

## 10. Limites et avertissements éthiques

### 10.1 Limites scientifiques

**Fiabilité des mesures courtes**
Le TIPI à 10 items a une fiabilité test-retest de 0.72 en moyenne — inférieure aux versions longues (NEO-PI-R : 0.87). Les scores individuels doivent être interprétés comme des tendances, pas des vérités absolues.

**Biais d'auto-évaluation**
Tous ces questionnaires reposent sur l'auto-perception, qui peut différer des évaluations par observateurs. Les biais connus : désirabilité sociale, leniency bias, halo effect. Le PVQ-21 est partiellement conçu pour réduire ce biais (portraits indirects).

**Variance situationnelle**
La personnalité (Big Five) est stable, mais les états (stress, engagement) fluctuent. Un score de stress mesuré un mauvais jour est moins fiable que la moyenne sur 4 semaines.

**Absence de données normatives localisées**
Les données normatives utilisées sont principalement issues d'études anglo-saxonnes. Des différences culturelles sont possibles, notamment pour les valeurs Schwartz et le RIASEC.

### 10.2 Avertissements éthiques

**Usage strictement personnel**
Ce système est conçu pour un usage personnel par Céline Rousselot uniquement. Il ne doit pas être utilisé pour évaluer des tiers sans leur consentement explicite.

**Non-diagnostique**
Ces questionnaires ne constituent pas un diagnostic médical ou psychiatrique. Ils ne remplacent pas l'évaluation d'un psychologue clinicien. En cas de détresse psychologique significative, consultez un professionnel.

**Limites de la prescription automatique**
Les paramètres ALFRED sont des suggestions basées sur des corrélations statistiques, pas des prescriptions individualisées. ALFRED peut se tromper — l'utilisateur reste le seul décisionnaire.

**Droit à l'effacement**
Céline peut supprimer l'intégralité des données psychologiques à tout moment (voir `docs/profil_systeme/securite_donnees.md`). Le système est conçu pour fonctionner sans profil psychologique (paramètres par défaut).

**Non-manipulation**
Les paramètres psychologiques ne sont jamais utilisés pour manipuler l'utilisateur ou créer une dépendance artificielle envers ALFRED. L'objectif unique est l'adaptation communicationnelle.
