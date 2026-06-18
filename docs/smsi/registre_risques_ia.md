# Système de Gestion des Risques IA

> **Référence :** EU AI Act — Art. 9 (Règlement UE 2024/1689)  
> **Version :** 1.0 — 2026-06-18  
> **Propriétaire :** Cognitive Products Lab — Céline Darras  
> **Statut :** Approuvé

---

## 1. Classification ALFRED — EU AI Act

**Niveau de risque :** Risque Limité (Art. 52)  
**Justification :** Assistant IA personnel, usage mono-utilisateur V1, aucune décision automatique impactant des droits fondamentaux, pas de biométrie, pas d'infrastructure critique.

**Obligations applicables :**
- Art. 13 : Transparence envers l'utilisateur ✅ (déclaration nature IA)
- Art. 14 : Supervision humaine HITL ✅ (voir `hitl_procedure.md`)
- Art. 52 : Obligation d'information ✅ (onboarding utilisateur)

---

## 2. Registre des risques IA

| ID | Risque IA | Probabilité | Impact | Niveau | Mesure de mitigation |
|---|---|---|---|---|---|
| RIA-001 | Biais dans les réponses (données d'entraînement LLM) | Modérée | Modéré | **Moyen** | Supervision humaine, diversification sources |
| RIA-002 | Hallucinations LLM (informations fausses) | Modérée | Modéré | **Moyen** | Transparence limites IA, vérification recommandée |
| RIA-003 | Manipulation émotionnelle involontaire | Faible | Élevé | **Moyen** | Mode bien-être, limites déclarées, HITL |
| RIA-004 | Sur-dépendance utilisateur à l'IA | Faible | Modéré | **Faible** | Promotion autonomie, suggestions consultation experts |
| RIA-005 | Fuite données via prompt injection | Très faible | Élevé | **Moyen** | `output_filter.py`, isolation données sensibles |
| RIA-006 | Utilisation non conforme EU AI Act | Très faible | Élevé | **Faible** | Veille réglementaire, conformité proactive |

---

## 3. Processus de gestion des risques IA

1. **Identification** : Revue trimestrielle des risques IA émergents
2. **Évaluation** : Probabilité × Impact (matrice 4×4)
3. **Traitement** : Mesures de mitigation documentées ici
4. **Monitoring** : Surveillance continue via `behavioral_detector.py`
5. **Révision** : Mise à jour annuelle ou si changement de modèle LLM

---

## 4. Révision

| Version | Date | Auteur | Modification |
|---|---|---|---|
| 1.0 | 2026-06-18 | Céline Darras | Création — conformité EU AI Act Art. 9 |

> **Cognitive Products Lab — Confidentiel interne**
