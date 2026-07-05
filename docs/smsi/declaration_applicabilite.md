<!--
============================================================
PROJECT  : ALFRED / Cognitive Products Lab
BLOCK    : B20 — Sécurité, Gouvernance & Conformité
DOCUMENT : Déclaration d'Applicabilité (DdA) — SMSI
TYPE     : Documentation SMSI
REF      : ISO/IEC 27001:2022 — A.5.36
VERSION  : V1.0
CREATED  : 2026-06-18
UPDATED  : 2026-06-18
AUTHOR   : Céline Darras — Cognitive Products Lab
STATUS   : Approuvé
============================================================
-->
# Déclaration d'Applicabilité (DdA) — SMSI ISO 27001:2022

> **Référence :** ISO/IEC 27001:2022 — Contrôle A.5.36  
> **Version :** 1.0 — 2026-06-18  
> **Approbation :** Céline Darras — Fondatrice / Directrice Générale  
> **Statut :** Approuvé

---

## 1. Contexte

**Organisation :** Cognitive Products Lab (CPL)  
**Système :** ALFRED — Assistant IA personnel  
**Périmètre SMSI :** Infrastructure ALFRED (PC Alfred, réseau, données, code source)  
**Version ISO :** ISO/IEC 27001:2022

---

## 2. Périmètre formel du SMSI

Le SMSI couvre :
- Les actifs informationnels listés dans `inventaire_actifs.json`
- L'infrastructure physique : PC Alfred (Minisforum MS-S1), réseau domestique sécurisé, stockage LaCie
- Le personnel : Céline Darras (seule collaboratrice en V1)
- Les processus : développement, exploitation, maintenance, incidents, conformité
- Les données personnelles des utilisateurs ALFRED

**Exclusions :** Infrastructure cloud tiers (OpenAI API) — couvert par DPA (`dpa_sous_traitants.md`)

---

## 3. Déclaration d'applicabilité — Contrôles ISO 27001:2022

| Ref. ISO | Contrôle | Applicable | Justification | Statut |
|---|---|---|---|---|
| A.5.1 | Politiques de sécurité | ✅ Oui | Gouvernance essentielle | ✅ Atteint |
| A.5.2 | Rôles et responsabilités | ✅ Oui | RACI défini | ✅ Atteint |
| A.5.9 | Inventaire actifs | ✅ Oui | Gestion des actifs | ✅ Atteint |
| A.5.12 | Classification information | ✅ Oui | C1→C4 implémenté | ✅ Atteint |
| A.5.15 | Contrôle d'accès | ✅ Oui | RBAC + MFA | ✅ Atteint |
| A.5.16/18 | Gestion identités/droits | ✅ Oui | `role_manager.py` | ✅ Atteint |
| A.5.17 | Authentification sécurisée | ✅ Oui | MFA TOTP obligatoire | ✅ Atteint |
| A.5.24 | Gestion incidents | ✅ Oui | Procédure PDCA | ✅ Atteint |
| A.5.27 | Analyse post-incident | ✅ Oui | Template et registre | ✅ Atteint |
| A.5.30 | Plan continuité | ✅ Oui | PCA documenté | ✅ Atteint |
| A.5.33 | Politique cryptographique | ✅ Oui | Fernet AES-256 | ✅ Atteint |
| A.5.34 | Gestion clés | ✅ Oui | `key_rotation_scheduler.py` | ✅ Atteint |
| A.5.36 | Conformité sécurité | ✅ Oui | Cette DdA | ✅ Atteint |
| A.7.1 | Sécurité physique | ✅ Oui | Zones documentées | ✅ Atteint |
| A.7.8 | Chiffrement disques | ✅ Oui | VeraCrypt + BitLocker | ✅ Atteint |
| A.8.7 | Protection malwares | ✅ Oui | Windows Defender | ✅ Atteint |
| A.8.8 | Gestion vulnérabilités | ✅ Oui | pip audit + CVE | ✅ Atteint |
| A.8.9 | Config sécurisée | ✅ Oui | Baseline documentée | ✅ Atteint |
| A.8.12 | Prévention fuites (DLP) | ✅ Oui | `output_filter.py` | ✅ Atteint |
| A.8.13 | Sauvegarde | ✅ Oui | Plan 3-2-1 documenté | ✅ Atteint |
| A.8.14 | Tests reprise | ✅ Oui | `tests_pca.md` | ✅ Atteint |
| A.8.15 | Journalisation | ✅ Oui | `audit_trail.py` | ✅ Atteint |
| A.8.16 | Surveillance anomalies | ✅ Oui | `behavioral_detector.py` | ✅ Atteint |
| A.6.7 | Travail à distance | ✅ Oui | VPN planifié — `acces_distant_durcissement_wan.md` | ⚠️ Partiel |
| A.8.20 | Sécurité réseau | ✅ Oui | ER605 + policy + `acces_distant_durcissement_wan.md` | ✅ Atteint |
| A.8.22 | Micro-segmentation | ✅ Oui | VLAN planifié Juillet 2026 — `vlan_config.md` v1.1 | ⚠️ Partiel |
| A.8.25 | SSDLC | ✅ Oui | Procédure documentée | ✅ Atteint |
| A.8.28 | Revue de code | ✅ Oui | Checklist + historique | ✅ Atteint |
| A.8.29 | Tests sécurité | ✅ Oui | 651 tests A+ | ✅ Atteint |
| A.9.2 | Audits internes | ✅ Oui | Programme défini | ✅ Atteint |
| A.9.3 | Revue de direction | ✅ Oui | Annuelle + initiale | ✅ Atteint |
| A.10.2 | Actions correctives | ✅ Oui | Registre NC actif | ✅ Atteint |

---

## 4. Signature

Approuvé par : **Céline Darras** — Fondatrice / Directrice Générale, Cognitive Products Lab  
Date : 2026-06-18

---

## 5. Révision

| Version | Date | Auteur | Modification |
|---|---|---|---|
| 1.0 | 2026-06-18 | Céline Darras | Création DdA initiale — conformité ISO A.5.36 |

> **Cognitive Products Lab — Confidentiel interne**
