# Documentation Sécurité ALFRED
## Table : Script · Rôle · Menace prise en charge · Fichiers de suivi · Classe de risque

---

> **Lecture du tableau**
> - **Script** : chemin du module depuis la racine du projet
> - **Rôle** : fonction de sécurité assurée
> - **Menaces prises en charge** : vecteurs d'attaque bloqués ou détectés
> - **Fichiers de suivi** : journaux, registres ou configs associés
> - **Classe de risque** : niveau OWASP / CWE ou catégorie interne

---

## Pipeline d'entrée

| Script | Rôle | Menaces prises en charge | Fichiers de suivi | Classe de risque |
|--------|------|--------------------------|-------------------|-----------------|
| `src/security/input_validator.py` | Sanitisation et validation de toutes les entrées utilisateur | SQL injection · XSS · path traversal · command injection · prompt injection · SSRF · homoglyphes · null bytes | `logs/security/security.log` | **CRITIQUE** — OWASP A03 (Injection) |
| `src/security/threat_detector.py` | Calcul d'un score de menace sur chaque input | SQL tautologies · XSS · command shells · prompt jailbreak · LDAP injection · null bytes · encodage suspect | `logs/security/audit_trail.jsonl` | **CRITIQUE** — OWASP A03 · CWE-20 |
| `src/security/output_filter.py` | Masquage des données sensibles dans les réponses générées | Fuite de clés API · JWT · tokens GitHub · chaînes base64 sensibles · variables d'environnement | `logs/security/security.log` | **ÉLEVÉ** — OWASP A02 (Exposition de données) |

---

## Authentification et contrôle d'accès

| Script | Rôle | Menaces prises en charge | Fichiers de suivi | Classe de risque |
|--------|------|--------------------------|-------------------|-----------------|
| `src/auth/authenticator.py` | Authentification PIN locale (bcrypt rounds=12 + sel aléatoire) | Brute-force · rainbow tables · attaque par dictionnaire · réutilisation de hash | `data/security/pins.json` · `logs/security/security.log` | **CRITIQUE** — OWASP A07 (Auth) · CWE-307 |
| `src/security/rate_limiter.py` | Limitation du taux de tentatives avec backoff exponentiel (30s→60s→120s) | Brute-force · credential stuffing · déni de service local | `logs/security/security.log` | **ÉLEVÉ** — OWASP A04 · CWE-307 |
| `src/security/session_manager.py` | Gestion du cycle de vie des sessions (création, validité, fermeture, blocage) | Session hijacking · session fixation · réutilisation après expiration | *(mémoire — migration SQLite prévue)* | **ÉLEVÉ** — OWASP A07 · CWE-613 |
| `src/security/mfa_manager.py` | Authentification multi-facteurs pondérée (face=3 · voix=2 · appareil=2 · PIN=1) | Usurpation d'identité · compromission d'un seul facteur | `config/security/security_settings.json` | **ÉLEVÉ** — OWASP A07 |
| `src/security/access_control.py` | Vérification des permissions par rôle (RBAC) | Escalade de privilèges · accès non autorisé à des ressources | `logs/security/security.log` | **CRITIQUE** — OWASP A01 (Broken Access Control) |
| `src/security/permission_manager.py` | Matrice de permissions par rôle (OWNER→EMERGENCY) | Accès latéral · privilege creep | `config/security/roles_permissions.json` | **CRITIQUE** — OWASP A01 |
| `src/security/role_manager.py` | Définition et gestion des 7 rôles | Confusion de rôles · élévation de privilèges | `config/security/roles_permissions.json` | **ÉLEVÉ** — OWASP A01 |

---

## Politique Zero Trust

| Script | Rôle | Menaces prises en charge | Fichiers de suivi | Classe de risque |
|--------|------|--------------------------|-------------------|-----------------|
| `src/security/zero_trust_orchestrator.py` | Orchestration du pipeline Zero Trust en 6 étapes (input → threat → device → access → policy → audit) | Toutes menaces combinées — aucune étape ne peut être contournée isolément | `logs/security/audit_trail.jsonl` · `logs/security/security.log` | **CRITIQUE** — Architecture globale |
| `src/security/policy_engine.py` | Évaluation des règles de politique (sensibilité ressource, action, rôle) | Accès à des ressources CRITICAL par des rôles non autorisés · actions destructives non autorisées | `config/security/zero_trust_rules.json` | **CRITIQUE** — OWASP A01 |
| `src/security/policy_decision_point.py` | Point de décision centralisé (PDP) — retourne ALLOW / DENY | Tentative de contournement de politique | `config/security/zero_trust_rules.json` | **ÉLEVÉ** — Architecture Zero Trust |
| `src/security/policy_enforcement_point.py` | Point d'application (PEP) — exécute la décision du PDP · fail-secure par défaut | Décisions inconnues ou ambiguës → refus systématique | `logs/security/audit_trail.jsonl` | **ÉLEVÉ** — CWE-636 (fail-open) |
| `src/security/device_registry.py` | Registre des appareils de confiance · vérification et révocation | Appareil non reconnu · appareil compromis · connexion depuis matériel inconnu | `data/security/trusted_devices.json` · `logs/security/security.log` | **ÉLEVÉ** — OWASP A07 · CWE-287 |

