# Questionnaire 06 — Intérêts professionnels RIASEC
## Basé sur la théorie hexagonale de Holland (1997) — Items originaux

---

### Informations sur le framework

| Champ | Information |
|-------|-------------|
| **Framework** | Théorie hexagonale des intérêts professionnels (RIASEC) |
| **Auteur** | Holland, J.L. |
| **Année** | 1997 (3e édition) |
| **Publication** | Holland, J.L. (1997). *Making vocational choices: A theory of vocational personalities and work environments* (3rd ed.). Psychological Assessment Resources, Odessa, FL. |
| **Références complémentaires** | Holland, J.L. (1985). *Making Vocational Choices: A Theory of Vocational Personalities and Work Environments* (2nd ed.). Prentice Hall. |
| **Note copyright** | Le Self-Directed Search (SDS) officiel est propriétaire (Psychological Assessment Resources). Les 18 items ci-dessous sont **originaux**, créés pour être fidèles aux descripteurs des types Holland sans reproduire les items du SDS. |
| **Durée estimée** | 8-10 minutes |
| **Fréquence recommandée** | Annuelle |
| **Domaine d'application** | Orientation professionnelle et identification des environnements de travail compatibles — usage personnel |

---

### Construits mesurés

Les **6 types RIASEC de Holland** correspondent à des combinaisons d'intérêts, de compétences et de valeurs professionnelles. Chaque personne est caractérisée par un profil hexagonal et un **code Holland à 3 lettres** (les 3 types dominants).

| Type | Caractéristiques | Environnements compatibles |
|------|-----------------|---------------------------|
| **R — Réaliste** | Concret, manuel, technique, physique | Ingénierie, artisanat, sport, agriculture |
| **I — Investigateur** | Analytique, scientifique, curieux, solitaire | Recherche, sciences, technologie, médecine |
| **A — Artistique** | Créatif, expressif, intuitif, non-conformiste | Arts, design, écriture, musique, entrepreneuriat créatif |
| **S — Social** | Altruiste, communicatif, pédagogue, empathique | Éducation, soin, conseil, RH |
| **E — Entreprenant** | Leader, persuasif, ambitieux, compétitif | Management, vente, politique, entrepreneuriat |
| **C — Conventionnel** | Ordonné, précis, fiable, procédurier | Comptabilité, administration, data, conformité |

**L'hexagone de Holland** : les types adjacents sont les plus compatibles (R-I, I-A, A-S, S-E, E-C, C-R). Les types opposés sont les moins compatibles (R-S, I-E, A-C).

---

### Instructions de passation

---

*Pour chaque affirmation, indiquez dans quelle mesure cette activité ou ce type de travail vous attire ou vous correspond, même si vous n'en avez pas encore fait l'expérience directe.*

| Score | Signification |
|-------|---------------|
| **1** | Cela ne m'attire pas du tout |
| **2** | Cela m'attire peu |
| **3** | Je suis neutre / pas certain(e) |
| **4** | Cela m'attire assez |
| **5** | Cela m'attire beaucoup |

---

### Items

**Type R — Réaliste (3 items)**

| N° | Affirmation | Ma réponse (1-5) |
|----|-------------|-----------------|
| **RI1** | Travailler avec des outils, des machines ou des équipements techniques concrets | |
| **RI2** | Résoudre des problèmes pratiques qui nécessitent des compétences manuelles ou techniques | |
| **RI3** | Effectuer des tâches physiques ou mécaniques avec un résultat tangible et mesurable | |

**Type I — Investigateur (3 items)**

| N° | Affirmation | Ma réponse (1-5) |
|----|-------------|-----------------|
| **RI4** | Analyser des données complexes pour découvrir des patterns ou des vérités cachées | |
| **RI5** | Mener des recherches approfondies pour répondre à des questions difficiles | |
| **RI6** | Construire des théories, des modèles ou des explications pour comprendre le monde | |

**Type A — Artistique (3 items)**

| N° | Affirmation | Ma réponse (1-5) |
|----|-------------|-----------------|
| **RI7** | Créer des œuvres originales (écriture, design, musique, art visuel, scénario) | |
| **RI8** | Travailler dans un environnement où l'expression personnelle est valorisée et attendue | |
| **RI9** | Imaginer et concevoir des choses nouvelles sans contraintes de règles ou de procédures fixes | |

**Type S — Social (3 items)**

| N° | Affirmation | Ma réponse (1-5) |
|----|-------------|-----------------|
| **RI10** | Enseigner, former ou transmettre des connaissances à d'autres personnes | |
| **RI11** | Accompagner des personnes en difficulté ou en développement (conseil, coaching, soin) | |
| **RI12** | Travailler en collaboration étroite avec des équipes et construire des relations humaines durables | |

