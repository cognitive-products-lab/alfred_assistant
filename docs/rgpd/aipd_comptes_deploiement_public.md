# Analyse d'Impact sur la Protection des Données (AIPD)
## Traitement : Comptes utilisateurs, préférences, conversations et logs anonymisés — déploiement public ALFRED_WEB

---

**Référence :** AIPD-ALFRED-002 (backlog T001)
**Version :** 1.0
**Date :** 2026-07-10
**Responsable du traitement :** Cognitive Products Lab — Céline (fondatrice)
**Délégué à la protection des données (DPD) :** Fondatrice (auto-DPD, entité de moins de 250 personnes)
**Base légale :** Art. 6 §1.a RGPD — Consentement explicite
**Référentiel CNIL :** Lignes directrices AIPD CNIL (2018)
**Document lié :** `docs/rgpd/aipd_donnees_sante.md` (AIPD-ALFRED-001, périmètre ALFRED_PC local mono-utilisateur — traitement distinct, non couvert ici)

---

## 1. Contexte et finalité du traitement

### 1.1 Description du traitement

Ce document couvre l'extension d'architecture de données réalisée les 08-09/07/2026 pour préparer le déploiement public d'ALFRED_WEB (site public, actuellement sans compte utilisateur réel) : création d'un premier système de comptes, extension du stockage MongoDB, et un PoC d'analyse de logs anonymisés. Quatre traitements distincts, tous **codés et testés mais aucun n'est ouvert au public à ce jour** :

| Traitement | Données | Stockage | Bloc |
|---|---|---|---|
| Comptes utilisateurs | email, mot de passe (haché bcrypt), rôle, date de création, date de consentement | PostgreSQL (`ALFRED_WEB/models/user.py`) | 21.23 |
| Préférences d'affichage | langue (fr/en), police OpenDyslexic (bool), date de consentement | MongoDB (`user_preferences`) | 21.24 |
| Conversations (scaffolding) | messages horodatés liés à un compte — **aucune fonctionnalité de chat n'existe encore côté ALFRED_WEB** | MongoDB (`conversations`), TTL 90j | 21.25 |
| PoC Hadoop | logs de sécurité ALFRED_PC anonymisés (date, endpoint, rôle, résultat, action, décision, niveau SOC) | HDFS temporaire, détruit après usage | 29 |

### 1.2 Finalités

- **Comptes :** authentification pour un accès personnalisé au site public ALFRED_WEB, en vue du déploiement public.
- **Préférences :** personnalisation de l'affichage (langue, accessibilité) liée au compte plutôt qu'au seul navigateur.
- **Conversations :** finalité anticipée — mémoire conversationnelle d'un futur chat web lié au compte. **Pas encore de finalité active : aucune donnée réelle n'existe dans cette collection.**
- **PoC Hadoop :** démonstration de compétence technique (Big Data) + amélioration produit potentielle via analyse de tendances d'usage agrégées, sur un jeu de données anonymisé et non connecté à un pipeline de production.
- **Exclue explicitement :** aucune transmission à des tiers, aucun profilage commercial, aucune inscription publique réelle ouverte à ce jour (gate — voir §6).

### 1.3 Catégories de personnes concernées

- **Aujourd'hui :** aucune — les routes existent et sont testées, mais aucun compte réel n'a été créé en dehors des tests automatisés (nettoyés après chaque exécution).
- **À l'ouverture du déploiement public :** visiteurs du site ALFRED_WEB souhaitant créer un compte (grand public, pas de mineurs identifiés comme cible pour cette fonctionnalité — ARTHUR, destiné aux enfants, fait l'objet d'une AIPD distincte à produire séparément).
- **PoC Hadoop :** aucune personne concernée directement — les logs analysés proviennent de l'usage local mono-utilisateur de la fondatrice sur ALFRED_PC, anonymisés avant traitement.

---

## 2. Nécessité et proportionnalité

### 2.1 Minimisation des données

| Traitement | Critère | Évaluation | Mesure |
|---|---|---|---|
| Comptes | Champs collectés | email + mot de passe uniquement — aucun nom, téléphone, adresse | ✅ Conforme |
| Préférences | Champs collectés | 2 champs (lang, dyslexic_font) — vérifiés comme les 2 seules préférences réellement exposées dans le code avant conception, aucune préférence hypothétique ajoutée | ✅ Conforme |
| Conversations | Champs collectés | Scaffolding minimal (rôle, contenu, horodatage) — pas de métadonnées superflues | ⚠️ À réévaluer si le chat devient réel |
| Hadoop | Champs collectés | Identifiants directs/quasi-directs supprimés avant tout chargement (api_key_hash, user_id, device_id, request_id, texte libre) | ✅ Conforme |

### 2.2 Mesures de minimisation implémentées

