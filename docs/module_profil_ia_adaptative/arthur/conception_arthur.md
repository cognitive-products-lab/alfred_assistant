# Conception ARTHUR V2 — Profil enfant & Contrôle parental
## Module Profil IA Adaptative — Cognitive Products Lab

> Version 0.1 — 2026-06-16 — CHANTIER (planifié après livraison V1 adulte)  
> Référence réglementaire : RGPD art.8 + LIL art.45 + DSA + recommandations CNIL mineurs

---

## Avertissement

**Ce chantier ne démarrera qu'après :**
1. Validation et merge du PR profil adulte (PR #10)
2. Revue par un professionnel de santé pédiatrique
3. Consultation CNIL recommandée (saisine préventive)
4. Avis juridique sur le cadre de consentement parental

---

## 1. Différences fondamentales ALFRED vs ARTHUR

| Aspect | ALFRED (adulte) | ARTHUR (enfant) |
|--------|----------------|-----------------|
| **Âge cible** | ≥ 18 ans | 6-15 ans (< seuil LIL art.45) |
| **Consentement** | Utilisateur lui-même | Représentant légal OBLIGATOIRE |
| **Données** | Art.9 RGPD (données sensibles) | Art.9 + données mineur (protection renforcée) |
| **Profil** | Psychométrique scientifique complexe | Simplifié, adapté à l'âge |
| **Instruments** | Big Five, PSS, UWES, etc. | Questionnaires pédagogiques validés cliniquement |
| **Scoring** | 0-100 normalisé adulte | Pas de scoring clinique — descriptif uniquement |
| **Accès profil** | Utilisateur seul | Représentant légal + enfant (séparé) |
| **Transfert hors UE** | Non | NON ABSOLU |
| **HDS** | Non requis | Requis si données de santé collectées |

---

## 2. Cadre réglementaire spécifique

### RGPD art. 8 + LIL art. 45 (France)
- **Seuil français** : 15 ans (non 16 ans comme le RGPD européen de base)
- **En-dessous de 15 ans** : consentement écrit du représentant légal OBLIGATOIRE
- **Entre 15 et 18 ans** : l'enfant peut consentir seul pour les traitements numériques courants, mais CPL applique la règle du niveau le plus strict → consentement parental requis jusqu'à 18 ans pour les données sensibles

### RGPD art. 9 spécial mineur
Les données de bien-être émotionnel d'un enfant relèvent de l'art.9 RGPD (catégories spéciales) si elles incluent :
- État de santé ou santé mentale
- Données biométriques (voix, etc.)
- Données de localisation régulière

### DSA (Digital Services Act) — art. 28
- Interdit le ciblage publicitaire des mineurs
- Oblige la déclaration de l'âge avant accès aux services
- ARTHUR doit implémenter une vérification d'âge du représentant légal

### Recommandations CNIL mineurs (2021)
- Minimisation stricte des données
- Durée de conservation limitée
- Interface adaptée à l'âge (lisible par l'enfant selon sa tranche d'âge)
- Droit à l'oubli renforcé à la majorité

---

## 3. Tranches d'âge et questionnaires adaptés

### Tranche 6-11 ans — "Poussin"

**Principes** :
- Questions très courtes, vocabulaire simple, pictos visuels
- Échelles visuelles (smiley, couleurs) plutôt que Likert numérique
- Maximum 10-12 questions par session
- Durée ≤ 8 minutes
- Co-passation avec parent recommandée

**Dimensions mesurées** :
- Humeur générale (smiley scale 3-5 niveaux)
- Centres d'intérêt (choix parmi pictos : musique, sport, dessins, etc.)
- Style d'apprentissage simplifié (visual / auditif / kinesthésique)
- Besoin d'aide (jamais / parfois / souvent / toujours)

**Instruments de référence** :
- Faces Pain Scale (émotion) — adapté
- Strengths and Difficulties Questionnaire (SDQ) — version parent
- McKnight Fear Survey (anxiété enfant) — items sélectifs
- KINDL-R (qualité de vie enfant 4-7 ans)

### Tranche 12-15 ans — "Cadet"

**Principes** :
- Questions un peu plus longues, registre ado
- Échelles Likert 5 acceptables
- Maximum 15-18 questions par session
- Durée ≤ 12 minutes
- Passation autonome recommandée (parents voient résumé, pas verbatim)

**Dimensions mesurées** :
- Bien-être émotionnel (adapté KIDSCREEN-10)
- Motivation scolaire et apprentissage (SDT simplifié)
- Style de communication (4 modes vs 5 adulte)
- Résilience simplifiée (5 items adapté BRS)
- Gestion du stress (5 items adapté PSS pour ados)

**Instruments de référence** :
- KIDSCREEN-10 (bien-être enfant 8-18 ans) — gratuit
- SDQ (Strengths and Difficulties Questionnaire) — validé France
- RCADS (anxiété/dépression ado) — version courte 25 items
- Brief Resilience Scale (BRS) adaptée ado

---

## 4. Système de contrôle parental

### Architecture

```
                    ARTHUR (interface enfant)
                           │
                           │ accès limité selon profil âge
                           │
                    ARTHUR Core
                           │
                           │ authentification séparée
                           │
                    Console parentale
                    (interface distincte)
                           │
                    Authentification forte
                    (mot de passe distinct du PIN enfant)
```

### Fonctionnalités console parentale V1

| Fonctionnalité | Description |
|----------------|-------------|
| **Voir le résumé du profil** | Vue descriptive (pas les scores bruts), dans un langage accessible |
| **Configurer les limites** | Durée max session, sujets autorisés/restreints |
| **Lire les résumés de sessions** | Thèmes abordés (pas le verbatim) |
| **Gérer le consentement** | Accord/refus par type de collecte |
| **Exporter les données** | Export JSON chiffré (droit de portabilité) |
| **Supprimer le profil** | Effacement complet avec confirmation 2 étapes |
| **Alertes** | Notification si ARTHUR détecte un sujet sensible (bullying, etc.) |

### Sécurité console parentale

- **Authentification** : mot de passe distinct du code PIN enfant
- **Session** : timeout automatique à 10 min d'inactivité
- **Accès** : console parentale inaccessible depuis l'interface enfant
- **Logs** : toute action parentale enregistrée dans l'audit trail
- **Chiffrement** : même Fernet AES-128-CBC que ALFRED

---

## 5. Données — Restrictions spéciales

### Ce qu'ARTHUR peut collecter

| Donnée | Base juridique | Conditions |
|--------|---------------|------------|
| Prénom (pseudonyme) | Contrat | Pas de nom complet |
| Tranche d'âge | Contrat | Jamais la date de naissance complète |
| Centres d'intérêt | Consentement parental | Opt-in explicite |
| Humeur auto-reportée | Consentement parental | Pas diagnostique |
| Style d'apprentissage | Contrat | À des fins pédagogiques uniquement |

### Ce qu'ARTHUR NE peut PAS collecter

- ❌ Données biométriques (voix en dehors du STT local, image)
- ❌ Localisation précise
- ❌ Données de santé sans HDS (hébergement données de santé)
- ❌ Données comportementales fins (tracking micro-comportements)
- ❌ Tout contenu permettant d'identifier l'enfant indirectement

### Durée de conservation spéciale mineur

Jusqu'aux 18 ans de l'enfant, puis :
- Option A : transfert du profil à l'enfant devenu majeur (avec son consentement)
- Option B : suppression automatique (choix par défaut)
- Les logs d'audit : 5 ans maximum

---

## 6. Structure des fichiers ARTHUR (à créer)

```
data/arthur/
├── arthur_profile_template.json          ← Template profil enfant (public)
├── questionnaires/
│   ├── poussins/                         ← Tranche 6-11 ans
│   │   ├── A01_humeur_emotion.md
│   │   ├── A02_centres_interet.md
│   │   └── A03_style_apprentissage.md
│   └── cadets/                           ← Tranche 12-15 ans
│       ├── A11_bien_etre_kidscreen.md
│       ├── A12_motivation_scolaire.md
│       ├── A13_resilience_simplifiee.md
│       └── A14_communication_ados.md
├── scoring/
│   └── arthur_scoring_keys.json          ← Clés simplifiées (descriptif)
└── controle_parental/
    ├── schema_controle_parental.json     ← Structure config parentale
    └── parental_dashboard_template.json  ← Template interface parent

docs/profil_systeme/arthur/
├── conception_arthur.md                  ← Ce fichier
├── securite_mineur.md                    ← Mesures spécifiques données mineur
└── conformite_arthur.md                  ← RGPD art.8 + HDS + DSA
```

---

## 7. Avis professionnels requis avant V2

Avant toute mise en production d'ARTHUR :

1. **Pédiatre ou pédopsychiatre** : valider la pertinence des questionnaires par tranche d'âge, s'assurer qu'aucun item ne peut provoquer de détresse psychologique chez un enfant
2. **Juriste spécialisé données mineurs** : confirmer la conformité RGPD art.8 + LIL art.45 + DSA + CNIL
3. **Ergonome ou UX spécialisé enfants** : valider l'interface de passation pour chaque tranche d'âge
4. **CNIL (consultation préventive)** : recommandée pour un traitement de données sensibles de mineurs (art.35 AIPD + démarche proactive)

---

## 8. Roadmap ARTHUR

```
2026 Q4 — Finalisation spec détaillée + avis pédiatre + avis juridique
2027 Q1 — Développement interface enfant (Poussin d'abord)
2027 Q1 — Développement console parentale V1
2027 Q2 — Tests utilisateurs parents + enfants (lab tests)
2027 Q2 — AIPD T004 (obligatoire avant toute mise en production)
2027 Q3 — Beta test fermé (20-30 familles)
2027 Q4 — Production ARTHUR (si feu vert éthique + légal)
```

---

*Document créé le 2026-06-16 — Cognitive Products Lab*  
*Révision : à chaque étape du chantier*
