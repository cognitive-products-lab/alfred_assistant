<!--
============================================================
PROJECT  : ALFRED / Cognitive Products Lab
BLOCK    : B20 — Sécurité, Gouvernance & Conformité
DOCUMENT : Politique de Sécurité du Système d'Information (SMSI)
TYPE     : Documentation SMSI
REF      : ISO/IEC 27001:2022 — A.5.1
VERSION  : V1.1
CREATED  : 2026-06-18
UPDATED  : 2026-07-10
AUTHOR   : Cognitive Products Lab — Céline Rousselot (rédaction assistée Claude)
STATUS   : Approuvé
============================================================
-->
# Politique de Sécurité du Système d'Information (SMSI)
## Cognitive Products Lab — ALFRED

> **Référence :** ISO/IEC 27001:2022 — Contrôle A.5.1
> **Version :** 1.1 — 2026-07-10
> **Approbation :** Céline Rousselot — Fondatrice / Directrice Générale
> **Statut :** Approuvé
> Version précédente (V1.0, mai 2026) : `docs/security/politique_cybersecurite_alfred.pdf` — ce document markdown en est la version maître mise à jour, à régénérer en PDF pour diffusion.

---

## 1. Déclaration d'intention

La cybersécurité n'est pas une fonctionnalité d'ALFRED — c'est son fondement. Chaque ligne de code, chaque décision d'architecture, chaque interaction utilisateur est conçue avec la sécurité comme contrainte primaire, non comme contrainte ajoutée après développement.

ALFRED traite des données personnelles sensibles : mémoire conversationnelle, données émotionnelles, données de santé (ARTHUR), et depuis juillet 2026, des comptes utilisateurs pour le déploiement public d'ALFRED_WEB (PostgreSQL) et une mémoire conversationnelle web (MongoDB). Cette responsabilité impose un niveau d'exigence maximal, à chaque nouveau composant.

**Approuvé par :** Céline Rousselot — Fondatrice, Cognitive Products Lab
**Date d'approbation :** 2026-06-18 (V1.0), révisé 2026-07-10 (V1.1)

---

## 2. Périmètre du SMSI

Le SMSI couvre :
- L'infrastructure ALFRED_PC (Minisforum MS-S1 Max — réseau domestique segmenté VLAN)
- L'infrastructure ALFRED_WEB (site public, PostgreSQL et MongoDB en Docker local à ce stade)
- Les données personnelles des utilisateurs (ALFRED local + futurs comptes ALFRED_WEB)
- Les systèmes de développement, de test et de production
- Les outils et services tiers (OpenAI API)
- Le code source et la propriété intellectuelle CPL

---

## 3. Les 8 principes non négociables

| Principe | Définition | Application ALFRED |
|---|---|---|
| **Local-First** | Les données sont traitées et stockées localement par défaut | Aucune donnée utilisateur transmise vers un serveur cloud sans consentement explicite |
| **Zero Trust** | Aucune confiance implicite — tout accès est vérifié, même en interne | Pipeline à 9 couches (§4) |
| **Security by Design** | La sécurité est intégrée dès la conception, pas ajoutée a posteriori | Chaque nouveau module intègre validation, logging et contrôle d'accès dès le premier commit — appliqué à PostgreSQL/MongoDB/Hadoop en juillet 2026 (CSRF, bcrypt, isolation par user_id, anonymisation avant traitement) |
| **Privacy by Design** | La protection des données personnelles est intégrée à l'architecture | Minimisation des données, chiffrement systématique, durées de rétention définies |
| **Fail-Safe** | En cas de doute ou d'erreur, le système refuse par défaut | Toute requête non validée est rejetée. Silence = refus. Dégradation propre si base injoignable (503, pas de crash) |
| **Least Privilege** | Chaque composant n'a accès qu'aux ressources strictement nécessaires | 7 rôles RBAC. Isolation stricte par `user_id` sur les nouvelles routes web (404, pas 403, pour ne pas révéler l'existence d'une ressource) |
| **Defense in Depth** | Multiplication des couches de protection indépendantes | Input → Threat → Device → Auth → MFA → RBAC → Policy → Output : 8 couches |
| **Auditabilité** | Toute action significative est tracée et consultable | Audit trail JSONL UTC, logs sécurité, dashboards temps réel, couverture de tests (1289 tests ALFRED_PC + 32 tests ALFRED_WEB au 09/07/2026) |

