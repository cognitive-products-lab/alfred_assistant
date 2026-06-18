# Cartographie des données — Cognitive Products Lab
## Data Map complet — ALFRED, ALFRED CPL, ARTHUR

> Version 1.0 — 2026-06-16  
> Référence réglementaire : RGPD art. 30 (registre), art. 32 (sécurité), art. 35 (AIPD)  
> Mise à jour : à chaque nouveau traitement ou modification significative

---

## 1. Architecture globale des flux de données

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         ÉCOSYSTÈME CPL — VUE GLOBALE                        │
└─────────────────────────────────────────────────────────────────────────────┘

┌──────────────────────┐     ┌──────────────────────┐     ┌──────────────────┐
│   APPAREIL LOCAL      │     │   SERVEURS CPL (FR)   │     │  SERVICES TIERS  │
│   (utilisateur)       │     │   (opt-in uniquement) │     │  (si applicable) │
│                       │     │                       │     │                  │
│  ┌─────────────────┐  │     │  ┌─────────────────┐  │     │  ┌────────────┐  │
│  │ Profil psy.     │  │ ──► │  │ Métriques       │  │     │  │ LLM API    │  │
│  │ (chiffré local) │  │     │  │ anonymisées     │  │     │  │ (futur)    │  │
│  └─────────────────┘  │     │  └─────────────────┘  │     │  └────────────┘  │
│  ┌─────────────────┐  │     │  ┌─────────────────┐  │     │  ┌────────────┐  │
│  │ Conversations   │  │ ✗   │  │ Logs erreurs    │  │     │  │ STT/TTS    │  │
│  │ (local only)    │  │     │  │ anonymisés      │  │     │  │ (futur)    │  │
│  └─────────────────┘  │     │  └─────────────────┘  │     │  └────────────┘  │
│  ┌─────────────────┐  │     │  ┌─────────────────┐  │     │                  │
│  │ Mémoire ALFRED  │  │ ✗   │  │ Feedback opt-in │  │     │                  │
│  │ (local only)    │  │     │  └─────────────────┘  │     │                  │
│  └─────────────────┘  │     │                       │     │                  │
│  ┌─────────────────┐  │     │                       │     │                  │
│  │ Clés Fernet     │  │ ✗   │                       │     │                  │
│  │ (local only)    │  │     │                       │     │                  │
│  └─────────────────┘  │     │                       │     │                  │
└──────────────────────┘     └──────────────────────┘     └──────────────────┘

