<!--
============================================================
PROJECT  : ALFRED / Cognitive Products Lab
BLOCK    : B20 — Sécurité, Gouvernance & Conformité
DOCUMENT : Plan de Continuité d'Activité (PCA)
TYPE     : Documentation SMSI
REF      : ISO/IEC 27001:2022 — A.5.30
VERSION  : V1.0
CREATED  : 2026-06-18
UPDATED  : 2026-06-18
AUTHOR   : Céline Darras — Cognitive Products Lab
STATUS   : Approuvé
============================================================
-->
# Plan de Continuité d'Activité (PCA)

> **Référence :** ISO/IEC 27001:2022 — Contrôle A.5.30  
> **Version :** 1.0 — 2026-06-18  
> **Propriétaire :** Cognitive Products Lab — Céline Darras  
> **Statut :** Approuvé

---

## 1. Objectif

Garantir la continuité des opérations ALFRED en cas d'incident majeur et définir les modalités de reprise d'activité.

---

## 2. Scénarios de sinistre

| Scénario | Probabilité | Impact | Priorité |
|---|---|---|---|
| Panne matérielle PC Alfred | Modérée | Élevé | P1 |
| Corruption données/chiffrement | Faible | Critique | P1 |
| Ransomware | Très faible | Critique | P1 |
| Panne réseau | Modérée | Modéré | P2 |
| Perte accès OpenAI API | Faible | Modéré | P2 |
| Sinistre physique (incendie, vol) | Très faible | Critique | P1 |
| Compromission des clés | Très faible | Critique | P1 |

---

## 3. Objectifs de reprise

| Indicateur | Valeur cible |
|---|---|
| **RTO** (délai reprise) | 4h pour P1, 8h pour P2 |
| **RPO** (perte données max) | 24h (sauvegarde quotidienne) |
| **MTPD** (durée max perturbation) | 48h |

---

## 4. Ressources de reprise

| Ressource | Localisation | État |
|---|---|---|
| Sauvegarde données (LaCie) | Domicile — rangement sécurisé | ✅ Disponible |
| Code source (GitHub) | Cloud — dépôt privé | ✅ Disponible |
| Clés cryptographiques hors-ligne | Stockage physique sécurisé | ✅ Disponible |
| PC de secours (si PC Alfred indisponible) | PC portable personnel | ✅ Disponible |
| Accès OpenAI API de secours | Compte backup préparé | 🟡 Recommandé |

---

## 5. Procédures de reprise par scénario

### Panne matérielle PC Alfred
1. Utiliser PC portable de secours
2. Restaurer depuis LaCie + cloner Git
3. Réinstaller environnement Python (`pip install -r requirements.txt`)
4. Restaurer clés cryptographiques
5. Valider via tests sécurité

### Corruption / Ransomware
1. Isoler immédiatement le PC du réseau
2. NE PAS payer la rançon
3. Restaurer depuis sauvegarde LaCie non chiffrée (hors-ligne)
4. Scanner le PC de secours avant toute restauration
5. Documenter incident et notifier CNIL si données exposées

### Perte accès OpenAI API
1. Activer mode dégradé ALFRED (LLM local Ollama si disponible)
2. Contacter support OpenAI
3. Utiliser clé API de secours

---

## 6. Contacts d'urgence

| Contact | Rôle | Coordonnées |
|---|---|---|
| Céline Darras | Fondatrice / RSSI | darkmiroir@gmail.com |
| CERT-FR | Incidents cyber | cert-fr.cossi@ssi.gouv.fr |
| CNIL | Violations données | https://notifications.cnil.fr |

---

## 7. Tests PCA

Voir `docs/smsi/tests_pca.md` pour le plan et les résultats de tests.

---

## 8. Révision

| Version | Date | Auteur | Modification |
|---|---|---|---|
| 1.0 | 2026-06-18 | Céline Darras | Création PCA — conformité ISO A.5.30 |

> **Cognitive Products Lab — Confidentiel interne**
