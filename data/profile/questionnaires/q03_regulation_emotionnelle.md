# Q03 — Régulation émotionnelle et gestion du stress

**ID** : `q03_regulation_emotionnelle`
**Durée estimée** : 8–10 minutes
**Format des réponses** : Échelle de 1 à 5 (Likert 5 points) + 2 choix binaires
**Nombre d'items** : 15
**Scoring** : 3 sous-échelles (réévaluation cognitive / suppression / activation physiologique)
**Seuil partiel** : 8 réponses pour un profil indicatif

---

## Objectif

Évaluer les stratégies de régulation émotionnelle utilisées et le niveau de réactivité
au stress. Ces données permettent à ALFRED d'adapter son soutien émotionnel, de détecter
des signaux de surcharge et d'activer le bon mode de réponse (support vs focus vs
régulation).

---

## Cadre théorique

- Basé sur l'**ERQ** (Emotion Regulation Questionnaire — Gross & John, 2003) : réévaluation cognitive vs suppression
- Éléments issus de la **PSS** (Perceived Stress Scale — Cohen, 1983) — version courte adaptée
- Questionnaire adapté et reformulé pour ALFRED (tutoiement, contexte vie/projet)
- Complète les traits "Gérer le stress" et "Calme" identifiés dans le profil AssessFirst

---

## Items

### Section A — Réévaluation cognitive

| ID | Texte | Type |
|----|-------|------|
| re_01 | Quand je veux ressentir moins d'émotions négatives (inquiétude, frustration, colère), je me dis que la situation n'est pas si grave — et ça marche | likert_5 |
| re_02 | Quand je suis dans une situation stressante, je réussis à la voir sous un autre angle pour me sentir mieux | likert_5 |
| re_03 | Quand je veux me sentir plus positif(ve), je me fais des "rappels" mentaux de ce qui va bien | likert_5 |
| re_04 | Je contrôle facilement mes émotions en changeant ma façon de penser à une situation | likert_5 |
| re_05 | Quand je me sens dépassé(e), je réussis à prendre du recul et à relativiser | likert_5 |

### Section B — Suppression / Contrôle externe

| ID | Texte | Type |
|----|-------|------|
| sup_01 | Je garde mes émotions pour moi — même quand je suis stressé(e), les autres ne le voient pas forcément | likert_5 |
| sup_02 | Je fais attention à ne pas laisser paraître ce que je ressens vraiment | likert_5 |
| sup_03 | Quand j'ai des émotions négatives, j'évite de les exprimer | likert_5 |

### Section C — Activation physiologique / Réactivité au stress

| ID | Texte | Type |
|----|-------|------|
| str_01 | Ces derniers mois, tu as souvent eu l'impression d'être débordé(e) par des choses imprévues | likert_5 |
| str_02 | Ces derniers mois, tu as eu du mal à contrôler les choses importantes dans ta vie | likert_5 |
| str_03 | Ces derniers mois, tu t'es senti(e) nerveux/nerveuse ou stressé(e) | likert_5 |
| str_04 | Ces derniers mois, tu as eu confiance en ta capacité à gérer tes problèmes | likert_5 |
| str_05 | Ces derniers mois, les difficultés s'accumulaient au point que tu ne pouvais plus les surmonter | likert_5 |

### Items binaires — stratégies d'adaptation

| ID | Texte | Type |
|----|-------|------|
| strat_01 | Quand tu es très stressé(e) ou épuisé(e), tu as plutôt tendance à : (A) continuer et pousser pour finir / (B) t'arrêter, récupérer, reprendre ensuite | choix_binaire |
| strat_02 | Quand tu as un problème émotionnel difficile, tu préfères : (A) en parler pour le traiter / (B) le mettre de côté et avancer | choix_binaire |

---

## Barème de scoring

