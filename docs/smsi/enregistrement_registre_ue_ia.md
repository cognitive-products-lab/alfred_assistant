<!--
============================================================
PROJECT  : ALFRED / Cognitive Products Lab
BLOCK    : B20 — Sécurité, Gouvernance & Conformité
DOCUMENT : Enregistrement au Registre UE IA
TYPE     : Documentation SMSI
REF      : EU AI Act Art. 49
VERSION  : V1.1
CREATED  : 2026-06-18
UPDATED  : 2026-07-10
AUTHOR   : Céline Darras — Cognitive Products Lab
STATUS   : Approuvé
============================================================
-->
# Enregistrement au Registre UE IA

> **Référence :** EU AI Act — Art. 49 (Règlement UE 2024/1689), texte consolidé :
> https://eur-lex.europa.eu/legal-content/FR/TXT/HTML/?uri=CELEX:32024R1689
> **Version :** 1.1 — 2026-07-10
> **Propriétaire :** Cognitive Products Lab — Céline Darras
> **Statut :** Approuvé

---

## 1. Contexte réglementaire

L'Art. 49 EU AI Act impose l'enregistrement des systèmes d'IA à haut risque dans la base de données UE (EU AI Act Database).

**Calendrier d'application :**
- Août 2024 : Entrée en vigueur du règlement
- Août 2026 : Application aux systèmes d'IA à haut risque (Annexe III)
- Août 2027 : Application complète (tous les systèmes concernés)

---

## 2. Évaluation ALFRED

**Classification actuelle :** Risque limité — obligations de transparence, **Art. 50** (et non Art. 52 comme indiqué en V1.0 — correction du 10/07/2026 après vérification sur le texte consolidé anglais : l'Art. 52 du texte final concerne la procédure de notification des modèles d'IA à usage général présentant un risque systémique, Art. 50 est le bon article pour l'obligation de transparence "informer l'utilisateur qu'il interagit avec un système d'IA", applicable à un assistant conversationnel comme ALFRED).
**Obligation Art. 50 (transparence)** : applicable — ALFRED doit informer clairement l'utilisateur qu'il interagit avec une IA, dès la première interaction (Art. 50§1 et §5). Déjà couvert en pratique (mentions légales IA sur le site, `docs/gouvernance/cadre_reglementaire_CPL.md`).
**Obligation Art. 49 (enregistrement registre UE)** : Non applicable en l'état — réservé aux systèmes à haut risque (Art. 6).

**Conditions de reclassification en haut risque (Annexe III, vérifiée article par article le 10/07/2026) — à surveiller :**
- **Emploi** (Annexe III §4) : recrutement, évaluation ou surveillance de la performance/du comportement de personnes dans une relation de travail — pertinent pour **ALFRED CPL** si utilisé pour de l'aide à la décision RH/managériale (déjà signalé comme risque potentiel dans `cadre_reglementaire_CPL.md`).
- **Éducation** (Annexe III §3) : accès/admission à un établissement, évaluation des résultats d'apprentissage — pertinent pour **ARTHUR** *uniquement* si utilisé pour de l'évaluation scolaire formelle, pas pour un simple accompagnement émotionnel/ludique.
- **Services essentiels** (Annexe III §5a) : concerne les *autorités publiques* évaluant l'éligibilité à des prestations, y compris de santé — ARTHUR n'est pas positionné comme tel (compagnon, pas autorité publique décisionnaire) ; **la classification "risque élevé" d'ARTHUR dans `cadre_reglementaire_CPL.md` est à réévaluer précisément une fois son périmètre fonctionnel réel figé** (actuellement en attente d'avis professionnels de santé, non déployé) plutôt que présumée par défaut.
- Utilisation multi-utilisateurs à grande échelle, intégration dans des décisions automatisées impactant des droits fondamentaux.

---

## 3. Veille et anticipation

CPL maintient une veille réglementaire EU AI Act pour anticiper :
- L'évolution de la classification ALFRED si élargissement du périmètre
- La mise en service du registre UE IA (eu-aiact-db.ec.europa.eu)
- Les lignes directrices CNIL et ENISA sur l'AI Act

**Action préparatoire :** En cas de reclassification, préparer le dossier d'enregistrement contenant :
- Nom et description du système
- Fournisseur et représentant UE
- Finalité et cas d'usage
- Évaluation de conformité
- Coordonnées de contact

---

## 4. Révision

| Version | Date | Auteur | Modification |
|---|---|---|---|
| 1.0 | 2026-06-18 | Céline Darras | Création — veille EU AI Act Art. 49 |
| 1.1 | 2026-07-10 | Claude (assistant) | Vérification sur le texte consolidé — correction Art. 52→Art. 50 pour la transparence, vérification article par article de l'Annexe III (§2), nuance sur la classification ARTHUR (à réévaluer, pas présumée) |

> **Cognitive Products Lab — Confidentiel interne**
