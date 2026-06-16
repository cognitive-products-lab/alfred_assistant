# Q02 — Style cognitif et préférences de traitement de l'information

**ID** : `q02_style_cognitif`
**Durée estimée** : 8–10 minutes
**Format des réponses** : Échelle de 1 à 7 (Likert 7 points) + 2 choix binaires
**Nombre d'items** : 16
**Scoring** : 4 dimensions (analytique / intuitif / verbal / visuel-spatial)
**Seuil partiel** : 8 réponses pour un profil cognitif indicatif

---

## Objectif

Identifier le style de traitement cognitif dominant : analytique/séquentiel vs intuitif/global,
verbal vs visuel-spatial. Ces données permettent à ALFRED d'adapter la structure de ses
réponses (listes vs prose, détails vs synthèse, exemples concrets vs abstraits).

---

## Cadre théorique

- Basé sur les modèles de styles cognitifs (Riding & Cheema, 1991 ; Kirton, 1994)
- Dimensions : Analytique–Global / Verbal–Imagery (Verbal-Imager Cognitive Style)
- Questionnaire maison calibré pour ALFRED — pas de validation psychométrique externe
- Complète les données AssessFirst (BRAIN) déjà disponibles dans `user_profile.json`

---

## Items

### Dimension A — Analytique vs Intuitif/Global

| ID | Texte | Type |
|----|-------|------|
| cog_a_01 | Quand j'aborde un problème complexe, je préfère le découper en étapes claires avant d'agir | likert_7 |
| cog_a_02 | Je me sens à l'aise pour travailler avec des règles précises et des procédures définies | likert_7 |
| cog_a_03 | J'ai tendance à vérifier chaque étape d'un raisonnement avant d'en tirer une conclusion | likert_7 |
| cog_a_04 | Je préfère comprendre les détails d'un sujet avant d'en saisir la vue d'ensemble | likert_7 |
| cog_i_01 | Je perçois souvent des solutions ou des connexions entre idées sans pouvoir expliquer immédiatement pourquoi | likert_7 |
| cog_i_02 | Je préfère commencer par comprendre la "big picture" d'un sujet, puis aller dans les détails si besoin | likert_7 |
| cog_i_03 | Je me fie facilement à mon instinct pour prendre des décisions, même sur des sujets complexes | likert_7 |
| cog_i_04 | Je trouve plus facile d'apprendre par l'expérience directe que par l'étude de théories | likert_7 |

### Dimension B — Verbal vs Visuel-spatial

| ID | Texte | Type |
|----|-------|------|
| cog_v_01 | Pour mémoriser quelque chose, je préfère l'écrire ou l'expliquer à voix haute | likert_7 |
| cog_v_02 | Quand je réfléchis, j'utilise plutôt des mots et des phrases intérieures | likert_7 |
| cog_v_03 | Je comprends mieux un concept quand il m'est expliqué avec des mots, même sans schéma | likert_7 |
| cog_vs_01 | Je retiens mieux les informations quand elles sont présentées sous forme de schéma ou de diagramme | likert_7 |
| cog_vs_02 | Quand j'essaie de me souvenir de quelque chose, je visualise souvent une image mentale | likert_7 |
| cog_vs_03 | Je comprends facilement les cartes, les graphiques et les représentations spatiales | likert_7 |

### Items binaires — préférences de format

| ID | Texte | Type |
|----|-------|------|
| fmt_01 | Pour une explication complexe, tu préfères : (A) une liste numérotée avec étapes / (B) un texte continu bien rédigé | choix_binaire |
| fmt_02 | Pour mémoriser un concept nouveau : (A) le lire/entendre plusieurs fois formulé de façons différentes / (B) voir un schéma ou une représentation visuelle | choix_binaire |

---

## Barème de scoring

### Analytique (cog_a_01 à cog_a_04)
- Score A : moyenne des 4 items (1.0–7.0)

### Intuitif (cog_i_01 à cog_i_04)
- Score I : moyenne des 4 items (1.0–7.0)

### Profil A–I
- A – I > 1.5 : profil analytique dominant
- I – A > 1.5 : profil intuitif dominant
- |A – I| ≤ 1.5 : profil mixte

### Verbal (cog_v_01 à cog_v_03)
- Score V : moyenne des 3 items (1.0–7.0)

### Visuel-spatial (cog_vs_01 à cog_vs_03)
- Score VS : moyenne des 3 items (1.0–7.0)

### Profil V–VS
- V – VS > 1.0 : préférence verbale
- VS – V > 1.0 : préférence visuelle-spatiale
- |V – VS| ≤ 1.0 : profil mixte

---

## Adaptation ALFRED selon profil

| Profil cognitif | Adaptation ALFRED |
|----------------|------------------|
| Analytique + Verbal | Listes numérotées, étapes séquentielles, explications textuelles |
| Analytique + Visuel | Tableaux, schémas ASCII, structures hiérarchiques |
| Intuitif + Verbal | Synthèses d'abord, métaphores, narration |
| Intuitif + Visuel | Cartes mentales, analogies visuelles, vue d'ensemble |

---

## Script conversationnel ALFRED

### Introduction (ALFRED dit)

