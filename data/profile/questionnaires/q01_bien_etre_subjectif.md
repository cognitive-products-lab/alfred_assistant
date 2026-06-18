# Q01 — Bien-être subjectif (SWLS + PANAS-SF adapté)

**ID** : `q01_bien_etre_subjectif`
**Durée estimée** : 7–9 minutes
**Format des réponses** : Échelle de 1 à 7 (Likert 7 points)
**Nombre d'items** : 14
**Scoring** : SWLS (5 items, score /35) + PANAS-SF positif (5 items) + négatif (4 items)
**Seuil partiel** : 7 réponses minimum pour un score indicatif

---

## Objectif

Mesurer la satisfaction globale de vie et l'état affectif récent (affects positifs vs négatifs).
Ces données permettent à ALFRED d'ajuster son niveau de soutien, le ton de ses interactions
et de détecter des besoins de régulation émotionnelle.

---

## Cadre théorique

- **SWLS** (Satisfaction With Life Scale — Diener et al., 1985) : 5 items, étalonnage population générale
- **PANAS-SF** (Positive and Negative Affect Schedule short form — Watson et al., 1988) : 10 items adaptés en français
- Adaptation conversationnelle pour ALFRED : reformulation en langue naturelle, tutoiement, ton bienveillant

---

## Items

### Section A — Satisfaction de vie (SWLS)

| ID | Texte original | Type |
|----|---------------|------|
| swls_01 | Dans l'ensemble, ma vie correspond presque à mon idéal | likert_7 |
| swls_02 | Les conditions de ma vie sont excellentes | likert_7 |
| swls_03 | Je suis satisfait(e) de ma vie | likert_7 |
| swls_04 | Jusqu'à présent, j'ai obtenu les choses importantes que je voulais dans la vie | likert_7 |
| swls_05 | Si je pouvais recommencer ma vie, je ne changerais presque rien | likert_7 |

### Section B — Affects positifs (PANAS-SF)

| ID | Texte original | Type |
|----|---------------|------|
| pan_p_01 | Ces dernières semaines, je me suis senti(e) **enthousiaste** | likert_7 |
| pan_p_02 | Ces dernières semaines, je me suis senti(e) **actif/active** et **énergique** | likert_7 |
| pan_p_03 | Ces dernières semaines, je me suis senti(e) **inspiré(e)** | likert_7 |
| pan_p_04 | Ces dernières semaines, je me suis senti(e) **déterminé(e)** | likert_7 |
| pan_p_05 | Ces dernières semaines, je me suis senti(e) **attentif/attentive** et **concentré(e)** | likert_7 |

### Section C — Affects négatifs (PANAS-SF)

| ID | Texte original | Type |
|----|---------------|------|
| pan_n_01 | Ces dernières semaines, je me suis senti(e) **irritable** ou **agacé(e)** | likert_7 |
| pan_n_02 | Ces dernières semaines, je me suis senti(e) **stressé(e)** ou **sous pression** | likert_7 |
| pan_n_03 | Ces dernières semaines, je me suis senti(e) **nerveux/nerveuse** ou **anxieux/anxieuse** | likert_7 |
| pan_n_04 | Ces dernières semaines, je me suis senti(e) **épuisé(e)** ou **à bout** | likert_7 |

---

## Barème de scoring

### SWLS (items swls_01 à swls_05)
- Score brut : somme des 5 réponses (5–35)
- 31–35 : très satisfait(e)
- 26–30 : satisfait(e)
- 20–25 : légèrement satisfait(e)
- 15–19 : légèrement insatisfait(e)
- 10–14 : insatisfait(e)
- 5–9 : très insatisfait(e)

### PANAS Positif (items pan_p_01 à pan_p_05)
- Score brut : somme des 5 réponses (5–35)
- Score ≥ 25 : affect positif élevé
- Score 15–24 : modéré
- Score < 15 : faible

