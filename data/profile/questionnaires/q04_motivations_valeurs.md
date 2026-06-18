# Q04 — Motivations profondes et valeurs (SDT + VIA adapté)

**ID** : `q04_motivations_valeurs`
**Durée estimée** : 9–11 minutes
**Format des réponses** : Échelle de 1 à 7 (Likert 7 points)
**Nombre d'items** : 18
**Scoring** : 3 besoins SDT (autonomie / compétence / appartenance) + 3 valeurs dominantes
**Seuil partiel** : 9 réponses pour un profil motivationnel indicatif

---

## Objectif

Identifier les motivations profondes (besoins psychologiques fondamentaux) et les valeurs
dominantes. Ces données permettent à ALFRED d'aligner ses suggestions sur ce qui compte
vraiment pour l'utilisateur, d'éviter les propositions en contradiction avec ses valeurs,
et d'adapter son niveau de challenge vs soutien.

---

## Cadre théorique

- **SDT** (Self-Determination Theory — Deci & Ryan, 2000) : 3 besoins fondamentaux :
  autonomie, compétence, appartenance
- **VIA** (Values In Action — Peterson & Seligman, 2004) : forces de caractère et valeurs
- Complémentaire au profil AssessFirst DRIVE (motivations) déjà disponible
- Questionnaire adapté pour ALFRED avec reformulation contextuelle

---

## Items

### Section A — Besoin d'autonomie

| ID | Texte | Type |
|----|-------|------|
| sdt_aut_01 | J'ai besoin de choisir moi-même comment je fais les choses — les approches imposées me freinent | likert_7 |
| sdt_aut_02 | Je travaille beaucoup mieux quand je peux organiser mon temps et mes tâches à ma façon | likert_7 |
| sdt_aut_03 | Il est important pour moi d'avoir le dernier mot sur mes propres décisions, même si je demande des avis | likert_7 |
| sdt_aut_04 | Je me sens frustré(e) quand quelqu'un me dit précisément quoi faire et comment le faire | likert_7 |
| sdt_aut_05 | Mon sens des valeurs guide mes actions — pas la pression externe ou l'approbation des autres | likert_7 |
| sdt_aut_06 | J'ai besoin de comprendre le "pourquoi" d'une tâche pour m'y impliquer vraiment | likert_7 |

### Section B — Besoin de compétence

| ID | Texte | Type |
|----|-------|------|
| sdt_comp_01 | J'ai besoin de sentir que je progresse, que je m'améliore — la stagnation me pèse | likert_7 |
| sdt_comp_02 | Les défis difficiles me motivent plus que les tâches faciles | likert_7 |
| sdt_comp_03 | J'aime maîtriser les sujets en profondeur — pas juste en surface | likert_7 |
| sdt_comp_04 | Quand j'apprends quelque chose, j'ai besoin de le comprendre vraiment pour me sentir à l'aise | likert_7 |
| sdt_comp_05 | La qualité de ce que je produis compte beaucoup pour moi — les approximations m'insatisfont | likert_7 |
| sdt_comp_06 | Je me sens bien quand je réussis des choses difficiles par mes propres moyens | likert_7 |

### Section C — Besoin d'appartenance et d'impact

| ID | Texte | Type |
|----|-------|------|
| sdt_app_01 | Il est important pour moi que mon travail ait un impact réel sur les autres | likert_7 |
| sdt_app_02 | J'ai besoin de me sentir connectée à quelque chose de plus grand que moi — une mission, une cause | likert_7 |
| sdt_app_03 | Le sentiment d'appartenir à un groupe ou d'être reconnue par mes pairs compte pour moi | likert_7 |
| sdt_app_04 | J'aime partager mes réussites et mes projets — pas pour me vanter, mais pour créer de la connexion | likert_7 |
| sdt_app_05 | Je suis plus motivée quand je travaille pour quelqu'un ou quelque chose en dehors de moi-même | likert_7 |
| sdt_app_06 | La reconnaissance de mon travail par des personnes que je respecte compte beaucoup | likert_7 |

---

## Barème de scoring

### Autonomie (sdt_aut_01 à sdt_aut_06)
- Score AUT : moyenne des 6 items (1.0–7.0)
- ≥ 5.5 : besoin d'autonomie très élevé → ALFRED ne doit jamais imposer, toujours proposer
- 4.0–5.4 : élevé → laisser le choix, expliquer le pourquoi
- < 4.0 : modéré → peut accepter des directives structurées

### Compétence (sdt_comp_01 à sdt_comp_06)
- Score COMP : moyenne des 6 items (1.0–7.0)
- ≥ 5.5 : besoin de maîtrise très élevé → ALFRED doit proposer des challenges, de la profondeur
- 4.0–5.4 : élevé → valoriser la progression, le détail
- < 4.0 : modéré → peut se satisfaire d'une vue d'ensemble

### Appartenance/Impact (sdt_app_01 à sdt_app_06)
- Score APP : moyenne des 6 items (1.0–7.0)
- ≥ 5.5 : besoin d'impact très élevé → lier les tâches à la mission, à l'effet sur les autres
- 4.0–5.4 : élevé → rappeler le sens, le projet global
- < 4.0 : modéré → peut fonctionner sur des objectifs intrinsèques

