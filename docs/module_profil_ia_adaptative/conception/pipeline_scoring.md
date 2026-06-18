# Pipeline de scoring — Normalisation & Mapping
## Module Profil IA Adaptative — ALFRED

> Version 1.0 — 2026-06-16

---

## Vue d'ensemble du pipeline

```
Réponses brutes    Calcul sous-échelles   Normalisation    Mapping            Paramètres ALFRED
(valeurs Likert) ──────────────────────▶  (scores bruts) ──(0-100)──▶ (matrice 40 règles) ──▶ (9 paramètres)
```

Le pipeline s'exécute en 5 étapes successives :

1. **Collecte** : réponses Likert brutes par item (via `QuestionnaireSession`)
2. **Agrégation** : calcul des scores par sous-échelle (somme ou moyenne)
3. **Normalisation** : conversion vers l'échelle 0-100
4. **Mapping** : application des règles de la matrice `alfred_mapping_matrix.json`
5. **Consolidation** : fusion des règles conflictuelles, génération des 9 paramètres ALFRED

---

## Étape 1 — Collecte des réponses

### Formats de réponse acceptés

| Type | Valeurs valides | Questionnaires |
|------|----------------|----------------|
| `likert_5` | Entier 1-5 | Q03, Q04, Q06, Q07 (certains items) |
| `likert_7` | Entier 1-7 | Q01, Q02, Q03 (certains) |
| `likert_06` | Entier 0-6 | Q07 (UWES-9) |
| `choix_binaire` | "A" ou "B" | Q02 (items de format) |
| `texte_libre` | String quelconque | Q00 (qualitatif) |

### Validation à la saisie (`_validate_answer`)
```python
# Exemple — Likert 7
val = int(answer)
if not (1 <= val <= 7):
    raise ValueError(f"Hors-échelle pour '{question_id}': attendu 1-7, reçu {val}")
```

Toute réponse invalide lève une `ValueError` avant persistance.

---

## Étape 2 — Calcul des sous-échelles

### Q01 — Bien-être subjectif (SWLS + PANAS-SF)

```
SWLS (Satisfaction With Life Scale)
────────────────────────────────────
Items   : swls_01, swls_02, swls_03, swls_04, swls_05
Méthode : Somme
Plage   : [5, 35]

Interprétation :
  5-9   → Très insatisfait
  10-14 → Insatisfait
  15-19 → Légèrement insatisfait
  20    → Point neutre
  21-25 → Légèrement satisfait
  26-30 → Satisfait
  31-35 → Très satisfait

PANAS Positif (Positive Affect)
───────────────────────────────
Items   : pan_p_01, pan_p_02, pan_p_03, pan_p_04, pan_p_05
Méthode : Somme
Plage   : [5, 35]

PANAS Négatif (Negative Affect)
───────────────────────────────
Items   : pan_n_01, pan_n_02, pan_n_03, pan_n_04
Méthode : Somme
Plage   : [4, 28]
```

**Code** :
```python
def _score_q01(self, answers):
    swls_total = sum(answers[k] for k in ["swls_01"..."swls_05"])
    panas_pos = sum(answers[k] for k in ["pan_p_01"..."pan_p_05"])
    panas_neg = sum(answers[k] for k in ["pan_n_01"..."pan_n_04"])
    return {"swls_total": swls_total, "panas_positif": panas_pos, "panas_negatif": panas_neg}
```

### Q02 — Style cognitif

```
Score analytique  : mean(cog_a_01, cog_a_02, cog_a_03, cog_a_04)    [1, 7]
Score intuitif    : mean(cog_i_01, cog_i_02, cog_i_03, cog_i_04)    [1, 7]
Score verbal      : mean(cog_v_01, cog_v_02, cog_v_03)               [1, 7]
Score visuel      : mean(cog_vs_01, cog_vs_02, cog_vs_03)            [1, 7]

Profil A/I :
  diff = score_analytique - score_intuitif
  diff > +1.5  → profil = "analytique"
  diff < -1.5  → profil = "intuitif"
  else         → profil = "mixte"

Profil V/VS :
  diff = score_verbal - score_visuel
  diff > +1.0  → profil = "verbal"
  diff < -1.0  → profil = "visuel_spatial"
  else         → profil = "mixte"
```

### Q03 — Régulation émotionnelle

```
Réévaluation cognitive : mean(re_01, re_02, re_03, re_04, re_05)    [1, 5]
Suppression            : mean(sup_01, sup_02, sup_03)                [1, 5]

PSS (Perceived Stress Scale) :
  Items normaux  : str_01, str_02, str_03, str_05                    [0, 4 chacun]
  Item inversé   : str_04 → score_item = 6 - réponse_brute
  PSS total      = somme(5 items après inversion)                    [0, 20]
  
  ATTENTION : str_04 est un item positif ("vous avez réussi à gérer...")
  → Score élevé sur cet item = MOINS de stress → inversion obligatoire
```

