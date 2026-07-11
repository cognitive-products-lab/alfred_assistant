# Rapport d'Audit Gouvernance — ALFRED / Cognitive Products Lab

> **Date d'audit :** 2026-07-11 07:01 UTC
> **Données générées le :** 2026-07-11 07:01:30 UTC
> **Manifest version :** V1.2
> **Généré par :** generate_audit_report.py

---

## 1. Synthèse Exécutive

| Indicateur | Valeur |
|---|---|
| **Score CPL global** | **97.1%** |
| **Grade** | **A+** — Excellence — conformité totale |
| Normes actives évaluées | 4 |
| Normes planifiées | 3 |
| Exigences totales (normes actives) | 51 |

```
Score global  [███████████████████░]  97.1%
```

## 2. Scores par norme

| Norme | Score | Grade | OK | Partial | À faire | Total |
|---|---|---|---|---|---|---|
| **RGPD** | `[███████████░]` 95.8% | A+ | 11 | 1 | 0 | 12 |
| **ISO27001** | `[████████████]` 98.4% | A+ | 30 | 1 | 0 | 31 |
| **AIACT** | `[███████████░]` 91.7% | A+ | 5 | 1 | 0 | 6 |
| **NIS2** | `[████████████]` 100.0% | A+ | 2 | 0 | 0 | 2 |
| HDS | _(planifié — V2 2027)_ | — | — | — | — | 5 |
| SECNUMCLOUD | _(planifié — V3 2027)_ | — | — | — | — | 3 |
| PASSI | _(planifié — V3 2027)_ | — | — | — | — | 3 |

## 3. Détail des exigences par norme

### RGPD — RGPD / GDPR
_Règlement (UE) 2016/679_  
**Score : 95.8%** `[███████████████████░]`  
11 atteints · 1 partiels · 0 à faire

| ID | Exigence | Domaine | Statut | Preuve | Priorité |
|---|---|---|---|---|---|
| RGPD-01 | Registre des traitements Art. 30 | Accountability | ✅ Atteint | ✓ |  |
| RGPD-02 | Bases légales documentées pour chaque traitement | Accountability | ✅ Atteint | ✓ |  |
| RGPD-03 | Droit d'accès Art. 15 — export_command.py | Droits personnes | ✅ Atteint | ✓ |  |
| RGPD-04 | Droit d'effacement Art. 17 — commandes /forget | Droits personnes | ✅ Atteint | ✓ |  |
| RGPD-05 | Droit de rectification Art. 16 — édition profil | Droits personnes | ✅ Atteint | ✓ |  |
| RGPD-06 | Consentement renforcé données sensibles Art. 9 _Procédure de consentement formel Art. 9 documentée_ | Données sensibles | ✅ Atteint | ✓ |  |
| RGPD-07 | Portabilité Art. 20 — export + réimportation complète | Droits personnes | ✅ Atteint | ✓ |  |
| RGPD-08 | Analyse d'impact AIPD données de santé | Données sensibles | ✅ Atteint | ✓ |  |
| RGPD-09 | DPA formelle avec sous-traitants (OpenAI API…) _DPA OpenAI acceptée formellement le 2026-06-18_ | Accountability | ✅ Atteint | ✓ |  |
| RGPD-10 | Procédure notification violation 72h (CNIL) | Incidents | ✅ Atteint | ✓ |  |
| RGPD-11 | Opposition Art. 21 — config/features.json fonctionnalités désactivables | Droits personnes | ✅ Atteint | ✓ |  |
| RGPD-12 | AIPD comptes/préférences/conversations/Hadoop — déploiement public (Art. 35) | Accountability | ⚠️ Partiel | ✓ | 🔴 HAUTE |


### ISO27001 — ISO/IEC 27001:2022
_Système de Management de la Sécurité de l'Information_  
**Score : 98.4%** `[████████████████████]`  
30 atteints · 1 partiels · 0 à faire

