# Q09 — HEXACO-24 : Personnalité (6 dimensions)
## Questionnaire psychométrique ALFRED — Cognitive Products Lab

---

**ID** : `q09_hexaco_personnalite`  
**Framework** : HEXACO-PI-R (Ashton & Lee, 2004/2009) — version courte 24 items  
**Source** : Ashton, M. C. & Lee, K. (2009). *The HEXACO–60: A short measure of the major dimensions of personality*. Journal of Personality Assessment, 91(4), 340–345.  
**Domaine public** : Les items HEXACO sont disponibles librement sur hexaco.org  
**Durée estimée** : 8-10 minutes  
**Périodicité recommandée** : Annuelle (traits très stables)

---

## Pourquoi HEXACO plutôt que Big Five seul ?

HEXACO ajoute une **6ème dimension absente du Big Five** : **H — Honnêteté-Humilité**, qui mesure la sincérité, la modestie, l'équité et la non-manipulation. Cette dimension est particulièrement importante pour :
- Prédire les comportements éthiques au travail
- Détecter les tendances narcissiques ou manipulatrices
- Différencier la coopération authentique de la coopération stratégique

La dimension H influence directement le **ton** qu'ALFRED adoptera : plus direct et moins flatteur avec un score H élevé.

---

## Les 6 dimensions HEXACO

| Dim. | Label | Ce que ça mesure | Corrélé Big Five |
|------|-------|-----------------|-----------------|
| **H** | Honnêteté-Humilité | Sincérité, modestie, équité, anti-manipulation | Absent du Big Five |
| **E** | Émotivité | Anxiété, dépendance émotionnelle, empathie | ≈ Névrosisme |
| **X** | eXtraversion | Sociabilité, assertivité, estime de soi sociale | ≈ Extraversion |
| **A** | Agréabilité | Patience, flexibilité, tolérance, douceur | ≈ Agréabilité |
| **C** | Conscienciosité | Organisation, diligence, perfectionnisme | ≈ Conscienciosité |
| **O** | Ouverture | Curiosité intellectuelle, créativité, esthétique | ≈ Ouverture |

---

## Instructions de passation (pour l'utilisateur)

Je vais te poser 24 courtes affirmations sur ta façon d'être en général.  
Pour chacune, indique dans quelle mesure elle te correspond :

**1** = pas du tout d'accord  
**2** = plutôt pas d'accord  
**3** = ni l'un ni l'autre  
**4** = plutôt d'accord  
**5** = tout à fait d'accord

Il n'y a pas de bonnes ou mauvaises réponses — réponds selon ce que tu ressens vraiment, pas selon ce que tu voudrais être.

---

## Items et script conversationnel ALFRED

### Dimension H — Honnêteté-Humilité

**[H1 — direct]**
```
ALFRED : "Première affirmation — je ne serais jamais prêt(e) à flatter quelqu'un pour obtenir une faveur, même si ça pourrait m'aider. De 1 (pas du tout d'accord) à 5 (tout à fait d'accord)."
```
**Item ID** : `hex_h_01` | **Sens** : direct | **Échelle** : Likert 5

---

**[H2 — inversé]**
```
ALFRED : "Si cela m'avantageait, je serais prêt(e) à tromper discrètement les gens. De 1 à 5."
```
**Item ID** : `hex_h_02` | **Sens** : inversé (score = 6 - réponse) | **Échelle** : Likert 5

---

**[H3 — direct]**
```
ALFRED : "Je traite tout le monde de façon égale — que la personne ait du pouvoir ou non, que je puisse en tirer quelque chose ou pas. De 1 à 5."
```
**Item ID** : `hex_h_03` | **Sens** : direct | **Échelle** : Likert 5

---

**[H4 — inversé]**
```
ALFRED : "Le statut social, le luxe, les marques — j'avoue que ça m'attire plus que je ne le laisse paraître. De 1 à 5."
```
**Item ID** : `hex_h_04` | **Sens** : inversé (score = 6 - réponse) | **Échelle** : Likert 5

---

### Dimension E — Émotivité

**[E1 — direct]**
```
ALFRED : "Passons aux émotions — quand quelqu'un me blesse, j'ai besoin d'un bon moment avant de me sentir mieux, même si je ne le montre pas forcément. De 1 à 5."
```
**Item ID** : `hex_e_01` | **Sens** : direct | **Échelle** : Likert 5

---

**[E2 — inversé]**
```
ALFRED : "En situation de stress ou de pression, je me détends assez facilement — ça ne me déstabilise pas longtemps. De 1 à 5."
```
**Item ID** : `hex_e_02` | **Sens** : inversé (score = 6 - réponse) | **Échelle** : Likert 5

