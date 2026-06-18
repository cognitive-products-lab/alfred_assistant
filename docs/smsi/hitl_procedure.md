<!--
============================================================
PROJECT  : ALFRED / Cognitive Products Lab
BLOCK    : B20 — Sécurité, Gouvernance & Conformité
DOCUMENT : Supervision Humaine — Human in the Loop (HITL)
TYPE     : Documentation SMSI
REF      : EU AI Act Art. 14
VERSION  : V1.0
CREATED  : 2026-06-18
UPDATED  : 2026-06-18
AUTHOR   : Céline Darras — Cognitive Products Lab
STATUS   : Approuvé
============================================================
-->
# Supervision Humaine — Human in the Loop (HITL)

> **Référence :** EU AI Act — Art. 14 (Règlement UE 2024/1689)  
> **Version :** 1.0 — 2026-06-18  
> **Propriétaire :** Cognitive Products Lab — Céline Darras  
> **Statut :** Approuvé

---

## 1. Contexte EU AI Act

L'Art. 14 impose que les systèmes d'IA à haut risque permettent une supervision humaine effective. ALFRED est classé à **risque limité** (Art. 52) — obligations de transparence — mais CPL applique le principe HITL par défaut pour garantir une IA responsable.

---

## 2. Principe HITL dans ALFRED

ALFRED est conçu pour **augmenter** l'utilisateur, jamais pour décider à sa place sur des sujets critiques.

### 2.1 Décisions exclusivement humaines (ALFRED ne décide pas)

| Domaine | Exemple | Rôle ALFRED |
|---|---|---|
| Santé et médical | Diagnostic, traitement, médicaments | Informer uniquement, rappeler de consulter un médecin |
| Juridique | Décisions légales, contrats importants | Informer, suggérer de consulter un avocat |
| Financier critique | Investissements majeurs, virements | Informer, ne jamais exécuter |
| Urgences | Urgences médicales, sécurité | Orienter vers les secours (15/17/18/112) |
| Données personnelles | Suppression, partage | Demander confirmation explicite |

### 2.2 Contrôles HITL implémentés

| Contrôle | Implémentation | Fichier |
|---|---|---|
| Confirmation explicite avant actions irréversibles | Prompt de confirmation | `src/conversation/` |
| Mode push-to-talk (écoute active) | Écoute manuelle uniquement | `config/device_settings.json` |
| Filtrage des sorties sensibles | DLP automatique | `src/security/output_filter.py` |
| Désactivation fonctionnalités | Via `features.json` | `config/features.json` |
| Transparence sur nature IA | Déclaration dans onboarding | EU AI Act Art. 13 ✅ |

---

## 3. Limitations déclarées

ALFRED déclare explicitement à l'utilisateur :
- Il est un assistant IA, pas un professionnel (médecin, avocat, thérapeute)
- Ses réponses peuvent contenir des erreurs
- Pour toute décision importante, une validation humaine qualifiée est recommandée

---

## 4. Révision

| Version | Date | Auteur | Modification |
|---|---|---|---|
| 1.0 | 2026-06-18 | Céline Darras | Création — conformité EU AI Act Art. 14 |

> **Cognitive Products Lab — Confidentiel interne**
