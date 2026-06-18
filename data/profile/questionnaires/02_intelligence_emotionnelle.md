# Questionnaire 02 — Intelligence émotionnelle
## Adapté du TEIQue-SF (Trait Emotional Intelligence Questionnaire - Short Form)

---

### Informations sur le framework

| Champ | Information |
|-------|-------------|
| **Framework** | Trait Emotional Intelligence Questionnaire — Short Form (TEIQue-SF) |
| **Auteur** | Petrides, K.V. |
| **Année** | 2009 |
| **Publication** | Petrides, K.V. (2009). Psychometric properties of the Trait Emotional Intelligence Questionnaire (TEIQue). In C. Stough, D.H. Saklofske, & J.D.A. Parker (Eds.), *Assessing Emotional Intelligence*. Springer, Boston, MA. |
| **Références complémentaires** | Mikolajczak, M., Luminet, O., Leroy, C., & Roy, E. (2007). Psychometric properties of the Trait Emotional Intelligence Questionnaire. *Journal of Personality Assessment*, 88(3), 338-353. |
| **Durée estimée** | 8-10 minutes |
| **Fréquence recommandée** | Semestrielle |
| **Domaine d'application** | Mesure de l'intelligence émotionnelle comme trait de personnalité — usage personnel non clinique |

---

### Construits mesurés

Ce questionnaire évalue 4 **facettes de l'intelligence émotionnelle** comme trait (IE-trait) :

- **Bien-être émotionnel** : satisfaction de vie, bonheur général, optimisme
- **Autocontrôle émotionnel** : régulation des émotions, contrôle des impulsions, gestion du stress
- **Émotivité** : empathie, perception et expression des émotions d'autrui et des siennes
- **Sociabilité émotionnelle** : compétences relationnelles, assertivité émotionnelle, gestion des relations

> **Note** : L'IE-trait mesurée ici diffère de l'IE-aptitude (modèle Mayer-Salovey-Caruso). L'IE-trait reflète la perception que vous avez de vos capacités émotionnelles, pas vos performances objectives sur des tâches émotionnelles.

---

### Instructions de passation

Lisez la consigne suivante avant de répondre :

---

*Les affirmations ci-dessous portent sur vos émotions et sur la façon dont vous les gérez. Indiquez dans quelle mesure chaque affirmation vous correspond, en utilisant l'échelle suivante :*

| Score | Signification |
|-------|---------------|
| **1** | Pas du tout d'accord |
| **2** | Plutôt pas d'accord |
| **3** | Un peu en désaccord |
| **4** | Ni d'accord ni en désaccord |
| **5** | Un peu d'accord |
| **6** | Plutôt d'accord |
| **7** | Tout à fait d'accord |

*Répondez spontanément. Il n'y a pas de bonnes ou mauvaises réponses — seule votre perception sincère compte.*

---

### Items

Notez votre réponse (1 à 7) dans la case à droite de chaque affirmation.

**Section A — Bien-être émotionnel (items EQ1 à EQ4)**

| N° | Affirmation | Ma réponse (1-7) |
|----|-------------|-----------------|
| **EQ1** | Dans l'ensemble, je suis satisfait(e) de ma vie | |
| **EQ2** | Je me sens optimiste quant à l'avenir | |
| **EQ3** | Je suis quelqu'un de généralement heureux/heureuse | |
| **EQ4** | Je vois le bon côté des choses même dans les situations difficiles | |

**Section B — Autocontrôle émotionnel (items EQ5 à EQ8)**

| N° | Affirmation | Ma réponse (1-7) |
|----|-------------|-----------------|
| **EQ5** | Je suis capable de contrôler mes émotions | |
| **EQ6** | Je garde mon calme dans les situations stressantes | |
| **EQ7** | Lorsque je suis contrarié(e), je reprends rapidement le dessus | |
| **EQ8** | Je suis capable de gérer la pression efficacement | |