---

**[E3 — direct]**
```
ALFRED : "Dans les moments difficiles, j'ai vraiment besoin du soutien de mes proches pour traverser ça. De 1 à 5."
```
**Item ID** : `hex_e_03` | **Sens** : direct | **Échelle** : Likert 5

---

**[E4 — inversé]**
```
ALFRED : "Je suis une personne assez peu sentimentale — les films et les histoires touchantes ne m'émeuvent pas beaucoup. De 1 à 5."
```
**Item ID** : `hex_e_04` | **Sens** : inversé (score = 6 - réponse) | **Échelle** : Likert 5

---

### Dimension X — eXtraversion

**[X1 — direct]**
```
ALFRED : "Nouvelle section — en groupe, j'aime être au centre de l'attention, animer, prendre la parole. De 1 à 5."
```
**Item ID** : `hex_x_01` | **Sens** : direct | **Échelle** : Likert 5

---

**[X2 — inversé]**
```
ALFRED : "Je préfère vraiment les activités solitaires ou en petit comité aux grandes réunions sociales. De 1 à 5."
```
**Item ID** : `hex_x_02` | **Sens** : inversé (score = 6 - réponse) | **Échelle** : Likert 5

---

**[X3 — direct]**
```
ALFRED : "Quand je rencontre de nouvelles personnes, j'entame facilement la conversation — je n'attends pas que l'autre fasse le premier pas. De 1 à 5."
```
**Item ID** : `hex_x_03` | **Sens** : direct | **Échelle** : Likert 5

---

**[X4 — inversé]**
```
ALFRED : "Dans les réunions ou soirées, j'ai souvent l'impression de ne pas avoir grand-chose à dire. De 1 à 5."
```
**Item ID** : `hex_x_04` | **Sens** : inversé (score = 6 - réponse) | **Échelle** : Likert 5

---

### Dimension A — Agréabilité

**[A1 — direct]**
```
ALFRED : "Je suis capable de pardonner facilement à quelqu'un qui m'a blessé(e), sans en garder de rancœur. De 1 à 5."
```
**Item ID** : `hex_a_01` | **Sens** : direct | **Échelle** : Likert 5

---

**[A2 — inversé]**
```
ALFRED : "Quand je ne suis pas d'accord avec quelqu'un, je le dis clairement — sans chercher à arrondir les angles. De 1 à 5."
```
**Item ID** : `hex_a_02` | **Sens** : inversé (score = 6 - réponse) | **Échelle** : Likert 5

---

**[A3 — direct]**
```
ALFRED : "Je préfère faire des compromis plutôt que de maintenir ma position jusqu'au bout d'une discussion. De 1 à 5."
```
**Item ID** : `hex_a_03` | **Sens** : direct | **Échelle** : Likert 5

---

**[A4 — inversé]**
```
ALFRED : "Je peux être assez critique envers les autres — surtout quand je pense qu'ils font les choses à moitié. De 1 à 5."
```
**Item ID** : `hex_a_04` | **Sens** : inversé (score = 6 - réponse) | **Échelle** : Likert 5

---

### Dimension C — Conscienciosité

**[C1 — direct]**
```
ALFRED : "Avant de rendre un travail, je vérifie toujours qu'il est exact et qu'il n'y a pas d'erreurs ou d'oublis. De 1 à 5."
```
**Item ID** : `hex_c_01` | **Sens** : direct | **Échelle** : Likert 5

---

**[C2 — inversé]**
```
ALFRED : "J'ai tendance à repousser les tâches — à laisser traîner des choses que j'aurais dû faire avant. De 1 à 5."
```
**Item ID** : `hex_c_02` | **Sens** : inversé (score = 6 - réponse) | **Échelle** : Likert 5

---

**[C3 — direct]**
```
ALFRED : "J'organise soigneusement mon temps et mes ressources — j'ai des systèmes, des listes, des méthodes. De 1 à 5."
```
**Item ID** : `hex_c_03` | **Sens** : direct | **Échelle** : Likert 5

---

**[C4 — inversé]**
```
ALFRED : "Il m'arrive d'être négligent(e) — de bâcler des tâches ou de ne pas finir ce que j'ai commencé. De 1 à 5."
```
**Item ID** : `hex_c_04` | **Sens** : inversé (score = 6 - réponse) | **Échelle** : Likert 5

---

### Dimension O — Ouverture à l'expérience