**Type E — Entreprenant (3 items)**

| N° | Affirmation | Ma réponse (1-5) |
|----|-------------|-----------------|
| **RI13** | Diriger des projets ou des équipes et prendre des décisions stratégiques | |
| **RI14** | Convaincre et influencer des personnes ou des organisations pour atteindre des objectifs | |
| **RI15** | Lancer des initiatives, prendre des risques calculés et développer une vision à long terme | |

**Type C — Conventionnel (3 items)**

| N° | Affirmation | Ma réponse (1-5) |
|----|-------------|-----------------|
| **RI16** | Organiser, classer et gérer des données ou des informations avec précision | |
| **RI17** | Suivre des procédures établies et s'assurer de leur bonne application | |
| **RI18** | Travailler dans un environnement structuré avec des règles claires et des responsabilités définies | |

---

### Calcul de votre code Holland

Notez vos scores par type :

| Type | Items | Total (max 15) | Rang |
|------|-------|---------------|------|
| R — Réaliste | RI1 + RI2 + RI3 | | |
| I — Investigateur | RI4 + RI5 + RI6 | | |
| A — Artistique | RI7 + RI8 + RI9 | | |
| S — Social | RI10 + RI11 + RI12 | | |
| E — Entreprenant | RI13 + RI14 + RI15 | | |
| C — Conventionnel | RI16 + RI17 + RI18 | | |

**Mon code Holland** (3 types avec les scores les plus élevés, du plus haut au plus bas) : **___ ___ ___**

---

### Après la passation — Où enregistrer vos réponses

1. Ouvrez `data/profile/scoring/answers_template.json`
2. Remplissez la section `riasec_interets_pro` :

```json
"riasec_interets_pro": {
  "completed": true,
  "date": "YYYY-MM-DD",
  "answers": {
    "ri1": VOTRE_RÉPONSE,
    "ri2": VOTRE_RÉPONSE,
    "ri3": VOTRE_RÉPONSE,
    "ri4": VOTRE_RÉPONSE,
    "ri5": VOTRE_RÉPONSE,
    "ri6": VOTRE_RÉPONSE,
    "ri7": VOTRE_RÉPONSE,
    "ri8": VOTRE_RÉPONSE,
    "ri9": VOTRE_RÉPONSE,
    "ri10": VOTRE_RÉPONSE,
    "ri11": VOTRE_RÉPONSE,
    "ri12": VOTRE_RÉPONSE,
    "ri13": VOTRE_RÉPONSE,
    "ri14": VOTRE_RÉPONSE,
    "ri15": VOTRE_RÉPONSE,
    "ri16": VOTRE_RÉPONSE,
    "ri17": VOTRE_RÉPONSE,
    "ri18": VOTRE_RÉPONSE
  }
}
```

---

### Clé de scoring

| Sous-dimension | Items | Calcul | Normalisation |
|----------------|-------|--------|---------------|
| Réaliste | RI1, RI2, RI3 | Somme (0-15) | `(somme / 15) × 100` |
| Investigateur | RI4, RI5, RI6 | Somme (0-15) | `(somme / 15) × 100` |
| Artistique | RI7, RI8, RI9 | Somme (0-15) | `(somme / 15) × 100` |
| Social | RI10, RI11, RI12 | Somme (0-15) | `(somme / 15) × 100` |
| Entreprenant | RI13, RI14, RI15 | Somme (0-15) | `(somme / 15) × 100` |
| Conventionnel | RI16, RI17, RI18 | Somme (0-15) | `(somme / 15) × 100` |

---

### Interprétation du code Holland

**Score normalisé :**
- **0-33** : Type non dominant — peu présent dans votre profil
- **34-66** : Type secondaire — présent en complément
- **67-100** : Type dominant — central dans votre profil d'intérêts

**Quelques codes Holland et leur signification :**

| Code | Profil caractéristique |
|------|----------------------|
| IAS | Chercheur créatif, scientifique en sciences humaines, consultant stratégique |
| SAI | Formateur créatif, coach, facilitateur artistique |
| EIS | Entrepreneur scientifique, directeur R&D, fondateur de startup tech |
| ESA | Dirigeant empathique, fondateur à impact, entrepreneur social |
| AIS | Créatif analytique, UX researcher, designer de systèmes |
| ISA | Chercheur en sciences sociales, psychologue, formateur académique |
| ESC | Manager organisé, directeur commercial, consultant en management |

---

*Référence principale : Holland, J.L. (1997). Making vocational choices: A theory of vocational personalities and work environments (3rd ed.). Psychological Assessment Resources.*