---

## 4. Architecture de sécurité — pipeline Zero Trust (ALFRED_PC)

Chaque requête utilisateur traverse obligatoirement les couches suivantes, dans cet ordre. Un refus à n'importe quelle couche arrête le traitement.

| # | Couche | Module principal | Contrôles | Latence |
|---|---|---|---|---|
| 1 | Validation entrée | `input_validator.py` | 25 patterns : SQLi, XSS, path traversal, cmd injection, prompt injection, SSRF, LDAP, null bytes | Immédiat |
| 2 | Détection menace | `threat_detector.py` + `behavioral_detector.py` | Score de menace calculé, analyse comportementale | < 10ms |
| 3 | Contrôle appareil | `device_registry.py` | Trust score appareil, appareils non reconnus rejetés | < 5ms |
| 4 | Authentification | `authenticator.py` | bcrypt rounds=12, PIN local, gestion sessions, anti brute-force | < 50ms |
| 5 | MFA | `mfa_manager.py` | TOTP RFC 6238, MFA appareil, secrets chiffrés | < 30ms |
| 6 | RBAC | `role_manager.py` + `permission_manager.py` | 7 rôles : OWNER / ADMIN / USER / GUEST / SERVICE / AI_MODULE / EMERGENCY | < 5ms |
| 7 | Politique Zero Trust | `policy_engine.py` + `zero_trust_orchestrator.py` | PDP/PEP, décision finale, refus par défaut | < 10ms |
| 8 | Filtrage sortie | `output_filter.py` | Masquage clés API, JWT, passwords, tokens, secrets | < 5ms |
| 9 | Audit trail | `audit_trail.py` + `security_logger.py` | Journalisation JSONL UTC, horodatage, immuable | Asynchrone |

### 4.1 Côté ALFRED_WEB (juillet 2026) — modèle simplifié adapté au contexte public

ALFRED_WEB (site public, framework Flask) applique un sous-ensemble adapté au contexte web plutôt que le pipeline complet à 9 couches (celui-ci reste spécifique à ALFRED_PC, application locale mono-utilisateur) :

| Contrôle | Implémentation |
|---|---|
| Hachage mots de passe | bcrypt, `auth/routes.py` |
| Protection CSRF | Jeton de session sur toutes les routes d'écriture (comptes, préférences, conversations) |
| Isolation par utilisateur | Filtrage `user_id` systématique, testé (32 tests) |
| Dégradation propre | 503 si PostgreSQL/MongoDB injoignable, jamais de crash (`data/postgres.py`, `data/mongo.py`) |
| Consentement horodaté et séparé par finalité | `consent_at` (comptes), `preferences_consent_at` (préférences) |

**Gap identifié et documenté (AIPD-ALFRED-002, non corrigé à ce jour)** : pas de rate limiting sur `/auth/login` et `/auth/register` — action requise avant toute ouverture publique réelle.

---

## 5. Règles de développement sécurisé (Secure SDLC)

### 5.1 Règles absolues

- **JAMAIS** de secret en clair dans le code (clés API, mots de passe, tokens) → `.env` + `python-dotenv`
- **JAMAIS** de `.env` dans Git → `.gitignore` exclut `.env`, `*.key`, `data/`, secrets
- **JAMAIS** de `except Exception:` sans logging → toute exception loggée via `security_logger`
- **JAMAIS** de permission accordée sans validation RBAC/isolation → toute route sensible vérifie l'accès
- **JAMAIS** de donnée persistante sensible non protégée → chiffrement (ALFRED_PC) ou hachage (mots de passe ALFRED_WEB)
- **TOUJOURS** valider les inputs avant tout traitement
- **TOUJOURS** écrire un test pour chaque fonction de sécurité — **1 script = 1 test**, sans exception (principe appliqué explicitement le 09/07/2026 sur le PoC Hadoop : `tests/b29_tests/`, 24 tests pour 4 scripts)

### 5.2 Processus de développement sécurisé