**[O1 — direct]**
```
ALFRED : "Dernière section — je suis curieux(se) de comprendre comment fonctionne le monde : les sciences, les comportements humains, les idées. De 1 à 5."
```
**Item ID** : `hex_o_01` | **Sens** : direct | **Échelle** : Likert 5

---

**[O2 — inversé]**
```
ALFRED : "Honnêtement, je ne me considère pas comme quelqu'un de très imaginatif ou créatif. De 1 à 5."
```
**Item ID** : `hex_o_02` | **Sens** : inversé (score = 6 - réponse) | **Échelle** : Likert 5

---

**[O3 — direct]**
```
ALFRED : "Quand j'ai un problème à résoudre, j'explore volontiers des approches inhabituelles — même si ça prend plus de temps. De 1 à 5."
```
**Item ID** : `hex_o_03` | **Sens** : direct | **Échelle** : Likert 5

---

**[O4 — inversé]**
```
ALFRED : "Je préfère les activités et environnements familiers aux expériences vraiment nouvelles. De 1 à 5."
```
**Item ID** : `hex_o_04` | **Sens** : inversé (score = 6 - réponse) | **Échelle** : Likert 5

---

## Conclusion de la session (script ALFRED)

```
ALFRED : "C'est terminé ! Merci pour ta franchise sur ces 24 affirmations — elles m'aident à mieux comprendre comment tu fonctionnes en profondeur.

Voici ce que je retiens pour adapter mon comportement à nos échanges.

[Afficher résumé descriptif selon les scores — voir scoring ci-dessous]

Je n'interprète pas ces résultats comme un diagnostic ou une étiquette — c'est une boussole pour mieux travailler ensemble."
```

---

## Clé de scoring

### Formule de calcul par dimension

```
score_dim = mean(items directs tels quels + items inversés après 6 - valeur)
Plage : [1.0 — 5.0]
```

### Items inversés (score = 6 - réponse brute)

| Dimension | Items inversés |
|-----------|---------------|
| H | `hex_h_02`, `hex_h_04` |
| E | `hex_e_02`, `hex_e_04` |
| X | `hex_x_02`, `hex_x_04` |
| A | `hex_a_02`, `hex_a_04` |
| C | `hex_c_02`, `hex_c_04` |
| O | `hex_o_02`, `hex_o_04` |

### Interprétation des scores

| Score | Interprétation |
|-------|---------------|
| **1.0 — 2.4** | Niveau bas sur cette dimension |
| **2.5 — 3.4** | Niveau moyen |
| **3.5 — 5.0** | Niveau élevé |

### Interprétation de H (Honnêteté-Humilité) — dimension clé

| Score H | Profil | Impact ALFRED |
|---------|--------|--------------|
| H ≥ 3.5 | Sincérité élevée, peu de manipulation | Ton direct, peu de flatterie, feedback honnête |
| 2.5 ≤ H < 3.5 | Profil équilibré | Ton adaptatif selon le contexte |
| H < 2.5 | Tendances à la flatterie ou au statut | Tone neutre + vigilance biais confirmation |

---

## Impact sur les paramètres ALFRED

| Dimension | Score élevé | Score bas |
|-----------|-------------|----------|
| **H** | Ton direct, pas de flatterie | Ton neutre, évite la confrontation |
| **E** | emotional_support_level = empathique | emotional_support_level = factuel |
| **X** | proactivity = élevé, tone = chaleureux | proactivity = minimal, tone = équilibré |
| **A** | challenge_level = confort (évite conflit) | challenge_level = modéré (direct) |
| **C** | structure_preference = structuré, explanation_depth = approfondi | structure_preference = fluide |
| **O** | explanation_depth = approfondi, humor_level = présent | explanation_depth = standard |

---

## Notes méthodologiques

- **Biais de désirabilité sociale** : HEXACO est conçu pour minimiser ce biais grâce à la formulation des items H. Rassurer l'utilisateur : il n'y a pas de "bonnes" réponses.
- **Stabilité temporelle** : les 6 dimensions HEXACO sont très stables (corrélations test-retest r > 0.70 à 6 semaines). Périodicité annuelle suffisante.
- **Cross-culturel** : validé dans plus de 20 pays dont la France. La traduction française est disponible sur hexaco.org.
- **Complément au TIPI** : HEXACO-24 et TIPI mesurent en partie les mêmes construits (OCEAN), mais HEXACO ajoute H et offre 4 items par dimension vs 2 pour TIPI → meilleure fiabilité.

---

*Questionnaire créé le 2026-06-16 — Cognitive Products Lab*  
*Source : Ashton & Lee (2004, 2009) — Items HEXACO libres de droits (hexaco.org)*
