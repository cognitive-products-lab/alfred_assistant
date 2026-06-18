# Dimensions psychologiques — Justifications scientifiques
## Module Profil IA Adaptative — ALFRED

> Version 1.0 — 2026-06-16  
> Sources : littérature scientifique peer-reviewed, instruments validés internationalement

---

## Principes de sélection des frameworks

Les frameworks retenus répondent à 5 critères :

1. **Validation scientifique** : études peer-reviewed, psychométrie rigoureuse (α > 0.70)
2. **Versions courtes disponibles** : ≤ 15 items pour limiter la charge cognitive
3. **Normalisation internationale** : données de référence (moyennes, écarts-types populationnels)
4. **Pertinence pour l'adaptation IA** : dimensions ayant un impact démontré sur les préférences d'interaction
5. **Disponibilité en français** : traductions validées pour population francophone

---

## Les 9 dimensions

### Dimension 1 — Personnalité (Big Five)

| Champ | Valeur |
|-------|--------|
| **Framework** | Big Five / Five Factor Model |
| **Instrument** | TIPI — Ten-Item Personality Inventory |
| **Source** | Gosling, Rentfrow & Swann (2003), *Journal of Research in Personality* |
| **Items** | 10 (2 items par dimension) |
| **Échelle** | Likert 7 (1 = pas du tout d'accord, 7 = tout à fait d'accord) |
| **Questionnaire** | `data/profile/questionnaires/01_big_five_TIPI.md` |
| **Scoring** | Moyenne par dimension (items inversés : 2, 4, 6, 8, 10) |

**Les 5 sous-dimensions (OCEAN)** :
- **O — Ouverture** : curiosité intellectuelle, créativité, ouverture aux nouvelles expériences
- **C — Conscienciosité** : organisation, autodiscipline, fiabilité, orientation vers les objectifs
- **E — Extraversion** : sociabilité, assertivité, énergie relationnelle
- **A — Agréabilité** : coopération, confiance, empathie, bienveillance
- **N — Névrosisme** : instabilité émotionnelle, anxiété (inversé → stabilité émotionnelle)

**Impact sur ALFRED** : ton (E, A), challenge_level (O, C), proactivity (E), emotional_support_level (N inversé)

**Alignement AssessFirst** : SWIPE correspond directement aux Big Five — résultats AssessFirst complètent le TIPI

---

### Dimension 2 — Intelligence Émotionnelle

| Champ | Valeur |
|-------|--------|
| **Framework** | Trait Emotional Intelligence (TEI) |
| **Instrument** | TEIQue-SF — Trait Emotional Intelligence Questionnaire Short Form |
| **Source** | Petrides (2009), *Psychometric Theory and Educational Assessment* |
| **Items** | 15 items (adaptés) |
| **Échelle** | Likert 7 (1 = pas du tout d'accord, 7 = tout à fait d'accord) |
| **Questionnaire** | `data/profile/questionnaires/02_intelligence_emotionnelle.md` |

**Les 4 facettes mesurées** :
- **Bien-être émotionnel** : satisfaction de vie, bonheur, optimisme
- **Auto-contrôle** : régulation émotionnelle, gestion du stress, faible impulsivité
- **Émotivité** : empathie, perception émotionnelle, relations intimes
- **Sociabilité** : assertivité, compétences sociales, gestion des émotions d'autrui

**Impact sur ALFRED** : emotional_support_level, tone (warmth), check_in_frequency

---

### Dimension 3 — Valeurs Fondamentales

| Champ | Valeur |
|-------|--------|
| **Framework** | Théorie des valeurs humaines de base |
| **Instrument** | PVQ-21 — Portrait Values Questionnaire |
| **Source** | Schwartz et al. (2001), *Journal of Cross-Cultural Psychology* |
| **Items** | 21 portraits (2 par valeur sauf sécurité = 3) |
| **Échelle** | Likert 6 (1 = ne me ressemble pas du tout, 6 = me ressemble tout à fait) |
| **Questionnaire** | `data/profile/questionnaires/03_valeurs_schwartz.md` |
| **Note** | Correction "ipsative" obligatoire : centrage par la moyenne individuelle |

**Les 10 valeurs universelles** :
- Universalisme, Bienveillance, Conformité, Tradition, Sécurité
- Pouvoir, Réussite, Hédonisme, Stimulation, Autonomie

**Regroupement en 4 valeurs supérieures** :
```
Ouverture au changement ←────────────────────────────────→ Conservation
(Autonomie, Stimulation, Hédonisme)          (Sécurité, Conformité, Tradition)

      ↑                                                          ↑
      │                                                          │
  Dépassement                                            Affirmation de soi
  de soi                                                 (Pouvoir, Réussite,
  (Universalisme,                                         Hédonisme)
   Bienveillance)
```

