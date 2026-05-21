# Bloc 20 — Sécurité ALFRED
## Tests d'intrusion · Dashboard · Gouvernance

---

## Table des matières

1. [Contexte et objectifs](#1-contexte-et-objectifs)
2. [Audit initial — état des lieux](#2-audit-initial--état-des-lieux)
3. [Architecture de sécurité retenue](#3-architecture-de-sécurité-retenue)
4. [Ce qui a été implémenté](#4-ce-qui-a-été-implémenté)
   - 4.1 Corrections critiques
   - 4.2 Nouveaux modules
   - 4.3 Dashboard de sécurité
   - 4.4 Gouvernance
   - 4.5 Suite de tests d'intrusion
5. [Résultats et métriques](#5-résultats-et-métriques)
6. [Flux de sécurité complet](#6-flux-de-sécurité-complet)
7. [Guide d'utilisation](#7-guide-dutilisation)
8. [Ce qui reste à faire](#8-ce-qui-reste-à-faire)

---

## 1. Contexte et objectifs

ALFRED est un assistant personnel local-first. Toutes les données restent sur l'appareil de l'utilisateur — aucun envoi vers le cloud. Ce choix architectural est la première ligne de défense GDPR.

Le Bloc 20 vise à couvrir trois axes complémentaires :

- **Tests d'intrusion** — vérifier automatiquement et en continu que les protections résistent aux attaques connues
- **Dashboard** — donner une vision en temps réel de la posture de sécurité
- **Gouvernance** — évaluer la conformité aux standards (OWASP Top 10, GDPR) et prioriser les actions correctives

---

## 2. Audit initial — état des lieux

Un audit de l'existant a révélé une architecture Zero Trust bien conçue (25 modules) mais avec plusieurs gaps critiques.

### Ce qui fonctionnait déjà

| Composant | État |
|-----------|------|
| Architecture Zero Trust (orchestrateur) | ✅ En place |
| Chiffrement Fernet (AES-128-CBC) | ✅ Opérationnel |
| Registre d'appareils de confiance | ✅ Fonctionnel |
| Audit trail JSONL horodaté | ✅ Actif |
| Filtre de sortie (données sensibles) | ✅ Basique |
| Journalisation sécurité structurée | ✅ Fonctionnel |
| Gestionnaire d'incidents | ✅ En place |

### Gaps identifiés (avant Bloc 20)

| Sévérité | Problème | Impact |
|----------|----------|--------|
| **CRITICAL** | RBAC vide — aucun rôle défini en config | Autorisations non appliquées |
| **CRITICAL** | Règles Zero Trust vides | Politique non appliquée |
| **CRITICAL** | Aucun module d'authentification | Identité non vérifiée |
| **HIGH** | Clé de chiffrement stockée en fichier disque | Compromission si accès fichier |
| **HIGH** | Aucun rate limiting | Brute-force possible |
| **HIGH** | Patterns d'injection trop limités (7 patterns) | Contournements possibles |
| **HIGH** | Patterns appliqués après html.escape | XSS `<script>` non bloqué |
| **MEDIUM** | MFA désactivé en config | 2e facteur inactif |
| **MEDIUM** | Aucun test de sécurité automatisé | Régressions non détectées |
| **MEDIUM** | Filtre de sortie basique (remplacement de chaînes) | JWT/API keys non masqués |

---

## 3. Architecture de sécurité retenue

### Principe Zero Trust — "Ne jamais faire confiance, toujours vérifier"

Chaque requête passe par un pipeline obligatoire avant d'être autorisée :

```
Entrée utilisateur
       │
       ▼
┌─────────────────┐
│  1. Validation  │  → Normalisation unicode, null bytes, longueur, 25 patterns
│     d'entrée    │
└────────┬────────┘
         │ OK
         ▼
┌─────────────────┐
│  2. Détection   │  → Score de menace (keywords + anomalies comportementales)
│    de menace    │
└────────┬────────┘
         │ score < seuil
         ▼
┌─────────────────┐
│  3. Vérification│  → Appareil connu et approuvé dans le registre
│    d'appareil   │
└────────┬────────┘
         │ appareil de confiance
         ▼
┌─────────────────┐
│  4. Contrôle    │  → Rôle de l'utilisateur vs permissions requises (RBAC)
│    d'accès      │
└────────┬────────┘
         │ permission accordée
         ▼
┌─────────────────┐
│  5. Politique   │  → Règles Zero Trust (sensibilité ressource, action)
│    Zero Trust   │
└────────┬────────┘
         │ décision = ALLOW
         ▼
┌─────────────────┐
│  6. Audit trail │  → Événement JSONL horodaté UTC signé
└─────────────────┘
         │
         ▼
    ✅ AUTORISÉ
```

Chaque étape échoue-sûre : tout résultat inconnu → refus.

### Modèle de rôles (RBAC)

| Rôle | Permissions clés | MFA requis | Timeout session |
|------|-----------------|------------|----------------|
| OWNER | Toutes (10) | Oui | 60 min |
| ADMIN | Lecture/écriture mémoire, logs, appareils | Oui | 30 min |
| USER | Lecture/écriture mémoire, IA | Non | 15 min |
| GUEST | IA uniquement | Non | 5 min |
| SERVICE | IA uniquement | Non | 10 min |
| AI_MODULE | IA uniquement | Non | 10 min |
| EMERGENCY | Alertes, contexte d'urgence | Non | 2 min |

---

## 4. Ce qui a été implémenté

### 4.1 Corrections critiques

#### Validation des entrées renforcée (`input_validator.py`)

**Problème** : 7 patterns basiques, appliqués après `html.escape()`. Un payload `<script>alert(1)</script>` devenait `&lt;script&gt;alert(1)&lt;/script&gt;` — les patterns ne matchaient plus rien.

**Solution** :
- Normalisation unicode NFKC en premier (bloque les attaques homoglyphes : `ｓcript` → `script`)
- Détection des null bytes (vecteur d'injection)
- **25 patterns** compilés couvrant :
  - SQL injection (DDL, DML, UNION SELECT, EXEC, tautologies)
  - XSS (script tags, event handlers, javascript: URI, iframes)
  - Path traversal (`../`, `..\\`, chemins système)
  - Command injection (shell invocation, command substitution, netcat)
  - Prompt injection (jailbreak, bypass safety, extraction de contexte)
  - SSRF / LDAP injection
- Patterns appliqués **avant** `html.escape()` — l'input brut est analysé
- `html.escape()` appliqué en sortie pour la sécurité de rendu

#### RBAC et règles Zero Trust (`roles_permissions.json`, `zero_trust_rules.json`)

**Problème** : Les fichiers de configuration existaient mais étaient vides (`{"roles": {}}`, `{"rules": []}`). L'architecture était présente mais sans données.

**Solution** : Population complète des 7 rôles et de 8 règles Zero Trust explicites (ZT-001 à ZT-007 + règle par défaut ALLOW).

#### Rate Limiter (`rate_limiter.py`)

**Problème** : Le compteur d'échecs existait mais sans délai de blocage — un attaquant pouvait tenter indéfiniment.

**Solution** : Fenêtre glissante de 60 secondes, maximum 5 tentatives, puis blocage avec **backoff exponentiel** :

```
Tentatives 5 → 6 : blocage 30s
Tentatives 6 → 7 : blocage 60s
Tentatives 7 → 8 : blocage 120s
...
```

Implémentation thread-safe (verrou Python). Chaque identifiant (user_id) est isolé.

#### Clé de chiffrement dans variable d'environnement

**Problème** : La clé Fernet (utilisée pour chiffrer les données sensibles) était stockée dans un fichier sur le disque. Si un attaquant accédait au système de fichiers, il obtenait simultanément les données chiffrées ET la clé — rendant le chiffrement inutile.

**Solution** :
- Clé déplacée dans la variable d'environnement `FERNET_KEY` (fichier `.env`, exclu de Git)
- Fichier clé disque supprimé
- Le fichier `.env` n'est jamais commité (règle `.gitignore`)

**Pourquoi c'est mieux** : Les variables d'environnement sont en mémoire, séparées du système de fichiers. Un accès aux fichiers ne suffit plus à compromettre le chiffrement.

#### Module d'authentification (`src/auth/authenticator.py`)

**Problème** : Le répertoire `src/auth/` existait mais ne contenait qu'un `__init__.py` vide. Aucune vérification d'identité n'était réalisée.

**Solution** : Authentification par code PIN avec :
- **bcrypt** (12 rounds) : hachage lent et résistant au brute-force GPU
- **Sel aléatoire** par utilisateur (16 bytes d'entropie) : rend les rainbow tables inutilisables
- **Rate limiter intégré** : blocage automatique après 5 échecs
- Fonctions : `register_pin()`, `authenticate()`, `change_pin()`, `has_pin()`

**Pourquoi bcrypt** : Contrairement à SHA-256 (microseconde par hash), bcrypt est intentionnellement lent (100ms+). Brute-forcer 1 million de PINs prendrait des années.

#### Protection des données au repos (`data_protection.py`)

**Problème** : Les profils utilisateurs, l'historique de dialogue et les préférences étaient stockés en JSON en clair.

**Solution** : Module de chiffrement sélectif des champs sensibles :
- `protect_dict(data)` : chiffre automatiquement les champs `password`, `api_key`, `token`, `secret`, etc.
- `expose_dict(data)` : déchiffre pour utilisation
- `write_protected_json()` / `read_protected_json()` : lecture/écriture transparente

Les champs non sensibles (nom, préférences, timestamps) restent lisibles pour faciliter le débogage.

#### Filtre de sortie renforcé (`output_filter.py`)

**Problème** : Remplacement simple de chaînes fixes. Un JWT ou une clé API dans une réponse n'était pas masqué.

**Solution** : Ajout de regex pour détecter les patterns de tokens courants :
- JWT (`eyJ...`)
- Clés API de style industriel (`sk-...`, `pk-...`)
- Tokens GitHub (`ghp_`, `gho_`, etc.)
- Chaînes base64 longues (>40 caractères)

#### MFA activé

**Problème** : La configuration avait `mfa_required: false`. Le module MFA (pondération face/voix/PIN/appareil) existait mais n'était jamais appelé.

**Solution** : `mfa_required: true` dans `security_settings.json`. L'intégration complète de la vérification MFA dans le flux Zero Trust est documentée comme prochaine étape.

---

### 4.2 Nouveaux modules

#### `src/security/rate_limiter.py`

```python
# Utilisation
from src.security.rate_limiter import is_rate_limited, record_attempt, reset

limited, retry_after = is_rate_limited("user_id")
if limited:
    return f"Réessayez dans {retry_after:.0f}s"

# Après une tentative
record_attempt("user_id", success=False)  # échec → incrémente
record_attempt("user_id", success=True)   # succès → réinitialise
```

#### `src/security/data_protection.py`

```python
from src.security.data_protection import protect_dict, expose_dict

# Écriture (les champs sensibles sont chiffrés)
protected = protect_dict({"username": "alice", "password": "***"})
# → {"username": "alice", "password": "gAAAAABm..."}

# Lecture (déchiffrement transparent)
clear = expose_dict(protected)
# → {"username": "alice", "password": "***"}
```

#### `src/auth/authenticator.py`

```python
from src.auth.authenticator import register_pin, authenticate

# Enregistrement (une seule fois)
register_pin("alice", "1234")

# Authentification
result = authenticate("alice", "1234")
# → {"success": True, "reason": "Authentification réussie"}
```

---

### 4.3 Dashboard de sécurité (`security_dashboard.py`)

Le dashboard agrège en temps réel :

| Métrique | Source | Description |
|----------|--------|-------------|
| Score global (0-100) | Analyse de configuration | Grade A (≥90), B (≥75), C (≥60), D (≥40), F (<40) |
| Conformité GDPR/OWASP | Vérification fichiers | 10 points de contrôle |
| Menaces détectées | `audit_trail.jsonl` | Comptage sur fenêtre glissante |
| Incidents ouverts | `incident_register.json` | Filtrés par sévérité |
| Appareils | `trusted_devices.json` | Approuvés vs révoqués |

**Calcul du score** : Le score part de 100 et des points sont déduits pour chaque lacune détectée :

| Lacune | Déduction |
|--------|-----------|
| Clé Fernet manquante | -20 |
| Module d'auth absent | -20 |
| RBAC vide | -15 |
| Incidents critiques ouverts | -15 |
| Règles Zero Trust vides | -10 |
| Rate limiter absent | -10 |
| Volume de menaces élevé (>10/24h) | -10 |
| Audit trail vide | -5 |

**Utilisation** :

```python
from src.security.security_dashboard import get_dashboard

dashboard = get_dashboard(lookback_hours=24)
print(dashboard.generate_report())

score = dashboard.get_security_score()
# → {"score": 100, "grade": "A", "deductions": []}

compliance = dashboard.get_compliance_status()
# → {"total": 10, "passed": 10, "compliance_rate": 100.0, "checks": [...]}
```

---

### 4.4 Gouvernance (`security_governance.py`)

Le module de gouvernance effectue 13 contrôles de durcissement et produit une matrice de risques.

**Les 13 contrôles** :

| # | Catégorie | Contrôle | Sévérité |
|---|-----------|----------|----------|
| 1 | AUTHENTIFICATION | Module PIN (bcrypt) | CRITICAL |
| 2 | CHIFFREMENT | Clé Fernet en variable d'env (non fichier) | HIGH |
| 3 | CHIFFREMENT | Module de protection des données au repos | HIGH |
| 4 | AUTORISATION | RBAC configuré avec rôles réels | CRITICAL |
| 5 | POLITIQUE | Règles Zero Trust définies | HIGH |
| 6 | RÉSILIENCE | Rate limiter avec backoff exponentiel | HIGH |
| 7 | VALIDATION | Validateur d'entrée (patterns étendus) | HIGH |
| 8 | TRAÇABILITÉ | Audit trail actif et non vide | MEDIUM |
| 9 | TRAÇABILITÉ | Registre d'incidents | MEDIUM |
| 10 | TESTS | Suite de tests d'intrusion | MEDIUM |
| 11 | AUTHENTIFICATION | MFA activé en configuration | MEDIUM |
| 12 | SECRETS | .gitignore protège .env et *.key | CRITICAL |
| 13 | DONNÉES | Filtre de sortie des données sensibles | MEDIUM |

**Matrice de risques** : chaque non-conformité est évaluée selon `score = vraisemblance × impact` pour prioriser les actions correctives.

**Utilisation** :

```python
from src.security.security_governance import SecurityGovernance

gov = SecurityGovernance()

# Rapport complet
print(gov.generate_governance_report())

# Recommandations CRITICAL en priorité
for rec in gov.get_recommendations(priority="CRITICAL"):
    print(f"[{rec['category']}] {rec['action']}")

# Matrice de risques triée
risks = gov.get_risk_matrix()
```

---

### 4.5 Suite de tests d'intrusion (`tests/security/`)

**Philosophie** : les tests de sécurité vérifient que les protections *résistent* aux attaques, pas seulement qu'elles *existent*. Chaque payload utilisé est un vrai vecteur d'attaque documenté.

#### `test_pentest_input.py` — Vecteurs d'injection

| Classe | Payloads testés | Exemple |
|--------|----------------|---------|
| SQL injection | 8 | `'; DROP TABLE users; --` |
| XSS | 8 | `<script>alert(1)</script>` |
| Path traversal | 5 | `../../etc/passwd` |
| Prompt injection | 8 | `Ignore previous instructions` |
| Command injection | 6 | `$(id)`, `` `whoami` `` |
| Edge cases | 8 | Null bytes, longueur, unicode, types invalides |

#### `test_pentest_auth.py` — Authentification

- Brute-force : blocage après 5 échecs
- Backoff exponentiel : délai croissant vérifié
- Isolation : un utilisateur bloqué n'affecte pas les autres
- Session : création, validité, fermeture
- PIN : enregistrement, vérification, rejet des PINs trop courts

#### `test_pentest_encryption.py` — Chiffrement

- Round-trip encrypt/decrypt
- IV aléatoire : même message → tokens différents (résistance aux attaques par fréquence)
- Falsification : token modifié → rejet
- Protection des champs sensibles par défaut
- Insensibilité à la casse des noms de champs (`PASSWORD` = `password`)

#### `test_pentest_zero_trust.py` — Orchestrateur complet

- Payload malveillant → refus (quel que soit le rôle)
- Appareil inconnu → refus avec message explicite
- Permission insuffisante → refus
- Ressource critique + rôle USER → refus
- Ressource critique + rôle OWNER → autorisation
- Chemin nominal (happy path) → autorisation + cleaned_input

#### `test_pentest_dashboard_governance.py` — Métriques

- Score dans la plage 0-100
- Cohérence grade/score
- Structure des objets retournés
- Idempotence des contrôles
- Filtrage par priorité

---

## 5. Résultats et métriques

### Score de sécurité final

```
Score global : 100/100  (grade A)
Conformité   : 10/10 checks (100%)
Gouvernance  : 13/13 contrôles (100%)
Tests        : 136/136 passed
```

### Avant / Après

| Indicateur | Avant Bloc 20 | Après Bloc 20 |
|------------|--------------|--------------|
| Score sécurité | ~45/100 (grade D) | 100/100 (grade A) |
| Contrôles durcissement | 3/13 | 13/13 |
| Patterns d'injection bloqués | 7 | 25 |
| Tests de sécurité automatisés | 0 | 136 |
| Rate limiting | ❌ | ✅ backoff exponentiel |
| Auth PIN | ❌ | ✅ bcrypt rounds=12 |
| Clé en fichier disque | ❌ exposée | ✅ variable d'env |
| MFA | ❌ désactivé | ✅ activé |
| RBAC | ❌ vide | ✅ 7 rôles |
| Règles Zero Trust | ❌ vides | ✅ 8 règles |

---

## 6. Flux de sécurité complet

### Authentification (nouveau)

```
Utilisateur entre son PIN
         │
         ▼
  Rate limiter vérifie
  (bloqué si >5 échecs/60s)
         │ non bloqué
         ▼
  bcrypt.checkpw(pin + sel, hash_stocké)
         │
     ┌───┴───┐
   ✅ OK   ❌ KO
     │       │
  Session  record_attempt(false)
  créée    → backoff si seuil atteint
```

### Traitement d'une requête (pipeline Zero Trust)

```
[Input brut]
     │ normalisation NFKC + null bytes
     │ 25 patterns sécurité
     │ html.escape()
     ▼
[Détection menace]
     │ score < 3
     ▼
[Appareil]     ← registre trusted_devices.json
     │ trusted=true
     ▼
[Permission]   ← RBAC roles_permissions.json
     │ permission in role.permissions
     ▼
[Politique]    ← zero_trust_rules.json (8 règles)
     │ ALLOW
     ▼
[Audit]        → audit_trail.jsonl (horodaté UTC)
     │
     ▼
[Réponse]      → filter_output() avant rendu
```

---

## 7. Guide d'utilisation

### Générer un rapport de sécurité

```python
from src.security.security_dashboard import get_dashboard

dashboard = get_dashboard()
print(dashboard.generate_report())
```

### Lancer un audit de gouvernance

```python
from src.security.security_governance import SecurityGovernance

gov = SecurityGovernance()
print(gov.generate_governance_report())

# Actions prioritaires uniquement
for rec in gov.get_recommendations(priority="CRITICAL"):
    print(f"→ {rec['action']}")
```

### Lancer les tests d'intrusion

```bash
python -m pytest tests/security/ -v
```

### Enregistrer un utilisateur

```python
from src.auth.authenticator import register_pin
register_pin("alice", "mon_code_pin")
```

### Authentifier un utilisateur

```python
from src.auth.authenticator import authenticate
result = authenticate("alice", "mon_code_pin")
if result["success"]:
    # démarrer la session
    pass
```

### Protéger des données sensibles avant stockage

```python
from src.security.data_protection import write_protected_json, read_protected_json
from pathlib import Path

# Écriture (champs sensibles chiffrés automatiquement)
write_protected_json(Path("data/users/alice.json"), {"username": "alice", "token": "secret"})

# Lecture (déchiffrement automatique)
data = read_protected_json(Path("data/users/alice.json"))
```

---

## 8. Ce qui reste à faire

### Priorité haute

- **Intégration MFA dans le pipeline Zero Trust** : MFA est activé en config mais le score pondéré (face/voix/appareil/PIN) doit être appelé dans l'orchestrateur
- **Chiffrement des données existantes** : les JSON déjà stockés (profils, historique) ne sont pas encore chiffrés rétrospectivement — migrer avec `data_protection.py`

### Priorité moyenne

- **Expiration automatique des appareils** : les appareils non vus depuis N jours devraient être révoqués automatiquement (`last_seen` est tracé mais non appliqué)
- **Rotation des clés** : la fonction `rotate_key()` existe mais un workflow de migration des données existantes n'est pas documenté
- **Persistance des sessions** : les sessions sont en mémoire (perdues au redémarrage) — migrer vers SQLite

### Priorité basse

- **Détection comportementale ML** : le module `behavioral_detector.py` utilise un seuil fixe — l'enrichir avec un modèle statistique
- **Rotation des logs d'audit** : définir et appliquer la politique de rétention `audit_retention_policy.json`
- **Certificate pinning** : si le fallback OpenAI est activé, implémenter le pinning de certificat

---

*Document généré dans le cadre du Bloc 20 — Sécurité ALFRED.*
*Aucune clé, secret, token ou donnée d'identification ne figure dans ce document.*
