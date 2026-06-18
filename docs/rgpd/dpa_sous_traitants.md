# Registre DPA — Accords de Traitement des Données avec Sous-traitants
## Data Processing Agreements — ALFRED / Cognitive Products Lab

---

**Référence :** DPA-ALFRED-REG-001  
**Version :** 1.0  
**Date :** 2026-06-18  
**Responsable du traitement :** Cognitive Products Lab — Céline  
**Base légale :** Art. 28 RGPD — Obligations du sous-traitant

---

## 1. Principe général

Conformément à l'Art. 28 RGPD, tout sous-traitant qui traite des données personnelles pour le compte d'ALFRED doit faire l'objet d'un accord de traitement des données (DPA) garantissant :

- Le traitement uniquement sur instruction documentée du responsable
- La confidentialité des données traitées
- La mise en place de mesures de sécurité appropriées (Art. 32)
- La notification des violations dans les meilleurs délais
- La suppression ou restitution des données en fin de contrat

---

## 2. Registre des sous-traitants actifs

### ST-01 — OpenAI, Inc.

| Champ | Valeur |
|---|---|
| **Sous-traitant** | OpenAI, Inc. |
| **Pays** | États-Unis (siège) / Traitement UE via API |
| **Services** | Inférence LLM — modèles GPT-4o/GPT-4-turbo via API REST |
| **Données transmises** | Contenu des prompts utilisateur (texte) · Peut inclure des extraits de mémoire |
| **Données sensibles Art. 9** | Possibles si l'utilisateur en inclut — filtrage par `output_filter.py` |
| **DPA signé** | Oui — DPA OpenAI (https://openai.com/policies/data-processing-addendum) |
| **Transfert hors UE** | Oui — couvert par les Clauses Contractuelles Types (CCT) UE 2021/914 |
| **Rétention données** | 0 jour (API sans rétention activée) — `"data_retention": false` dans settings |
| **Mesures complémentaires** | Filtrage PII avant envoi (`src/security/output_filter.py`) · Pas d'envoi automatique wellbeing_log |
| **Statut** | ✅ DPA publique acceptée |

### ST-02 — Anthropic, PBC

| Champ | Valeur |
|---|---|
| **Sous-traitant** | Anthropic, PBC |
| **Pays** | États-Unis |
| **Services** | Inférence LLM — Claude API (usage développement) |
| **Données transmises** | Contenu des prompts (développement/tests) |
| **DPA signé** | Oui — DPA Anthropic (https://www.anthropic.com/legal/data-processing-agreement) |
| **Transfert hors UE** | Oui — CCT UE 2021/914 |
| **Rétention données** | Politique no-training par défaut sur API |
| **Mesures complémentaires** | Usage restreint au développement — pas en production utilisateur |
| **Statut** | ✅ DPA publique acceptée |

### ST-03 — Piper TTS (local)

| Champ | Valeur |
|---|---|
| **Sous-traitant** | N/A — Traitement 100% local |
| **Services** | Synthèse vocale Text-to-Speech |
| **Données transmises** | Aucune — modèle embarqué local |
| **DPA requis** | Non |
| **Statut** | ✅ Local — pas de transfert |

### ST-04 — Ollama (local)

| Champ | Valeur |
|---|---|
| **Sous-traitant** | N/A — Traitement 100% local |
| **Services** | Inférence LLM local (modèles embarqués) |
| **Données transmises** | Aucune — serveur local uniquement |
| **DPA requis** | Non |
| **Statut** | ✅ Local — pas de transfert |

---

## 3. Sous-traitants planifiés (V2/V3)

| Sous-traitant | Services | Statut DPA |
|---|---|---|
| Prestataire hébergement HDS | Hébergement données santé ARTHUR | À établir — V3 2027 |
| Éditeur ARTHUR | Développement module pédiatrique | À établir — V3 2027 |

---

## 4. Mesures de contrôle des sous-traitants

### 4.1 Filtrage avant envoi API

Le module `src/security/output_filter.py` filtre les données personnelles identifiantes avant toute transmission à une API externe :
- Suppression des noms propres détectés
- Masquage des numéros (téléphone, SS, email)
- Avertissement si données de santé détectées dans le prompt

### 4.2 Paramétrage API

Pour OpenAI et Anthropic, la configuration `data/settings/device_settings.json` inclut :
- `"store_conversations": false` — désactivation de la mémorisation côté API
- `"training_opt_out": true` — opt-out du réentraînement

### 4.3 Audit annuel

Chaque sous-traitant fait l'objet d'une revue annuelle :
- Vérification de la DPA en vigueur
- Vérification du statut de certification (ISO 27001, SOC 2)
- Vérification de l'absence de sous-sous-traitants non déclarés

---

## 5. Procédure en cas de violation par un sous-traitant

1. Le sous-traitant notifie le responsable du traitement **sans délai** (Art. 28.3.f)
2. Le responsable du traitement évalue l'impact sur les personnes concernées
3. Si risque élevé : notification CNIL sous 72h (voir procédure RGPD-10)
4. Si risque très élevé : notification de la personne concernée (Art. 34)

---

## 6. Revue et mise à jour

| | |
|---|---|
| **Validé par** | Céline — Responsable du traitement |
| **Date** | 2026-06-18 |
| **Prochaine revue** | 2027-06-18 ou lors de l'ajout d'un nouveau sous-traitant |

---

*Document confidentiel interne — Cognitive Products Lab*
