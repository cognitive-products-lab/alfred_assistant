# PSSI — Politique de Sécurité des Systèmes d'Information ALFRED

Cognitive Products Lab · ALFRED · V1.0 · Synthèse — Juin 2026 · Confidentiel interne

Ce document est la **synthèse PSSI** du projet ALFRED. Il s'appuie sur les documents
détaillés présents dans ce dossier (`docs/security/`) :

- `politique_cybersecurite_alfred.pdf` — Politique cybersécurité complète (architecture
  Zero Trust, Secure SDLC, IAM, chiffrement, conformité OWASP, gouvernance, roadmap)
- `politique_donnees_rgpd_alfred.pdf` — Politique de protection des données / RGPD
- `protocole_incidents_alfred.pdf` — Protocole de gestion des incidents
- `addendum_cybersecurite_alfred.pdf` — Addendum cybersécurité
- `document_data_security_20_05_2026.pdf` — Document sécurité des données (20/05/2026)

**SMSI ISO 27001:2022 — Documents opérationnels** (`docs/smsi/`) :

| Document | Référence ISO |
|---|---|
| `politique_securite.md` | A.5.1 — Politique SMSI |
| `raci_securite.md` | A.5.2 — Rôles et responsabilités |
| `inventaire_actifs.json` | A.5.9 — Inventaire actifs |
| `procedure_incidents.md` | A.5.24 — Gestion incidents (PDCA+RACI) |
| `post_incident_analysis.md` | A.5.27 — Analyse post-incident |
| `pca.md` | A.5.30 — Plan de continuité |
| `declaration_applicabilite.md` | A.5.36 — Déclaration d'applicabilité (DdA) |
| `securite_physique.md` | A.7.1 — Zones sécurisées |
| `chiffrement_disque.md` | A.7.8 — Chiffrement disques |
| `antimalware.md` | A.8.7 — Protection malwares |
| `vuln_management.md` | A.8.8 — Gestion vulnérabilités |
| `baseline_config.md` | A.8.9 — Configuration sécurisée |
| `plan_sauvegarde.md` | A.8.13 — Sauvegarde 3-2-1 |
| `tests_pca.md` | A.8.14 — Tests PCA |
| `vlan_config.md` | A.8.22 — VLAN isolation (Juillet 2026) |
| `acces_distant_durcissement_wan.md` | A.8.20/A.6.7 — VPN accès distant + durcissement WAN (Juillet 2026) |
| `ssdlc_procedure.md` | A.8.25 — SSDLC |
| `revue_code.md` | A.8.28 — Revue de code |
| `audit_interne.md` | A.9.2 — Audits internes |
| `revue_direction.md` | A.9.3 — Revue de direction |
| `actions_correctives.md` | A.10.2 — Non-conformités |

**Conformité réglementaire complémentaire** :
- `docs/gouvernance/consentement_art9.md` — RGPD Art.9 consentement données sensibles
- `docs/smsi/aipd_donnees_sante.md` — RGPD Art.35 AIPD
- `docs/smsi/dpa_sous_traitants.md` — RGPD Art.28 DPA sous-traitants
- `docs/smsi/procedure_notification_violation.md` — RGPD Art.33-34 notification 72h CNIL
- `docs/smsi/procedure_signalement_nis2.md` — NIS2 Art.23 signalement ANSSI/CERT-FR
- `docs/smsi/hitl_procedure.md` — AI Act Art.14 Human in the Loop
- `docs/smsi/registre_risques_ia.md` — AI Act Art.9 gestion risques IA
- `docs/smsi/gouvernance_donnees_entrainement.md` — AI Act Art.10

**Score conformité global : 97% (A+)** — Rapports horodatés : `dashboard/dashboard_gouvernance/reports/`

Responsable : Céline Darras, Fondatrice — Cognitive Products Lab.

## 1. Principes directeurs

8 principes non négociables : **Local-First**, **Zero Trust**, **Security by Design**,
**Privacy by Design**, **Fail-Safe**, **Least Privilege**, **Defense in Depth**,
**Auditabilité**.

## 2. Architecture de sécurité — Pipeline Zero Trust

Toute requête traverse, dans l'ordre, 9 couches (un refus à une couche arrête le
traitement) :

| # | Couche | Module |
|---|--------|--------|
| 1 | Validation entrée | `input_validator.py` |
| 2 | Détection menace | `threat_detector.py` + `behavioral_detector.py` |
| 3 | Contrôle appareil | `device_registry.py` |
| 4 | Authentification | `authenticator.py` |
| 5 | MFA | `mfa_manager.py` |
| 6 | RBAC | `role_manager.py` + `permission_manager.py` |
| 7 | Politique Zero Trust | `policy_engine.py` + `zero_trust_orchestrator.py` |
| 8 | Filtrage sortie | `output_filter.py` |
| 9 | Audit trail | `audit_trail.py` + `security_logger.py` |

Détail des règles : voir `config/security/zero_trust_rules.json` (ZT-01 → ZT-11).

## 3. Gestion des identités et des accès (IAM/RBAC)