Légende :
──►  Flux autorisé (opt-in explicite + anonymisation)
 ✗   Flux interdit (données ne quittent jamais l'appareil)
```

---

## 2. Inventaire complet des données

### 2.1 Données résidant exclusivement sur l'appareil utilisateur

| ID | Donnée | Catégorie | Sensibilité | Chiffrement | Accès |
|----|--------|-----------|-------------|-------------|-------|
| D01 | Profil psychologique (scores questionnaires) | Profil psychologique | CRITIQUE — art. 9 RGPD | Fernet (AES-128-CBC) | Utilisateur seul |
| D02 | Réponses brutes aux questionnaires | Profil psychologique | CRITIQUE — art. 9 RGPD | Fernet | Utilisateur seul |
| D03 | Historique des conversations ALFRED | Données conversation | CRITIQUE | Fernet | Utilisateur seul |
| D04 | Mémoire adaptative ALFRED (préférences apprises) | Profil comportemental | ÉLEVÉE | Fernet | Utilisateur seul |
| D05 | Paramètres ALFRED dérivés du profil | Configuration | CONFIDENTIELLE | Fernet | Utilisateur seul |
| D06 | Clés de chiffrement Fernet | Sécurité | CRITIQUE | Stockage sécurisé séparé | Utilisateur seul |
| D07 | Journal d'accès local (audit trail local) | Métadonnées | CONFIDENTIELLE | Fernet | Utilisateur seul |
| D08 | Données biométriques si voix activée (empreinte vocale) | Biométrique — art. 9 RGPD | CRITIQUE | Fernet | Utilisateur seul |
| D09 | Données de santé (ARTHUR) si collectées | Santé — art. 9 RGPD | CRITIQUE | Fernet + HDS obligatoire | Utilisateur + parent légal |
| D10 | Profil enfant ARTHUR (scores simplifiés) | Données mineur | CRITIQUE | Fernet | Parent légal seul |
| D11 | Paramètres contrôle parental ARTHUR | Configuration parentale | ÉLEVÉE | Fernet | Parent légal seul |

### 2.2 Données pouvant être transmises à CPL (opt-in uniquement)

| ID | Donnée | Conditions | Anonymisation | Finalité CPL | Rétention CPL |
|----|--------|-----------|---------------|--------------|---------------|
| D12 | Métriques d'usage agrégées | Opt-in explicite + renouvellement annuel | Complète + agrégation | Amélioration produit | 24 mois |
| D13 | Logs d'erreurs techniques anonymisés | Opt-in + consentement séparé | Pseudonymisation | Débogage, stabilité | 12 mois |
| D14 | Feedback utilisateur volontaire | Opt-in par acte positif (bouton feedback) | Pseudonymisation | Amélioration UX | 36 mois |
| D15 | Statistiques de performance (latence, temps réponse) | Opt-in | Agrégation, pas d'ID | Optimisation technique | 12 mois |
| D16 | Rapport de crash | Opt-in séparé | Pseudonymisation, nettoyage données perso | Correction bugs | 6 mois |

### 2.3 Données ne pouvant JAMAIS quitter l'appareil utilisateur

| ID | Donnée | Justification |
|----|--------|---------------|
| D01–D11 | Voir tableau 2.1 | Données personnelles sensibles, local-first non négociable |
| D17 | Contenu des messages échangés avec ALFRED | Confidentialité absolue des échanges |
| D18 | Identité réelle associée au profil psychologique | Pseudonymisation non réversible par CPL |
| D19 | Réponses aux questionnaires psychologiques brutes | Art. 9 RGPD — consentement insuffisant pour tout transfert |
| D20 | Données vocales brutes | Biométrique — protection maximale |

---

## 3. Flux de données détaillés

### 3.1 Flux local (appareil utilisateur)

```
Utilisateur
    │
    ▼ (saisie texte / voix)
┌─────────────────────────────────────────────────────┐
│                    ALFRED (local)                    │
│                                                      │
│  Input → STT (local) → Compréhension intention      │
│       → Récupération mémoire (D04, chiffré)         │
│       → Récupération profil (D05, chiffré)          │
│       → Moteur comportemental (alfred_behavior_engine)│
│       → Génération réponse (LLM local)              │
│       → TTS (local) → Output                        │
│       → Sauvegarde conversation (D03, chiffré)      │
│       → Mise à jour mémoire (D04, chiffré)          │
└─────────────────────────────────────────────────────┘
    │
    ▼ (opt-in uniquement)
Métriques anonymisées → Chiffrement transit (TLS 1.3) → Serveur CPL
```

### 3.2 Flux de profilage psychologique

```
ALFRED (session questionnaire)
    │
    ▼ Question par question (conversationnel)
Réponse utilisateur → Sauvegarde immédiate chiffrée (D02)
    │
    ▼ (session complète ou partielle)
ProfileAnalyzer.compute_scores()
    │
    ▼
Scores normalisés 0-100 → alfred_mapping_matrix → Paramètres ALFRED
    │                                                      │
    ▼                                                      ▼
user_profile.json (scores) ◄──────────────────── alfred_derived_params
(chiffré, local)
```

### 3.3 Flux contrôle parental ARTHUR

```
Parent légal (authentification forte)
    │
    ▼
Interface Contrôle Parental (séparée de l'interface enfant)
    │
    ├── Lecture profil enfant (D10)
    ├── Modification paramètres (D11)
    ├── Consultation logs résumés (non verbatim)
    └── Tout acte tracé dans audit_trail (D07)
```

---

## 4. Cartographie des lieux de stockage

| Lieu | Données stockées | Chiffrement | Sauvegarde | Accès CPL |
|------|-----------------|-------------|------------|-----------|
| **Appareil utilisateur** (SSD/HDD local) | D01-D11, D17-D20 | Fernet (repos) | Sauvegarde locale chiffrée uniquement | ❌ JAMAIS |
| **Serveur CPL — France** | D12-D16 (opt-in) | AES-256 (repos) + TLS 1.3 (transit) | Réplication géographique FR | ✅ Équipes autorisées uniquement |
| **Mémoire vive (RAM)** | Données en cours de traitement | Jamais persistées non chiffrées | N/A | ❌ |
| **Logs système** | Événements techniques (sans données perso) | Chiffrement selon sensibilité | 90 jours | ✅ RSSI |

---

## 5. Durées de rétention

| Catégorie | Lieu | Durée | Déclencheur suppression |
|-----------|------|-------|------------------------|
| Profil psychologique (D01-D02) | Local | Durée vie du compte + 3 mois grâce | Demande effacement / fermeture compte |
| Conversations (D03) | Local | Configurable par utilisateur (défaut : 12 mois glissants) | Expiration / demande / fermeture compte |
| Mémoire adaptative (D04-D05) | Local | Durée vie du compte | Demande réinitialisation / fermeture compte |
| Métriques anonymisées (D12) | Serveur CPL | 24 mois | Expiration automatique |
| Logs erreurs (D13) | Serveur CPL | 12 mois | Expiration automatique |
| Feedback (D14) | Serveur CPL | 36 mois | Expiration / demande d'effacement |
| Logs de crash (D16) | Serveur CPL | 6 mois | Expiration automatique |
| Audit trail local (D07) | Local | 5 ans (traçabilité légale) | Fermeture compte + délai légal |

---

## 6. Responsabilités par donnée

| Donnée | Responsable de traitement | Responsable opérationnel | Sous-traitants |
|--------|--------------------------|-------------------------|----------------|
| D01-D11 (local) | CPL / Céline Rousselot | Utilisateur (gardien physique) | Aucun |
| D12-D15 (serveur CPL) | CPL / Céline Rousselot | RSSI CPL | Hébergeur FR (DPA signé) |
| D16 (crash logs) | CPL / Céline Rousselot | Équipe technique | Hébergeur FR (DPA signé) |

---

## 7. Registre des accès autorisés (par rôle)

| Rôle | D01-D11 (local) | D12-D15 (serveur) | Audit trail |
|------|:---------------:|:-----------------:|:-----------:|
| Utilisateur | ✅ Lecture + écriture | ✅ Ses propres données | ✅ Lecture |
| Parent légal (ARTHUR) | ✅ Profil enfant (D10-D11) | ✅ Ses propres données | ✅ Lecture (résumés) |
| Équipe produit CPL | ❌ | ✅ Agrégées/anonymisées | ❌ |
| Data scientist CPL | ❌ | ✅ Anonymisées uniquement | ❌ |
| RSSI CPL | ❌ | ✅ Logs techniques | ✅ Serveur CPL |
| DPO CPL | ❌ (droits théoriques) | ✅ Métadonnées registre | ✅ Complet |
| Autorités légales | Sur réquisition judiciaire uniquement | Sur réquisition judiciaire | Sur réquisition judiciaire |

---

## 8. Points de risque identifiés

| Risque | Probabilité | Impact | Mesure d'atténuation | Responsable |
|--------|------------|--------|---------------------|-------------|
| Perte appareil utilisateur | Moyenne | Critique | Chiffrement intégral Fernet, clé séparée | RSSI |
| Compromission clé Fernet | Faible | Critique | Rotation des clés, stockage sécurisé isolé | RSSI |
| Fuite données serveur CPL | Faible | Élevé | Anonymisation avant collecte, DPA hébergeur | RSSI |
| Accès non autorisé ARTHUR par tiers | Faible | Critique | Auth forte parent, séparation profils | Équipe produit |
| Re-identification données "anonymisées" | Faible | Élevé | Tests de re-identification avant mise en prod | DPO |
| Perte intégrité audit trail | Très faible | Élevé | Audit trail immuable, hachage chaîné | RSSI |

---

*Document créé le 2026-06-16 — Cognitive Products Lab*  
*Révision annuelle obligatoire ou à chaque modification de l'architecture de données*