### Profil motivationnel dominant
- Dimension la plus haute (≥ 0.5 point d'écart) = motivation dominante
- Si toutes proches : profil équilibré

---

## Adaptation ALFRED selon profil

| Profil motivationnel | Adaptation ALFRED |
|---------------------|------------------|
| AUT dominant | Proposer des options, jamais imposer, expliquer le pourquoi |
| COMP dominant | Challenges clairs, feedback sur progression, profondeur |
| APP dominant | Relier aux autres, à la mission, valoriser l'impact |
| Équilibré | Alterner registres selon le contexte |

---

## Script conversationnel ALFRED

### Introduction (ALFRED dit)

> "Ce questionnaire, c'est le plus stratégique des quatre pour moi. Il porte sur
> ce qui te motive vraiment en profondeur — pas ce que tu penses que tu devras
> répondre, mais ce qui te ressemble réellement.
>
> **18 questions**, toutes de **1 à 7**. 1 = pas du tout vrai pour moi,
> 7 = totalement vrai pour moi. Aucune bonne ou mauvaise réponse.
>
> Ces infos vont directement influencer comment je te parle et ce que
> je te propose. Environ 9 minutes."

---

### Questions formatées pour le dialogue

**sdt_aut_01**
> "ALFRED : Première question — est-ce que tu as besoin de choisir toi-même comment
> tu fais les choses ? Les approches imposées, ça te freine ? De 1 (pas vraiment,
> je m'adapte) à 7 (oui, j'ai besoin d'autonomie sur la méthode)."

**sdt_aut_02**
> "ALFRED : Tu travailles nettement mieux quand tu peux organiser ton temps et tes
> tâches à ta propre façon ? De 1 à 7."

**sdt_aut_03**
> "ALFRED : Même quand tu demandes des avis, c'est important pour toi d'avoir le
> dernier mot sur tes propres décisions ? De 1 à 7."

**sdt_aut_04**
> "ALFRED : Quand quelqu'un te dit précisément quoi faire et comment le faire,
> tu te sens frustrée ? De 1 à 7."

**sdt_aut_05**
> "ALFRED : C'est tes propres valeurs qui guident tes actions, pas la pression externe
> ou l'approbation des autres ? De 1 à 7."

**sdt_aut_06**
> "ALFRED : Tu as besoin de comprendre le 'pourquoi' d'une tâche pour vraiment t'y
> impliquer — pas juste exécuter ? De 1 à 7."

*[Transition]*
> "ALFRED : Quelques questions maintenant sur ton rapport à la compétence et à la
> maîtrise."

**sdt_comp_01**
> "ALFRED : Tu as besoin de sentir que tu progresses, que tu t'améliores —
> la stagnation te pèse vraiment ? De 1 à 7."

**sdt_comp_02**
> "ALFRED : Les défis difficiles te motivent plus que les tâches faciles ?
> De 1 à 7."

**sdt_comp_03**
> "ALFRED : Tu aimes maîtriser les sujets en profondeur — pas juste avoir une
> vague idée ? De 1 à 7."

**sdt_comp_04**
> "ALFRED : Quand tu apprends quelque chose, tu as besoin de vraiment comprendre
> pour te sentir à l'aise — pas juste connaître les grandes lignes ? De 1 à 7."

**sdt_comp_05**
> "ALFRED : La qualité de ce que tu produis compte beaucoup pour toi —
> les approximations t'insatisfont ? De 1 à 7."

**sdt_comp_06**
> "ALFRED : Tu te sens particulièrement bien quand tu réussis des choses difficiles
> par toi-même — sans aide extérieure ? De 1 à 7."

*[Transition]*
> "ALFRED : Dernière partie — ton rapport aux autres, à l'impact et au sens."

**sdt_app_01**
> "ALFRED : C'est important pour toi que ton travail ait un impact réel sur
> les autres — pas juste pour toi ? De 1 à 7."

**sdt_app_02**
> "ALFRED : Tu as besoin de te sentir connectée à quelque chose de plus grand —
> une mission, une cause — pour être vraiment engagée ? De 1 à 7."

**sdt_app_03**
> "ALFRED : Le fait d'appartenir à un groupe ou d'être reconnue par tes pairs
> compte pour toi ? De 1 à 7."

**sdt_app_04**
> "ALFRED : Tu aimes partager tes réussites et tes projets — pas pour te vanter,
> mais pour créer de la connexion ? De 1 à 7."

**sdt_app_05**
> "ALFRED : Tu es plus motivée quand tu travailles pour quelqu'un ou quelque chose
> en dehors de toi — pas juste pour toi ? De 1 à 7."

**sdt_app_06**
> "ALFRED : La reconnaissance par des personnes que tu respectes compte vraiment
> pour toi ? De 1 à 7."

---

### Conclusion / Résumé oral (ALFRED dit selon résultats)

**AUT dominant :**
> "Ce que je retiens : tu es profondément autonome. Tu as besoin de comprendre le
> pourquoi, de choisir ta méthode, et tu ne fonctionnes pas bien sous contrainte
> imposée. Je vais donc toujours te proposer des options, jamais te dire 'fais comme
> ça', et t'expliquer le raisonnement derrière mes suggestions."

**COMP dominant :**
> "Tu fonctionnes beaucoup sur le challenge et la maîtrise — tu as besoin de sentir
> que tu progresses, que tu creuses vraiment les sujets. Je vais te proposer de la
> profondeur, du détail, et je vais valoriser chaque progression — même les petites."

**APP dominant :**
> "Le sens et l'impact sont centraux pour toi — pas juste accomplir des choses,
> mais les accomplir pour quelque chose ou quelqu'un. Je vais régulièrement relier
> ce qu'on fait à la mission globale d'ALFRED et à l'impact sur tes utilisateurs
> futurs."

**Message de clôture :**
> "Ces motivations, c'est la fondation de comment je vais te parler. Elles peuvent
> évoluer — si tu sens que quelque chose ne colle plus, dis-le moi."