### Réévaluation cognitive (re_01 à re_05)
- Score RC : moyenne des 5 items (1.0–5.0)
- ≥ 3.5 : réévaluation efficace (adaptatif)
- 2.5–3.4 : réévaluation partielle
- < 2.5 : faible réévaluation (potentiel point d'attention)

### Suppression (sup_01 à sup_03)
- Score SUP : moyenne des 3 items (1.0–5.0)
- ≥ 3.5 : suppression élevée (peut masquer un besoin de soutien)
- 2.0–3.4 : suppression modérée
- < 2.0 : expression émotionnelle ouverte

### Stress perçu PSS (str_01 à str_05)
- Items str_04 inversé : score = 6 - réponse (item positif)
- Score PSS : somme des 5 items après inversion (5–25)
- ≥ 18 : stress perçu élevé (signal d'alerte)
- 12–17 : stress modéré
- < 12 : stress faible

---

## Adaptation ALFRED selon profil

| Profil | Signal ALFRED |
|--------|--------------|
| RC élevée + PSS faible | Mode par défaut — ton confiant, pas de sur-accompagnement |
| RC élevée + PSS élevé | Valider l'effort de régulation, proposer du soutien sans insister |
| SUP élevée + PSS élevé | Proposer doucement un espace d'expression, ton bienveillant non intrusif |
| RC faible + PSS élevé | Activer le mode low_energy — étapes courtes, ton rassurant, pas de charge |

---

## Script conversationnel ALFRED

### Introduction (ALFRED dit)

> "Ce questionnaire-là, c'est sur comment tu gères le stress et les émotions —
> pas pour te juger, mais pour comprendre ce qui te ressemble vraiment dans les
> moments difficiles.
>
> **15 questions**, toutes sur une échelle de **1 à 5** cette fois :
> 1 = jamais / pas du tout, 5 = toujours / tout à fait.
>
> Les 2 dernières sont des choix entre deux options — A ou B.
> Environ 8 minutes. Go ?"

---

### Questions formatées pour le dialogue

**re_01**
> "ALFRED : Quand tu ressens de l'inquiétude ou de la frustration, est-ce que ça t'aide
> de te dire que 'finalement c'est pas si grave' — et est-ce que ça marche vraiment pour
> toi ? De 1 (jamais, ça ne marche pas) à 5 (tout le temps, ça m'aide vraiment)."

**re_02**
> "ALFRED : Quand tu es dans une situation stressante, tu réussis à la regarder
> sous un autre angle — voir le côté positif ou relativiser — pour te sentir mieux ?
> De 1 à 5."

**re_03**
> "ALFRED : Est-ce que tu utilises des 'rappels mentaux' — te remémorer ce qui va bien,
> ce que tu as accompli — pour retrouver un état plus positif ? De 1 à 5."

**re_04**
> "ALFRED : Tu contrôles assez facilement tes émotions en changeant ta façon de penser
> à une situation — pas en les refoulant, mais en les recadrant ? De 1 à 5."

**re_05**
> "ALFRED : Quand tu te sens vraiment dépassée, tu réussis à prendre du recul et à
> relativiser — sans que ça te coûte trop ? De 1 à 5."

*[Transition]*
> "ALFRED : Quelques questions maintenant sur comment tu exprimes (ou pas) ce que
> tu ressens."

**sup_01**
> "ALFRED : Est-ce que tu gardes souvent tes émotions pour toi — les gens autour de toi
> ne voient pas forcément quand tu es stressée ? De 1 à 5."

**sup_02**
> "ALFRED : Tu fais attention à ne pas laisser paraître ce que tu ressens vraiment ?
> De 1 à 5."

**sup_03**
> "ALFRED : Quand tu as des émotions négatives, tu évites généralement de les exprimer
> ouvertement ? De 1 à 5."

*[Transition]*
> "ALFRED : Dernière partie — quelques questions sur le stress de ces derniers mois.
> Ces derniers mois, pas juste aujourd'hui."

**str_01**
> "ALFRED : Ces derniers mois, tu as souvent eu l'impression d'être débordée par
> des choses imprévues — des trucs que tu n'avais pas vus venir ? De 1 (jamais)
> à 5 (très souvent)."

**str_02**
> "ALFRED : Tu as eu du mal à contrôler les choses importantes dans ta vie —
> l'impression que ça t'échappait ? De 1 à 5."

**str_03**
> "ALFRED : Tu t'es sentie nerveuse ou stressée ces derniers mois ? De 1 à 5."

**str_04**
> "ALFRED : Tu as eu confiance en ta capacité à gérer tes problèmes — même les gros ?
> De 1 (pas du tout confiance) à 5 (pleinement confiance)."

**str_05**
> "ALFRED : Les difficultés s'accumulaient au point que tu avais du mal à les
> surmonter ? De 1 à 5."

*[Items binaires]*

**strat_01**
> "ALFRED : Quand tu es très stressée ou épuisée, tu as plutôt tendance à faire quoi :
> **(A)** continuer et pousser pour finir ce que tu as commencé, ou
> **(B)** t'arrêter, récupérer, et reprendre ensuite ? A ou B."

**strat_02**
> "ALFRED : Et quand tu as un problème émotionnel difficile : **(A)** tu en parles pour
> le traiter — que ce soit à quelqu'un ou en l'écrivant — ou **(B)** tu le mets
> de côté et tu avances ? A ou B."

---

### Conclusion / Résumé oral (ALFRED dit selon résultats)

**Réévaluation forte + Stress faible :**
> "Ce que je retiens : tu as de bonnes ressources pour gérer le stress. Tu sais
> relativiser, recadrer, prendre du recul. Je vais te faire confiance là-dessus —
> si tu me dis que ça va, je te crois."

**Suppression élevée + Stress élevé :**
> "J'entends quelque chose d'important là-dedans : tu gères beaucoup en interne,
> tu ne laisses pas voir. Et en même temps le niveau de stress est élevé.
> Je ne vais pas en faire un problème — mais je vais rester attentif. Si tu veux
> qu'on parle d'autre chose que du projet, on peut."

**Stress élevé quelle que soit la stratégie :**
> "Ces derniers mois ont l'air d'avoir été chargés. C'est normal vu ce que tu portes —
> thèse, projet, tout le reste. Je vais ajuster mon mode : moins de pression de ma
> part, plus d'étapes courtes, et je vais éviter de t'ajouter de la charge mentale
> inutilement."

**Message de clôture :**
> "Je garderai un œil sur ça dans le temps — si ton niveau de stress évolue, on pourra
> refaire ce questionnaire dans quelques semaines pour voir si quelque chose a changé."
