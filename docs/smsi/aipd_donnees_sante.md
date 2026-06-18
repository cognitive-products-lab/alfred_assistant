<!--
============================================================
PROJECT  : ALFRED / Cognitive Products Lab
BLOCK    : B20 — Sécurité, Gouvernance & Conformité
DOCUMENT : Analyse d'Impact AIPD — Données de Santé
TYPE     : Documentation SMSI
REF      : RGPD Art. 35
VERSION  : V1.0
CREATED  : 2026-06-18
UPDATED  : 2026-06-18
AUTHOR   : Céline Darras — Cognitive Products Lab
STATUS   : Approuvé
============================================================
-->
# Analyse d'Impact relative à la Protection des Données (AIPD)
## Données de santé et données sensibles — ALFRED

> **Référence :** RGPD Art. 35 — Analyse d'impact obligatoire (données sensibles, Art. 9)  
> **Version :** 1.0 — 2026-06-18  
> **Responsable :** Céline Darras — DPO de fait, Cognitive Products Lab  
> **Statut :** Approuvé

---

## 1. Contexte et obligation

L'Art. 35 RGPD impose une AIPD lorsque le traitement est susceptible d'engendrer un risque élevé pour les droits et libertés des personnes, notamment :
- Traitement à grande échelle de données sensibles (Art. 9) — données de santé, données biométriques
- Traitement avec surveillance systématique

**ALFRED traite des données pouvant inclure :**
- Données de bien-être psychologique et émotionnel (wellbeing_log.json)
- Données comportementales et conversationnelles personnelles
- Potentiellement des informations de santé partagées par l'utilisateur

---

## 2. Description du traitement analysé

| Champ | Détail |
|---|---|
| **Traitement** | Assistance conversationnelle IA personnalisée avec mémoire épisodique |
| **Responsable** | Cognitive Products Lab (Céline Darras) |
| **Finalité** | Assistance personnelle, bien-être, productivité utilisateur |
| **Base légale** | Consentement explicite (Art. 6.1.a + Art. 9.2.a) |
| **Données sensibles** | Données de bien-être/santé mentale partagées, données comportementales |
| **Personnes concernées** | Utilisateurs ALFRED (actuellement : Céline Darras — usage personnel) |
| **Volume** | Faible — usage mono-utilisateur V1 |
| **Durée de conservation** | Définie par l'utilisateur via commandes /forget |
| **Sous-traitants** | OpenAI API (LLM) — DPA à formaliser |

---

## 3. Évaluation des risques

### 3.1 Risques identifiés

| Risque | Probabilité | Gravité | Niveau |
|---|---|---|---|
| Accès non autorisé aux données de santé | Faible | Élevée | **Modéré** |
| Fuite vers sous-traitant (OpenAI) | Faible | Élevée | **Modéré** |
| Utilisation détournée des données émotionnelles | Très faible | Élevée | **Faible** |
| Perte/destruction accidentelle | Très faible | Modérée | **Faible** |
| Profilage non consenti | Très faible | Élevée | **Faible** |

### 3.2 Mesures techniques en place

| Mesure | Fichier/Mécanisme |
|---|---|
| Chiffrement AES-256 des données au repos | `src/security/encryption_service.py` |
| Contrôle d'accès MFA obligatoire | `src/security/mfa_manager.py` |
| Journalisation sécurisée | `src/security/audit_trail.py` |
| Détection d'anomalies comportementales | `src/security/behavioral_detector.py` |
| Minimisation des données | Conception ALFRED (mémoire contextuelle, pas de stockage brut LLM) |
| Droit d'effacement opérationnel | Commandes /forget |
| Filtrage sorties (DLP) | `src/security/output_filter.py` |

---

## 4. Mesures de protection spécifiques données sensibles

1. **Consentement explicite renforcé :** L'utilisateur doit confirmer explicitement le traitement de toute donnée de santé (formulaire de consentement Art. 9 — voir `docs/gouvernance/consentement_art9.md`)
2. **Principe de minimisation :** ALFRED ne stocke que ce qui est nécessaire à la personalisation ; les données de santé ne sont pas indexées séparément
3. **Chiffrement de bout en bout :** Toutes les données sensibles sont chiffrées avant stockage
4. **Droit d'accès facilité :** Export complet via `export_command.py`
5. **Transferts internationaux limités :** OpenAI API est le seul sous-traitant hors UE — DPA à formaliser

---

## 5. Évaluation — Risques résiduels

Après application des mesures techniques :

| Risque résiduel | Niveau |
|---|---|
| Accès non autorisé | **Faible** (MFA + chiffrement) |
| Fuite sous-traitant | **Faible à modéré** (en attente DPA formelle OpenAI) |
| Ensemble des risques | **Acceptable pour usage V1 mono-utilisateur** |

---

## 6. Conclusion

Le traitement ALFRED peut être poursuivi sous réserve :
1. ✅ Chiffrement AES-256 en place
2. ✅ MFA obligatoire
3. ⚠️ DPA formelle OpenAI à signer (RGPD-09)
4. ⚠️ Formulaire de consentement Art. 9 à finaliser (RGPD-06)

**Consultation CNIL préalable :** Non requise à ce stade (risques résiduels acceptables, volume faible, usage personnel V1). À reconsidérer lors du passage en mode multi-utilisateurs.

---

## 7. Révision

| Version | Date | Auteur | Modification |
|---|---|---|---|
| 1.0 | 2026-06-18 | Céline Darras | Création AIPD initiale — conformité RGPD Art. 35 |

> **Cognitive Products Lab — Confidentiel interne**
