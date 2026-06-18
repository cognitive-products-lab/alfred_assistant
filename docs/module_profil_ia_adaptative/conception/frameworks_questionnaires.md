# Comparatif des frameworks de personnalité
## Sélection et justification pour le module profil ALFRED

> Version 1.0 — 2026-06-16  
> Classement par robustesse scientifique (littérature peer-reviewed)

---

## Tableau de comparaison global

| # | Framework | Items | Validité | Fiabilité | Intégré CPL | Note |
|---|-----------|-------|----------|-----------|-------------|------|
| 1 | **Big Five / NEO PI-R** | 240 (NEO PI-R) / 10 (TIPI) | ★★★★★ | ★★★★★ | ✅ TIPI | Référence scientifique internationale |
| 2 | **HEXACO** | 60-100 (HEXACO-PI-R) / 24 (court) | ★★★★★ | ★★★★★ | 📋 À intégrer | Ajoute Honnêteté-Humilité au Big Five |
| 3 | **MMPI-3** | 335 | ★★★★★ | ★★★★★ | ❌ Exclu | Clinique — nécessite psychologue |
| 4 | **16PF** | 185 | ★★★★☆ | ★★★★☆ | 📋 Envisageable | Cattell — 16 facteurs primaires |
| 5 | **Hogan (HPI)** | 206 | ★★★★☆ | ★★★★☆ | ❌ Exclu | Licencié, usage RH professionnel uniquement |
| 6 | **PAI** | 344 | ★★★★☆ | ★★★★☆ | ❌ Exclu | Clinique — PAI-A ou PAI-SP pour contexts |
| 7 | **AssessFirst** | ~250 (SWIPE+DRIVE+BRAIN) | ★★★★☆ | ★★★★☆ | ✅ Intégré | Déjà réalisé — données dans user_profile.json |
| 8 | **SOSIE 2nd Generation** | 98 | ★★★★☆ | ★★★★☆ | ❌ Exclu | Licencié PEARSON — usage RH seulement |
| 9 | **MBTI** | 93 | ★★☆☆☆ | ★★★☆☆ | 📋 Optionnel | Populaire en France, validité scientifique limitée |
| 10 | **DISC** | ~24-28 | ★★☆☆☆ | ★★★☆☆ | 📋 Optionnel | Simple, populaire entreprise, 4 profils |
| 11 | **Ennéagramme** | Variable | ★☆☆☆☆ | ★★☆☆☆ | ❌ Exclu | Aucune validation psychométrique sérieuse |

---

## Analyse détaillée par framework

### 1. Big Five / NEO PI-R ★★★★★

**Fondateurs** : Costa & McCrae (1985, 1992)  
**Statut CPL** : ✅ Implémenté via TIPI (Gosling 2003, 10 items)

Le Big Five est le modèle de personnalité le plus validé scientifiquement au monde. Ses 5 dimensions (OCEAN) sont reproductibles cross-culturellement et prédisent des comportements réels (performance, satisfaction, longévité).

**Versions disponibles** :
| Version | Items | Usage recommandé |
|---------|-------|-----------------|
| NEO PI-R | 240 | Clinique/recherche — trop long pour ALFRED |
| NEO-FFI | 60 | Bonne alternative si plus de profondeur souhaitée |
| BFI-2 | 60 | Version récente, meilleure structure factorielle |
| BFI-2-S | 30 | Court, bonne fiabilité (α ≥ 0.75) |
| **TIPI** | **10** | **Utilisé dans CPL** — ultra court, suffisant pour paramétrage ALFRED |
| BFI-10 | 10 | Alternative au TIPI, légèrement moins fiable |

**Décision CPL** : TIPI est le bon choix pour une passation conversationnelle de 5 min. Le NEO PI-R apporterait davantage de nuances mais est inadapté à l'UX ALFRED.

---

### 2. HEXACO ★★★★★

**Fondateurs** : Ashton & Lee (2001, 2007)  
**Statut CPL** : 📋 À intégrer — apporte une valeur réelle vs. Big Five seul

HEXACO est une extension à 6 facteurs du Big Five, ajoutant la dimension **Honnêteté-Humilité (H)**. Cette dimension, absente du Big Five, est particulièrement pertinente pour prédire :
- L'intégrité et les comportements éthiques
- La manipulation et le narcissisme (faible H)
- La coopération authentique vs. stratégique

**Les 6 dimensions HEXACO** :
```
H — Honnêteté-Humilité    : sincérité, modestie, équité, non-avidité
E — Émotivité             : anxiété, dépendance émotionnelle, empathie
X — eXtraversion          : estime de soi, assertivité, sociabilité
A — Agréabilité           : patience, flexibilité, tolérance, douceur
C — Conscienciosité       : organisation, diligence, perfectionnisme
O — Ouverture             : curiosité intellectuelle, créativité
```

