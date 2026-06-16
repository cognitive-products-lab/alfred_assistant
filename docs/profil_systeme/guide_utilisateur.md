# Guide utilisateur — Profilage psychologique ALFRED

**Pour** : Céline Rousselot  
**Version** : 1.0  
**Date** : 2026-06-16

---

## Résumé rapide

Ce guide explique comment utiliser le système de profilage psychologique d'ALFRED. En quelques étapes :
1. Remplissez les questionnaires (Markdown dans `data/profile/questionnaires/`)
2. Saisissez vos réponses dans `data/profile/scoring/answers_template.json`
3. Lancez `python src/core/profile_analyzer.py`
4. ALFRED s'adapte automatiquement à votre profil

---

## Table des matières

1. [Comment démarrer](#1-comment-démarrer)
2. [Comment remplir answers_template.json](#2-comment-remplir-answers_templatejson)
3. [Comment lancer profile_analyzer.py](#3-comment-lancer-profile_analyzerpy)
4. [Comment interpréter les résultats](#4-comment-interpréter-les-résultats)
5. [Comment ALFRED utilise ces paramètres](#5-comment-alfred-utilise-ces-paramètres)
6. [Quand refaire les tests — périodicité](#6-quand-refaire-les-tests--périodicité)
7. [Gérer la clé de chiffrement](#7-gérer-la-clé-de-chiffrement)
8. [FAQ](#8-faq)

---

## 1. Comment démarrer

### 1.1 Votre profil AssessFirst est la base

Avant de remplir les questionnaires ALFRED, sachez que **votre profil AssessFirst (SWIPE + DRIVE + BRAIN) constitue la source de vérité prioritaire** pour la personnalité Big Five, vos motivations professionnelles (DRIVE) et votre style cognitif (BRAIN). Les questionnaires ALFRED complètent AssessFirst sur des dimensions qu'il ne couvre pas.

Vos données AssessFirst sont accessibles sur votre profil : https://profil.assessfirst.com

### 1.2 Ordre de passation recommandé pour la première fois

Ne cherchez pas à tout faire en un jour. Voici un plan sur 3 sessions courtes :

**Session 1 — Fondations (~25 minutes, idéalement un matin)**

| Questionnaire | Durée | Priorité |
|---------------|-------|----------|
| `05_resilience_stress.md` | 7 min | PRIORITAIRE (santé) |
| `07_engagement_burnout.md` | 8 min | PRIORITAIRE (santé) |
| `04_chronotype_energie.md` | 10 min | Utile pour l'organisation |

**Session 2 — Personnalité et intérêts (~22 minutes, à votre rythme)**

| Questionnaire | Durée | Note |
|---------------|-------|------|
| `01_big_five_TIPI.md` | 5 min | Complémentaire à AssessFirst SWIPE |
| `03_valeurs_schwartz.md` | 12 min | Différent de DRIVE — valeurs de vie |
| `06_riasec_interets_pro.md` | 10 min | Complémentaire à DRIVE |

**Session 3 — Relations et émotions (~27 minutes)**

| Questionnaire | Durée | Note |
|---------------|-------|------|
| `02_intelligence_emotionnelle.md` | 10 min | Non couvert par AssessFirst |
| `08_communication_conflit.md` | 15 min | Non couvert par AssessFirst |

### 1.3 Durée totale estimée

- Session 1 seule : 25 minutes → paramètres santé et énergie actifs
- Sessions 1+2 : 47 minutes → profil de personnalité et intérêts actifs
- Sessions 1+2+3 : 74 minutes → profil complet

---

## 2. Comment remplir answers_template.json

### 2.1 Trouver le fichier

```
data/profile/scoring/answers_template.json
```

### 2.2 Structure du fichier

```json
{
  "user_id": "",
  "completed_at": "",
  "questionnaires": {
    "resilience_stress": {
      "completed": false,
      "date": null,
      "answers": {
        "r1": null,
        "r2": null,
        ...
      }
    }
  }
}
```

### 2.3 Comment remplir — étape par étape

**Étape 1** : Ouvrez le questionnaire dans votre éditeur de texte (ex : VS Code, Notepad++, même le Bloc-notes)

```
data/profile/questionnaires/05_resilience_stress.md
```

**Étape 2** : Lisez les instructions de passation (en haut du fichier)

**Étape 3** : Répondez à chaque item sur une feuille de brouillon OU directement en notant les scores

**Étape 4** : Ouvrez `answers_template.json` dans votre éditeur

**Étape 5** : Trouvez la section correspondante (ex: `"resilience_stress"`)

**Étape 6** : Remplacez chaque `null` par votre réponse

**Exemple concret — questionnaire résilience/stress :**

```json
"resilience_stress": {
  "completed": true,
  "date": "2026-06-16",
  "duree_minutes": 6,
  "answers": {
    "r1": 3,
    "r2": 3,
    "r3": 4,
    "r4": 2,
    "r5": 3,
    "r6": 4,
    "r7": 2,
    "r8": 3,
    "r9": 3,
    "r10": 4,
    "s1": 2,
    "s2": 1,
    "s3": 3,
    "s4": 4
  }
}
```

**Important :**
- Mettez `"completed": true` (pas `false`) quand vous avez rempli le questionnaire
- Mettez la date du jour au format `"YYYY-MM-DD"` (ex: `"2026-06-16"`)
- Les réponses sont des **nombres entiers**, pas des chaînes de texte
- Pour les items ipsatifs (communication), les réponses sont des **lettres** : `"A"` ou `"B"`

### 2.4 Sauvegarder le fichier

Après avoir saisi vos réponses, sauvegardez `answers_template.json` (Ctrl+S ou Cmd+S).

### 2.5 Vérifier que vos réponses sont dans les bonnes plages

| Questionnaire | Plage valide par item | Items spéciaux |
|---------------|----------------------|----------------|
| big_five_TIPI | 1 à 7 | — |
| intelligence_emotionnelle | 1 à 7 | — |
| valeurs_schwartz | 1 à 6 | — |
| chronotype (CH1-CH5) | Voir questionnaire | Plages variables |
| energie (EN1-EN10) | 1 à 5 | — |
| resilience (R1-R10) | 0 à 4 | — |
| stress (S1-S4) | 0 à 4 | — |
| riasec | 1 à 5 | — |
| engagement (UW1-UW9) | 0 à 6 | — |
| burnout (BU1-BU5) | 0 à 4 | — |
| communication ipsatifs (IP1-IP10) | "A" ou "B" | Lettres, pas chiffres |
| communication likert (CC1-CC15) | 1 à 5 | — |

---

## 3. Comment lancer profile_analyzer.py

### 3.1 Commande de base

Depuis le répertoire racine du projet ALFRED :

```bash
python src/core/profile_analyzer.py
```

### 3.2 Ce que vous allez voir

```
[ProfileAnalyzer] Démarrage du pipeline de profilage...
[ProfileAnalyzer] Fichiers chargés.
[ProfileAnalyzer] Scores calculés — complétude : 62.5%
[ProfileAnalyzer] Dimensions renseignées : resilience_stress, engagement_burnout, chronotype_energie
[ProfileAnalyzer] Paramètres ALFRED générés — tone: chaleureux, support: standard

============================================================
RAPPORT DES SCORES PSYCHOLOGIQUES ALFRED
============================================================

[resilience_stress] ✓ Complété
  Score global : 71.3/100 (élevé)
    - resilience_globale : 75.0/100 (élevé)
    - stress_percu : 67.5/100 (élevé)

[engagement_burnout] ✓ Complété
  Score global : 58.4/100 (moyen)
    - vigueur : 55.6/100 (moyen)
    - devouement : 66.7/100 (moyen)
    - absorption : 44.4/100 (moyen)
    - epuisement : 62.5/100 (moyen)
    - cynisme : 75.0/100 (élevé)
    - efficacite_reduite : 50.0/100 (moyen)

[ProfileAnalyzer] Profil mis à jour : data/profile/user_profile.json
[ProfileAnalyzer] Réponses brutes chiffrées et sécurisées.
[ProfileAnalyzer] Pipeline terminé.
```

### 3.3 Options disponibles

```bash
# Rapport de scores uniquement (sans mise à jour du profil)
python src/core/profile_analyzer.py --report-only

# Analyse sans chiffrement des réponses après (déconseillé)
python src/core/profile_analyzer.py --no-encrypt

# Utiliser un fichier de réponses spécifique
python src/core/profile_analyzer.py --answers /chemin/vers/mes_reponses.json

# Déchiffrer un fichier de réponses archivé
python src/core/profile_analyzer.py --decrypt data/profile/answers_encrypted/answers_20260616_120000.fernet
```

### 3.4 Si une erreur se produit

**Erreur "Fichier introuvable"** :
Vérifiez que vous lancez la commande depuis la racine du projet ALFRED, pas depuis un sous-dossier.

**Erreur "completed est false"** :
Vous n'avez pas mis `"completed": true` dans la section du questionnaire dans `answers_template.json`.

**Erreur de JSON invalide** :
Vérifiez que votre JSON est bien formé (virgules, guillemets). Utilisez un validateur JSON en ligne ou VS Code qui souligne les erreurs JSON.

**Erreur de plage (valeur hors limites)** :
Une réponse est hors de la plage valide pour ce questionnaire. Vérifiez le questionnaire correspondant.

---

## 4. Comment interpréter les résultats

### 4.1 Dans user_profile.json

Après l'analyse, ouvrez `data/profile/user_profile.json`. Vous trouverez une section `psychological_profile` :

```json
"psychological_profile": {
  "last_updated": "2026-06-16T12:30:00",
  "profile_completeness": 62.5,
  "dimensions": {
    "resilience_stress": {
      "completed": true,
      "global_score": 71.3,
      "global_level": "élevé",
      "sub_dimensions": {
        "resilience_globale": { "score": 75.0, "level": "élevé", "completed": true },
        "stress_percu": { "score": 67.5, "level": "élevé", "completed": true }
      }
    }
  }
}
```

Et une section `alfred_derived_params` :

```json
"alfred_derived_params": {
  "last_computed": "2026-06-16T12:30:00",
  "tone": "directif",
  "response_length": "adaptatif",
  "proactivity": "élevé",
  "emotional_support_level": "minimal",
  "challenge_level": "élevé",
  "check_in_frequency": "à_la_demande",
  "explanation_depth": "expert",
  "humor_level": "modéré",
  "structure_preference": "libre",
  "applied_rules": ["rule_resilience_stress_faible", "rule_engagement_eleve"],
  "alerts": []
}
```

### 4.2 Signification des scores (0-100)

| Score | Signification générale |
|-------|------------------------|
| 0-33 | Dimension faiblement présente / niveau bas |
| 34-66 | Zone moyenne / modérée |
| 67-100 | Dimension fortement présente / niveau élevé |

Exceptions notables :
- **Stress perçu** : score élevé = FAIBLE stress (inversé pour cohérence)
- **Épuisement burnout** : score élevé = PEU épuisé (inversé)
- **Chronotype** : score élevé = chronotype SOIR

### 4.3 Alertes importantes

Si la section `alerts` contient des messages, lisez-les attentivement. Exemple :

```json
"alerts": ["Zone de vulnérabilité élevée — envisager un accompagnement professionnel"]
```

Ces alertes ne sont pas des diagnostics — elles indiquent que votre profil combine plusieurs indicateurs défavorables. Elles peuvent signaler le bon moment pour parler à un médecin, un psychologue ou un coach.

---

## 5. Comment ALFRED utilise ces paramètres

### 5.1 Paramètres et leur effet concret

| Paramètre | Valeur | Ce que vous verrez dans ALFRED |
|-----------|--------|-------------------------------|
| `tone: "directif"` | — | Réponses concises, orientées action, pas de "Comment vous sentez-vous ?" |
| `tone: "soutenant"` | — | Plus de reconnaissance émotionnelle, ton doux et rassurant |
| `tone: "analytique"` | — | Raisonnements détaillés, chiffres, arguments structurés |
| `response_length: "court"` | — | Réponses brèves, pas de longs développements |
| `proactivity: "faible"` | — | ALFRED attend que vous demandiez, propose peu spontanément |
| `proactivity: "élevé"` | — | ALFRED suggère proactivement des tâches, insights, rappels |
| `emotional_support: "intensif"` | — | ALFRED commence par reconnaître votre état avant toute action |
| `challenge_level: "élevé"` | — | ALFRED propose des objectifs ambitieux, vous pousse à aller plus loin |
| `humor_level: "modéré"` | — | ALFRED utilise un peu d'humour pour alléger l'atmosphère |
| `structure_preference: "très_structuré"` | — | Listes, étapes numérotées, cadres clairs |

### 5.2 Comment les paramètres sont appliqués

Les paramètres de `alfred_derived_params` sont lus par le moteur comportemental ALFRED (`alfred_behavior_engine.py`) et influencent chaque réponse. Ils ne "forcent" pas ALFRED dans un mode unique — ils orientent ses décisions quand le contexte est ambigu.

Par exemple : si `emotional_support_level = "intensif"` mais que vous demandez "donne-moi la liste de mes réunions", ALFRED vous donnera la liste — mais il sera peut-être attentif à un signe de stress dans votre formulation.

### 5.3 Priorité entre le profil et la situation actuelle

Le profil psychologique est un paramètre de fond. Les signaux de la conversation du moment prennent la priorité :

```
Priorité 1 (plus forte) : Situation d'urgence détectée
Priorité 2 : Émotion exprimée dans le message actuel
Priorité 3 : Profil psychologique (alfred_derived_params)
Priorité 4 : Paramètres par défaut
```

---

## 6. Quand refaire les tests — périodicité

### 6.1 Calendrier de re-passation

| Questionnaire | Fréquence | Prochain rappel conseillé |
|---------------|-----------|--------------------------|
| Résilience + stress (05) | **Mensuelle** | ~30 jours après la première passation |
| Engagement + burnout (07) | **Mensuelle** | ~30 jours après la première passation |
| Chronotype + énergie (04) | Trimestrielle | ~3 mois / changement de saison |
| Intelligence émotionnelle (02) | Semestrielle | ~6 mois |
| Communication + conflits (08) | Semestrielle | ~6 mois |
| Big Five TIPI (01) | Annuelle | ~12 mois |
| Valeurs Schwartz (03) | Annuelle | ~12 mois |
| RIASEC (06) | Annuelle | ~12 mois |
| AssessFirst | Changement de vie | Délai minimum : 3 ans |

### 6.2 Signes qui déclenchent une re-passation anticipée

**Re-passez le questionnaire stress/résilience si :**
- Vous avez vécu un événement difficile (deuil, rupture, conflit majeur)
- Vous vous sentez épuisé(e) de façon persistante
- Votre score précédent était en zone critique

**Re-passez le questionnaire engagement/burnout si :**
- Vous avez perdu la motivation pour des tâches qui vous plaisaient
- Vous avez du mal à vous lever le matin sans redouter votre journée
- Vous travaillez régulièrement plus de 50h/semaine depuis plusieurs semaines

**Re-passez le questionnaire chronotype/énergie si :**
- Le passage à l'heure d'été ou d'hiver vous impacte fortement
- Vous avez changé vos habitudes de sommeil, d'exercice ou d'alimentation

### 6.3 Comment gérer plusieurs questionnaires dus en même temps

Ne vous forcez pas à tout faire d'un coup. Règle simple :
1. Commencez TOUJOURS par stress/résilience et engagement/burnout (santé prioritaire)
2. Ajoutez un questionnaire secondaire si vous avez l'énergie
3. Maximum 2 questionnaires par session

---

## 7. Gérer la clé de chiffrement

### 7.1 Qu'est-ce que la clé de chiffrement ?

C'est le fichier `data/security/fernet.key`. Il permet de déchiffrer vos réponses brutes stockées dans `data/profile/answers_encrypted/`. Sans cette clé, les archives `.fernet` sont illisibles.

### 7.2 La clé est créée automatiquement

La première fois que vous lancez `profile_analyzer.py`, une clé est automatiquement créée si elle n'existe pas. Vous verrez le message :
```
[ProfileAnalyzer] Génération d'une nouvelle clé Fernet...
[ProfileAnalyzer] Clé sauvegardée : data/security/fernet.key
[ProfileAnalyzer] ATTENTION : ne jamais commiter ce fichier de clé !
```

### 7.3 Sauvegarder votre clé

**Très important** : si vous perdez votre clé, vous ne pourrez plus déchiffrer vos archives de réponses.

Trois options pour sauvegarder la clé :

**Option 1 (recommandée) : Gestionnaire de mots de passe**
Copiez le contenu de `data/security/fernet.key` et stockez-le dans votre gestionnaire de mots de passe (Bitwarden, 1Password, etc.) sous le nom "ALFRED Fernet Key".

**Option 2 : Variable d'environnement dans .env**
```bash
# Dans .env (déjà exclu de git)
FERNET_KEY=gAAAAAB...votre_clé_ici
```

**Option 3 : Backup physique chiffré**
Exportez la clé sur une clé USB chiffrée stockée en lieu sûr.

### 7.4 Ne jamais commiter la clé

Le fichier `data/security/fernet.key` est exclu du git via `.gitignore`. Si vous faites accidentellement `git add data/security/fernet.key`, annulez immédiatement avec `git reset data/security/fernet.key`.

### 7.5 Déchiffrer vos réponses passées

Pour relire vos réponses archivées :

```bash
python src/core/profile_analyzer.py --decrypt data/profile/answers_encrypted/answers_20260616_120000.fernet
```

Cela affichera vos réponses en JSON dans le terminal.

---

## 8. FAQ

**Q : Je dois remplir les questionnaires dans quel ordre exactement ?**
Commencez par les questionnaires marqués "mensuelle" (stress/résilience et engagement/burnout). Ce sont les plus importants pour adapter immédiatement ALFRED. Les autres peuvent être faits dans n'importe quel ordre.

---

**Q : Je me sens nulle si je vois un score faible en résilience. Est-ce grave ?**
Non. Un score faible à un moment donné reflète votre état actuel ou récent — pas une vérité permanente sur vous. La résilience se développe et varie avec les circonstances. ALFRED interprétera ce score pour vous apporter plus de soutien, pas pour vous juger.

---

**Q : Mes réponses AssessFirst et mes scores TIPI sont différents. Lequel est juste ?**
Les deux peuvent l'être simultanément. AssessFirst est une mesure plus précise (plus d'items, algorithme adaptatif). Le TIPI est une mesure rapide avec une marge d'erreur plus large. En cas de discordance, **les données AssessFirst priment** dans le système ALFRED.

---

**Q : Est-ce que je peux modifier mes réponses après coup ?**
Oui. Éditez simplement `answers_template.json`, changez les valeurs, et relancez `profile_analyzer.py`. Une nouvelle archive chiffrée sera créée et le profil sera mis à jour.

---

**Q : Que se passe-t-il si je mens dans mes réponses ?**
Le système vous donne un profil qui ne correspondra pas à la réalité, et ALFRED adaptera son comportement de façon inappropriée. Ces données n'ont de valeur que si elles sont authentiques. Personne d'autre que vous ne les voit.

---

**Q : Mon score de burnout est critique. Que dois-je faire ?**
ALFRED activera automatiquement un mode de soutien renforcé. Mais un score critique de burnout est un signal que vous devriez aussi consulter un médecin ou un psychologue. ALFRED n'est pas un outil thérapeutique — il peut vous accompagner mais pas vous soigner.

---

**Q : Puis-je partager mon profil user_profile.json avec quelqu'un ?**
Techniquement oui, mais réfléchissez à ce que vous partagez : ce fichier contient vos scores de résilience, de stress, d'engagement et vos valeurs fondamentales. C'est de l'information psychologique sensible. Partagez uniquement si vous faites pleinement confiance à la personne.

---

**Q : ALFRED va-t-il changer radicalement de comportement après la première analyse ?**
Oui, potentiellement. Si votre profil indique par exemple une préférence pour la directivité et les réponses courtes, ALFRED sera moins bavard et plus orienté action. Si votre profil indique un besoin de soutien émotionnel élevé, ALFRED sera plus attentif à votre état. Les changements sont graduels et toujours dans le but de mieux vous servir.

---

**Q : Et si je ne veux pas qu'ALFRED adapte son comportement à mon profil ?**
Vous pouvez supprimer les sections `psychological_profile` et `alfred_derived_params` de `user_profile.json`. ALFRED utilisera alors ses paramètres par défaut. Vous pouvez aussi simplement ne pas remplir les questionnaires.

---

*Pour toute question sur la sécurité des données, consultez `docs/profil_systeme/securite_donnees.md`.*  
*Pour comprendre la conception technique, consultez `docs/profil_systeme/conception_technique.md`.*