7 rôles définis dans `config/security/roles_permissions.json` (synchronisé avec
`src/security/permission_manager.py`) : **OWNER, ADMIN, USER, GUEST, SERVICE, AI_MODULE,
EMERGENCY**.

- MFA (TOTP) obligatoire pour OWNER et ADMIN, et pour tous les rôles non exemptés quand
  `security_settings.json.mfa_required = true`.
- PIN : bcrypt rounds≥12, blocage après 5 tentatives échouées, session 900s.
- Aucun rôle ne dépasse sa sensibilité maximale autorisée (`policy_engine.py`).

> **Note** : `config/security/access_policies.json` (`{"policies": []}`) est un
> fichier d'inventaire historique, non lu par le code. Les politiques d'accès
> effectives (`_RESTRICTED_ACTIONS`, `_ROLE_MAX_SENSITIVITY`) sont codées dans
> `policy_engine.py`, cf. section 2 et `zero_trust_rules.json` (ZT-07, ZT-08).
> Même constat (B04) pour `config/ethics_rules.json` (`{"rules": []}`) : le
> cadre éthique réel est dans `knowledges/system/ethics/ethical_framework.json`
> et `knowledges/cpl/ethics_governance/*.json`, chargés via
> `knowledges/knowledge_registry.json` (`knowledge_loader.py`, Bloc 18).

## 4. Chiffrement et secrets

- Données persistantes (JSON mémoire) : Fernet (AES-128-CBC + HMAC-SHA256), clé
  `FERNET_KEY` dans `.env` uniquement (jamais sur disque ni dans Git).
- PIN/mots de passe : bcrypt rounds≥12.
- Secrets MFA (TOTP) : chiffrés Fernet avant stockage.
- `.gitignore` exclut `.env`, `*.key`, `*.pem`, `*.p12`, `data/`.
- Rotation des clés : planificateur `key_rotation_scheduler.py` (rotation effective
  manuelle, V2).

## 5. Règles de développement sécurisé (Secure SDLC)

Règles absolues : jamais de secret en clair, jamais de `.env` dans Git, jamais
d'`except Exception` sans `security_logger`, jamais de permission sans `has_access()`,
jamais de donnée persistante non chiffrée, toujours valider via `input_validator.py`,
toujours un test unitaire par fonction de sécurité.

## 6. Conformité OWASP Top 10

Couverture A01→A10 assurée par RBAC/Zero Trust (A01), Fernet/bcrypt/TOTP (A02),
`input_validator`/`threat_detector` (A03), architecture Zero Trust (A04),
`security_governance` (A05), tests automatisés (A06), bcrypt/MFA/rate limiter (A07),
`audit_trail` (A08), `security_dashboard`/`security_logger` (A09), patterns SSRF dans
`input_validator` (A10).

## 7. KPI sécurité

| KPI | Objectif |
|-----|----------|
| Score sécurité global (dashboard) | ≥ 90/100 |
| Conformité OWASP | ≥ 95% |
| Couverture tests sécurité | ≥ 80% (100% modules critiques) |
| Temps détection incident | < 30s |
| Temps réponse P1 | < 15 min |
| Incidents non résolus > 48h (P1/P2) | 0 |

## 8. Gouvernance et revues

- Après chaque commit : tests + `.gitignore` + absence de secrets (vérifié par
  `security_governance.py`, score actuel : voir `dashboard/dashboard_security/`).
- Hebdomadaire : revue dashboard sécurité, incidents ouverts, KPI.
- Mensuelle : audit complet, revue des rôles actifs, mise à jour dépendances.
- À chaque version majeure : revue complète de la politique sécurité.
- Incident P1/P2 : post-mortem + mise à jour `protocole_incidents_alfred.pdf`.

## 9. Roadmap sécurité V2 → V3+

Priorités critiques V2 : rotation des clés Fernet, expiration/révocation automatique
des appareils, tests de charge sécurité, corrélation d'événements multi-incidents.
Détail complet : `politique_cybersecurite_alfred.pdf` section 8.

## 10. Risques résiduels acceptés

| Date | Risque | Évaluation | Décision |
|------|--------|------------|----------|
| 2026-06-14 | Ancienne valeur de `data/security/fernet.key` (supprimée du suivi git, commit `3916aa8`) reste présente dans l'historique git de la branche `dev`. | Clé différente de celle active dans `.env` (`FERNET_KEY`). Vérification : aucune occurrence de l'ancienne valeur dans le code, les données ou la config actuels (`grep` sur tout le repo, 0 résultat). `encryption_service.py` utilise exclusivement `FERNET_KEY` (env). Impact réel jugé faible — la clé exposée n'est plus utilisée pour chiffrer/déchiffrer aucune donnée active. | **Risque accepté** sans réécriture d'historique (réécriture jugée plus risquée sur branche `dev` partagée que l'exposition résiduelle). À réévaluer lors de la prochaine rotation de clé planifiée (`key_rotation_scheduler.py`, V2) : si une réécriture d'historique est faite pour une autre raison, en profiter pour purger cette clé. |

---
*Document vivant — mis à jour à chaque version majeure et après chaque incident
significatif. Référence : `politique_cybersecurite_alfred.pdf` V1.0 (Mai 2026).*
