# Questionnaire — Profil fondatrice (complément)

**ID** : `q00_profil_complementaire`
**Durée estimée** : 10–15 minutes
**Format des réponses** : Texte libre — une phrase suffit par question
**Nombre d'items** : 23
**Type** : Qualitatif (pas de scoring numérique — intégration directe au profil)
**Seuil partiel** : N/A — chaque réponse est utile indépendamment

Ce questionnaire complète `data/profile/user_profile.json` (rempli avec les
résultats AssessFirst) sur des points que le test ne couvre pas : énergie au
quotidien, accessibilité, limites, style de communication et préférences
d'interaction avec ALFRED.

Les questions sont posées par ALFRED une à une dans la conversation. Les
réponses sont sauvegardées au fur et à mesure et peuvent être complétées
en plusieurs sessions.

Les réponses sont intégrées dans `data/users/instances/user_celine_instance.json`
et `data/profile/user_profile.json`.

---

## 1. Énergie & attention

- Quels moments de la journée es-tu la plus concentrée / la plus productive ?
- Combien de temps tiens-tu en moyenne sur une tâche complexe avant d'avoir
  besoin d'une pause ?
- À quoi ressemble une "surcharge" pour toi (signes de fatigue, de saturation) ?
- Qu'est-ce qui t'aide à récupérer (pause courte, changement d'activité,
  silence, mouvement...) ?
- Préfères-tu un rythme de travail soutenu et continu, ou des cycles
  courts avec des pauses fréquentes ?

## 2. Accessibilité

- As-tu des préférences visuelles (taille de texte, contraste, thème
  sombre/clair, sensibilité à certaines couleurs) ?
- As-tu des préférences audio (vitesse de la voix, ton, sensibilité à
  certains sons) ?
- Préfères-tu interagir par la voix, par l'écrit, ou les deux selon le
  contexte ?
- As-tu besoin de sous-titres ou de transcriptions systématiques ?
- Souhaites-tu des notifications, et à quelle fréquence (immédiate, groupée,
  désactivée par défaut) ?

## 3. Limites & sujets sensibles

- Y a-t-il des sujets que tu préfères qu'ALFRED n'aborde jamais de
  lui-même ?
- Y a-t-il des sujets sensibles sur lesquels ALFRED doit faire preuve de
  prudence particulière ?
- Y a-t-il des tons ou façons de répondre à éviter absolument (en dehors de
  ceux déjà listés : vague, froid, surprotecteur...) ?
- Y a-t-il des actions qu'ALFRED ne doit jamais faire sans confirmation
  explicite ?

## 4. Style de communication détaillé