| ID | Exigence | Domaine | Statut | Preuve | Priorité |
|---|---|---|---|---|---|
| ISO-01 | Politique SMSI formelle approuvée par la direction (A.5.1) | Politiques | ✅ Atteint | ✓ |  |
| ISO-02 | Rôles et responsabilités sécurité documentés (A.5.2) _RACI formel établi + rôles techniques JSON_ | Organisation | ✅ Atteint | ✓ |  |
| ISO-03 | Inventaire des actifs informationnels (A.5.9) | Actifs | ✅ Atteint | ✓ |  |
| ISO-04 | Classification de l'information C1→C4 (A.5.12) | Actifs | ✅ Atteint | ✓ |  |
| ISO-05 | Politique de contrôle d'accès (A.5.15) | Contrôle d'accès | ✅ Atteint | ✓ |  |
| ISO-06 | Gestion des identités et des droits d'accès (A.5.16/A.5.18) | Contrôle d'accès | ✅ Atteint | ✓ |  |
| ISO-07 | Authentification sécurisée — MFA obligatoire (A.5.17) | Contrôle d'accès | ✅ Atteint | ✓ |  |
| ISO-08 | Politique cryptographique — Fernet AES-256 (A.5.33) | Cryptographie | ✅ Atteint | ✓ |  |
| ISO-09 | Gestion et rotation des clés cryptographiques (A.5.34) | Cryptographie | ✅ Atteint | ✓ |  |
| ISO-10 | Sécurité physique — zones sécurisées documentées (A.7.1) | Physique | ✅ Atteint | ✓ |  |
| ISO-11 | Chiffrement intégral des disques — poste de travail (A.7.8) _VeraCrypt D: + BitLocker C: documentés avec procédures audit_ | Physique | ✅ Atteint | ✓ |  |
| ISO-12 | Journalisation sécurisée des activités (A.8.15) | Surveillance | ✅ Atteint | ✓ |  |
| ISO-13 | Surveillance et détection des anomalies comportementales (A.8.16) | Surveillance | ✅ Atteint | ✓ |  |
| ISO-14 | Gestion des vulnérabilités — scan et patching (A.8.8) | Opérations | ✅ Atteint | ✓ |  |
| ISO-15 | Gestion de configuration sécurisée — baseline (A.8.9) _Baseline documentée avec procédure de contrôle des dérives_ | Opérations | ✅ Atteint | ✓ |  |
| ISO-16 | Prévention des fuites de données — DLP (A.8.12) | Opérations | ✅ Atteint | ✓ |  |
| ISO-17 | Sauvegarde et plan de restauration testés (A.8.13) _Plan 3-2-1 documenté + test de restauration 2026-06-18_ | Continuité | ✅ Atteint | ✓ |  |
| ISO-18 | Tests de sécurité automatisés — 651 tests (A.8.29) | Développement | ✅ Atteint | ✓ |  |
| ISO-19 | Sécurité des réseaux — firewall, règles documentées (A.8.20) _Politique réseau complète avec règles firewall ER605_ | Réseau | ✅ Atteint | ✓ |  |
| ISO-20 | Micro-segmentation réseau — VLAN isolation (A.8.22) _Architecture VLAN documentée — implémentation physique Q3 2026 (2026-06-18)_ | Réseau | ⚠️ Partiel | ✓ | 🟡 MOYENNE |
| ISO-21 | Cycle de développement sécurisé — SSDLC (A.8.25) | Développement | ✅ Atteint | ✓ |  |
| ISO-22 | Revue de code et audit sécurité applicative (A.8.28) | Développement | ✅ Atteint | ✓ |  |
| ISO-23 | Protection contre les logiciels malveillants (A.8.7) | Opérations | ✅ Atteint | ✓ |  |
| ISO-24 | Procédure formelle de gestion des incidents (A.5.24) _Procédure PDCA complète avec RACI et niveaux de gravité_ | Incidents | ✅ Atteint | ✓ |  |
| ISO-25 | Analyse post-incident et leçons apprises (A.5.27) | Incidents | ✅ Atteint | ✓ |  |
| ISO-26 | Plan de continuité d'activité PCA documenté (A.5.30) | Continuité | ✅ Atteint | ✓ |  |
| ISO-27 | Tests PCA et exercices de reprise (A.8.14) _Plan trimestriel + test partiel 2026-06-18_ | Continuité | ✅ Atteint | ✓ |  |
| ISO-28 | Revue de direction et revue SMSI annuelle (A.9.3) | Amélioration | ✅ Atteint | ✓ |  |
| ISO-29 | Audits internes SMSI planifiés (A.9.2) | Amélioration | ✅ Atteint | ✓ |  |
| ISO-30 | Gestion des non-conformités et actions correctives (A.10.2) | Amélioration | ✅ Atteint | ✓ |  |
| ISO-31 | Déclaration d'applicabilité (DdA) et scope SMSI formel (A.5.36) _DdA complète avec tous les contrôles ISO 27001:2022_ | Conformité | ✅ Atteint | ✓ |  |


