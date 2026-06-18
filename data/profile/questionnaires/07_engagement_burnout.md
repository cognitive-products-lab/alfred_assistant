# Questionnaire 07 — Engagement et risque burnout
## UWES-9 (Schaufeli & Bakker, 2004) + Indicateur de risque burnout (items originaux)

---

### Informations sur le framework

| Champ | Information |
|-------|-------------|
| **Framework Engagement** | Utrecht Work Engagement Scale — 9 items (UWES-9) |
| **Auteurs** | Schaufeli, W.B. & Bakker, A.B. |
| **Année** | 2004 |
| **Publication** | Schaufeli, W.B. & Bakker, A.B. (2004). Job demands, job resources, and their relationship with burnout and engagement: A multi-sample study. *Journal of Organizational Behavior*, 25(3), 293-315. |
| **Adaptation française** | Version francophone disponible dans la littérature, notamment : Neveu, J.P. (2007). Jailed resources: Conservation of resources theory as applied to burnout among prison guards. *Journal of Organizational Behavior*, 28(1), 21-42. |
| **Framework Burnout** | Inspiré du Maslach Burnout Inventory (Maslach & Jackson, 1981) — items **originaux** non soumis à copyright |
| **Note copyright** | Le MBI officiel est propriétaire (Mind Garden Inc.). Les 5 items d'indicateur de risque burnout ci-dessous sont originaux, fidèles aux construits de Maslach mais distincts de l'instrument officiel. |
| **Durée estimée** | 6-8 minutes |
| **Fréquence recommandée** | **Mensuelle** (indicateur de santé prioritaire) |
| **Domaine d'application** | Monitoring de la santé au travail — usage personnel |

---

### Construits mesurés

**UWES-9 — Engagement au travail (3 sous-dimensions) :**
- **Vigueur** : niveau d'énergie, de résistance mentale et de persévérance au travail
- **Dévouement** : sens, enthousiasme, inspiration, fierté et défi ressenti dans le travail
- **Absorption** : état de concentration totale, de flow, d'immersion dans le travail

**Indicateur de risque burnout (3 sous-dimensions) :**
- **Épuisement** : sentiment d'être vidé de ses ressources émotionnelles et physiques
- **Cynisme** : détachement, attitude négative ou distanciée envers son travail
- **Efficacité réduite** : doute sur sa compétence, impression de ne plus être performant

> **Note clinique** : l'engagement et le burnout sont deux extrémités d'un continuum mais ne sont pas simplement des opposés. On peut avoir une vigueur élevée mais un cynisme croissant (phase précoce de burnout). C'est pourquoi les deux mesures sont nécessaires.

---

### Instructions de passation

---

*Les questions suivantes portent sur votre rapport au travail au cours des **4 dernières semaines**. Répondez en pensant à votre travail au sens large (activité professionnelle principale, projets, missions).*

---

## PARTIE A — Engagement au travail (UWES-9)

*À quelle fréquence ressentez-vous les états décrits ci-dessous dans votre travail ?*

| Score | Signification |
|-------|---------------|
| **0** | Jamais |
| **1** | Quelques fois par an ou moins |
| **2** | Une fois par mois ou moins |
| **3** | Quelques fois par mois |
| **4** | Une fois par semaine |
| **5** | Quelques fois par semaine |
| **6** | Chaque jour |

**Vigueur (items UW1 à UW3)**

| N° | Affirmation | Ma réponse (0-6) |
|----|-------------|-----------------|
| **UW1** | Au travail, je déborde d'énergie | |
| **UW2** | Au travail, je me sens fort(e) et vigoureux/vigoureuse | |
| **UW3** | Lorsque je me lève le matin, j'ai envie d'aller travailler | |

**Dévouement (items UW4 à UW6)**

| N° | Affirmation | Ma réponse (0-6) |
|----|-------------|-----------------|
| **UW4** | Mon travail a du sens et de l'importance pour moi | |
| **UW5** | Je suis enthousiaste à propos de mon travail | |
| **UW6** | Mon travail m'inspire | |

**Absorption (items UW7 à UW9)**

| N° | Affirmation | Ma réponse (0-6) |
|----|-------------|-----------------|
| **UW7** | Quand je travaille, je m'oublie et le temps passe très vite | |
| **UW8** | Je suis totalement absorbé(e) par mon travail | |
| **UW9** | Il m'est difficile de me détacher de mon travail | |

---

## PARTIE B — Indicateur de risque burnout (items originaux)

*Pour les affirmations suivantes, indiquez la fréquence à laquelle vous avez ressenti cela au cours des **4 dernières semaines** :*

