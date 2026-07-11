<!--
============================================================
PROJECT  : ALFRED / Cognitive Products Lab
BLOCK    : B20 — Sécurité, Gouvernance & Conformité
DOCUMENT : Politique de Gestion des Données (RGPD)
TYPE     : Documentation gouvernance — document destiné à publication publique
REF      : Règlement (UE) 2016/679 — RGPD
VERSION  : V1.2
CREATED  : 2026-05 (V1.0, docs/security/politique_donnees_rgpd_alfred.pdf)
UPDATED  : 2026-07-11
AUTHOR   : Cognitive Products Lab — Céline Rousselot (rédaction assistée Claude)
STATUS   : Approuvé (version interne) — version publique site web en attente de mise à jour, cf. §12
============================================================
-->
# Politique de Gestion des Données
## Conformité RGPD · Protection des données personnelles · Droits des utilisateurs

> **Référence :** Règlement (UE) 2016/679 (RGPD), texte consolidé :
> https://www.cnil.fr/fr/reglement-europeen-protection-donnees
> **Version :** 1.2 — 2026-07-11
> **Responsable du traitement :** Cognitive Products Lab — Céline Rousselot
> **Statut :** Approuvé (usage interne) — voir §12 pour la publication web

> Ce document est rédigé en langage clair et accessible, conformément à l'article 12 du RGPD qui impose que l'information soit fournie « de façon concise, transparente, compréhensible et aisément accessible ». Il est destiné à terme à la publication sur le site web de Cognitive Products Lab.

---

## 1. Qui sommes-nous ?

| Information | Détail |
|---|---|
| Nom de l'organisation | Cognitive Products Lab |
| Responsable du traitement | Céline Rousselot |
| Qualité | Fondatrice — Chef de projet IA |
| Projets concernés | ALFRED (assistant personnel), ALFRED_WEB (site public), ALFRED CPL, ARTHUR |
| Délégué à la Protection des Données (DPO) | Céline Rousselot assure cette fonction à ce stade. Un DPO externe sera désigné lors de la mise en production commerciale |

---

## 2. Quelles données collectons-nous ?

### 2.1 ALFRED (local, PC/Android) — inchangé depuis mai 2026

| Catégorie | Données concernées | Finalité |
|---|---|---|
| Données d'interaction | Textes saisis, commandes vocales, historique des conversations | Répondre et se souvenir du contexte |
| Données de personnalisation | Préférences, profil utilisateur, adaptations apprises | Personnaliser les réponses |
| Données émotionnelles | Émotions détectées dans le discours | Adapter le comportement d'ALFRED |
| Données d'authentification | PIN haché (bcrypt, jamais en clair), token de session | Sécuriser l'accès local |
| Données techniques | Logs d'utilisation, identifiant d'appareil, horodatages | Sécurité, débogage |
| Données de santé (ARTHUR, si activé) | Contexte médical/pédiatrique | Adaptation du compagnon — catégorie spéciale, consentement explicite requis. ARTHUR n'est pas déployé à ce jour |

### 2.2 ALFRED_WEB — nouveau depuis juillet 2026, non ouvert au public

Extension réalisée pour préparer un futur déploiement public. **Aucun compte réel n'existe à ce jour** — ces traitements sont codés et testés, pas encore actifs pour de vrais utilisateurs (cf. §9, gate).

| Catégorie | Données concernées | Finalité | Stockage |
|---|---|---|---|
| Comptes utilisateurs | Email, mot de passe (haché bcrypt), rôle, date de création, date de consentement | Authentification pour un accès personnalisé au site public | PostgreSQL (local Docker à ce stade) |
| Préférences d'affichage | Langue (fr/en), police adaptée (OpenDyslexic) | Personnalisation de l'affichage liée au compte | MongoDB |
| Conversations (scaffolding) | Messages horodatés liés à un compte | Anticipation d'un futur chat web — **aucune donnée réelle n'existe, aucune fonctionnalité de chat n'est active** | MongoDB, index TTL 90 jours (placeholder, non validé comme politique de rétention définitive) |

### 2.3 PoC Hadoop (démonstrateur, non permanent)

Logs de sécurité ALFRED_PC anonymisés (date, endpoint, rôle, résultat — identifiants directs supprimés) analysés ponctuellement à des fins de démonstration technique et d'amélioration produit potentielle. Infrastructure détruite après chaque usage (`docker compose down -v`). Détail : `docs/hadoop_poc_bilan.md`.

### Ce que nous ne collectons pas

Nous ne collectons pas : données bancaires, numéros de sécurité sociale, données de localisation GPS, données de navigation web. Nous ne vendons pas vos données. Nous ne les transmettons pas à des tiers à des fins publicitaires. Nous n'utilisons pas vos données pour entraîner des modèles d'IA externes.

