# Tests — Module Profil IA Adaptative
## Guide de lancement et interprétation

> Version 1.0 — 2026-06-16

---

## Prérequis

```bash
# Python 3.13+
python --version

# Installer pytest
pip install pytest pytest-cov

# Depuis la racine du projet alfred_assistant/
cd /chemin/vers/alfred_assistant
```

---

## Lancer les tests

### Tous les tests du module

```bash
pytest docs/module_profil_ia_adaptative/tests/ -v
```

### Tests par fichier

```bash
# Tests unitaires — QuestionnaireSession
pytest docs/module_profil_ia_adaptative/tests/test_profile_analyzer.py -v

# Tests unitaires — PersonalityAdapter
pytest docs/module_profil_ia_adaptative/tests/test_personality_adapter.py -v

# Tests du scoring
pytest docs/module_profil_ia_adaptative/tests/test_scoring.py -v

# Tests d'intégration
pytest docs/module_profil_ia_adaptative/tests/integration/test_full_pipeline.py -v
```

### Tests avec couverture

```bash
pytest docs/module_profil_ia_adaptative/tests/ -v --cov=src --cov-report=term-missing
```

### Tests d'un seul test

```bash
pytest docs/module_profil_ia_adaptative/tests/test_profile_analyzer.py::TestComputeScores::test_q01_swls_total_correct -v
```

---

## Description des fichiers de test

### `test_profile_analyzer.py`

Tests unitaires complets pour `src/profile/profile_analyzer.py` (classe `QuestionnaireSession`).

| Classe de test | Méthode testée | Nb de tests |
|---------------|---------------|------------|
| `TestNextQuestion` | `next_question()` | ~6 |
| `TestSaveAnswer` | `save_answer()` | ~10 |
| `TestGetProgress` | `get_progress()` | ~5 |
| `TestCanComputePartialScores` | `can_compute_partial_scores()` | ~4 |
| `TestComputeScores` | `compute_scores()` | ~12 |

**Pattern** : utilise `tmp_path` de pytest → chaque test est isolé dans un dossier temporaire.

### `test_personality_adapter.py`

Tests unitaires pour `src/core/personality_adapter.py` (classe `PersonalityAdapter`).

| Classe de test | Méthode testée | Nb de tests |
|---------------|---------------|------------|
| `TestPersonalityAdapterInit` | `__init__()` | ~6 |
| `TestValidateRequiredSections` | `validate_required_sections()` | ~3 |
| `TestAdaptationMethods` | Méthodes d'adaptation | ~6 |

### `test_scoring.py`

Tests unitaires des méthodes de scoring statiques.

| Classe de test | Description |
|---------------|-------------|
| `TestScoringHelpers` | Tests `_mean()` et `_sum_likert()` |
| `TestScoreQ01` | Calcul SWLS + PANAS |
| `TestScoreQ02` | Style cognitif + profil analytique/intuitif |
| `TestScoreQ03` | Régulation émotionnelle + inversion PSS |
| `TestScoreQ04` | Motivations SDT + détection dominante |

### `integration/test_full_pipeline.py`

Tests d'intégration end-to-end simulant une passation complète.

| Test | Description |
|------|-------------|
| `test_full_questionnaire_q01` | Passation complète Q01 + vérification scores |
| `test_multiple_questionnaires_independent` | Q01 + Q02 indépendants |
| `test_session_resume_after_partial` | Reprise après interruption |
| `test_complete_pipeline_q01_q04` | Passation des 4 questionnaires en séquence |

---

## Fixtures

### `fixtures/sample_answers.json`

Réponses de test valides pour les 4 questionnaires. Utilisées dans les tests d'intégration.

### `fixtures/expected_scores.json`

Scores attendus correspondant à `sample_answers.json`. Utilisés pour vérifier la correction des calculs.

---

## Interpréter les résultats

### Sortie normale (tous les tests passent)

```
tests/test_profile_analyzer.py::TestNextQuestion::test_returns_first_question PASSED
tests/test_profile_analyzer.py::TestSaveAnswer::test_saves_valid_likert7_answer PASSED
...
========================= 37 passed in 0.85s =========================
```

### Test en échec

```
tests/test_profile_analyzer.py::TestComputeScores::test_q01_swls_total_correct FAILED
─────────────────────────── FAILURES ──────────────────────────────
AssertionError: assert 26 == 28
```

→ Vérifier `_score_q01()` dans `src/profile/profile_analyzer.py` + les réponses dans `fixtures/sample_answers.json`.

### Erreur d'import

```
ModuleNotFoundError: No module named 'src.profile.profile_analyzer'
```

→ Lancer depuis la racine du projet (`/alfred_assistant/`) :
```bash
cd /chemin/vers/alfred_assistant
pytest docs/module_profil_ia_adaptative/tests/ -v
```

---

## Ajouter un test

1. Identifier le fichier cible (`test_profile_analyzer.py`, etc.)
2. Ajouter la méthode dans la classe appropriée
3. Utiliser `tmp_path` pour les fichiers temporaires
4. Suivre le pattern des tests existants

```python
def test_nouveau_comportement(tmp_path):
    # Arrange
    session = make_session(tmp_path)
    
    # Act
    result = session.next_question("q01_bien_etre_subjectif")
    
    # Assert
    assert result is not None
    assert result["type"] == "likert_7"
```

---

*Document créé le 2026-06-16 — Cognitive Products Lab*