| Phase | Exigences sécurité |
|---|---|
| Conception | Revue d'architecture avant développement, réflexion RGPD/AIPD dès la conception (cf. `docs/gouvernance/politique_gouvernance.md` §5) |
| Développement | Secure coding rules, headers de métadonnées à jour sur chaque fichier |
| Test | Tests unitaires sécurité obligatoires pour chaque script — contre les systèmes réels quand c'est possible (PostgreSQL/MongoDB/Hadoop réels, pas de mocks systématiques) |
| Revue | Vérification `.gitignore`, absence de secrets, cohérence des headers |
| Déploiement | Validation dégradation propre si dépendance externe injoignable |
| Maintenance | Audit régulier, mise à jour dépendances |

---

## 6. Gestion des identités et des accès

### 6.1 ALFRED_PC (local)

| Règle | Exigence |
|---|---|
| Longueur PIN | Minimum 6 chiffres |
| Hachage | bcrypt rounds=12 minimum |
| Tentatives | Blocage automatique après 5 tentatives échouées |
| Durée session | Expiration après 900 secondes d'inactivité |
| MFA | Obligatoire pour OWNER et ADMIN |

### 6.2 ALFRED_WEB (comptes publics, Bloc 21.23)

| Règle | Exigence |
|---|---|
| Longueur mot de passe | Minimum 10 caractères |
| Hachage | bcrypt |
| CSRF | Jeton de session sur register/login/logout et toute route d'écriture |
| Rate limiting | **Non implémenté — gap identifié, cf. §4.1** |

### 6.3 Rôles RBAC (ALFRED_PC)

| Rôle | Permissions | Règles d'attribution |
|---|---|---|
| OWNER | Accès total, administration sécurité | Réservé à la fondatrice, non délégable |
| ADMIN | Gestion utilisateurs, configuration modules | Attribution par OWNER, max 2 personnes |
| USER | Interaction ALFRED, lecture mémoire propre | Utilisateur final standard |
| GUEST | Lecture seule | Accès temporaire, max 24h |
| SERVICE | Accès API inter-modules | Modules internes uniquement |
| AI_MODULE | Accès lecture mémoire, génération réponses | Modules IA uniquement |
| EMERGENCY | Accès restreint d'urgence | Activation manuelle OWNER, audit obligatoire |

---

## 7. Politique de chiffrement et gestion des secrets

| Donnée | Méthode de protection |
|---|---|
| Données persistantes ALFRED_PC (JSON mémoire) | Fernet (AES 128-CBC + HMAC-SHA256), clé dans `.env` |
| Mots de passe ALFRED_PC (PIN) et ALFRED_WEB (comptes) | bcrypt, jamais stockés en clair |
| Secrets MFA (TOTP) | Chiffrés Fernet avant stockage |
| Clés API et tokens | Stockés dans `.env`, jamais dans le code |
| Sessions | Token signé, expiration, révocation possible |
| Logs sécurité | Stockage local uniquement |
| PostgreSQL (comptes ALFRED_WEB) | Identifiants via variables d'environnement (`POSTGRES_USER`/`POSTGRES_PASSWORD`), jamais en clair dans `docker-compose.yml` versionné |

**Règles critiques** : la clé Fernet est générée une seule fois et ne doit jamais être commitée dans Git. Rotation des clés planifiée (roadmap V2). Backup chiffré séparé du backup des données.

---

## 8. Conformité aux référentiels — couverture OWASP Top 10

| Réf. | Risque | Mesure ALFRED |
|---|---|---|
| A01 | Broken Access Control | RBAC 7 rôles + isolation `user_id` (web) + policy_engine + Zero Trust orchestrator |
| A02 | Cryptographic Failures | Fernet + bcrypt + TOTP + clés hors Git |
| A03 | Injection | 25 patterns input_validator + threat_detector |
| A04 | Insecure Design | Architecture Zero Trust + fail-safe + défense en profondeur |
| A05 | Security Misconfiguration | security_governance + dashboard conformité (§9) |
| A06 | Vulnerable Components | Tests automatisés + surveillance dépendances |
| A07 | Authentication Failures | bcrypt + MFA + CSRF + session timeout — **rate limiting web manquant, cf. §4.1** |
| A08 | Software/Data Integrity | audit_trail JSONL + chiffrement + gouvernance |
| A09 | Logging & Monitoring | security_dashboard + security_logger + audit_trail |
| A10 | SSRF | input_validator : patterns localhost + gopher + LDAP |

