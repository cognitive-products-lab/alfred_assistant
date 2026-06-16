# Sécurité et protection des données — Profil psychologique ALFRED

**Version** : 1.0  
**Date** : 2026-06-16  
**Classification** : Données Hautement Sensibles (DHS)  
**Conforme à** : RGPD Art. 9 (données sensibles), Security by Design, Zero Trust Architecture

---

## Table des matières

1. [Classification des données](#1-classification-des-données)
2. [Architecture de sécurité](#2-architecture-de-sécurité)
3. [Chiffrement au repos](#3-chiffrement-au-repos)
4. [Structure des fichiers — chiffrés vs non-chiffrés](#4-structure-des-fichiers--chiffrés-vs-non-chiffrés)
5. [Droits d'accès et principe de moindre privilège](#5-droits-daccès-et-principe-de-moindre-privilège)
6. [Conformité RGPD](#6-conformité-rgpd)
7. [Procédure d'effacement des données](#7-procédure-deffacement-des-données)
8. [Procédure de sauvegarde sécurisée](#8-procédure-de-sauvegarde-sécurisée)
9. [Git — Ce qui est commité vs ce qui ne l'est jamais](#9-git--ce-qui-est-commité-vs-ce-qui-ne-lest-jamais)
10. [Incidents de sécurité — Procédures](#10-incidents-de-sécurité--procédures)

---

## 1. Classification des données

### 1.1 Taxonomie des données du profil psychologique

| Type de donnée | Exemples | Sensibilité | Stockage |
|----------------|---------|-------------|---------|
| **Réponses brutes aux questionnaires** | q1=6, s3=2, uw7=5 | CRITIQUE | Chiffré (Fernet) ou en mémoire uniquement |
| **Scores normalisés (0-100)** | ouverture: 72.5, stress: 34.0 | HAUTE | En clair dans user_profile.json (local uniquement) |
| **Niveaux agrégés** | resilience: "élevé", tone: "analytique" | MODÉRÉE | En clair dans user_profile.json |
| **Paramètres ALFRED dérivés** | emotional_support: "standard" | FAIBLE | En clair dans user_profile.json |
| **Métadonnées** | dates de passation, complétude | FAIBLE | En clair |

### 1.2 Pourquoi les données psychologiques sont hautement sensibles

Les réponses aux questionnaires psychologiques constituent des **données de catégorie spéciale** au sens de l'Article 9 du RGPD. Elles révèlent :

- Des informations sur la santé mentale (stress, burnout, résilience)
- Des traits de personnalité qui peuvent être utilisés pour influencer ou discriminer
- Des valeurs et croyances personnelles (Schwartz)
- Des états émotionnels et des vulnérabilités

Même non médicales au sens strict, ces données tombent dans la catégorie des **données relatives à la santé** (Art. 9.1 RGPD) par leur nature et leurs implications potentielles.

---

## 2. Architecture de sécurité

### 2.1 Principes fondamentaux

**Local-First Architecture**
Toutes les données psychologiques restent sur le poste local de Céline. Aucune donnée n'est transmise à des serveurs distants, API tierces ou services cloud. ALFRED est architecturé sans télémétrie.

**Zero Trust Interne**
Même en contexte local, le principe Zero Trust s'applique : les données sensibles sont chiffrées au repos même si elles ne "voyagent" pas. En cas de vol ou de partage accidentel du disque, les réponses brutes restent illisibles sans la clé.

**Security by Design**
La sécurité est intégrée à l'architecture dès la conception :
- Les réponses brutes ne sont JAMAIS stockées en clair en dehors d'une session active
- Les fichiers contenant des données sensibles ont des emplacements définis et documentés
- Le `.gitignore` est configuré pour exclure tout fichier de données sensibles

**Principe de moindre divulgation**
Seuls les scores agrégés (niveaux) sont propagés dans le système ALFRED. Les réponses individuelles restent confinées à l'étape de scoring et sont chiffrées immédiatement après.

### 2.2 Cohérence avec le Bloc 20 existant

Ce système s'inscrit dans la continuité du Bloc Sécurité 20 déjà en place :

| Module existant | Rôle | Interaction avec le profil psy |
|-----------------|------|-------------------------------|
| `encryption_service.py` | Chiffrement Fernet global | Même technologie pour les réponses |
| `security_logger.py` | Traçabilité des événements | Logs des opérations de chiffrement/déchiffrement |
| `zero_trust_orchestrator.py` | Politique Zero Trust | Cohérence avec la politique globale |
| `access_control.py` | Contrôle d'accès | L'utilisateur seul accède aux données |
| `audit_trail.py` | Piste d'audit | Enregistrement des accès aux données sensibles |

---

## 3. Chiffrement au repos

### 3.1 Algorithme : Fernet (AES-128-CBC + HMAC-SHA256)

**Fernet** est une recette de chiffrement symétrique authentifié, implémentée dans la bibliothèque `cryptography` (Python). Elle combine :

- **AES-128-CBC** : chiffrement symétrique par blocs (Advanced Encryption Standard, 128 bits, mode Cipher Block Chaining)
- **HMAC-SHA256** : authentification de l'intégrité (Hash-based Message Authentication Code)
- **IV aléatoire** : vecteur d'initialisation unique par message (128 bits aléatoires)
- **Horodatage** : chaque token Fernet inclut l'heure de chiffrement

Un token Fernet est :
```
base64url(IV + AES-128-CBC(key, IV, data) + HMAC-SHA256(signing_key, IV + ciphertext))
```

**Niveau de sécurité** : AES-128-CBC avec padding aléatoire est considéré comme résistant aux attaques connues jusqu'à 2030 et au-delà (NIST SP 800-131A).

### 3.2 Gestion de la clé de chiffrement

**Règle absolue** : la clé Fernet ne doit JAMAIS être committée dans git.

**Emplacements de stockage de la clé :**

```
Priorité 1 (recommandée) : Variable d'environnement FERNET_KEY
  → Définie dans .env (exclu de git via .gitignore)
  → export FERNET_KEY="gAAAAAB..."

Priorité 2 : Fichier local
  → data/security/fernet.key
  → Droits recommandés : chmod 600 (lecture seule par l'utilisateur)
  → JAMAIS dans git (voir .gitignore)

Priorité 3 : Auto-génération
  → Si aucune clé existante, profile_analyzer.py génère et sauvegarde une nouvelle clé
  → Avertissement affiché : "ATTENTION : ne jamais commiter ce fichier de clé"
```

**Rotation de la clé :**
La rotation de la clé entraîne l'impossibilité de déchiffrer les fichiers chiffrés avec l'ancienne clé. Avant toute rotation :
1. Déchiffrer tous les fichiers existants avec l'ancienne clé
2. Générer la nouvelle clé
3. Re-chiffrer les fichiers avec la nouvelle clé
4. Supprimer l'ancienne clé

### 3.3 Fichiers chiffrés

Les réponses brutes chiffrées sont stockées dans :
```
data/profile/answers_encrypted/
  answers_20260616_120000.fernet
  answers_20260716_083000.fernet
  ...
```

Format du nom de fichier : `answers_YYYYMMDD_HHMMSS.fernet`

Chaque passation génère un nouveau fichier — les archives permettent de retrouver l'historique si nécessaire.

---

## 4. Structure des fichiers — chiffrés vs non-chiffrés

```
data/profile/
├── user_profile.json                    [NON CHIFFRÉ — scores agrégés seulement]
├── scoring/
│   ├── answers_template.json            [SENSIBLE — chiffrer après analyse]
│   └── scoring_keys.json                [NON CHIFFRÉ — configuration neutre]
├── schema/
│   ├── dimensions_schema.json           [NON CHIFFRÉ — métadonnées]
│   ├── alfred_mapping_matrix.json       [NON CHIFFRÉ — règles métier]
│   └── periodicity_schema.json          [NON CHIFFRÉ — calendrier]
├── questionnaires/
│   └── *.md                             [NON CHIFFRÉ — questions publiques]
└── answers_encrypted/
    └── answers_YYYYMMDD_HHMMSS.fernet  [CHIFFRÉ — réponses brutes]

data/security/
└── fernet.key                           [CLEF — NE PAS COMMITER — chmod 600]
```

### Justification de ce qui est non-chiffré

**user_profile.json** (scores agrégés) : Ce fichier contient des niveaux ("élevé", "moyen") qui ne permettent pas de reconstituer les réponses individuelles. Un score global de résilience de 72/100 est insuffisant pour inférer les réponses item par item. Ce niveau d'agrégation est jugé acceptable pour un fichier local.

**scoring_keys.json** : Contient uniquement les règles de calcul — aucune donnée personnelle.

**schema/ et questionnaires/** : Contenu entièrement public et non-personnel.

---

## 5. Droits d'accès et principe de moindre privilège

### 5.1 Accès aux données

**Données psychologiques** : accès exclusif à Céline Rousselot, propriétaire unique du système.

| Acteur | Accès autorisé | Détail |
|--------|---------------|--------|
| Céline (utilisatrice) | TOTAL | Lecture, écriture, effacement de toutes les données |
| ALFRED (IA locale) | LECTURE SCORES | user_profile.json — scores et paramètres uniquement |
| Autres personnes | AUCUN | Pas de partage prévu — usage strictement personnel |
| Sauvegarde chiffrée | LECTURE CHIFFRÉE | Backup uniquement si chiffrement préalable des données sensibles |

### 5.2 Droits système recommandés

```bash
# Droits recommandés sur les fichiers sensibles
chmod 600 data/security/fernet.key
chmod 600 data/profile/scoring/answers_template.json
chmod 600 data/profile/answers_encrypted/*.fernet
chmod 644 data/profile/user_profile.json
```

### 5.3 Absence de partage cloud

ALFRED est un système **local-first**. Aucune donnée psychologique ne doit être :
- Synchronisée vers un cloud personnel (Google Drive, Dropbox, iCloud)
- Transmise à un modèle de langage externe (OpenAI, Anthropic, etc.)
- Partagée avec un tiers pour quelque raison que ce soit

Si ALFRED est connecté à un LLM externe (Ollama en local ou API), les paramètres ALFRED dérivés (`tone`, `emotional_support_level`, etc.) peuvent être transmis dans le contexte système — mais jamais les réponses brutes ou les scores détaillés.

---

## 6. Conformité RGPD

### 6.1 Catégorie juridique des données

Les données psychologiques collectées entrent dans la **catégorie spéciale des données sensibles** définie par l'**Article 9 du RGPD** (Règlement Général sur la Protection des Données, UE 2016/679). Plus spécifiquement :

- **Article 9.1** : données révélant des opinions politiques, convictions religieuses ou philosophiques → concerné (valeurs Schwartz, motivations)
- **Article 9.1** : données relatives à la santé → concerné (stress perçu, burnout, résilience)
- **Article 4.15** : "données relatives à la santé" inclut les données sur la santé mentale

### 6.2 Base juridique du traitement

Le traitement de ces données repose sur **deux bases juridiques cumulatives** (Art. 6 + Art. 9 RGPD) :

**Art. 6.1.a — Consentement**  
Céline Rousselot consent explicitement au traitement de ses données psychologiques en utilisant ce système et en remplissant les questionnaires. Ce consentement est :
- Libre (pas de conséquence professionnelle)
- Spécifique (usage personnel ALFRED uniquement)
- Éclairé (ce document constitue l'information)
- Univoque (action positive de remplir les questionnaires)

**Art. 9.2.a — Consentement explicite pour données sensibles**  
Le consentement pour les données de catégorie spéciale doit être explicite. En lisant ce document et en utilisant le système, Céline consent explicitement au traitement de ses données psychologiques.

### 6.3 Droits de l'utilisateur

| Droit RGPD | Article | Implémentation dans ALFRED |
|------------|---------|--------------------------|
| **Droit d'accès** | Art. 15 | `decrypt_answers()` — accès aux réponses brutes à tout moment |
| **Droit de rectification** | Art. 16 | Remplir à nouveau le questionnaire et relancer `profile_analyzer.py` |
| **Droit à l'effacement** | Art. 17 | Procédure décrite en section 7 |
| **Droit à la portabilité** | Art. 20 | Les données sont en JSON — format portable par nature |
| **Droit à la limitation** | Art. 18 | Supprimer `psychological_profile` de `user_profile.json` |
| **Droit d'opposition** | Art. 21 | Ne pas remplir les questionnaires — le système fonctionne sans |

### 6.4 Durée de conservation

| Catégorie de données | Durée | Justification |
|---------------------|-------|---------------|
| Réponses brutes chiffrées | Jusqu'à effacement explicite | Usage longitudinal pour comparaison |
| Scores agrégés dans user_profile.json | Jusqu'à effacement explicite | Nécessaire au fonctionnement d'ALFRED |
| Logs système (security_logger) | 90 jours | Sécurité opérationnelle |

Il n'existe pas de durée de conservation imposée pour un usage strictement personnel. L'utilisatrice est seule décisionnaire.

### 6.5 Absence de transfert hors UE

Les données restent en local sur le territoire de l'utilisatrice. Aucun transfert vers des pays tiers n'est prévu. Si ALFRED utilise un LLM en ligne (ex : API Anthropic basée aux USA), les données psychologiques brutes ou détaillées ne doivent JAMAIS être incluses dans les requêtes.

### 6.6 Délégué à la Protection des Données (DPO)

Ce système est destiné à un usage strictement personnel (traitement "des activités personnelles ou domestiques", Art. 2.2.c RGPD). Il est donc **exempté de l'obligation de nomination d'un DPO** et de l'obligation d'établir un registre des traitements.

---

## 7. Procédure d'effacement des données

### 7.1 Effacement des réponses brutes

```bash
# Supprimer les réponses non chiffrées
rm data/profile/scoring/answers_template.json

# Réinitialiser le template (answers_template.json vide)
python src/core/profile_analyzer.py --reset-answers  # (à implémenter en V2)
# Ou manuellement : remettre tous les champs à null

# Supprimer les archives chiffrées
rm -rf data/profile/answers_encrypted/
```

### 7.2 Effacement des scores dans user_profile.json

```python
import json

with open("data/profile/user_profile.json", "r") as f:
    profile = json.load(f)

# Supprimer uniquement les données psychologiques
profile.pop("psychological_profile", None)
profile.pop("alfred_derived_params", None)

with open("data/profile/user_profile.json", "w") as f:
    json.dump(profile, f, ensure_ascii=False, indent=2)
```

### 7.3 Effacement complet (remise à zéro totale)

```bash
# ATTENTION : opération irréversible

# 1. Supprimer les réponses chiffrées
rm -rf data/profile/answers_encrypted/

# 2. Réinitialiser le template de réponses
# Remettre tous les champs à null dans answers_template.json

# 3. Supprimer les scores du profil
# Éditer user_profile.json pour supprimer psychological_profile et alfred_derived_params

# 4. Optionnel : supprimer la clé de chiffrement (les archives .fernet deviennent illisibles)
rm data/security/fernet.key

# 5. Confirmer que le historique git ne contient pas de données sensibles
git log --all --full-history -- "data/profile/answers_encrypted/**"
git log --all --full-history -- "data/security/fernet.key"
```

---

## 8. Procédure de sauvegarde sécurisée

### 8.1 Principes

- Ne jamais sauvegarder des données sensibles EN CLAIR sur un support externe ou cloud
- Toujours chiffrer avant de sauvegarder

### 8.2 Sauvegarde recommandée

```bash
# Étape 1 : S'assurer que les réponses sont chiffrées
python src/core/profile_analyzer.py --encrypt-only

# Étape 2 : Identifier les fichiers à sauvegarder
# À sauvegarder :
# - data/profile/answers_encrypted/*.fernet (réponses chiffrées)
# - data/profile/user_profile.json (scores)
# - data/security/fernet.key (clé — à stocker SÉPARÉMENT du reste)

# Étape 3 : Sauvegarde de la clé SÉPARÉMENT
# La clé et les données chiffrées ne doivent PAS être au même endroit
# Recommandé : clé sur gestionnaire de mots de passe (Bitwarden, 1Password)
# OU clé imprimée et stockée physiquement

# Étape 4 : Sauvegarde des archives chiffrées
# Peut aller sur cloud (Dropbox, etc.) car chiffrées
cp -r data/profile/answers_encrypted/ /chemin/sauvegarde/
cp data/profile/user_profile.json /chemin/sauvegarde/
```

### 8.3 Restauration

```bash
# Étape 1 : Restaurer la clé Fernet
cp /chemin/sauvegarde/fernet.key data/security/fernet.key
# OU définir FERNET_KEY dans .env

# Étape 2 : Restaurer les archives chiffrées
cp /chemin/sauvegarde/*.fernet data/profile/answers_encrypted/

# Étape 3 : Déchiffrer si nécessaire pour re-analyse
python src/core/profile_analyzer.py --decrypt data/profile/answers_encrypted/answers_DERNIÈRE_DATE.fernet

# Étape 4 : Restaurer user_profile.json si nécessaire
cp /chemin/sauvegarde/user_profile.json data/profile/user_profile.json
```

---

## 9. Git — Ce qui est commité vs ce qui ne l'est jamais

### 9.1 Ce qui EST commité (sûr)

```
data/profile/schema/             ← JSON de configuration — aucune donnée personnelle
data/profile/questionnaires/     ← Fichiers Markdown publics
data/profile/scoring/scoring_keys.json  ← Clés de calcul — aucune donnée personnelle
data/profile/scoring/answers_template.json  ← Template VIDE (tous les champs à null)
docs/profil_systeme/             ← Documentation
src/core/profile_analyzer.py    ← Code source
```

### 9.2 Ce qui N'EST JAMAIS commité

```
data/profile/scoring/answers_template.json  ← si rempli (réponses brutes)
data/profile/answers_encrypted/             ← archives chiffrées (données sensibles)
data/profile/answers/                       ← tout fichier de réponses non chiffré
data/security/fernet.key                    ← clé de chiffrement
*.fernet_key                                ← tout fichier de clé
user_answers_*.json                         ← tout fichier de réponses personnalisé
.env                                        ← variables d'environnement (déjà exclu)
```

### 9.3 Entrées .gitignore à ajouter

Voir le fichier `.gitignore` du projet — section ajoutée par ce commit :

```gitignore
# Profil psychologique - données sensibles
data/profile/answers/
data/profile/answers_encrypted/
data/profile/keys/
*.fernet_key
user_answers_*.json
```

### 9.4 Vérification que rien de sensible n'est commité

```bash
# Vérifier les fichiers trackés qui ne devraient pas l'être
git ls-files data/profile/answers_encrypted/
git ls-files data/security/fernet.key
git ls-files "*.fernet"

# Vérifier l'historique git pour d'éventuelles fuites passées
git log --all --full-history -- "data/security/fernet.key"
git log --all --full-history -- "data/profile/answers_encrypted/"
```

---

## 10. Incidents de sécurité — Procédures

### 10.1 Fuite de réponses brutes (answers_template.json commité)

```
1. Identifier le commit fautif : git log --all -- data/profile/scoring/answers_template.json
2. Révoquer l'accès au dépôt si public
3. Purger l'historique git : git filter-branch ou git-filter-repo
4. Forcer un push --force sur la branche (après confirmation de la suppression)
5. Générer une nouvelle clé Fernet (rotation de clé)
6. Re-chiffrer les données avec la nouvelle clé
7. Documenter l'incident dans data/security/ (audit trail)
```

### 10.2 Fuite de la clé Fernet (fernet.key commité)

```
1. Toutes les données chiffrées avec cette clé sont compromises
2. Générer immédiatement une nouvelle clé
3. Déchiffrer les archives avec l'ancienne clé (si possible)
4. Re-chiffrer avec la nouvelle clé
5. Purger l'ancienne clé de l'historique git
6. Si les archives étaient sur un dépôt public : considérer les données comme exposées
```

### 10.3 Accès non autorisé au poste de travail

```
1. Si chiffrement en place : les réponses brutes sont illisibles sans la clé
2. Vérifier que fernet.key n'est pas stockée dans un emplacement évident
3. Changer tous les mots de passe du poste
4. Décider si une rotation de clé et un re-chiffrement sont nécessaires
```

---

*Document conforme aux exigences RGPD Art. 9 — Dernière révision : 2026-06-16*