**Section C — Émotivité (items EQ9 à EQ12)**

| N° | Affirmation | Ma réponse (1-7) |
|----|-------------|-----------------|
| **EQ9** | Je comprends facilement ce que ressentent les autres | |
| **EQ10** | J'exprime facilement mes émotions aux personnes qui me sont chères | |
| **EQ11** | Je suis très sensible aux émotions et aux besoins des autres | |
| **EQ12** | Je ressens profondément les émotions des personnes qui m'entourent | |

**Section D — Sociabilité émotionnelle (items EQ13 à EQ15)**

| N° | Affirmation | Ma réponse (1-7) |
|----|-------------|-----------------|
| **EQ13** | Je sais comment influer positivement sur les émotions des autres | |
| **EQ14** | Je suis à l'aise dans les situations sociales | |
| **EQ15** | Je suis capable de défendre mes droits sans agressivité | |

---

### Après la passation — Où enregistrer vos réponses

1. Ouvrez `data/profile/scoring/answers_template.json`
2. Remplissez la section `intelligence_emotionnelle` :

```json
"intelligence_emotionnelle": {
  "completed": true,
  "date": "YYYY-MM-DD",
  "answers": {
    "eq1": VOTRE_RÉPONSE,
    "eq2": VOTRE_RÉPONSE,
    "eq3": VOTRE_RÉPONSE,
    "eq4": VOTRE_RÉPONSE,
    "eq5": VOTRE_RÉPONSE,
    "eq6": VOTRE_RÉPONSE,
    "eq7": VOTRE_RÉPONSE,
    "eq8": VOTRE_RÉPONSE,
    "eq9": VOTRE_RÉPONSE,
    "eq10": VOTRE_RÉPONSE,
    "eq11": VOTRE_RÉPONSE,
    "eq12": VOTRE_RÉPONSE,
    "eq13": VOTRE_RÉPONSE,
    "eq14": VOTRE_RÉPONSE,
    "eq15": VOTRE_RÉPONSE
  }
}
```

---

### Clé de scoring (pour référence)

| Sous-dimension | Items | Items inversés | Calcul |
|----------------|-------|----------------|--------|
| Bien-être émotionnel | EQ1, EQ2, EQ3, EQ4 | Aucun | Moyenne |
| Autocontrôle émotionnel | EQ5, EQ6, EQ7, EQ8 | Aucun | Moyenne |
| Émotivité | EQ9, EQ10, EQ11, EQ12 | Aucun | Moyenne |
| Sociabilité émotionnelle | EQ13, EQ14, EQ15 | Aucun | Moyenne |
| **IE globale** | Tous les items (EQ1-EQ15) | Aucun | Moyenne générale |

Normalisation : score brut moyen (1-7) → score 0-100 par formule linéaire : `(score_brut - 1) / 6 × 100`

---

### Interprétation indicative

| Score normalisé (0-100) | Signification |
|------------------------|---------------|
| 0-33 | IE faible — difficultés de régulation émotionnelle ou de compréhension d'autrui |
| 34-66 | IE modérée — gestion fonctionnelle avec des axes de progression identifiables |
| 67-100 | IE élevée — excellente régulation émotionnelle, forte empathie, aisance relationnelle |

**Profils typiques :**

- **Bien-être faible + IE globale élevée** : compétences émotionnelles présentes mais mal appliquées à soi-même (care pour les autres mais pas pour soi)
- **Émotivité élevée + Autocontrôle faible** : forte empathie mais difficulté à ne pas absorber les émotions d'autrui
- **Sociabilité élevée + Émotivité faible** : aisance sociale "de surface" sans profondeur empathique

---

*Référence principale : Petrides, K.V. (2009). Psychometric properties of the Trait Emotional Intelligence Questionnaire (TEIQue). In C. Stough, D.H. Saklofske, & J.D.A. Parker (Eds.), Assessing Emotional Intelligence. Springer.*
