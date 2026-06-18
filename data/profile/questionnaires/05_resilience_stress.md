# Questionnaire 05 — Résilience et stress perçu
## CD-RISC-10 (Campbell-Sills & Stein, 2007) + PSS-4 (Cohen et al., 1983)

---

### Informations sur le framework

| Champ | Information |
|-------|-------------|
| **Framework Résilience** | Connor-Davidson Resilience Scale — 10 items (CD-RISC-10) |
| **Auteurs** | Campbell-Sills, L. & Stein, M.B. |
| **Année** | 2007 |
| **Publication** | Campbell-Sills, L. & Stein, M.B. (2007). Psychometric analysis and refinement of the Connor-Davidson Resilience Scale (CD-RISC): Validation of a 10-item measure of resilience. *Journal of Traumatic Stress*, 20(6), 1019-1028. |
| **Échelle originale complète** | Connor, K.M. & Davidson, J.R.T. (2003). Development of a new resilience scale: The Connor-Davidson Resilience Scale (CD-RISC). *Depression and Anxiety*, 18(2), 76-82. |
| **Framework Stress** | Perceived Stress Scale — 4 items (PSS-4) |
| **Auteurs** | Cohen, S., Kamarck, T., & Mermelstein, R. |
| **Année** | 1983 |
| **Publication** | Cohen, S., Kamarck, T., & Mermelstein, R. (1983). A global measure of perceived stress. *Journal of Health and Social Behavior*, 24(4), 385-396. |
| **Adaptation française PSS** | Lesage, F.X., Berjot, S., & Deschamps, F. (2012). Psychometric properties of the French versions of the Perceived Stress Scale. *International Journal of Occupational Medicine and Environmental Health*, 25(2), 178-184. |
| **Durée estimée** | 5-7 minutes |
| **Fréquence recommandée** | **Mensuelle** (indicateur de santé prioritaire) |
| **Domaine d'application** | Monitoring de la santé psychologique — usage personnel |

---

### Construits mesurés

**CD-RISC-10** — Résilience globale : capacité à faire face à l'adversité, à s'adapter aux changements, à rebondir après les difficultés, à maintenir son fonctionnement sous pression.

**PSS-4** — Stress perçu : niveau subjectif de stress ressenti, sentiment de contrôle sur sa vie, capacité perçue à faire face. Mesure l'expérience subjective du stress, pas les événements stressants objectifs.

> **Important** : Ces deux construits sont complémentaires mais distincts. Une personne peut avoir une résilience élevée (capacité théorique à rebondir) mais un stress perçu élevé actuellement (période difficile). Ce sont ces deux niveaux combinés qui guident le comportement ALFRED.

---

### Instructions de passation

---

*Ce questionnaire comporte deux parties. Répondez en vous basant sur les **4 dernières semaines**, pas uniquement aujourd'hui. Choisissez la réponse qui reflète le mieux votre vécu habituel récent.*

---

## PARTIE A — Résilience (CD-RISC-10)

*Indiquez dans quelle mesure chacune des affirmations suivantes est vraie pour vous :*

| Score | Signification |
|-------|---------------|
| **0** | Pas du tout vrai |
| **1** | Rarement vrai |
| **2** | Parfois vrai |
| **3** | Souvent vrai |
| **4** | Presque toujours vrai |

| N° | Affirmation | Ma réponse (0-4) |
|----|-------------|-----------------|
| **R1** | Je suis capable de m'adapter lorsque des changements surviennent | |
| **R2** | Je peux faire face à tout ce qui se présente à moi | |
| **R3** | J'essaie de voir le côté positif des choses même lorsque les choses ne se déroulent pas bien | |
| **R4** | Faire face au stress peut me fortifier | |
| **R5** | J'ai tendance à rebondir rapidement après les moments difficiles | |
| **R6** | Je crois que je peux atteindre mes buts même en faisant face à des obstacles | |
| **R7** | Sous pression, je reste concentré(e) et je pense de façon claire | |
| **R8** | Je n'abandonne pas facilement devant les problèmes | |
| **R9** | Je suis capable de gérer des sentiments désagréables | |
| **R10** | Je sais où trouver de l'aide | |

**Mon score de résilience total (R1+...+R10) :** ___ / 40

---

## PARTIE B — Stress perçu (PSS-4)

*Au cours du **dernier mois**, à quelle fréquence vous êtes-vous senti(e) dans les situations suivantes ?*

| Score | Signification |
|-------|---------------|
| **0** | Jamais |
| **1** | Presque jamais |
| **2** | Parfois |
| **3** | Assez souvent |
| **4** | Très souvent |

