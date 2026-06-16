# Architecture technique — Module Profil IA Adaptative
## Cognitive Products Lab — ALFRED

> Version 1.0 — 2026-06-16  
> Dernière mise à jour : 2026-06-16

---

## 1. Vue d'ensemble

Le module de profil IA adaptative est composé de 4 couches distinctes :

```
┌─────────────────────────────────────────────────────────────────────┐
│                     COUCHE PRÉSENTATION                             │
│          (Interface conversationnelle ALFRED — Kivy GUI)            │
│  ALFRED pose les questions une par une, comme dans un dialogue      │
└───────────────────────────┬─────────────────────────────────────────┘
                            │ questions / réponses
┌───────────────────────────▼─────────────────────────────────────────┐
│                     COUCHE LOGIQUE MÉTIER                           │
│                                                                     │
│  ┌─────────────────────────┐   ┌─────────────────────────────────┐  │
│  │   QuestionnaireSession  │   │      PersonalityAdapter         │  │
│  │  (src/profile/          │   │    (src/core/                   │  │
│  │   profile_analyzer.py)  │   │     personality_adapter.py)     │  │
│  │                         │   │                                 │  │
│  │ • next_question()       │   │ • load personality_core         │  │
│  │ • save_answer()         │   │ • load user_profile             │  │
│  │ • get_progress()        │   │ • adapt_tone()                  │  │
│  │ • compute_scores()      │   │ • prepare_context()             │  │
│  └────────────┬────────────┘   └───────────────┬─────────────────┘  │
│               │                                │                     │
└───────────────┼────────────────────────────────┼─────────────────────┘
                │ lecture/écriture                │ lecture
┌───────────────▼────────────────────────────────▼─────────────────────┐
│                      COUCHE DONNÉES                                   │
│                                                                       │
│  data/profile/                     config/                            │
│  ├── answers_template.json         ├── personality_core.json          │
│  │   (réponses chiffrées)          │   (personnalité stable ALFRED)   │
│  ├── user_profile.json             └── user_adaptation_profile.json   │
│  │   (profil utilisateur)                                             │
│  └── schema/                                                          │
│      ├── dimensions_schema.json    data/profile/scoring/              │
│      ├── alfred_mapping_matrix.json ├── scoring_keys.json             │
│      └── periodicity_schema.json   └── answers_template.json          │
└───────────────────────────────────────────────────────────────────────┘
                                │
                                │ chiffrement/déchiffrement
┌───────────────────────────────▼───────────────────────────────────────┐
│                      COUCHE SÉCURITÉ                                  │
│                                                                       │
│  • Fernet (AES-128-CBC) — cryptography library                        │
│  • Clé séparée des données (data/security/fernet.key — gitignored)    │
│  • Données sensibles uniquement en mémoire pendant le calcul          │
│  • Réponses brutes → chiffrées immédiatement après scoring            │
└───────────────────────────────────────────────────────────────────────┘
```

---

## 2. Composants principaux

### 2.1 QuestionnaireSession (`src/profile/profile_analyzer.py`)

**Rôle** : Gestion de la passation conversationnelle des questionnaires.

**Responsabilités** :
- Maintenir l'état de progression de chaque questionnaire
- Retourner la prochaine question non répondue
- Valider et sauvegarder chaque réponse immédiatement
- Calculer les scores par sous-échelle
- Permettre la reprise d'une session interrompue

**Interface** :
```python
class QuestionnaireSession:
    def __init__(self, answers_path: str = None)
    def next_question(self, questionnaire_id: str) -> Optional[Dict]
    def save_answer(self, questionnaire_id: str, question_id: str, answer: Any) -> None
    def get_progress(self) -> Dict[str, Dict[str, Any]]
    def can_compute_partial_scores(self, questionnaire_id: str) -> bool
    def compute_scores(self, questionnaire_id: str, partial: bool = False) -> Optional[Dict]
```

**Persistance** : Toutes les réponses sont sauvegardées dans `answers_template.json` après chaque réponse (écriture atomique).

### 2.2 PersonalityAdapter (`src/core/personality_adapter.py`)

**Rôle** : Adapter le comportement d'ALFRED selon la personnalité et le profil utilisateur.

**Responsabilités** :
- Charger la personnalité stable d'ALFRED (`personality_core.json`)
- Charger le profil utilisateur (`user_profile.json`)
- Valider que les fichiers ne sont pas des templates publics
- Adapter le ton, le niveau émotionnel, le style de réponse
- Préparer le contexte pour `response_generator.py`