### PANAS Négatif (items pan_n_01 à pan_n_04)
- Score brut : somme des 4 réponses (4–28)
- Score ≥ 18 : affect négatif élevé (signal d'alerte pour ALFRED)
- Score 10–17 : modéré
- Score < 10 : faible

---

## Script conversationnel ALFRED

### Introduction (ALFRED dit)

> "Avant qu'on travaille ensemble, j'aimerais mieux comprendre comment tu vas en ce moment —
> pas de manière abstraite, mais vraiment : ton niveau d'énergie, ta satisfaction globale,
> ce que tu ressens ces dernières semaines.
>
> Je vais te poser **14 questions courtes**. Tu réponds juste avec un chiffre de **1 à 7**,
> où 1 veut dire 'pas du tout d'accord' ou 'pas du tout ça', et 7 'tout à fait d'accord'
> ou 'tout à fait ça'. Aucune mauvaise réponse — je cherche juste à calibrer mes réponses
> à ce que tu vis réellement.
>
> Ça prend environ 7 minutes. Prête ?"

---

### Questions formatées pour le dialogue

**swls_01**
> "ALFRED : Première question — dans l'ensemble, est-ce que tu as l'impression que ta vie
> correspond à ce que tu imaginais qu'elle serait, à ton idéal ? Tu peux répondre de 1
> (pas du tout) à 7 (tout à fait)."

**swls_02**
> "ALFRED : Est-ce que tu dirais que les conditions de ta vie en ce moment sont excellentes ?
> De 1 à 7."

**swls_03**
> "ALFRED : Et globalement, tu es satisfaite de ta vie en ce moment ? De 1 à 7."

**swls_04**
> "ALFRED : Est-ce que tu as l'impression d'avoir obtenu les choses importantes que tu
> voulais jusqu'ici dans ta vie — même si tout n'est pas parfait ? De 1 à 7."

**swls_05**
> "ALFRED : Si tu pouvais recommencer ta vie depuis le début, est-ce que tu changerais
> beaucoup de choses ? Réponds en inversant : 1 = je changerais tout, 7 = je ne changerais
> presque rien."

*[Transition entre sections]*
> "ALFRED : Bien. Maintenant je vais te demander comment tu t'es sentie **ces dernières
> semaines** — pas aujourd'hui spécifiquement, mais sur les 2-3 dernières semaines.
> Toujours de 1 à 7."

**pan_p_01**
> "ALFRED : Ces dernières semaines, à quel point tu t'es sentie enthousiaste — pleine
> d'élan, d'envie ? De 1 (pas du tout) à 7 (énormément)."

**pan_p_02**
> "ALFRED : Et active, énergique — physiquement et mentalement ? De 1 à 7."

**pan_p_03**
> "ALFRED : Est-ce que tu t'es sentie inspirée ces dernières semaines — des idées qui
> viennent, une envie de créer ? De 1 à 7."

**pan_p_04**
> "ALFRED : Déterminée — avec une direction claire, une volonté d'avancer ? De 1 à 7."

**pan_p_05**
> "ALFRED : Et attentive, concentrée — capable de te focaliser sur ce que tu faisais ?
> De 1 à 7."

*[Transition vers affects négatifs]*
> "ALFRED : Dernière série — les états un peu moins agréables. Même principe, de 1 à 7
> selon ce que tu as ressenti ces dernières semaines."

**pan_n_01**
> "ALFRED : Ces dernières semaines, tu t'es sentie irritable ou agacée — des choses qui
> t'ont mis les nerfs en pelote ? De 1 à 7."

**pan_n_02**
> "ALFRED : Stressée ou sous pression — avec l'impression d'avoir trop à gérer ? De 1 à 7."

**pan_n_03**
> "ALFRED : Nerveuse ou anxieuse — avec des pensées qui tournent, de l'inquiétude ?
> De 1 à 7."

**pan_n_04**
> "ALFRED : Et épuisée, à bout — vraiment vidée ? De 1 à 7."

---

### Conclusion / Résumé oral (ALFRED dit selon résultats)

**Si SWLS ≥ 26 et PANAS négatif ≤ 12 :**
> "Merci. Ce que tu me dis me donne une image assez positive : tu es dans une période
> globalement satisfaisante, avec de l'énergie et peu de charge négative. Je vais garder
> ça comme baseline — et si quelque chose change, dis-le moi."

**Si SWLS 15–25 ou PANAS négatif 13–20 :**
> "Merci d'avoir joué le jeu. J'entends que c'est une période avec des hauts et des bas —
> c'est normal, surtout avec tout ce que tu portes en ce moment. Je vais en tenir compte
> pour calibrer mes propositions et mon ton."

**Si SWLS ≤ 14 ou PANAS négatif ≥ 21 :**
> "Merci de m'avoir dit ça franchement. Ce que tu me décris, c'est une période difficile —
> et c'est important que je le sache. Je ne vais pas en rajouter. Si tu veux qu'on en
> parle, on peut. Sinon, on avance doucement, à ton rythme."

**Message de clôture universel :**
> "Ces données restent ici, elles ne sortent pas. Je les utilise juste pour mieux t'accompagner.
> Tu peux refaire ce questionnaire quand tu veux — je garderai un historique pour suivre
> l'évolution dans le temps."
