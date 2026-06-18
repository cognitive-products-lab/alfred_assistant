# API Reference — Module Profil IA Adaptative
## Cognitive Products Lab — ALFRED

> Version 1.0 — 2026-06-16

---

## `QuestionnaireSession` (`src/profile/profile_analyzer.py`)

Classe principale de gestion de la passation conversationnelle des questionnaires.

### Constructeur

```python
QuestionnaireSession(answers_path: str = None)
```

| Paramètre | Type | Défaut | Description |
|-----------|------|--------|-------------|
| `answers_path` | `str \| None` | `data/profile/answers_template.json` | Chemin vers le fichier de réponses. Si `None`, utilise le chemin par défaut du projet. |

**Exemple** :
```python
from src.profile.profile_analyzer import QuestionnaireSession

# Usage standard
session = QuestionnaireSession()

# Usage avec chemin personnalisé (tests, développement)
session = QuestionnaireSession(answers_path="/tmp/test_answers.json")
```

**Comportement** : Si le fichier n'existe pas, un template vide est créé automatiquement au premier `save_answer()`.

---

### `next_question(questionnaire_id)`

Retourne la prochaine question sans réponse d'un questionnaire.

```python
def next_question(self, questionnaire_id: str) -> Optional[Dict[str, Any]]
```

**Paramètres** :

| Paramètre | Type | Description |
|-----------|------|-------------|
| `questionnaire_id` | `str` | ID du questionnaire (voir tableau des IDs ci-dessous) |

**Retourne** : `dict` ou `None`

```python
# Retourne un dict quand une question est disponible :
{
    "id": "swls_01",                   # str — identifiant unique de l'item
    "text": "Dans l'ensemble, est-ce…", # str — texte de la question pour ALFRED
    "type": "likert_7",                # str — type de réponse attendu
    "index": 0,                        # int — position (0-based) dans le questionnaire
    "total": 14,                       # int — nombre total d'items du questionnaire
    "progress_pct": 0.0,               # float — % de questions répondues [0.0-100.0]
}

# Retourne None si le questionnaire est complet
None
```

**Lève** : `ValueError` si `questionnaire_id` est inconnu.

**Exemple** :
```python
session = QuestionnaireSession()
q = session.next_question("q01_bien_etre_subjectif")
if q:
    alfred_says(q["text"])
    # => "Dans l'ensemble, est-ce que tu as l'impression que ta vie..."
else:
    alfred_says("Tu as déjà complété ce questionnaire.")
```

---

### `save_answer(questionnaire_id, question_id, answer)`

Valide et sauvegarde une réponse. Écriture immédiate sur disque.

```python
def save_answer(
    self,
    questionnaire_id: str,
    question_id: str,
    answer: Any
) -> None
```

**Paramètres** :

| Paramètre | Type | Description |
|-----------|------|-------------|
| `questionnaire_id` | `str` | ID du questionnaire |
| `question_id` | `str` | ID de la question (ex: `"swls_01"`) |
| `answer` | `Any` | Valeur de la réponse |

**Types de réponse et valeurs valides** :

| `type` de l'item | Valeurs valides | Exemple |
|-----------------|----------------|---------|
| `likert_5` | Entier `1` à `5` | `3` |
| `likert_7` | Entier `1` à `7` | `6` |
| `choix_binaire` | String `"A"` ou `"B"` (insensible à la casse) | `"A"` |
| `texte_libre` | N'importe quelle string | `"Je préfère le matin"` |

**Lève** :
- `ValueError` si la valeur est hors-échelle (Likert) ou invalide (choix binaire)
- `ValueError` si `questionnaire_id` ou `question_id` est inconnu

**Exemple** :
```python
session.save_answer("q01_bien_etre_subjectif", "swls_01", 5)
session.save_answer("q02_style_cognitif", "fmt_01", "A")
session.save_answer("q00_profil_complementaire", "prof_01", "Je préfère travailler le matin")

# Erreur — hors échelle
session.save_answer("q01...", "swls_01", 8)
# => ValueError: Réponse hors-échelle pour 'swls_01' (likert_7, attendu 1-7, reçu 8)
```