- Mot de passe jamais stocké en clair — hachage bcrypt (`auth/routes.py`), coût de calcul par défaut de la bibliothèque.
- Consentement des préférences **distinct** de celui du compte (décision explicite de Céline, 08/07/2026) — finalité différente, pas de réutilisation abusive d'un consentement pour une autre finalité.
- Anonymisation Hadoop faite **avant** tout chargement HDFS, jamais de log brut chargé (`scripts/anonymize_logs_for_hadoop.py`), cluster détruit après usage (`docker compose down -v`, exécuté le 09/07/2026).
- Aucune donnée transmise à un sous-traitant tiers hors du périmètre déjà couvert (`docs/rgpd/dpa_sous_traitants.md`) — PostgreSQL et MongoDB tournent en local (Docker) à ce stade, pas encore en production hébergée.

---

## 3. Identification et évaluation des risques

### 3.1 Risque 1 — Ouverture prématurée de l'inscription publique sans cadre RGPD complet

| | |
|---|---|
| **Menace** | Activation en production du endpoint `/auth/register` avant que les droits des personnes (accès, effacement, portabilité) soient réellement implémentés côté web |
| **Probabilité** | Faible actuellement (aucun déploiement public actif), mais réelle si l'ouverture se fait sans repasser par cette AIPD |
| **Impact** | Élevé (collecte de données personnelles réelles sans cadre légal complet) |
| **Risque résiduel** | **Élevé tant que §4.3 (droits des personnes) n'est pas comblé — voir actions requises §7** |
| **Mesures** | Gate explicite documenté à chaque étape du code (`auth/routes.py`, mémoire projet) : ne pas ouvrir d'inscription publique réelle avant validation de cette AIPD |

### 3.2 Risque 2 — Absence de suppression en cascade PostgreSQL → MongoDB

| | |
|---|---|
| **Menace** | Suppression d'un compte PostgreSQL (`users`) sans suppression corrélée des documents MongoDB associés (`user_preferences`, `conversations`) — violation potentielle du droit à l'effacement (Art. 17) |
| **Probabilité** | Élevée si un compte est supprimé aujourd'hui — **aucune procédure de suppression de compte n'existe encore côté code** (pas de route `DELETE /auth/account`) |
| **Impact** | Moyen (deux bases distinctes, pas de contrainte technique FK cross-moteur) |
| **Risque résiduel** | **Élevé — gap réel non comblé, à traiter avant ouverture publique** |
| **Mesures existantes** | Isolation stricte par `user_id` (aucun accès cross-utilisateur possible, testé) |
| **Mesures manquantes** | Route de suppression de compte + procédure de purge cascade Postgres→Mongo — **à développer** |

### 3.3 Risque 3 — Durée de rétention des conversations non fondée

| | |
|---|---|
| **Menace** | Index TTL fixé à 90 jours sur la collection `conversations` sans analyse réelle de nécessité — actuellement un **placeholder technique**, pas une décision de gouvernance |
| **Probabilité** | Sans objet tant qu'aucune conversation réelle n'existe (scaffolding) |
| **Impact** | Faible à ce stade, deviendrait moyen si le chat devient réel sans revalidation de la durée |
| **Risque résiduel** | Faible actuellement, **à revalider avant toute mise en production du chat** |
| **Mesures** | Documenté comme placeholder dans le code (`scripts/init_mongo_conversations_index.py`) et cette AIPD |

### 3.4 Risque 4 — Accès non autorisé aux comptes (mots de passe faibles, absence de limitation de tentatives)

| | |
|---|---|
| **Menace** | Attaque par force brute / credential stuffing sur `/auth/login` |
| **Probabilité** | Moyenne si le service est exposé publiquement sans mesure complémentaire |
| **Impact** | Élevé (accès à un compte tiers) |
| **Risque résiduel** | Moyen |
| **Mesures existantes** | Mot de passe minimum 10 caractères, bcrypt, CSRF sur toutes les routes d'écriture |
| **Mesures manquantes** | Rate limiting sur `/auth/login` — **non implémenté à ce jour, à ajouter avant ouverture publique** |

### 3.5 Risque 5 — Ré-identification via corrélation des logs Hadoop

