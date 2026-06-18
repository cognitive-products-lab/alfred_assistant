# DPA — Data Processing Agreement (Accord de Traitement des Données)
## Sous-traitants de Cognitive Products Lab

> **Référence :** RGPD Art. 28 — Sous-traitant ; Art. 46 — Transferts internationaux  
> **Version :** 1.0 — 2026-06-18  
> **Propriétaire :** Cognitive Products Lab — Céline Darras  
> **Statut :** Approuvé (en attente signature formelle sous-traitants)

---

## 1. Cadre légal

L'Art. 28 RGPD impose qu'un contrat formel (DPA) soit conclu avec tout sous-traitant traitant des données personnelles pour le compte du responsable de traitement.

---

## 2. Inventaire des sous-traitants

### 2.1 OpenAI (API LLM)

| Champ | Détail |
|---|---|
| **Entité** | OpenAI, LLC — 3180 18th Street, San Francisco, CA 94110, USA |
| **Rôle** | Sous-traitant — traitement LLM des conversations |
| **Données transmises** | Conversations textuelles (potentiellement avec données personnelles) |
| **Localisation** | USA — transfert hors UE |
| **Base transfert** | Clauses Contractuelles Types (CCT) — Commission Européenne 2021/914 |
| **DPA OpenAI** | https://openai.com/policies/data-processing-addendum |
| **Statut** | DPA OpenAI disponible — à accepter formellement par CPL |
| **Mesures techniques** | Données non utilisées pour entraînement (via API, option Zero Data Retention) |

**Actions requises :**
- [ ] Accepter formellement le DPA OpenAI via le portail OpenAI
- [ ] Activer l'option Zero Data Retention (ZDR) sur l'API si disponible
- [ ] Documenter l'acceptation dans ce registre

### 2.2 Hébergement local (PC Alfred)

| Champ | Détail |
|---|---|
| **Entité** | Cognitive Products Lab — Infrastructure propre |
| **Rôle** | Hébergeur des données (interne — pas de DPA requis) |
| **Localisation** | France — Domicile Céline Darras |
| **Statut** | N/A (traitement interne) |

### 2.3 Futurs sous-traitants potentiels

| Sous-traitant | Service | Statut DPA |
|---|---|---|
| Ollama / LLM local | LLM local (futur — Minisforum MS-S1) | N/A (traitement local) |
| Fournisseur cloud TTS | Synthèse vocale web | À qualifier si activation |

---

## 3. Clauses minimales DPA (Art. 28.3 RGPD)

Tout DPA signé avec un sous-traitant doit inclure :
- Traitement uniquement sur instruction documentée du responsable
- Obligation de confidentialité pour les personnes autorisées
- Mesures de sécurité appropriées (Art. 32)
- Pas de recours à un autre sous-traitant sans autorisation préalable
- Assistance pour les droits des personnes (accès, effacement, portabilité)
- Suppression ou restitution des données à la fin du contrat
- Mise à disposition des informations pour démontrer le respect des obligations
- Audit possible par le responsable

---

## 4. Registre des DPA signés

| Sous-traitant | Date acceptation DPA | Version DPA | Référence |
|---|---|---|---|
| OpenAI | ⚠️ À compléter | — | https://openai.com/policies/data-processing-addendum |

---

## 5. Révision

| Version | Date | Auteur | Modification |
|---|---|---|---|
| 1.0 | 2026-06-18 | Céline Darras | Création — conformité RGPD Art. 28 |

> **Cognitive Products Lab — Confidentiel interne**