---

## Chiffrement et protection des données

| Script | Rôle | Menaces prises en charge | Fichiers de suivi | Classe de risque |
|--------|------|--------------------------|-------------------|-----------------|
| `src/security/encryption_service.py` | Chiffrement / déchiffrement Fernet (AES-128-CBC + HMAC-SHA256) · rotation de clé | Lecture des données au repos · exfiltration de fichiers | *(clé dans variable d'env `FERNET_KEY`)* | **CRITIQUE** — OWASP A02 · CWE-311 |
| `src/security/data_protection.py` | Chiffrement sélectif des champs sensibles dans les JSON (`password`, `token`, `api_key`, etc.) | Exposition de secrets dans les fichiers de données utilisateur | `logs/security/security.log` | **ÉLEVÉ** — OWASP A02 · CWE-312 |
| `src/security/secret_manager.py` | Validation des secrets critiques au démarrage (SECRET_KEY, FERNET_KEY, PIN_SALT) | Démarrage avec secrets par défaut ou manquants | `.env` (exclu de Git) | **CRITIQUE** — OWASP A05 (Mauvaise config) |
| `src/security/backup_security.py` | Vérification de l'intégrité des sauvegardes | Corruption de backup · substitution de données · restauration malveillante | *(à configurer)* | **MOYEN** — CWE-354 |

---

## Détection et réponse aux incidents

| Script | Rôle | Menaces prises en charge | Fichiers de suivi | Classe de risque |
|--------|------|--------------------------|-------------------|-----------------|
| `src/security/incident_manager.py` | Enregistrement structuré des incidents de sécurité (level, status, source) | Traçabilité des événements critiques · gestion des incidents ouverts | `data/security/incident_register.json` | **ÉLEVÉ** — OWASP A09 (Logging) |
| `src/security/behavioral_detector.py` | Détection d'anomalies comportementales (écart vs baseline + score) | Comportement anormal d'un utilisateur · dérive de session · usage atypique | *(score en mémoire)* | **MOYEN** — CWE-754 |
| `src/security/quarantine_service.py` | Isolation des données suspectes | Contamination de la mémoire · données corrompues ou malveillantes | *(à configurer)* | **MOYEN** — Architecture défensive |
| `src/security/prompt_guard.py` | Protection contre les injections de prompts dans les chaînes LLM | Jailbreak · extraction de contexte système · manipulation du LLM | `logs/security/security.log` | **ÉLEVÉ** — Spécifique LLM |

---

## Journalisation et traçabilité

| Script | Rôle | Menaces prises en charge | Fichiers de suivi | Classe de risque |
|--------|------|--------------------------|-------------------|-----------------|
| `src/security/audit_trail.py` | Journal JSONL horodaté UTC de tous les événements d'accès (user · action · resource · decision) | Non-répudiation · investigation post-incident · conformité GDPR | `logs/security/audit_trail.jsonl` | **ÉLEVÉ** — OWASP A09 · GDPR Art.30 |
| `src/security/security_logger.py` | Logger dédié sécurité (INFO/WARNING/ERROR/CRITICAL) · `log_access()` · `log_auth()` | Traçabilité des événements d'authentification et d'accès | `logs/security/security.log` | **ÉLEVÉ** — OWASP A09 |
| `src/security/compliance_manager.py` | Suivi de la conformité réglementaire | Non-conformité GDPR · drift de configuration | `config/security/audit_retention_policy.json` | **MOYEN** — GDPR · ISO 27001 |

---

## Gouvernance et monitoring

| Script | Rôle | Menaces prises en charge | Fichiers de suivi | Classe de risque |
|--------|------|--------------------------|-------------------|-----------------|
| `src/security/security_dashboard.py` | Score de sécurité 0-100 · conformité GDPR/OWASP · résumé menaces/incidents · rapport | Posture de sécurité dégradée non détectée · accumulation silencieuse de risques | `logs/security/audit_trail.jsonl` · `data/security/incident_register.json` | Monitoring transverse |
| `src/security/security_governance.py` | 13 contrôles de durcissement · matrice de risques (likelihood × impact) · recommandations CRITICAL→LOW | Dérives de configuration · lacunes non traitées · risques non prioritisés | Tous les fichiers de config sécurité | Gouvernance transverse |

---

## Configuration de sécurité

| Fichier | Rôle | Menaces prises en charge | Utilisé par | Classe de risque |
|---------|------|--------------------------|-------------|-----------------|
| `config/security/roles_permissions.json` | Matrice RBAC — 7 rôles · permissions · MFA · timeout session | Escalade de privilèges · accès non autorisé | `permission_manager.py` · `access_control.py` | **CRITIQUE** — OWASP A01 |
| `config/security/zero_trust_rules.json` | 8 règles Zero Trust (ZT-001→ZT-007 + DEFAULT) | Accès à ressources critiques · actions destructives non autorisées | `policy_engine.py` | **CRITIQUE** — Architecture ZT |
| `config/security/security_settings.json` | Paramètres globaux : méthode chiffrement · MFA requis | MFA contourné · chiffrement faible | `mfa_manager.py` | **ÉLEVÉ** — Configuration |
| `config/security/audit_retention_policy.json` | Politique de rétention des logs d'audit | Suppression non autorisée de journaux · non-conformité GDPR | `compliance_manager.py` | **MOYEN** — GDPR Art.5 |
| `config/security/trusted_devices.json` | Configuration initiale du registre d'appareils | Appareils non autorisés | `device_registry.py` | **ÉLEVÉ** — OWASP A07 |

---

## Tests de sécurité automatisés

| Script | Rôle | Menaces testées | Résultat | Classe de risque couverte |
|--------|------|-----------------|----------|--------------------------|
| `tests/security/test_pentest_input.py` | Tests d'intrusion — vecteurs d'injection | SQL (8) · XSS (8) · path traversal (5) · prompt injection (8) · command injection (6) · edge cases (8) = **43 tests** | 43/43 ✅ | CRITIQUE — OWASP A03 |
| `tests/security/test_pentest_auth.py` | Tests d'intrusion — authentification | Brute-force · backoff · lockout · isolation utilisateurs · session lifecycle · PIN bcrypt = **20 tests** | 20/20 ✅ | CRITIQUE — OWASP A07 |
| `tests/security/test_pentest_encryption.py` | Tests d'intrusion — chiffrement | Round-trip · IV aléatoire · falsification token · protection champs · insensibilité casse = **16 tests** | 16/16 ✅ | ÉLEVÉ — OWASP A02 |
| `tests/security/test_pentest_zero_trust.py` | Tests d'intrusion — orchestrateur Zero Trust | Payloads malveillants · appareil inconnu · permission insuffisante · ressource critique · happy path = **13 tests** | 13/13 ✅ | CRITIQUE — Architecture ZT |
| `tests/security/test_pentest_dashboard_governance.py` | Tests dashboard et gouvernance | Score/grade · compliance structure · matrice risques · idempotence · filtrage priorité = **44 tests** | 44/44 ✅ | Monitoring |

---

## Intégration dans le point d'entrée principal

| Point d'intégration | Module appelé | Quand | Effet |
|--------------------|---------------|-------|-------|
| `src/main.py` — démarrage | `device_registry.init_default_device()` | Au lancement d'ALFRED | Enregistrement de l'appareil local dans le registre de confiance |
| `src/main.py` — démarrage | `audit_trail.write_audit_event()` | Au lancement | Événement STARTUP tracé dans l'audit trail |
| `src/main.py` — boucle principale | `input_validator.sanitize_input()` | Chaque saisie utilisateur | Rejet des inputs malveillants (25 patterns) |
| `src/main.py` — boucle principale | `threat_detector.detect_threat()` | Chaque saisie validée | Blocage si score de menace ≥ 3 |
| `src/main.py` — boucle principale | `output_filter.filter_output()` | Chaque réponse générée | Masquage des données sensibles avant affichage |
| `src/main.py` — boucle principale | `audit_trail.write_audit_event()` | Chaque échange | Trace CONVERSATION/ALLOW dans l'audit trail |
| `src/main.py` — commande `reset` | `audit_trail.write_audit_event()` | Commande de suppression | Trace DELETE_DATA dans l'audit trail |

---

## Synthèse par classe de risque OWASP

| Classe OWASP | Modules couvrants | Statut |
|--------------|-------------------|--------|
| **A01 — Contrôle d'accès** | `access_control`, `permission_manager`, `role_manager`, `policy_engine`, `zero_trust_orchestrator` | ✅ Couvert |
| **A02 — Exposition de données** | `encryption_service`, `data_protection`, `output_filter` | ✅ Couvert |
| **A03 — Injection** | `input_validator`, `threat_detector`, `prompt_guard` | ✅ Couvert |
| **A04 — Design non sécurisé** | `rate_limiter`, `policy_enforcement_point` (fail-secure) | ✅ Couvert |
| **A05 — Mauvaise configuration** | `secret_manager`, `security_governance`, `roles_permissions.json` | ✅ Couvert |
| **A07 — Auth et identification** | `authenticator`, `session_manager`, `mfa_manager`, `device_registry` | ✅ Couvert |
| **A09 — Logging et monitoring** | `audit_trail`, `security_logger`, `incident_manager`, `security_dashboard` | ✅ Couvert |
| **A06 — Composants vulnérables** | *(pip-audit prévu en CI)* | ⚠️ Partiel |
| **A08 — Intégrité** | `backup_security` | ⚠️ À compléter |
| **A10 — SSRF** | `input_validator` (patterns localhost/ldap) | ✅ Couvert |

---

*Document mis à jour : Bloc 20 — Sécurité ALFRED.*
*Aucune clé, secret, token ou vecteur d'exploitation n'est divulgué dans ce document.*