| | |
|---|---|
| **Menace** | Recoupement des enregistrements anonymisés (date, endpoint, rôle) pour ré-identifier un usage |
| **Probabilité** | Très faible — usage mono-utilisateur actuel, échantillon (1 399 lignes) trop petit et non nominatif pour permettre une ré-identification significative |
| **Impact** | Faible |
| **Risque résiduel** | **Faible** |
| **Mesures** | Anonymisation systématique avant chargement, agrégation par jour/catégorie (pas d'événement individuel exposé dans le résultat), cluster détruit après usage |

---

## 4. Mesures de protection

### 4.1 Mesures techniques en place

| Mesure | Implémentation | Fichier de preuve |
|---|---|---|
| Hachage des mots de passe | bcrypt | `ALFRED_WEB/auth/routes.py` |
| Protection CSRF | Jeton de session sur toutes les routes d'écriture | `ALFRED_WEB/auth/routes.py`, `conversations/routes.py` |
| Isolation stricte par utilisateur | Filtrage `user_id` systématique, 404 (pas 403) sur accès cross-utilisateur | `ALFRED_WEB/conversations/routes.py`, tests dédiés |
| Consentement horodaté et séparé par finalité | `consent_at` (comptes), `preferences_consent_at` (préférences) | `models/user.py`, `data/preferences_repository.py` |
| Anonymisation avant traitement Big Data | Suppression identifiants directs, troncature temporelle | `scripts/anonymize_logs_for_hadoop.py` |
| Dégradation propre si base injoignable | Pas de crash, réponse 503 | `data/postgres.py`, `data/mongo.py` |
| Couverture de tests | 32 tests ALFRED_WEB (comptes/préférences/conversations) + 24 tests Hadoop, tous exécutés contre les bases réelles | `ALFRED_WEB/tests/`, `ALFRED_PC/tests/b29_tests/` |

### 4.2 Mesures manquantes (actions requises avant ouverture publique — voir §7)

- Route de suppression de compte (`DELETE /auth/account`) + procédure de purge cascade PostgreSQL → MongoDB.
- Export des données personnelles (droit à la portabilité, Art. 20) côté web — n'existe pas encore pour les comptes ALFRED_WEB (existe déjà côté ALFRED_PC local via `export_command.py`, périmètre différent).
- Rate limiting sur `/auth/login` et `/auth/register`.
- Revalidation de la durée de rétention des conversations (90 jours est un placeholder, pas une décision de gouvernance actée).

### 4.3 Mesures organisationnelles

- Gate explicite dans le code et la documentation projet : pas d'inscription publique réelle sans validation de cette AIPD.
- PostgreSQL et MongoDB hébergés en local (Docker) à ce stade — aucun sous-traitant cloud tiers impliqué pour l'instant. Si un hébergeur managé est utilisé en production (ex. add-on PostgreSQL Render), une DPA devra être formalisée (voir `docs/rgpd/dpa_sous_traitants.md`) avant la mise en production.

---

## 5. Droits des personnes

| Droit | État actuel |
|---|---|
| Accès Art. 15 | ❌ Non implémenté côté ALFRED_WEB |
| Rectification Art. 16 | ❌ Non implémenté côté ALFRED_WEB |
| Effacement Art. 17 | ❌ Non implémenté (voir Risque 2, §3.2) |
| Portabilité Art. 20 | ❌ Non implémenté côté ALFRED_WEB |
| Opposition Art. 21 | ⚠️ Partiel — refuser la connexion suffit à ne pas générer de nouvelles données, mais pas de mécanisme actif |
| Retrait du consentement | ❌ Non implémenté (pas de `revoke_consent()` côté web, contrairement à ALFRED_PC) |

**Constat honnête :** contrairement au périmètre ALFRED_PC (AIPD-ALFRED-001, où ces droits sont opérationnels via des commandes locales), **aucun des droits des personnes n'est encore implémenté côté ALFRED_WEB**. C'est le principal gap identifié par cette AIPD et la raison pour laquelle le gate « pas d'inscription publique réelle » doit rester actif.

---

## 6. Consultation de la CNIL

### 6.1 Nécessité de consultation préalable

**Conclusion :** Consultation préalable **non requise à ce stade** — aucun traitement réel de données personnelles n'est actuellement actif (pas d'utilisateur public inscrit), le risque résiduel principal (§3.1, §3.2) porte sur une activation *future* du service, pas sur un traitement en cours.

**Seuil de réexamen :** Cette AIPD doit être revue et les actions du §7 complétées **avant** toute ouverture réelle de `/auth/register` en production avec de vrais utilisateurs.

---

## 7. Conclusion et actions requises avant ouverture publique

Le traitement peut continuer à être développé et testé (comme actuellement), mais **l'ouverture publique réelle des comptes ALFRED_WEB est conditionnée à** :

1. ❌ Implémenter la suppression de compte + purge cascade PostgreSQL → MongoDB (Risque 2)
2. ❌ Implémenter l'export des données personnelles côté web (droit à la portabilité)
3. ❌ Implémenter un mécanisme de retrait du consentement côté web
4. ❌ Ajouter un rate limiting sur `/auth/login` et `/auth/register` (Risque 4)
5. ❌ Revalider (ou réduire) la durée de rétention TTL des conversations avant toute mise en production du chat (Risque 3)
6. ⚠️ Formaliser une DPA si un hébergeur managé tiers est utilisé en production (dépend du choix d'hébergement)

Tant que ces points ne sont pas traités, le gate déjà présent dans le code (`auth/routes.py`, mémoire projet) doit rester actif : **pas d'inscription publique réelle**.

---

## 8. Validation et revue

| | |
|---|---|
| **Validée par** | À valider par Céline — Responsable du traitement |
| **Date de rédaction** | 2026-07-10 |
| **Prochaine revue** | Avant toute ouverture publique réelle, ou lors d'un changement substantiel (chat web réel, hébergement managé tiers) |
| **Déclencheurs de révision** | Implémentation des droits des personnes (§7) · Choix d'un hébergeur de production · Activation réelle du chat web (Bloc 21.25) · Incident de sécurité |

---

*Document confidentiel interne — Cognitive Products Lab*
*Généré conformément aux lignes directrices AIPD de la CNIL et au Règlement (UE) 2016/679*