**Impact sur ALFRED** : challenge_level (Réussite/Stimulation), humor_level (Hédonisme), tone (Universalisme)

---

### Dimension 4 — Chronotype & Énergie

| Champ | Valeur |
|-------|--------|
| **Framework** | Chronobiologie — rythmes circadiens |
| **Instrument** | rMEQ — Reduced Morningness-Eveningness Questionnaire |
| **Source** | Adan & Almirall (1991), *Personality and Individual Differences* |
| **Items** | 5 items rMEQ + 10 items énergie personnalisés |
| **Questionnaire** | `data/profile/questionnaires/04_chronotype_energie.md` |

**Types chronobiologiques** :
- **Matinal** (score > 18) : pic d'énergie 6h-12h, baisse l'après-midi
- **Intermédiaire** (10-18) : flexibilité relative
- **Vespéral** (< 10) : pic d'énergie 14h-22h

**Impact sur ALFRED** : timing des check-ins, tone selon l'heure, proactivity (ne pas solliciter pendant creux d'énergie)

---

### Dimension 5 — Résilience & Stress

| Champ | Valeur |
|-------|--------|
| **Frameworks** | Résilience psychologique + Stress perçu |
| **Instruments** | CD-RISC-10 + PSS-4 |
| **Sources** | Connor & Davidson (2003), *Depression and Anxiety* / Cohen, Kamarck & Mermelstein (1983), *Journal of Health and Social Behavior* |
| **Items** | 10 (CD-RISC-10) + 4 (PSS-4) = 14 items |
| **Questionnaire** | `data/profile/questionnaires/05_resilience_stress.md` |

**CD-RISC-10** — 10 items, Likert 5 (0-4) :
- Capacité d'adaptation, persévérance, contrôle, sens de l'efficacité
- Score 0-40 : < 25 = résilience faible ; 25-32 = modérée ; > 32 = élevée

**PSS-4** — 4 items, Likert 5 (0-4) — dont 2 inversés :
- Mesure l'évaluation subjective du stress des 30 derniers jours
- Score 0-16 : > 9 = stress élevé

**ALERTE CRITIQUE** : PSS-4 > 12 + UWES exhaustion élevé → risk burnout → paramètres ALFRED modifiés (soutien renforcé, check-in quotidien)

---

### Dimension 6 — Intérêts Professionnels (RIASEC)

| Champ | Valeur |
|-------|--------|
| **Framework** | Théorie des types de personnalité professionnelle |
| **Instrument** | RIASEC — Inventory of Holland (1997) |
| **Source** | Holland (1997), *Making Vocational Choices: A Theory of Vocational Personalities* |
| **Items** | 18 items (3 par type), Likert 5 |
| **Questionnaire** | `data/profile/questionnaires/06_riasec_interets_pro.md` |

**Les 6 types RIASEC** :
- **R — Réaliste** : technique, manuel, concret
- **I — Investigateur** : analytique, recherche, scientifique
- **A — Artistique** : créatif, expressif, intuitif
- **S — Social** : enseignement, aide, travail en équipe
- **E — Entrepreneur** : leadership, influence, gestion
- **C — Conventionnel** : organisation, précision, méthode

**Hexagone de Holland** :
```
        R ─── I
       / \   / \
      C   \ /   A
      │    X    │
      E   / \   S
       \ /   \ /
        E ─── S
```
Les types adjacents = compatibles. Types opposés = tension.

**Impact sur ALFRED** : tone (S vs R), challenge_level (I vs C), proactivity (E vs I)

---

### Dimension 7 — Engagement & Burnout

| Champ | Valeur |
|-------|--------|
| **Frameworks** | Engagement professionnel + indicateurs de burnout |
| **Instruments** | UWES-9 + indicateur burnout simplifié CPL |
| **Source** | Schaufeli & Bakker (2004), *Journal of Organizational Behavior* |
| **Items** | 9 (UWES-9) + 3 (burnout) = 12 items |
| **Échelle** | Likert 7 (0 = jamais, 6 = toujours) |
| **Questionnaire** | `data/profile/questionnaires/07_engagement_burnout.md` |

**UWES-9 — 3 sous-échelles** :
- **Vigueur** (3 items) : énergie, résilience, persévérance au travail
- **Dévouement** (3 items) : enthousiasme, inspiration, fierté, sens
- **Absorption** (3 items) : concentration intense, temps qui "file"