**Instruments disponibles** :
| Version | Items | Durée estimée |
|---------|-------|---------------|
| HEXACO-PI-R (complet) | 100 | 20-25 min |
| HEXACO-60 | 60 | 12-15 min |
| HEXACO-24 | 24 | 5-7 min |

**Recommandation CPL** : Intégrer **HEXACO-24** (24 items, 4 par dimension) en questionnaire conversationnel ALFRED. La dimension H (Honnêteté-Humilité) améliore la prédiction du style de communication d'ALFRED.

**Impact sur les paramètres ALFRED** :
- H élevé → tone plus direct, moins de flatterie dans les réponses
- H faible → surveillance accrue des biais de confirmation dans les suggestions
- E élevé → emotional_support_level plus empathique
- C élevé → structure_preference = structuré, explanation_depth = approfondi

---

### 3. MMPI-3 ★★★★★ — EXCLU

**Fondateurs** : Hathaway & McKinley (1943), révision MMPI-3 (2020)

**Pourquoi exclu** :
- Instrument **clinique** — nécessite une administration et une interprétation par un psychologue qualifié
- 335 items — incompatible avec l'UX conversationnelle ALFRED
- Conçu pour détecter des psychopathologies, pas pour la personnalité "normale"
- Usage dans une app grand public serait **éthiquement problématique** et potentiellement dangereux (faux positifs, stigmatisation)

**Verdict** : Ne pas intégrer. Si un utilisateur d'ALFRED présente des signes de détresse clinique, ALFRED peut suggérer de consulter un professionnel de santé — mais ne peut pas diagnostiquer.

---

### 4. 16PF (Sixteen Personality Factor) ★★★★☆

**Fondateur** : Raymond Cattell (1949), version actuelle 16PF5

**Pourquoi envisageable mais non prioritaire** :
- 16 facteurs primaires → 5 facteurs globaux (proches du Big Five)
- 185 items version standard — trop long
- 16PF Select (court) existe mais reste licencié
- Apporte une granularité supérieure au Big Five mais la version courte est moins fiable

**Verdict CPL** : Le Big Five via TIPI + HEXACO-24 couvre mieux les besoins pour moins de charge cognitive. 16PF n'est pas prioritaire en V1.

---

### 5. Hogan Personality Inventory (HPI) ★★★★☆ — EXCLU

**Fondateurs** : R. & J. Hogan (1992)

**Pourquoi exclu** :
- **Instrument propriétaire** — licence obligatoire via Hogan Assessment Systems
- Conçu pour le **recrutement RH** — prédit la performance professionnelle
- 206 items — trop long pour ALFRED
- Accès réglementé (certifications requises pour administrer)

**Verdict** : Non intégrable légalement et techniquement. AssessFirst couvre déjà ce besoin (résultats déjà intégrés dans user_profile.json).

---

### 6. PAI (Personality Assessment Inventory) ★★★★☆ — EXCLU

**Fondateur** : Morey (1991)

**Pourquoi exclu** :
- Instrument **clinique** — conçu pour évaluer des troubles de la personnalité
- 344 items
- Comme le MMPI, son usage dans une app grand public est éthiquement inadapté

**Verdict** : Exclu. Voir MMPI-3.

---

### 7. AssessFirst (SWIPE-DRIVE-BRAIN) ★★★★☆

**Éditeur** : AssessFirst (France)  
**Statut CPL** : ✅ Déjà intégré

**Pourquoi déjà intégré** : Céline Rousselot a réalisé l'évaluation complète (15/06/2026). Les résultats sont dans `data/profile/user_profile.json`.

**Ce qu'il mesure** :
- **SWIPE** : Personnalité (proche Big Five, normé sur population emploi)
- **DRIVE** : Motivations et soft skills
- **BRAIN** : Aptitudes cognitives

**Complémentarité** : AssessFirst mesure les traits stables (benchmark emploi). Les questionnaires CPL mesurent l'état actuel (évolutif dans le temps).

---

### 8. SOSIE 2nd Generation ★★★★☆ — EXCLU

**Éditeur** : Pearson (France)

**Pourquoi exclu** :
- **Instrument propriétaire** sous licence Pearson
- Usage réglementé (formation obligatoire pour administrer)
- 98 items sur valeurs + personnalité (Spranger + Big Five)
- Très utilisé en RH France — mais pas accessible pour intégration libre

**Verdict** : Non intégrable. Les valeurs sont couvertes par PVQ-21/Schwartz (libre).

---

### 9. MBTI ★★☆☆☆ — Optionnel avec mise en garde

**Fondateurs** : Myers & Briggs (1940s, basé sur Jung)