> "Je voudrais mieux comprendre comment tu traites l'information — ce qui te convient
> le mieux pour apprendre, réfléchir, résoudre des problèmes.
>
> Il y a **16 questions** en tout. Les 14 premières se répondent de **1 à 7**
> (1 = pas du tout moi, 7 = tout à fait moi), et les 2 dernières par un choix
> entre deux options — je te dirai A ou B.
>
> Il n'y a pas de profil "meilleur" qu'un autre — je cherche juste à calibrer
> ma façon de te présenter les choses. Environ 8 minutes."

---

### Questions formatées pour le dialogue

**cog_a_01**
> "ALFRED : Quand tu as un problème complexe à résoudre, est-ce que tu préfères
> naturellement le découper en étapes avant d'agir ? De 1 (non, j'y vais à l'intuition)
> à 7 (oui, j'ai besoin de structurer d'abord)."

**cog_a_02**
> "ALFRED : Est-ce que tu te sens à l'aise quand il y a des règles précises et des
> procédures claires à suivre ? De 1 à 7."

**cog_a_03**
> "ALFRED : Quand tu raisonnes, tu as tendance à vérifier chaque étape avant de
> conclure — ou tu vas assez directement à la conclusion ? De 1 (je conclus vite)
> à 7 (je vérifie chaque étape)."

**cog_a_04**
> "ALFRED : Est-ce que tu préfères comprendre les détails avant de voir la vue
> d'ensemble, ou c'est plutôt l'inverse ? De 1 (vue d'ensemble d'abord)
> à 7 (détails d'abord)."

*[Transition]*
> "ALFRED : Maintenant, quelques questions sur l'intuition et l'approche globale."

**cog_i_01**
> "ALFRED : Est-ce qu'il t'arrive souvent de percevoir des solutions ou des connexions
> entre idées sans pouvoir l'expliquer clairement sur le moment ? De 1 à 7."

**cog_i_02**
> "ALFRED : Tu préfères comprendre la 'big picture' d'un sujet avant d'aller dans les
> détails ? De 1 (non, je préfère les détails d'abord) à 7 (oui, vue d'ensemble
> avant tout)."

**cog_i_03**
> "ALFRED : Est-ce que tu te fies facilement à ton instinct pour prendre des
> décisions, même sur des sujets complexes ? De 1 à 7."

**cog_i_04**
> "ALFRED : Est-ce que tu apprends mieux en faisant les choses directement qu'en
> étudiant des théories ? De 1 à 7."

*[Transition]*
> "ALFRED : Dernière série — comment tu mémorises et traites visuellement
> vs verbalement les infos."

**cog_v_01**
> "ALFRED : Pour mémoriser quelque chose, tu préfères l'écrire ou l'expliquer à
> voix haute plutôt que de faire un dessin ou un schéma ? De 1 à 7."

**cog_v_02**
> "ALFRED : Quand tu réfléchis, tu utilises plutôt des mots et des phrases
> dans ta tête ? De 1 à 7."

**cog_v_03**
> "ALFRED : Tu comprends mieux un concept quand il t'est expliqué en mots,
> même sans schéma ? De 1 à 7."

**cog_vs_01**
> "ALFRED : Est-ce que tu retiens mieux les infos quand elles sont sous forme
> de schéma ou de diagramme ? De 1 à 7."

**cog_vs_02**
> "ALFRED : Quand tu essaies de te souvenir de quelque chose, tu visualises
> souvent une image mentale ? De 1 à 7."

**cog_vs_03**
> "ALFRED : Tu comprends facilement les cartes, graphiques et représentations
> spatiales ? De 1 à 7."

*[Items binaires]*

**fmt_01**
> "ALFRED : Question de format — pour une explication complexe, tu préfères
> quoi : **(A)** une liste numérotée avec des étapes bien séparées, ou
> **(B)** un texte continu bien rédigé ? Réponds A ou B."

**fmt_02**
> "ALFRED : Et pour mémoriser un concept nouveau : **(A)** le lire ou l'entendre
> plusieurs fois formulé de façons différentes, ou **(B)** voir un schéma ou une
> représentation visuelle ? A ou B."

---

### Conclusion / Résumé oral (ALFRED dit selon résultats)

**Profil Analytique-Verbal :**
> "Bon, voilà ce que je retiens : tu fonctionnes de manière très structurée — tu aimes
> décomposer, vérifier, procéder par étapes, et le texte te convient mieux que le schéma.
> Je vais donc te présenter les choses avec des listes claires, des étapes numérotées,
> et du texte structuré. Pas de carte mentale abstraite, pas de big picture floue."

**Profil Intuitif-Visuel :**
> "Ce que je retiens : tu as un fonctionnement plutôt global et intuitif, et le visuel
> t'aide à retenir. Je vais donc te donner la vue d'ensemble en premier, avec des
> schémas quand c'est possible, et je t'épargnerai les détails dont tu n'as pas besoin."

**Profil mixte :**
> "Tu as un profil assez équilibré — pas de dominante très marquée. Je vais proposer
> les deux : une structure claire ET une vue d'ensemble, et on verra ce qui te parle
> le mieux au fil du temps."

**Message de clôture :**
> "Ces infos vont directement influencer comment je te présente les choses. Si à un
> moment tu veux que je change de format — plus de listes, moins de texte, un schéma —
> dis-le moi simplement."