- Préfères-tu des réponses directes (conclusion d'abord) ou progressives
  (raisonnement puis conclusion) ?
- Préfères-tu systématiquement des étapes numérotées, ou seulement pour les
  sujets complexes ?
- As-tu besoin d'exemples concrets même pour des sujets simples ?
- Préfères-tu un résumé en fin de réponse longue, ou cela alourdit-il
  inutilement ?
- Le niveau d'humour actuel (`humor: true`) te convient-il toujours ?

## 5. Contexte de vie quotidien

- À quoi ressemble une journée type actuellement (travail/thèse/projet
  ALFRED/vie perso) ?
- Quels sont tes objectifs prioritaires sur les 3 prochains mois ?
- Y a-t-il des contraintes récurrentes (santé, emploi du temps, charge
  mentale) dont ALFRED devrait tenir compte dans ses propositions ?

## 6. Préférences d'interaction avec ALFRED

- Quel mode par défaut souhaites-tu (`companion_mode` actuel convient-il
  toujours, ou préfères-tu un autre mode selon les moments) ?
- Souhaites-tu qu'ALFRED soit proactif (proposer spontanément des actions)
  ou qu'il attende toujours une demande explicite ?
- À quelle fréquence souhaites-tu qu'ALFRED te fasse un point d'avancement
  sur les projets en cours ?

---

## IDs des items (pour answers_template.json)

| Section | ID question | Description courte |
|---------|------------|-------------------|
| Énergie | energie_01 | Moments de pic de concentration |
| Énergie | energie_02 | Durée de tenue sur une tâche |
| Énergie | energie_03 | Signes de surcharge |
| Énergie | energie_04 | Stratégies de récupération |
| Énergie | energie_05 | Rythme de travail préféré |
| Accessibilité | access_01 | Préférences visuelles |
| Accessibilité | access_02 | Préférences audio |
| Accessibilité | access_03 | Mode voix/écrit |
| Accessibilité | access_04 | Besoin de sous-titres |
| Accessibilité | access_05 | Fréquence notifications |
| Limites | limites_01 | Sujets interdits proactifs |
| Limites | limites_02 | Sujets sensibles |
| Limites | limites_03 | Tons à éviter |
| Limites | limites_04 | Actions à confirmer |
| Communication | comm_01 | Style direct vs progressif |
| Communication | comm_02 | Étapes numérotées systématiques |
| Communication | comm_03 | Besoin d'exemples |
| Communication | comm_04 | Résumé en fin de réponse |
| Communication | comm_05 | Niveau d'humour |
| Contexte | contexte_01 | Journée type |
| Contexte | contexte_02 | Objectifs 3 mois |
| Contexte | contexte_03 | Contraintes récurrentes |
| Interaction | interaction_01 | Mode ALFRED par défaut |
| Interaction | interaction_02 | Proactivité souhaitée |
| Interaction | interaction_03 | Fréquence points d'avancement |

---

## Script conversationnel ALFRED

### Introduction (ALFRED dit)

> "Ce questionnaire, c'est le plus personnel des quatre — il porte sur toi
> concrètement : comment tu fonctionnes au quotidien, ce qui t'aide, ce qui te
> nuit, et comment tu veux qu'on travaille ensemble.
>
> Il y a **23 questions**, toutes ouvertes — pas de chiffre, juste tes mots.
> Une phrase suffit par question. Je les pose une à une.
>
> Tu peux t'arrêter à n'importe quel moment et reprendre plus tard —
> je garde tout. Environ 10 à 15 minutes si tu fais tout d'un bloc.
> On commence ?"

---

### Questions formatées pour le dialogue

**Section Énergie & Attention**

> "ALFRED : Première question — quels moments de la journée tu es la plus concentrée,
> la plus productive ? Matin, après-midi, soir ? Ou ça dépend ?"

> "ALFRED : Et combien de temps tu tiens en moyenne sur une tâche complexe avant
> d'avoir vraiment besoin d'une pause ?"

> "ALFRED : À quoi ressemble une 'surcharge' pour toi — les signes que tu as atteint
> ta limite ? Physique, mental, émotionnel ?"

> "ALFRED : Qu'est-ce qui t'aide à récupérer — une pause courte, changer d'activité,
> du silence, bouger, autre chose ?"

> "ALFRED : Tu préfères un rythme de travail soutenu et continu, ou des cycles courts
> avec des pauses fréquentes ?"

**Section Accessibilité**

> "ALFRED : Est-ce que tu as des préférences visuelles — taille de texte, contraste
> élevé, thème sombre ou clair, sensibilité à certaines couleurs ?"

> "ALFRED : Et des préférences audio — vitesse de ma voix, ton, sensibilité à certains
> sons aigus ou forts ?"

> "ALFRED : Tu préfères interagir avec moi par la voix, par l'écrit, ou les deux
> selon le contexte ?"

> "ALFRED : Est-ce que tu as besoin de sous-titres ou de transcriptions systématiques
> quand je parle ?"

> "ALFRED : Tu veux que je t'envoie des notifications, et à quelle fréquence —
> immédiatement quand c'est pertinent, groupées, ou désactivées par défaut ?"

**Section Limites & Sujets sensibles**

> "ALFRED : Y a-t-il des sujets que tu préfères que je n'aborde jamais de moi-même —
> sans que tu m'en parles d'abord ?"

> "ALFRED : Y a-t-il des sujets sensibles sur lesquels je dois faire preuve de
> prudence particulière — des zones que tu veux qu'on navigue doucement ?"

> "ALFRED : Y a-t-il des tons ou façons de répondre à éviter absolument — en dehors
> de ce qu'on a déjà dit : vague, froid, surprotecteur ?"

> "ALFRED : Y a-t-il des actions que je ne dois jamais faire sans confirmation
> explicite de ta part ?"

**Section Style de communication détaillé**

> "ALFRED : Tu préfères que je te donne la conclusion d'abord, puis le raisonnement —
> ou l'inverse, le raisonnement qui amène à la conclusion ?"

> "ALFRED : Tu veux des étapes numérotées systématiquement pour tout, ou seulement
> pour les sujets vraiment complexes ?"

> "ALFRED : Tu as besoin d'exemples concrets même pour des sujets simples, ou c'est
> seulement quand c'est abstrait ?"

> "ALFRED : Tu préfères un résumé à la fin des réponses longues, ou ça alourdit
> inutilement ?"

> "ALFRED : Le niveau d'humour actuel te convient — ou tu veux plus, moins,
> ou différent ?"

**Section Contexte de vie quotidien**

> "ALFRED : À quoi ressemble une journée type pour toi en ce moment — entre le travail,
> la thèse, le projet ALFRED et la vie perso ?"

> "ALFRED : Quels sont tes objectifs prioritaires sur les 3 prochains mois ?"

> "ALFRED : Y a-t-il des contraintes récurrentes — santé, emploi du temps, charge
> mentale — dont je devrais tenir compte dans mes propositions et suggestions ?"

**Section Préférences d'interaction**

> "ALFRED : Quel mode par défaut tu veux avec moi ? Le companion_mode actuel te
> convient, ou tu préfères un autre mode — ou plusieurs selon les moments ?"

> "ALFRED : Tu veux que je sois proactif — que je propose spontanément des actions,
> des suggestions, des rappels — ou tu préfères que j'attende toujours que tu
> me demandes quelque chose ?"

> "ALFRED : À quelle fréquence tu veux que je te fasse un point d'avancement
> sur les projets en cours — quotidien, hebdomadaire, à la demande ?"

---

### Conclusion / Résumé oral (ALFRED dit)

> "Merci. Ce que tu viens de me dire, c'est de l'or pour calibrer mon comportement.
>
> Je vais intégrer tout ça dans ton profil adaptatif — les horaires de productivité,
> tes limites, le style de communication, le tout. À partir de maintenant, je vais
> tenir compte de ça dans chaque interaction.
>
> Si quelque chose change — ton rythme, tes besoins, tes limites — dis-le moi
> simplement et je mettrai à jour. Ce profil n'est pas figé."

---

*Une fois complétées, ces réponses sont intégrées dans le profil
adaptatif de Céline (`data/users/instances/user_celine_instance.json`) et
dans `data/profile/user_profile.json`.*