---

## 9. Gouvernance, dashboards et indicateurs

### 9.1 Rôles et responsabilités

| Rôle | Responsable | Missions |
|---|---|---|
| Directrice Générale / Fondatrice | Céline Rousselot | Approbation politique, décisions stratégiques sécurité |
| Responsable Sécurité (RSSI) de fait | Céline Rousselot | Implémentation, monitoring, incidents, audits |
| DPO de fait | Céline Rousselot | Conformité RGPD, droits des personnes, AIPD |

*Note : phase mono-fondatrice — Céline Rousselot cumule ces rôles (cf. `docs/smsi/raci_securite.md` pour le détail RACI par activité). Séparation des rôles prévue lors du recrutement.*

### 9.2 Dashboards de suivi

| Dashboard | Rôle | Périmètre actuel |
|---|---|---|
| `dashboard_data.json` | Statut fichiers (présent/codé/testé/validé) | ALFRED_PC + fichiers ALFRED_WEB explicitement ajoutés au manifest (blocs b21, b29) |
| `dashboard_tests.json` | Résultats de tests | ALFRED_PC uniquement (groupes `TEST_GROUPS` de `tests/run_all_tests.py`) — **ALFRED_WEB a sa propre suite pytest non intégrée ici**, trou de périmètre documenté dans `ALFRED_CONTEXT.md` |
| `dashboard_conformite.json` | 71 exigences réglementaires, 9 normes | RGPD, LIL, AI Act, NIS2, ISO 27001, CRA (actives) |
| `dashboard_gouvernance` | Vue croisée conformité + preuves | Recoupe déclaratif et fichiers réels sur disque, dégrade automatiquement le statut si preuve absente |

### 9.3 KPI de sécurité

| KPI | Objectif |
|---|---|
| Score sécurité global (dashboard) | ≥ 90/100 en permanence |
| Taux de conformité OWASP | ≥ 95% |
| Couverture tests sécurité | ≥ 80%, 100% sur modules critiques |
| Score conformité réglementaire global | Suivi honnête — pas d'optimisation artificielle (84%, Grade B au 10/07/2026, reflète un gate RGPD volontairement actif) |

---

## 10. Cadre réglementaire

CPL respecte et s'engage à maintenir la conformité avec (détail complet et statut par exigence : `docs/gouvernance/cadre_reglementaire_CPL.md`) :
- **RGPD** (Règlement UE 2016/679) — données personnelles
- **ISO/IEC 27001:2022** — management de la sécurité de l'information
- **EU AI Act** (Règlement UE 2024/1689) — IA responsable, transparence Art. 50
- **NIS2** (Directive UE 2022/2555) — hors champ légal (micro-entreprise, aucun secteur applicable), conformité volontaire assumée — cf. `docs/smsi/procedure_signalement_nis2.md`

---

## 11. Sanctions et non-conformités

Tout manquement à cette politique fait l'objet d'une action corrective documentée dans `docs/smsi/actions_correctives.md`. Les violations graves sont traitées selon `procedure_incidents.md`.

---

## 12. Révision

Cette politique est révisée annuellement et à chaque changement organisationnel ou réglementaire majeur.

| Version | Date | Auteur | Modification |
|---|---|---|---|
| 1.0 | 2026-06-18 | Céline Rousselot | Création — conformité ISO A.5.1 |
| 1.1 | 2026-07-10 | Céline Rousselot (rédaction assistée Claude) | Fusion avec le contenu du PDF `politique_cybersecurite_alfred.pdf` (pipeline Zero Trust détaillé, Secure SDLC, OWASP, KPIs) ; ajout du volet ALFRED_WEB (comptes PostgreSQL, gap rate limiting identifié) ; reformulation NIS2 hors champ/conformité volontaire ; ajout section dashboards |

> **Cognitive Products Lab — Confidentiel interne**
