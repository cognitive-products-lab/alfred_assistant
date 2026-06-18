# Gestion des Non-conformités et Actions Correctives

> **Référence :** ISO/IEC 27001:2022 — Contrôle A.10.2  
> **Version :** 1.0 — 2026-06-18  
> **Propriétaire :** Cognitive Products Lab — Céline Darras  
> **Statut :** Approuvé

---

## 1. Processus de traitement des non-conformités

1. **Identification** : Via audit automatique, audit interne ou incident
2. **Enregistrement** : Dans ce registre avec ID unique
3. **Analyse cause racine** : Identification de la source
4. **Plan d'action** : Définition des mesures correctives
5. **Implémentation** : Réalisation des mesures
6. **Vérification efficacité** : Validation que la NC est levée
7. **Clôture** : Archivage

---

## 2. Registre des non-conformités actives

| ID NC | Source | Description | Priorité | Responsable | Échéance | Statut |
|---|---|---|---|---|---|---|
| NC-2026-001 | Audit 2026-06-18 | DPA OpenAI non formalisée (RGPD-09) | HAUTE | Céline Darras | 2026-07-31 | 🟡 En cours |
| NC-2026-002 | Audit 2026-06-18 | VLAN isolation PC Alfred absent (ISO-19/20) | MOYENNE | Céline Darras | 2026-09-30 | 🟡 Planifié |
| NC-2026-003 | Audit 2026-06-18 | Score AI Act 33% (AIACT-03/04/05/06) | MOYENNE | Céline Darras | 2026-12-31 | 🟡 Planifié |

---

## 3. Non-conformités clôturées (ce sprint)

| ID NC | Description | Date clôture | Mesure corrective |
|---|---|---|---|
| NC-2026-010 | Procédure incidents PDCA absente (ISO-24) | 2026-06-18 | procedure_incidents.md créé |
| NC-2026-011 | Analyse post-incident absente (ISO-25) | 2026-06-18 | post_incident_analysis.md créé |
| NC-2026-012 | Notification violation 72h absente (RGPD-10) | 2026-06-18 | procedure_notification_violation.md créé |
| NC-2026-013 | AIPD données santé absente (RGPD-08) | 2026-06-18 | aipd_donnees_sante.md créé |
| NC-2026-014 | Signalement NIS2 absent (NIS2-02) | 2026-06-18 | procedure_signalement_nis2.md créé |
| NC-2026-015 | Politique SMSI absente (ISO-01) | 2026-06-18 | politique_securite.md créé |
| NC-2026-016 | RACI formel absent (ISO-02) | 2026-06-18 | raci_securite.md créé |
| NC-2026-017 | Inventaire actifs absent (ISO-03) | 2026-06-18 | inventaire_actifs.json créé |
| NC-2026-018 | Sécurité physique non documentée (ISO-10) | 2026-06-18 | securite_physique.md créé |
| NC-2026-019 | Chiffrement disque non documenté (ISO-11) | 2026-06-18 | chiffrement_disque.md créé |
| NC-2026-020 | Gestion vulnérabilités absente (ISO-14) | 2026-06-18 | vuln_management.md créé |
| NC-2026-021 | Baseline config absente (ISO-15) | 2026-06-18 | baseline_config.md créé |
| NC-2026-022 | Plan sauvegarde absent (ISO-17) | 2026-06-18 | plan_sauvegarde.md créé |
| NC-2026-023 | Politique réseau absente (ISO-19) | 2026-06-18 | network_policy.json créé |
| NC-2026-024 | VLAN config absente (ISO-20) | 2026-06-18 | vlan_config.md créé (planifié Q3) |
| NC-2026-025 | SSDLC absent (ISO-21) | 2026-06-18 | ssdlc_procedure.md créé |
| NC-2026-026 | Revue de code absente (ISO-22) | 2026-06-18 | revue_code.md créé |
| NC-2026-027 | Antimalware non documenté (ISO-23) | 2026-06-18 | antimalware.md créé |
| NC-2026-028 | PCA absent (ISO-26) | 2026-06-18 | pca.md créé |
| NC-2026-029 | Tests PCA absents (ISO-27) | 2026-06-18 | tests_pca.md créé |
| NC-2026-030 | Revue direction absente (ISO-28) | 2026-06-18 | revue_direction.md créé |
| NC-2026-031 | Audit interne absent (ISO-29) | 2026-06-18 | audit_interne.md créé |
| NC-2026-032 | DdA SMSI absente (ISO-31) | 2026-06-18 | declaration_applicabilite.md créé |
| NC-2026-033 | Consentement Art.9 absent (RGPD-06) | 2026-06-18 | consentement_art9.md créé |

---

## 4. Révision

| Version | Date | Auteur | Modification |
|---|---|---|---|
| 1.0 | 2026-06-18 | Céline Darras | Création registre NC — conformité ISO A.10.2 |

> **Cognitive Products Lab — Confidentiel interne**
