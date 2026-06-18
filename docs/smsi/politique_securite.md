# Politique de Sécurité du Système d'Information (SMSI)
## Cognitive Products Lab — ALFRED

> **Référence :** ISO/IEC 27001:2022 — Contrôle A.5.1  
> **Version :** 1.0 — 2026-06-18  
> **Approbation :** Céline Darras — Fondatrice / Directrice Générale  
> **Statut :** Approuvé

---

## 1. Déclaration d'intention

Cognitive Products Lab (CPL) s'engage à protéger la confidentialité, l'intégrité et la disponibilité des informations traitées dans le cadre du projet ALFRED. La sécurité de l'information est une priorité stratégique fondamentale, indissociable de notre mission de développer une IA personnelle fiable, éthique et souveraine.

**Approuvé par :** Céline Darras — Fondatrice, Cognitive Products Lab  
**Date d'approbation :** 2026-06-18

---

## 2. Périmètre du SMSI

Le SMSI couvre :
- L'infrastructure ALFRED (PC Alfred — Minisforum MS-S1, réseau domestique sécurisé)
- Les données personnelles des utilisateurs ALFRED
- Les systèmes de développement, de test et de production
- Les outils et services tiers (OpenAI API)
- Le code source et la propriété intellectuelle CPL

---

## 3. Objectifs de sécurité

### 3.1 Confidentialité
- Chiffrement AES-256 (Fernet) de toutes les données sensibles au repos
- Classification des données C1→C4 (Public → Secret)
- Contrôle d'accès basé sur les rôles (RBAC) + MFA obligatoire
- Aucun partage de données sans base légale documentée

### 3.2 Intégrité
- Journalisation sécurisée et immuable de toutes les actions (`audit_trail.py`)
- Détection des anomalies comportementales (`behavioral_detector.py`)
- Tests de sécurité automatisés (651 tests A+)
- Gestion des versions et contrôle des modifications (Git)

### 3.3 Disponibilité
- Sauvegardes automatiques régulières
- Plan de continuité d'activité (PCA) documenté
- Rotation des clés cryptographiques planifiée

---

## 4. Principes directeurs

1. **Zero Trust** : Aucune confiance implicite — vérification systématique de chaque accès
2. **Privacy by Design** : Protection des données intégrée dès la conception
3. **Moindre privilège** : Accès limités au strict nécessaire à chaque rôle
4. **Défense en profondeur** : Couches multiples de protection (réseau, OS, application, données)
5. **Amélioration continue** : Revue annuelle du SMSI, audits internes, leçons apprises

---

## 5. Rôles et responsabilités

| Rôle | Responsable | Missions |
|---|---|---|
| Directrice Générale / Fondatrice | Céline Darras | Approbation politique, décisions stratégiques sécurité |
| Responsable Sécurité (RSSI) | Céline Darras | Implémentation, monitoring, incidents, audits |
| Développeur | Céline Darras | Sécurité du code, tests, intégration |
| DPO de fait | Céline Darras | Conformité RGPD, droits des personnes |

*Note : En phase V1 (organisation mono-fondatrice), Céline Darras cumule ces rôles. La séparation des rôles sera mise en œuvre lors du recrutement.*

---

## 6. Cadre réglementaire

CPL respecte et s'engage à maintenir la conformité avec :
- **RGPD** (Règlement UE 2016/679) — données personnelles
- **ISO/IEC 27001:2022** — management de la sécurité de l'information
- **EU AI Act** (Règlement UE 2024/1689) — IA responsable
- **NIS2** (Directive UE 2022/2555) — sécurité réseaux et SI

---

## 7. Sanctions et non-conformités

Tout manquement à cette politique fait l'objet d'une action corrective documentée dans `docs/smsi/actions_correctives.md`. Les violations graves sont traitées selon la procédure incidents `procedure_incidents.md`.

---

## 8. Révision

Cette politique est révisée annuellement et à chaque changement organisationnel ou réglementaire majeur.

| Version | Date | Auteur | Modification |
|---|---|---|---|
| 1.0 | 2026-06-18 | Céline Darras | Création — conformité ISO A.5.1 |

> **Cognitive Products Lab — Confidentiel interne**