**Popularité vs. validité** : Le MBTI est extrêmement populaire en entreprise française (coaching, team building) mais souffre de critiques scientifiques sérieuses :
- Dichotomisation artificielle de traits continus (E vs. I, T vs. F, etc.)
- Fiabilité test-retest modeste : ~50% des personnes obtiennent un type différent à 5 semaines
- Les 16 types ne couvrent pas mieux la personnalité que les Big Five
- Faux sentiment de précision ("Je suis INFJ") alors que le modèle est binaire

**Ce qui est correct dans le MBTI** : Les 4 dichotomies correspondent approximativement à des dimensions Big Five réelles (E/I ≈ Extraversion, T/F ≈ Agréabilité, J/P ≈ Conscienciosité).

**Verdict CPL** : Optionnel. Si intégré, afficher le MBTI comme un **outil de communication** (l'utilisateur connaît souvent son type) mais se fier aux Big Five pour le paramétrage réel d'ALFRED.

---

### 10. DISC ★★☆☆☆ — Optionnel

**Fondateur** : Marston (1928), commercialisé en version actuelle dans les années 70

**Les 4 profils** :
- **D (Dominant)** : direct, résultats, décision rapide
- **I (Influent)** : enthousiaste, sociable, optimiste
- **S (Stable)** : patient, fiable, coopératif
- **C (Consciencieux)** : précis, analytique, qualité

**Avantages** : Simple, populaire en entreprise, facile à comprendre.  
**Limites** : 4 profils seulement — granularité très faible. Pas de norme psychométrique internationale stable.

**Verdict CPL** : Optionnel. Moins utile que le Big Five pour le paramétrage d'ALFRED. Peut être affiché à titre informatif si l'utilisateur le connaît (saisie manuelle de son profil).

---

### 11. Ennéagramme ★☆☆☆☆ — EXCLU

**Origine** : Traditions ésotériques (Gurdjieff, Ichazo), vulgarisé par Riso & Hudson

**Pourquoi exclu** :
- **Aucune validation psychométrique** sérieuse (pas de peer-review, pas de normalisation)
- Structure arbitraire (pourquoi 9 types et pas 7 ou 12 ?)
- Fiabilité très faible (le type varie selon les versions du test)
- Les "ailes" et "niveaux de développement" ajoutent de la complexité sans valeur ajoutée prouvée

**Ce qui est vrai** : L'ennéagramme capture certaines réalités de la personnalité humaine, mais elles sont mieux et plus précisément mesurées par le Big Five ou HEXACO.

**Verdict CPL** : Exclu du système de scoring. Peut être mentionné dans un contexte culturel (si l'utilisateur dit "je suis un 4 ennéagramme") mais pas utilisé pour paramétrer ALFRED.

---

## Roadmap d'intégration recommandée

### V1 — LIVRÉ
- ✅ TIPI (Big Five — 10 items)
- ✅ TEIQue-SF (IE — 15 items)
- ✅ PVQ-21 (Schwartz — 21 items)
- ✅ rMEQ (Chronotype — 5+10 items)
- ✅ CD-RISC-10 + PSS-4 (Résilience/Stress — 14 items)
- ✅ RIASEC Holland (18 items)
- ✅ UWES-9 + burnout (12 items)
- ✅ TKI-inspiré (Communication/Conflit)
- ✅ SDT (Motivations — 18 items)
- ✅ AssessFirst (résultats externes)

### V2 — À INTÉGRER
- 📋 **HEXACO-24** — priorité haute (apporte Honnêteté-Humilité)
- 📋 **BFI-2-S (30 items)** — pour remplacer TIPI si plus de granularité souhaitée
- 📋 MBTI auto-déclaratif (optionnel — saisie manuelle type connu)
- 📋 DISC auto-déclaratif (optionnel — saisie manuelle profil connu)

### JAMAIS
- ❌ MMPI / PAI (instruments cliniques)
- ❌ Hogan / SOSIE / 16PF complet (licences propriétaires)
- ❌ Ennéagramme (absence de validation scientifique)

---

## Proposition de questionnaire HEXACO-24 pour ALFRED

Le HEXACO-24 (24 items, 4 par dimension, Likert 5) peut être intégré comme `09_hexaco_personnalite.md`.

**Durée estimée** : 8-10 min en format conversationnel  
**Périodicité** : Annuelle (traits très stables)  
**Impact sur ALFRED** : Surtout la dimension H (Honnêteté-Humilité) → style de communication  
**Fichier** : `data/profile/questionnaires/09_hexaco_personnalite.md` (à créer)  
**Source** : Ashton & Lee (2009), International Journal of Personality Psychology — domaine public

---

*Document créé le 2026-06-16 — Cognitive Products Lab*