---

## 3. Sur quelle base traitons-nous vos données ?

| Base légale (Art. 6 RGPD) | Application ALFRED |
|---|---|
| Consentement (Art. 6.1.a) | Toute collecte non strictement nécessaire au fonctionnement requiert un consentement explicite, révocable à tout moment. Les comptes ALFRED_WEB et les préférences ont chacun leur **propre** consentement horodaté, séparé — décision explicite retenue le 08/07/2026 plutôt que de réutiliser un même consentement pour deux finalités différentes |
| Exécution du contrat (Art. 6.1.b) | Données d'interaction et d'authentification nécessaires à la fourniture du service demandé |
| Intérêt légitime (Art. 6.1.f) | Logs techniques et données de sécurité, dans notre intérêt légitime de sécurisation, sous réserve de ne pas prévaloir sur vos droits |
| Consentement explicite données sensibles (Art. 9) | Données émotionnelles et, pour ARTHUR, données de santé — consentement explicite séparé, révocable |

---

## 4. Où sont stockées vos données ?

**Principe local-first — ALFRED reste conçu autour de ce principe.** Vos données d'assistant personnel (ALFRED PC/Android) sont stockées sur votre appareil, chiffrées (AES-256/Fernet), jamais transmises à un serveur cloud sans consentement explicite préalable.

