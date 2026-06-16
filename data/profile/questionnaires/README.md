# Guide d'utilisation des questionnaires psychologiques ALFRED

## Vue d'ensemble

Ce dossier contient les **8 questionnaires psychologiques** qui constituent le système de profilage personnel ALFRED. Ces outils permettent à ALFRED d'adapter son comportement, son ton et ses recommandations à votre profil psychologique unique.

---

## Avertissement éthique important

> **Ces questionnaires sont conçus à des fins d'usage personnel uniquement.**
>
> - Ils **ne constituent pas un diagnostic clinique ou médical**.
> - Ils **ne remplacent pas** l'avis d'un psychologue, d'un psychiatre ou d'un professionnel de santé mentale.
> - En cas de détresse psychologique importante, de symptômes de dépression, d'anxiété sévère ou de pensées suicidaires, consultez un professionnel de santé mentale.
> - Les résultats sont des **indicateurs de tendance**, non des vérités absolues sur votre personnalité.

---

## Liste des questionnaires

| # | Fichier | Mesure | Durée estimée | Fréquence |
|---|---------|--------|---------------|-----------|
| 1 | `01_big_five_TIPI.md` | Personnalité Big Five (TIPI) | ~5 min | Annuelle |
| 2 | `02_intelligence_emotionnelle.md` | Intelligence émotionnelle (TEIQue-SF adapté) | ~10 min | Semestrielle |
| 3 | `03_valeurs_schwartz.md` | Valeurs fondamentales (PVQ-21) | ~12 min | Annuelle |
| 4 | `04_chronotype_energie.md` | Chronotype et énergie (rMEQ + original) | ~10 min | Trimestrielle |
| 5 | `05_resilience_stress.md` | Résilience + stress perçu (CD-RISC-10 + PSS-4) | ~7 min | Mensuelle |
| 6 | `06_riasec_interets_pro.md` | Intérêts professionnels RIASEC | ~10 min | Annuelle |
| 7 | `07_engagement_burnout.md` | Engagement et burnout (UWES-9 + items originaux) | ~8 min | Mensuelle |
| 8 | `08_communication_conflit.md` | Communication et gestion des conflits (TKI-inspiré) | ~15 min | Semestrielle |

**Durée totale pour la première passation complète : environ 1h15**

---

## Ordre de passation recommandé

### Première passation (session initiale)

Répartissez la passation en **3 sessions** pour éviter la fatigue :

**Session 1 — Fondations (25 min)**
1. `01_big_five_TIPI.md` — Base de la personnalité (rapide)
2. `03_valeurs_schwartz.md` — Valeurs fondamentales
3. `04_chronotype_energie.md` — Énergie et rythme

**Session 2 — Dynamiques professionnelles (23 min)**
4. `06_riasec_interets_pro.md` — Intérêts professionnels
5. `07_engagement_burnout.md` — Santé au travail (important)

**Session 3 — Relations et régulation (32 min)**
6. `02_intelligence_emotionnelle.md` — IE
7. `05_resilience_stress.md` — Résilience et stress
8. `08_communication_conflit.md` — Communication

### Re-passations périodiques

Ordre de priorité selon la fréquence recommandée :
1. **Mensuelle** : résilience/stress (`05`) et engagement/burnout (`07`) — à faire en premier
2. **Trimestrielle** : chronotype (`04`)
3. **Semestrielle** : IE (`02`) et communication (`08`)
4. **Annuelle** : Big Five (`01`), valeurs (`03`), RIASEC (`06`)

---

## Comment remplir les questionnaires

### Étape 1 : Choisir le bon moment

- Remplissez dans un moment **calme et sans interruption**.
- Ne remplissez pas immédiatement après un événement émotionnel fort (conflit, excellente nouvelle) — attendez 30 minutes.
- Les questionnaires mensuels (stress, engagement) doivent refléter les **4 dernières semaines**, pas uniquement aujourd'hui.

### Étape 2 : Répondre honnêtement

