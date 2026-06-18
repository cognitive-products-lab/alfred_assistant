# RACI — Rôles et Responsabilités Sécurité

> **Référence :** ISO/IEC 27001:2022 — Contrôle A.5.2  
> **Version :** 1.0 — 2026-06-18  
> **Propriétaire :** Cognitive Products Lab — Céline Darras  
> **Statut :** Approuvé

---

## 1. Légende RACI

| Lettre | Rôle | Définition |
|---|---|---|
| **R** | Responsible | Réalise l'activité |
| **A** | Accountable | Approuve et est responsable final |
| **C** | Consulted | Consulté (communication bilatérale) |
| **I** | Informed | Informé (communication unilatérale) |

---

## 2. Intervenants CPL

| Sigle | Rôle | Titulaire |
|---|---|---|
| **DG** | Directrice Générale / Fondatrice | Céline Darras |
| **RSSI** | Responsable Sécurité SI | Céline Darras (double rôle V1) |
| **DEV** | Développeur principal | Céline Darras (double rôle V1) |
| **SYS** | Système ALFRED | Module automatique |

*En phase V1, Céline Darras cumule DG + RSSI + DEV. Le RACI reflète les responsabilités conceptuelles pour la gouvernance formelle et la montée en charge.*

---

## 3. RACI — Activités de Sécurité

### Gouvernance et Politique

| Activité | DG | RSSI | DEV | SYS |
|---|---|---|---|---|
| Approbation politique SMSI | **A** | R | I | — |
| Révision annuelle SMSI | A | **R** | C | — |
| Définition objectifs sécurité | **A** | R | C | — |
| Revue de direction | **A/R** | R | I | — |
| Gestion des non-conformités | A | **R** | C | — |

### Contrôle d'Accès

| Activité | DG | RSSI | DEV | SYS |
|---|---|---|---|---|
| Création / suppression comptes | A | **R** | — | — |
| Attribution des rôles (RBAC) | A | **R** | C | — |
| Activation / révocation MFA | A | **R** | — | SYS |
| Revue des droits d'accès | A | **R** | — | — |

### Gestion des Incidents

| Activité | DG | RSSI | DEV | SYS |
|---|---|---|---|---|
| Détection incidents | I | I | — | **R** |
| Triage et qualification | A | **R** | — | C |
| Containment | A | **R** | C | — |
| Notification CNIL / ANSSI | **A/R** | C | — | — |
| Remédiation technique | A | R | **R** | — |
| Analyse post-incident | A | **R** | C | — |
| Clôture et archivage | A | **R** | — | — |

### Cryptographie et Clés

| Activité | DG | RSSI | DEV | SYS |
|---|---|---|---|---|
| Politique cryptographique | A | **R** | C | — |
| Rotation des clés | A | **R** | — | SYS |
| Audit clés cryptographiques | A | **R** | — | — |

### Développement Sécurisé

| Activité | DG | RSSI | DEV | SYS |
|---|---|---|---|---|
| Revue de code sécurité | A | C | **R** | — |
| Tests de sécurité automatisés | I | A | **R** | SYS |
| Analyse vulnérabilités | A | R | **R** | — |
| Mise à jour dépendances | A | C | **R** | — |

### Continuité d'Activité

| Activité | DG | RSSI | DEV | SYS |
|---|---|---|---|---|
| Définition PCA | **A** | R | C | — |
| Sauvegardes automatiques | I | A | R | **SYS** |
| Tests de restauration | A | **R** | C | — |
| Activation PCA | **A/R** | R | C | — |

### Conformité Réglementaire

| Activité | DG | RSSI | DEV | SYS |
|---|---|---|---|---|
| Veille réglementaire | A | **R** | I | — |
| Conformité RGPD | **A** | R | C | — |
| Conformité ISO 27001 | A | **R** | C | — |
| Audits de conformité | **A** | R | C | — |
| Droits des personnes (Art.15-21) | **A** | R | **R** | SYS |

---

## 4. Révision

| Version | Date | Auteur | Modification |
|---|---|---|---|
| 1.0 | 2026-06-18 | Céline Darras | Création RACI formel — conformité ISO A.5.2 |

> **Cognitive Products Lab — Confidentiel interne**
