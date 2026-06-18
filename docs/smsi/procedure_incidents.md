# Procédure Formelle de Gestion des Incidents de Sécurité

> **Référence :** ISO/IEC 27001:2022 — Contrôle A.5.24  
> **Norme liée :** NIS2 Art. 23 — Signalement autorité compétente  
> **Version :** 1.0 — 2026-06-18  
> **Propriétaire :** Cognitive Products Lab — Responsable Sécurité (Céline Darras)  
> **Statut :** Approuvé

---

## 1. Objectif

Définir le processus PDCA complet pour détecter, qualifier, traiter, notifier et clore tout incident de sécurité affectant ALFRED ou les données utilisateurs de Cognitive Products Lab.

---

## 2. Périmètre

S'applique à tous les incidents touchant :
- L'infrastructure ALFRED (PC Alfred, serveurs, réseau)
- Les données personnelles utilisateurs (données sensibles chiffrées)
- Les systèmes d'IA et de traitement conversationnel
- Les accès non autorisés, violations de données, anomalies comportementales

---

## 3. RACI — Rôles et Responsabilités

| Activité | R | A | C | I |
|---|---|---|---|---|
| Détection et signalement initial | Système auto / Utilisateur | — | — | Resp. Sécurité |
| Qualification et triage | Resp. Sécurité | Fondatrice | — | — |
| Containment immédiat | Resp. Sécurité | Fondatrice | — | Utilisateurs concernés |
| Investigation et analyse | Resp. Sécurité | Fondatrice | — | — |
| Notification CNIL / ANSSI | Fondatrice | — | Resp. Sécurité | — |
| Remédiation technique | Resp. Sécurité | Fondatrice | — | — |
| Analyse post-incident | Resp. Sécurité | Fondatrice | — | — |
| Clôture et archivage | Resp. Sécurité | Fondatrice | — | — |

**Rôles CPL :**
- **Fondatrice / DG :** Céline Darras — approbation finale, notifications réglementaires
- **Responsable Sécurité :** Céline Darras (double casquette V1) — opérationnel sécurité
- **Système ALFRED :** détection automatique via `behavioral_detector.py`, `audit_trail.py`

---

## 4. Cycle PDCA

### P — Préparation
- Registre incidents : `data/security/incident_register.json`
- Détection : `src/security/behavioral_detector.py`, `src/security/audit_trail.py`
- Seuils d'alerte : `config/security/security_settings.json`

### D — Exécution

**Étape 1 — Détection (H+0)**
- Enregistrement immédiat dans `incident_register.json` avec horodatage
- Identifiant unique : `INC-AAAA-MM-DD-NNN`

**Étape 2 — Triage**

| Niveau | Critère | Délai réponse |
|---|---|---|
| P1 — Critique | Violation données personnelles, accès non autorisé, ransomware | H+1 |
| P2 — Haute | Anomalie persistante, intrusions répétées | H+4 |
| P3 — Modérée | Erreur config sécurité, anomalie isolée | J+1 |
| P4 — Faible | Faux positif, événement mineur | J+3 |

**Étape 3 — Containment** : isolation système, révocation accès suspects, sauvegarde preuves

**Étape 4 — Investigation** : analyse logs `audit_trail.py`, corrélation `behavioral_detector.py`, cause racine

**Étape 5 — Notification réglementaire**
- CNIL : 72h si risque pour droits → `procedure_notification_violation.md`
- ANSSI/CERT-FR : si entité NIS2 → `procedure_signalement_nis2.md`
- Personnes concernées : sans délai injustifié si risque élevé

**Étape 6 — Remédiation** : correction cause racine, rotation clés si nécessaire (`key_rotation_scheduler.py`)

### C — Vérification
- Validation efficacité remédiation
- Mise à jour registre `incident_register.json` — statut "resolved"

### A — Amélioration
- Rapport post-incident (`post_incident_analysis.md`)
- Leçons apprises → revue de direction

---

## 5. Obligations de notification

| Gravité | Données personnelles | CNIL | ANSSI |
|---|---|---|---|
| P1 — Critique | Oui | Notification 72h | Signalement NIS2 |
| P2 — Haute | Possible | Évaluation + notification si risque | Évaluation |
| P3/P4 | Non | Documentation interne | Non requis |

---

## 6. Révision

| Version | Date | Auteur | Modification |
|---|---|---|---|
| 1.0 | 2026-06-18 | Céline Darras | Création — conformité ISO A.5.24 + NIS2 Art.23 |

> **Cognitive Products Lab — Confidentiel interne**