| N° | Affirmation | Ma réponse (0-4) |
|----|-------------|-----------------|
| **S1** | Au cours du dernier mois, à quelle fréquence vous êtes-vous senti(e) incapable de contrôler les aspects importants de votre vie ? | |
| **S2** | Au cours du dernier mois, à quelle fréquence avez-vous ressenti des difficultés qui s'accumulaient à un point tel que vous ne pouviez plus les surmonter ? | |
| **S3** | Au cours du dernier mois, à quelle fréquence avez-vous été capable de contrôler la façon dont vous utilisiez votre temps ? *(item inversé)* | |
| **S4** | Au cours du dernier mois, à quelle fréquence avez-vous eu l'impression que les choses allaient dans votre sens ? *(item inversé)* | |

> **Note pour S3 et S4** : ces items sont **inversés**. Lors du scoring, leur valeur sera retournée (4-score).

**Mon score stress brut :** ___ / 16 (avant inversion des items S3, S4)

---

### Après la passation — Où enregistrer vos réponses

1. Ouvrez `data/profile/scoring/answers_template.json`
2. Remplissez la section `resilience_stress` :

```json
"resilience_stress": {
  "completed": true,
  "date": "YYYY-MM-DD",
  "answers": {
    "r1": VOTRE_RÉPONSE,
    "r2": VOTRE_RÉPONSE,
    "r3": VOTRE_RÉPONSE,
    "r4": VOTRE_RÉPONSE,
    "r5": VOTRE_RÉPONSE,
    "r6": VOTRE_RÉPONSE,
    "r7": VOTRE_RÉPONSE,
    "r8": VOTRE_RÉPONSE,
    "r9": VOTRE_RÉPONSE,
    "r10": VOTRE_RÉPONSE,
    "s1": VOTRE_RÉPONSE,
    "s2": VOTRE_RÉPONSE,
    "s3": VOTRE_RÉPONSE,
    "s4": VOTRE_RÉPONSE
  }
}
```

---

### Clé de scoring détaillée

**CD-RISC-10 (Résilience) :**
- Items directs : R1, R2, R3, R4, R5, R6, R7, R8, R9, R10 (aucun item inversé)
- Score brut : somme des 10 items (0-40)
- Score normalisé 0-100 : `(score_brut / 40) × 100`
- Score normalisé élevé = résilience élevée

**PSS-4 (Stress perçu) :**
- Items directs : S1, S2 (score élevé = stress élevé)
- Items inversés : S3, S4 (recodage : 4-score avant calcul)
- Score brut : S1 + S2 + (4-S3) + (4-S4) = 0 à 16
- Score normalisé stress 0-100 : `(score_brut / 16) × 100`
- **Attention** : score normalisé élevé = stress élevé
- Pour le paramètre ALFRED : le score PSS est inversé pour la matrice (`100 - score_pss`) afin que niveau "élevé" = bien-être (faible stress)

---

### Interprétation des scores bruts

**CD-RISC-10 (Résilience) :**

| Score brut | Score normalisé | Interprétation |
|------------|----------------|----------------|
| 0-13 | 0-33 | Résilience faible — ressources limitées face à l'adversité |
| 14-26 | 34-66 | Résilience modérée — fonctionnel mais avec des zones de fragilité |
| 27-40 | 67-100 | Résilience élevée — bonne capacité d'adaptation et de rebond |

> Données normatives : score moyen dans la population générale ~ 31/40 (Campbell-Sills & Stein, 2007)

**PSS-4 (Stress perçu) :**

| Score brut | Score normalisé stress | Interprétation |
|------------|----------------------|----------------|
| 0-5 | 0-31 | Stress faible — bonne gestion subjective du stress |
| 6-10 | 37-62 | Stress modéré — pression ressentie mais gérable |
| 11-16 | 69-100 | Stress élevé — surcharge perçue, ressources insuffisantes |

> Données normatives : score moyen population générale ~ 5-6/16 (Cohen et al., 1983)

---

### Seuils d'alerte clinique

> Ces seuils sont indicatifs et ne constituent pas un diagnostic. En cas de score d'alerte persistant, consultez un professionnel de santé mentale.

- **CD-RISC-10 < 14/40 + PSS-4 > 10/16** : combinaison critique — ALFRED activera le mode de soutien renforcé
- **PSS-4 > 13/16** sur 2 mois consécutifs : stress chronique probable — envisager un accompagnement professionnel

---

*Références : Campbell-Sills & Stein (2007), Journal of Traumatic Stress, 20(6), 1019-1028 ; Cohen et al. (1983), Journal of Health and Social Behavior, 24(4), 385-396.*