### Q04 — Motivations SDT (Self-Determination Theory)

```
Autonomie     : mean(sdt_aut_01 ... sdt_aut_06)    [1, 5]
Compétence    : mean(sdt_comp_01 ... sdt_comp_06)  [1, 5]
Appartenance  : mean(sdt_app_01 ... sdt_app_06)    [1, 5]

Dominante :
  max_k = argmax(autonomie, compétence, appartenance)
  diff = max_valeur - second_plus_haut
  diff >= 0.5 → dominante = max_k
  diff < 0.5  → dominante = "equilibre"
```

---

## Étape 3 — Normalisation 0-100

### Formule générale

```
score_normalisé = (score_brut - min_théorique) / (max_théorique - min_théorique) × 100
```

### Table de normalisation par sous-échelle

| Sous-échelle | Brut min | Brut max | Formule |
|-------------|----------|----------|---------|
| SWLS total | 5 | 35 | `(x - 5) / 30 × 100` |
| PANAS positif | 5 | 35 | `(x - 5) / 30 × 100` |
| PANAS négatif | 4 | 28 | `(x - 4) / 24 × 100` (inversé : `100 - formule`) |
| Score analytique | 1 | 7 | `(x - 1) / 6 × 100` |
| Score intuitif | 1 | 7 | `(x - 1) / 6 × 100` |
| Réévaluation cognitive | 1 | 5 | `(x - 1) / 4 × 100` |
| Suppression | 1 | 5 | `(x - 1) / 4 × 100` |
| PSS | 0 | 20 | `x / 20 × 100` (inversé : `100 - formule`) |
| Autonomie SDT | 1 | 5 | `(x - 1) / 4 × 100` |
| Compétence SDT | 1 | 5 | `(x - 1) / 4 × 100` |
| Appartenance SDT | 1 | 5 | `(x - 1) / 4 × 100` |

