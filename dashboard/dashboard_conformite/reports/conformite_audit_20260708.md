# Rapport Conformité ALFRED — 2026-07-08

**Score global** : 85% — Grade B+

| Métrique | Valeur |
|---|---|
| Total exigences | 70 |
| Applicables | 62 |
| Conformes | 53 |
| En cours | 4 |
| À faire | 5 |
| Non concerné | 8 |

## RGPD — RGPD / GDPR
Score : 100% (11/11 conformes)

- ✅ `RGPD-01` Registre des activités de traitement — *conforme*
- ✅ `RGPD-02` Bases légales documentées — données sensibles — *conforme*
- ✅ `RGPD-03` Information et transparence à la collecte — *conforme*
- ✅ `RGPD-04` Droit d'accès — export_command.py — *conforme*
- ✅ `RGPD-05` Droit de rectification — édition profil — *conforme*
- ✅ `RGPD-06` Droit à l'effacement — commandes /forget — *conforme*
- ✅ `RGPD-07` Portabilité — export + réimportation complète — *conforme*
- ✅ `RGPD-08` Droit d'opposition — config/features.json — *conforme*
- ✅ `RGPD-09` DPA formelle avec sous-traitants (OpenAI API) — *conforme*
- ✅ `RGPD-10` Procédure notification violation 72h CNIL — *conforme*
- ✅ `RGPD-11` AIPD obligatoire — données psychologiques art.9 — *conforme*

## LIL — LIL — Loi Informatique et Libertés
Score : 100% (2/2 conformes)

- ✅ `LIL-01` Traitement données sensibles en France — *conforme*
- ✅ `LIL-02` Déclaration/autorisation CNIL si applicable — *conforme*

## AIACT — EU AI Act
Score : 83% (5/6 conformes)

- ✅ `AIACT-01` Classification et documentation du niveau de risque — *conforme*
- ✅ `AIACT-02` Transparence envers l'utilisateur — *conforme*
- ✅ `AIACT-03` Supervision humaine — Human in the Loop — *conforme*
- ✅ `AIACT-04` Système de gestion des risques IA documenté — *conforme*
- ✅ `AIACT-05` Gouvernance des données d'entraînement — *conforme*
- ⏳ `AIACT-06` Enregistrement au registre UE IA (si requis) — *en_cours*

## NIS2 — NIS2
Score : 100% (4/4 conformes)

- ✅ `NIS2-01` Mesures de sécurité des réseaux et SI — *conforme*
- ✅ `NIS2-02` Sécurité de la chaîne d'approvisionnement — *conforme*
- ✅ `NIS2-03` Authentification multifacteur (MFA) obligatoire — *conforme*
- ✅ `NIS2-04` Signalement incidents à l'autorité compétente — *conforme*

## ISO27001 — ISO 27001:2022
Score : 97% (30/31 conformes)

- ✅ `ISO-01` Politique SMSI formelle approuvée — *conforme*
- ✅ `ISO-02` Rôles et responsabilités sécurité documentés — *conforme*
- ✅ `ISO-03` Inventaire des actifs informationnels — *conforme*
- ✅ `ISO-04` Classification de l'information C1→C4 — *conforme*
- ✅ `ISO-05` Politique de contrôle d'accès — *conforme*
- ✅ `ISO-06` Gestion des identités et droits d'accès — *conforme*
- ✅ `ISO-07` Authentification sécurisée — MFA TOTP — *conforme*
- ✅ `ISO-08` Politique cryptographique — Fernet AES-256 — *conforme*
- ✅ `ISO-09` Gestion et rotation des clés cryptographiques — *conforme*
- ✅ `ISO-10` Sécurité physique — zones sécurisées documentées — *conforme*
- ✅ `ISO-11` Chiffrement intégral des disques — *conforme*
- ✅ `ISO-12` Journalisation sécurisée des activités — *conforme*
- ✅ `ISO-13` Surveillance et détection des anomalies — *conforme*
- ✅ `ISO-14` Gestion des vulnérabilités et patching — *conforme*
- ✅ `ISO-15` Gestion de configuration sécurisée — baseline — *conforme*
- ✅ `ISO-16` Prévention des fuites de données — DLP — *conforme*
- ✅ `ISO-17` Sauvegarde et plan de restauration testés — *conforme*
- ✅ `ISO-18` Tests de sécurité automatisés — 651 tests — *conforme*
- ✅ `ISO-19` Sécurité des réseaux — firewall, règles documentées — *conforme*
- ⏳ `ISO-20` Micro-segmentation réseau — VLAN isolation — *en_cours*
- ✅ `ISO-21` Cycle de développement sécurisé — SSDLC — *conforme*
- ✅ `ISO-22` Revue de code et audit sécurité applicative — *conforme*
- ✅ `ISO-23` Protection contre les logiciels malveillants — *conforme*
- ✅ `ISO-24` Procédure formelle de gestion des incidents — *conforme*
- ✅ `ISO-25` Analyse post-incident et leçons apprises — *conforme*
- ✅ `ISO-26` Plan de continuité d'activité PCA documenté — *conforme*
- ✅ `ISO-27` Tests PCA et exercices de reprise — *conforme*
- ✅ `ISO-28` Revue de direction et revue SMSI annuelle — *conforme*
- ✅ `ISO-29` Audits internes SMSI planifiés — *conforme*
- ✅ `ISO-30` Gestion des non-conformités et actions correctives — *conforme*
- ✅ `ISO-31` Déclaration d'Applicabilité (DdA) — 93 contrôles — *conforme*

## HDS — HDS — Hébergeur Données de Santé
Score : 0% (0/0 conformes)

- — `HDS-01` Certification hébergeur données de santé — *non_concerne*
- — `HDS-02` Contrat d'hébergement conforme HDS — *non_concerne*
- — `HDS-03` Séparation logique des données de santé — *non_concerne*
- — `HDS-04` Traçabilité et audits accès données santé — *non_concerne*
- — `HDS-05` Plan de sauvegarde données de santé — *non_concerne*

## SECNUMCLOUD — SecNumCloud
Score : 0% (0/0 conformes)

- — `SNC-01` Hébergement infrastructure souveraine (UE) — *non_concerne*
- — `SNC-02` Isolation des données clients (multitenancy) — *non_concerne*
- — `SNC-03` Audit de qualification ANSSI — *non_concerne*

## PASSI — PASSI — Pentest ANSSI
Score : 0% (0/3 conformes)

- ❌ `PASSI-01` Audit pentest par prestataire qualifié PASSI — *todo*
- ❌ `PASSI-02` Rapport d'audit — synthèse et plan de remédiation — *todo*
- ❌ `PASSI-03` Vérification annuelle par auditeur externe — *todo*

## CRA — Cyber Resilience Act
Score : 20% (1/5 conformes)

- ✅ `CRA-01` Sécurité by design — conception et développement sécurisés — *conforme*
- ⏳ `CRA-02` Politique de gestion des vulnérabilités — PSIRT/CVD — *en_cours*
- ⏳ `CRA-03` Mises à jour de sécurité — durée de vie du produit — *en_cours*
- ❌ `CRA-04` SBOM — Software Bill of Materials — *todo*
- ❌ `CRA-05` Déclaration de conformité UE (DoC) + marquage CE — *todo*

