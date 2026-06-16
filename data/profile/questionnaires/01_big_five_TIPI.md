# Questionnaire 01 — Big Five (TIPI)
## Ten-Item Personality Inventory — Version française

---

### Informations sur le framework

| Champ | Information |
|-------|-------------|
| **Framework** | Ten-Item Personality Inventory (TIPI) |
| **Auteurs originaux** | Gosling, S.D., Rentfrow, P.J., & Swann, W.B. Jr. |
| **Année** | 2003 |
| **Publication** | Journal of Research in Personality, 37(6), 504-528 |
| **Adaptation française** | Basé sur la version française adaptée (cf. Hahn et al., 2012 pour la validation en langue germanique ; version française dans la littérature académique francophone) |
| **Durée estimée** | 3-5 minutes |
| **Fréquence recommandée** | Annuelle |
| **Domaine d'application** | Mesure rapide des traits de personnalité Big Five pour usage non clinique |

---

### Construits mesurés

Ce questionnaire évalue les **5 grandes dimensions de la personnalité** (modèle Big Five / OCEAN) :

- **O — Ouverture à l'expérience** : curiosité intellectuelle, créativité, sensibilité esthétique, ouverture aux idées nouvelles
- **C — Conscienciosité** : organisation, autodiscipline, fiabilité, persévérance, sens du devoir
- **E — Extraversion** : sociabilité, assertivité, enthousiasme, énergie relationnelle
- **A — Agréabilité** : bienveillance, coopération, confiance, empathie
- **N — Stabilité émotionnelle** (inverse du Neuroticisme) : calme émotionnel, résistance aux émotions négatives

> **Note importante** : Votre profil AssessFirst (SWIPE) constitue la source de vérité prioritaire pour les Big Five. Ce questionnaire sert de mesure complémentaire légère et de vérification de cohérence périodique. En cas de discordance, les données AssessFirst priment.

---

### Instructions de passation

Lisez la consigne suivante avant de répondre :

---

*Voici quelques traits de personnalité qui peuvent vous décrire ou non. Pour chaque paire d'adjectifs, indiquez dans quelle mesure elle vous correspond en tant que personne, en utilisant l'échelle suivante :*

| Score | Signification |
|-------|---------------|
| **1** | Pas du tout d'accord |
| **2** | Plutôt pas d'accord |
| **3** | Un peu en désaccord |
| **4** | Ni d'accord ni en désaccord |
| **5** | Un peu d'accord |
| **6** | Plutôt d'accord |
| **7** | Tout à fait d'accord |

*Je me vois comme quelqu'un qui est...*

---

### Items

Notez votre réponse (1 à 7) dans la case à droite de chaque affirmation.

| N° | Affirmation | Ma réponse (1-7) |
|----|-------------|-----------------|
| **Q1** | ...extraverti(e), enthousiaste | |
| **Q2** | ...critique, conflictuel(le) | |
| **Q3** | ...fiable, autodiscipliné(e) | |
| **Q4** | ...anxieux/anxieuse, facilement perturbé(e) | |
| **Q5** | ...ouvert(e) à de nouvelles expériences, complexe | |
| **Q6** | ...réservé(e), discret/discrète | |
| **Q7** | ...sympathique, chaleureux/chaleureuse | |
| **Q8** | ...désordonné(e), négligent(e) | |
| **Q9** | ...calme, émotionnellement stable | |
| **Q10** | ...conventionnel(le), peu créatif/créative | |

---

### Après la passation — Où enregistrer vos réponses

1. Ouvrez `data/profile/scoring/answers_template.json`
2. Remplissez la section `big_five_TIPI` :

```json
"big_five_TIPI": {
  "completed": true,
  "date": "YYYY-MM-DD",
  "answers": {
    "q1": VOTRE_RÉPONSE,
    "q2": VOTRE_RÉPONSE,
    "q3": VOTRE_RÉPONSE,
    "q4": VOTRE_RÉPONSE,
    "q5": VOTRE_RÉPONSE,
    "q6": VOTRE_RÉPONSE,
    "q7": VOTRE_RÉPONSE,
    "q8": VOTRE_RÉPONSE,
    "q9": VOTRE_RÉPONSE,
    "q10": VOTRE_RÉPONSE
  }
}
```

---

### Clé de scoring (pour référence)

Le calcul détaillé est dans `data/profile/scoring/scoring_keys.json`. Pour votre information :

| Dimension | Items directs | Items inversés | Calcul |
|-----------|---------------|----------------|--------|
| Extraversion (E) | Q1 | Q6 | Moyenne(Q1, 8-Q6) |
| Agréabilité (A) | Q7 | Q2 | Moyenne(Q7, 8-Q2) |
| Conscienciosité (C) | Q3 | Q8 | Moyenne(Q3, 8-Q8) |
| Stabilité émotionnelle (N inversé) | Q9 | Q4 | Moyenne(Q9, 8-Q4) |
| Ouverture (O) | Q5 | Q10 | Moyenne(Q5, 8-Q10) |

**Les items inversés** (Q2, Q4, Q6, Q8, Q10) sont recodés : score inversé = 8 - score original.

Le score brut (1-7) est ensuite normalisé sur 0-100 par le module `profile_analyzer.py`.

---

### Interprétation indicative

| Score normalisé (0-100) | Signification |
|------------------------|---------------|
| 0-19 | Très faible sur cette dimension |
| 20-39 | Faible — en dessous de la moyenne |
| 40-59 | Dans la moyenne populationnelle |
| 60-79 | Élevé — au-dessus de la moyenne |
| 80-100 | Très élevé sur cette dimension |

**Ce que mesure chaque dimension en pratique :**

- **Ouverture élevée** : curiosité intellectuelle marquée, goût pour l'abstraction, créativité, ouverture aux idées non conventionnelles
- **Conscienciosité élevée** : organisation naturelle, fiabilité, tendance à planifier, perfectionnisme éventuel
- **Extraversion élevée** : rechargement de l'énergie en groupe, assertivité, communication facile
- **Agréabilité élevée** : tendance à la coopération, empathie prononcée, évitement des conflits
- **Stabilité émotionnelle élevée** : calme sous pression, résilience aux critiques, faible anxiété de base

---

*Référence : Gosling, S.D., Rentfrow, P.J., & Swann, W.B. Jr. (2003). A very brief measure of the Big Five personality domains. Journal of Research in Personality, 37(6), 504-528.*