---

### `get_progress()`

Retourne l'état d'avancement de tous les questionnaires.

```python
def get_progress(self) -> Dict[str, Dict[str, Any]]
```

**Retourne** : `dict` keyed par `questionnaire_id`

```python
{
    "q01_bien_etre_subjectif": {
        "label": "Bien-être subjectif",         # str
        "answered": 7,                           # int — questions répondues
        "total": 14,                             # int — total d'items
        "pct_complete": 50.0,                    # float — % [0.0-100.0]
        "is_complete": False,                    # bool
        "started_at": "2026-06-16T09:00:00Z",   # str ISO 8601 ou None
        "last_saved_at": "2026-06-16T09:05:30Z", # str ISO 8601 ou None
        "estimated_remaining_min": 5,            # int — minutes restantes estimées
    },
    "q02_style_cognitif": { ... },
    "q03_regulation_emotionnelle": { ... },
    "q04_motivations_valeurs": { ... },
    "q00_profil_complementaire": { ... },
}
```

**Exemple** :
```python
progress = session.get_progress()
for qid, state in progress.items():
    print(f"{state['label']}: {state['pct_complete']:.0f}% ({state['answered']}/{state['total']})")
# => Bien-être subjectif: 50% (7/14)
# => Style cognitif: 0% (0/16)
```

---

### `can_compute_partial_scores(questionnaire_id)`

Indique si suffisamment de réponses sont disponibles pour un score partiel.

```python
def can_compute_partial_scores(self, questionnaire_id: str) -> bool
```

**Seuils minimaux** (définis dans `QUESTIONNAIRE_META`) :

| Questionnaire | Items totaux | Seuil partiel |
|--------------|-------------|---------------|
| `q01_bien_etre_subjectif` | 14 | 7 |
| `q02_style_cognitif` | 16 | 8 |
| `q03_regulation_emotionnelle` | 11 | 8 |
| `q04_motivations_valeurs` | 18 | 9 |
| `q00_profil_complementaire` | 23 | 12 |

**Lève** : `ValueError` si `questionnaire_id` est inconnu.

---

### `compute_scores(questionnaire_id, partial=False)`

Calcule les scores d'un questionnaire.

```python
def compute_scores(
    self,
    questionnaire_id: str,
    partial: bool = False
) -> Optional[Dict[str, Any]]
```

**Retourne** : `dict` ou `None`

```python
# Q01 — Bien-être subjectif
{
    "swls_total": 28,           # int — somme SWLS (5-35)
    "panas_positif": 30,        # int — somme PANAS+ (5-35)
    "panas_negatif": 8,         # int — somme PANAS- (4-28)
    "computed_at": "2026-06-16T09:10:00Z",
    "is_partial": False
}

# Q02 — Style cognitif
{
    "score_analytique": 5.75,           # float — moyenne [1-7]
    "score_intuitif": 4.0,              # float — moyenne [1-7]
    "profil_ai": "analytique",          # str — "analytique"|"intuitif"|"mixte"
    "score_verbal": 5.0,                # float
    "score_visuel_spatial": 4.33,       # float
    "profil_vvs": "verbal",             # str — "verbal"|"visuel_spatial"|"mixte"
    "computed_at": "...",
    "is_partial": False
}

# Q03 — Régulation émotionnelle
{
    "reevaluation_cognitive": 4.2,   # float — moyenne re_01..05 [1-5]
    "suppression": 2.0,              # float — moyenne sup_01..03 [1-5]
    "stress_percu_pss": 7,           # int — somme PSS avec inversion str_04 [0-20]
    "computed_at": "...",
    "is_partial": False
}

# Q04 — Motivations SDT
{
    "autonomie": 4.17,               # float — moyenne sdt_aut [1-5]
    "competence": 3.83,              # float
    "appartenance": 3.5,             # float
    "motivation_dominante": "autonomie", # str — "autonomie"|"competence"|"appartenance"|"equilibre"
    "computed_at": "...",
    "is_partial": False
}
```