**Nuance introduite en juillet 2026** : les comptes ALFRED_WEB (site public) reposent nécessairement sur une base de données serveur (PostgreSQL, MongoDB) — le principe local-first s'applique à ALFRED en tant qu'assistant personnel, pas au site web public qui, par nature, nécessite un stockage centralisé pour gérer des comptes. Ce stockage est actuellement local (Docker sur l'infrastructure CPL) ; en cas d'hébergement cloud managé pour la mise en production, cette section sera mise à jour et une DPA formalisée avec l'hébergeur (cf. `docs/rgpd/dpa_sous_traitants.md`).

| Localisation | Détail |
|---|---|
| PC (Windows, ALFRED local) | `D:\PROJET_ALFRED\ALFRED_PC\data\` — chiffré Fernet |
| Android | Base Room + SQLCipher — chiffrée sur l'appareil |
| ALFRED_WEB (comptes, préférences, conversations) | PostgreSQL + MongoDB, Docker local (pas encore en production hébergée) |
| Serveurs cloud tiers | Aucun à ce stade pour les données personnelles réelles |
| Transferts hors UE | Aucun |

---

## 5. Combien de temps conservons-nous vos données ?

| Type de donnée | Durée de conservation |
|---|---|
| Historique de conversations (ALFRED local) | Jusqu'à suppression par l'utilisateur |
| Profil et préférences (ALFRED local) | Durée d'utilisation + 1 an après désactivation |
| Comptes ALFRED_WEB | Durée du compte — **procédure de suppression pas encore implémentée côté web, cf. §9** |
| Préférences ALFRED_WEB | Liée au compte |
| Conversations ALFRED_WEB (scaffolding) | Index TTL 90 jours — **placeholder technique, pas une politique de rétention validée** (à revoir avant toute mise en production du chat) |
| Logs techniques et sécurité | 90 jours glissants |
| Données d'incidents | 3 ans (obligation légale) |
| Données ARTHUR (santé) | Durée d'utilisation, suppression sur demande sous 30 jours |

---

## 6. Vos droits sur vos données

| Droit | ALFRED local (PC/Android) | ALFRED_WEB |
|---|---|---|
| Accès (Art. 15) | ✅ Export JSON disponible | ❌ Non implémenté |
| Rectification (Art. 16) | ✅ Modification directe dans l'interface | ❌ Non implémenté |
| Effacement (Art. 17) | ✅ `src/conversation/commands/erasure_command.py` — suppression fichiers sensibles + purge mémoire long terme, confirmation obligatoire (créé 11/07/2026 ; les fonctions sous-jacentes existaient et étaient testées depuis mai 2026 mais n'avaient aucun point d'entrée utilisateur avant cette date) | ❌ Non implémenté — pas de route de suppression de compte, pas de purge cascade PostgreSQL→MongoDB |
| Portabilité (Art. 20) | ✅ Export JSON structuré | ❌ Non implémenté |
| Opposition (Art. 21) | ✅ Désactivation par catégorie | ⚠️ Partiel — refuser la connexion évite toute nouvelle donnée, pas de mécanisme actif |
| Retrait du consentement (Art. 7.3) | ✅ Paramètres → Confidentialité | ❌ Non implémenté |

**Constat honnête (identique à celui de l'AIPD-ALFRED-002)** : les droits des personnes sont opérationnels côté ALFRED local depuis plusieurs mois, mais **aucun n'est encore implémenté côté ALFRED_WEB**. C'est la raison principale du gate décrit au §9 — nous ne considérons pas cette politique comme respectée pour ALFRED_WEB tant que ce tableau n'est pas entièrement vert.

**Délai de réponse** : un mois (Art. 12 RGPD), prolongeable de deux mois pour les demandes complexes. Réclamation possible auprès de la CNIL (www.cnil.fr).

---

## 7. Comment protégeons-nous vos données ?

Conformément à l'article 32 du RGPD (détail technique complet : `docs/smsi/politique_securite.md`) :

| Mesure | Description |
|---|---|
| Chiffrement | AES-256/Fernet (ALFRED local), bcrypt pour les mots de passe (partout) |
| Architecture Zero Trust | Chaque accès vérifié indépendamment (ALFRED local) |
| Isolation par compte | Filtrage systématique par identifiant utilisateur (ALFRED_WEB), testé |
| CSRF | Jeton de session sur toutes les routes d'écriture (ALFRED_WEB) |
| Audit trail | Actions tracées avec horodatage |
| Tests de sécurité | Suite automatisée (1289 tests ALFRED_PC, 32 tests comptes/préférences/conversations ALFRED_WEB, 24 tests PoC Hadoop) |

---

## 8. En cas de violation de données

1. Notification CNIL sous 72h si risque pour les personnes (Art. 33)
2. Information des personnes concernées sans délai si risque élevé (Art. 34)
3. Mesures correctives immédiates
4. Documentation de l'incident (Art. 33.5) — procédure détaillée : `docs/smsi/procedure_notification_violation_72h.md`

---

## 9. Gate — pourquoi l'inscription publique ALFRED_WEB n'est pas encore ouverte

Le code des comptes utilisateurs, préférences et conversations ALFRED_WEB est écrit, testé et fonctionnel depuis le 09/07/2026. **Il n'est volontairement pas activé pour de vrais utilisateurs.** L'AIPD-ALFRED-002 (`docs/rgpd/aipd_comptes_deploiement_public.md`), rédigée le 10/07/2026, documente précisément pourquoi : droits des personnes non implémentés côté web (§6), pas de suppression de compte, pas de rate limiting sur la connexion. Ces points doivent être traités, et l'AIPD validée par la Responsable du traitement, avant toute ouverture publique réelle.

---

## 10. Cas particuliers — ARTHUR et les données d'enfants

ARTHUR est destiné à un usage avec des enfants. Protections renforcées prévues : consentement parental obligatoire, aucune donnée partagée ou commercialisée, consentement explicite séparé pour les données de santé (Art. 9), durée de conservation minimale. **ARTHUR est actuellement en attente d'avis professionnels de santé — il n'est pas déployé.**

---

## 11. Utilisation des données à des fins de recherche (thèse professionnelle)

Dans le cadre d'une thèse professionnelle (Master Expert IT, épreuve D52), une version expérimentale privée d'ALFRED peut être utilisée comme terrain d'expérimentation, strictement séparée de toute version publique/commerciale. Tout participant est informé et consent explicitement. Les données de recherche sont anonymisées avant analyse. Le PoC Hadoop (§2.3) s'inscrit dans cette même logique de démonstration technique encadrée, sur données déjà anonymisées.

---

## 12. Publication et mise à jour

Ce document (V1.1) est la version markdown maître, mise à jour au 10/07/2026 pour refléter l'extension d'architecture de données (comptes ALFRED_WEB, MongoDB, PoC Hadoop). La version précédente publiée en PDF (`docs/security/politique_donnees_rgpd_alfred.pdf`, V1.0, mai 2026) est antérieure à cette extension et doit être régénérée à partir de ce document avant toute republication sur le site web public. En cas de modification substantielle future, notification dans l'application et/ou par email.

**Contact et réclamations :** [adresse à compléter lors de la mise en ligne] · CNIL : www.cnil.fr — 3, Place de Fontenoy, 75007 Paris.

---

## 13. Révision

| Version | Date | Auteur | Modification |
|---|---|---|---|
| 1.0 | 2026-05 | Céline Rousselot | Création (PDF `politique_donnees_rgpd_alfred.pdf`) |
| 1.1 | 2026-07-10 | Céline Rousselot (rédaction assistée Claude) | Version markdown maître. Ajout §2.2/2.3 (comptes ALFRED_WEB, PoC Hadoop), §9 (gate explicite), tableau droits des personnes différencié local/web (§6) — reflète honnêtement les gaps identifiés par l'AIPD-ALFRED-002 |

> **Cognitive Products Lab**