**Protection contre les templates** :
```python
# Empêche l'usage direct d'un template public
adapter = PersonalityAdapter(
    personality_path="config/personality_core.json",
    user_profile_path="data/profile/user_profile.json",
    allow_templates=False  # default
)
```

### 2.3 ProfileAnalyzer (`src/core/profile_analyzer.py`)

**Rôle** : Pipeline complet de traitement (variante avec CLI).

**Responsabilités** :
- Charger et calculer tous les scores
- Appliquer la matrice de mapping
- Mettre à jour `user_profile.json` avec les paramètres ALFRED dérivés
- Chiffrer les réponses brutes après traitement
- Exposer une interface CLI pour l'usage manuel

**CLI** :
```bash
python src/core/profile_analyzer.py --report-only    # affiche les scores sans mise à jour
python src/core/profile_analyzer.py --no-encrypt     # traitement sans chiffrement (dev)
python src/core/profile_analyzer.py --decrypt        # déchiffre les réponses
```

---

## 3. Flux de données — Passation d'un questionnaire

```
Utilisateur                ALFRED (GUI)           QuestionnaireSession        answers_template.json
    │                          │                         │                           │
    │  "Je veux faire          │                         │                           │
    │   le test de             │                         │                           │
    │   bien-être"             │                         │                           │
    │──────────────────────────▶                         │                           │
    │                          │ session.next_question(  │                           │
    │                          │   "q01_bien_etre_       │                           │
    │                          │    subjectif")          │                           │
    │                          │─────────────────────────▶                           │
    │                          │                         │  load(answers_path)       │
    │                          │                         │──────────────────────────▶│
    │                          │                         │◀──────────────────────────│
    │                          │                         │  trouve première question  │
    │                          │                         │  sans réponse              │
    │                          │◀────────────────────────│                           │
    │  {question_id: "swls_01",│                         │                           │
    │   text: "Dans l'ensemble,│                         │                           │
    │   est-ce que...",        │                         │                           │
    │   type: "likert_7",      │                         │                           │
    │   index: 0, progress: 0%}│                         │                           │
    │◀──────────────────────────                         │                           │
    │                          │                         │                           │
    │  Réponse : 5             │                         │                           │
    │──────────────────────────▶                         │                           │
    │                          │ session.save_answer(    │                           │
    │                          │   "q01...", "swls_01", 5)                           │
    │                          │─────────────────────────▶                           │
    │                          │                         │  validate(5, "likert_7")  │
    │                          │                         │  update answers["swls_01"]│
    │                          │                         │  update session_state     │
    │                          │                         │──────────────────────────▶│
    │                          │                         │  _save() [atomique]       │
    │                          │◀────────────────────────│                           │
    │  [boucle jusqu'à         │                         │                           │
    │   completion]            │                         │                           │
```

---

## 4. Flux de données — Calcul du profil ALFRED

```
answers_template.json   scoring_keys.json    dimensions_schema.json   alfred_mapping_matrix.json
        │                      │                      │                         │
        │                      │                      │                         │
        ▼                      ▼                      ▼                         │
┌───────────────────────────────────────────────────────┐                       │
│                ProfileAnalyzer.load_all()             │                       │
└───────────────────────────────┬───────────────────────┘                       │
                                │                                               │
                                ▼                                               │
┌───────────────────────────────────────────────────────┐                       │
│              ProfileAnalyzer.compute_scores()         │                       │
│                                                       │                       │
│  Q01: SWLS = Σ(swls_01..05)    [5-35]                 │                       │
│       PANAS+ = Σ(pan_p_01..05) [5-35]                 │                       │
│       PANAS- = Σ(pan_n_01..04) [4-28]                 │                       │
│                                                       │                       │
│  Q02: score_analytique = mean(cog_a_01..04) [1-7]     │                       │
│       score_intuitif = mean(cog_i_01..04)   [1-7]     │                       │
│       profil_ai = "analytique"/"intuitif"/"mixte"     │                       │
│                                                       │                       │
│  Q03: réévaluation = mean(re_01..05) [1-5]            │                       │
│       suppression = mean(sup_01..03) [1-5]            │                       │
│       PSS = Σ(str, avec inversion str_04) [0-20]      │                       │
│                                                       │                       │
│  Q04: autonomie = mean(sdt_aut_01..06) [1-5]          │                       │
│       compétence = mean(sdt_comp_01..06) [1-5]        │                       │
│       appartenance = mean(sdt_app_01..06) [1-5]       │                       │
│       dominante = argmax si diff >= 0.5               │                       │
└───────────────────────────────┬───────────────────────┘                       │
                                │ scores bruts                                  │
                                ▼                                               │
┌───────────────────────────────────────────────────────────────────────────────▼──┐
│                    ProfileAnalyzer.generate_alfred_params(scores)                 │
│                                                                                   │
│  Applique les 40+ règles de la matrice de mapping :                               │
│  swls_total >= 25  →  emotional_support_level = "équilibré"                       │
│  PSS >= 14         →  ALERTE BURNOUT → check_in_frequency = "quotidien"           │
│  profil_ai == "analytique" →  explanation_depth = "approfondi"                   │
│  motivation_dominante == "autonomie" →  proactivity = "minimal"                   │
│  ...                                                                              │
│                                                                                   │
│  Combine les règles conflictuelles via priorité :                                 │
│  CRITIQUE > ALERTE > STANDARD                                                     │
└───────────────────────────────┬───────────────────────────────────────────────────┘
                                │ alfred_params
                                ▼
                    user_profile.json (mis à jour)
```