**Score engagement global** = mean(9 items). < 3.0 = faible, 3.0-4.5 = modéré, > 4.5 = élevé

**Indicateur burnout** : exhaustion + cynisme + efficacité réduite

**Impact sur ALFRED** :
- Engagement élevé → challenge_level élevé, proactivity élevée
- Burnout détecté → ALERTE → soutien émotionnel max, check-in quotidien, challenge réduit

---

### Dimension 8 — Communication & Gestion des Conflits

| Champ | Valeur |
|-------|--------|
| **Framework** | 5 modes de gestion des conflits |
| **Instrument** | Inspiré du TKI — Thomas-Kilmann Conflict Mode Instrument |
| **Source** | Thomas & Kilmann (1974), *Thomas-Kilmann Conflict Mode Instrument* |
| **Items** | Hybride Likert 5 + items ipsatifs |
| **Questionnaire** | `data/profile/questionnaires/08_communication_conflit.md` |

**Les 5 modes** :
```
                    Assertivité
                        ↑
            Compétition │ Collaboration
                        │
         ───────────────┼─────────────── →
                        │            Coopération
           Évitement    │  Compromis
                        │
            Accommodement
                        ↓
```

| Mode | Assertivité | Coopération | Description |
|------|-------------|-------------|-------------|
| **Compétition** | Haute | Basse | Impose sa position |
| **Collaboration** | Haute | Haute | Cherche solution gagnant-gagnant |
| **Compromis** | Moyenne | Moyenne | Trouver un terrain d'entente |
| **Évitement** | Basse | Basse | Reporte ou esquive le conflit |
| **Accommodation** | Basse | Haute | Cède pour préserver la relation |

**Impact sur ALFRED** : tone (Collaboration vs Compétition), structure_preference (Évitement = pas de conflit direct), emotional_support_level

---

### Dimension 9 — Profil AssessFirst (SWIPE-DRIVE-BRAIN)

| Champ | Valeur |
|-------|--------|
| **Framework** | Propriétaire AssessFirst — basé sur Big Five + motivations + cognition |
| **Instrument** | SWIPE (personnalité) + DRIVE (motivations) + BRAIN (aptitudes cognitives) |
| **Source** | `data/profile/user_profile.json` |
| **Passation** | Déjà réalisée (15/06/2026 — Céline Rousselot) |
| **URL profil** | https://my.assessfirst.com/public/profile/wslje1tn-celine-rousselot?lang=fr-FR |

**Données intégrées dans `user_profile.json`** :
- `personality_traits` : 14 traits issus de SWIPE
- `softskills` : 12 compétences comportementales de DRIVE
- `why_keywords` : motivations profondes
- `preferences.style_personnel` : "Partenaire"
- `preferences.prise_de_decision` : "Raisonnée"
- `preferences.style_apprentissage` : "Innovante"

**Complémentarité avec les questionnaires scientifiques** :
- AssessFirst mesure sur des populations normées (benchmark emploi)
- Les questionnaires CPL mesurent l'état actuel et évoluent dans le temps
- AssessFirst reste stable (traits de personnalité profonds)

---

## Tableau récapitulatif

| # | Dimension | Items | Durée | Périodicité | Déclencheur alerte |
|---|-----------|-------|-------|-------------|-------------------|
| 1 | Big Five (TIPI) | 10 | 5 min | Annuelle | < 20/70 Conscienciosité |
| 2 | Intelligence émotionnelle | 15 | 7 min | Semestrielle | Facette bien-être < 30/100 |
| 3 | Valeurs Schwartz | 21 | 10 min | Annuelle | Conflit valeurs-travail fort |
| 4 | Chronotype & énergie | 15 | 8 min | Trimestrielle | Décalage chronotype > 3h |
| 5 | Résilience & stress | 14 | 6 min | Mensuelle | PSS > 12 ou CD-RISC < 20 |
| 6 | RIASEC | 18 | 8 min | Annuelle | Mismatch profil-activité |
| 7 | Engagement & burnout | 12 | 6 min | Mensuelle | UWES < 2.5 ou burnout > 3 |
| 8 | Communication | ~15 | 8 min | Semestrielle | Mode évitement dominant |
| 9 | AssessFirst | — | Déjà fait | Changement de vie | N/A |
| — | Profil complémentaire Q00 | 23 | 10-15 min | À la demande | N/A |

**Durée totale passation complète** : ~1h15 (8 questionnaires + Q00)  
**Durée minimale (questionnaires prioritaires)** : ~25 min (Q05 stress + Q07 engagement)

---

*Document créé le 2026-06-16 — Cognitive Products Lab*
