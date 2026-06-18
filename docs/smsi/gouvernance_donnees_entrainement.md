# Gouvernance des Données d'Entraînement

> **Référence :** EU AI Act — Art. 10 (Règlement UE 2024/1689)  
> **Version :** 1.0 — 2026-06-18  
> **Propriétaire :** Cognitive Products Lab — Céline Darras  
> **Statut :** Approuvé

---

## 1. Contexte

L'Art. 10 EU AI Act impose une gouvernance des données d'entraînement pour les systèmes d'IA à haut risque. ALFRED étant classé à risque limité, cet article n'est pas directement obligatoire mais CPL applique ses principes par démarche proactive.

---

## 2. Architecture des données ALFRED

ALFRED n'entraîne pas de modèle IA en propre. Il s'appuie sur :

| Composant | Source | Gouvernance |
|---|---|---|
| **LLM** | OpenAI GPT (API) | Gouvernance OpenAI — données non utilisées pour entraînement via API |
| **Mémoire épisodique** | Interactions utilisateur ALFRED | Données personnelles — RGPD Art. 6 |
| **Profil utilisateur** | Saisie utilisateur | Données personnelles — RGPD Art. 6 |
| **Paramètres comportementaux** | Configuration CPL | Propriété intellectuelle CPL |

---

## 3. Principes de gouvernance des données

### 3.1 Données OpenAI (LLM)
- CPL n'utilise l'API que pour inférence (pas d'entraînement)
- Option Zero Data Retention (ZDR) à activer sur le compte API
- Les conversations ne sont pas utilisées par OpenAI pour entraîner ses modèles via l'API (selon les CGU API)
- Référence DPA OpenAI : `docs/smsi/dpa_sous_traitants.md`

### 3.2 Données utilisateur ALFRED
- Collecte minimale : uniquement ce qui est nécessaire à la personnalisation
- Pas de données utilisateur transmises à des tiers sans consentement explicite
- Chiffrement AES-256 au repos
- Droits RGPD complets (accès, rectification, effacement, portabilité)

### 3.3 Si entraînement futur (V2/V3)
En cas de fine-tuning ou d'entraînement local sur modèle Ollama :
- Inventaire des datasets utilisés
- Vérification des licences et droits
- Évaluation des biais potentiels
- Documentation dans ce registre

---

## 4. Révision

| Version | Date | Auteur | Modification |
|---|---|---|---|
| 1.0 | 2026-06-18 | Céline Darras | Création — conformité EU AI Act Art. 10 |

> **Cognitive Products Lab — Confidentiel interne**