### AIACT — EU AI Act
_Règlement (UE) 2024/1689 — GPAI & Systèmes à risque_  
**Score : 91.7%** `[██████████████████░░]`  
5 atteints · 1 partiels · 0 à faire

| ID | Exigence | Domaine | Statut | Preuve | Priorité |
|---|---|---|---|---|---|
| AIACT-01 | Classification et documentation du niveau de risque | Risk Management | ✅ Atteint | ✓ |  |
| AIACT-02 | Transparence envers l'utilisateur (Art. 13) | Transparence | ✅ Atteint | ✓ |  |
| AIACT-03 | Supervision humaine — Human in the Loop (Art. 14) | Contrôle humain | ✅ Atteint | ✓ |  |
| AIACT-04 | Système de gestion des risques IA documenté (Art. 9) | Risk Management | ✅ Atteint | ✓ |  |
| AIACT-05 | Gouvernance des données d'entraînement (Art. 10) | Données | ✅ Atteint | ✓ |  |
| AIACT-06 | Enregistrement au registre UE IA haute priorité (Art. 49) _Évaluation documentée — risque limité, obligation non applicable. Veille active._ | Conformité | ⚠️ Partiel | ✓ | 🟡 MOYENNE |


### NIS2 — NIS2
_Directive (UE) 2022/2555 — hors champ légal (micro-entreprise), conformité volontaire_  
**Score : 100.0%** `[████████████████████]`  
2 atteints · 0 partiels · 0 à faire

| ID | Exigence | Domaine | Statut | Preuve | Priorité |
|---|---|---|---|---|---|
| NIS2-01 | Mesures de sécurité des réseaux et SI (Art. 21) | Sécurité technique | ✅ Atteint | ✓ |  |
| NIS2-02 | Signalement incidents à l'autorité compétente (Art. 23) | Incidents | ✅ Atteint | ✓ |  |





## 4. Plan d'action — Exigences à traiter

### 4.1 Priorité HAUTE

- **[RGPD]** `RGPD-12` — AIPD comptes/préférences/conversations/Hadoop — déploiement public (Art. 35) ⚠️

### 4.2 Priorité MOYENNE

- **[ISO27001]** `ISO-20` — Micro-segmentation réseau — VLAN isolation (A.8.22) ⚠️
  > _Architecture VLAN documentée — implémentation physique Q3 2026 (2026-06-18)_
- **[AIACT]** `AIACT-06` — Enregistrement au registre UE IA haute priorité (Art. 49) ⚠️
  > _Évaluation documentée — risque limité, obligation non applicable. Veille active._

## 5. Fichiers de preuve

✅ Tous les fichiers de preuve déclarés sont présents sur disque.

## 6. Normes planifiées

### HDS — HDS
_Hébergement de Données de Santé — Décret 2018-137_  
**Horizon :** V2 2027  
**Périmètre :** 5 exigences à cadrer

| ID | Exigence | Domaine |
|---|---|---|
| HDS-01 | Certification hébergeur données de santé | Certification |
| HDS-02 | Contrat d'hébergement conforme HDS | Contractuel |
| HDS-03 | Séparation logique des données de santé | Architecture |
| HDS-04 | Traçabilité et audits accès données santé | Audit |
| HDS-05 | Plan de sauvegarde données santé | Continuité |

### SECNUMCLOUD — SecNumCloud
_Qualification ANSSI — Services Cloud souverains_  
**Horizon :** V3 2027  
**Périmètre :** 3 exigences à cadrer