**Note sur l'inversion** : les scores de stress (PSS) et d'affect négatif (PANAS-) sont inversés pour que 100 = optimal (pas de stress, pas d'affect négatif).

---

## Étape 4 — Matrice de mapping (`alfred_mapping_matrix.json`)

### Architecture de la matrice

La matrice contient **40 règles individuelles** et **4 règles de combinaison** mappant les scores vers 9 paramètres comportementaux ALFRED.

**Structure d'une règle** :
```json
{
  "rule_id": "R001",
  "dimension": "bien_etre",
  "subscale": "swls_total",
  "condition": {"operator": ">=", "threshold": 25},
  "output": {
    "parameter": "emotional_support_level",
    "value": "equilibre",
    "priority": "standard"
  },
  "rationale": "Satisfaction de vie élevée → pas besoin de soutien émotionnel renforcé"
}
```

### Paramètres ALFRED et valeurs possibles

| Paramètre | Valeurs | Description |
|-----------|---------|-------------|
| `tone` | `formel` / `equilibre` / `chaleureux` / `casual` | Registre de langue |
| `response_length` | `court` / `moyen` / `long` / `adaptatif` | Longueur des réponses |
| `proactivity` | `minimal` / `modere` / `eleve` | Initiative prise par ALFRED |
| `emotional_support_level` | `factuel` / `equilibre` / `empathique` | Niveau de soutien émotionnel |
| `challenge_level` | `confort` / `modere` / `intense` | Niveau de challenge proposé |
| `check_in_frequency` | `jamais` / `mensuel` / `hebdo` / `quotidien` | Fréquence des prises de nouvelles |
| `explanation_depth` | `surface` / `standard` / `approfondi` | Profondeur des explications |
| `humor_level` | `aucun` / `sobre` / `present` | Présence d'humour |
| `structure_preference` | `fluide` / `mixte` / `structure` | Format des réponses |

### Exemples de règles clés

```
SWLS >= 25    →  emotional_support_level = "équilibré"       (priorité: standard)
SWLS < 15     →  emotional_support_level = "empathique"      (priorité: élevée)

PSS >= 14     →  check_in_frequency = "quotidien"            (priorité: ALERTE)
              →  challenge_level = "confort"                  (priorité: ALERTE)
              →  emotional_support_level = "empathique"       (priorité: ALERTE)

profil_ai = "analytique"  →  explanation_depth = "approfondi"   (standard)
profil_ai = "intuitif"    →  explanation_depth = "surface"       (standard)

motivation_dominante = "autonomie"  →  proactivity = "minimal"   (standard)
motivation_dominante = "appartenance" → proactivity = "élevé"    (standard)

UWES < 2.5 ET PSS >= 12  →  ALERTE BURNOUT
                         →  tous paramètres → mode soutien maximal
```

---

## Étape 5 — Consolidation et résolution de conflits

### Règles de priorité

```
CRITIQUE > ALERTE > ÉLEVÉE > STANDARD
```

Si deux règles ciblent le même paramètre avec des valeurs différentes, la priorité la plus haute gagne.

**Exemple** :
- Règle R012 (standard) : RIASEC_S élevé → tone = "chaleureux"
- Règle R035 (alerte) : PSS > 14 → tone = "empathique"
- **Résultat** : tone = "empathique" (alerte gagne sur standard)

### Règles de combinaison (4 règles)

```json
{
  "combo_id": "C001",
  "label": "Burnout critique",
  "conditions": [
    {"subscale": "uwes_global", "operator": "<", "value": 2.5},
    {"subscale": "pss_total", "operator": ">=", "value": 12}
  ],
  "operator": "AND",
  "override_all": true,
  "output": {
    "emotional_support_level": "empathique",
    "check_in_frequency": "quotidien",
    "challenge_level": "confort",
    "proactivity": "minimal",
    "tone": "chaleureux"
  }
}
```

### Output final

Le résultat est un objet Python / JSON :
```json
{
  "computed_at": "2026-06-16T09:00:00Z",
  "source_scores": { "swls_total": 28, "panas_positif": 30, "pss_total": 5, ... },
  "alerts": [],
  "alfred_params": {
    "tone": "equilibre",
    "response_length": "moyen",
    "proactivity": "modere",
    "emotional_support_level": "equilibre",
    "challenge_level": "intense",
    "check_in_frequency": "mensuel",
    "explanation_depth": "approfondi",
    "humor_level": "sobre",
    "structure_preference": "structure"
  }
}
```

---

## Gestion des données manquantes

### Stratégies par situation

| Situation | Comportement |
|-----------|-------------|
| Item unique manquant | `_mean()` / `_sum_likert()` ignorent les `None` |
| Questionnaire incomplet | `compute_scores(partial=True)` si seuil atteint |
| Questionnaire non commencé | Score = None → paramètre ALFRED = valeur par défaut |
| Toutes réponses None | Retourne None → pas de calcul |

### Valeurs par défaut des paramètres ALFRED
Si aucun score disponible pour un paramètre, les valeurs par défaut s'appliquent :
- tone = "equilibre", response_length = "moyen", proactivity = "modere"
- emotional_support_level = "equilibre", challenge_level = "modere"
- check_in_frequency = "jamais", explanation_depth = "standard"
- humor_level = "sobre", structure_preference = "mixte"

---

## Seuils d'alerte et notifications

### Alertes actives en V1

| ID | Condition | Paramètres impactés | Message utilisateur |
|----|-----------|--------------------|--------------------|
| A001 | PSS >= 14 | check_in + challenge + support | Soutien renforcé silencieux |
| A002 | UWES < 2.5 | check_in + challenge + tone | Check-in activé |
| A003 | UWES < 2.5 ET PSS >= 12 | Tous → mode soutien | Suggestion consultation |
| A004 | CD-RISC < 20 | emotional_support + proactivity | Adaptation silencieuse |

**Principe d'alerte** : ALFRED adapte son comportement silencieusement. Il ne diagnostique pas, ne médicalise pas. Si l'alerte A003 est déclenchée, ALFRED peut simplement dire :
> "Je remarque que tu sembles avoir beaucoup à gérer en ce moment. Je suis là si tu veux en parler."

---

## Périodicité de re-calcul

| Dimension | Fréquence | Justification |
|-----------|-----------|---------------|
| Stress (PSS) | Mensuelle | État variable — capture les fluctuations |
| Engagement/Burnout | Mensuelle | Indicateur de santé psychologique |
| Chronotype | Trimestrielle | Stable mais influence saisonnière possible |
| Intelligence émotionnelle | Semestrielle | Trait semi-stable, évolue avec la pratique |
| Communication | Semestrielle | Mode dominant peut changer avec l'expérience |
| Big Five | Annuelle | Traits très stables chez l'adulte |
| Valeurs Schwartz | Annuelle | Valeurs fondamentales = très stables |
| RIASEC | Annuelle | Intérêts professionnels évoluent lentement |
| AssessFirst | Changement de vie | Traits profonds — benchmarkés sur population |

---

*Document créé le 2026-06-16 — Cognitive Products Lab*
