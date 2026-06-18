# Chantier V2 — Profil ARTHUR (enfants < 16 ans)

> Planifié après livraison du système de profilage ALFRED/CPL (V1).
> Créé le 2026-06-16.

---

## Objectif

Créer un système de profilage adapté aux enfants de moins de 16 ans pour
ARTHUR, version simplifiée et sécurisée du système ALFRED, avec contrôle
parental intégré.

---

## Deux composantes

### 1. Profil enfant (simplifié)

Système semblable au profil adulte mais radicalement adapté :

- **Questions simplifiées** : formulation adaptée à l'âge (vocabulaire,
  longueur, concepts concrets), avec pictogrammes/emojis possibles
- **Moins de choix** : échelles de 3 points max (pas bien / moyen / bien),
  ou choix binaires pour les plus jeunes
- **Questionnaires courts** : max 5 min par questionnaire
- **Dimensions réduites** : pas de RIASEC/burnout/valeurs Schwartz,
  focus sur bien-être émotionnel, style d'apprentissage simplifié,
  besoins de soutien, centres d'intérêt
- **Tranches d'âge** : prévoir au minimum 2 modes (6-11 ans / 12-15 ans)
- **Consentement adapté** : le parent valide chaque questionnaire avant
  passation

### 2. Contrôle parental

Système de paramétrage parent sécurisé et rassurant :

- **Interface parent séparée** : accès protégé par mot de passe parent
  (distinct du profil enfant)
- **Paramètres configurables** :
  - Sujets autorisés / interdits
  - Niveau de filtre de contenu (strict / standard)
  - Plages horaires d'utilisation
  - Durée max de session
  - Accès aux logs de conversation (résumés, pas verbatim)
  - Validation parentale obligatoire pour certaines fonctions
- **Mode supervisé** : parent peut voir en temps réel (opt-in)
- **Alertes** : signalement automatique si ARTHUR détecte un contenu
  préoccupant (bien-être, sécurité)
- **RGPD mineurs** : conformité art. 8 RGPD (consentement parental
  obligatoire < 16 ans), principe de minimisation des données, droit
  d'effacement renforcé
- **Audit trail** : journal chiffré des accès et modifications de
  paramètres parent

---

## Fichiers à créer (V2)

```
data/profile/
└── arthur/
    ├── schema/
    │   ├── dimensions_enfant_schema.json
    │   ├── alfred_mapping_arthur.json
    │   └── controle_parental_schema.json
    ├── questionnaires/
    │   ├── enfant_6_11/
    │   │   ├── bien_etre_emotionnel.md
    │   │   ├── centres_interet.md
    │   │   └── style_apprentissage.md
    │   └── enfant_12_15/
    │       ├── bien_etre_emotionnel.md
    │       ├── centres_interet.md
    │       ├── style_apprentissage.md
    │       └── relations_sociales.md
    ├── controle_parental/
    │   ├── parametres_parent_template.json
    │   └── journal_acces_template.json
    └── scoring/
        ├── scoring_keys_arthur.json
        └── answers_template_arthur.json

src/core/
└── arthur_profile_analyzer.py

docs/profil_systeme/
├── conception_arthur.md
├── securite_mineurs_rgpd.md
└── guide_parent.md
```

---

## Notes critiques

- Ce chantier dépend de la V1 (système ALFRED/CPL) — ne pas démarrer
  avant que le système adulte soit stable et validé.
- Prévoir un avis professionnel de santé pédiatrique avant finalisation
  des questionnaires enfant (contrainte déjà identifiée dans ALFRED_CONTEXT.md).
- Les questionnaires enfant doivent être validés par des professionnels
  (psychologue spécialisé enfance) avant tout usage réel.
- Le contrôle parental est non négociable légalement (RGPD art. 8,
  DSA, COPPA si usage international envisagé).

---

*À reprendre après validation et merge de la PR #10 (système profil adulte).*