- Il n'y a pas de "bonnes" ou "mauvaises" réponses.
- Répondez selon **ce que vous êtes réellement**, pas ce que vous aimeriez être.
- La première réponse intuitive est généralement la plus précise — n'analysez pas trop.
- Évitez la tendance à répondre "moyen" à tout (biais d'acquiescement central).

### Étape 3 : Enregistrer vos réponses

Après avoir répondu à chaque questionnaire :

1. Ouvrez le fichier `data/profile/scoring/answers_template.json`
2. Trouvez la section correspondant au questionnaire (ex : `"big_five_TIPI"`)
3. Renseignez chaque réponse dans le champ correspondant (`"q1": 5`, `"q2": 3`, etc.)
4. Mettez à jour `"completed": true` et `"date": "YYYY-MM-DD"`

**Exemple :**
```json
"big_five_TIPI": {
  "completed": true,
  "date": "2026-06-16",
  "answers": {
    "q1": 6,
    "q2": 3,
    "q3": 4,
    "q4": 2,
    "q5": 5,
    "q6": 4,
    "q7": 6,
    "q8": 3,
    "q9": 5,
    "q10": 2
  }
}
```

---

## Lancer le calcul des scores

Une fois vos réponses saisies dans `answers_template.json`, lancez le module Python :

```bash
python src/core/profile_analyzer.py
```

Ce module va :
1. Calculer tous vos scores normalisés (0-100)
2. Générer vos paramètres comportementaux ALFRED
3. Fusionner avec votre profil AssessFirst
4. Mettre à jour `data/profile/user_profile.json`
5. Chiffrer vos réponses brutes (Fernet AES-128)

---

## Comment interpréter vos résultats

Après exécution du module, vos résultats apparaissent dans `data/profile/user_profile.json` sous la section `psychological_profile`. Les scores sont exprimés sur **0-100** :

- **0-33** : Score faible / dimension peu présente
- **34-66** : Score moyen / dimension modérément présente
- **67-100** : Score élevé / dimension fortement présente

Consultez `docs/profil_systeme/guide_utilisateur.md` pour une interprétation détaillée.

---

## Sécurité des données

- Vos **réponses brutes** sont chiffrées automatiquement (AES-128 Fernet) — seul vous pouvez les lire.
- Vos **scores agrégés** (niveaux, pas les réponses individuelles) sont stockés en clair dans `user_profile.json`.
- Rien n'est transmis sur Internet — tout reste en local sur votre machine.
- Ne committez jamais `answers_template.json` rempli ni les fichiers de clé de chiffrement.

Pour plus de détails, consultez `docs/profil_systeme/securite_donnees.md`.

---

## Système de scoring

Le fichier `data/profile/scoring/scoring_keys.json` contient les clés de scoring pour chaque questionnaire :
- Items directs vs inversés
- Méthode de calcul (moyenne / somme)
- Normalisation sur 0-100

Ce fichier est utilisé automatiquement par `profile_analyzer.py` — vous n'avez pas besoin de l'utiliser directement.

---

## Questions fréquentes

**Q : Dois-je remplir tous les questionnaires d'un coup ?**
Non. Commencez par les questionnaires les plus prioritaires (résilience/stress et engagement, marqués "mensuelle"). Les autres peuvent attendre.

**Q : Que faire si je n'arrive pas à choisir entre deux réponses ?**
Choisissez la première réponse qui vous est venue. En cas de doute persistant, optez pour la légèrement plus haute. Ne restez pas bloqué plus de 30 secondes sur un item.

**Q : Mes réponses peuvent-elles changer avec le temps ?**
Oui, c'est précisément pourquoi ce système prévoit des re-passations périodiques. Certains traits (Big Five) changent peu, d'autres (stress, engagement) peuvent varier significativement en quelques semaines.

**Q : ALFRED va-t-il utiliser ces données pour me manipuler ?**
Non. Ces données servent uniquement à adapter le style de communication et les recommandations d'ALFRED à ce qui vous convient le mieux. ALFRED ne prend jamais de décision à votre place.

**Q : Et si mes scores AssessFirst contredisent les résultats du TIPI ?**
C'est normal et attendu — le TIPI est une mesure rapide (10 items vs le SWIPE complet d'AssessFirst). En cas de discordance, la source AssessFirst est prioritaire. Le TIPI sert de vérification de cohérence.