| ID | Exigence | Domaine |
|---|---|---|
| SNC-01 | Hébergement infrastructure souveraine (UE) | Souveraineté |
| SNC-02 | Isolation des données clients (multitenancy) | Architecture |
| SNC-03 | Audit de qualification ANSSI | Certification |

### PASSI — PASSI
_Prestataire d'Audit SSI — qualification ANSSI_  
**Horizon :** V3 2027  
**Périmètre :** 3 exigences à cadrer

| ID | Exigence | Domaine |
|---|---|---|
| PASSI-01 | Audit pentest par prestataire qualifié PASSI | Audit |
| PASSI-02 | Rapport d'audit — synthèse et plan de remédiation | Audit |
| PASSI-03 | Vérification annuelle par auditeur externe | Amélioration |

## 7. Roadmap Conformité

| Statut | Jalon | Horizon |
|---|---|---|
| ✅ Terminé | Socle Zero Trust — 43 modules · 651 tests A+ | Juin 2026 |
| ✅ Terminé | RGPD Art. 30 — registre 6 traitements · 0 transfert hors UE | Juin 2026 |
| ✅ Terminé | SMSI ISO 27001 — classification C1→C4, journalisation, MFA | Juin 2026 |
| ✅ Terminé | Dashboard Conformité Réglementaire dynamique (7 normes) | Juin 2026 |
| ✅ Terminé | RGPD — consentement Art. 9 formel + AIPD + notification 72h CNIL | Juin 2026 |
| ✅ Terminé | ISO 27001 — SMSI complet : PCA, RACI, revue direction, vulnérabilités, SSDLC (97%) | Juin 2026 |
| ✅ Terminé | AI Act — HITL, registre risques IA, gouvernance données entraînement | Juin 2026 |
| ✅ Terminé | NIS2 — procédure signalement incidents (ANSSI/CERT-FR) | Juin 2026 |
| ✅ Terminé | DPA formelle OpenAI — acceptation portail (RGPD-09) | Juin 2026 |
| 🟡 Planifié | VLAN isolation PC Alfred · micro-segmentation réseau (ISO A.8.20) | Q3 2026 |
| 🔮 Futur | HDS — hébergement données santé ARTHUR (Décret 2018-137) | V2 2027 |
| 🔮 Futur | SecNumCloud — infrastructure souveraine + audit ANSSI | V3 2027 |
| 🔮 Futur | PASSI — pentest qualifié ANSSI annuel | V3 2027 |

## 8. Focus — Droits individuels RGPD

| Droit | Exigence | Statut | Preuve |
|---|---|---|---|
| **Art. 15 — Accès** | Droit d'accès Art. 15 — export_command.py | ✅ Atteint | ✓ présente |
| **Art. 16 — Rectification** | Droit d'effacement Art. 17 — commandes /forget | ✅ Atteint | ✓ présente |
| **Art. 17 — Effacement** | Droit de rectification Art. 16 — édition profil | ✅ Atteint | ✓ présente |
| **Art. 20 — Portabilité** | Portabilité Art. 20 — export + réimportation complète | ✅ Atteint | ✓ présente |
| **Art. 21 — Opposition** | Opposition Art. 21 — config/features.json fonctionnalités désactivables | ✅ Atteint | ✓ présente |

---

## 9. Informations d'audit

| Champ | Valeur |
|---|---|
| Date du rapport | 2026-07-11 07:01 UTC |
| Méthode d'évaluation | Vérification automatique des fichiers de preuve sur disque |
| Scoring | done = 1.0 · partial = 0.5 · todo = 0.0 |
| Pondération | Proportionnelle au nombre d'exigences par norme |
| Outil | `tools/dashboard_tools/dashboard_gouvernance/generate_audit_report.py` |
| Données source | `dashboard/dashboard_gouvernance/dashboard_gouvernance_data.json` |
| Manifest | `dashboard/dashboard_gouvernance/_manifest.json` |

> Ce rapport est généré automatiquement à chaque exécution de `update_gouvernance_data.py`.
> Il constitue la trace d'audit horodatée de l'état de conformité réglementaire d'ALFRED.
> **Cognitive Products Lab — Confidentiel interne**