**Retourne `None`** si :
- `partial=False` et le questionnaire est incomplet
- `partial=True` et le seuil minimal n'est pas atteint
- Questionnaire qualitatif `q00` (pas de scoring numérique)

---

## IDs des questionnaires

| `questionnaire_id` | Label | Items | Durée |
|-------------------|-------|-------|-------|
| `q01_bien_etre_subjectif` | Bien-être subjectif (SWLS + PANAS) | 14 | 7-9 min |
| `q02_style_cognitif` | Style cognitif (Analytique/Intuitif) | 16 | 8-10 min |
| `q03_regulation_emotionnelle` | Régulation émotionnelle (ERQ + PSS) | 11 | 8-10 min |
| `q04_motivations_valeurs` | Motivations SDT | 18 | 9-11 min |
| `q00_profil_complementaire` | Profil complémentaire (qualitatif) | 23 | 10-15 min |

---

## `PersonalityAdapter` (`src/core/personality_adapter.py`)

Adapte le comportement d'ALFRED selon la personnalité core et le profil utilisateur.

### Constructeur

```python
PersonalityAdapter(
    personality_path: str,
    user_profile_path: str,
    allow_templates: bool = False
)
```

| Paramètre | Type | Description |
|-----------|------|-------------|
| `personality_path` | `str` | Chemin vers `personality_core.json` (instance privée) |
| `user_profile_path` | `str` | Chemin vers `user_profile.json` |
| `allow_templates` | `bool` | Si `False` (défaut), rejette les fichiers marqués `is_template: true` |

**Lève** :
- `FileNotFoundError` si un fichier est introuvable
- `ValueError` si un fichier JSON est invalide
- `ValueError` si `allow_templates=False` et un fichier est un template public

**Exemple** :
```python
adapter = PersonalityAdapter(
    personality_path="config/personality_core.json",
    user_profile_path="data/profile/user_profile.json"
)
adapter.validate_required_sections()
context = adapter.prepare_adaptation_context()
```

---

## Constantes importantes

### `QUESTIONNAIRE_META`

```python
QUESTIONNAIRE_META: Dict[str, Dict[str, Any]] = {
    "q01_bien_etre_subjectif": {
        "label": "Bien-être subjectif",
        "duration_min": 7,
        "duration_max": 9,
        "min_for_partial": 7,
        "sections": ["swls", "panas_positif", "panas_negatif"],
    },
    # ...
}
```

### `QUESTIONNAIRE_ITEMS`

```python
QUESTIONNAIRE_ITEMS: Dict[str, List[Tuple[str, str, str]]] = {
    "q01_bien_etre_subjectif": [
        ("swls_01", "texte de la question...", "likert_7"),
        # ...
    ],
    # ...
}
```

Chaque item est un tuple `(question_id, texte_alfred, type_reponse)`.

---

## Erreurs communes

| Erreur | Cause | Solution |
|--------|-------|---------|
| `ValueError: Questionnaire inconnu` | `questionnaire_id` invalide | Vérifier les IDs dans `QUESTIONNAIRE_META` |
| `ValueError: Réponse hors-échelle` | Valeur Likert hors plage | Valider avant d'appeler `save_answer()` |
| `ValueError: choix_binaire, attendu A ou B` | Réponse binaire invalide | Passer `"A"` ou `"B"` |
| `ValueError: Template public` | Fichier `is_template: true` passé à `PersonalityAdapter` | Créer une instance privée avant utilisation |
| `FileNotFoundError` | Fichier JSON introuvable | Vérifier les chemins |

---

*Document créé le 2026-06-16 — Cognitive Products Lab*