| Score | Signification |
|-------|---------------|
| **0** | Jamais |
| **1** | Rarement |
| **2** | Parfois |
| **3** | Souvent |
| **4** | Très souvent ou toujours |

**Épuisement**

| N° | Affirmation | Ma réponse (0-4) |
|----|-------------|-----------------|
| **BU1** | Je me sens vidé(e) de mon énergie émotionnelle et physique après ma journée de travail | |
| **BU2** | Je me sens épuisé(e) dès le matin à l'idée d'affronter ma journée de travail | |

**Cynisme / Détachement**

| N° | Affirmation | Ma réponse (0-4) |
|----|-------------|-----------------|
| **BU3** | Je me sens de plus en plus indifférent(e) ou distant(e) par rapport à mon travail | |

**Efficacité professionnelle réduite**

| N° | Affirmation | Ma réponse (0-4) |
|----|-------------|-----------------|
| **BU4** | Je doute de ma capacité à accomplir efficacement mon travail | |
| **BU5** | J'ai l'impression que, quoi que je fasse, mes efforts ne font pas vraiment de différence | |

---

### Après la passation — Où enregistrer vos réponses

1. Ouvrez `data/profile/scoring/answers_template.json`
2. Remplissez la section `engagement_burnout` :

```json
"engagement_burnout": {
  "completed": true,
  "date": "YYYY-MM-DD",
  "answers": {
    "uw1": VOTRE_RÉPONSE,
    "uw2": VOTRE_RÉPONSE,
    "uw3": VOTRE_RÉPONSE,
    "uw4": VOTRE_RÉPONSE,
    "uw5": VOTRE_RÉPONSE,
    "uw6": VOTRE_RÉPONSE,
    "uw7": VOTRE_RÉPONSE,
    "uw8": VOTRE_RÉPONSE,
    "uw9": VOTRE_RÉPONSE,
    "bu1": VOTRE_RÉPONSE,
    "bu2": VOTRE_RÉPONSE,
    "bu3": VOTRE_RÉPONSE,
    "bu4": VOTRE_RÉPONSE,
    "bu5": VOTRE_RÉPONSE
  }
}
```

---

### Clé de scoring

**UWES-9 (Engagement) :**

| Sous-dimension | Items | Calcul | Score brut max |
|----------------|-------|--------|---------------|
| Vigueur | UW1, UW2, UW3 | Moyenne | 6 |
| Dévouement | UW4, UW5, UW6 | Moyenne | 6 |
| Absorption | UW7, UW8, UW9 | Moyenne | 6 |
| **Engagement global** | UW1-UW9 | Moyenne générale | 6 |

Normalisation engagement : `(moyenne / 6) × 100`

**Indicateur de risque burnout :**

| Sous-dimension | Items | Calcul | Score brut max |
|----------------|-------|--------|---------------|
| Épuisement | BU1, BU2 | Moyenne | 4 |
| Cynisme | BU3 | Score direct | 4 |
| Efficacité réduite | BU4, BU5 | Moyenne | 4 |
| **Risque burnout global** | BU1-BU5 | Moyenne générale | 4 |

Normalisation burnout : `(moyenne / 4) × 100` → score élevé = risque élevé.
Pour la matrice ALFRED : le score burnout est inversé `(100 - score_burnout)` avant mapping.

---

### Seuils normatifs UWES-9 (Schaufeli & Bakker, 2004)

| Score moyen UWES-9 | Interprétation |
|-------------------|----------------|
| < 1.0 | Très faible engagement — zone critique |
| 1.0 - 2.99 | Faible engagement |
| 3.0 - 4.49 | Engagement moyen |
| 4.5 - 5.49 | Engagement élevé |
| ≥ 5.5 | Très fort engagement |

### Seuils d'alerte burnout

| Score risque burnout (0-4) | Interprétation |
|---------------------------|----------------|
| 0.0 - 1.0 | Risque faible |
| 1.0 - 2.5 | Risque modéré — surveiller |
| > 2.5 | Risque élevé — action recommandée |

> **Combinaison critique** : UWES-9 < 2.0 ET score risque burnout > 2.5 → situation d'épuisement professionnel probable. Consulter un professionnel de santé mentale.

---

*Références : Schaufeli, W.B. & Bakker, A.B. (2004). Journal of Organizational Behavior, 25(3), 293-315 ; Maslach, C. & Jackson, S.E. (1981). The measurement of experienced burnout. Journal of Organizational Behavior, 2(2), 99-113.*