---

## 5. Sécurité des données

### Séparation clé / données
```
data/
├── profile/
│   ├── answers/
│   │   └── user_answers_YYYY-MM-DD.json    ← réponses en clair (temporaire)
│   ├── answers_encrypted/
│   │   └── user_answers_YYYY-MM-DD.enc     ← réponses chiffrées (persistant)
│   └── keys/
│       └── [gitignored]                    ← clé Fernet (jamais commitée)
└── security/
    └── fernet.key                          ← [gitignored]
```

### Règle de vie des données sensibles
```
Passation questionnaire  →  réponses en mémoire  →  scoring  →  chiffrement  →  suppression clair
                                                                  (Fernet)
                                                                  ↓
                                                    answers_encrypted/*.enc
```

### Ce qui est JAMAIS commité
Voir `.gitignore` :
- `data/profile/answers/` — réponses brutes
- `data/profile/answers_encrypted/` — réponses chiffrées
- `data/profile/keys/` — clés de déchiffrement
- `*.fernet_key` — clés Fernet
- `user_answers_*.json` — exports temporaires
- `data/security/fernet.key` — clé principale

---

## 6. Dépendances techniques

```python
# Chiffrement
cryptography>=41.0.0     # Fernet (AES-128-CBC)

# Calculs (si intégration avancée)
# Pas de numpy/pandas dans V1 — calculs Python pur pour légèreté

# Tests
pytest>=8.0.0
pytest-cov>=5.0.0

# Runtime
python>=3.13
pathlib (stdlib)
json (stdlib)
math (stdlib)
datetime (stdlib)
```

---

## 7. Conventions de code

### Nommage des fichiers de données
- Questionnaires : `{NN}_{nom_dimension}.md` pour les scientifiques, `q{NN}_{nom}.md` pour les conversationnels ALFRED
- Clés de scoring : `scoring_keys.json` (unique, versionné en JSON)
- Réponses utilisateur : `user_answers_{YYYY-MM-DD}.json` (gitignored)

### Nommage des IDs d'items
- Pattern : `{prefixe_echelle}_{NN}` ex : `swls_01`, `pan_p_03`, `cog_a_02`, `sdt_aut_04`
- Items inversés : documentés dans `scoring_keys.json` (liste `reversed_items`)

### Versioning des schémas
- Chaque fichier JSON inclut un champ `"_meta"` avec `version`, `created_at`, `updated_at`
- Changement de structure → bump de version dans `_meta`

---

## 8. Décisions d'architecture

| # | Décision | Justification |
|---|----------|---------------|
| D1 | **Local-first absolu** : toutes les données restent sur l'appareil | RGPD art.9 + Privacy by Design + confiance utilisateur |
| D2 | **Passation conversationnelle** : 1 question à la fois dans ALFRED | UX : évite l'effet formulaire, maintient l'engagement |
| D3 | **Sauvegarde immédiate** après chaque réponse | Résilience : reprise sans perte si l'app se ferme |
| D4 | **Chiffrement Fernet** sur les réponses brutes | AES-128-CBC éprouvé, compatible avec encryption_service.py existant |
| D5 | **Schémas JSON** pour les dimensions et mappings | Évolutivité : modifier le profil sans toucher au code Python |
| D6 | **Séparation stricte** clé Fernet / données | Principe Kerckhoffs : compromis données ≠ compromis clé |
| D7 | **Scores normalisés 0-100** après calcul | Interopérabilité et lecture humaine uniforme |
| D8 | **Profil qualitatif Q00** en texte libre | Complète les scores quantitatifs avec les nuances contextuelles |
| D9 | **Périodicité différenciée** par dimension | Traits stables (annuel) vs état (mensuel) — évite la surcharge |

---

*Document créé le 2026-06-16 — Cognitive Products Lab*
